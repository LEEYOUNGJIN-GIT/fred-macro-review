#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Global_signals.py — 글로벌 보조 신호 5개 (v1)
입력: global_latest.csv
"""
from __future__ import annotations

import pandas as pd
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "global_latest.csv"
OUTPUT_PATH = BASE_DIR / "data" / "global_signals.md"

_STATUS_LEVEL = {
    "강한 확장": 1, "확장": 1, "견조": 1, "흑자": 1, "약세": 1, "완화": 1,
    "중립": 2, "균형": 2, "정상": 2,
    "둔화": 3, "주의": 3, "적자": 3, "압력": 3,
    "위축": 4, "경계": 4, "고인플레": 4, "긴축": 4,
    "침체": 5, "위기": 5, "심각": 5,
}
_LEVEL_EMOJI = {5: "🔴", 4: "🟠", 3: "🟡", 2: "🔵", 1: "🟢", 0: "⚪"}


def load_data() -> pd.DataFrame:
    df = pd.read_csv(CSV_PATH, dtype={"series_id": str})
    df.set_index("series_id", inplace=True)
    for c in ["latest_value", "chg_prev", "chg_mid", "chg_yoy"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def safe_val(df: pd.DataFrame, sid: str, col: str = "latest_value"):
    if sid not in df.index:
        return None
    v = df.at[sid, col]
    if isinstance(v, pd.Series):
        v = v.iloc[0]
    if pd.isna(v):
        return None
    return float(v)


def calc_global_growth(df: pd.DataFrame) -> dict:
    kr = safe_val(df, "WB_KR_GDP_GROWTH")
    us = safe_val(df, "WB_US_GDP_GROWTH")
    kr_cli = safe_val(df, "OECD_KR_CLI")
    us_cli = safe_val(df, "OECD_US_CLI")
    score = 5.0
    d = []
    if kr is not None:
        d.append(f"KR GDP={kr:.1f}%")
        if kr >= 3:
            score += 1.5
        elif kr >= 2:
            score += 0.5
        elif kr <= 0:
            score -= 2
        elif kr <= 1:
            score -= 1
    if us is not None:
        d.append(f"US GDP={us:.1f}%")
        if us >= 3:
            score += 0.5
        elif us <= 0:
            score -= 1
    if kr_cli is not None:
        d.append(f"KR CLI={kr_cli:.1f}")
        if kr_cli >= 101:
            score += 0.5
        elif kr_cli <= 99:
            score -= 0.5
    if us_cli is not None:
        d.append(f"US CLI={us_cli:.1f}")
    score = max(0, min(10, score))
    if score >= 7:
        st = "강한 확장"
    elif score >= 5.5:
        st = "견조"
    elif score >= 4:
        st = "둔화"
    elif score >= 2.5:
        st = "위축"
    else:
        st = "침체"
    d.append(f"점수={score:.1f}")
    return {"status": st, "value": score, "detail": ", ".join(d), "series": ["WB_KR_GDP_GROWTH", "WB_US_GDP_GROWTH", "OECD_KR_CLI", "OECD_US_CLI"]}


def calc_global_inflation(df: pd.DataFrame) -> dict:
    kr = safe_val(df, "WB_KR_CPI")
    us = safe_val(df, "WB_US_CPI")
    vals = [v for v in [kr, us] if v is not None]
    if not vals:
        return {"status": "N/A", "value": None, "detail": "데이터 없음", "series": ["WB_KR_CPI", "WB_US_CPI"]}
    avg = sum(vals) / len(vals)
    d = []
    if kr is not None:
        d.append(f"KR CPI={kr:.1f}%")
    if us is not None:
        d.append(f"US CPI={us:.1f}%")
    d.append(f"평균={avg:.1f}%")
    if avg >= 5:
        st = "고인플레"
    elif avg >= 3:
        st = "압력"
    elif avg >= 1.5:
        st = "중립"
    else:
        st = "완화"
    return {"status": st, "value": round(avg, 2), "detail": ", ".join(d), "series": ["WB_KR_CPI", "WB_US_CPI"]}


def calc_oecd_cli_momentum(df: pd.DataFrame) -> dict:
    kr = safe_val(df, "OECD_KR_CLI")
    us = safe_val(df, "OECD_US_CLI")
    de = safe_val(df, "OECD_DEU_CLI")
    kr_m = safe_val(df, "OECD_KR_CLI", "chg_mid")
    if kr is None and us is None:
        return {"status": "N/A", "value": None, "detail": "데이터 없음", "series": ["OECD_KR_CLI", "OECD_US_CLI", "OECD_DEU_CLI"]}
    d = []
    above = 0
    for label, v in [("KR", kr), ("US", us), ("DEU", de)]:
        if v is not None:
            d.append(f"{label}={v:.2f}")
            if v >= 100:
                above += 1
    if kr_m is not None:
        d.append(f"KR 3M Δ={kr_m:+.2f}")
    if above >= 2:
        st = "확장"
    elif above == 1:
        st = "중립"
    else:
        st = "둔화"
    return {"status": st, "value": above, "detail": ", ".join(d), "series": ["OECD_KR_CLI", "OECD_US_CLI", "OECD_DEU_CLI"]}


def calc_external_balance(df: pd.DataFrame) -> dict:
    ca = safe_val(df, "IMF_KR_CURRENT_ACCOUNT")
    ca_q = safe_val(df, "IMF_KR_CURRENT_ACCOUNT", "chg_prev")
    if ca is None:
        return {"status": "N/A", "value": None, "detail": "데이터 없음", "series": ["IMF_KR_CURRENT_ACCOUNT"]}
    bil = ca / 1e9
    d = [f"경상수지={bil:,.1f}B USD"]
    if ca_q is not None:
        d.append(f"전분기 Δ={ca_q/1e9:+,.1f}B")
    if ca >= 0:
        st = "흑자" if bil >= 5 else "균형"
    else:
        st = "적자" if bil <= -5 else "주의"
    return {"status": st, "value": bil, "detail": ", ".join(d), "series": ["IMF_KR_CURRENT_ACCOUNT"]}


def calc_euro_financial(df: pd.DataFrame) -> dict:
    eur = safe_val(df, "ECB_EURUSD")
    mro = safe_val(df, "ECB_POLICY_RATE_MRO")
    eur_y = safe_val(df, "ECB_EURUSD", "chg_yoy")
    d = []
    if eur is not None:
        d.append(f"EUR/USD={eur:.4f}")
    if eur_y is not None:
        d.append(f"YoY={eur_y:+.4f}")
    if mro is not None:
        d.append(f"ECB MRO={mro:.2f}%")
    if eur is None and mro is None:
        return {"status": "N/A", "value": None, "detail": "데이터 없음", "series": ["ECB_EURUSD", "ECB_POLICY_RATE_MRO"]}
    if eur_y is not None and eur_y >= 0.05:
        st = "유로 강세"
    elif eur_y is not None and eur_y <= -0.05:
        st = "유로 약세"
    else:
        st = "중립"
    if mro is not None and mro >= 4:
        st = "긴축"
    return {"status": st, "value": eur, "detail": ", ".join(d), "series": ["ECB_EURUSD", "ECB_POLICY_RATE_MRO"]}


def calc_overall_risk(signals: dict) -> dict:
    levels = []
    for sig in signals.values():
        lv = _STATUS_LEVEL.get(sig.get("status", "N/A"))
        if lv is not None:
            levels.append(lv)
    if not levels:
        return {"level": 0, "label": "N/A", "emoji": "⚪", "score": 0}
    avg = sum(levels) / len(levels)
    mx = max(levels)
    composite = 0.7 * avg + 0.3 * mx
    risk_lv = max(1, min(5, int(round(composite))))
    labels = {5: "위험", 4: "경계", 3: "주의", 2: "관심", 1: "안정"}
    emojis = {5: "🔴", 4: "🟠", 3: "🟡", 2: "🔵", 1: "🟢"}
    return {"level": risk_lv, "label": labels[risk_lv], "emoji": emojis[risk_lv], "score": round(composite, 2), "count": len(levels)}


_SIGNAL_NAMES = OrderedDict([
    ("global_growth", "글로벌 성장"),
    ("global_inflation", "글로벌 물가"),
    ("oecd_cli", "OECD CLI 모멘텀"),
    ("external_balance", "한국 대외수지"),
    ("euro_financial", "유로존 금융"),
])

_CALC_MAP = OrderedDict([
    ("global_growth", calc_global_growth),
    ("global_inflation", calc_global_inflation),
    ("oecd_cli", calc_oecd_cli_momentum),
    ("external_balance", calc_external_balance),
    ("euro_financial", calc_euro_financial),
])


def generate_markdown(signals: dict, risk: dict, generated_at: str) -> str:
    lines = [
        "# 🌍 Global Macro Signals (v1)\n",
        "> **보조 레이어** — 공식 거시는 fred_latest.md 우선\n",
        f"> Generated: {generated_at}\n",
        f"## 종합: {risk['emoji']} {risk['label']} (score {risk['score']:.2f})\n",
        "## 📊 신호 요약\n",
        "| # | 신호 | 상태 | 값 | 핵심 요약 |",
        "|---|------|------|----|----------|",
    ]
    for i, (key, name) in enumerate(_SIGNAL_NAMES.items(), 1):
        sig = signals.get(key, {})
        st = sig.get("status", "N/A")
        lv = _STATUS_LEVEL.get(st, 0)
        emoji = _LEVEL_EMOJI.get(lv, "⚪")
        val = sig.get("value")
        val_s = f"{val:.2f}" if val is not None else "N/A"
        lines.append(f"| {i} | {name} | {emoji} {st} | {val_s} | {sig.get('detail', '')} |")
    lines.append("\n## 📋 상세\n")
    for key, name in _SIGNAL_NAMES.items():
        sig = signals.get(key, {})
        st = sig.get("status", "N/A")
        lv = _STATUS_LEVEL.get(st, 0)
        emoji = _LEVEL_EMOJI.get(lv, "⚪")
        lines.append(f"### {emoji} {name} — {st}")
        lines.append(f"- **값**: {sig.get('value')}")
        lines.append(f"- **상세**: {sig.get('detail', '')}")
        lines.append(f"- **시리즈**: {', '.join(sig.get('series', []))}\n")
    return "\n".join(lines)


def main() -> None:
    print("Global_signals.py start")
    df = load_data()
    print(f"  loaded {len(df)} series")
    signals = {k: fn(df) for k, fn in _CALC_MAP.items()}
    risk = calc_overall_risk(signals)
    for key, name in _SIGNAL_NAMES.items():
        print(f"  {name}: {signals[key]['status']}")
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    md = generate_markdown(signals, risk, generated_at)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(md, encoding="utf-8")
    print(f"  saved {OUTPUT_PATH} ({len(md):,} chars)")


if __name__ == "__main__":
    main()
