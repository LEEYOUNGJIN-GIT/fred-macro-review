#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fred_regime.py – 성장 / 인플레 2×2 레짐 분류 엔진 (v3)
═══════════════════════════════════════════════════════
fred_fetch.py → data/fred_latest.csv 를 읽어
① 성장 점수(0~10) 10개 구성요소
② 인플레 점수(0~10) 10개 구성요소
③ 4개 레짐 분류 Goldilocks / Overheating / Stagflation / Recession Risk
④ 레짐 전환 조건 + 신뢰도
을 산출하고 data/fred_regime.md 로 출력한다.

사용법:
    python scripts/Fred_regime.py

변경사항 (v3):
    - C-01: GDPC1 chg_prev → chg_yoy 전환, 임계값 재조정
    - C-02: 인플레 구성요소 기여값 ±1.5pt cap, 음방향 확대
    - 3순위: 성장 10개, 인플레 10개로 확장 (SP500, PCEC96, CSUSHPINSA, MORTGAGE30US)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timezone
from pathlib import Path

# ═══════════════════════════════════════════════════════════
# 경로
# ═══════════════════════════════════════════════════════════

BASE_DIR    = Path(__file__).resolve().parent.parent   # repo root
CSV_PATH    = BASE_DIR / "data" / "fred_latest.csv"
OUTPUT_PATH = BASE_DIR / "data" / "fred_regime.md"

# ═══════════════════════════════════════════════════════════
# 유틸
# ═══════════════════════════════════════════════════════════

def load_data() -> pd.DataFrame:
    "fred_latest.csv 를 읽어 series_id 를 인덱스로 반환."
    df = pd.read_csv(CSV_PATH, dtype={"series_id": str})
    df.set_index("series_id", inplace=True)
    for c in ["latest_value", "chg_prev", "chg_mid", "chg_yoy"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

def safe_val(df: pd.DataFrame, sid: str, col: str = "latest_value"):
    "시리즈 ID → 숫자값. 없으면 None."
    if sid not in df.index:
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
    if v < 0 or v > 0:
        return f"{v:+.{decimal}f}{suffix}"
    return f"{v:.{decimal}f}{suffix}"

def _clamp(score: float, lo: float = 0.0, hi: float = 10.0) -> float:
    return max(lo, min(hi, score))

# ═══════════════════════════════════════════════════════════
# 1. 성장 점수 (Growth Score: 0~10, 중립=5)  — 10개 구성요소
# ═══════════════════════════════════════════════════════════

def calc_growth_score(df) -> dict:
    """10개 구성요소로 성장 점수를 산출한다.

    [C-01 수정] GDPC1: chg_prev(비연율화 QoQ%) → chg_yoy(YoY%)로 전환
    [3순위 확장] SP500 chg_yoy, PCEC96 chg_yoy 추가
    """
    score = 5.0
    components = []

    # ── 1) 실질 GDP YoY% (C-01 수정: chg_prev → chg_yoy)
    gdp_yoy = safe_val(df, "GDPC1", "chg_yoy")
    contrib = 0.0
    if gdp_yoy is not None:
        if   gdp_yoy >= 3.0:  contrib = +2.0   # 강한 확장
        elif gdp_yoy >= 2.0:  contrib = +1.0   # 추세 상회
        elif gdp_yoy >= 1.0:  contrib = +0.5   # 추세 성장
        elif gdp_yoy <= 0.0:  contrib = -2.5   # 역성장
        elif gdp_yoy <= 0.5:  contrib = -1.5   # 추세 크게 하회
        elif gdp_yoy <= 1.0:  contrib = -0.5   # 소폭 둔화
    score += contrib
    components.append({"name": "실질 GDP YoY%", "series": "GDPC1",
                        "value": gdp_yoy, "contrib": contrib})

    # ── 2) 산업생산 YoY%
    indpro_yoy = safe_val(df, "INDPRO", "chg_yoy")
    contrib = 0.0
    if indpro_yoy is not None:
        if   indpro_yoy >= 4.0:  contrib = +1.5
        elif indpro_yoy >= 2.0:  contrib = +0.5
        elif indpro_yoy <= -2.0: contrib = -1.5
        elif indpro_yoy <= 0.0:  contrib = -0.5
    score += contrib
    components.append({"name": "산업생산 YoY%", "series": "INDPRO",
                        "value": indpro_yoy, "contrib": contrib})

    # ── 3) 소매판매 MoM%
    rsafs_mom = safe_val(df, "RSAFS", "chg_prev")
    contrib = 0.0
    if rsafs_mom is not None:
        if   rsafs_mom >= 0.5:  contrib = +1.0
        elif rsafs_mom >= 0.3:  contrib = +0.5
        elif rsafs_mom <= -0.5: contrib = -1.0
        elif rsafs_mom <= 0.0:  contrib = -0.5
    score += contrib
    components.append({"name": "소매판매 MoM%", "series": "RSAFS",
                        "value": rsafs_mom, "contrib": contrib})

    # ── 4) 비농업 고용 (전월 차이, 천명)
    nfp = safe_val(df, "PAYEMS", "chg_prev")
    contrib = 0.0
    if nfp is not None:
        if   nfp >= 200: contrib = +1.5
        elif nfp >= 100: contrib = +0.5
        elif nfp <= 0:   contrib = -1.5
        elif nfp <= 50:  contrib = -0.5
    score += contrib
    components.append({"name": "비농업고용 MoM(천명)", "series": "PAYEMS",
                        "value": nfp, "contrib": contrib})

    # ── 5) CFNAI 경기활동지수
    cfnai = safe_val(df, "CFNAI")
    contrib = 0.0
    if cfnai is not None:
        if   cfnai >= 0.2:  contrib = +1.0
        elif cfnai >= 0.0:  contrib = +0.5
        elif cfnai <= -0.7: contrib = -1.5
        elif cfnai <= -0.3: contrib = -0.5
    score += contrib
    components.append({"name": "CFNAI 경기활동", "series": "CFNAI",
                        "value": cfnai, "contrib": contrib})

    # ── 6) 소비자심리
    umcs = safe_val(df, "UMCSENT")
    contrib = 0.0
    if umcs is not None:
        if   umcs >= 80: contrib = +0.5
        elif umcs >= 70: contrib = +0.25
        elif umcs <= 50: contrib = -1.0
        elif umcs <= 60: contrib = -0.5
    score += contrib
    components.append({"name": "소비자심리", "series": "UMCSENT",
                        "value": umcs, "contrib": contrib})

    # ── 7) Philly Fed 선행지수
    usslind = safe_val(df, "USSLIND")
    contrib = 0.0
    if usslind is not None:
        if   usslind >= 1.0:  contrib = +0.5
        elif usslind >= 0.0:  contrib = +0.25
        elif usslind <= -2.0: contrib = -1.0
        elif usslind <= 0.0:  contrib = -0.5
    score += contrib
    components.append({"name": "선행지수(Philly)", "series": "USSLIND",
                        "value": usslind, "contrib": contrib})

    # ── 8) 설비가동률
    tcu = safe_val(df, "TCU")
    contrib = 0.0
    if tcu is not None:
        if   tcu >= 80.0: contrib = +0.5
        elif tcu >= 78.0: contrib = +0.25
        elif tcu <= 70.0: contrib = -1.0
        elif tcu <= 75.0: contrib = -0.5
    score += contrib
    components.append({"name": "설비가동률", "series": "TCU",
                        "value": tcu, "contrib": contrib})

    # ── 9) [3순위 확장] S&P 500 YoY%
    sp_yoy = safe_val(df, "SP500", "chg_yoy")
    contrib = 0.0
    if sp_yoy is not None:
        if   sp_yoy >= 20.0:  contrib = +0.5
        elif sp_yoy >= 10.0:  contrib = +0.25
        elif sp_yoy <= -20.0: contrib = -1.5
        elif sp_yoy <= -10.0: contrib = -0.5
    score += contrib
    components.append({"name": "S&P 500 YoY%", "series": "SP500",
                        "value": sp_yoy, "contrib": contrib})

    # ── 10) [3순위 확장] 실질 개인소비지출 YoY%
    pcec_yoy = safe_val(df, "PCEC96", "chg_yoy")
    contrib = 0.0
    if pcec_yoy is not None:
        if   pcec_yoy >= 3.0: contrib = +0.5
        elif pcec_yoy >= 2.0: contrib = +0.25
        elif pcec_yoy <= 0.0: contrib = -1.0
        elif pcec_yoy <= 1.0: contrib = -0.5
    score += contrib
    components.append({"name": "실질소비지출 YoY%", "series": "PCEC96",
                        "value": pcec_yoy, "contrib": contrib})

    score = _clamp(score)
    return {"score": score, "components": components}

# ═══════════════════════════════════════════════════════════
# 2. 인플레 점수 (Inflation Score: 0~10, 목표=5)  — 10개 구성요소
# ═══════════════════════════════════════════════════════════

def calc_inflation_score(df) -> dict:
    """10개 구성요소로 인플레 점수를 산출한다.

    [C-02 수정] 각 구성요소 기여값을 ±1.5pt로 cap.
    음방향 기여 확대 → 양/음 밸런스 개선 (max+8.0 / max-7.5)
    [3순위 확장] 주택가격(CSUSHPINSA), 모기지금리(MORTGAGE30US) 추가
    """
    score = 5.0
    components = []

    # ── 1) Core PCE YoY%  (C-02: cap ±1.5, 음방향 확대)
    core_pce = safe_val(df, "PCEPILFE", "chg_yoy")
    contrib = 0.0
    if core_pce is not None:
        if   core_pce >= 4.0: contrib = +1.5   # cap
        elif core_pce >= 3.0: contrib = +1.0
        elif core_pce >= 2.5: contrib = +0.5
        elif core_pce <= 1.0: contrib = -1.5
        elif core_pce <= 1.5: contrib = -1.0
        elif core_pce <= 2.0: contrib = -0.5
    score += contrib
    components.append({"name": "Core PCE YoY%", "series": "PCEPILFE",
                        "value": core_pce, "contrib": contrib})

    # ── 2) CPI YoY%
    cpi_yoy = safe_val(df, "CPIAUCSL", "chg_yoy")
    contrib = 0.0
    if cpi_yoy is not None:
        if   cpi_yoy >= 5.0: contrib = +1.5
        elif cpi_yoy >= 3.5: contrib = +0.5
        elif cpi_yoy <= 1.0: contrib = -1.5
        elif cpi_yoy <= 2.0: contrib = -0.5
    score += contrib
    components.append({"name": "CPI YoY%", "series": "CPIAUCSL",
                        "value": cpi_yoy, "contrib": contrib})

    # ── 3) PPI YoY%
    ppi_yoy = safe_val(df, "PPIFIS", "chg_yoy")
    contrib = 0.0
    if ppi_yoy is not None:
        if   ppi_yoy >= 6.0: contrib = +1.0
        elif ppi_yoy >= 3.0: contrib = +0.5
        elif ppi_yoy <= -2.0: contrib = -1.0
        elif ppi_yoy <= 0.0:  contrib = -0.5
    score += contrib
    components.append({"name": "PPI YoY%", "series": "PPIFIS",
                        "value": ppi_yoy, "contrib": contrib})

    # ── 4) 미시간 인플레 기대
    mich = safe_val(df, "MICH")
    contrib = 0.0
    if mich is not None:
        if   mich >= 4.0: contrib = +1.0
        elif mich >= 3.5: contrib = +0.5
        elif mich <= 2.0: contrib = -1.0
        elif mich <= 2.5: contrib = -0.5
    score += contrib
    components.append({"name": "인플레기대(미시간)", "series": "MICH",
                        "value": mich, "contrib": contrib})

    # ── 5) 5Y5Y 선도 인플레
    t5yifr = safe_val(df, "T5YIFR")
    contrib = 0.0
    if t5yifr is not None:
        if   t5yifr >= 2.8: contrib = +1.0
        elif t5yifr >= 2.5: contrib = +0.5
        elif t5yifr <= 1.8: contrib = -1.0
        elif t5yifr <= 2.0: contrib = -0.5
    score += contrib
    components.append({"name": "5Y5Y 선도 인플레", "series": "T5YIFR",
                        "value": t5yifr, "contrib": contrib})

    # ── 6) 임금 상승률 YoY%
    wage = safe_val(df, "CES0500000003", "chg_yoy")
    contrib = 0.0
    if wage is not None:
        if   wage >= 5.0: contrib = +1.0
        elif wage >= 4.0: contrib = +0.5
        elif wage <= 2.0: contrib = -1.0
        elif wage <= 2.5: contrib = -0.5
    score += contrib
    components.append({"name": "임금 YoY%", "series": "CES0500000003",
                        "value": wage, "contrib": contrib})

    # ── 7) 원자재 종합 YoY%
    comm_yoy = safe_val(df, "PALLFNFINDEXM", "chg_yoy")
    contrib = 0.0
    if comm_yoy is not None:
        if   comm_yoy >= 30.0:  contrib = +1.0
        elif comm_yoy >= 15.0:  contrib = +0.5
        elif comm_yoy <= -20.0: contrib = -1.0
        elif comm_yoy <= -10.0: contrib = -0.5
    score += contrib
    components.append({"name": "원자재 YoY%", "series": "PALLFNFINDEXM",
                        "value": comm_yoy, "contrib": contrib})

    # ── 8) WTI 유가
    wti = safe_val(df, "DCOILWTICO")
    contrib = 0.0
    if wti is not None:
        if   wti >= 100: contrib = +0.5
        elif wti >= 80:  contrib = +0.25
        elif wti <= 40:  contrib = -1.0
        elif wti <= 50:  contrib = -0.5
    score += contrib
    components.append({"name": "WTI 유가($/bbl)", "series": "DCOILWTICO",
                        "value": wti, "contrib": contrib})

    # ── 9) [3순위 확장] 주택가격 YoY%
    house_yoy = safe_val(df, "CSUSHPINSA", "chg_yoy")
    contrib = 0.0
    if house_yoy is not None:
        if   house_yoy >= 10.0: contrib = +0.5
        elif house_yoy >= 5.0:  contrib = +0.25
        elif house_yoy <= -5.0: contrib = -1.0
        elif house_yoy <= 0.0:  contrib = -0.5
    score += contrib
    components.append({"name": "주택가격 YoY%", "series": "CSUSHPINSA",
                        "value": house_yoy, "contrib": contrib})

    # ── 10) [3순위 확장] 30년 모기지 금리 (간접 인플레 압력)
    mort = safe_val(df, "MORTGAGE30US")
    contrib = 0.0
    if mort is not None:
        if   mort >= 7.5: contrib = +0.5
        elif mort >= 7.0: contrib = +0.25
        elif mort <= 5.0: contrib = -0.5
        elif mort <= 5.5: contrib = -0.25
    score += contrib
    components.append({"name": "30Y 모기지(%)", "series": "MORTGAGE30US",
                        "value": mort, "contrib": contrib})

    score = _clamp(score)
    return {"score": score, "components": components}

# ═══════════════════════════════════════════════════════════
# 3. 레짐 분류
# ═══════════════════════════════════════════════════════════

_REGIME_TABLE = {
    "overheating": {
        "regime": "Overheating (과열)",
        "emoji":  "🔥",
        "description": "성장과 인플레 모두 높음. 긴축 정책 가능성. 실질금리 상승·장기채 약세 주의.",
    },
    "goldilocks": {
        "regime": "Goldilocks (골디락스)",
        "emoji":  "✨",
        "description": "성장은 견조하나 인플레 안정. 위험자산 우호적. 안정적 정책 환경.",
    },
    "stagflation": {
        "regime": "Stagflation (스태그플레이션)",
        "emoji":  "⚠️",
        "description": "성장 둔화 + 인플레 상승. 정책 딜레마. 방어적 포지셔닝 필요.",
    },
    "recession_risk": {
        "regime": "Recession Risk (침체 우려)",
        "emoji":  "❄️",
        "description": "성장과 인플레 모두 낮음. 경기 부양·금리 인하 기대. 안전자산 선호.",
    },
}

def _strength_label(g_score, i_score):
    "점수가 중립(5.0)에서 얼마나 먼지에 따라 강도를 분류."
    g_dist = abs(g_score - 5.0)
    i_dist = abs(i_score - 5.0)
    avg_dist = (g_dist + i_dist) / 2
    if avg_dist >= 2.5:
        return "강한", "HIGH"
    elif avg_dist >= 1.0:
        return "보통", "MODERATE"
    else:
        return "약한", "MILD"

def _confidence_pct(g_score, i_score):
    """레짐 판정의 신뢰도(0~100%)를 산출한다.
    중립(5.0)에서 멀수록 높은 신뢰도."""
    g_dist = abs(g_score - 5.0)
    i_dist = abs(i_score - 5.0)
    raw = (g_dist + i_dist) / 2.0  # 0~5.0
    return min(100.0, raw / 5.0 * 100.0)

def classify_regime(growth_score: float, inflation_score: float) -> dict:
    "성장·인플레 점수를 기반으로 4개 레짐 중 하나를 반환."
    g_high = growth_score > 5.0
    i_high = inflation_score > 5.0

    if g_high and i_high:
        key = "overheating"
    elif g_high and not i_high:
        key = "goldilocks"
    elif not g_high and i_high:
        key = "stagflation"
    else:
        key = "recession_risk"

    regime = _REGIME_TABLE[key].copy()
    regime["key"] = key
    label_kr, label_en = _strength_label(growth_score, inflation_score)
    regime["strength_kr"] = label_kr
    regime["strength_en"] = label_en
    regime["confidence"] = _confidence_pct(growth_score, inflation_score)

    # 경계 근접성 (boundary proximity)
    g_margin = abs(growth_score - 5.0)
    i_margin = abs(inflation_score - 5.0)
    regime["g_margin"] = g_margin
    regime["i_margin"] = i_margin
    if g_margin < 0.5 or i_margin < 0.5:
        regime["boundary_warning"] = True
        regime["boundary_note"] = (
            f"⚠️ 경계 근접: 성장={g_margin:.1f}pt, 인플레={i_margin:.1f}pt 차이. "
            f"소폭 데이터 변동으로 레짐 전환 가능."
        )
    else:
        regime["boundary_warning"] = False
        regime["boundary_note"] = ""

    return regime

# ═══════════════════════════════════════════════════════════
# 4. 레짐 전환 조건 분석
# ═══════════════════════════════════════════════════════════

def get_transition_conditions(regime_key: str, g: float, i: float, df) -> list:
    "현 레짐에서 다른 레짐으로 전환되기 위한 조건을 정리."
    conditions = []
    g_gap = g - 5.0   # 양이면 성장 높음
    i_gap = i - 5.0   # 양이면 인플레 높음

    if regime_key == "overheating":
        conditions.append(f"→ ✨ Goldilocks: 인플레 {abs(i_gap):.1f}pt 하락 필요 "
                          f"(Core PCE 둔화, 원자재 안정)")
        conditions.append(f"→ ⚠️ Stagflation: 성장 {abs(g_gap):.1f}pt 하락 필요 "
                          f"(고용 둔화, GDP 하향)")
    elif regime_key == "goldilocks":
        conditions.append(f"→ 🔥 Overheating: 인플레 {abs(i_gap):.1f}pt 상승 필요 "
                          f"(유가 급등, 임금 상승 가속)")
        conditions.append(f"→ ❄️ Recession: 성장 {abs(g_gap):.1f}pt 하락 필요 "
                          f"(고용 급감, 소비 위축)")
    elif regime_key == "stagflation":
        conditions.append(f"→ 🔥 Overheating: 성장 {abs(g_gap):.1f}pt 상승 필요 "
                          f"(GDP 반등, 고용 회복)")
        conditions.append(f"→ ❄️ Recession: 인플레 {abs(i_gap):.1f}pt 하락 필요 "
                          f"(유가·원자재 급락, 수요 위축)")
    elif regime_key == "recession_risk":
        conditions.append(f"→ ✨ Goldilocks: 성장 {abs(g_gap):.1f}pt 상승 필요 "
                          f"(정책 부양, 고용 반등)")
        conditions.append(f"→ ⚠️ Stagflation: 인플레 {abs(i_gap):.1f}pt 상승 필요 "
                          f"(공급 충격, 비용 상승)")

    return conditions

# ═══════════════════════════════════════════════════════════
# 5. 마크다운 생성
# ═══════════════════════════════════════════════════════════

def _score_bar(score, width=20):
    "0~10 점수를 시각 바로 변환."
    filled = int(round(score / 10 * width))
    return "█" * filled + "░" * (width - filled)

def _component_table(title, result):
    "구성요소 표를 마크다운으로 생성."
    lines = []
    lines.append(f"### {title} — **{result['score']:.1f} / 10**\n")
    lines.append(f"{_score_bar(result['score'])} {result['score']:.1f}\n")
    lines.append("| 구성요소 | 시리즈 | 값 | 기여 |")
    lines.append("|----------|--------|----|------|")
    for c in result["components"]:
        val_str = _fmt(c["value"]) if c["value"] is not None else "N/A"
        cont_str = f"{c['contrib']:+.2f}" if c["contrib"] != 0 else "0.00"
        lines.append(f"| {c['name']} | {c['series']} | {val_str} | {cont_str} |")
    lines.append("")
    return "\n".join(lines)

def generate_markdown(growth: dict, inflation: dict, regime: dict,
                      transitions: list, generated_at: str) -> str:
    g = growth["score"]
    i = inflation["score"]

    lines = []
    lines.append("# 🏛️ FRED Macro Regime Report")
    lines.append(f"> Generated: {generated_at}\n")

    # 레짐 요약
    lines.append("## 📊 현재 레짐\n")
    lines.append(f"### {regime['emoji']} {regime['regime']}\n")
    lines.append(f"- **강도**: {regime['strength_kr']} ({regime['strength_en']})")
    lines.append(f"- **신뢰도**: {regime['confidence']:.0f}%")
    lines.append(f"- **성장 점수**: {g:.1f} / 10")
    lines.append(f"- **인플레 점수**: {i:.1f} / 10")
    lines.append(f"- **시사점**: {regime['description']}")
    if regime.get("boundary_warning"):
        lines.append(f"\n{regime['boundary_note']}")
    lines.append("")

    # 점수 시각화
    lines.append("## 📐 2×2 레짐 맵\n")
    lines.append("```")
    lines.append("          인플레 ↑ (>5)")
    lines.append("               │")
    lines.append("  ⚠️ Stagflation │ 🔥 Overheating")
    lines.append("   (성장↓ 인플레↑) │ (성장↑ 인플레↑)")
    lines.append("─────────────┼──────────────  성장 →")
    lines.append("  ❄️ Recession  │ ✨ Goldilocks")
    lines.append("   (성장↓ 인플레↓) │ (성장↑ 인플레↓)")
    lines.append("               │")
    lines.append("          인플레 ↓ (≤5)")
    lines.append(f"\n  → 현재 위치: 성장={g:.1f}, 인플레={i:.1f}")
    lines.append("```\n")

    # 구성요소 상세
    lines.append("## 📈 성장 점수 상세\n")
    lines.append(_component_table("성장 점수", growth))
    lines.append("## 📈 인플레 점수 상세\n")
    lines.append(_component_table("인플레 점수", inflation))

    # 전환 조건
    lines.append("## 🔄 레짐 전환 조건\n")
    for t in transitions:
        lines.append(f"- {t}")
    lines.append("")

    # 메타데이터
    lines.append("---")
    lines.append(f"*v3 — 성장 10요소, 인플레 10요소, ±1.5pt cap, 신뢰도 포함*")

    return "\n".join(lines)

# ═══════════════════════════════════════════════════════════
# main
# ═══════════════════════════════════════════════════════════

def main():
    print("🏛️  Fred_regime.py 시작 (v3)")
    df = load_data()
    print(f"  ✅ {len(df)}개 시리즈 로드 완료")

    growth    = calc_growth_score(df)
    inflation = calc_inflation_score(df)
    print(f"  📊 성장 점수: {growth['score']:.1f} / 10")
    print(f"  📊 인플레 점수: {inflation['score']:.1f} / 10")

    regime = classify_regime(growth["score"], inflation["score"])
    print(f"  📊 레짐: {regime['emoji']} {regime['regime']} "
          f"({regime['strength_kr']}, 신뢰도 {regime['confidence']:.0f}%)")
    if regime.get("boundary_warning"):
        print(f"  {regime['boundary_note']}")

    transitions = get_transition_conditions(
        regime["key"], growth["score"], inflation["score"], df)

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    md = generate_markdown(growth, inflation, regime, transitions, generated_at)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(md, encoding="utf-8")
    print(f"  ✅ {OUTPUT_PATH} 저장 완료 ({len(md):,}자)")

if __name__ == "__main__":
    main()
