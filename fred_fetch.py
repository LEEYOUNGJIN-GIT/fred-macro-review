#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FRED API 거시경제 팩트 테이블 자동 생성 스크립트 (풀 버전)
──────────────────────────────────────────────────────────
• 77개 FRED 시리즈 + 1개 파생지표(구리/금 비율) = 78개 매크로 지표
• 15개 카테고리별 팩트 테이블을 Markdown + CSV로 저장
• GitHub Actions + claude.ai GitHub Integration 연동 목적

사용법:
    export FRED_API_KEY="your-api-key"
    python fred_fetch.py
"""

import os
import sys
import time
import json
import requests
import pandas as pd
from datetime import datetime, timedelta, timezone
from pathlib import Path


# ═══════════════════════════════════════════════════════════
# 1. 환경 설정
# ═══════════════════════════════════════════════════════════

FRED_API_KEY = os.environ.get("FRED_API_KEY", "")
if not FRED_API_KEY:
    print("❌ FRED_API_KEY 환경변수가 설정되지 않았습니다.")
    sys.exit(1)

FRED_BASE_URL = "https://api.stlouisfed.org/fred/series/observations"
REQUEST_DELAY = 0.5  # FRED API rate limit 준수
END_DATE = datetime.today().strftime("%Y-%m-%d")
START_DATE = (datetime.today() - timedelta(days=1095)).strftime("%Y-%m-%d")


# ═══════════════════════════════════════════════════════════
# 2. 시리즈 레지스트리 (78개)
# ═══════════════════════════════════════════════════════════
# tf 필드: level=원값, yoy_pct=YoY% 변환, mom_pct=MoM%,
#          mom_diff=전월차, calculated=파생

REG = {
    # ── 01_금리채권 (15개) ──
    "T10Y2Y":   {"cat":"01_금리채권","kr":"장단기 스프레드(10Y-2Y)","en":"10Y-2Y Treasury Spread","freq":"D","unit":"%","src":"Fed","tf":"level","note":"음수=역전=침체 경고"},
    "DFII10":   {"cat":"01_금리채권","kr":"10Y 실질금리(TIPS)","en":"10Y TIPS Yield","freq":"D","unit":"%","src":"Fed","tf":"level","note":"실질 자금조달 비용. 2%↑ 긴축적"},
    "T10YIE":   {"cat":"01_금리채권","kr":"10Y BEI","en":"10Y Breakeven Inflation","freq":"D","unit":"%","src":"Fed","tf":"level","note":"시장 10년 인플레 기대. 2~2.5% 정상"},
    "T5YIE":    {"cat":"01_금리채권","kr":"5Y BEI","en":"5Y Breakeven Inflation","freq":"D","unit":"%","src":"Fed","tf":"level","note":"중기 인플레이션 기대"},
    "T5YIFR":   {"cat":"01_금리채권","kr":"5Y5Y 선도 인플레 기대","en":"5Y5Y Forward Inflation","freq":"D","unit":"%","src":"Fed","tf":"level","note":"Fed 최중시 장기 인플레 앵커링. 2~2.5% 정상"},
    "DGS2":     {"cat":"01_금리채권","kr":"미국채 2년물","en":"2Y Treasury Yield","freq":"D","unit":"%","src":"Fed","tf":"level","note":"단기 금리 기대. Fed 정책 민감"},
    "DGS10":    {"cat":"01_금리채권","kr":"미국채 10년물","en":"10Y Treasury Yield","freq":"D","unit":"%","src":"Fed","tf":"level","note":"글로벌 벤치마크 금리"},
    "DGS30":    {"cat":"01_금리채권","kr":"미국채 30년물","en":"30Y Treasury Yield","freq":"D","unit":"%","src":"Fed","tf":"level","note":"초장기 금리. 연금/보험 할인율"},
    "TB3MS":    {"cat":"01_금리채권","kr":"3개월 T-Bill","en":"3M Treasury Bill","freq":"M","unit":"%","src":"Fed","tf":"level","note":"단기 무위험 금리"},
    "DFF":      {"cat":"01_금리채권","kr":"연방기금 실효금리(일간)","en":"Fed Funds Effective Rate","freq":"D","unit":"%","src":"Fed","tf":"level","note":"Fed 기준금리 실시간"},
    "FEDFUNDS": {"cat":"01_금리채권","kr":"연방기금금리(월간)","en":"Fed Funds Rate(Monthly)","freq":"M","unit":"%","src":"Fed","tf":"level","note":"기준금리 월간 평균"},
    "SOFR":     {"cat":"01_금리채권","kr":"SOFR(담보부 익일물)","en":"Secured Overnight Financing Rate","freq":"D","unit":"%","src":"NY Fed","tf":"level","note":"LIBOR 대체 단기 기준금리"},
    "AAA":      {"cat":"01_금리채권","kr":"Aaa 회사채 수익률","en":"Moody's Aaa Corp Bond Yield","freq":"D","unit":"%","src":"Moody's","tf":"level","note":"최우량 기업 조달비용"},
    "BAA":      {"cat":"01_금리채권","kr":"Baa 회사채 수익률","en":"Moody's Baa Corp Bond Yield","freq":"D","unit":"%","src":"Moody's","tf":"level","note":"투자등급 하한 조달비용"},
    "BAA10Y":   {"cat":"01_금리채권","kr":"Baa-10Y 신용 스프레드","en":"Baa-10Y Treasury Spread","freq":"D","unit":"%","src":"Moody's/Fed","tf":"level","note":"기업 디폴트 프리미엄. 3%↑ 경계"},

    # ── 02_리스크신용 (3개) ──
    "VIXCLS":       {"cat":"02_리스크신용","kr":"VIX 공포지수","en":"CBOE VIX","freq":"D","unit":"Index","src":"CBOE","tf":"level","note":"20↑ 불안, 30↑ 위기, 40↑ 패닉"},
    "BAMLH0A0HYM2": {"cat":"02_리스크신용","kr":"하이일드 스프레드(OAS)","en":"ICE BofA US HY OAS","freq":"D","unit":"%","src":"ICE/BofA","tf":"level","note":"400bp↑ 경계, 600bp↑ 위기"},
    "TOTBKCR":      {"cat":"02_리스크신용","kr":"상업은행 총 대출","en":"Bank Credit All Commercial Banks","freq":"W","unit":"Bil.USD","src":"Fed","tf":"yoy_pct","note":"은행 대출 추세. YoY 감소→경기 위축"},

    # ── 03_금융스트레스 (4개) ──
    "NFCI":    {"cat":"03_금융스트레스","kr":"시카고 금융여건지수","en":"Chicago Fed NFCI","freq":"W","unit":"Index","src":"Chicago Fed","tf":"level","note":"0=평균, +=긴축. +1.0↑ 위기"},
    "STLFSI4": {"cat":"03_금융스트레스","kr":"STL 금융스트레스","en":"STL Fed FSI","freq":"W","unit":"Index","src":"STL Fed","tf":"level","note":"0=평균. +1σ↑ 스트레스"},
    "KCFSI":   {"cat":"03_금융스트레스","kr":"KC 금융스트레스","en":"KC Financial Stress Index","freq":"M","unit":"Index","src":"KC Fed","tf":"level","note":"보조 확인용"},
    "CFNAI":   {"cat":"03_금융스트레스","kr":"시카고 경제활동지수","en":"Chicago Fed NAI","freq":"M","unit":"Index","src":"Chicago Fed","tf":"level","note":"85개 변수 종합. -0.7↓=침체 진입"},

    # ── 04_노동시장 (7개) ──
    "UNRATE":        {"cat":"04_노동시장","kr":"실업률","en":"Unemployment Rate","freq":"M","unit":"%","src":"BLS","tf":"level","note":"Sahm Rule: 3M이평 +0.5%p↑=침체"},
    "PAYEMS":        {"cat":"04_노동시장","kr":"비농업 고용자수","en":"Nonfarm Payrolls","freq":"M","unit":"Thousands","src":"BLS","tf":"mom_diff","note":"전월대비. +200K↑ 견조, 0↓ 침체"},
    "ICSA":          {"cat":"04_노동시장","kr":"신규 실업수당 청구","en":"Initial Jobless Claims","freq":"W","unit":"Number","src":"DOL","tf":"level","note":"300K↑ 약화, 250K↓ 견조"},
    "CCSA":          {"cat":"04_노동시장","kr":"계속 실업수당 청구","en":"Continued Claims","freq":"W","unit":"Number","src":"DOL","tf":"level","note":"장기 실업 추세"},
    "JTSJOL":        {"cat":"04_노동시장","kr":"JOLTS 구인건수","en":"JOLTS Job Openings","freq":"M","unit":"Thousands","src":"BLS","tf":"level","note":"V/U ratio로 타이트니스 측정"},
    "CIVPART":       {"cat":"04_노동시장","kr":"경제활동 참가율","en":"Labor Force Participation","freq":"M","unit":"%","src":"BLS","tf":"level","note":"코로나 이전 63.3% 대비"},
    "CES0500000003": {"cat":"04_노동시장","kr":"시간당 평균 임금(민간)","en":"Avg Hourly Earnings","freq":"M","unit":"$/hour","src":"BLS","tf":"yoy_pct","note":"임금 인플레. YoY 4%↑ Fed 경계"},

    # ── 05_물가인플레 (7개) ──
    "CPIAUCSL": {"cat":"05_물가인플레","kr":"CPI 소비자물가","en":"CPI All Urban","freq":"M","unit":"Index","src":"BLS","tf":"yoy_pct","note":"헤드라인 인플레. 2%=목표"},
    "CPILFESL": {"cat":"05_물가인플레","kr":"근원 CPI","en":"Core CPI","freq":"M","unit":"Index","src":"BLS","tf":"yoy_pct","note":"식품·에너지 제외 기조 물가"},
    "PCEPI":    {"cat":"05_물가인플레","kr":"PCE 물가지수","en":"PCE Price Index","freq":"M","unit":"Index","src":"BEA","tf":"yoy_pct","note":"Fed 공식 인플레 타겟"},
    "PCEPILFE": {"cat":"05_물가인플레","kr":"근원 PCE","en":"Core PCE","freq":"M","unit":"Index","src":"BEA","tf":"yoy_pct","note":"★ Fed 최선호 물가. 목표 2.0%"},
    "PPIFIS":   {"cat":"05_물가인플레","kr":"PPI 생산자물가","en":"PPI Final Demand","freq":"M","unit":"Index","src":"BLS","tf":"yoy_pct","note":"기업 비용→CPI 선행 3~6개월"},
    "MICH":     {"cat":"05_물가인플레","kr":"미시간대 인플레 기대","en":"U.Michigan Inflation Exp.","freq":"M","unit":"%","src":"U.Michigan","tf":"level","note":"소비자 기반. 3%↑ 디앵커링 우려"},

    # ── 06_GDP생산 (6개) ──
    "GDP":       {"cat":"06_GDP생산","kr":"명목 GDP","en":"Nominal GDP","freq":"Q","unit":"Bil.USD","src":"BEA","tf":"yoy_pct","note":"경제 규모(명목)"},
    "GDPC1":     {"cat":"06_GDP생산","kr":"실질 GDP","en":"Real GDP","freq":"Q","unit":"Bil.2017USD","src":"BEA","tf":"yoy_pct","note":"2연속 QoQ 음수=기술적 침체"},
    "INDPRO":    {"cat":"06_GDP생산","kr":"산업생산지수","en":"Industrial Production","freq":"M","unit":"Index(2017=100)","src":"Fed","tf":"yoy_pct","note":"제조·광업·유틸리티"},
    "RSAFS":     {"cat":"06_GDP생산","kr":"소매판매","en":"Retail Sales","freq":"M","unit":"Mil.USD","src":"Census","tf":"mom_pct","note":"소비=GDP 70%. MoM 기준"},
    "DGORDER":   {"cat":"06_GDP생산","kr":"내구재 주문","en":"Durable Goods Orders","freq":"M","unit":"Mil.USD","src":"Census","tf":"mom_pct","note":"기업 투자 선행"},
    "CMRMTSPL":  {"cat":"06_GDP생산","kr":"실질 제조업/무역 판매","en":"Real Mfg & Trade Sales","freq":"M","unit":"Mil.USD","src":"Census","tf":"yoy_pct","note":"실질 기업 활동"},

    # ── 07_소비심리통화 (2개) ──
    "UMCSENT": {"cat":"07_소비심리통화","kr":"미시간 소비자심리","en":"U.Michigan Sentiment","freq":"M","unit":"Index","src":"U.Michigan","tf":"level","note":"80↑ 양호, 60↓ 위축"},
    "M2SL":    {"cat":"07_소비심리통화","kr":"M2 통화량","en":"M2 Money Stock","freq":"M","unit":"Bil.USD","src":"Fed","tf":"yoy_pct","note":"YoY 음수→디플레 우려"},

    # ── 08_주택시장 (5개) ──
    "CSUSHPINSA":    {"cat":"08_주택시장","kr":"케이스-쉴러 전국 주택가격","en":"Case-Shiller Home Price","freq":"M","unit":"Index(2000=100)","src":"S&P","tf":"yoy_pct","note":"YoY 20%↑ 과열, 0%↓ 조정"},
    "HOUST":         {"cat":"08_주택시장","kr":"신규주택 착공","en":"Housing Starts","freq":"M","unit":"Thousands","src":"Census","tf":"level","note":"1500K↑ 활황, 1000K↓ 부진"},
    "PERMIT":        {"cat":"08_주택시장","kr":"건축허가","en":"Building Permits","freq":"M","unit":"Thousands","src":"Census","tf":"level","note":"주택착공 선행"},
    "MORTGAGE30US":  {"cat":"08_주택시장","kr":"30년 모기지 금리","en":"30Y Fixed Mortgage","freq":"W","unit":"%","src":"Freddie Mac","tf":"level","note":"7%↑ 수요 급감"},
    "EXHOSLUSM495S": {"cat":"08_주택시장","kr":"기존주택 판매","en":"Existing Home Sales","freq":"M","unit":"Thousands","src":"NAR","tf":"level","note":"거래량/수요 강도"},

    # ── 09_무역국제수지 (5개) ──
    "NETFI":   {"cat":"09_무역국제수지","kr":"경상수지(순금융투자)","en":"Balance on Current Account (NIPA's)","freq":"Q","unit":"Bil.USD","src":"BEA","tf":"level","note":"미국 경상적자 규모"},
    "FYFSD":   {"cat":"09_무역국제수지","kr":"연방 재정적자","en":"Federal Surplus or Deficit","freq":"A","unit":"Mil.USD","src":"Treasury","tf":"level","note":"재정 건전성. 적자확대→장기금리↑"},
    "BOPGSTB": {"cat":"09_무역국제수지","kr":"무역수지","en":"Trade Balance","freq":"M","unit":"Mil.USD","src":"Census","tf":"level","note":"수출-수입. 적자확대→달러약세"},
    "EXPGS":   {"cat":"09_무역국제수지","kr":"실질 수출","en":"Real Exports","freq":"Q","unit":"Bil.USD","src":"BEA","tf":"yoy_pct","note":"수출 동향"},
    "IMPGS":   {"cat":"09_무역국제수지","kr":"실질 수입","en":"Real Imports","freq":"Q","unit":"Bil.USD","src":"BEA","tf":"yoy_pct","note":"수입/내수 강도"},

    # ── 10_환율달러 (5개) ──
    "DEXKOUS":    {"cat":"10_환율달러","kr":"원/달러 환율","en":"USD/KRW","freq":"D","unit":"KRW/USD","src":"Fed","tf":"level","note":"1400↑ 원화약세 경계"},
    "DEXBZUS":    {"cat":"10_환율달러","kr":"헤알/달러 환율","en":"USD/BRL","freq":"D","unit":"BRL/USD","src":"Fed","tf":"level","note":"5.5↑ EM 스트레스"},
    "DTWEXBGS":   {"cat":"10_환율달러","kr":"무역가중 달러지수(광범위)","en":"Trade-Weighted Dollar(Broad)","freq":"D","unit":"Index(2006=100)","src":"Fed","tf":"level","note":"DXY 대용. 26개국 통화 대비"},
    "DTWEXAFEGS": {"cat":"10_환율달러","kr":"선진국 대비 달러","en":"Dollar vs Advanced Econ.","freq":"D","unit":"Index","src":"Fed","tf":"level","note":"선진국 통화 대비 달러"},
    "DTWEXEMEGS": {"cat":"10_환율달러","kr":"신흥국 대비 달러","en":"Dollar vs Emerging Mkts","freq":"D","unit":"Index","src":"Fed","tf":"level","note":"상승=EM 자본유출 압력"},

    # ── 11_Fed유동성 (5개) ──
    "WALCL":     {"cat":"11_Fed유동성","kr":"Fed 총자산","en":"Fed Total Assets","freq":"W","unit":"Mil.USD","src":"Fed","tf":"level","note":"QE/QT 추적. 감소=양적긴축"},
    "RRPONTSYD": {"cat":"11_Fed유동성","kr":"역레포 잔액(ON RRP)","en":"Overnight Reverse Repo","freq":"D","unit":"Bil.USD","src":"NY Fed","tf":"level","note":"과잉 유동성 흡수. 0근접시 고갈 우려"},
    "WTREGEN":   {"cat":"11_Fed유동성","kr":"재무부 일반계좌(TGA)","en":"Treasury General Account","freq":"W","unit":"Mil.USD","src":"Fed","tf":"level","note":"TGA↑=유동성흡수, TGA↓=유동성공급"},
    "TOTRESNS":  {"cat":"11_Fed유동성","kr":"은행 지급준비금","en":"Total Reserves","freq":"M","unit":"Bil.USD","src":"Fed","tf":"level","note":"은행 시스템 유동성"},
    "BOGMBASE":  {"cat":"11_Fed유동성","kr":"본원통화","en":"Monetary Base","freq":"M","unit":"Bil.USD","src":"Fed","tf":"yoy_pct","note":"YoY%로 유동성 추세 판단"},

    # ── 12_원자재 (12개) ──
    "GOLDAMGBD228NLBM": {"cat":"12_원자재","kr":"금 가격","en":"Gold(London AM Fix)","freq":"D","unit":"USD/Troy Oz","src":"LBMA","tf":"level","note":"안전자산. 실질금리 역상관"},
    "DCOILWTICO":       {"cat":"12_원자재","kr":"WTI 원유","en":"WTI Crude Oil","freq":"D","unit":"USD/Barrel","src":"EIA","tf":"level","note":"에너지비용/인플레. $80↑ 압력"},
    "DHHNGSP":          {"cat":"12_원자재","kr":"천연가스 현물","en":"Henry Hub Natural Gas","freq":"D","unit":"$/MMBTU","src":"EIA","tf":"level","note":"에너지 보조 지표"},
    "PCOPPUSDM":        {"cat":"12_원자재","kr":"구리 가격","en":"Copper Price","freq":"M","unit":"USD/MT","src":"IMF","tf":"level","note":"Dr.Copper=글로벌 경기 선행"},
    "PIORECRUSDM":      {"cat":"12_원자재","kr":"철광석 가격","en":"Iron Ore Price","freq":"M","unit":"USD/DMT","src":"IMF","tf":"level","note":"중국 경기 프록시"},
    "PSOYBUSDM":        {"cat":"12_원자재","kr":"대두 가격","en":"Soybean Price","freq":"M","unit":"USD/MT","src":"IMF","tf":"level","note":"브라질 수출 핵심"},
    "PALUMUSDM":        {"cat":"12_원자재","kr":"알루미늄","en":"Aluminum Price","freq":"M","unit":"USD/MT","src":"IMF","tf":"level","note":"산업 원자재"},
    "PNBRLTDUSDM":      {"cat":"12_원자재","kr":"니켈","en":"Nickel Price","freq":"M","unit":"USD/MT","src":"IMF","tf":"level","note":"배터리 원재료"},
    "PWHEAMTUSDM":      {"cat":"12_원자재","kr":"밀","en":"Wheat Price","freq":"M","unit":"USD/MT","src":"IMF","tf":"level","note":"식량 인플레이션"},
    "PMAIZMTUSDM":      {"cat":"12_원자재","kr":"옥수수","en":"Corn Price","freq":"M","unit":"USD/MT","src":"IMF","tf":"level","note":"식량/사료/바이오연료"},
    "PALLFNFINDEXM":    {"cat":"12_원자재","kr":"전체 원자재 가격지수","en":"All Commodity Index","freq":"M","unit":"Index(2016=100)","src":"IMF","tf":"yoy_pct","note":"원자재 종합 동향"},

    # ── 13_주가지수 (1개) ──
    "SP500": {"cat":"13_주가지수","kr":"S&P 500","en":"S&P 500 Index","freq":"D","unit":"Index","src":"S&P","tf":"level","note":"미국 대표 주가. 200일선 하회→약세장"},

    # ── 14_브라질 (2개) ──
    "INTDSRBRM193N":  {"cat":"14_브라질","kr":"브라질 기준금리(SELIC 프록시)","en":"Brazil Discount Rate","freq":"M","unit":"%","src":"IMF IFS","tf":"level","note":"브라질 통화정책 기조"},
    "GGNLBABRA188N":  {"cat":"14_브라질","kr":"브라질 재정수지","en":"Brazil Net Lending/Borrowing","freq":"A","unit":"%GDP","src":"IMF WEO","tf":"level","note":"재정건전성. 적자확대→헤알약세"},

    # ── 15_파생지표 (1개) ──
    "COPPER_GOLD_RATIO": {"cat":"15_파생지표","kr":"구리/금 비율","en":"Copper/Gold Ratio","freq":"M","unit":"Ratio","src":"Calculated","tf":"calculated","note":"PCOPPUSDM÷GOLDAMGBD228NLBM. 경기낙관↑, 위험회피↓"},
}


# ═══════════════════════════════════════════════════════════
# 3. 빈도별 비교 기간 설정
# ═══════════════════════════════════════════════════════════

COMPARE_PERIODS = {
    "D": {"prev": 1, "mid": 20, "yoy": 252},   # 전일 / 4주(20영업일) / 1년
    "W": {"prev": 1, "mid": 4,  "yoy": 52},     # 전주 / 4주 / 1년
    "M": {"prev": 1, "mid": 3,  "yoy": 12},     # 전월 / 3개월 / 1년
    "Q": {"prev": 1, "mid": 2,  "yoy": 4},      # 전분기 / 2분기 / 1년
    "A": {"prev": 1, "mid": 2,  "yoy": 3},      # 전년 / 2년전 / 3년전
}

MID_LABELS = {
    "D": "4W전비", "W": "4W전비", "M": "3M전비", "Q": "2Q전비", "A": "2Y전비"
}


# ═══════════════════════════════════════════════════════════
# 4. 핵심 함수 (Core Functions)
# ═══════════════════════════════════════════════════════════

def fetch_fred_series(series_id, api_key=FRED_API_KEY,
                      start_date=START_DATE, end_date=END_DATE):
    """FRED API에서 단일 시리즈 관측값을 조회한다."""
    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json",
        "observation_start": start_date,
        "observation_end": end_date,
        "sort_order": "desc"
    }
    try:
        r = requests.get(FRED_BASE_URL, params=params, timeout=30)
        r.raise_for_status()
        obs = r.json().get("observations", [])
        return [{"date": o["date"], "value": float(o["value"])}
                for o in obs if o["value"] != "."]
    except Exception as e:
        print(f"  [ERROR] {series_id}: {e}")
        return []


def fetch_all_series(registry=REG):
    """레지스트리 전체 시리즈를 일괄 조회한다(파생지표 제외)."""
    data = {}
    api_total = sum(1 for m in registry.values() if m["tf"] != "calculated")
    cnt = 0
    for sid, m in registry.items():
        if m["tf"] == "calculated":
            continue
        cnt += 1
        print(f"  [{cnt}/{api_total}] {sid} ({m['kr']})...", end="", flush=True)
        obs = fetch_fred_series(sid)
        data[sid] = obs
        print(f" ✓ {len(obs)}건")
        time.sleep(REQUEST_DELAY)
    return data


def get_comparisons(obs, freq):
    """최신값 및 전기/중기/YoY 비교값을 추출한다."""
    if not obs:
        return {"val": None, "date": None, "prev": None, "mid": None, "yoy": None}
    cp = COMPARE_PERIODS.get(freq, COMPARE_PERIODS["M"])
    def safe_get(idx):
        return obs[idx]["value"] if len(obs) > idx else None
    return {
        "val":  obs[0]["value"],
        "date": obs[0]["date"],
        "prev": safe_get(cp["prev"]),
        "mid":  safe_get(cp["mid"]),
        "yoy":  safe_get(cp["yoy"]),
    }


def calc_change(cur, prev, tf):
    """변동률 또는 변화량을 계산한다."""
    if cur is None or prev is None:
        return None
    if tf == "level":
        return round(cur - prev, 4)
    elif tf in ("yoy_pct", "mom_pct"):
        return round((cur - prev) / abs(prev) * 100, 2) if prev != 0 else None
    elif tf == "mom_diff":
        return round(cur - prev, 1)
    elif tf == "calculated":
        return round(cur - prev, 4)
    return None


def calc_copper_gold_ratio(all_data):
    """구리/금 비율을 계산한다(금은 월평균으로 집계)."""
    cu = all_data.get("PCOPPUSDM", [])
    au = all_data.get("GOLDAMGBD228NLBM", [])
    if not cu or not au:
        return []
    # 금 가격을 월별 평균으로 집계
    au_monthly = {}
    for g in au:
        ym = g["date"][:7]
        au_monthly.setdefault(ym, []).append(g["value"])
    au_avg = {ym: sum(vals) / len(vals) for ym, vals in au_monthly.items()}
    return [{"date": c["date"],
             "value": round(c["value"] / au_avg[c["date"][:7]], 4)}
            for c in cu if c["date"][:7] in au_avg and au_avg[c["date"][:7]] > 0]


def fmt_val(v):
    """숫자를 가독성 있게 포맷한다."""
    if v is None:
        return "-"
    av = abs(v)
    if av >= 1_000_000:
        return f"{v/1_000_000:,.1f}M"
    elif av >= 10_000:
        return f"{v:,.0f}"
    else:
        return f"{v:,.2f}"


def fmt_chg(chg, tf="level"):
    """변화량을 부호 포함 문자열로 tf 타입별 포맷한다."""
    if chg is None:
        return "-"
    if tf == "mom_diff":
        return f"{chg:+,.0f}"
    elif tf in ("yoy_pct", "mom_pct"):
        return f"{chg:+.2f}%"
    elif tf == "calculated":
        return f"{chg:+.4f}"
    else:
        return f"{chg:+.2f}"


# ═══════════════════════════════════════════════════════════
# 5. 팩트 테이블 생성 (Fact Table Generation)
# ═══════════════════════════════════════════════════════════

def generate_fact_table(all_data, registry=REG):
    """전체 데이터로 팩트 테이블을 생성한다 (시그널 판단 없음)."""
    report = []
    report.append(f"# 📊 거시경제 팩트 테이블")
    report.append(f"**기준일**: {END_DATE}\n")

    # 카테고리별 그룹핑
    cats = {}
    for sid, m in registry.items():
        cats.setdefault(m["cat"], []).append((sid, m))

    for cat_name in sorted(cats.keys()):
        items = cats[cat_name]
        label = cat_name.split("_", 1)[1] if "_" in cat_name else cat_name
        report.append(f"\n## {label}\n")
        report.append("| 지표 | 주기 | 최신값 | 기준일 | 전기비 | 중기비 | YoY비 |")
        report.append("|------|:---:|------:|:------|------:|------:|------:|")

        for sid, m in items:
            if m["tf"] == "calculated":
                obs = calc_copper_gold_ratio(all_data)
            else:
                obs = all_data.get(sid, [])

            info = get_comparisons(obs, m["freq"])
            v = info["val"]
            d = info["date"] or "-"
            chg_prev = calc_change(v, info["prev"], m["tf"])
            chg_mid  = calc_change(v, info["mid"],  m["tf"])
            chg_yoy  = calc_change(v, info["yoy"],  m["tf"])

            report.append(
                f"| {m['kr']} | {m['freq']} | {fmt_val(v)} | {d} "
                f"| {fmt_chg(chg_prev, m['tf'])} | {fmt_chg(chg_mid, m['tf'])} | {fmt_chg(chg_yoy, m['tf'])} |"
            )

    # 비교 기간 범례
    report.append("\n---")
    report.append("**비교 기간 범례**")
    report.append("- **전기비**: D=전일, W=전주, M=전월, Q=전분기, A=전년")
    report.append("- **중기비**: D/W=4주전, M=3개월전, Q=2분기전, A=2년전")
    report.append("- **YoY비**: D/W/M=1년전, Q=4분기전, A=3년전")

    return "\n".join(report)


# ═══════════════════════════════════════════════════════════
# 6. Markdown 보고서 생성 (Claude-friendly)
# ═══════════════════════════════════════════════════════════

def write_markdown(fact_table_md, path):
    """Claude용 Markdown 보고서를 생성한다."""
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    lines = []
    lines.append("# FRED 거시경제 지표 보고서")
    lines.append("")
    lines.append(f"Generated at: {generated_at}")
    lines.append(f"Data range: {START_DATE} ~ {END_DATE}")
    lines.append("")
    lines.append("## Purpose")
    lines.append("")
    lines.append("이 파일은 GitHub Actions에 의해 자동 생성되며, Claude.ai 분석 컨텍스트로 사용됩니다.")
    lines.append("`fred_latest.csv`를 원천 데이터로, 이 Markdown을 요약 레이어로 활용하세요.")
    lines.append("")

    # 포함 시리즈 목록
    lines.append("## Included Series (78개)")
    lines.append("")
    lines.append("| # | Series ID | Category | Korean | English | Freq | Unit |")
    lines.append("|--:|-----------|----------|--------|---------|:----:|------|")
    for i, (sid, m) in enumerate(REG.items(), 1):
        cat_label = m["cat"].split("_", 1)[1] if "_" in m["cat"] else m["cat"]
        lines.append(f"| {i} | {sid} | {cat_label} | {m['kr']} | {m['en']} | {m['freq']} | {m['unit']} |")
    lines.append("")

    # 팩트 테이블 본문
    lines.append(fact_table_md)
    lines.append("")

    # Claude 지시사항
    lines.append("---")
    lines.append("## Instruction for Claude")
    lines.append("")
    lines.append("- `fred_latest.csv`를 원천 데이터셋으로 취급하세요.")
    lines.append("- 이 파일로 포함된 경제지표 구성을 파악하세요.")
    lines.append("- 거시경제 분석 요청 시, 최신값과 과거 관측값을 비교하세요.")
    lines.append("- 값이 `-`이거나 비어 있으면 해당 관측이 불가함을 명시하세요.")
    lines.append("- 전기비·중기비·YoY비를 모두 활용하여 추세를 판단하세요.")
    lines.append("")

    Path(path).write_text("\n".join(lines), encoding="utf-8")


# ═══════════════════════════════════════════════════════════
# 7. CSV 저장 함수
# ═══════════════════════════════════════════════════════════

def save_csv(all_data, registry, path):
    """전체 데이터를 CSV로 저장한다."""
    rows = []
    for sid, m in registry.items():
        if m["tf"] == "calculated":
            obs = calc_copper_gold_ratio(all_data)
        else:
            obs = all_data.get(sid, [])

        info = get_comparisons(obs, m["freq"])
        v = info["val"]
        chg_prev = calc_change(v, info["prev"], m["tf"])
        chg_mid  = calc_change(v, info["mid"],  m["tf"])
        chg_yoy  = calc_change(v, info["yoy"],  m["tf"])

        rows.append({
            "series_id": sid,
            "category": m["cat"],
            "korean_name": m["kr"],
            "english_name": m["en"],
            "frequency": m["freq"],
            "unit": m["unit"],
            "source": m["src"],
            "transform": m["tf"],
            "latest_date": info["date"],
            "latest_value": v,
            "chg_prev": chg_prev,
            "chg_mid": chg_mid,
            "chg_yoy": chg_yoy,
            "note": m["note"],
        })

    df = pd.DataFrame(rows)
    df.to_csv(path, index=False, encoding="utf-8-sig")
    return df


# ═══════════════════════════════════════════════════════════
# 8. 메인 실행 흐름
# ═══════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("FRED API 거시경제 팩트 테이블 생성 (풀 버전)")
    print(f"기간: {START_DATE} ~ {END_DATE}")
    print("=" * 60)

    # 출력 디렉토리 생성
    Path("data/fred_history").mkdir(parents=True, exist_ok=True)

    # Step 1: 전체 데이터 조회
    print("\n[Step 1] FRED API 데이터 조회 시작...")
    all_data = fetch_all_series()

    # Step 1.5: API 성공률 확인
    api_total = sum(1 for m in REG.values() if m["tf"] != "calculated")
    success = sum(1 for v in all_data.values() if v)
    rate = success / api_total * 100 if api_total > 0 else 0
    print(f"\n  → 성공: {success}/{api_total} ({rate:.0f}%)")
    if rate < 50:
        print("\n❌ API 성공률 50% 미만 — 보고서 생성 중단")
        sys.exit(1)

    # Step 2: 파생 지표 계산
    print("\n[Step 2] 구리/금 비율 계산...")
    all_data["COPPER_GOLD_RATIO"] = calc_copper_gold_ratio(all_data)

    # Step 3: 팩트 테이블 생성
    print("\n[Step 3] 팩트 테이블 생성 중...")
    fact_table_md = generate_fact_table(all_data)

    # Step 4: 파일 저장
    run_id = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    latest_csv  = "data/fred_latest.csv"
    latest_md   = "data/fred_latest.md"
    history_csv = f"data/fred_history/fred_{run_id}.csv"

    print("\n[Step 4] 파일 저장 중...")
    df = save_csv(all_data, REG, latest_csv)
    df.to_csv(history_csv, index=False, encoding="utf-8-sig")
    write_markdown(fact_table_md, latest_md)

    print(f"\n  ✅ Saved: {latest_csv}  ({len(df)}건)")
    print(f"  ✅ Saved: {latest_md}")
    print(f"  ✅ Saved: {history_csv}")

    # 요약 출력
    print("\n" + "=" * 60)
    print("📊 팩트 테이블 미리보기")
    print("=" * 60)
    print(fact_table_md[:2000] + "\n... (이하 생략)")
    print("\n✅ 완료! claude.ai에서 data/fred_latest.md 와 data/fred_latest.csv 를 연결하세요.")


if __name__ == "__main__":
    main()
