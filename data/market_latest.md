# Market 보조지표 보고서

> **데이터 성격: 보조지표 (Supplementary)**
> - 공식 거시경제 기준: `fred_latest.md` (FRED API)
> - 본 파일: Yahoo Finance 일봉 — 시장·한국·breadth 보조
> - 단위: Index=지수 종가 | USD=ETF adjusted close | Ratio=무차원(절대값 해석 금지)
> - 미포함(FRED 사용): 금리, VIX, SP500, WTI, USD/KRW, USD/JPY, USD/CNY, CPI/PCE, 고용
> - fetch 1건이라도 실패 시 본 파일은 갱신되지 않음

Generated at: 2026-10-01 00:18:12 UTC
Source: Yahoo Finance (unofficial) | Rows: 25 (fixed)

### Included Series (25개)

| # | Series ID | Category | Korean | English | Freq | Unit |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | ^KS11 | 한국주식 | KOSPI | KOSPI Index | D | Index |
| 2 | ^KQ11 | 한국주식 | KOSDAQ | KOSDAQ Index | D | Index |
| 3 | ^NDX | 미국지수 | 나스닥 100 | Nasdaq 100 | D | Index |
| 4 | ^RUT | 미국지수 | 러셀 2000 | Russell 2000 | D | Index |
| 5 | ^VIX3M | 변동성 | VIX 3개월 | VIX 3-Month | D | Index |
| 6 | RSP | breadth | S&P 동일가중 ETF | S&P Equal Weight ETF | D | USD |
| 7 | SPY | breadth | S&P 500 ETF | SPDR S&P 500 ETF | D | USD |
| 8 | SPHB | risk | S&P 고베타 ETF | S&P High Beta ETF | D | USD |
| 9 | SPLV | risk | S&P 저변동 ETF | S&P Low Vol ETF | D | USD |
| 10 | XLK | 섹터 | 섹터:기술 | Sector: Technology | D | USD |
| 11 | XLF | 섹터 | 섹터:금융 | Sector: Financials | D | USD |
| 12 | XLE | 섹터 | 섹터:에너지 | Sector: Energy | D | USD |
| 13 | XLP | 섹터 | 섹터:필수소비 | Sector: Staples | D | USD |
| 14 | XLU | 섹터 | 섹터:유틸리티 | Sector: Utilities | D | USD |
| 15 | XLY | 섹터 | 섹터:경기소비 | Sector: Discretionary | D | USD |
| 16 | KRE | 신용 | 지역은행 ETF | Regional Banks ETF | D | USD |
| 17 | HYG | 신용 | 하이일드 ETF | HY Credit ETF | D | USD |
| 18 | LQD | 신용 | IG 회사채 ETF | IG Credit ETF | D | USD |
| 19 | ^N225 | 글로벌 | 닛케이 225 | Nikkei 225 | D | Index |
| 20 | ^HSI | 글로벌 | 항셍 | Hang Seng Index | D | Index |
| 21 | EEM | 글로벌 | 신흥국 ETF | Emerging Markets ETF | D | USD |
| 22 | AUDJPY=X | FX | AUD/JPY | AUD/JPY FX | D | JPY_per_AUD |
| 23 | MARKET_BREADTH | 파생 | 시장 Breadth | RSP/SPY Ratio | D | Ratio |
| 24 | MARKET_RISK_ON | 파생 | Risk-on/off | SPHB/SPLV Ratio | D | Ratio |
| 25 | HYG_LQD_RATIO | 파생 | HY/IG 가격비 | HYG/LQD Ratio | D | Ratio |

## Market 보조 팩트 테이블

**기준일**: 2026-10-01


### 한국주식

| 지표 | 주기 | 최신값 | 기준일 | 전기비 | 4W전비 | YoY비 |
| --- | --- | --- | --- | --- | --- | --- |
| KOSPI | D | 6,870.81 | 2026-09-29 | -18.93 | +81.93 | +3475.27 |
| KOSDAQ | D | 849.80 | 2026-09-29 | +3.22 | +11.39 | +2.72 |

### 미국지수

| 지표 | 주기 | 최신값 | 기준일 | 전기비 | 4W전비 | YoY비 |
| --- | --- | --- | --- | --- | --- | --- |
| 나스닥 100 | D | 30,409 | 2026-09-30 | +69.17 | +1331.28 | +5797.15 |
| 러셀 2000 | D | 2,796.86 | 2026-09-30 | -11.06 | -123.27 | +361.61 |

### 변동성

| 지표 | 주기 | 최신값 | 기준일 | 전기비 | 4W전비 | YoY비 |
| --- | --- | --- | --- | --- | --- | --- |
| VIX 3개월 | D | 18.37 | 2026-09-30 | +0.28 | +0.04 | -0.39 |

### breadth

| 지표 | 주기 | 최신값 | 기준일 | 전기비 | 4W전비 | YoY비 |
| --- | --- | --- | --- | --- | --- | --- |
| S&P 동일가중 ETF | D | 209.50 | 2026-09-29 | -0.24 | -9.07 | +23.90 |
| S&P 500 ETF | D | 764.20 | 2026-09-29 | -1.41 | -0.95 | +109.44 |

### risk

| 지표 | 주기 | 최신값 | 기준일 | 전기비 | 4W전비 | YoY비 |
| --- | --- | --- | --- | --- | --- | --- |
| S&P 고베타 ETF | D | 151.83 | 2026-09-29 | +1.33 | +5.67 | +43.03 |
| S&P 저변동 ETF | D | 71.19 | 2026-09-29 | +0.07 | -3.35 | -0.00 |

### 섹터

| 지표 | 주기 | 최신값 | 기준일 | 전기비 | 4W전비 | YoY비 |
| --- | --- | --- | --- | --- | --- | --- |
| 섹터:기술 | D | 194.50 | 2026-09-29 | -0.03 | +8.22 | +55.79 |
| 섹터:금융 | D | 54.01 | 2026-09-29 | -0.18 | -3.50 | +0.99 |
| 섹터:에너지 | D | 61.54 | 2026-09-29 | -0.56 | -2.04 | +16.82 |
| 섹터:필수소비 | D | 81.85 | 2026-09-29 | -0.43 | -2.57 | +5.97 |
| 섹터:유틸리티 | D | 39.71 | 2026-09-29 | +0.46 | -2.21 | -2.49 |
| 섹터:경기소비 | D | 109.15 | 2026-09-29 | +0.15 | -7.18 | -9.73 |

### 신용

| 지표 | 주기 | 최신값 | 기준일 | 전기비 | 4W전비 | YoY비 |
| --- | --- | --- | --- | --- | --- | --- |
| 지역은행 ETF | D | 69.83 | 2026-09-29 | -0.72 | -3.31 | +7.13 |
| 하이일드 ETF | D | 77.36 | 2026-09-29 | -0.18 | -2.02 | +0.93 |
| IG 회사채 ETF | D | 102.41 | 2026-09-29 | -0.06 | -3.36 | -3.82 |

### 글로벌

| 지표 | 주기 | 최신값 | 기준일 | 전기비 | 4W전비 | YoY비 |
| --- | --- | --- | --- | --- | --- | --- |
| 닛케이 225 | D | 67,371 | 2026-10-01 | +1889.50 | +965.21 | +22602.65 |
| 항셍 | D | 24,524 | 2026-09-29 | -118.94 | -806.16 | -2021.28 |
| 신흥국 ETF | D | 67.40 | 2026-09-29 | +0.20 | +0.38 | +15.70 |

### FX

| 지표 | 주기 | 최신값 | 기준일 | 전기비 | 4W전비 | YoY비 |
| --- | --- | --- | --- | --- | --- | --- |
| AUD/JPY | D | 109.47 | 2026-10-01 | -0.53 | -4.37 | +9.12 |

### 파생

| 지표 | 주기 | 최신값 | 기준일 | 전기비 | 4W전비 | YoY비 |
| --- | --- | --- | --- | --- | --- | --- |
| 시장 Breadth | D | 0.27 | 2026-09-29 | +0.0002 | -0.0115 | -0.0093 |
| Risk-on/off | D | 2.13 | 2026-09-29 | +0.0166 | +0.1720 | +0.6045 |
| HY/IG 가격비 | D | 0.76 | 2026-09-29 | -0.0013 | +0.0049 | +0.0359 |

**비교 기간 범례**
- **전기비**: 전일 | **4W전비**: 20영업일 전 | **YoY비**: 252영업일 전

### Instruction for Claude

- **본 파일은 보조지표입니다.** 공식 거시 분석은 fred_latest.md를 기준으로 하세요.
- 충돌 시 항상 FRED(fred_latest.md)를 우선하세요.
- Ratio(unit) 지표는 무차원입니다. 절대값 기준 없이 전기/YoY 방향만 해석하세요.
- ETF(USD)와 Index는 다른 단위입니다. SP500(FRED)와 SPY(Yahoo)를 동일 지표로 취급하지 마세요.
- 값이 비어 있으면 해당 fetch가 실패했음을 의미합니다.