#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FRED 시리즈별 전체 이력 수집기 (시계열 저장 레이어)
──────────────────────────────────────────────────────────
• 대상: fred_fetch.py 의 REG 레지스트리 중 API 시리즈 전체 (calculated 제외)
• 산출물 (모두 data/series/ 하위):
    fred/{SERIES_ID}.csv        date,value   시리즈별 전체 이력
    fred_meta.csv               시리즈별 실측 메타
    _revisions.csv              재조회 구간에서 감지된 값 개정 로그 (append)
    fred_vintage/{ID}.csv       --vintages 사용 시, 개정 이력 (realtime 구간)
• 기존 fred_fetch.py 와 독립 실행된다. REG 는 import 하지 않고 AST 로 읽는다
  (fred_fetch.py 는 import 시 API 키가 없으면 종료하고 전역 날짜를 계산하므로).
• 결측(".")은 결측으로 저장한다. 보간·직전값 채움 없음.

사용법:
    export FRED_API_KEY="..."
    python scripts/fred_series_collect.py                 # 백필(최초) 또는 증분
    python scripts/fred_series_collect.py --vintages      # + 개정 이력(2단계)
    python scripts/fred_series_collect.py --series DGS10 UNRATE   # 일부만

종료코드: 0=전체 성공, 1=하나 이상 실패(성공분은 저장됨), 2=설정 오류
"""

import argparse
import ast
import math
import os
import re
import sys
import time
from datetime import date, datetime, timezone
from pathlib import Path

import pandas as pd
import requests

# ═══════════════════════════════════════════════════════════
# 1. 설정
# ═══════════════════════════════════════════════════════════

FRED_API_ROOT = "https://api.stlouisfed.org/fred"
OBS_LIMIT = 100000           # FRED observations 최대 limit
REVISIT_OBS = 12             # 증분 시 재조회할 최근 관측 개수
REQUEST_DELAY = 0.6          # FRED 한도 120 req/min 이하 유지
MAX_RETRIES = 4              # 429/5xx/연결 오류 재시도 횟수
RETRY_BACKOFF = 2.0          # 지수 백오프 밑 (2, 4, 8, 16초)
SHORT_HISTORY_YEARS = 10     # 미만이면 short_history=True

# 개정 이력(vintage) 대상. 모두 REG 에 존재하는 시리즈만 둔다.
VINTAGE_SERIES = ["CPIAUCSL", "CPILFESL", "PCEPILFE", "UNRATE", "PAYEMS", "GDPC1"]
VINTAGE_YEARS = 10           # 관측 구간 제한(용량 통제). 전체 이력은 과다.

BASE_DIR = Path(__file__).resolve().parent.parent
FRED_FETCH_PATH = BASE_DIR / "fred_fetch.py"
DEFAULT_OUT = BASE_DIR / "data" / "series"

SERIES_COLUMNS = ["date", "value"]
VINTAGE_COLUMNS = ["date", "value", "realtime_start", "realtime_end"]
REVISION_COLUMNS = ["series_id", "date", "old", "new", "detected_at"]
META_COLUMNS = [
    "series_id", "title", "units", "frequency", "seasonal_adjustment",
    "series_type", "observation_start", "observation_end", "years_available",
    "last_updated", "vintage", "probed_at", "short_history",
]
SERIES_TYPES = {"level", "rate", "spread", "fx", "price_index", "count"}

# ── series_type 분류 (명시 매핑, 추정 아님) ──
# rate: 수익률·금리·비율(%) / spread: 두 금리의 차 또는 차로 정의된 지표
# fx: 환율·달러지수 / price_index: 물가·가격 지수 / count: 인원·건수·호수·대수
# level: 그 밖의 수준값(금액, 지수형 활동·심리지표, 현물가격, 주가지수 등)
SERIES_TYPE = {
    # 금리·채권
    "T10Y2Y": "spread", "DFII10": "rate", "T10YIE": "spread", "T5YIE": "spread",
    "T5YIFR": "rate", "DGS2": "rate", "DGS10": "rate", "DGS30": "rate",
    "TB3MS": "rate", "DFF": "rate", "FEDFUNDS": "rate", "SOFR": "rate",
    "AAA": "rate", "BAA": "rate", "BAA10Y": "spread", "T10Y3M": "spread",
    "MORTGAGE30US": "rate",
    # 리스크·신용·금융여건
    "VIXCLS": "level", "BAMLH0A0HYM2": "spread", "TOTBKCR": "level",
    "NFCI": "level", "STLFSI4": "level", "KCFSI": "level",
    # 고용
    "CFNAI": "level", "UNRATE": "rate", "PAYEMS": "count", "ICSA": "count",
    "CCSA": "count", "JTSJOL": "count", "JTSQUR": "rate", "CIVPART": "rate",
    "LNS11300060": "rate", "SAHMREALTIME": "rate", "MANEMP": "count",
    # 물가
    "CES0500000003": "level", "CPIAUCSL": "price_index", "CPIAUCNS": "price_index",
    "CPILFESL": "price_index", "PCEPI": "price_index", "PCEPILFE": "price_index",
    "PPIFIS": "price_index", "MICH": "rate", "CSUSHPINSA": "price_index",
    "PALLFNFINDEXM": "price_index",
    # 성장·활동
    "GDP": "level", "GDPC1": "level", "INDPRO": "level", "RSAFS": "level",
    "DGORDER": "level", "CMRMTSPL": "level", "UMCSENT": "level", "TCU": "rate",
    "ISRATIO": "level", "AMTMNO": "level", "PSAVERT": "rate", "TOTALSA": "count",
    "DSPIC96": "level", "PCEC96": "level",
    # 통화·유동성
    "M2SL": "level", "WALCL": "level", "TREAST": "level", "WSHOMCB": "level",
    "RRPONTSYD": "level", "WTREGEN": "level", "TOTRESNS": "level",
    "BOGMBASE": "level",
    # 주택
    "HOUST": "count", "PERMIT": "count", "EXHOSLUSM495S": "count",
    # 대외·재정
    "NETFI": "level", "FYFSD": "level", "BOPGSTB": "level", "EXPGS": "level",
    "IMPGS": "level",
    # 환율·달러
    "DEXKOUS": "fx", "DTWEXBGS": "fx", "DTWEXAFEGS": "fx", "DTWEXEMEGS": "fx",
    "DEXJPUS": "fx", "DEXCHUS": "fx",
    # 원자재 (현물가격 = level, 지수형 = price_index)
    "NASDAQQGLDI": "level", "DCOILWTICO": "level", "DHHNGSP": "level",
    "PCOPPUSDM": "level", "PIORECRUSDM": "level", "PSOYBUSDM": "level",
    "PALUMUSDM": "level", "PNICKUSDM": "level", "PWHEAMTUSDM": "level",
    "PMAIZMTUSDM": "level",
    # 주가
    "SP500": "level",
    # 신용·연체
    "DRCCLACBS": "rate", "DRSFRMACBS": "rate", "BUSLOANS": "level",
    "CONSUMER": "level",
    # 한국
    "IRSTCI01KRM156N": "rate", "IRLTLT01KRM156N": "rate",
    "LRHUTTTTKRM156S": "rate", "KORLOLITOAASTSAM": "level",
    "NGDPRSAXDCKRQ": "level",
}

# ═══════════════════════════════════════════════════════════
# 2. 레지스트리 / 비밀값 처리
# ═══════════════════════════════════════════════════════════


def load_registry(path=FRED_FETCH_PATH):
    """fred_fetch.py 를 실행하지 않고 REG 리터럴만 AST 로 읽는다."""
    tree = ast.parse(Path(path).read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                getattr(t, "id", None) == "REG" for t in node.targets):
            return ast.literal_eval(node.value)
    raise RuntimeError(f"REG not found in {path}")


def registry_series_ids(registry):
    """API 로 수집하는 시리즈 ID (파생 calculated 제외), REG 순서 유지."""
    return [sid for sid, m in registry.items() if m.get("tf") != "calculated"]


_KEY_PARAM_RE = re.compile(r"(api_key=)[^&\s'\"]+", re.IGNORECASE)


def redact(text, api_key=None):
    """로그·예외 문자열에서 API 키를 제거한다."""
    s = str(text)
    if api_key:
        s = s.replace(api_key, "***")
    return _KEY_PARAM_RE.sub(r"\1***", s)


# ═══════════════════════════════════════════════════════════
# 3. HTTP 클라이언트 (재시도 정책)
# ═══════════════════════════════════════════════════════════


class FredError(Exception):
    """키가 제거된 메시지만 담는 예외."""

    def __init__(self, message, status=None):
        super().__init__(message)
        self.status = status


class FredClient:
    def __init__(self, api_key, session=None, sleep=time.sleep,
                 delay=REQUEST_DELAY, max_retries=MAX_RETRIES,
                 backoff=RETRY_BACKOFF):
        self.api_key = api_key
        self.session = session or requests.Session()
        self.sleep = sleep
        self.delay = delay
        self.max_retries = max_retries
        self.backoff = backoff
        self.calls = 0

    def get(self, endpoint, **params):
        """429/5xx/연결오류는 지수 백오프 재시도, 그 밖의 4xx 는 즉시 실패."""
        url = f"{FRED_API_ROOT}/{endpoint}"
        q = dict(params, api_key=self.api_key, file_type="json")
        last = None
        for attempt in range(1, self.max_retries + 1):
            if self.calls:
                self.sleep(self.delay)
            self.calls += 1
            try:
                r = self.session.get(url, params=q, timeout=60)
            except requests.RequestException as e:
                last = FredError(f"{type(e).__name__}: {redact(e, self.api_key)}")
            else:
                status = r.status_code
                if status == 200:
                    try:
                        return r.json()
                    except ValueError:
                        raise FredError("invalid JSON response", status)
                msg = _error_message(r, self.api_key)
                if status == 429 or status >= 500:
                    last = FredError(f"HTTP {status}: {msg}", status)
                else:
                    raise FredError(f"HTTP {status}: {msg}", status)
            if attempt < self.max_retries:
                wait = self.backoff ** attempt
                print(f"    [RETRY {attempt}/{self.max_retries}] {endpoint}: "
                      f"{last} → {wait:.0f}s")
                self.sleep(wait)
        raise last


def _error_message(resp, api_key):
    try:
        msg = resp.json().get("error_message", "")
    except ValueError:
        msg = ""
    return redact(msg or (resp.text or "")[:200], api_key)


# ═══════════════════════════════════════════════════════════
# 4. 순수 함수 (파싱·병합) — 테스트 대상
# ═══════════════════════════════════════════════════════════


def parse_value(v):
    """FRED 값 문자열 → float. "." 및 빈값은 결측(NaN)."""
    if v is None:
        return math.nan
    s = str(v).strip()
    if s in ("", "."):
        return math.nan
    return float(s)


def obs_to_frame(observations):
    df = pd.DataFrame(
        [(o["date"], parse_value(o.get("value"))) for o in observations],
        columns=SERIES_COLUMNS,
    )
    df["value"] = df["value"].astype("float64")
    df = df.drop_duplicates("date", keep="last").sort_values("date")
    return df.reset_index(drop=True)


def read_series(path):
    if not Path(path).exists():
        return pd.DataFrame({"date": pd.Series(dtype=str),
                             "value": pd.Series(dtype="float64")})
    df = pd.read_csv(path, dtype={"date": str, "value": "float64"},
                     keep_default_na=False, na_values=[""])
    return df[SERIES_COLUMNS]


def _same(a, b):
    if isinstance(a, float) and isinstance(b, float) and math.isnan(a) and math.isnan(b):
        return True
    return a == b


def _fmt(v):
    return "" if v is None or (isinstance(v, float) and math.isnan(v)) else repr(float(v))


def merge_series(stored, fetched, series_id, detected_at):
    """저장본과 조회본을 병합한다.

    - 저장본에 없는 날짜: 추가
    - 겹치는 날짜에서 값이 다르면(결측↔값 포함): 조회본으로 갱신 + 개정 기록
    - 저장본에만 있는 날짜: 유지(삭제하지 않음), 경고 대상으로 반환
    반환: (merged_df, revisions(list[dict]), dropped_dates(list[str]))
    """
    old = dict(zip(stored["date"], stored["value"]))
    revisions = []
    for d, v in zip(fetched["date"], fetched["value"]):
        if d in old and not _same(old[d], v):
            revisions.append({"series_id": series_id, "date": d,
                              "old": _fmt(old[d]), "new": _fmt(v),
                              "detected_at": detected_at})
    fetched_dates = set(fetched["date"])
    start = fetched["date"].min() if len(fetched) else None
    dropped = [d for d in stored["date"]
               if start is not None and d >= start and d not in fetched_dates]
    merged = dict(old)
    merged.update(zip(fetched["date"], fetched["value"]))
    out = pd.DataFrame(sorted(merged.items()), columns=SERIES_COLUMNS)
    out["value"] = out["value"].astype("float64")
    return out, revisions, dropped


def incremental_start(stored, revisit=REVISIT_OBS):
    """증분 조회 시작일: 저장된 최근 revisit 개 관측의 첫 날짜. 저장본 없으면 None(전체)."""
    if stored.empty:
        return None
    dates = sorted(stored["date"])
    return dates[-revisit] if len(dates) >= revisit else dates[0]


def years_available(df):
    """실제 저장된 비결측 관측의 첫~끝 기간(년)."""
    v = df.dropna(subset=["value"])
    if v.empty:
        return 0.0
    d0 = date.fromisoformat(v["date"].iloc[0])
    d1 = date.fromisoformat(v["date"].iloc[-1])
    return round((d1 - d0).days / 365.25, 1)


def write_csv_if_changed(df, path):
    """to_csv 결과가 기존 파일과 같으면 쓰지 않는다. 변경 여부 반환."""
    path = Path(path)
    text = df.to_csv(index=False, lineterminator="\n")
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8", lineterminator="\n")
    return True


def append_revisions(revisions, path):
    if not revisions:
        return
    path = Path(path)
    df = pd.DataFrame(revisions, columns=REVISION_COLUMNS)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, mode="a", header=not path.exists(), index=False,
              encoding="utf-8", lineterminator="\n")


# ═══════════════════════════════════════════════════════════
# 5. FRED 호출 래퍼
# ═══════════════════════════════════════════════════════════


def fetch_meta(client, series_id):
    js = client.get("series", series_id=series_id)
    s = (js.get("seriess") or [None])[0]
    if not s:
        raise FredError("empty series metadata")
    return s


def fetch_observations(client, series_id, start=None, **extra):
    """observations 전체를 페이지 단위로 받는다 (sort asc, units 기본=lin)."""
    out, offset = [], 0
    while True:
        params = dict(series_id=series_id, sort_order="asc",
                      limit=OBS_LIMIT, offset=offset, **extra)
        if start:
            params["observation_start"] = start
        js = client.get("series/observations", **params)
        obs = js.get("observations", [])
        out.extend(obs)
        count = int(js.get("count", len(out)))
        offset += len(obs)
        if not obs or offset >= count:
            return out


def vintage_frame(observations):
    rows = [(o["date"], parse_value(o.get("value")), o["realtime_start"],
             o["realtime_end"]) for o in observations]
    df = pd.DataFrame(rows, columns=VINTAGE_COLUMNS)
    df["value"] = df["value"].astype("float64")
    df = df.drop_duplicates(["date", "realtime_start"], keep="last")
    return df.sort_values(["date", "realtime_start"]).reset_index(drop=True)


# ═══════════════════════════════════════════════════════════
# 6. 메인 흐름
# ═══════════════════════════════════════════════════════════


def build_meta_row(series_id, meta, stored, probed_at):
    years = years_available(stored)
    return {
        "series_id": series_id,
        "title": meta.get("title", ""),
        "units": meta.get("units", ""),
        "frequency": meta.get("frequency_short", ""),
        "seasonal_adjustment": meta.get("seasonal_adjustment_short", ""),
        "series_type": SERIES_TYPE.get(series_id, ""),
        "observation_start": meta.get("observation_start", ""),
        "observation_end": meta.get("observation_end", ""),
        "years_available": years,
        "last_updated": meta.get("last_updated", ""),
        "vintage": "Y" if series_id in VINTAGE_SERIES else "N",
        "probed_at": probed_at,
        "short_history": years < SHORT_HISTORY_YEARS,
    }


def read_meta(path):
    if not Path(path).exists():
        return pd.DataFrame(columns=META_COLUMNS)
    return pd.read_csv(path, dtype=str, keep_default_na=False)


def collect(series_ids, out_dir, client, now=None, vintages=False,
            vintage_series=None, today=None):
    """시리즈별로 독립 수집. 실패는 기록만 하고 다음 시리즈로 진행한다.
    반환: 실패 목록 list[(series_id, stage, message)]"""
    out_dir = Path(out_dir)
    now = now or datetime.now(timezone.utc)
    stamp = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    today = today or now.date()
    series_dir = out_dir / "fred"
    meta_path = out_dir / "fred_meta.csv"
    rev_path = out_dir / "_revisions.csv"

    meta_df = read_meta(meta_path)
    meta_rows = {r["series_id"]: r for r in meta_df.to_dict("records")}
    failures = []

    for i, sid in enumerate(series_ids, 1):
        path = series_dir / f"{sid}.csv"
        try:
            meta = fetch_meta(client, sid)
            stored = read_series(path)
            start = incremental_start(stored)
            mode = "증분" if start else "백필"
            fetched = obs_to_frame(fetch_observations(client, sid, start))
            if stored.empty and fetched.empty:
                raise FredError("no observations returned")
            merged, revs, dropped = merge_series(stored, fetched, sid, stamp)
            changed = write_csv_if_changed(merged, path)
            append_revisions(revs, rev_path)
            meta_rows[sid] = build_meta_row(sid, meta, merged, stamp)
            n_missing = int(merged["value"].isna().sum())
            print(f"  [{i}/{len(series_ids)}] {sid} {mode} start={start or '-'} "
                  f"rows={len(merged)} missing={n_missing} revisions={len(revs)}"
                  f"{' (변경)' if changed else ''}")
            if dropped:
                print(f"    [WARN] {sid}: 재조회 응답에 없는 저장 날짜 {len(dropped)}건 유지 "
                      f"(예: {dropped[0]})")
        except Exception as e:  # 시리즈 단위 격리
            msg = redact(e, client.api_key)
            failures.append((sid, "series", msg))
            print(f"  [{i}/{len(series_ids)}] {sid} 실패: {msg}")

    if vintages:
        vdir = out_dir / "fred_vintage"
        vstart = date(today.year - VINTAGE_YEARS, 1, 1).isoformat()
        for sid in (vintage_series or VINTAGE_SERIES):
            try:
                obs = fetch_observations(client, sid, vstart,
                                         realtime_start="1776-07-04",
                                         realtime_end="9999-12-31")
                vdf = vintage_frame(obs)
                write_csv_if_changed(vdf, vdir / f"{sid}.csv")
                print(f"  [vintage] {sid} rows={len(vdf)} (obs≥{vstart})")
            except Exception as e:
                msg = redact(e, client.api_key)
                failures.append((sid, "vintage", msg))
                print(f"  [vintage] {sid} 실패: {msg}")

    if meta_rows:
        order = [s for s in series_ids if s in meta_rows]
        order += sorted(s for s in meta_rows if s not in set(series_ids))
        mdf = pd.DataFrame([meta_rows[s] for s in order], columns=META_COLUMNS)
        write_csv_if_changed(mdf.astype(str), meta_path)
    return failures


def print_failures(failures):
    if not failures:
        print("\n실패 없음")
        return
    print(f"\n실패 {len(failures)}건")
    print("| series_id | stage | error |")
    print("| --- | --- | --- |")
    for sid, stage, msg in failures:
        print(f"| {sid} | {stage} | {msg.replace('|', '/')} |")


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="FRED 시리즈별 이력 수집기")
    p.add_argument("--out", default=str(DEFAULT_OUT), help="출력 루트 (기본 data/series)")
    p.add_argument("--series", nargs="+", help="수집 대상 ID (기본: REG 전체)")
    p.add_argument("--vintages", action="store_true",
                   help="개정 이력 수집 (기본 off, VINTAGE_SERIES 한정)")
    return p.parse_args(argv)


def main(argv=None, session=None, sleep=time.sleep, now=None):
    args = parse_args(argv)
    api_key = os.environ.get("FRED_API_KEY", "")
    if not api_key:
        print("FRED_API_KEY 환경변수가 설정되지 않았습니다.")
        return 2
    series_ids = args.series or registry_series_ids(load_registry())
    print(f"FRED 시리즈 이력 수집: {len(series_ids)}개 → {args.out}")
    client = FredClient(api_key, session=session, sleep=sleep)
    failures = collect(series_ids, args.out, client, now=now,
                       vintages=args.vintages)
    print(f"\nAPI 호출 수: {client.calls}")
    print_failures(failures)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
