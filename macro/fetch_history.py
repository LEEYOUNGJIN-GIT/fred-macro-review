#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_history.py - 거시 관측 시계열 백필·증분 수집 (data/macro/obs/{SERIES}.csv)

기존 fred_fetch.py는 '최신 1점 + 변화율' 요약표를 만든다. 이 스크립트는 백분위·조건부 분포에
필요한 관측 시계열 자체를 시리즈별 파일로 쌓는다. FRED는 FRED_API_KEY(없으면 keyless CSV), 한국 일별(ECOS)은 ECOS_API_KEY가 필요하다.

사용법
    python macro/fetch_history.py                 # 증분 (파일이 없으면 자동 백필)
    python macro/fetch_history.py --full          # 전 기간 재수집
    python macro/fetch_history.py --series DGS10  # 특정 시리즈만
    python macro/fetch_history.py --source csv    # 키 없이 fredgraph.csv로 수집 (로컬 시험용)

안전장치
  - 응답이 비어 있으면 기존 파일을 건드리지 않고 실패로 기록한다 (조용히 빈 파일이 되는 것 방지)
  - 병합 방식이라 응답이 짧아도 기존 이력이 줄지 않는다
  - 같은 날짜의 값이 바뀌면(개정) 덮어쓰되 data/macro/obs/_revisions.csv에 이전 값을 남긴다
  - 하나라도 실패하면 종료코드 1 (워크플로가 실패로 표시한다)
"""
from __future__ import annotations

import argparse
import io
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
import macro_lib as L  # noqa: E402

API_URL = "https://api.stlouisfed.org/fred/series/observations"
ECOS_URL = "https://ecos.bok.or.kr/api/StatisticSearch/{key}/json/kr/1/100000/{stat}/{cycle}/{start}/{end}/{item}"
CSV_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv"
OVERLAP_DAYS = 60            # 증분 수집 시 마지막 관측일에서 이만큼 되짚어 받아 개정·지연 반영을 잡는다
MAX_RETRIES = 3


def _get(url: str, params: dict) -> requests.Response:
    last = None
    for i in range(MAX_RETRIES):
        try:
            r = requests.get(url, params=params, timeout=40)
            if r.status_code == 200:
                return r
            last = RuntimeError(f"HTTP {r.status_code}: {r.text[:120]}")
        except requests.RequestException as e:      # 네트워크 오류
            last = e
        time.sleep(2.0 * (i + 1))
    raise RuntimeError(f"요청 실패: {last}")


def fetch_api(sid: str, start: str, key: str) -> pd.Series:
    r = _get(API_URL, {"series_id": sid, "api_key": key, "file_type": "json",
                       "observation_start": start})
    obs = r.json().get("observations", [])
    s = pd.Series({pd.Timestamp(o["date"]): pd.to_numeric(o["value"], errors="coerce") for o in obs},
                  dtype=float)
    return s.dropna().sort_index()


def fetch_csv(sid: str, start: str) -> pd.Series:
    r = _get(CSV_URL, {"id": sid, "cosd": start})
    df = pd.read_csv(io.StringIO(r.text))
    if df.shape[1] < 2:
        raise RuntimeError("CSV 형식이 예상과 다르다")
    s = pd.Series(pd.to_numeric(df.iloc[:, 1], errors="coerce").to_numpy(),
                  index=pd.DatetimeIndex(pd.to_datetime(df.iloc[:, 0])), dtype=float)
    return s.dropna().sort_index()


def parse_ecos(payload: dict, expect_name: str) -> pd.Series:
    """ECOS StatisticSearch JSON -> 일별 Series. 오류 응답·항목명 불일치·빈 응답은 예외로 처리한다.
    항목명 검사는 코드가 바뀌어 다른 계열이 조용히 섞이는 것을 막는다."""
    if "RESULT" in payload:
        r = payload["RESULT"]
        raise RuntimeError(f"ECOS 오류 {r.get('CODE')}: {r.get('MESSAGE')}")
    rows = payload.get("StatisticSearch", {}).get("row", [])
    if not rows:
        raise RuntimeError("ECOS 응답에 행이 없다")
    names = {r.get("ITEM_NAME1") or "" for r in rows}
    if expect_name and not all(expect_name in n for n in names):
        raise RuntimeError(f"ECOS 항목명 불일치: 기대 '{expect_name}' / 실제 {sorted(names)}")
    s = pd.Series({pd.Timestamp(r["TIME"]): pd.to_numeric(r["DATA_VALUE"], errors="coerce") for r in rows},
                  dtype=float)
    return s.dropna().sort_index()


def fetch_ecos(spec: str, start: str, key: str) -> pd.Series:
    stat, cycle, item, expect = (spec.split("|") + [""])[:4]
    url = ECOS_URL.format(key=key, stat=stat, cycle=cycle, item=item,
                          start=pd.Timestamp(start).strftime("%Y%m%d"),
                          end=pd.Timestamp.now().strftime("%Y%m%d"))
    r = _get(url, {})
    return parse_ecos(r.json(), expect)


def write_atomic(path: Path, s: pd.Series) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".csv.tmp")
    out = pd.DataFrame({"date": s.index.strftime("%Y-%m-%d"), "value": s.to_numpy()})
    out.to_csv(tmp, index=False, float_format="%.10g")
    os.replace(tmp, path)


def merge(old: pd.Series, new: pd.Series, window_start: pd.Timestamp):
    """window_start 이후 구간은 새 응답으로 교체, 이전 구간은 보존. (병합 결과, 개정 목록) 반환."""
    keep = old[old.index < window_start]
    fresh = new[new.index >= window_start]
    merged = pd.concat([keep, fresh]).sort_index()
    merged = merged[~merged.index.duplicated(keep="last")]
    both = old.index.intersection(fresh.index)
    changed = [(d, old[d], fresh[d]) for d in both if abs(old[d] - fresh[d]) > 1e-9]
    return merged, changed


def run(series: list[str] | None, full: bool, source: str, obs_dir: Path | None = None) -> int:
    cat = L.load_catalog()
    obs_dir = obs_dir or L.OBS_DIR
    key = os.environ.get("FRED_API_KEY", "")
    if source == "auto":
        source = "api" if key else "csv"
    if source == "api" and not key:
        print("[오류] FRED_API_KEY가 없다 (--source csv로 키 없이 수집 가능)")
        return 1
    ids = series or list(cat.index)
    ekey = os.environ.get("ECOS_API_KEY", "")
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    failures, revisions = [], []
    print(f"[수집] 경로={source} 시리즈={len(ids)}개 {'(전 기간)' if full else '(증분)'}")

    for sid in ids:
        if sid not in cat.index:
            failures.append((sid, "series_catalog.csv에 없음"))
            continue
        path = obs_dir / f"{sid}.csv"
        old = L.read_obs(sid, obs_dir=obs_dir)
        start = cat.loc[sid, "start"]
        if full or old.empty:
            window_start = pd.Timestamp(start)
        else:
            window_start = max(pd.Timestamp(start), old.index.max() - pd.Timedelta(days=OVERLAP_DAYS))
        try:
            ws = window_start.strftime("%Y-%m-%d")
            if cat.loc[sid, "source"] == "ecos":
                if not ekey:
                    raise RuntimeError("ECOS_API_KEY가 없다 (기존 파일 보존)")
                new = fetch_ecos(cat.loc[sid, "ecos"], ws, ekey)
            else:
                new = fetch_api(sid, ws, key) if source == "api" else fetch_csv(sid, ws)
            if new.empty:
                raise RuntimeError("응답이 비어 있다 (기존 파일 보존)")
            merged, changed = merge(old, new, window_start)
            write_atomic(path, merged)
            for d, a, b in changed:
                revisions.append((stamp, sid, d.strftime("%Y-%m-%d"), a, b))
            print(f"  {sid:<14} {len(old):>6} -> {len(merged):>6}행  ~{merged.index.max().date()}"
                  f"{'  개정 ' + str(len(changed)) + '건' if changed else ''}")
        except Exception as e:                              # noqa: BLE001
            failures.append((sid, str(e)))
            print(f"  {sid:<14} 실패: {e}")
        time.sleep(0.2)

    if revisions:
        rp = obs_dir / "_revisions.csv"
        df = pd.DataFrame(revisions, columns=["collected_at", "series_id", "date", "old", "new"])
        df.to_csv(rp, mode="a", header=not rp.exists(), index=False, float_format="%.10g")
    if failures:
        print(f"[실패 {len(failures)}건] " + "; ".join(f"{s}: {m}" for s, m in failures))
        return 1
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--series", nargs="*")
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--source", choices=["auto", "api", "csv"], default="auto")
    a = ap.parse_args()
    return run(a.series, a.full, a.source)


if __name__ == "__main__":
    sys.exit(main())
