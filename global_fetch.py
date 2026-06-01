#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Global Macro Layer — World Bank / OECD / IMF / ECB (no API keys)
────────────────────────────────────────────────────────────────
• 12 series (6 WB + 3 OECD CLI + 1 IMF BOP + 2 ECB)
• FRED·Market 레이어와 merge 없음 — 글로벌 거시 보조
• 50% 미만 성공 시 중단 (fred_fetch.py와 동일)
"""
from __future__ import annotations

import os
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import requests

# ═══════════════════════════════════════════════════════════
# 1. 환경 설정
# ═══════════════════════════════════════════════════════════

REQUEST_DELAY = 0.5
MAX_RETRIES = 3
RETRY_BACKOFF = 2.0
MIN_SUCCESS_RATE = 0.5
HTTP_TIMEOUT = (5, 20)

END_DATE = datetime.now(timezone.utc).strftime("%Y-%m-%d")
START_DATE = (datetime.now(timezone.utc) - timedelta(days=1095)).strftime("%Y-%m-%d")
WB_START_YEAR = int(START_DATE[:4])
WB_END_YEAR = int(END_DATE[:4])

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
HISTORY_DIR = DATA_DIR / "global_history"

NOTE_PREFIX = "⚠ 글로벌 보조지표. 공식 거시는 fred_latest.md."


def _note(desc: str, limit: str = "") -> str:
    s = f"{NOTE_PREFIX} {desc}."
    if limit:
        s += f" {limit}."
    return s


def _session() -> requests.Session:
    s = requests.Session()
    s.trust_env = False
    return s


def _get_json(url: str, *, params: dict | None = None, headers: dict | None = None) -> dict | list:
    last_err: Exception | None = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            r = _session().get(url, params=params, headers=headers, timeout=HTTP_TIMEOUT)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            last_err = e
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_BACKOFF ** attempt)
    raise last_err  # type: ignore[misc]


# ═══════════════════════════════════════════════════════════
# 2. 시리즈 레지스트리 (12개)
# ═══════════════════════════════════════════════════════════

REG = {
    "WB_KR_GDP_GROWTH": {
        "cat": "G01_성장",
        "kr": "한국 실질 GDP 성장률",
        "en": "Korea Real GDP Growth",
        "freq": "A",
        "unit": "%",
        "src": "World Bank",
        "tf": "level",
        "provider": "worldbank",
        "note": _note("연간 YoY", "World Bank NY.GDP.MKTP.KD.ZG"),
    },
    "WB_US_GDP_GROWTH": {
        "cat": "G01_성장",
        "kr": "미국 실질 GDP 성장률",
        "en": "US Real GDP Growth",
        "freq": "A",
        "unit": "%",
        "src": "World Bank",
        "tf": "level",
        "provider": "worldbank",
        "note": _note("연간 YoY", "World Bank NY.GDP.MKTP.KD.ZG"),
    },
    "WB_KR_CPI": {
        "cat": "G02_물가",
        "kr": "한국 CPI 인플레이션",
        "en": "Korea CPI Inflation",
        "freq": "A",
        "unit": "%",
        "src": "World Bank",
        "tf": "level",
        "provider": "worldbank",
        "note": _note("연간", "World Bank FP.CPI.TOTL.ZG"),
    },
    "WB_US_CPI": {
        "cat": "G02_물가",
        "kr": "미국 CPI 인플레이션",
        "en": "US CPI Inflation",
        "freq": "A",
        "unit": "%",
        "src": "World Bank",
        "tf": "level",
        "provider": "worldbank",
        "note": _note("연간", "World Bank FP.CPI.TOTL.ZG"),
    },
    "WB_KR_UNEMP": {
        "cat": "G03_노동",
        "kr": "한국 실업률",
        "en": "Korea Unemployment Rate",
        "freq": "A",
        "unit": "%",
        "src": "World Bank",
        "tf": "level",
        "provider": "worldbank",
        "note": _note("연간", "World Bank SL.UEM.TOTL.ZS"),
    },
    "WB_US_UNEMP": {
        "cat": "G03_노동",
        "kr": "미국 실업률",
        "en": "US Unemployment Rate",
        "freq": "A",
        "unit": "%",
        "src": "World Bank",
        "tf": "level",
        "provider": "worldbank",
        "note": _note("연간", "World Bank SL.UEM.TOTL.ZS"),
    },
    "OECD_KR_CLI": {
        "cat": "G04_선행지수",
        "kr": "한국 OECD CLI",
        "en": "OECD CLI Korea",
        "freq": "M",
        "unit": "Index",
        "src": "OECD",
        "tf": "level",
        "provider": "oecd_cli",
        "ref_area": "KOR",
        "note": _note("월간 CLI", "100=추세. OECD SDMX DF_CLI"),
    },
    "OECD_US_CLI": {
        "cat": "G04_선행지수",
        "kr": "미국 OECD CLI",
        "en": "OECD CLI USA",
        "freq": "M",
        "unit": "Index",
        "src": "OECD",
        "tf": "level",
        "provider": "oecd_cli",
        "ref_area": "USA",
        "note": _note("월간 CLI", "100=추세. OECD SDMX DF_CLI"),
    },
    "OECD_DEU_CLI": {
        "cat": "G04_선행지수",
        "kr": "독일 OECD CLI",
        "en": "OECD CLI Germany",
        "freq": "M",
        "unit": "Index",
        "src": "OECD",
        "tf": "level",
        "provider": "oecd_cli",
        "ref_area": "DEU",
        "note": _note("월간 CLI", "유로존 대용(DEU). OECD SDMX DF_CLI"),
    },
    "IMF_KR_CURRENT_ACCOUNT": {
        "cat": "G05_대외",
        "kr": "한국 경상수지",
        "en": "Korea Current Account Balance",
        "freq": "Q",
        "unit": "USD",
        "src": "IMF",
        "tf": "level",
        "provider": "imf_bop",
        "note": _note("분기 USD", "IMF BOP CAB. KOR.NETCD_T.CAB.USD.Q"),
    },
    "ECB_EURUSD": {
        "cat": "G06_금융",
        "kr": "EUR/USD",
        "en": "EUR/USD Exchange Rate",
        "freq": "D",
        "unit": "USD/EUR",
        "src": "ECB",
        "tf": "level",
        "provider": "ecb",
        "ecb_flow": "EXR",
        "ecb_key": "D.USD.EUR.SP00.A",
        "note": _note("일간", "ECB EXR. FRED DEXUSEU와 단위 확인"),
    },
    "ECB_POLICY_RATE_MRO": {
        "cat": "G06_금융",
        "kr": "ECB MRO 금리",
        "en": "ECB Main Refinancing Rate",
        "freq": "M",
        "unit": "%",
        "src": "ECB",
        "tf": "level",
        "provider": "ecb",
        "ecb_flow": "FM",
        "ecb_key": "B.U2.EUR.4F.KR.MRR_FR.LEV",
        "note": _note("월간", "ECB FM MRR"),
    },
}

WB_MAP = {
    "WB_KR_GDP_GROWTH": ("KR", "NY.GDP.MKTP.KD.ZG"),
    "WB_US_GDP_GROWTH": ("US", "NY.GDP.MKTP.KD.ZG"),
    "WB_KR_CPI": ("KR", "FP.CPI.TOTL.ZG"),
    "WB_US_CPI": ("US", "FP.CPI.TOTL.ZG"),
    "WB_KR_UNEMP": ("KR", "SL.UEM.TOTL.ZS"),
    "WB_US_UNEMP": ("US", "SL.UEM.TOTL.ZS"),
}

COMPARE_PERIODS = {
    "D": {"prev": 1, "mid": 20, "yoy": 252},
    "W": {"prev": 1, "mid": 4, "yoy": 52},
    "M": {"prev": 1, "mid": 3, "yoy": 12},
    "Q": {"prev": 1, "mid": 2, "yoy": 4},
    "A": {"prev": 1, "mid": 2, "yoy": 3},
}

OECD_CLI_URL = (
    "https://sdmx.oecd.org/public/rest/data/OECD.SDD.STES,DSD_STES@DF_CLI/.M.LI...AA...H"
)
IMF_BOP_URL = (
    "https://api.imf.org/external/sdmx/3.0/data/dataflow/IMF.STA/BOP/21.0.0/KOR.NETCD_T.CAB.USD.Q"
)
ECB_BASE = "https://data-api.ecb.europa.eu/service/data"

# ═══════════════════════════════════════════════════════════
# 3. Fetch helpers
# ═══════════════════════════════════════════════════════════

Obs = list[dict]


def fetch_worldbank(country: str, indicator: str) -> Obs:
    url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}"
    j = _get_json(
        url,
        params={
            "format": "json",
            "date": f"{WB_START_YEAR}:{WB_END_YEAR}",
            "per_page": 500,
        },
    )
    rows = j[1] if isinstance(j, list) and len(j) > 1 else []
    obs = [
        {"date": f"{r['date']}-01-01", "value": float(r["value"])}
        for r in rows
        if r.get("value") is not None
    ]
    obs.sort(key=lambda x: x["date"], reverse=True)
    return obs


def fetch_ecb(flow: str, key: str) -> Obs:
    url = f"{ECB_BASE}/{flow}/{key}"
    j = _get_json(
        url,
        headers={"Accept": "application/json"},
        params={"startPeriod": START_DATE},
    )
    structure = j.get("structure") or j.get("data", {}).get("structures", [{}])[0]
    time_vals = structure["dimensions"]["observation"][0]["values"]
    times = [v.get("id") or v.get("name") or v.get("value", "") for v in time_vals]
    series = j["dataSets"][0]["series"]
    first = next(iter(series.values()))
    raw = first.get("observations", {})
    obs: Obs = []
    for idx, val in raw.items():
        i = int(idx)
        if i >= len(times):
            continue
        v = val[0]
        if v is None:
            continue
        obs.append({"date": str(times[i]), "value": float(v)})
    obs.sort(key=lambda x: x["date"], reverse=True)
    return obs


def fetch_imf_bop() -> Obs:
    j = _get_json(
        IMF_BOP_URL,
        params={
            "dimensionAtObservation": "TIME_PERIOD",
            "startPeriod": START_DATE[:4],
        },
    )
    struct = j["data"]["structures"][0]
    time_vals = struct["dimensions"]["observation"][0]["values"]
    times = [v.get("value") or v.get("id") for v in time_vals]
    ds = j["data"]["dataSets"][0]
    series = ds.get("series") or {}
    if not series:
        return []
    first = next(iter(series.values()))
    raw = first.get("observations", {})
    obs: Obs = []
    for idx, val in raw.items():
        i = int(idx)
        if i >= len(times):
            continue
        period = str(times[i])
        date = period if len(period) > 7 else _quarter_to_date(period)
        obs.append({"date": date, "value": float(val[0])})
    obs.sort(key=lambda x: x["date"], reverse=True)
    return obs


def _quarter_to_date(period: str) -> str:
    """2024-Q3 -> 2024-07-01 (quarter start)."""
    if "-Q" not in period:
        return f"{period}-01-01"
    y, q = period.split("-Q")
    month = {"1": "01", "2": "04", "3": "07", "4": "10"}.get(q, "01")
    return f"{y}-{month}-01"


def fetch_oecd_cli_bulk() -> dict[str, Obs]:
    j = _get_json(
        OECD_CLI_URL,
        params={"format": "jsondata", "lastNObservations": 120},
    )
    struct = j["data"]["structures"][0]
    areas = [v["id"] for v in struct["dimensions"]["series"][0]["values"]]
    time_vals = struct["dimensions"]["observation"][0]["values"]
    times = [v.get("id") or v.get("value") or v.get("name", "") for v in time_vals]
    ds = j["data"]["dataSets"][0]
    out: dict[str, Obs] = {}
    targets = {"KOR", "USA", "DEU"}
    for area in targets:
        if area not in areas:
            out[area] = []
            continue
        idx = areas.index(area)
        sk = f"{idx}:0:0:0:0:0:0:0:0"
        ser = ds.get("series", {}).get(sk, {})
        raw = ser.get("observations", {})
        obs: Obs = []
        for oidx, val in raw.items():
            i = int(oidx)
            if i >= len(times):
                continue
            period = str(times[i])
            date = f"{period}-01" if len(period) == 7 else period
            obs.append({"date": date, "value": float(val[0])})
        obs.sort(key=lambda x: x["date"], reverse=True)
        out[area] = obs
    return out


def fetch_all_series() -> dict[str, Obs]:
    data: dict[str, Obs] = {}
    oecd_cache: dict[str, Obs] | None = None

    api_total = len(REG)
    cnt = 0
    for sid, meta in REG.items():
        cnt += 1
        provider = meta["provider"]
        print(f"  [{cnt}/{api_total}] {sid} ({meta['kr']})...", end="", flush=True)
        try:
            if provider == "worldbank":
                country, indicator = WB_MAP[sid]
                obs = fetch_worldbank(country, indicator)
            elif provider == "ecb":
                obs = fetch_ecb(meta["ecb_flow"], meta["ecb_key"])
            elif provider == "imf_bop":
                obs = fetch_imf_bop()
            elif provider == "oecd_cli":
                if oecd_cache is None:
                    oecd_cache = fetch_oecd_cli_bulk()
                    time.sleep(REQUEST_DELAY)
                obs = oecd_cache.get(meta["ref_area"], [])
            else:
                obs = []
            data[sid] = obs
            print(f" OK {len(obs)}")
        except Exception as e:
            print(f" FAIL {e}")
            data[sid] = []
        time.sleep(REQUEST_DELAY)
    return data


# ═══════════════════════════════════════════════════════════
# 4. 비교·출력 (fred_fetch.py 패턴)
# ═══════════════════════════════════════════════════════════

def get_comparisons(obs: Obs, freq: str) -> dict:
    if not obs:
        return {"val": None, "date": None, "prev": None, "mid": None, "yoy": None}
    cp = COMPARE_PERIODS.get(freq, COMPARE_PERIODS["M"])

    def safe_get(idx: int):
        return obs[idx]["value"] if len(obs) > idx else None

    return {
        "val": obs[0]["value"],
        "date": obs[0]["date"],
        "prev": safe_get(cp["prev"]),
        "mid": safe_get(cp["mid"]),
        "yoy": safe_get(cp["yoy"]),
    }


def calc_change(cur, prev, tf: str):
    if cur is None or prev is None:
        return None
    if tf == "level":
        return round(cur - prev, 4)
    if tf in ("yoy_pct", "mom_pct"):
        return round((cur - prev) / abs(prev) * 100, 2) if prev != 0 else None
    if tf == "mom_diff":
        return round(cur - prev, 1)
    return None


def fmt_val(v):
    if v is None:
        return "-"
    av = abs(v)
    if av >= 1_000_000_000:
        return f"{v/1_000_000_000:,.2f}B"
    if av >= 1_000_000:
        return f"{v/1_000_000:,.1f}M"
    if av >= 10_000:
        return f"{v:,.0f}"
    return f"{v:,.2f}"


def fmt_chg(chg, tf="level"):
    if chg is None:
        return "-"
    if tf in ("yoy_pct", "mom_pct"):
        return f"{chg:+.2f}%"
    return f"{chg:+.2f}"


def filter_successful(all_data: dict[str, Obs]) -> tuple[dict[str, Obs], dict]:
    """재시도 후에도 obs가 없는 시리즈는 레지스트리·출력에서 제외."""
    active_reg = {sid: m for sid, m in REG.items() if all_data.get(sid)}
    dropped = sorted(set(REG) - set(active_reg))
    if dropped:
        print(f"\n  dropped (fetch failed): {', '.join(dropped)}")
    active_data = {sid: all_data[sid] for sid in active_reg}
    return active_data, active_reg


def generate_fact_table(all_data: dict, registry: dict | None = None) -> str:
    reg = registry or REG
    report = ["## 🌍 글로벌 거시 보조 팩트 테이블\n", f"**기준일**: {END_DATE}\n"]
    categories: dict[str, list[str]] = {}
    for sid, m in reg.items():
        categories.setdefault(m["cat"], []).append(sid)
    for cat in sorted(categories):
        label = cat.split("_", 1)[1]
        report.append(f"\n### {label}\n")
        report.append("| 지표 | 주기 | 최신값 | 기준일 | 전기비 | 중기비 | YoY비 |")
        report.append("| --- | --- | --- | --- | --- | --- | --- |")
        for sid in categories[cat]:
            m = reg[sid]
            obs = all_data.get(sid, [])
            comp = get_comparisons(obs, m["freq"])
            tf = m["tf"]
            val = comp["val"]
            report.append(
                f"| {m['kr']} | {m['freq']} | {fmt_val(val)} | {comp['date'] or '-'} "
                f"| {fmt_chg(calc_change(val, comp['prev'], tf), tf)} "
                f"| {fmt_chg(calc_change(val, comp['mid'], tf), tf)} "
                f"| {fmt_chg(calc_change(val, comp['yoy'], tf), tf)} |"
            )
    return "\n".join(report)


def write_markdown(fact_table_md: str, path: Path, registry: dict | None = None) -> None:
    reg = registry or REG
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines = [
        "# Global Macro 보조지표 보고서\n",
        "> **데이터 성격: 글로벌 보조 (Supplementary)**",
        "> - 공식 거시경제 기준: `fred_latest.md` (FRED API)",
        "> - 본 파일: World Bank / OECD / IMF / ECB — API Key 불필요",
        "> - FRED·Market 레이어와 merge 없음. 충돌 시 **항상 FRED 우선**",
        "> - 한국 CLI는 FRED `KORLOLITOAASTSAM`과 중복 가능 — 교차 확인용\n",
        f"Generated at: {generated_at}",
        f"Data range: {START_DATE} ~ {END_DATE}",
        f"Series count: {len(reg)}\n",
        "### Included Series\n",
        "| # | Series ID | Category | Korean | English | Freq | Unit | Source |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for i, (sid, m) in enumerate(reg.items(), 1):
        cat_label = m["cat"].split("_", 1)[1]
        lines.append(
            f"| {i} | {sid} | {cat_label} | {m['kr']} | {m['en']} | {m['freq']} | {m['unit']} | {m['src']} |"
        )
    lines.extend([
        "", fact_table_md, "",
        "**비교 기간 범례**",
        "- **전기비**: D=전일, W=전주, M=전월, Q=전분기, A=전년",
        "- **중기비**: D/W=4주전, M=3개월전, Q=2분기전, A=2년전",
        "- **YoY비**: D/W/M=1년전, Q=4분기전, A=3년전\n",
        "### Instruction for Claude\n",
        "- 본 파일은 글로벌 보조 레이어입니다. 공식 분석은 fred_latest.md를 우선하세요.",
        "- IMF 경상수지 단위는 USD(raw). OECD CLI는 100=추세 기준입니다.",
        "- World Bank 지표는 연간(A) 업데이트 lag가 클 수 있습니다.",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"OK Markdown: {path}")


def save_csv(all_data: dict, path: Path, registry: dict | None = None) -> None:
    reg = registry or REG
    rows = []
    for sid, m in reg.items():
        obs = all_data.get(sid, [])
        comp = get_comparisons(obs, m["freq"])
        tf = m["tf"]
        val = comp["val"]
        rows.append({
            "series_id": sid,
            "category": m["cat"],
            "korean_name": m["kr"],
            "english_name": m["en"],
            "frequency": m["freq"],
            "unit": m["unit"],
            "source": m["src"],
            "transform": tf,
            "latest_date": comp["date"] or "",
            "latest_value": val if val is not None else "",
            "chg_prev": calc_change(val, comp["prev"], tf) or "",
            "chg_mid": calc_change(val, comp["mid"], tf) or "",
            "chg_yoy": calc_change(val, comp["yoy"], tf) or "",
            "note": m["note"],
        })
    df = pd.DataFrame(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"OK CSV: {path} ({len(df)} rows)")


def main() -> None:
    print("=" * 60)
    print("Global Macro Layer - WB / OECD / IMF / ECB fetch")
    print(f"기간: {START_DATE} ~ {END_DATE}")
    print("=" * 60)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)

    print("\n[1/3] Global API 데이터 조회...")
    all_data = fetch_all_series()

    api_total = len(REG)
    success = sum(1 for sid in REG if all_data.get(sid))
    rate = success / api_total if api_total else 0
    print(f"\n  -> success: {success}/{api_total} ({rate:.0%})")
    if rate < MIN_SUCCESS_RATE:
        print(f"ERROR success rate {rate:.0%} < {MIN_SUCCESS_RATE:.0%} -> abort")
        sys.exit(1)

    all_data, active_reg = filter_successful(all_data)

    print("\n[2/3] 팩트 테이블 생성...")
    fact_md = generate_fact_table(all_data, active_reg)
    write_markdown(fact_md, DATA_DIR / "global_latest.md", active_reg)

    print("\n[3/3] CSV 저장...")
    save_csv(all_data, DATA_DIR / "global_latest.csv", active_reg)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    save_csv(all_data, HISTORY_DIR / f"global_{ts}.csv", active_reg)

    print("\n" + "=" * 60)
    print("Done")
    print("=" * 60)


if __name__ == "__main__":
    main()
