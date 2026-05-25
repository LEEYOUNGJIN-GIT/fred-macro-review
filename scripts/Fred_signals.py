#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fred_signals.py – FRED 기반 18개 매크로 파생 신호 대시보드 (v3)
═══════════════════════════════════════════════════════════════
v3: W-01~W-06 수정, 신호 14→18개 확장
"""
import pandas as pd
import numpy as np
from datetime import datetime, timezone
from pathlib import Path
from collections import OrderedDict

BASE_DIR    = Path(__file__).resolve().parent.parent
CSV_PATH    = BASE_DIR / "data" / "fred_latest.csv"
OUTPUT_PATH = BASE_DIR / "data" / "fred_signals.md"

def load_data() -> pd.DataFrame:
    df = pd.read_csv(CSV_PATH, dtype={"series_id": str})
    df.set_index("series_id", inplace=True)
    for c in ["latest_value", "chg_prev", "chg_mid", "chg_yoy"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

def safe_val(df, sid, col="latest_value"):
    if sid not in df.index: return None
    v = df.at[sid, col]
    if isinstance(v, pd.Series): v = v.iloc[0]
    if pd.isna(v): return None
    return float(v)

def _fmt(v, suffix="", decimal=2):
    if v is None: return "N/A"
    if v != 0: return f"{v:+.{decimal}f}{suffix}"
    return f"{v:.{decimal}f}{suffix}"

# ═══ 1. Yield Curve (W-06: T10Y3M 보조) ═══
def calc_yield_curve(df):
    s2y = safe_val(df, "T10Y2Y"); s3m = safe_val(df, "T10Y3M")
    p = s2y if s2y is not None else s3m
    if p is None: return {"status":"N/A","value":None,"detail":"데이터 없음","series":["T10Y2Y","T10Y3M"]}
    if p < -0.5: st = "심각한 역전"
    elif p < 0: st = "역전"
    elif p < 0.5: st = "플랫"
    elif p > 1.5: st = "가파름"
    else: st = "정상"
    d = [f"10Y-2Y={_fmt(s2y,'%')}"]
    if s3m is not None: d.append(f"10Y-3M={_fmt(s3m,'%')}")
    if s2y is not None and s3m is not None and ((s2y>0>s3m) or (s3m>0>s2y)): d.append("⚠️신호불일치")
    return {"status":st,"value":p,"detail":", ".join(d),"series":["T10Y2Y","T10Y3M"]}

# ═══ 2. Sahm Rule ═══
def calc_sahm_rule(df):
    sahm = safe_val(df, "SAHMREALTIME"); ur_yoy = safe_val(df, "UNRATE", "chg_yoy")
    if sahm is not None: val, src = sahm, f"Sahm={sahm:.2f}"
    elif ur_yoy is not None: val, src = ur_yoy, f"UR YoY Δ={ur_yoy:+.1f}%p(대체)"
    else: return {"status":"N/A","value":None,"detail":"데이터 없음","series":["SAHMREALTIME","UNRATE"]}
    if val >= 1.0: st = "발동(심각)"
    elif val >= 0.5: st = "발동"
    elif val >= 0.3: st = "임계 근접"
    else: st = "안정"
    return {"status":st,"value":val,"detail":src,"series":["SAHMREALTIME","UNRATE"]}

# ═══ 3. Real Rate Gap ═══
def calc_real_rate_gap(df):
    ff = safe_val(df, "DFF"); pce = safe_val(df, "PCEPILFE", "chg_yoy")
    if ff is None or pce is None: return {"status":"N/A","value":None,"detail":"데이터 부족","series":["DFF","PCEPILFE"]}
    gap = round(ff - pce, 2)
    if gap >= 2.5: st = "강한 긴축"
    elif gap >= 1.5: st = "긴축적"
    elif gap >= 0.5: st = "중립"
    elif gap >= -0.5: st = "완화적"
    else: st = "강한 완화"
    return {"status":st,"value":gap,"detail":f"FFR={ff:.2f}% − CorePCE={pce:.2f}% = {gap:+.2f}%p","series":["DFF","PCEPILFE"]}

# ═══ 4. TIPS Real Rate ═══
def calc_tips_real_rate(df):
    tips = safe_val(df, "DFII10"); cm = safe_val(df, "DFII10", "chg_mid")
    if tips is None: return {"status":"N/A","value":None,"detail":"데이터 없음","series":["DFII10"]}
    if tips >= 2.5: st = "강한 긴축"
    elif tips >= 1.5: st = "긴축적"
    elif tips >= 0.5: st = "중립"
    elif tips >= 0: st = "완화적"
    else: st = "강한 완화"
    tr = ""
    if cm is not None: tr = " ↑상승" if cm > 0.3 else (" ↓하락" if cm < -0.3 else " →횡보")
    d = f"TIPS 10Y={tips:.2f}%{tr}"
    if cm is not None: d += f" (4W Δ={cm:+.2f}%p)"
    return {"status":st,"value":tips,"detail":d,"series":["DFII10"]}

# ═══ 5. VIX (W-02: pt단위, W-06: HY OAS 보조) ═══
def calc_vix_regime(df):
    vix = safe_val(df, "VIXCLS"); vy = safe_val(df, "VIXCLS", "chg_yoy"); hy = safe_val(df, "BAMLH0A0HYM2")
    if vix is None: return {"status":"N/A","value":None,"detail":"데이터 없음","series":["VIXCLS","BAMLH0A0HYM2"]}
    if vix >= 40: st = "패닉"
    elif vix >= 30: st = "위기"
    elif vix >= 20: st = "불안"
    elif vix >= 15: st = "정상"
    else: st = "과도 낙관"
    d = [f"VIX={vix:.1f}"]
    if vy is not None: d.append(f"YoY={vy:+.1f}pt")
    if hy is not None: d.append(f"HY OAS={hy:.2f}%")
    if hy is not None and hy >= 5.0 and vix < 25: d.append("⚠️신용↔VIX괴리")
    return {"status":st,"value":vix,"detail":", ".join(d),"series":["VIXCLS","BAMLH0A0HYM2"]}

# ═══ 6. Inflation Regime ═══
def calc_inflation_regime(df):
    cp = safe_val(df, "PCEPILFE", "chg_yoy"); ci = safe_val(df, "CPIAUCSL", "chg_yoy"); pp = safe_val(df, "PPIFIS", "chg_yoy")
    vals = [v for v in [cp, ci, pp] if v is not None]
    if not vals: return {"status":"N/A","value":None,"detail":"데이터 없음","series":["PCEPILFE","CPIAUCSL","PPIFIS"]}
    avg = sum(vals)/len(vals)
    if avg >= 5.0: st = "초고인플레"
    elif avg >= 3.5: st = "고인플레"
    elif avg >= 2.5: st = "목표 초과"
    elif avg >= 1.5: st = "목표 부근"
    elif avg >= 0: st = "목표 하회"
    else: st = "디플레"
    d = []
    if cp is not None: d.append(f"CorePCE={cp:.2f}%")
    if ci is not None: d.append(f"CPI={ci:.2f}%")
    if pp is not None: d.append(f"PPI={pp:.2f}%")
    d.append(f"평균={avg:.2f}%")
    return {"status":st,"value":round(avg,2),"detail":", ".join(d),"series":["PCEPILFE","CPIAUCSL","PPIFIS"]}

# ═══ 7. Inflation Expectations ═══
def calc_inflation_expectations(df):
    mich = safe_val(df, "MICH"); t5y = safe_val(df, "T5YIE"); t5f = safe_val(df, "T5YIFR")
    score = 0
    d = []
    if mich is not None:
        d.append(f"MICH={mich:.1f}%")
        if mich >= 4.0: score += 2
        elif mich >= 3.5: score += 1
    if t5y is not None:
        d.append(f"5Y BEI={t5y:.2f}%")
        if t5y > 2.8: score += 1
    if t5f is not None:
        d.append(f"5Y5Y={t5f:.2f}%")
        if t5f > 2.5: score += 1
    if not d: return {"status":"N/A","value":None,"detail":"데이터 없음","series":["MICH","T5YIE","T5YIFR"]}
    if score >= 4: st = "디앵커링(심각)"
    elif score >= 3: st = "디앵커링 경계"
    elif score >= 2: st = "상향 이탈"
    else: st = "앵커링 유지"
    d.append(f"점수={score}")
    return {"status":st,"value":score,"detail":", ".join(d),"series":["MICH","T5YIE","T5YIFR"]}

# ═══ 8. Credit Stress ═══
def calc_credit_stress(df):
    hy = safe_val(df, "BAMLH0A0HYM2"); baa = safe_val(df, "BAA10Y"); drc = safe_val(df, "DRCCLACBS")
    if hy is None: return {"status":"N/A","value":None,"detail":"데이터 없음","series":["BAMLH0A0HYM2","BAA10Y","DRCCLACBS"]}
    if hy >= 6.0: st = "위기"
    elif hy >= 5.0: st = "경계"
    elif hy >= 4.0: st = "주의"
    else: st = "양호"
    d = [f"HY OAS={hy:.2f}%"]
    if baa is not None: d.append(f"BAA-10Y={baa:.2f}%")
    if drc is not None: d.append(f"카드연체={drc:.1f}%")
    return {"status":st,"value":hy,"detail":", ".join(d),"series":["BAMLH0A0HYM2","BAA10Y","DRCCLACBS"]}

# ═══ 9. Financial Stress ═══
def calc_financial_stress(df):
    nf = safe_val(df, "NFCI"); st4 = safe_val(df, "STLFSI4"); kc = safe_val(df, "KCFSI")
    vals = [v for v in [nf, st4, kc] if v is not None]
    if not vals: return {"status":"N/A","value":None,"detail":"데이터 없음","series":["NFCI","STLFSI4","KCFSI"]}
    avg = sum(vals)/len(vals)
    if avg >= 1.0: st = "심각한 스트레스"
    elif avg >= 0.5: st = "스트레스"
    elif avg >= 0: st = "주의"
    elif avg >= -0.5: st = "양호"
    else: st = "완화"
    d = []
    if nf is not None: d.append(f"NFCI={nf:.3f}")
    if st4 is not None: d.append(f"STLFSI={st4:.3f}")
    if kc is not None: d.append(f"KCFSI={kc:.3f}")
    d.append(f"평균={avg:.3f}")
    return {"status":st,"value":round(avg,3),"detail":", ".join(d),"series":["NFCI","STLFSI4","KCFSI"]}

# ═══ 10. Labor Market (W-05: 천명 표시) ═══
def calc_labor_market(df):
    ur = safe_val(df, "UNRATE"); nfp = safe_val(df, "PAYEMS", "chg_prev")
    icsa = safe_val(df, "ICSA"); jolt = safe_val(df, "JTSJOL"); civ = safe_val(df, "CIVPART")
    score = 5.0
    d = []
    if ur is not None:
        d.append(f"실업률={ur:.1f}%")
        if ur <= 3.5: score += 1.5
        elif ur <= 4.0: score += 0.5
        elif ur >= 5.5: score -= 2.0
        elif ur >= 5.0: score -= 1.0
    if nfp is not None:
        d.append(f"NFP={nfp:+,.0f}천명")  # W-05
        if nfp >= 200: score += 1.5
        elif nfp >= 100: score += 0.5
        elif nfp <= 0: score -= 2.0
        elif nfp <= 50: score -= 1.0
    if icsa is not None:
        d.append(f"실업청구={icsa:,.0f}건")
        if icsa <= 200000: score += 0.5
        elif icsa >= 350000: score -= 1.5
        elif icsa >= 300000: score -= 0.5
    if jolt is not None:
        d.append(f"구인={jolt:,.0f}K")
        if jolt >= 10000: score += 0.5
        elif jolt <= 5000: score -= 1.0
    if civ is not None:
        d.append(f"경활={civ:.1f}%")
    score = max(0, min(10, score))
    if score >= 7: st = "견조"
    elif score >= 5.5: st = "양호"
    elif score >= 4: st = "냉각"
    elif score >= 2.5: st = "약화"
    else: st = "심각한 위축"
    d.append(f"점수={score:.1f}")
    return {"status":st,"value":score,"detail":", ".join(d),"series":["UNRATE","PAYEMS","ICSA","JTSJOL","CIVPART"]}

# ═══ 11. Liquidity (W-01: WALCL YoY %) ═══
def calc_liquidity(df):
    rrp = safe_val(df, "RRPONTSYD"); res = safe_val(df, "TOTRESNS")
    # WALCL chg_yoy는 절대 변화(Mil.USD). 전년 수준으로 나눠 YoY% 환산 필요.
    walcl_level = safe_val(df, "WALCL")
    walcl_abs = safe_val(df, "WALCL", "chg_yoy")
    base_y = safe_val(df, "BOGMBASE", "chg_yoy")
    walcl_y = None
    if walcl_level is not None and walcl_abs is not None:
        prev = walcl_level - walcl_abs
        if prev and prev != 0:
            walcl_y = round(walcl_abs / abs(prev) * 100, 2)
    score = 5.0
    d = []
    if rrp is not None:
        d.append(f"RRP=${rrp:.1f}B")
        if rrp <= 10: score -= 1.0
        elif rrp <= 50: score -= 0.5
        elif rrp >= 500: score += 1.0
    if res is not None:
        d.append(f"준비금=${res:.0f}B")
        if res <= 2800: score -= 1.0
        elif res <= 3000: score -= 0.5
        elif res >= 3500: score += 0.5
    if walcl_y is not None:
        d.append(f"Fed자산YoY={walcl_y:+.1f}%")
        if walcl_y <= -10: score -= 1.0
        elif walcl_y < 0: score -= 0.5
        elif walcl_y >= 10: score += 1.0
        elif walcl_y > 5: score += 0.5
    if base_y is not None:
        d.append(f"본원통화YoY={base_y:+.1f}%")
        if base_y < -5: score -= 0.5
        elif base_y > 10: score += 0.5
    score = max(0, min(10, score))
    if score >= 7: st = "과잉"
    elif score >= 5.5: st = "양호"
    elif score >= 4: st = "주의"
    elif score >= 2.5: st = "위축"
    else: st = "소진"
    d.append(f"점수={score:.1f}")
    return {"status":st,"value":score,"detail":", ".join(d),"series":["RRPONTSYD","TOTRESNS","WALCL","BOGMBASE"]}

# ═══ 12. Commodity Pressure ═══
def calc_commodity_pressure(df):
    wti = safe_val(df, "DCOILWTICO"); cy = safe_val(df, "PALLFNFINDEXM", "chg_yoy")
    cu = safe_val(df, "PCOPPUSDM")
    pressure = 0.0
    d = []
    if wti is not None:
        d.append(f"WTI=${wti:.1f}")
        if wti >= 100: pressure += 2
        elif wti >= 80: pressure += 1
        elif wti <= 40: pressure -= 2
        elif wti <= 60: pressure -= 1
    if cy is not None:
        d.append(f"원자재YoY={cy:+.1f}%")
        if cy >= 30: pressure += 2
        elif cy >= 15: pressure += 1
        elif cy <= -20: pressure -= 2
        elif cy <= -10: pressure -= 1
    if cu is not None:
        d.append(f"구리=${cu:,.0f}/MT")
    if not d: return {"status":"N/A","value":None,"detail":"데이터 없음","series":["DCOILWTICO","PALLFNFINDEXM","PCOPPUSDM"]}
    if pressure >= 3: st = "강한 압력"
    elif pressure >= 1: st = "상방 압력"
    elif pressure <= -3: st = "하방 압력"
    elif pressure <= -1: st = "하방 압력"
    else: st = "중립"
    d.append(f"압력={pressure:+.0f}")
    return {"status":st,"value":pressure,"detail":", ".join(d),"series":["DCOILWTICO","PALLFNFINDEXM","PCOPPUSDM"]}

# ═══ 13. Dollar Trend ═══
def calc_dollar_trend(df):
    dxy_y = safe_val(df, "DTWEXBGS", "chg_yoy"); dxy = safe_val(df, "DTWEXBGS"); krw = safe_val(df, "DEXKOUS")
    if dxy is None: return {"status":"N/A","value":None,"detail":"데이터 없음","series":["DTWEXBGS","DEXKOUS"]}
    d = [f"DXY={dxy:.1f}"]
    if dxy_y is not None:
        d.append(f"YoY={dxy_y:+.1f}pt")
        if dxy_y >= 5: st = "강한 강세"
        elif dxy_y >= 2: st = "약한 강세"
        elif dxy_y <= -5: st = "강한 약세"
        elif dxy_y <= -2: st = "약한 약세"
        else: st = "중립"
    else:
        st = "중립"
    if krw is not None: d.append(f"USD/KRW={krw:,.0f}")
    return {"status":st,"value":dxy_y,"detail":", ".join(d),"series":["DTWEXBGS","DEXKOUS"]}

# ═══ 14. Consumer Sentiment (W-06: MICH 보조) ═══
def calc_consumer_sentiment(df):
    umcs = safe_val(df, "UMCSENT"); uy = safe_val(df, "UMCSENT", "chg_yoy"); mich = safe_val(df, "MICH")
    if umcs is None: return {"status":"N/A","value":None,"detail":"데이터 없음","series":["UMCSENT","MICH"]}
    if umcs >= 80: st = "견조"
    elif umcs >= 70: st = "양호"
    elif umcs >= 60: st = "냉각"
    elif umcs >= 50: st = "불안"
    else: st = "심각한 위축"
    d = [f"UMCS={umcs:.1f}"]
    if uy is not None: d.append(f"YoY={uy:+.1f}pt")
    if mich is not None: d.append(f"인플레기대={mich:.1f}%")
    if mich is not None and mich >= 4.0 and umcs < 60: d.append("⚠️심리↓+기대↑ 괴리")
    return {"status":st,"value":umcs,"detail":", ".join(d),"series":["UMCSENT","MICH"]}

# ═══ 15. Housing Market (NEW) ═══
def calc_housing_market(df):
    mort = safe_val(df, "MORTGAGE30US"); houst = safe_val(df, "HOUST")
    perm = safe_val(df, "PERMIT"); cs_y = safe_val(df, "CSUSHPINSA", "chg_yoy")
    score = 5.0; d = []
    if mort is not None:
        d.append(f"모기지30Y={mort:.2f}%")
        if mort >= 7.5: score -= 1.5
        elif mort >= 6.5: score -= 0.5
        elif mort <= 5.0: score += 1.5
        elif mort <= 5.5: score += 0.5
    if houst is not None:
        d.append(f"착공={houst:.0f}K")
        if houst >= 1500: score += 1.0
        elif houst >= 1200: score += 0.5
        elif houst <= 800: score -= 1.5
        elif houst <= 1000: score -= 0.5
    if perm is not None:
        d.append(f"허가={perm:.0f}K")
    if cs_y is not None:
        d.append(f"주택가격YoY={cs_y:+.1f}%")
        if cs_y >= 15: score += 0.5
        elif cs_y >= 5: score += 0.25
        elif cs_y <= -5: score -= 1.0
        elif cs_y <= 0: score -= 0.5
    score = max(0, min(10, score))
    if not d: return {"status":"N/A","value":None,"detail":"데이터 없음","series":["MORTGAGE30US","HOUST","PERMIT","CSUSHPINSA"]}
    if score >= 7: st = "활황"
    elif score >= 5.5: st = "양호"
    elif score >= 4: st = "냉각"
    elif score >= 2.5: st = "약화"
    else: st = "심각한 위축"
    d.append(f"점수={score:.1f}")
    return {"status":st,"value":score,"detail":", ".join(d),"series":["MORTGAGE30US","HOUST","PERMIT","CSUSHPINSA"]}

# ═══ 16. Trade & Fiscal (NEW) ═══
def calc_trade_fiscal(df):
    tb = safe_val(df, "BOPGSTB"); fsd = safe_val(df, "FYFSD")
    d = []
    concern = 0
    if tb is not None:
        d.append(f"무역수지=${tb:,.0f}M")
        if tb < -80000: concern += 2
        elif tb < -60000: concern += 1
    if fsd is not None:
        d.append(f"재정적자=${fsd:,.0f}M")
        if fsd < -1500000: concern += 2
        elif fsd < -1000000: concern += 1
    if not d: return {"status":"N/A","value":None,"detail":"데이터 없음","series":["BOPGSTB","FYFSD"]}
    if concern >= 3: st = "심각한 적자"
    elif concern >= 2: st = "경계"
    elif concern >= 1: st = "주의"
    else: st = "양호"
    return {"status":st,"value":concern,"detail":", ".join(d),"series":["BOPGSTB","FYFSD"]}

# ═══ 17. Korea Cross (NEW) ═══
def calc_korea_cross(df):
    ts = safe_val(df, "KOR_US_10Y_SPREAD")
    cli = safe_val(df, "KORLOLITOAASTSAM")
    krw = safe_val(df, "DEXKOUS")
    score = 5.0; d = []
    if ts is not None:
        d.append(f"10Y금리차={ts:+.2f}%p")
        if ts < -1.5: score -= 1.0
        elif ts < -0.5: score -= 0.5
    if cli is not None:
        d.append(f"CLI={cli:.1f}")
        if cli >= 101: score += 1.0
        elif cli >= 100: score += 0.5
        elif cli <= 98: score -= 1.5
        elif cli <= 99: score -= 0.5
    if krw is not None:
        d.append(f"USD/KRW={krw:,.0f}")
        if krw >= 1450: score -= 1.0
        elif krw >= 1350: score -= 0.5
        elif krw <= 1150: score += 0.5
    score = max(0, min(10, score))
    if not d: return {"status":"N/A","value":None,"detail":"데이터 없음","series":["KOR_US_10Y_SPREAD","KORLOLITOAASTSAM","DEXKOUS"]}
    if score >= 7: st = "양호"
    elif score >= 5.5: st = "중립"
    elif score >= 4: st = "주의"
    elif score >= 2.5: st = "경계"
    else: st = "위기(한국)"
    d.append(f"점수={score:.1f}")
    return {"status":st,"value":score,"detail":", ".join(d),"series":["KOR_US_10Y_SPREAD","KORLOLITOAASTSAM","DEXKOUS"]}

# ═══ 18. Consumption (NEW) ═══
def calc_consumption(df):
    sav = safe_val(df, "PSAVERT"); pce_y = safe_val(df, "PCEC96", "chg_yoy"); auto = safe_val(df, "TOTALSA")
    score = 5.0; d = []
    if sav is not None:
        d.append(f"저축률={sav:.1f}%")
        if sav < 3: score += 0.5  # 과소비 → 단기 소비 강세
        elif sav > 10: score -= 1.0  # 예비적 저축 → 소비 위축
    if pce_y is not None:
        d.append(f"실질소비YoY={pce_y:+.1f}%")
        if pce_y >= 3.0: score += 1.5
        elif pce_y >= 2.0: score += 0.5
        elif pce_y <= 0: score -= 2.0
        elif pce_y <= 1.0: score -= 0.5
    if auto is not None:
        d.append(f"자동차={auto:.1f}M대")
        if auto >= 17: score += 0.5
        elif auto >= 16: score += 0.25
        elif auto <= 13: score -= 1.0
        elif auto <= 14: score -= 0.5
    score = max(0, min(10, score))
    if not d: return {"status":"N/A","value":None,"detail":"데이터 없음","series":["PSAVERT","PCEC96","TOTALSA"]}
    if score >= 7: st = "견조"
    elif score >= 5.5: st = "양호"
    elif score >= 4: st = "냉각"
    elif score >= 2.5: st = "약화"
    else: st = "심각한 위축"
    d.append(f"점수={score:.1f}")
    return {"status":st,"value":score,"detail":", ".join(d),"series":["PSAVERT","PCEC96","TOTALSA"]}

# ═══ STATUS → RISK LEVEL (W-03: "위기" Level 5 통일) ═══
_STATUS_LEVEL = {
    "심각한 역전": 5, "발동(심각)": 5, "강한 긴축": 5, "패닉": 5,
    "초고인플레": 5, "디앵커링(심각)": 5, "위기": 5, "심각한 스트레스": 5,
    "심각한 위축": 5, "소진": 5, "강한 압력": 5, "심각한 적자": 5, "위기(한국)": 5,
    "역전": 4, "발동": 4, "긴축적": 4, "고인플레": 4,
    "디앵커링 경계": 4, "경계": 4, "스트레스": 4, "약화": 4,
    "강한 강세": 4, "강한 약세": 4, "위축": 4,
    "플랫": 3, "임계 근접": 3, "목표 초과": 3, "상향 이탈": 3,
    "주의": 3, "냉각": 3, "불안": 3, "상방 압력": 3,
    "약한 강세": 3, "약한 약세": 3,
    "정상": 2, "중립": 2, "목표 부근": 2, "앵커링 유지": 2,
    "양호": 2, "완화": 2, "활황": 2,
    "가파름": 1, "안정": 1, "완화적": 1, "강한 완화": 1,
    "목표 하회": 1, "과도 낙관": 1, "과도 완화": 1, "과잉": 1,
    "하방 압력": 1, "낙관": 1, "견조": 1, "디플레": 1,
}
_LEVEL_LABEL = {5: "위험 (Critical)", 4: "경계 (High)", 3: "주의 (Elevated)", 2: "관심 (Guarded)", 1: "안정 (Low)"}
_LEVEL_EMOJI = {5: "🔴", 4: "🟠", 3: "🟡", 2: "🔵", 1: "🟢", 0: "⚪"}

def calc_overall_risk(signals):
    levels = []
    for name, sig in signals.items():
        lv = _STATUS_LEVEL.get(sig.get("status", "N/A"))
        if lv is not None: levels.append(lv)
    if not levels: return {"level": 0, "label": "N/A", "emoji": "⚪", "score": 0}
    avg = sum(levels) / len(levels)
    mx = max(levels)
    composite = 0.7 * avg + 0.3 * mx
    risk_lv = int(round(composite))
    risk_lv = max(1, min(5, risk_lv))
    return {"level": risk_lv, "label": _LEVEL_LABEL.get(risk_lv, "?"),
            "emoji": _LEVEL_EMOJI.get(risk_lv, "⚪"), "score": round(composite, 2),
            "avg": round(avg, 2), "max": mx, "count": len(levels)}

_SIGNAL_NAMES = OrderedDict([
    ("yield_curve",      "장단기 스프레드"),   ("sahm_rule",        "Sahm Rule"),
    ("real_rate_gap",    "실질금리 갭"),       ("tips_real_rate",   "TIPS 실질금리"),
    ("vix_regime",       "VIX 레짐"),         ("inflation_regime", "인플레이션 레짐"),
    ("inflation_exp",    "인플레 기대"),       ("credit_stress",    "신용 스트레스"),
    ("financial_stress", "금융 스트레스"),     ("labor_market",     "노동 시장"),
    ("liquidity",        "유동성"),           ("commodity",        "원자재 압력"),
    ("dollar_trend",     "달러 추세"),        ("consumer_sent",    "소비자 심리"),
    ("housing_market",   "주택시장"),         ("trade_fiscal",     "무역·재정"),
    ("korea_cross",      "한국 크로스"),       ("consumption",      "소비 동향"),
])

_CALC_MAP = OrderedDict([
    ("yield_curve", calc_yield_curve),     ("sahm_rule", calc_sahm_rule),
    ("real_rate_gap", calc_real_rate_gap),  ("tips_real_rate", calc_tips_real_rate),
    ("vix_regime", calc_vix_regime),        ("inflation_regime", calc_inflation_regime),
    ("inflation_exp", calc_inflation_expectations), ("credit_stress", calc_credit_stress),
    ("financial_stress", calc_financial_stress),     ("labor_market", calc_labor_market),
    ("liquidity", calc_liquidity),          ("commodity", calc_commodity_pressure),
    ("dollar_trend", calc_dollar_trend),    ("consumer_sent", calc_consumer_sentiment),
    ("housing_market", calc_housing_market), ("trade_fiscal", calc_trade_fiscal),
    ("korea_cross", calc_korea_cross),      ("consumption", calc_consumption),
])

def generate_markdown(signals, risk, generated_at):
    L = []
    L.append("# 📡 FRED Macro Signals Dashboard (v3)")
    L.append(f"> Generated: {generated_at}")
    L.append(f"> 18개 신호 종합\n")
    L.append(f"## 종합 위험도: {risk['emoji']} {risk['label']}\n")
    L.append(f"- 종합 점수: **{risk['score']:.2f}** (70%×평균{risk['avg']:.2f} + 30%×최대{risk['max']})")
    L.append(f"- 평가 신호: {risk['count']}개\n")
    L.append("## 📊 신호 요약\n")
    L.append("| # | 신호 | 상태 | 값 | 핵심 요약 |")
    L.append("|---|------|------|----|----------|")
    for i, (key, name) in enumerate(_SIGNAL_NAMES.items(), 1):
        sig = signals.get(key, {})
        st = sig.get("status", "N/A")
        lv = _STATUS_LEVEL.get(st, 0)
        emoji = _LEVEL_EMOJI.get(lv, "⚪")
        val = sig.get("value")
        val_s = f"{val:.2f}" if val is not None else "N/A"
        detail = sig.get("detail", "")
        L.append(f"| {i} | {name} | {emoji} {st} | {val_s} | {detail} |")
    L.append("")
    L.append("## 📋 신호 상세\n")
    for key, name in _SIGNAL_NAMES.items():
        sig = signals.get(key, {})
        st = sig.get("status", "N/A")
        lv = _STATUS_LEVEL.get(st, 0)
        emoji = _LEVEL_EMOJI.get(lv, "⚪")
        L.append(f"### {emoji} {name} — {st}")
        L.append(f"- **값**: {sig.get('value')}")
        L.append(f"- **상세**: {sig.get('detail', '')}")
        L.append(f"- **시리즈**: {', '.join(sig.get('series', []))}\n")
    L.append("---")
    L.append(f"*v3 — 18개 신호, W-01~W-06 수정, 주택/무역/한국/소비 확장*")
    return "\n".join(L)

def main():
    print("📡 Fred_signals.py 시작 (v3 — 18개 신호)")
    df = load_data()
    print(f"  ✅ {len(df)}개 시리즈 로드 완료")
    signals = {}
    for key, func in _CALC_MAP.items():
        signals[key] = func(df)
        st = signals[key].get("status", "N/A")
        lv = _STATUS_LEVEL.get(st, 0)
        print(f"  {_LEVEL_EMOJI.get(lv,'⚪')} {_SIGNAL_NAMES[key]}: {st}")
    risk = calc_overall_risk(signals)
    print(f"\n  🎯 종합 위험도: {risk['emoji']} {risk['label']} ({risk['score']:.2f})")
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    md = generate_markdown(signals, risk, generated_at)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(md, encoding="utf-8")
    print(f"  ✅ {OUTPUT_PATH} 저장 완료 ({len(md):,}자)")

if __name__ == "__main__":
    main()
