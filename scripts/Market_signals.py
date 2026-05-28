#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Market_signals.py — Yahoo Finance 보조 신호 6개 (v1)
입력: market_latest.csv (+ optional fred_latest.csv for VIX term)
"""
from __future__ import annotations

import pandas as pd
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STALE_DAYS = 5  # calendar days; oldest latest_date in market_latest.csv
MARKET_CSV = BASE_DIR / "data" / "market_latest.csv"
FRED_CSV = BASE_DIR / "data" / "fred_latest.csv"
OUTPUT_PATH = BASE_DIR / "data" / "market_signals.md"

_STATUS_LEVEL = {
    "강한 risk-on": 1, "risk-on": 1, "견조": 1, "contango": 1, "확장": 1, "완화": 1,
    "중립": 2, "정상": 2, "균형": 2,
    "risk-off": 3, "주의": 3, "쏠림": 3, "backwardation": 3, "둔화": 3, "압력": 3,
    "강한 risk-off": 4, "경계": 4, "위축": 4, "긴축": 4,
    "심각": 5, "위기": 5,
}
_LEVEL_EMOJI = {5: "🔴", 4: "🟠", 3: "🟡", 2: "🔵", 1: "🟢", 0: "⚪"}


def load_market() -> pd.DataFrame:
    df = pd.read_csv(MARKET_CSV, dtype={"series_id": str})
    df.set_index("series_id", inplace=True)
    for c in ["latest_value", "chg_prev", "chg_mid", "chg_yoy"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def load_fred_optional() -> pd.DataFrame | None:
    if not FRED_CSV.exists():
        return None
    df = pd.read_csv(FRED_CSV, dtype={"series_id": str})
    df.set_index("series_id", inplace=True)
    for c in ["latest_value", "chg_prev", "chg_mid", "chg_yoy"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def safe_val(df: pd.DataFrame | None, sid: str, col: str = "latest_value"):
    if df is None or sid not in df.index:
        return None
    v = df.at[sid, col]
    if isinstance(v, pd.Series):
        v = v.iloc[0]
    if pd.isna(v):
        return None
    return float(v)


def _fmt(v, suffix="", decimal=2):
    if v is None:
        return "N/A"
    if v != 0:
        return f"{v:+.{decimal}f}{suffix}"
    return f"{v:.{decimal}f}{suffix}"


def data_freshness_lines(df: pd.DataFrame) -> list[str]:
    """Data as-of from latest_date; WARN if oldest row exceeds STALE_DAYS."""
    if "latest_date" not in df.columns:
        return ["> Data as-of: N/A"]
    parsed = pd.to_datetime(df["latest_date"], errors="coerce")
    valid = parsed.dropna()
    if valid.empty:
        return ["> Data as-of: N/A"]
    oldest_sid = valid.idxmin()
    newest = valid.max().date()
    oldest = valid.min().date()
    age = (datetime.now(timezone.utc).date() - oldest).days
    lines = [f"> Data as-of: {newest} (oldest: {oldest} {oldest_sid})"]
    if age > STALE_DAYS:
        lines.append(
            f"> ⚠ **Stale**: oldest data is {age}d old (>{STALE_DAYS}d) — fetch may be failing"
        )
    else:
        lines.append(f"> Freshness: OK (oldest {age}d ≤ {STALE_DAYS}d)")
    return lines


def yoy_pct_from_level(df: pd.DataFrame, sid: str):
    """level transform: chg_yoy는 절대차 → YoY % 환산."""
    val = safe_val(df, sid)
    chg = safe_val(df, sid, "chg_yoy")
    if val is None or chg is None:
        return None
    prior = val - chg
    if prior == 0:
        return None
    return round((val / prior - 1) * 100, 2)


def mid_pct_from_level(df: pd.DataFrame, sid: str):
    """level transform: chg_mid(4W) 절대차 → % 환산."""
    val = safe_val(df, sid)
    chg = safe_val(df, sid, "chg_mid")
    if val is None or chg is None:
        return None
    prior = val - chg
    if prior == 0:
        return None
    return round((val / prior - 1) * 100, 2)


def calc_korea_momentum(df: pd.DataFrame) -> dict:
    kospi_y = yoy_pct_from_level(df, "^KS11")
    kosdaq_y = yoy_pct_from_level(df, "^KQ11")
    kospi_m = mid_pct_from_level(df, "^KS11")
    if kospi_y is None and kosdaq_y is None:
        return {"status": "N/A", "value": None, "detail": "데이터 없음", "series": ["^KS11", "^KQ11"]}
    score = 0.0
    if kospi_y is not None:
        score += kospi_y
    if kosdaq_y is not None:
        score += kosdaq_y
    avg = score / (int(kospi_y is not None) + int(kosdaq_y is not None))
    d = [f"KOSPI YoY={_fmt(kospi_y, '%')}", f"KOSDAQ YoY={_fmt(kosdaq_y, '%')}"]
    if kospi_m is not None:
        d.append(f"KOSPI 4W={_fmt(kospi_m, '%')}")
    if avg >= 15:
        st = "견조"
    elif avg >= 5:
        st = "중립"
    elif avg >= -5:
        st = "둔화"
    elif avg >= -15:
        st = "위축"
    else:
        st = "심각"
    return {"status": st, "value": round(avg, 2), "detail": ", ".join(d), "series": ["^KS11", "^KQ11"]}


def calc_market_breadth(df: pd.DataFrame) -> dict:
    val = safe_val(df, "MARKET_BREADTH")
    chg = safe_val(df, "MARKET_BREADTH", "chg_mid")
    if val is None:
        return {"status": "N/A", "value": None, "detail": "데이터 없음", "series": ["MARKET_BREADTH"]}
    d = [f"RSP/SPY={val:.4f} (Ratio, 무차원)", f"4W Δ={_fmt(chg, '', 4)}"]
    if val >= 0.30:
        st = "균형"
    elif val >= 0.27:
        st = "중립"
    elif val >= 0.25:
        st = "쏠림"
    else:
        st = "심각"
    if chg is not None and chg > 0.005:
        d.append("4W 상승=breadth 개선")
    elif chg is not None and chg < -0.005:
        d.append("4W 하락=대형주 쏠림")
    return {"status": st, "value": val, "detail": ", ".join(d), "series": ["MARKET_BREADTH", "RSP", "SPY"]}


def calc_risk_on_off(df: pd.DataFrame) -> dict:
    val = safe_val(df, "MARKET_RISK_ON")
    chg = safe_val(df, "MARKET_RISK_ON", "chg_mid")
    if val is None:
        return {"status": "N/A", "value": None, "detail": "데이터 없음", "series": ["MARKET_RISK_ON"]}
    d = [f"SPHB/SPLV={val:.4f} (Ratio, 무차원)", f"4W Δ={_fmt(chg, '', 4)}"]
    if val >= 2.0:
        st = "강한 risk-on"
    elif val >= 1.7:
        st = "risk-on"
    elif val >= 1.3:
        st = "중립"
    elif val >= 1.0:
        st = "risk-off"
    else:
        st = "강한 risk-off"
    return {"status": st, "value": val, "detail": ", ".join(d), "series": ["MARKET_RISK_ON", "SPHB", "SPLV"]}


def calc_vix_term(df: pd.DataFrame, fred: pd.DataFrame | None) -> dict:
    vix3m = safe_val(df, "^VIX3M")
    vix3m_m = safe_val(df, "^VIX3M", "chg_mid")
    vix_fred = safe_val(fred, "VIXCLS")
    d = [f"VIX3M={vix3m:.2f}" if vix3m else "VIX3M=N/A"]
    ratio = None
    if vix_fred is not None and vix3m and vix3m > 0:
        ratio = round(vix_fred / vix3m, 4)
        d.append(f"VIX/VIX3M={ratio:.4f} (FRED VIXCLS/^VIX3M)")
    elif fred is None:
        d.append("FRED VIXCLS 미로드 — ^VIX3M 단독")
    if vix3m_m is not None:
        d.append(f"VIX3M 4W Δ={_fmt(vix3m_m)}")
    if ratio is not None:
        if ratio > 1.05:
            st = "backwardation"
        elif ratio < 0.95:
            st = "contango"
        else:
            st = "중립"
    elif vix3m_m is not None:
        st = "주의" if vix3m_m > 1 else ("완화" if vix3m_m < -1 else "중립")
    elif vix3m is not None:
        st = "중립"
    else:
        return {"status": "N/A", "value": None, "detail": "데이터 없음", "series": ["^VIX3M", "VIXCLS"]}
    return {
        "status": st,
        "value": ratio if ratio is not None else vix3m,
        "detail": ", ".join(d),
        "series": ["^VIX3M", "VIXCLS"],
    }


def calc_sector_rotation(df: pd.DataFrame) -> dict:
    xlk_m = mid_pct_from_level(df, "XLK")
    xle_m = mid_pct_from_level(df, "XLE")
    xlp_m = mid_pct_from_level(df, "XLP")
    if xlk_m is None or xle_m is None:
        return {"status": "N/A", "value": None, "detail": "데이터 없음", "series": ["XLK", "XLE", "XLP"]}
    spread = round(xlk_m - xle_m, 2)
    d = [f"XLK 4W={_fmt(xlk_m, '%')}", f"XLE 4W={_fmt(xle_m, '%')}", f"XLK-XLE={_fmt(spread, '%p')}"]
    if xlp_m is not None:
        d.append(f"XLP 4W={_fmt(xlp_m, '%')}")
    if spread >= 3:
        st = "확장"
    elif spread >= 0:
        st = "중립"
    elif spread >= -3:
        st = "둔화"
    else:
        st = "경계"
    if xlp_m is not None and xlp_m > xlk_m:
        d.append("방어(XLP) > 기술 → risk-off 로테이션")
    return {"status": st, "value": spread, "detail": ", ".join(d), "series": ["XLK", "XLE", "XLP"]}


def calc_credit_direction(df: pd.DataFrame) -> dict:
    val = safe_val(df, "HYG_LQD_RATIO")
    chg = safe_val(df, "HYG_LQD_RATIO", "chg_mid")
    if val is None:
        return {"status": "N/A", "value": None, "detail": "데이터 없음", "series": ["HYG_LQD_RATIO"]}
    d = [
        f"HYG/LQD={val:.4f} (Ratio, OAS 아님)",
        f"4W Δ={_fmt(chg, '', 4)}",
    ]
    if chg is not None and chg > 0.005:
        st = "완화"
    elif chg is not None and chg < -0.005:
        st = "긴축"
    else:
        st = "중립"
    return {"status": st, "value": val, "detail": ", ".join(d), "series": ["HYG_LQD_RATIO", "HYG", "LQD"]}


_SIGNAL_NAMES = OrderedDict([
    ("korea_momentum", "한국 주식"),
    ("market_breadth", "Breadth"),
    ("risk_on_off", "Risk-on/off"),
    ("vix_term", "VIX Term"),
    ("sector_rotation", "섹터 로테이션"),
    ("credit_direction", "신용 방향"),
])


def generate_markdown(signals: dict, generated_at: str, freshness_lines: list[str]) -> str:
    lines = [
        "# Market 보조 신호 대시보드\n",
        "> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**",
        "> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용",
        "> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)",
        "> - market_fetch 실패 시 본 파일 갱신 없음",
        *freshness_lines,
        f"> Generated: {generated_at}\n",
        "## 신호 요약\n",
        "| # | 신호 | 상태 | 값 | 핵심 요약 |",
        "|---|------|------|-----|----------|",
    ]
    for i, (key, name) in enumerate(_SIGNAL_NAMES.items(), 1):
        sig = signals.get(key, {})
        st = sig.get("status", "N/A")
        emoji = _LEVEL_EMOJI.get(_STATUS_LEVEL.get(st, 0), "⚪")
        val = sig.get("value")
        val_s = f"{val:.4f}" if val is not None else "N/A"
        lines.append(f"| {i} | {name} | {emoji} {st} | {val_s} | {sig.get('detail', '')} |")
    lines.append("\n## 신호 상세\n")
    for key, name in _SIGNAL_NAMES.items():
        sig = signals.get(key, {})
        st = sig.get("status", "N/A")
        emoji = _LEVEL_EMOJI.get(_STATUS_LEVEL.get(st, 0), "⚪")
        lines.append(f"### {emoji} {name} — {st}")
        lines.append(f"- **값**: {sig.get('value')}")
        lines.append(f"- **상세**: {sig.get('detail', '')}")
        lines.append(f"- **시리즈**: {', '.join(sig.get('series', []))}\n")
    lines.append("---")
    lines.append("*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*")
    return "\n".join(lines)


def main() -> None:
    print("Market_signals.py (v1 — 6 signals)")
    if not MARKET_CSV.exists():
        print(f"ERROR: {MARKET_CSV} not found. Run market_fetch.py first.")
        raise SystemExit(1)
    df = load_market()
    fred = load_fred_optional()
    print(f"  market: {len(df)} series")
    print(f"  fred cross-read: {'yes' if fred is not None else 'skipped'}")

    signals = {
        "korea_momentum": calc_korea_momentum(df),
        "market_breadth": calc_market_breadth(df),
        "risk_on_off": calc_risk_on_off(df),
        "vix_term": calc_vix_term(df, fred),
        "sector_rotation": calc_sector_rotation(df),
        "credit_direction": calc_credit_direction(df),
    }
    for key, name in _SIGNAL_NAMES.items():
        print(f"  {_SIGNAL_NAMES[key]}: {signals[key].get('status')}")

    freshness = data_freshness_lines(df)
    for line in freshness:
        print(f"  {line.lstrip('> ')}")
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    md = generate_markdown(signals, generated_at, freshness)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(md, encoding="utf-8")
    print(f"  saved: {OUTPUT_PATH} ({len(md):,} chars)")


if __name__ == "__main__":
    main()
