#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
10년 히스토리 백필 스크립트 (1회성, daily fetch 파이프라인과 완전히 분리)
──────────────────────────────────────────────────────────────────
대상 9개 시리즈:
  FRED (4)        : DGS30, DFII10, BAMLH0A0HYM2(HY OAS), DEXKOUS(USD/KRW)
  Yahoo Finance(5): ^SOX, TIP, VTIP, DBMF, KMLM

fred_fetch.py / market_fetch.py는 "1건이라도 실패 시 파일 미갱신"인
100% strict 정책이지만, 이 백필 스크립트는 정책이 다르다:
  - 시리즈별로 독립 fetch. 일부가 실패해도 나머지는 저장하고 프로세스는 완료한다.
  - ETF 상장일이 10년 이내인 경우(DBMF·KMLM 등) 상장 이후 확보 가능한 구간만
    받아오고 PARTIAL로 표기한다. 10년 미달을 오류로 취급하지 않는다.
  - 전체가 실패한 경우에만 비정상 종료(exit 1)한다.

사용법:
    export FRED_API_KEY="your-api-key"
    python backfill_history.py
"""
from __future__ import annotations

import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests
from dateutil.relativedelta import relativedelta

try:
    import yfinance as yf
except ImportError:
    yf = None

# ── 경로 ──
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "data" / "backfill_10y"

# ── 기간 ──
BACKFILL_YEARS = 10
END_DATE = datetime.now(timezone.utc)
START_DATE = END_DATE - relativedelta(years=BACKFILL_YEARS)
END_DATE_STR = END_DATE.strftime("%Y-%m-%d")
START_DATE_STR = START_DATE.strftime("%Y-%m-%d")

# ── FRED ──
FRED_API_KEY = os.environ.get("FRED_API_KEY", "")
FRED_BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

MAX_RETRIES = 3
RETRY_BACKOFF = 2.0
REQUEST_DELAY = 0.5

FRED_SERIES = {
    "DGS30": {"kr": "미국채 30년물", "en": "30Y Treasury Yield", "unit": "%"},
    "DFII10": {"kr": "10Y 실질금리(TIPS)", "en": "10Y TIPS Yield", "unit": "%"},
    "BAMLH0A0HYM2": {"kr": "하이일드 스프레드(OAS)", "en": "ICE BofA US HY OAS", "unit": "%"},
    "DEXKOUS": {"kr": "원/달러 환율", "en": "USD/KRW", "unit": "KRW/USD"},
}

YAHOO_SERIES = {
    "^SOX": {"kr": "필라델피아 반도체지수", "en": "PHLX Semiconductor Index", "unit": "Index"},
    "TIP": {"kr": "iShares TIPS 채권 ETF", "en": "iShares TIPS Bond ETF", "unit": "USD"},
    "VTIP": {"kr": "Vanguard 단기 TIPS ETF", "en": "Vanguard Short-Term TIPS ETF", "unit": "USD"},
    "DBMF": {"kr": "iMGP 관리선물 ETF", "en": "iMGP DBi Managed Futures ETF", "unit": "USD"},
    "KMLM": {"kr": "KFA/Mount Lucas 관리선물 ETF", "en": "KFA Mount Lucas Managed Futures ETF", "unit": "USD"},
}


# ═══════════════════════════════════════════════════════════
# fetch
# ═══════════════════════════════════════════════════════════

def fetch_fred_series(series_id: str) -> list[dict] | None:
    """FRED API에서 단일 시리즈를 조회한다. 재시도 소진 시 None(실패)을 반환한다."""
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "observation_start": START_DATE_STR,
        "observation_end": END_DATE_STR,
        "sort_order": "asc",
    }
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            r = requests.get(FRED_BASE_URL, params=params, timeout=30)
            r.raise_for_status()
            obs = r.json().get("observations", [])
            data = [{"date": o["date"], "value": float(o["value"])}
                    for o in obs if o["value"] != "."]
            return data if data else None
        except Exception as exc:
            print(f"    [RETRY {attempt}/{MAX_RETRIES}] {series_id}: {exc}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_BACKOFF ** attempt)
    return None


def fetch_yahoo_series(ticker: str) -> list[dict] | None:
    """Yahoo Finance에서 단일 티커를 조회한다. 재시도 소진 시 None(실패)을 반환한다."""
    if yf is None:
        return None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            hist = yf.Ticker(ticker).history(
                start=START_DATE_STR, end=END_DATE_STR, auto_adjust=True,
            )
            if hist is None or hist.empty:
                raise ValueError("empty history")
            h = hist.dropna(subset=["Close"])
            data = [{"date": pd.Timestamp(idx).strftime("%Y-%m-%d"), "value": float(row["Close"])}
                    for idx, row in h.iterrows()]
            data.sort(key=lambda x: x["date"])
            return data if data else None
        except Exception as exc:
            print(f"    [RETRY {attempt}/{MAX_RETRIES}] {ticker}: {exc}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_BACKOFF ** attempt)
    return None


# ═══════════════════════════════════════════════════════════
# 결과 분류 — 일부 실패를 허용하는 핵심 로직
# ═══════════════════════════════════════════════════════════

def classify_result(obs: list[dict] | None, meta: dict, source: str) -> dict:
    """
    fetch 결과를 OK / PARTIAL / FAILED 로 분류한다.
    - FAILED : 재시도 소진, 데이터 0건 → 결측 처리(빈 obs)하고 계속 진행
    - PARTIAL: 데이터는 있으나 시작일이 10년 전 목표(START_DATE_STR)보다 늦음
               → 상장일/시리즈 시작일 이후만 확보된 것으로 간주(정상)
    - OK     : 10년 전 구간까지 확보
    """
    base = {"source": source, **meta}
    if not obs:
        return {**base, "status": "FAILED", "obs": [], "rows": 0,
                "first_date": None, "last_date": None,
                "note": "fetch 실패(재시도 소진) 또는 응답 데이터 없음 — 결측 처리"}
    first_date, last_date = obs[0]["date"], obs[-1]["date"]
    if first_date > START_DATE_STR:
        note = f"데이터/상장 시작일({first_date}) 이후만 확보 — 10년 전체 미달(정상, 트랙레코드 한계)"
        status = "PARTIAL"
    else:
        note = "10년 전 구간까지 확보"
        status = "OK"
    return {**base, "status": status, "obs": obs, "rows": len(obs),
            "first_date": first_date, "last_date": last_date, "note": note}


def run_backfill() -> dict[str, dict]:
    results: dict[str, dict] = {}

    print(f"[FRED] {len(FRED_SERIES)}개 시리즈 백필 (목표 시작일: {START_DATE_STR})")
    if not FRED_API_KEY:
        print("  [WARN] FRED_API_KEY 미설정 — FRED 4종 전체 결측 처리 후 계속 진행")
        for sid, meta in FRED_SERIES.items():
            results[sid] = classify_result(None, meta, "FRED")
            results[sid]["note"] = "FRED_API_KEY 미설정 — 결측 처리"
    else:
        for sid, meta in FRED_SERIES.items():
            print(f"  - {sid} ({meta['kr']})...", end=" ", flush=True)
            obs = fetch_fred_series(sid)
            results[sid] = classify_result(obs, meta, "FRED")
            print(results[sid]["status"])
            time.sleep(REQUEST_DELAY)

    print(f"\n[Yahoo Finance] {len(YAHOO_SERIES)}개 시리즈 백필")
    if yf is None:
        print("  [WARN] yfinance 미설치 — Yahoo 5종 전체 결측 처리 후 계속 진행")
        for tk, meta in YAHOO_SERIES.items():
            results[tk] = classify_result(None, meta, "Yahoo Finance")
            results[tk]["note"] = "yfinance 미설치 — 결측 처리"
    else:
        for tk, meta in YAHOO_SERIES.items():
            print(f"  - {tk} ({meta['kr']})...", end=" ", flush=True)
            obs = fetch_yahoo_series(tk)
            results[tk] = classify_result(obs, meta, "Yahoo Finance")
            print(results[tk]["status"])

    return results


# ═══════════════════════════════════════════════════════════
# 저장
# ═══════════════════════════════════════════════════════════

def _safe_filename(series_id: str) -> str:
    return series_id.replace("^", "").replace("=X", "")


def save_series_csv(series_id: str, obs: list[dict]) -> Path:
    path = OUTPUT_DIR / f"{_safe_filename(series_id)}.csv"
    df = pd.DataFrame(obs)  # columns: date, value (오름차순 — 과거→최신)
    df.to_csv(path, index=False, encoding="utf-8-sig")
    return path


def write_summary_md(results: dict[str, dict], path: Path) -> None:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    total = len(results)
    ok = sum(1 for r in results.values() if r["status"] == "OK")
    partial = sum(1 for r in results.values() if r["status"] == "PARTIAL")
    failed = sum(1 for r in results.values() if r["status"] == "FAILED")

    lines = [
        "# 10년 히스토리 백필 요약\n",
        f"Generated at: {generated_at}",
        f"목표 기간: {START_DATE_STR} ~ {END_DATE_STR} ({BACKFILL_YEARS}년)",
        f"결과: 총 {total}개 — OK {ok} / PARTIAL {partial} / FAILED {failed}\n",
        "> PARTIAL은 오류가 아니라 상장일·시리즈 시작일이 10년 전보다 늦어",
        "> 확보 가능한 전체 구간을 받아온 정상 케이스다.",
        "> FAILED는 결측 처리되었으며 이 프로세스의 실행 자체를 막지 않는다.\n",
        "| Series | Source | 상태 | 확보 구간 | 행 수 | 비고 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for sid, r in results.items():
        span = f"{r['first_date']} ~ {r['last_date']}" if r["first_date"] else "-"
        lines.append(
            f"| {sid} | {r['source']} | {r['status']} | {span} | {r['rows']} | {r['note']} |"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nSummary saved: {path}")


def main() -> None:
    print("=" * 60)
    print(f"10년 히스토리 백필 (일회성) — {START_DATE_STR} ~ {END_DATE_STR}")
    print("=" * 60)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results = run_backfill()

    print("\n[저장] 성공/부분성공 시리즈만 CSV로 저장, 실패는 결측 처리...")
    saved = 0
    for sid, r in results.items():
        if r["obs"]:
            path = save_series_csv(sid, r["obs"])
            print(f"  - {sid}: {path} ({r['rows']}건, {r['status']})")
            saved += 1
        else:
            print(f"  - {sid}: 저장 생략 (FAILED — {r['note']})")

    write_summary_md(results, OUTPUT_DIR / "backfill_summary.md")

    print("\n" + "=" * 60)
    print(f"완료: {saved}/{len(results)} 시리즈 저장됨")
    print("=" * 60)

    if saved == 0:
        print("전체 실패 — 저장된 데이터가 없어 비정상 종료합니다.")
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
