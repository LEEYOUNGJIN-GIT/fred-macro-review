#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Yahoo Finance 보조 시장 팩트 테이블 (Market Layer v1)
──────────────────────────────────────────────────────
• 22 raw + 3 derived = 25 row (고정)
• FRED와 merge 없음 — 공식 거시는 fred_latest.md
• 1 ticker라도 실패 시 exit 1, 파일 미갱신
"""
from __future__ import annotations

import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

try:
    import yfinance as yf
except ImportError:
    print("yfinance 미설치. pip install yfinance")
    sys.exit(1)

# ── 경로 ──
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
HISTORY_DIR = DATA_DIR / "market_history"

MAX_RETRIES = 3
RETRY_BACKOFF = 2.0
MIN_OBS = 253  # YoY(252 trading days) 계산용
EXPECTED_ROWS = 25

NOTE_PREFIX = "⚠ 보조지표. 공식 거시는 fred_latest.md."

COMPARE_PERIODS = {
    "D": {"prev": 1, "mid": 20, "yoy": 252},
}

MID_LABELS = {"D": "4W전비"}


def _note(unit_desc: str, limit: str = "") -> str:
    s = f"{NOTE_PREFIX} {unit_desc}."
    if limit:
        s += f" {limit}."
    return s


REG = {
    "^KS11": {
        "cat": "M01_한국주식", "kr": "KOSPI", "en": "KOSPI Index",
        "freq": "D", "unit": "Index", "src": "Yahoo Finance", "tf": "level",
        "note": _note("지수 종가(KRW)", "한국 주식시장 벤치마크"),
    },
    "^KQ11": {
        "cat": "M01_한국주식", "kr": "KOSDAQ", "en": "KOSDAQ Index",
        "freq": "D", "unit": "Index", "src": "Yahoo Finance", "tf": "level",
        "note": _note("지수 종가(KRW)", "성장주·벤처 중심"),
    },
    "^NDX": {
        "cat": "M02_미국지수", "kr": "나스닥 100", "en": "Nasdaq 100",
        "freq": "D", "unit": "Index", "src": "Yahoo Finance", "tf": "level",
        "note": _note("지수 종가", "SP500(FRED) 보완 — 성장/기술"),
    },
    "^RUT": {
        "cat": "M02_미국지수", "kr": "러셀 2000", "en": "Russell 2000",
        "freq": "D", "unit": "Index", "src": "Yahoo Finance", "tf": "level",
        "note": _note("지수 종가", "소형주·내수 경기 프록시"),
    },
    "^VIX3M": {
        "cat": "M03_변동성", "kr": "VIX 3개월", "en": "VIX 3-Month",
        "freq": "D", "unit": "Index", "src": "Yahoo Finance", "tf": "level",
        "note": _note("CBOE vol index", "VIX 본체는 FRED VIXCLS"),
    },
    "RSP": {
        "cat": "M04_breadth", "kr": "S&P 동일가중 ETF", "en": "S&P Equal Weight ETF",
        "freq": "D", "unit": "USD", "src": "Yahoo Finance", "tf": "level",
        "note": _note("ETF adjusted close", "지수 레벨 아님"),
    },
    "SPY": {
        "cat": "M04_breadth", "kr": "S&P 500 ETF", "en": "SPDR S&P 500 ETF",
        "freq": "D", "unit": "USD", "src": "Yahoo Finance", "tf": "level",
        "note": _note("ETF adjusted close", "SP500(FRED)와 숫자 다를 수 있음"),
    },
    "SPHB": {
        "cat": "M04_risk", "kr": "S&P 고베타 ETF", "en": "S&P High Beta ETF",
        "freq": "D", "unit": "USD", "src": "Yahoo Finance", "tf": "level",
        "note": _note("ETF adjusted close", "risk-on 프록시"),
    },
    "SPLV": {
        "cat": "M04_risk", "kr": "S&P 저변동 ETF", "en": "S&P Low Vol ETF",
        "freq": "D", "unit": "USD", "src": "Yahoo Finance", "tf": "level",
        "note": _note("ETF adjusted close", "risk-off/방어 프록시"),
    },
    "XLK": {
        "cat": "M05_섹터", "kr": "섹터:기술", "en": "Sector: Technology",
        "freq": "D", "unit": "USD", "src": "Yahoo Finance", "tf": "level",
        "note": _note("SPDR sector ETF adjusted close"),
    },
    "XLF": {
        "cat": "M05_섹터", "kr": "섹터:금융", "en": "Sector: Financials",
        "freq": "D", "unit": "USD", "src": "Yahoo Finance", "tf": "level",
        "note": _note("SPDR sector ETF adjusted close"),
    },
    "XLE": {
        "cat": "M05_섹터", "kr": "섹터:에너지", "en": "Sector: Energy",
        "freq": "D", "unit": "USD", "src": "Yahoo Finance", "tf": "level",
        "note": _note("SPDR sector ETF adjusted close"),
    },
    "XLP": {
        "cat": "M05_섹터", "kr": "섹터:필수소비", "en": "Sector: Staples",
        "freq": "D", "unit": "USD", "src": "Yahoo Finance", "tf": "level",
        "note": _note("SPDR sector ETF adjusted close", "방어 섹터"),
    },
    "XLU": {
        "cat": "M05_섹터", "kr": "섹터:유틸리티", "en": "Sector: Utilities",
        "freq": "D", "unit": "USD", "src": "Yahoo Finance", "tf": "level",
        "note": _note("SPDR sector ETF adjusted close", "방어 섹터"),
    },
    "XLY": {
        "cat": "M05_섹터", "kr": "섹터:경기소비", "en": "Sector: Discretionary",
        "freq": "D", "unit": "USD", "src": "Yahoo Finance", "tf": "level",
        "note": _note("SPDR sector ETF adjusted close", "경기민감"),
    },
    "KRE": {
        "cat": "M06_신용", "kr": "지역은행 ETF", "en": "Regional Banks ETF",
        "freq": "D", "unit": "USD", "src": "Yahoo Finance", "tf": "level",
        "note": _note("ETF adjusted close", "은행 신용 스트레스 프록시"),
    },
    "HYG": {
        "cat": "M06_신용", "kr": "하이일드 ETF", "en": "HY Credit ETF",
        "freq": "D", "unit": "USD", "src": "Yahoo Finance", "tf": "level",
        "note": _note("ETF adjusted close", "OAS(bp) 아님 — HYG/LQD ratio용"),
    },
    "LQD": {
        "cat": "M06_신용", "kr": "IG 회사채 ETF", "en": "IG Credit ETF",
        "freq": "D", "unit": "USD", "src": "Yahoo Finance", "tf": "level",
        "note": _note("ETF adjusted close", "OAS(bp) 아님 — HYG/LQD ratio용"),
    },
    "^N225": {
        "cat": "M07_글로벌", "kr": "닛케이 225", "en": "Nikkei 225",
        "freq": "D", "unit": "Index", "src": "Yahoo Finance", "tf": "level",
        "note": _note("지수 종가(JPY)"),
    },
    "^HSI": {
        "cat": "M07_글로벌", "kr": "항셍", "en": "Hang Seng Index",
        "freq": "D", "unit": "Index", "src": "Yahoo Finance", "tf": "level",
        "note": _note("지수 종가(HKD)", "중국/홍콩 프록시"),
    },
    "EEM": {
        "cat": "M07_글로벌", "kr": "신흥국 ETF", "en": "Emerging Markets ETF",
        "freq": "D", "unit": "USD", "src": "Yahoo Finance", "tf": "level",
        "note": _note("ETF adjusted close", "EM risk 프록시"),
    },
    "AUDJPY=X": {
        "cat": "M08_FX", "kr": "AUD/JPY", "en": "AUD/JPY FX",
        "freq": "D", "unit": "JPY_per_AUD", "src": "Yahoo Finance", "tf": "level",
        "note": _note("FX 일봉", "risk sentiment — 상승=risk-on"),
    },
    "MARKET_BREADTH": {
        "cat": "M09_파생", "kr": "시장 Breadth", "en": "RSP/SPY Ratio",
        "freq": "D", "unit": "Ratio", "src": "Calculated", "tf": "calculated",
        "note": _note("RSP÷SPY", "무차원 — 절대값 해석 금지, 방향만"),
    },
    "MARKET_RISK_ON": {
        "cat": "M09_파생", "kr": "Risk-on/off", "en": "SPHB/SPLV Ratio",
        "freq": "D", "unit": "Ratio", "src": "Calculated", "tf": "calculated",
        "note": _note("SPHB÷SPLV", "무차원 — risk-on/off 방향만"),
    },
    "HYG_LQD_RATIO": {
        "cat": "M09_파생", "kr": "HY/IG 가격비", "en": "HYG/LQD Ratio",
        "freq": "D", "unit": "Ratio", "src": "Calculated", "tf": "calculated",
        "note": _note("HYG÷LQD", "OAS(bp) 아님 — 신용 방향만"),
    },
}

RAW_TICKERS = [sid for sid, m in REG.items() if m["tf"] != "calculated"]


def _hist_to_obs(hist: pd.DataFrame) -> list[dict]:
    if hist is None or hist.empty:
        return []
    h = hist.dropna(subset=["Close"])
    if h.empty:
        return []
    obs = [
        {"date": pd.Timestamp(idx).strftime("%Y-%m-%d"), "value": float(row["Close"])}
        for idx, row in h.iterrows()
    ]
    obs.sort(key=lambda x: x["date"], reverse=True)
    return obs


def _fetch_single(ticker: str) -> list[dict]:
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            hist = yf.Ticker(ticker).history(period="2y", auto_adjust=True)
            obs = _hist_to_obs(hist)
            if obs:
                return obs
        except Exception as exc:
            print(f"  [RETRY {attempt}/{MAX_RETRIES}] {ticker}: {exc}")
        if attempt < MAX_RETRIES:
            time.sleep(RETRY_BACKOFF ** attempt)
    return []


def _fetch_batch(tickers: list[str]) -> dict[str, list[dict]]:
    result: dict[str, list[dict]] = {t: [] for t in tickers}
    try:
        raw = yf.download(
            tickers, period="2y", auto_adjust=True,
            group_by="ticker", threads=True, progress=False,
        )
        if raw is None or raw.empty:
            return result
        if len(tickers) == 1:
            result[tickers[0]] = _hist_to_obs(raw)
            return result
        for t in tickers:
            try:
                sub = raw[t].dropna(how="all")
                result[t] = _hist_to_obs(sub)
            except (KeyError, TypeError):
                pass
    except Exception as exc:
        print(f"  [WARN] batch download: {exc}")
    return result


def fetch_all_raw() -> dict[str, list[dict]]:
    print(f"  batch download ({len(RAW_TICKERS)} tickers)...")
    data = _fetch_batch(RAW_TICKERS)
    for i, ticker in enumerate(RAW_TICKERS, 1):
        if data.get(ticker):
            print(f"  [{i}/{len(RAW_TICKERS)}] {ticker} OK ({len(data[ticker])} obs)")
            continue
        print(f"  [{i}/{len(RAW_TICKERS)}] {ticker} batch miss, fallback...")
        data[ticker] = _fetch_single(ticker)
        if data[ticker]:
            print(f"    -> OK ({len(data[ticker])} obs)")
        else:
            print(f"    -> FAILED")
    return data


def calc_ratio_series(num_obs: list[dict], den_obs: list[dict]) -> list[dict]:
    nmap = {o["date"]: o["value"] for o in num_obs}
    dmap = {o["date"]: o["value"] for o in den_obs}
    dates = sorted(set(nmap) & set(dmap), reverse=True)
    out = []
    for d in dates:
        if dmap[d] != 0:
            out.append({"date": d, "value": round(nmap[d] / dmap[d], 6)})
    return out


def calc_market_breadth(all_data: dict) -> list[dict]:
    return calc_ratio_series(all_data["RSP"], all_data["SPY"])


def calc_market_risk_on(all_data: dict) -> list[dict]:
    return calc_ratio_series(all_data["SPHB"], all_data["SPLV"])


def calc_hyg_lqd_ratio(all_data: dict) -> list[dict]:
    return calc_ratio_series(all_data["HYG"], all_data["LQD"])


CALC_FUNCS = {
    "MARKET_BREADTH": calc_market_breadth,
    "MARKET_RISK_ON": calc_market_risk_on,
    "HYG_LQD_RATIO": calc_hyg_lqd_ratio,
}


def get_series_obs(series_id: str, meta: dict, all_data: dict) -> list[dict]:
    if meta.get("tf") != "calculated":
        return all_data.get(series_id, [])
    fn = CALC_FUNCS.get(series_id)
    return fn(all_data) if fn else []


def get_comparisons(obs: list[dict], freq: str) -> dict:
    if not obs:
        return {"val": None, "date": None, "prev": None, "mid": None, "yoy": None}
    cp = COMPARE_PERIODS.get(freq, COMPARE_PERIODS["D"])

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
    if tf == "calculated":
        return round(cur - prev, 4)
    return None


def validate_all_data(all_data: dict) -> None:
    for ticker in RAW_TICKERS:
        obs = all_data.get(ticker, [])
        if not obs:
            raise ValueError(f"fetch failed: {ticker}")
        if len(obs) < MIN_OBS:
            raise ValueError(f"insufficient history: {ticker} ({len(obs)} < {MIN_OBS})")
        if obs[0]["value"] <= 0:
            raise ValueError(f"invalid latest value: {ticker}={obs[0]['value']}")
    for sid in CALC_FUNCS:
        obs = get_series_obs(sid, REG[sid], all_data)
        if not obs or obs[0]["value"] is None:
            raise ValueError(f"derived calc failed: {sid}")


def validate_csv_rows(rows: list[dict]) -> None:
    if len(rows) != EXPECTED_ROWS:
        raise ValueError(f"row count {len(rows)} != {EXPECTED_ROWS}")
    for row in rows:
        if row.get("latest_value") == "" or row.get("latest_value") is None:
            raise ValueError(f"empty latest_value: {row.get('series_id')}")
        if "보조지표" not in str(row.get("note", "")):
            raise ValueError(f"missing 보조지표 note: {row.get('series_id')}")
        if not row.get("unit"):
            raise ValueError(f"missing unit: {row.get('series_id')}")


def fmt_val(v):
    if v is None:
        return "-"
    av = abs(v)
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
    if tf == "calculated":
        return f"{chg:+.4f}"
    return f"{chg:+.2f}"


def generate_fact_table(all_data: dict) -> str:
    end = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = ["## Market 보조 팩트 테이블\n", f"**기준일**: {end}\n"]
    categories: dict[str, list[str]] = {}
    for sid, m in REG.items():
        categories.setdefault(m["cat"], []).append(sid)
    for cat in sorted(categories):
        label = cat.split("_", 1)[1]
        lines.append(f"\n### {label}\n")
        lines.append("| 지표 | 주기 | 최신값 | 기준일 | 전기비 | 4W전비 | YoY비 |")
        lines.append("| --- | --- | --- | --- | --- | --- | --- |")
        for sid in categories[cat]:
            m = REG[sid]
            obs = get_series_obs(sid, m, all_data)
            comp = get_comparisons(obs, m["freq"])
            tf = m["tf"]
            val = comp["val"]
            lines.append(
                f"| {m['kr']} | {m['freq']} | {fmt_val(val)} | {comp['date'] or '-'} "
                f"| {fmt_chg(calc_change(val, comp['prev'], tf), tf)} "
                f"| {fmt_chg(calc_change(val, comp['mid'], tf), tf)} "
                f"| {fmt_chg(calc_change(val, comp['yoy'], tf), tf)} |"
            )
    return "\n".join(lines)


def write_markdown(fact_table_md: str, path: Path) -> None:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines = [
        "# Market 보조지표 보고서\n",
        "> **데이터 성격: 보조지표 (Supplementary)**",
        "> - 공식 거시경제 기준: `fred_latest.md` (FRED API)",
        "> - 본 파일: Yahoo Finance 일봉 — 시장·한국·breadth 보조",
        "> - 단위: Index=지수 종가 | USD=ETF adjusted close | Ratio=무차원(절대값 해석 금지)",
        "> - 미포함(FRED 사용): 금리, VIX, SP500, WTI, USD/KRW, CPI/PCE, 고용",
        "> - fetch 1건이라도 실패 시 본 파일은 갱신되지 않음\n",
        f"Generated at: {generated_at}",
        f"Source: Yahoo Finance (unofficial) | Rows: {EXPECTED_ROWS} (fixed)\n",
        f"### Included Series ({EXPECTED_ROWS}개)\n",
        "| # | Series ID | Category | Korean | English | Freq | Unit |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for i, (sid, m) in enumerate(REG.items(), 1):
        cat_label = m["cat"].split("_", 1)[1]
        lines.append(
            f"| {i} | {sid} | {cat_label} | {m['kr']} | {m['en']} | {m['freq']} | {m['unit']} |"
        )
    lines.extend([
        "", fact_table_md, "",
        "**비교 기간 범례**",
        "- **전기비**: 전일 | **4W전비**: 20영업일 전 | **YoY비**: 252영업일 전\n",
        "### Instruction for Claude\n",
        "- **본 파일은 보조지표입니다.** 공식 거시 분석은 fred_latest.md를 기준으로 하세요.",
        "- 충돌 시 항상 FRED(fred_latest.md)를 우선하세요.",
        "- Ratio(unit) 지표는 무차원입니다. 절대값 기준 없이 전기/YoY 방향만 해석하세요.",
        "- ETF(USD)와 Index는 다른 단위입니다. SP500(FRED)와 SPY(Yahoo)를 동일 지표로 취급하지 마세요.",
        "- 값이 비어 있으면 해당 fetch가 실패했음을 의미합니다.",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Markdown saved: {path}")


def build_csv_rows(all_data: dict) -> list[dict]:
    rows = []
    for sid, m in REG.items():
        obs = get_series_obs(sid, m, all_data)
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
    return rows


def save_csv(rows: list[dict], path: Path) -> None:
    validate_csv_rows(rows)
    df = pd.DataFrame(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"CSV saved: {path} ({len(df)} rows)")


def main() -> None:
    print("=" * 60)
    print("Market Layer v1 — Yahoo Finance supplementary fetch")
    print("=" * 60)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)

    print("\n[1/3] Yahoo Finance fetch (100% required)...")
    all_data = fetch_all_raw()
    try:
        validate_all_data(all_data)
    except ValueError as exc:
        print(f"VALIDATION FAILED: {exc}")
        sys.exit(1)

    print(f"\n  -> {len(RAW_TICKERS)}/{len(RAW_TICKERS)} raw OK")

    print("\n[2/3] Build outputs...")
    rows = build_csv_rows(all_data)
    fact_md = generate_fact_table(all_data)

    print("\n[3/3] Save (all-or-nothing)...")
    try:
        save_csv(rows, DATA_DIR / "market_latest.csv")
        write_markdown(fact_md, DATA_DIR / "market_latest.md")
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        save_csv(rows, HISTORY_DIR / f"market_{ts}.csv")
    except ValueError as exc:
        print(f"SAVE FAILED: {exc}")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("Done")
    print("=" * 60)


if __name__ == "__main__":
    main()
