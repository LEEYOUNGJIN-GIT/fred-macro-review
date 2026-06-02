#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Alpha Vantage 보조 팩트 테이블 (AV Layer v2)
──────────────────────────────────────────
• 11 API calls → 12 series (BRENT + BTC/ETH)
• FRED와 merge 없음 — 공식 거시는 fred_latest.md
• 1 call이라도 실패 시 exit 1, 파일 미갱신
• Rate limit: 25/day, 5/min (REQUEST_DELAY + sliding window)
"""
from __future__ import annotations

import os
import sys
import time
from collections import deque
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

# ── 경로 ──
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
HISTORY_DIR = DATA_DIR / "av_history"

AV_BASE_URL = "https://www.alphavantage.co/query"
API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY", "")

REQUEST_DELAY = 13
MAX_CALLS_PER_MINUTE = 5
MAX_RETRIES = 3
RETRY_BACKOFF = 2.0
HTTP_TIMEOUT = 30
MIN_COMMODITY_OBS = 13
EXPECTED_API_CALLS = 12
EXPECTED_ROWS = 12

NOTE_PREFIX = "⚠ AV 보조지표. 공식 거시는 fred_latest.md."

COMPARE_PERIODS = {
    "D": {"prev": 1, "mid": 20, "yoy": 252},
    "W": {"prev": 1, "mid": 4, "yoy": 52},
    "M": {"prev": 1, "mid": 3, "yoy": 12},
    "Q": {"prev": 1, "mid": 2, "yoy": 4},
    "A": {"prev": 1, "mid": 2, "yoy": 3},
}

MID_LABELS = {"D": "4W전비", "W": "4W전비", "M": "3M전비", "Q": "2Q전비", "A": "2Y전비"}

_call_times: deque[float] = deque(maxlen=MAX_CALLS_PER_MINUTE)
_call_counter = 0

Obs = list[dict]


def _note(desc: str, fred_ref: str = "", limit: str = "") -> str:
    s = f"{NOTE_PREFIX} {desc}."
    if fred_ref:
        s += f" FRED {fred_ref} 교차확인."
    if limit:
        s += f" {limit}."
    return s


REG = {
    "AV_GOLD_SPOT": {
        "cat": "AV01_금속",
        "kr": "금 프록시(GLD ETF)",
        "en": "Gold Proxy GLD ETF",
        "freq": "D",
        "unit": "USD/oz",
        "src": "Alpha Vantage",
        "tf": "level",
        "note": _note("GLD ETF daily (금 프록시)", "NASDAQQGLDI", "현물 아님 ETF"),
    },
    "AV_SILVER_SPOT": {
        "cat": "AV01_금속",
        "kr": "은 프록시(SLV ETF)",
        "en": "Silver Proxy SLV ETF",
        "freq": "D",
        "unit": "USD",
        "src": "Alpha Vantage",
        "tf": "level",
        "note": _note("SLV ETF daily", limit="귀금속 보조 ETF"),
    },
    "AV_COPPER": {
        "cat": "AV02_원자재",
        "kr": "구리",
        "en": "Copper",
        "freq": "M",
        "unit": "USD/MT",
        "src": "Alpha Vantage",
        "tf": "yoy_pct",
        "note": _note("COPPER monthly", "PCOPPUSDM"),
    },
    "AV_ALUMINUM": {
        "cat": "AV02_원자재",
        "kr": "알루미늄",
        "en": "Aluminum",
        "freq": "M",
        "unit": "USD/MT",
        "src": "Alpha Vantage",
        "tf": "yoy_pct",
        "note": _note("ALUMINUM monthly", "PALUMUSDM"),
    },
    "AV_WHEAT": {
        "cat": "AV02_원자재",
        "kr": "밀",
        "en": "Wheat",
        "freq": "M",
        "unit": "USD/MT",
        "src": "Alpha Vantage",
        "tf": "yoy_pct",
        "note": _note("WHEAT monthly", "PWHEAMTUSDM"),
    },
    "AV_CORN": {
        "cat": "AV02_원자재",
        "kr": "옥수수",
        "en": "Corn",
        "freq": "M",
        "unit": "USD/MT",
        "src": "Alpha Vantage",
        "tf": "yoy_pct",
        "note": _note("CORN monthly", "PMAIZMTUSDM"),
    },
    "AV_BRENT": {
        "cat": "AV02_원자재",
        "kr": "브렌트유",
        "en": "Brent Crude",
        "freq": "M",
        "unit": "USD/Barrel",
        "src": "Alpha Vantage",
        "tf": "yoy_pct",
        "note": _note("BRENT monthly", "DCOILWTICO", "WTI와 괴리 참고"),
    },
    "AV_USDKRW": {
        "cat": "AV03_FX",
        "kr": "USD/KRW",
        "en": "USD/KRW",
        "freq": "D",
        "unit": "KRW/USD",
        "src": "Alpha Vantage",
        "tf": "level",
        "note": _note("FX_DAILY", "DEXKOUS", "단위·기준일 다를 수 있음"),
    },
    "AV_USDJPY": {
        "cat": "AV03_FX",
        "kr": "USD/JPY",
        "en": "USD/JPY",
        "freq": "D",
        "unit": "JPY/USD",
        "src": "Alpha Vantage",
        "tf": "level",
        "note": _note("FX_DAILY", "DEXJPUS"),
    },
    "AV_USDCNY": {
        "cat": "AV03_FX",
        "kr": "USD/CNY",
        "en": "USD/CNY",
        "freq": "D",
        "unit": "CNY/USD",
        "src": "Alpha Vantage",
        "tf": "level",
        "note": _note("FX_DAILY", "DEXCHUS"),
    },
    "AV_BTCUSD": {
        "cat": "AV04_크립토",
        "kr": "비트코인(USD)",
        "en": "Bitcoin USD",
        "freq": "D",
        "unit": "USD",
        "src": "Alpha Vantage",
        "tf": "yoy_pct",
        "note": _note(
            "DIGITAL_CURRENCY_DAILY BTC",
            limit="공식 거시 아님 risk-on/off 보조",
        ),
    },
    "AV_ETHUSD": {
        "cat": "AV04_크립토",
        "kr": "이더리움(USD)",
        "en": "Ethereum USD",
        "freq": "D",
        "unit": "USD",
        "src": "Alpha Vantage",
        "tf": "yoy_pct",
        "note": _note(
            "DIGITAL_CURRENCY_DAILY ETH",
            limit="공식 거시 아님 risk-on/off 보조",
        ),
    },
}


def _reject_av_errors(data: dict) -> None:
    err = data.get("Error Message")
    if isinstance(err, str) and err.strip():
        raise ValueError(err.strip())
    for key in ("Note", "Information", "message"):
        msg = data.get(key)
        if not isinstance(msg, str) or not msg.strip():
            continue
        lower = msg.lower()
        if any(
            x in lower
            for x in (
                "rate limit",
                "frequency",
                "thank you for using",
                "sparingly",
                "api key",
            )
        ):
            raise ValueError(msg.strip())


def _throttle_before_call() -> None:
    global _call_counter
    now = time.time()
    if len(_call_times) >= MAX_CALLS_PER_MINUTE:
        oldest = _call_times[0]
        wait_win = 60.0 - (now - oldest)
        if wait_win > 0:
            print(f"  [throttle] 5/min window wait {wait_win:.1f}s")
            time.sleep(wait_win)
            now = time.time()
    since_last = now - (_call_times[-1] if _call_times else 0.0)
    if since_last < REQUEST_DELAY:
        time.sleep(REQUEST_DELAY - since_last)


def _record_call() -> int:
    global _call_counter
    _call_counter += 1
    _call_times.append(time.time())
    return _call_counter


def _get_av(params: dict) -> dict:
    if not API_KEY:
        raise RuntimeError("ALPHAVANTAGE_API_KEY not set")
    last_err: Exception | None = None
    for attempt in range(1, MAX_RETRIES + 1):
        _throttle_before_call()
        n = _record_call()
        print(f"  [API {n}/{EXPECTED_API_CALLS}] {params.get('function')}...", end="", flush=True)
        try:
            r = requests.get(
                AV_BASE_URL,
                params={**params, "apikey": API_KEY},
                timeout=HTTP_TIMEOUT,
            )
            r.raise_for_status()
            data = r.json()
            if not isinstance(data, dict):
                raise ValueError("response is not a JSON object")
            _reject_av_errors(data)
            print(" OK")
            return data
        except Exception as e:
            last_err = e
            print(f" FAIL ({e})")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_BACKOFF ** attempt)
    raise last_err  # type: ignore[misc]


def _sort_obs_desc(obs: Obs) -> Obs:
    out = [{"date": o["date"], "value": float(o["value"])} for o in obs if o.get("value") is not None]
    out.sort(key=lambda x: x["date"], reverse=True)
    return out


def _parse_commodity(data: dict) -> Obs:
    rows = data.get("data")
    if not isinstance(rows, list):
        raise ValueError("commodity: missing data[]")
    obs = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        d = row.get("date")
        v = row.get("value")
        if d and v not in (None, "", "."):
            obs.append({"date": str(d)[:10], "value": float(v)})
    obs = _sort_obs_desc(obs)
    if not obs:
        raise ValueError("commodity: empty series")
    return obs


def _find_time_series_key(data: dict, substring: str) -> str | None:
    for k in data:
        if substring.lower() in k.lower() and "time series" in k.lower():
            return k
    return None


def _parse_fx_daily(data: dict) -> Obs:
    ts_key = _find_time_series_key(data, "FX")
    if not ts_key:
        raise ValueError("fx: missing Time Series FX (Daily)")
    ts = data[ts_key]
    if not isinstance(ts, dict):
        raise ValueError("fx: invalid time series")
    obs = []
    for date_str, row in ts.items():
        if not isinstance(row, dict):
            continue
        close = None
        for k, v in row.items():
            if "close" in k.lower():
                close = v
                break
        if close not in (None, "", "."):
            obs.append({"date": date_str[:10], "value": float(close)})
    obs = _sort_obs_desc(obs)
    if not obs:
        raise ValueError("fx: empty series")
    return obs


def _parse_time_series_daily(data: dict) -> Obs:
    ts_key = _find_time_series_key(data, "Daily")
    if not ts_key:
        raise ValueError("equity: missing Time Series (Daily)")
    ts = data[ts_key]
    if not isinstance(ts, dict):
        raise ValueError("equity: invalid time series")
    obs = []
    for date_str, row in ts.items():
        if not isinstance(row, dict):
            continue
        close = None
        for k, v in row.items():
            if "close" in k.lower() and "adjusted" not in k.lower():
                close = v
                break
        if close not in (None, "", "."):
            obs.append({"date": date_str[:10], "value": float(close)})
    obs = _sort_obs_desc(obs)
    if not obs:
        raise ValueError("equity: empty series")
    return obs


def _parse_crypto_daily(data: dict) -> Obs:
    ts_key = _find_time_series_key(data, "Digital Currency")
    if not ts_key:
        raise ValueError("crypto: missing Time Series (Digital Currency Daily)")
    ts = data[ts_key]
    if not isinstance(ts, dict):
        raise ValueError("crypto: invalid time series")
    obs = []
    for date_str, row in ts.items():
        if not isinstance(row, dict):
            continue
        close = None
        for k, v in row.items():
            kl = k.lower()
            if "close" in kl and "usd" in kl:
                close = v
                break
        if close is None:
            for k, v in row.items():
                if "close" in k.lower():
                    close = v
                    break
        if close not in (None, "", "."):
            obs.append({"date": date_str[:10], "value": float(close)})
    obs = _sort_obs_desc(obs)
    if not obs:
        raise ValueError("crypto: empty series")
    return obs


def fetch_equity_daily(symbol: str) -> Obs:
    data = _get_av(
        {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize": "compact",
        }
    )
    return _parse_time_series_daily(data)


def fetch_commodity(name: str) -> Obs:
    data = _get_av({"function": name, "interval": "monthly"})
    return _parse_commodity(data)


def fetch_fx(from_sym: str, to_sym: str) -> Obs:
    data = _get_av(
        {
            "function": "FX_DAILY",
            "from_symbol": from_sym,
            "to_symbol": to_sym,
            "outputsize": "compact",
        }
    )
    return _parse_fx_daily(data)


def fetch_crypto(symbol: str) -> Obs:
    data = _get_av(
        {
            "function": "DIGITAL_CURRENCY_DAILY",
            "symbol": symbol,
            "market": "USD",
        }
    )
    return _parse_crypto_daily(data)


def fetch_all() -> dict[str, Obs]:
    global _call_counter
    _call_counter = 0
    _call_times.clear()

    out: dict[str, Obs] = {}

    out["AV_GOLD_SPOT"] = fetch_equity_daily("GLD")
    out["AV_SILVER_SPOT"] = fetch_equity_daily("SLV")

    for sid, fn in (
        ("AV_COPPER", "COPPER"),
        ("AV_ALUMINUM", "ALUMINUM"),
        ("AV_WHEAT", "WHEAT"),
        ("AV_CORN", "CORN"),
        ("AV_BRENT", "BRENT"),
    ):
        out[sid] = fetch_commodity(fn)

    out["AV_USDKRW"] = fetch_fx("USD", "KRW")
    out["AV_USDJPY"] = fetch_fx("USD", "JPY")
    out["AV_USDCNY"] = fetch_fx("USD", "CNY")

    out["AV_BTCUSD"] = fetch_crypto("BTC")
    out["AV_ETHUSD"] = fetch_crypto("ETH")

    if _call_counter != EXPECTED_API_CALLS:
        raise RuntimeError(
            f"API call count {_call_counter} != expected {EXPECTED_API_CALLS}"
        )
    return out


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
    return None


def validate_all_data(all_data: dict[str, Obs]) -> None:
    for sid in REG:
        obs = all_data.get(sid, [])
        if not obs:
            raise ValueError(f"empty series: {sid}")
        meta = REG[sid]
        if meta["freq"] == "M" and len(obs) < MIN_COMMODITY_OBS:
            raise ValueError(f"insufficient commodity history: {sid} ({len(obs)})")
        if meta["freq"] == "D" and obs[0]["value"] <= 0:
            raise ValueError(f"invalid latest value: {sid}={obs[0]['value']}")


def validate_csv_rows(rows: list[dict]) -> None:
    if len(rows) != EXPECTED_ROWS:
        raise ValueError(f"row count {len(rows)} != {EXPECTED_ROWS}")
    for row in rows:
        if row.get("latest_value") == "" or row.get("latest_value") is None:
            raise ValueError(f"empty latest_value: {row.get('series_id')}")
        if "AV 보조" not in str(row.get("note", "")):
            raise ValueError(f"missing AV note: {row.get('series_id')}")
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
    return f"{chg:+.2f}"


def generate_fact_table(all_data: dict[str, Obs]) -> str:
    end = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = ["## AV 보조 팩트 테이블\n", f"**기준일**: {end}\n"]
    categories: dict[str, list[str]] = {}
    for sid, m in REG.items():
        categories.setdefault(m["cat"], []).append(sid)
    for cat in sorted(categories):
        label = cat.split("_", 1)[1]
        lines.append(f"\n### {label}\n")
        mid_lbl = MID_LABELS.get(REG[categories[cat][0]]["freq"], "중기비")
        lines.append(f"| 지표 | 주기 | 최신값 | 기준일 | 전기비 | {mid_lbl} | YoY비 |")
        lines.append("| --- | --- | --- | --- | --- | --- | --- |")
        for sid in categories[cat]:
            m = REG[sid]
            obs = all_data.get(sid, [])
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
        "# Alpha Vantage 보조지표 보고서\n",
        "> **데이터 성격: AV 보조 (Supplementary)**",
        "> - 공식 거시경제 기준: `fred_latest.md` (FRED API)",
        "> - 본 파일: Alpha Vantage — commodities / FX / crypto 보조",
        "> - FRED·Market·Global과 merge 없음. 충돌 시 **항상 FRED 우선**",
        f"> - 일 {EXPECTED_API_CALLS} API calls / {EXPECTED_ROWS} series | Rate limit 5/min·25/day·1/sec 준수",
        "> - fetch 1 call이라도 실패 시 본 파일은 갱신되지 않음\n",
        f"Generated at: {generated_at}",
        f"Source: Alpha Vantage | Rows: {EXPECTED_ROWS} (fixed)\n",
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
        "",
        fact_table_md,
        "",
        "**비교 기간 범례**",
        "- **전기비**: D=전일, W=전주, M=전월, Q=전분기, A=전년",
        f"- **중기비**: {MID_LABELS['D']} (D), {MID_LABELS['M']} (M) 등",
        "- **YoY비**: D/W/M=1년전, Q=4분기전, A=3년전\n",
        "### Instruction for Claude\n",
        "- **본 파일은 AV 보조 레이어입니다.** 공식 분석은 fred_latest.md를 우선하세요.",
        "- 크립토(BTC/ETH)는 공식 거시가 아닌 risk sentiment 보조입니다.",
        "- BRENT는 FRED WTI(DCOILWTICO)와 교차 확인하세요.",
        "- 값이 비어 있으면 해당 fetch가 실패했음을 의미합니다.",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Markdown saved: {path}")


def build_csv_rows(all_data: dict[str, Obs]) -> list[dict]:
    rows = []
    for sid, m in REG.items():
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
    return rows


def save_csv(rows: list[dict], path: Path) -> None:
    validate_csv_rows(rows)
    df = pd.DataFrame(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"CSV saved: {path} ({len(df)} rows)")


def main() -> None:
    print("=" * 60)
    print("AV Layer v2 - Alpha Vantage supplementary fetch")
    print("=" * 60)

    if not API_KEY:
        print("ERROR: ALPHAVANTAGE_API_KEY not set")
        sys.exit(1)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)

    print(f"\n[1/3] Alpha Vantage fetch ({EXPECTED_API_CALLS} calls required)...")
    try:
        all_data = fetch_all()
        validate_all_data(all_data)
    except Exception as exc:
        print(f"VALIDATION FAILED: {exc}")
        sys.exit(1)

    print(f"\n  -> {EXPECTED_ROWS}/{EXPECTED_ROWS} series OK, {_call_counter} API calls")

    print("\n[2/3] Build outputs...")
    rows = build_csv_rows(all_data)
    fact_md = generate_fact_table(all_data)

    print("\n[3/3] Save (all-or-nothing)...")
    try:
        save_csv(rows, DATA_DIR / "av_latest.csv")
        write_markdown(fact_md, DATA_DIR / "av_latest.md")
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        save_csv(rows, HISTORY_DIR / f"av_{ts}.csv")
    except ValueError as exc:
        print(f"SAVE FAILED: {exc}")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("Done")
    print("=" * 60)


if __name__ == "__main__":
    main()
