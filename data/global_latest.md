# Global Macro 보조지표 보고서

> **데이터 성격: 글로벌 보조 (Supplementary)**
> - 공식 거시경제 기준: `fred_latest.md` (FRED API)
> - 본 파일: World Bank / OECD / IMF / ECB — API Key 불필요
> - FRED·Market 레이어와 merge 없음. 충돌 시 **항상 FRED 우선**
> - 한국 CLI는 FRED `KORLOLITOAASTSAM`과 중복 가능 — 교차 확인용

Generated at: 2026-08-10 22:07:08 UTC
Data range: 2023-08-11 ~ 2026-08-10
Series count: 6

### Included Series

| # | Series ID | Category | Korean | English | Freq | Unit | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | OECD_KR_CLI | 선행지수 | 한국 OECD CLI | OECD CLI Korea | M | Index | OECD |
| 2 | OECD_US_CLI | 선행지수 | 미국 OECD CLI | OECD CLI USA | M | Index | OECD |
| 3 | OECD_DEU_CLI | 선행지수 | 독일 OECD CLI | OECD CLI Germany | M | Index | OECD |
| 4 | IMF_KR_CURRENT_ACCOUNT | 대외 | 한국 경상수지 | Korea Current Account Balance | Q | USD | IMF |
| 5 | ECB_EURUSD | 금융 | EUR/USD | EUR/USD Exchange Rate | D | USD/EUR | ECB |
| 6 | ECB_POLICY_RATE_MRO | 금융 | ECB MRO 금리 | ECB Main Refinancing Rate | M | % | ECB |

## 🌍 글로벌 거시 보조 팩트 테이블

**기준일**: 2026-08-10


### 선행지수

| 지표 | 주기 | 최신값 | 기준일 | 전기비 | 중기비 | YoY비 |
| --- | --- | --- | --- | --- | --- | --- |
| 한국 OECD CLI | M | 102.87 | 2026-06-01 | +0.21 | +0.87 | +3.26 |
| 미국 OECD CLI | M | 100.80 | 2026-06-01 | +0.04 | +0.16 | +1.15 |
| 독일 OECD CLI | M | 100.72 | 2026-06-01 | -0.04 | -0.17 | +0.40 |

### 대외

| 지표 | 주기 | 최신값 | 기준일 | 전기비 | 중기비 | YoY비 |
| --- | --- | --- | --- | --- | --- | --- |
| 한국 경상수지 | Q | 73.78B | 2026-01-01 | +34610700000.00 | +37765500000.00 | +54292500000.00 |

### 금융

| 지표 | 주기 | 최신값 | 기준일 | 전기비 | 중기비 | YoY비 |
| --- | --- | --- | --- | --- | --- | --- |
| EUR/USD | D | 1.16 | 2026-08-10 | +0.00 | +0.01 | -0.02 |
| ECB MRO 금리 | M | 2.40 | 2026-06-17 | +0.25 | -0.25 | - |

**비교 기간 범례**
- **전기비**: D=전일, W=전주, M=전월, Q=전분기, A=전년
- **중기비**: D/W=4주전, M=3개월전, Q=2분기전, A=2년전
- **YoY비**: D/W/M=1년전, Q=4분기전, A=3년전

### Instruction for Claude

- 본 파일은 글로벌 보조 레이어입니다. 공식 분석은 fred_latest.md를 우선하세요.
- IMF 경상수지 단위는 USD(raw). OECD CLI는 100=추세 기준입니다.
- World Bank 지표는 연간(A) 업데이트 lag가 클 수 있습니다.