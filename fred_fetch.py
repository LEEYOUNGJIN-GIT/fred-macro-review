#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FRED API 거시경제 팩트 테이블 자동 생성 스크립트 (풀 버전)
──────────────────────────────────────────────────────────
• 98개 FRED 시리즈 + 3개 파생지표 = 101개 매크로 지표
• 20개 카테고리별 팩트 테이블을 Markdown + CSV로 저장
• GitHub Actions + claude.ai GitHub Integration 연동 목적

사용법:
    export FRED_API_KEY="your-api-key"
    python fred_fetch.py
"""

import os
import sys
import time
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
REQUEST_DELAY  = 0.5        # FRED API rate limit 준수
MAX_RETRIES    = 3           # API 호출 재시도 횟수
RETRY_BACKOFF  = 2.0         # 지수 백오프 배수
MIN_SUCCESS_RATE = 0.5       # 50% 미만 성공 시 중단

END_DATE   = datetime.now(timezone.utc).strftime("%Y-%m-%d")
START_DATE = (datetime.now(timezone.utc) - timedelta(days=1095)).strftime("%Y-%m-%d")

# ── 경로 설정 ──
BASE_DIR    = Path(__file__).resolve().parent
DATA_DIR    = BASE_DIR / "data"
HISTORY_DIR = DATA_DIR / "fred_history"

# ═══════════════════════════════════════════════════════════
# 2. 시리즈 레지스트리 (101개)
# ═══════════════════════════════════════════════════════════
# tf 필드: level=원값, yoy_pct=YoY% 변환, mom_pct=MoM%,
#          mom_diff=전월차, calculated=파생

REG = {'T10Y2Y': {'cat': '01_금리채권', 'kr': '장단기 스프레드(10Y-2Y)', 'en': '10Y-2Y Treasury Spread', 'freq': 'D', 'unit': '%', 'src': 'Fed', 'tf': 'level', 'note': '음수=역전=침체 경고. 역전 후 12~18M 내 침체 다수. 정상 1~2%'},
 'DFII10': {'cat': '01_금리채권', 'kr': '10Y 실질금리(TIPS)', 'en': '10Y TIPS Yield', 'freq': 'D', 'unit': '%', 'src': 'Fed', 'tf': 'level', 'note': '실질 자금조달 비용. 2%↑ 긴축적. 0%↓ 완화적. 자산가격·성장주 역상관'},
 'T10YIE': {'cat': '01_금리채권', 'kr': '10Y BEI', 'en': '10Y Breakeven Inflation', 'freq': 'D', 'unit': '%', 'src': 'Fed', 'tf': 'level', 'note': '시장 10년 인플레 기대. 2~2.5% 정상. 2.5%↑ 디앵커링 경계'},
 'T5YIE': {'cat': '01_금리채권', 'kr': '5Y BEI', 'en': '5Y Breakeven Inflation', 'freq': 'D', 'unit': '%', 'src': 'Fed', 'tf': 'level', 'note': '중기 인플레 기대. 2~2.5% 정상. T10YIE 대비 상방이면 단기 인플레 압력'},
 'T5YIFR': {'cat': '01_금리채권', 'kr': '5Y5Y 선도 인플레 기대', 'en': '5Y5Y Forward Inflation', 'freq': 'D', 'unit': '%', 'src': 'Fed', 'tf': 'level', 'note': 'Fed 최중시 장기 인플레 앵커링. 2~2.5% 정상. 2.5%↑ 신뢰 훼손'},
 'DGS2': {'cat': '01_금리채권', 'kr': '미국채 2년물', 'en': '2Y Treasury Yield', 'freq': 'D', 'unit': '%', 'src': 'Fed', 'tf': 'level', 'note': '단기 금리 기대. Fed 정책 선반영. DFF 대비 괴리=인하/인상 기대 내재'},
 'DGS10': {'cat': '01_금리채권', 'kr': '미국채 10년물', 'en': '10Y Treasury Yield', 'freq': 'D', 'unit': '%', 'src': 'Fed', 'tf': 'level', 'note': '글로벌 벤치마크. 모기지·회사채 기준. 5%↑ 재정·기업 부담 가중'},
 'TB3MS': {'cat': '01_금리채권', 'kr': '3개월 T-Bill', 'en': '3M Treasury Bill', 'freq': 'M', 'unit': '%', 'src': 'Fed', 'tf': 'level', 'note': '단기 무위험 금리. DFF와 동행. T10Y3M 산출 기준'},
 'DFF': {'cat': '01_금리채권', 'kr': '연방기금 실효금리(일간)', 'en': 'Fed Funds Effective Rate', 'freq': 'D', 'unit': '%', 'src': 'Fed', 'tf': 'level', 'note': 'Fed 기준금리 실시간. Core PCE 차감→실질금리 갭 산출. 중립금리 약 2.5%'},
 'FEDFUNDS': {'cat': '01_금리채권', 'kr': '연방기금금리(월간)', 'en': 'Fed Funds Rate(Monthly)', 'freq': 'M', 'unit': '%', 'src': 'Fed', 'tf': 'level', 'note': '기준금리 월간 평균. FOMC 결정 직후 변동. DFF의 월간 스무딩'},
 'SOFR': {'cat': '01_금리채권',
          'kr': 'SOFR(담보부 익일물)',
          'en': 'Secured Overnight Financing Rate',
          'freq': 'D',
          'unit': '%',
          'src': 'NY Fed',
          'tf': 'level',
          'note': 'LIBOR 대체 단기 기준금리. 레포 시장 유동성 반영. DFF와 ±10bp 동행'},
 'AAA': {'cat': '01_금리채권', 'kr': 'Aaa 회사채 수익률', 'en': "Moody's Aaa Corp Bond Yield", 'freq': 'D', 'unit': '%', 'src': "Moody's", 'tf': 'level', 'note': '최우량 기업 조달비용. 국채+신용 프리미엄. 장기 투자등급 벤치마크'},
 'BAA': {'cat': '01_금리채권', 'kr': 'Baa 회사채 수익률', 'en': "Moody's Baa Corp Bond Yield", 'freq': 'D', 'unit': '%', 'src': "Moody's", 'tf': 'level', 'note': '투자등급 하한 조달비용. AAA 대비 스프레드=신용 리스크 프리미엄'},
 'BAA10Y': {'cat': '01_금리채권', 'kr': 'Baa-10Y 신용 스프레드', 'en': 'Baa-10Y Treasury Spread', 'freq': 'D', 'unit': '%', 'src': "Moody's/Fed", 'tf': 'level', 'note': '기업 디폴트 프리미엄. 2%=정상. 3%↑ 경계. GFC 피크 6%'},
 'VIXCLS': {'cat': '02_리스크신용', 'kr': 'VIX 공포지수', 'en': 'CBOE VIX', 'freq': 'D', 'unit': 'Index', 'src': 'CBOE', 'tf': 'level', 'note': '시장 공포 지수. 15↓ 과도 낙관. 20↑ 불안. 30↑ 위기. 40↑ 패닉'},
 'BAMLH0A0HYM2': {'cat': '02_리스크신용',
                  'kr': '하이일드 스프레드(OAS)',
                  'en': 'ICE BofA US HY OAS',
                  'freq': 'D',
                  'unit': '%',
                  'src': 'ICE/BofA',
                  'tf': 'level',
                  'note': '하이일드 스프레드(OAS). 확대=신용 스트레스. 축소=리스크온. 급등은 디폴트 우려'},
 'TOTBKCR': {'cat': '02_리스크신용',
             'kr': '상업은행 총 대출',
             'en': 'Bank Credit All Commercial Banks',
             'freq': 'W',
             'unit': 'Bil.USD',
             'src': 'Fed',
             'tf': 'yoy_pct',
             'note': '은행 총 대출. YoY 증가=경기 확장. YoY 감소=신용 긴축→경기 위축 선행'},
 'NFCI': {'cat': '03_금융스트레스', 'kr': '시카고 금융여건지수', 'en': 'Chicago Fed NFCI', 'freq': 'W', 'unit': 'Index', 'src': 'Chicago Fed', 'tf': 'level', 'note': '시카고 금융여건. 0=평균. -=완화. +=긴축. +1.0↑ 시스템 위기 수준'},
 'STLFSI4': {'cat': '03_금융스트레스', 'kr': 'STL 금융스트레스', 'en': 'STL Fed FSI', 'freq': 'W', 'unit': 'Index', 'src': 'STL Fed', 'tf': 'level', 'note': 'STL 금융스트레스. 0=평균. +1σ↑ 스트레스. 3개 Fed 지수 교차확인'},
 'KCFSI': {'cat': '03_금융스트레스',
           'kr': 'KC 금융스트레스',
           'en': 'KC Financial Stress Index',
           'freq': 'M',
           'unit': 'Index',
           'src': 'KC Fed',
           'tf': 'level',
           'note': 'KC 금융스트레스. 0=평균. +1σ↑ 스트레스. NFCI·STLFSI4 보조 확인'},
 'CFNAI': {'cat': '03_금융스트레스', 'kr': '시카고 경제활동지수', 'en': 'Chicago Fed NAI', 'freq': 'M', 'unit': 'Index', 'src': 'Chicago Fed', 'tf': 'level', 'note': '85개 변수 종합. 0=추세 성장. -0.7↓=침체 진입. +0.7↑=인플레 압력'},
 'UNRATE': {'cat': '04_노동시장', 'kr': '실업률', 'en': 'Unemployment Rate', 'freq': 'M', 'unit': '%', 'src': 'BLS', 'tf': 'level', 'note': '실업률. Sahm Rule: 3M이평 12M저점 대비 +0.5%p↑=침체. 자연실업률 약 4%'},
 'PAYEMS': {'cat': '04_노동시장',
            'kr': '비농업 고용자수',
            'en': 'Nonfarm Payrolls',
            'freq': 'M',
            'unit': 'Thousands',
            'src': 'BLS',
            'tf': 'mom_diff',
            'note': '비농업 고용 전월차. +200K↑ 견조. +100K↓ 냉각. 0↓ 침체. 3M이평 추세 중시'},
 'ICSA': {'cat': '04_노동시장', 'kr': '신규 실업수당 청구', 'en': 'Initial Jobless Claims', 'freq': 'W', 'unit': 'Number', 'src': 'DOL', 'tf': 'level', 'note': '신규 실업청구. 250K↓ 견조. 300K↑ 약화. 4주 이평으로 노이즈 제거 필요'},
 'CCSA': {'cat': '04_노동시장', 'kr': '계속 실업수당 청구', 'en': 'Continued Claims', 'freq': 'W', 'unit': 'Number', 'src': 'DOL', 'tf': 'level', 'note': '계속 실업청구. 장기 실업 추세. 1.9M↑ 재취업 난항. 2M↑ 고용 심각 위축'},
 'JTSJOL': {'cat': '04_노동시장',
            'kr': 'JOLTS 구인건수',
            'en': 'JOLTS Job Openings',
            'freq': 'M',
            'unit': 'Thousands',
            'src': 'BLS',
            'tf': 'level',
            'note': 'JOLTS 구인. V/U ratio(구인/실업) 1.0↓=노동 수급 균형. 0.8↓=고용 위축'},
 'JTSQUR': {'cat': '04_노동시장',
            'kr': 'JOLTS 이직률',
            'en': 'JOLTS Quits Rate',
            'freq': 'M',
            'unit': 'Rate (%)',
            'src': 'BLS',
            'tf': 'level',
            'note': 'JOLTS 이직률(Rate). JTSJOL(Thousands)과 단위·의미 다름. 2.0%↑ 타이트. JTSJOL과 동일 월간 릴리스'},
 'CIVPART': {'cat': '04_노동시장', 'kr': '경제활동 참가율', 'en': 'Labor Force Participation', 'freq': 'M', 'unit': '%', 'src': 'BLS', 'tf': 'level', 'note': '전체 경활률(~62%). 구조적 변화(고령화 등) 반영. LNS11300060(25-54세)과 연령대·수준 다름'},
 'LNS11300060': {'cat': '04_노동시장',
                 'kr': '핵심연령(25-54) 참가율',
                 'en': 'LFPR 25-54 Years',
                 'freq': 'M',
                 'unit': '%',
                 'src': 'BLS',
                 'tf': 'level',
                 'note': '25-54세 경활률(~84%). CIVPART(전체)과 혼동 금지. 구조적 노이즈 적은 경기 지표'},
 'CES0500000003': {'cat': '04_노동시장',
                   'kr': '시간당 평균 임금(민간)',
                   'en': 'Avg Hourly Earnings',
                   'freq': 'M',
                   'unit': '$/hour',
                   'src': 'BLS',
                   'tf': 'yoy_pct',
                   'note': '민간 시간당 임금 YoY. 3~3.5%=생산성 정합. 4%↑ 임금-물가 스파이럴 경계'},
 'CPIAUCSL': {'cat': '05_물가인플레',
              'kr': 'CPI 소비자물가',
              'en': 'CPI All Urban',
              'freq': 'M',
              'unit': 'Index',
              'src': 'BLS',
              'tf': 'yoy_pct',
              'note': '헤드라인 CPI YoY. 2% 물가목표 대비 3%↑는 목표 초과 구간. 에너지·식품 포함(변동성↑)'},
 'CPILFESL': {'cat': '05_물가인플레', 'kr': '근원 CPI', 'en': 'Core CPI', 'freq': 'M', 'unit': 'Index', 'src': 'BLS', 'tf': 'yoy_pct', 'note': '근원 CPI YoY. 식품·에너지 제외 기조 물가. Fed 2차 참조. 3%↑ 경계'},
 'PCEPI': {'cat': '05_물가인플레', 'kr': 'PCE 물가지수', 'en': 'PCE Price Index', 'freq': 'M', 'unit': 'Index', 'src': 'BEA', 'tf': 'yoy_pct', 'note': 'PCE 물가 YoY. Fed 공식 타겟. CPI보다 소비 가중치 유연. 2%=목표'},
 'PCEPILFE': {'cat': '05_물가인플레', 'kr': '근원 PCE', 'en': 'Core PCE', 'freq': 'M', 'unit': 'Index', 'src': 'BEA', 'tf': 'yoy_pct', 'note': '★ Core PCE YoY. Fed 최선호 물가. 목표 2.0%. 2.5%↑ 인하 지연. 3%↑ 긴축 유지'},
 'PPIFIS': {'cat': '05_물가인플레', 'kr': 'PPI 생산자물가', 'en': 'PPI Final Demand', 'freq': 'M', 'unit': 'Index', 'src': 'BLS', 'tf': 'yoy_pct', 'note': 'PPI 최종수요 YoY. 기업 비용→CPI 선행 3~6M. 5%↑ 마진 압박·전가 우려'},
 'MICH': {'cat': '05_물가인플레',
          'kr': '미시간대 인플레 기대',
          'en': 'U.Michigan Inflation Exp.',
          'freq': 'M',
          'unit': '%',
          'src': 'U.Michigan',
          'tf': 'level',
          'note': '미시간대 1년 인플레 기대. 3%↑ 디앵커링 우려. Fed 커뮤니케이션 리스크'},
 'GDP': {'cat': '06_GDP생산', 'kr': '명목 GDP', 'en': 'Nominal GDP', 'freq': 'Q', 'unit': 'Bil.USD', 'src': 'BEA', 'tf': 'yoy_pct', 'note': '명목 GDP YoY. 경제 규모. 실질+인플레 합산. 세수·부채/GDP 비율 기준'},
 'GDPC1': {'cat': '06_GDP생산', 'kr': '실질 GDP', 'en': 'Real GDP', 'freq': 'Q', 'unit': 'Bil.2017USD', 'src': 'BEA', 'tf': 'yoy_pct', 'note': '실질 GDP QoQ. 2연속 음수=기술적 침체. 잠재성장률 약 2%. 1%↓ 둔화 경고'},
 'INDPRO': {'cat': '06_GDP생산',
            'kr': '산업생산지수',
            'en': 'Industrial Production',
            'freq': 'M',
            'unit': 'Index(2017=100)',
            'src': 'Fed',
            'tf': 'yoy_pct',
            'note': '산업생산 YoY. 제조·광업·유틸. YoY 0%↓=산업 침체. 경기순환 민감'},
 'RSAFS': {'cat': '06_GDP생산', 'kr': '소매판매', 'en': 'Retail Sales', 'freq': 'M', 'unit': 'Mil.USD', 'src': 'Census', 'tf': 'mom_pct', 'note': '소매판매 MoM. 소비=GDP 70%. +0.5%↑ 견조. 2개월 연속 음수=소비 위축'},
 'DGORDER': {'cat': '06_GDP생산', 'kr': '내구재 주문', 'en': 'Durable Goods Orders', 'freq': 'M', 'unit': 'Mil.USD', 'src': 'Census', 'tf': 'mom_pct', 'note': '내구재 주문 MoM. 기업 설비투자 선행. 운송 제외 시 기조 파악 용이'},
 'CMRMTSPL': {'cat': '06_GDP생산',
              'kr': '실질 제조업/무역 판매',
              'en': 'Real Mfg & Trade Sales',
              'freq': 'M',
              'unit': 'Mil.USD',
              'src': 'Census',
              'tf': 'yoy_pct',
              'note': '실질 제조업/무역 판매 YoY. NBER 침체 판정 4대 지표 중 하나'},
 'UMCSENT': {'cat': '07_소비심리통화',
             'kr': '미시간 소비자심리',
             'en': 'U.Michigan Sentiment',
             'freq': 'M',
             'unit': 'Index',
             'src': 'U.Michigan',
             'tf': 'level',
             'note': '미시간 소비자심리. 80↑ 양호. 60↓ 위축. 50↓ 심각 비관. 소비 선행'},
 'M2SL': {'cat': '07_소비심리통화', 'kr': 'M2 통화량', 'en': 'M2 Money Stock', 'freq': 'M', 'unit': 'Bil.USD', 'src': 'Fed', 'tf': 'yoy_pct', 'note': 'M2 통화량 YoY. 음수→디플레 우려. 10%↑ 과잉 유동성. 인플레 선행 12~18M'},
 'CSUSHPINSA': {'cat': '08_주택시장',
                'kr': '케이스-쉴러 전국 주택가격',
                'en': 'Case-Shiller Home Price',
                'freq': 'M',
                'unit': 'Index(2000=100)',
                'src': 'S&P',
                'tf': 'yoy_pct',
                'note': '케이스-쉴러 전국 주택가격 YoY. 20%↑ 과열. 0%↓ 조정. 자산효과→소비 연동'},
 'HOUST': {'cat': '08_주택시장', 'kr': '신규주택 착공', 'en': 'Housing Starts', 'freq': 'M', 'unit': 'Thousands', 'src': 'Census', 'tf': 'level', 'note': '신규주택 착공. 1,500K↑ 활황. 1,000K↓ 부진. 모기지 금리 6~12M 후행'},
 'PERMIT': {'cat': '08_주택시장', 'kr': '건축허가', 'en': 'Building Permits', 'freq': 'M', 'unit': 'Thousands', 'src': 'Census', 'tf': 'level', 'note': '건축허가. 착공 선행 1~2M. 경기전환점 포착. 허가↓+착공↑=재고 소진'},
 'MORTGAGE30US': {'cat': '08_주택시장',
                  'kr': '30년 모기지 금리',
                  'en': '30Y Fixed Mortgage',
                  'freq': 'W',
                  'unit': '%',
                  'src': 'Freddie Mac',
                  'tf': 'level',
                  'note': '30년 고정 모기지. 7%↑ 수요 급감. 6%↓ 리파이 수요 증가. 주택경기 핵심'},
 'EXHOSLUSM495S': {'cat': '08_주택시장', 'kr': '기존주택 판매', 'en': 'Existing Home Sales', 'freq': 'M', 'unit': 'Thousands', 'src': 'NAR', 'tf': 'level', 'note': '기존주택 판매. 거래량=수요 강도. 재고 6M분↑=매수자 시장'},
 'NETFI': {'cat': '09_무역국제수지',
           'kr': '경상수지(순금융투자)',
           'en': "Balance on Current Account (NIPA's)",
           'freq': 'Q',
           'unit': 'Bil.USD',
           'src': 'BEA',
           'tf': 'level',
           'note': '순금융투자(Net Financial Investment). 경상수지와 연관. 적자 확대=대외자금조달 의존↑'},
 'FYFSD': {'cat': '09_무역국제수지',
           'kr': '연방 재정적자',
           'en': 'Federal Surplus or Deficit',
           'freq': 'A',
           'unit': 'Mil.USD',
           'src': 'Treasury',
           'tf': 'level',
           'note': '연방 재정적자. 적자 확대→장기금리↑·국채 공급 부담. GDP 대비 5%↑ 경계'},
 'BOPGSTB': {'cat': '09_무역국제수지', 'kr': '무역수지', 'en': 'Trade Balance', 'freq': 'M', 'unit': 'Mil.USD', 'src': 'Census', 'tf': 'level', 'note': '무역수지. 적자 확대→달러 약세. 관세 효과·교역 조건 변동 반영'},
 'EXPGS': {'cat': '09_무역국제수지', 'kr': '실질 수출', 'en': 'Real Exports', 'freq': 'Q', 'unit': 'Bil.USD', 'src': 'BEA', 'tf': 'yoy_pct', 'note': '실질 수출 YoY. 글로벌 수요·달러 강도 반영. 수출↓+달러↑=교역 위축'},
 'IMPGS': {'cat': '09_무역국제수지', 'kr': '실질 수입', 'en': 'Real Imports', 'freq': 'Q', 'unit': 'Bil.USD', 'src': 'BEA', 'tf': 'yoy_pct', 'note': '실질 수입 YoY. 내수 강도 반영. 수입 급증=관세 전 선구매(frontloading) 가능'},
 'DEXKOUS': {'cat': '10_환율달러', 'kr': '원/달러 환율', 'en': 'USD/KRW', 'freq': 'D', 'unit': 'KRW/USD', 'src': 'Fed', 'tf': 'level', 'note': '원/달러. 상승=원화약세(수입물가↑). 급등 시 외화부채·자본유출 리스크, 변동성 확대 주의'},
 'DTWEXBGS': {'cat': '10_환율달러',
              'kr': '무역가중 달러지수(광범위)',
              'en': 'Trade-Weighted Dollar(Broad)',
              'freq': 'D',
              'unit': 'Index(2006=100)',
              'src': 'Fed',
              'tf': 'level',
              'note': '무역가중 달러(광범위). DXY 대용. 26개국 대비. YoY↑=EM 자본유출 압력'},
 'DTWEXAFEGS': {'cat': '10_환율달러', 'kr': '선진국 대비 달러', 'en': 'Dollar vs Advanced Econ.', 'freq': 'D', 'unit': 'Index', 'src': 'Fed', 'tf': 'level', 'note': '선진국 대비 달러. EUR·JPY·GBP 중심. 통화정책 차별화 반영'},
 'DTWEXEMEGS': {'cat': '10_환율달러', 'kr': '신흥국 대비 달러', 'en': 'Dollar vs Emerging Mkts', 'freq': 'D', 'unit': 'Index', 'src': 'Fed', 'tf': 'level', 'note': '신흥국 대비 달러. 상승=EM 자본유출·외채 부담 증가. 원자재 역상관'},
 'DEXJPUS': {'cat': '10_환율달러',
             'kr': 'USD/JPY 환율',
             'en': 'USD/JPY',
             'freq': 'D',
             'unit': 'JPY/USD',
             'src': 'Fed',
             'tf': 'level',
             'note': 'H.10 공식. 상승=엔약세·캐리 유리. 급락=엔강세·글로벌 risk-off. DTWEXAFEGS(지수)와 혼동 금지'},
 'DEXCHUS': {'cat': '10_환율달러',
             'kr': 'USD/CNY 환율',
             'en': 'USD/CNY',
             'freq': 'D',
             'unit': 'CNY/USD',
             'src': 'Fed',
             'tf': 'level',
             'note': 'H.10 공식. 상승=위안 약세·EM·원화 압력. ^HSI(홍콩 주식)와 다른 지표'},
 'WALCL': {'cat': '11_Fed유동성', 'kr': 'Fed 총자산', 'en': 'Fed Total Assets', 'freq': 'W', 'unit': 'Mil.USD', 'src': 'Fed', 'tf': 'level', 'note': 'Fed 총자산. QE 확대/QT 축소의 결과값. 감소=유동성 흡수(긴축), 증가=유동성 공급'},
 'TREAST': {'cat': '11_Fed유동성',
            'kr': 'Fed 국채 보유',
            'en': 'Fed Treasury Holdings',
            'freq': 'W',
            'unit': 'Mil.USD',
            'src': 'Fed',
            'tf': 'level',
            'note': 'WALCL 세부(국채). TREAST+WSHOMCB≠WALCL(기타자산 포함). QT 국채 축소 속도'},
 'WSHOMCB': {'cat': '11_Fed유동성',
             'kr': 'Fed MBS 보유',
             'en': 'Fed MBS Holdings',
             'freq': 'W',
             'unit': 'Mil.USD',
             'src': 'Fed',
             'tf': 'level',
             'note': 'WALCL 세부(MBS). MBST 폐기→WSHOMCB 사용. TREAST+WSHOMCB≠WALCL'},
 'RRPONTSYD': {'cat': '11_Fed유동성',
               'kr': '역레포 잔액(ON RRP)',
               'en': 'Overnight Reverse Repo',
               'freq': 'D',
               'unit': 'Bil.USD',
               'src': 'NY Fed',
               'tf': 'level',
               'note': '역레포(ON RRP). 과잉 유동성 흡수. 0 근접=유동성 고갈. QT 종료 시그널'},
 'WTREGEN': {'cat': '11_Fed유동성',
             'kr': '재무부 일반계좌(TGA)',
             'en': 'Treasury General Account',
             'freq': 'W',
             'unit': 'Mil.USD',
             'src': 'Fed',
             'tf': 'level',
             'note': '재무부 일반계좌(TGA). TGA↑=유동성 흡수(국채 발행). TGA↓=유동성 공급'},
 'TOTRESNS': {'cat': '11_Fed유동성', 'kr': '은행 지급준비금', 'en': 'Total Reserves', 'freq': 'M', 'unit': 'Bil.USD', 'src': 'Fed', 'tf': 'level', 'note': '은행 지급준비금. $3T↓ 유동성 긴장 시작. 은행간 금리 변동성 확대'},
 'BOGMBASE': {'cat': '11_Fed유동성', 'kr': '본원통화', 'en': 'Monetary Base', 'freq': 'M', 'unit': 'Bil.USD', 'src': 'Fed', 'tf': 'yoy_pct', 'note': '본원통화 YoY. 통화 공급 기초. YoY 음수=긴축 기조. 인플레 장기 추세'},
 # GOLDAMGBD228NLBM(LBMA AM Fix)은 FRED API 호출 오류로 사용 불가.
 # NASDAQQGLDI(NASDAQ Gold FLOWS103 지수)로 대체 운용.
 # ※ 주의: 단위는 지수(Index)이며 USD/oz가 아님. 절대값(예: 2886)은 달러 현물가가 아니므로
 #   WTI·구리 등 다른 원자재(USD 기준)와 직접 비교 불가. 추세·방향성 해석만 유효.
 #   구리/금 비율(COPPER_GOLD_RATIO)도 절대값이 아닌 방향성으로만 해석할 것.
 'NASDAQQGLDI': {'cat': '12_원자재',
                 'kr': '금 가격(NASDAQ 지수, USD/oz 아님)',
                 'en': 'Gold Price Index (NASDAQ Gold FLOWS103)',
                 'freq': 'D',
                 'unit': 'Index (not USD/oz)',
                 'src': 'Nasdaq',
                 'tf': 'level',
                 'note': '⚠ LBMA Fix(GOLDAMGBD228NLBM) API 오류로 대체. 지수단위(Index)이며 달러 현물가 아님. 절대값 비교 불가 — 추세·방향성만 참고'},
 'DCOILWTICO': {'cat': '12_원자재', 'kr': 'WTI 원유', 'en': 'WTI Crude Oil', 'freq': 'D', 'unit': 'USD/Barrel', 'src': 'EIA', 'tf': 'level', 'note': 'WTI 원유. $60↓ 수요위축 우려. $80↑ 인플레 압력. $100↑ 스태그 리스크'},
 'DHHNGSP': {'cat': '12_원자재', 'kr': '천연가스 현물', 'en': 'Henry Hub Natural Gas', 'freq': 'D', 'unit': '$/MMBTU', 'src': 'EIA', 'tf': 'level', 'note': '천연가스. 에너지 보조. 계절성 강함. $4↑ 유틸리티 비용 전가→CPI 영향'},
 'PCOPPUSDM': {'cat': '12_원자재', 'kr': '구리 가격', 'en': 'Copper Price', 'freq': 'M', 'unit': 'USD/MT', 'src': 'IMF', 'tf': 'level', 'note': '구리(Dr.Copper). 글로벌 경기 선행. 중국 수요 프록시. YoY↑=확장 기대'},
 'PIORECRUSDM': {'cat': '12_원자재', 'kr': '철광석 가격', 'en': 'Iron Ore Price', 'freq': 'M', 'unit': 'USD/DMT', 'src': 'IMF', 'tf': 'level', 'note': '철광석. 중국 부동산·인프라 경기 프록시. 구리와 교차 확인'},
 'PSOYBUSDM': {'cat': '12_원자재', 'kr': '대두 가격', 'en': 'Soybean Price', 'freq': 'M', 'unit': 'USD/MT', 'src': 'IMF', 'tf': 'level', 'note': '대두. 브라질 수출 핵심. 라니냐/엘니뇨 공급 충격. 식량 인플레 기여'},
 'PALUMUSDM': {'cat': '12_원자재', 'kr': '알루미늄', 'en': 'Aluminum Price', 'freq': 'M', 'unit': 'USD/MT', 'src': 'IMF', 'tf': 'level', 'note': '알루미늄. 에너지 집약 산업재. 전력비용·중국 생산 영향. 건설 수요 반영'},
 'PNICKUSDM': {'cat': '12_원자재', 'kr': '니켈', 'en': 'Nickel Price', 'freq': 'M', 'unit': 'USD/MT', 'src': 'IMF', 'tf': 'level', 'note': '니켈(IMF). 배터리·스테인리스 원재료. EV 수요 구조적 증가. 인니 공급 집중'},
 'PWHEAMTUSDM': {'cat': '12_원자재', 'kr': '밀', 'en': 'Wheat Price', 'freq': 'M', 'unit': 'USD/MT', 'src': 'IMF', 'tf': 'level', 'note': '밀. 식량 안보 핵심. 흑해 지정학 민감. CPI 식품 구성요소'},
 'PMAIZMTUSDM': {'cat': '12_원자재', 'kr': '옥수수', 'en': 'Corn Price', 'freq': 'M', 'unit': 'USD/MT', 'src': 'IMF', 'tf': 'level', 'note': '옥수수. 식량/사료/바이오연료. 에탄올 수요=유가 연동. 기후 민감'},
 'PALLFNFINDEXM': {'cat': '12_원자재',
                   'kr': '전체 원자재 가격지수',
                   'en': 'All Commodity Index',
                   'freq': 'M',
                   'unit': 'Index(2016=100)',
                   'src': 'IMF',
                   'tf': 'yoy_pct',
                   'note': '원자재 종합지수 YoY. 전체 원자재 동향. 30%↑ 인플레 경고. 음수=디플레 압력'},
 'SP500': {'cat': '13_주가지수', 'kr': 'S&P 500', 'en': 'S&P 500 Index', 'freq': 'D', 'unit': 'Index', 'src': 'S&P', 'tf': 'level', 'note': '미국 대표 주가. 200일선 하회→기술적 약세. 고점 대비 -10%=조정. -20%=약세장'},
 'COPPER_GOLD_RATIO': {'cat': '15_파생지표',
                       'kr': '구리/금 비율',
                       'en': 'Copper/Gold Ratio',
                       'freq': 'M',
                       'unit': 'Ratio',
                       'src': 'Calculated',
                       'tf': 'calculated',
                       'note': '⚠ 구리(USD/MT)÷금NASDAQ지수(Index). 금이 지수단위이므로 비율 절대값 무의미 — 방향성(상승=경기낙관·위험선호, 하락=위험회피)만 유효. 장기금리 방향성과 높은 상관'},
 'KOR_US_10Y_SPREAD': {'cat': '15_파생지표',
                       'kr': '한미 10년물 금리차(한-미)',
                       'en': 'KOR-US 10Y Yield Spread',
                       'freq': 'M',
                       'unit': '%p',
                       'src': 'Calculated',
                       'tf': 'calculated',
                       'note': '한국 10Y(IRLTLT01KRM156N) - 미국 10Y(DGS10, 일간→월평균). 스프레드 축소/역전은 환율 압력 점검'},
 'KOR_US_POLICY_SPREAD': {'cat': '15_파생지표',
                          'kr': '한미 기준금리 스프레드(한-미)',
                          'en': 'KOR-US Policy Rate Spread',
                          'freq': 'M',
                          'unit': '%p',
                          'src': 'Calculated',
                          'tf': 'calculated',
                          'note': '한국 콜금리(IRSTCI01KRM156N) - 미국 FFR(DFF, 일간→월평균). SIG17 한국 크로스 신호 입력'},
 'T10Y3M': {'cat': '16_침체조기경보',
            'kr': '10Y-3M 스프레드',
            'en': '10Y-3M Treasury Spread',
            'freq': 'D',
            'unit': '%',
            'src': 'Fed',
            'tf': 'level',
            'note': '10Y-3M 스프레드. NY Fed Estrella-Mishkin 모델 기반. 역전→12~18M 내 침체. 재역전 시 침체 임박'},
 'SAHMREALTIME': {'cat': '16_침체조기경보',
                  'kr': 'Sahm Rule 실시간',
                  'en': 'Real-time Sahm Rule Indicator',
                  'freq': 'M',
                  'unit': '%p',
                  'src': 'STL Fed',
                  'tf': 'level',
                  'note': 'Sahm Rule 실시간. 0.5↑=실업률 상승 기반 침체 신호. 전환점 조기경보로 활용'},
 'TCU': {'cat': '17_생산경기', 'kr': '설비가동률', 'en': 'Capacity Utilization Total', 'freq': 'M', 'unit': '%', 'src': 'Fed', 'tf': 'level', 'note': '설비가동률. 장기평균 79.6%. 80%↑ 인플레 압력. 75%↓ 경기 둔화. 70%↓ 심각 위축'},
 'ISRATIO': {'cat': '17_생산경기',
             'kr': '재고/판매 비율',
             'en': 'Inventory to Sales Ratio',
             'freq': 'M',
             'unit': 'Ratio',
             'src': 'Census',
             'tf': 'level',
             'note': '재고/판매 비율. 1.25↓=타이트(호황). 1.45↑=재고적체(둔화). 경기전환점 선행'},
 'AMTMNO': {'cat': '17_생산경기',
            'kr': '제조업 신규주문',
            'en': 'Manufacturers New Orders Total',
            'freq': 'M',
            'unit': 'Mil.USD',
            'src': 'Census',
            'tf': 'mom_pct',
            'note': '제조업 신규주문 MoM. 기업 투자 선행. 내구재보다 넓은 커버리지. 3M이평 추세 중시'},
 'MANEMP': {'cat': '17_생산경기',
            'kr': '제조업 고용',
            'en': 'Manufacturing Employment',
            'freq': 'M',
            'unit': 'Thousands',
            'src': 'BLS',
            'tf': 'mom_diff',
            'note': '제조업 고용 전월차. ISM 고용 프록시. 경기 민감 섹터. 음수 지속=제조업 침체'},
 'PSAVERT': {'cat': '18_소비가계', 'kr': '개인저축률', 'en': 'Personal Saving Rate', 'freq': 'M', 'unit': '%', 'src': 'BEA', 'tf': 'level', 'note': '개인저축률. 장기평균 약 7%. 3%↓ 과소비·가계 취약. 10%↑ 위축·예비적 저축'},
 'TOTALSA': {'cat': '18_소비가계', 'kr': '자동차 판매', 'en': 'Total Vehicle Sales', 'freq': 'M', 'unit': 'Mil.Units', 'src': 'BEA', 'tf': 'level', 'note': '자동차 판매. 장기평균 약 16M대. 금리 민감도 최고. 14M↓ 소비 위축 신호'},
 'DSPIC96': {'cat': '18_소비가계',
             'kr': '실질 가처분소득',
             'en': 'Real Disposable Personal Income',
             'freq': 'M',
             'unit': 'Bil.2017USD',
             'src': 'BEA',
             'tf': 'yoy_pct',
             'note': '실질 가처분소득 YoY. 소비 능력 실질 기반. 음수=실질 구매력 하락→소비 위축'},
 'PCEC96': {'cat': '18_소비가계',
            'kr': '실질 개인소비지출',
            'en': 'Real Personal Consumption',
            'freq': 'M',
            'unit': 'Bil.2017USD',
            'src': 'BEA',
            'tf': 'yoy_pct',
            'note': '실질 개인소비지출 YoY. GDP의 70%. 2%↓ 소비 둔화. 음수=침체 핵심 확인'},
 'DRCCLACBS': {'cat': '19_신용연체',
               'kr': '신용카드 연체율',
               'en': 'Delinquency Rate Credit Cards',
               'freq': 'Q',
               'unit': '%',
               'src': 'Fed',
               'tf': 'level',
               'note': '신용카드 연체율. 장기평균 3.5%. 4%↑ 가계 스트레스 경계. GFC 피크 6.8%'},
 'DRSFRMACBS': {'cat': '19_신용연체',
                'kr': '주택담보 연체율',
                'en': 'Delinquency Rate Single-Family Mortgages',
                'freq': 'Q',
                'unit': '%',
                'src': 'Fed',
                'tf': 'level',
                'note': '주택담보 연체율. 장기평균 약 3%. 4%↑ 주택시장 리스크. GFC 피크 11.5%'},
 'BUSLOANS': {'cat': '19_신용연체',
              'kr': '상업·산업 대출',
              'en': 'Commercial and Industrial Loans',
              'freq': 'M',
              'unit': 'Bil.USD',
              'src': 'Fed',
              'tf': 'yoy_pct',
              'note': 'C&I 대출 YoY. 증가=기업 투자 확대. 감소=은행 대출 기준 강화→경기 위축 선행'},
 'CONSUMER': {'cat': '19_신용연체',
              'kr': '소비자 대출',
              'en': 'Consumer Loans at Commercial Banks',
              'freq': 'M',
              'unit': 'Bil.USD',
              'src': 'Fed',
              'tf': 'yoy_pct',
              'note': '소비자 대출 YoY. 가계 레버리지 추세. 급감=소비 위축. 급증=과열 경계'},
 'IRSTCI01KRM156N': {'cat': '20_한국거시',
                     'kr': '한국 콜/인터뱅크 금리(익일)',
                     'en': 'Call Money/Interbank Rate: Total for Korea',
                     'freq': 'M',
                     'unit': '%',
                     'src': 'OECD',
                     'tf': 'level',
                     'note': '단기 유동성 여건 반영. 기준금리와 괴리 확대 시 시장 스트레스 점검'},
 'IRLTLT01KRM156N': {'cat': '20_한국거시',
                     'kr': '한국 국채 10년물',
                     'en': 'Interest Rates: Long-Term Government Bond Yields: 10-Year for Korea',
                     'freq': 'M',
                     'unit': '%',
                     'src': 'OECD',
                     'tf': 'level',
                     'note': '장기금리 벤치마크. 경기·물가·정책 기대 반영. 한미 10Y 스프레드(파생)로 교차 확인'},
 'LRHUTTTTKRM156S': {'cat': '20_한국거시',
                     'kr': '한국 실업률(15세+, SA)',
                     'en': 'Monthly Unemployment Rate Total: 15 Years or over for Korea',
                     'freq': 'M',
                     'unit': '%',
                     'src': 'OECD',
                     'tf': 'level',
                     'note': '실업률(계절조정). 상승=고용 둔화. 경기후행이지만 전환점에 민감'},
 'KORLOLITOAASTSAM': {'cat': '20_한국거시',
                      'kr': '한국 경기선행지수(OECD CLI)',
                      'en': 'OECD Composite Leading Indicator (Amplitude Adjusted) for Korea',
                      'freq': 'M',
                      'unit': 'Index',
                      'src': 'OECD',
                      'tf': 'level',
                      'note': 'OECD CLI(Amplitude Adjusted). 100 상회=확장, 100 하회=둔화. 방향 전환을 중점 관찰'},
 'NGDPRSAXDCKRQ': {'cat': '20_한국거시',
                   'kr': '한국 실질 GDP(분기, SA)',
                   'en': 'Real Gross Domestic Product for Republic of Korea',
                   'freq': 'Q',
                   'unit': 'Millions of Domestic Currency',
                   'src': 'IMF',
                   'tf': 'yoy_pct',
                   'note': '실질GDP(수준) 분기자료. 표의 전기비/중기비/YoY비는 수준 기반 변화율(%)로 계산'}}

# ═══════════════════════════════════════════════════════════
# 3. 빈도별 비교 기간 설정
# ═══════════════════════════════════════════════════════════

COMPARE_PERIODS = {
    "D": {"prev": 1,  "mid": 20, "yoy": 252},   # 전일 / 4주(20영업일) / 1년
    "W": {"prev": 1,  "mid": 4,  "yoy": 52},     # 전주 / 4주 / 1년
    "M": {"prev": 1,  "mid": 3,  "yoy": 12},     # 전월 / 3개월 / 1년
    "Q": {"prev": 1,  "mid": 2,  "yoy": 4},      # 전분기 / 2분기 / 1년
    "A": {"prev": 1,  "mid": 2,  "yoy": 3},      # 전년 / 2년전 / 3년전
}

MID_LABELS = {
    "D": "4W전비", "W": "4W전비", "M": "3M전비", "Q": "2Q전비", "A": "2Y전비"
}

# ═══════════════════════════════════════════════════════════
# 4. 핵심 함수 (Core Functions)
# ═══════════════════════════════════════════════════════════

def fetch_fred_series(series_id, api_key=FRED_API_KEY,
                      start_date=START_DATE, end_date=END_DATE):
    """FRED API에서 단일 시리즈 관측값을 조회한다 (최대 3회 재시도)."""
    params = {
        "series_id": series_id,
        "api_key":   api_key,
        "file_type": "json",
        "observation_start": start_date,
        "observation_end":   end_date,
        "sort_order": "desc"
    }
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            r = requests.get(FRED_BASE_URL, params=params, timeout=30)
            r.raise_for_status()
            obs = r.json().get("observations", [])
            return [{"date": o["date"], "value": float(o["value"])}
                    for o in obs if o["value"] != "."]
        except Exception as e:
            wait = RETRY_BACKOFF ** attempt
            print(f"  [RETRY {attempt}/{MAX_RETRIES}] {series_id}: {e}")
            if attempt < MAX_RETRIES:
                print(f"  → {wait:.1f}초 후 재시도...")
                time.sleep(wait)
            else:
                print(f"  [ERROR] {series_id}: {MAX_RETRIES}회 시도 실패")
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
    """구리/금 비율을 계산한다(금은 월평균으로 집계).
    금은 NASDAQQGLDI(지수단위, USD/oz 아님)를 사용하므로 비율 절대값은 무의미.
    방향성(상승=경기낙관, 하락=위험회피)만 유효하게 해석할 것."""
    cu = all_data.get("PCOPPUSDM", [])
    au = all_data.get("NASDAQQGLDI", [])
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


def _monthly_avg_map(obs):
    """관측값(list[{'date','value'}])을 YYYY-MM 기준 평균으로 집계한다."""
    m = {}
    for o in obs or []:
        ym = o['date'][:7]
        m.setdefault(ym, []).append(o['value'])
    return {ym: sum(vs) / len(vs) for ym, vs in m.items() if vs}


def calc_kor_us_10y_spread(all_data):
    """한미 10년물 금리차(한국 10Y - 미국 10Y, 미국은 일간→월평균)"""
    kor = _monthly_avg_map(all_data.get('IRLTLT01KRM156N', []))
    us  = _monthly_avg_map(all_data.get('DGS10', []))
    common = sorted(set(kor.keys()) & set(us.keys()), reverse=True)
    return [{'date': f"{ym}-01", 'value': round(kor[ym] - us[ym], 4)} for ym in common]


def calc_kor_us_policy_spread(all_data):
    """한미 기준금리 스프레드(한국 콜금리 - 미국 FFR, 미국은 일간→월평균)"""
    kor = _monthly_avg_map(all_data.get('IRSTCI01KRM156N', []))
    us  = _monthly_avg_map(all_data.get('DFF', []))
    common = sorted(set(kor.keys()) & set(us.keys()), reverse=True)
    return [{'date': f"{ym}-01", 'value': round(kor[ym] - us[ym], 4)} for ym in common]


# calculated 시리즈별 계산 함수 매핑
CALC_FUNCS = {
    'COPPER_GOLD_RATIO':    calc_copper_gold_ratio,
    'KOR_US_10Y_SPREAD':    calc_kor_us_10y_spread,
    'KOR_US_POLICY_SPREAD': calc_kor_us_policy_spread,
}


def get_series_obs(series_id, meta, all_data):
    """레지스트리 메타와 all_data를 받아 해당 시리즈의 관측값(list)을 반환한다."""
    if meta.get('tf') != 'calculated':
        return all_data.get(series_id, [])
    fn = CALC_FUNCS.get(series_id)
    return fn(all_data) if fn else []


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
    report.append(f"## 📊 거시경제 팩트 테이블\n")
    report.append(f"**기준일**: {END_DATE}\n")

    # 카테고리별 그룹화
    categories = {}
    for sid, m in registry.items():
        cat = m["cat"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(sid)

    for cat in sorted(categories.keys()):
        cat_label = cat.split("_", 1)[1]
        report.append(f"\n### {cat_label}\n")
        report.append("| 지표 | 주기 | 최신값 | 기준일 | 전기비 | 중기비 | YoY비 |")
        report.append("| --- | --- | --- | --- | --- | --- | --- |")

        for sid in categories[cat]:
            m = registry[sid]
            tf = m["tf"]
            obs = get_series_obs(sid, m, all_data)

            comp = get_comparisons(obs, m["freq"])
            val      = comp["val"]
            date_str = comp["date"] if comp["date"] else "-"
            chg_prev = calc_change(val, comp["prev"], tf)
            chg_mid  = calc_change(val, comp["mid"],  tf)
            chg_yoy  = calc_change(val, comp["yoy"],  tf)

            report.append(
                f"| {m['kr']} "
                f"| {m['freq']} "
                f"| {fmt_val(val)} "
                f"| {date_str} "
                f"| {fmt_chg(chg_prev, tf)} "
                f"| {fmt_chg(chg_mid, tf)} "
                f"| {fmt_chg(chg_yoy, tf)} |"
            )

    return "\n".join(report)

# ═══════════════════════════════════════════════════════════
# 6. Markdown 보고서 생성 (Claude-friendly)
# ═══════════════════════════════════════════════════════════

def write_markdown(fact_table_md, path):
    """Claude용 Markdown 보고서를 생성한다."""
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    lines = []
    lines.append("# FRED 거시경제 지표 보고서\n")
    lines.append(f"Generated at: {generated_at}")
    lines.append(f"Data range: {START_DATE} ~ {END_DATE}\n")

    lines.append("### Purpose\n")
    lines.append("이 파일은 GitHub Actions에 의해 자동 생성되며, Claude.ai 분석 컨텍스트로 사용됩니다.")
    lines.append("fred_latest.csv를 원천 데이터로, 이 Markdown을 요약 레이어로 활용하세요.\n")

    lines.append(f"### Included Series ({len(REG)}개)\n")
    lines.append("| # | Series ID | Category | Korean | English | Freq | Unit |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for i, (sid, m) in enumerate(REG.items(), 1):
        cat_label = m["cat"].split("_", 1)[1]
        lines.append(f"| {i} | {sid} | {cat_label} | {m['kr']} | {m['en']} | {m['freq']} | {m['unit']} |")

    lines.append("")
    lines.append(fact_table_md)
    lines.append("")

    lines.append("**비교 기간 범례**")
    lines.append("- **전기비**: D=전일, W=전주, M=전월, Q=전분기, A=전년")
    lines.append("- **중기비**: D/W=4주전, M=3개월전, Q=2분기전, A=2년전")
    lines.append("- **YoY비**: D/W/M=1년전, Q=4분기전, A=3년전\n")

    lines.append("### Instruction for Claude\n")
    lines.append("- fred_latest.csv를 원천 데이터셋으로 취급하세요.")
    lines.append("- 이 파일로 포함된 경제지표 구성을 파악하세요.")
    lines.append("- 거시경제 분석 요청 시, 최신값과 과거 관측값을 비교하세요.")
    lines.append("- 값이 -이거나 비어 있으면 해당 관측이 불가함을 명시하세요.")
    lines.append("- 전기비·중기비·YoY비를 모두 활용하여 추세를 판단하세요.")

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ Markdown 저장: {path}")

# ═══════════════════════════════════════════════════════════
# 7. CSV 저장 함수
# ═══════════════════════════════════════════════════════════

def save_csv(all_data, registry, path):
    """전체 데이터를 CSV로 저장한다."""
    rows = []
    for sid, m in registry.items():
        obs = get_series_obs(sid, m, all_data)

        comp = get_comparisons(obs, m["freq"])
        tf   = m["tf"]
        val  = comp["val"]

        rows.append({
            "series_id":    sid,
            "category":     m["cat"],
            "korean_name":  m["kr"],
            "english_name": m["en"],
            "frequency":    m["freq"],
            "unit":         m["unit"],
            "source":       m["src"],
            "transform":    tf,
            "latest_date":  comp["date"] if comp["date"] else "",
            "latest_value": val if val is not None else "",
            "chg_prev":     calc_change(val, comp["prev"], tf) or "",
            "chg_mid":      calc_change(val, comp["mid"],  tf) or "",
            "chg_yoy":      calc_change(val, comp["yoy"],  tf) or "",
            "note":         m["note"],
        })

    df = pd.DataFrame(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"✅ CSV 저장: {path} ({len(df)}건)")

# ═══════════════════════════════════════════════════════════
# 8. 메인 실행 흐름
# ═══════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("FRED API 거시경제 팩트 테이블 생성 (풀 버전)")
    print(f"기간: {START_DATE} ~ {END_DATE}")
    print("=" * 60)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)

    print("\n[1/4] FRED API 데이터 조회...")
    all_data = fetch_all_series(REG)

    api_total = sum(1 for m in REG.values() if m["tf"] != "calculated")
    success   = sum(1 for sid, obs in all_data.items() if obs)
    rate      = success / api_total if api_total > 0 else 0
    print(f"\n  → 성공: {success}/{api_total} ({rate:.0%})")
    if rate < MIN_SUCCESS_RATE:
        print(f"❌ 성공률 {rate:.0%} < {MIN_SUCCESS_RATE:.0%} → 중단합니다.")
        sys.exit(1)
    print("\n[2/4] 파생지표 계산...")
    for k, fn in CALC_FUNCS.items():
        obs = fn(all_data)
        print(f"  → {k}: {len(obs)}건")

    print("\n[3/4] 팩트 테이블 생성...")
    fact_md = generate_fact_table(all_data, REG)
    md_path = DATA_DIR / "fred_latest.md"
    write_markdown(fact_md, md_path)

    print("\n[4/4] CSV 저장...")
    csv_path = DATA_DIR / "fred_latest.csv"
    save_csv(all_data, REG, csv_path)

    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    hist_path = HISTORY_DIR / f"fred_{ts}.csv"
    save_csv(all_data, REG, hist_path)

    print("\n" + "=" * 60)
    print("✅ 완료")
    print("=" * 60)


if __name__ == "__main__":
    main()
