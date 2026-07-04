# Global Macro 보조지표 보고서

> **데이터 성격: 글로벌 보조 (Supplementary)**
> - 공식 거시경제 기준: `fred_latest.md` (FRED API)
> - 본 파일: World Bank / OECD / IMF / ECB — API Key 불필요
> - FRED·Market 레이어와 merge 없음. 충돌 시 **항상 FRED 우선**
> - 한국 CLI는 FRED `KORLOLITOAASTSAM`과 중복 가능 — 교차 확인용

Generated at: 2026-07-04 22:13:54 UTC
Data range: 2023-07-05 ~ 2026-07-04
Series count: 12

### Included Series

| # | Series ID | Category | Korean | English | Freq | Unit | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | WB_KR_GDP_GROWTH | 성장 | 한국 실질 GDP 성장률 | Korea Real GDP Growth | A | % | World Bank |
| 2 | WB_US_GDP_GROWTH | 성장 | 미국 실질 GDP 성장률 | US Real GDP Growth | A | % | World Bank |
| 3 | WB_KR_CPI | 물가 | 한국 CPI 인플레이션 | Korea CPI Inflation | A | % | World Bank |
| 4 | WB_US_CPI | 물가 | 미국 CPI 인플레이션 | US CPI Inflation | A | % | World Bank |
| 5 | WB_KR_UNEMP | 노동 | 한국 실업률 | Korea Unemployment Rate | A | % | World Bank |
| 6 | WB_US_UNEMP | 노동 | 미국 실업률 | US Unemployment Rate | A | % | World Bank |
| 7 | OECD_KR_CLI | 선행지수 | 한국 OECD CLI | OECD CLI Korea | M | Index | OECD |
| 8 | OECD_US_CLI | 선행지수 | 미국 OECD CLI | OECD CLI USA | M | Index | OECD |
| 9 | OECD_DEU_CLI | 선행지수 | 독일 OECD CLI | OECD CLI Germany | M | Index | OECD |
| 10 | IMF_KR_CURRENT_ACCOUNT | 대외 | 한국 경상수지 | Korea Current Account Balance | Q | USD | IMF |
| 11 | ECB_EURUSD | 금융 | EUR/USD | EUR/USD Exchange Rate | D | USD/EUR | ECB |
| 12 | ECB_POLICY_RATE_MRO | 금융 | ECB MRO 금리 | ECB Main Refinancing Rate | M | % | ECB |

## 🌍 글로벌 거시 보조 팩트 테이블

**기준일**: 2026-07-04


### 성장

| 지표 | 주기 | 최신값 | 기준일 | 전기비 | 중기비 | YoY비 |
| --- | --- | --- | --- | --- | --- | --- |
| 한국 실질 GDP 성장률 | A | 1.01 | 2025-01-01 | -1.00 | -0.58 | - |
| 미국 실질 GDP 성장률 | A | 2.16 | 2025-01-01 | -0.63 | -0.77 | - |

### 물가

| 지표 | 주기 | 최신값 | 기준일 | 전기비 | 중기비 | YoY비 |
| --- | --- | --- | --- | --- | --- | --- |
| 한국 CPI 인플레이션 | A | 2.12 | 2025-01-01 | -0.20 | -1.47 | - |
| 미국 CPI 인플레이션 | A | 2.95 | 2024-01-01 | -1.17 | - | - |

### 노동

| 지표 | 주기 | 최신값 | 기준일 | 전기비 | 중기비 | YoY비 |
| --- | --- | --- | --- | --- | --- | --- |
| 한국 실업률 | A | 2.68 | 2025-01-01 | -0.10 | +0.01 | - |
| 미국 실업률 | A | 4.20 | 2025-01-01 | +0.18 | +0.56 | - |

### 선행지수

| 지표 | 주기 | 최신값 | 기준일 | 전기비 | 중기비 | YoY비 |
| --- | --- | --- | --- | --- | --- | --- |
| 한국 OECD CLI | M | 102.60 | 2026-05-01 | +0.28 | +0.91 | +2.92 |
| 미국 OECD CLI | M | 101.02 | 2026-05-01 | +0.10 | +0.37 | +1.42 |
| 독일 OECD CLI | M | 100.84 | 2026-05-01 | -0.05 | -0.14 | +0.66 |

### 대외

| 지표 | 주기 | 최신값 | 기준일 | 전기비 | 중기비 | YoY비 |
| --- | --- | --- | --- | --- | --- | --- |
| 한국 경상수지 | Q | 73.78B | 2026-01-01 | +34610700000.00 | +37765500000.00 | +54292500000.00 |

### 금융

| 지표 | 주기 | 최신값 | 기준일 | 전기비 | 중기비 | YoY비 |
| --- | --- | --- | --- | --- | --- | --- |
| EUR/USD | D | 1.14 | 2026-07-03 | +0.00 | -0.02 | -0.03 |
| ECB MRO 금리 | M | 2.40 | 2026-06-17 | +0.25 | -0.25 | - |

**비교 기간 범례**
- **전기비**: D=전일, W=전주, M=전월, Q=전분기, A=전년
- **중기비**: D/W=4주전, M=3개월전, Q=2분기전, A=2년전
- **YoY비**: D/W/M=1년전, Q=4분기전, A=3년전

### Instruction for Claude

- 본 파일은 글로벌 보조 레이어입니다. 공식 분석은 fred_latest.md를 우선하세요.
- IMF 경상수지 단위는 USD(raw). OECD CLI는 100=추세 기준입니다.
- World Bank 지표는 연간(A) 업데이트 lag가 클 수 있습니다.