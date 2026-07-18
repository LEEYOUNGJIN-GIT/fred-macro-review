# Alpha Vantage 보조지표 보고서

> **데이터 성격: AV 보조 (Supplementary)**
> - 공식 거시경제 기준: `fred_latest.md` (FRED API)
> - 본 파일: Alpha Vantage — commodities / FX / crypto 보조
> - FRED·Market·Global과 merge 없음. 충돌 시 **항상 FRED 우선**
> - 일 12 API calls / 12 series | Rate limit 5/min·25/day·1/sec 준수
> - fetch 1 call이라도 실패 시 본 파일은 갱신되지 않음

Generated at: 2026-07-18 22:13:56 UTC
Source: Alpha Vantage | Rows: 12 (fixed)

### Included Series (12개)

| # | Series ID | Category | Korean | English | Freq | Unit |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | AV_GOLD_SPOT | 금속 | 금 프록시(GLD ETF) | Gold Proxy GLD ETF | D | USD/oz |
| 2 | AV_SILVER_SPOT | 금속 | 은 프록시(SLV ETF) | Silver Proxy SLV ETF | D | USD |
| 3 | AV_COPPER | 원자재 | 구리 | Copper | M | USD/MT |
| 4 | AV_ALUMINUM | 원자재 | 알루미늄 | Aluminum | M | USD/MT |
| 5 | AV_WHEAT | 원자재 | 밀 | Wheat | M | USD/MT |
| 6 | AV_CORN | 원자재 | 옥수수 | Corn | M | USD/MT |
| 7 | AV_BRENT | 원자재 | 브렌트유 | Brent Crude | M | USD/Barrel |
| 8 | AV_USDKRW | FX | USD/KRW | USD/KRW | D | KRW/USD |
| 9 | AV_USDJPY | FX | USD/JPY | USD/JPY | D | JPY/USD |
| 10 | AV_USDCNY | FX | USD/CNY | USD/CNY | D | CNY/USD |
| 11 | AV_BTCUSD | 크립토 | 비트코인(USD) | Bitcoin USD | D | USD |
| 12 | AV_ETHUSD | 크립토 | 이더리움(USD) | Ethereum USD | D | USD |

## AV 보조 팩트 테이블

**기준일**: 2026-07-18


### 금속

| 지표 | 주기 | 최신값 | 기준일 | 전기비 | 4W전비 | YoY비 |
| --- | --- | --- | --- | --- | --- | --- |
| 금 프록시(GLD ETF) | D | 368.41 | 2026-07-17 | +3.45 | -20.19 | - |
| 은 프록시(SLV ETF) | D | 50.78 | 2026-07-17 | +0.39 | -9.83 | - |

### 원자재

| 지표 | 주기 | 최신값 | 기준일 | 전기비 | 3M전비 | YoY비 |
| --- | --- | --- | --- | --- | --- | --- |
| 구리 | M | 13,552 | 2026-06-01 | +0.30% | +8.17% | +37.79% |
| 알루미늄 | M | 3,438.85 | 2026-06-01 | -6.00% | +1.95% | +36.14% |
| 밀 | M | 199.65 | 2026-06-01 | -9.61% | +2.98% | +15.27% |
| 옥수수 | M | 195.78 | 2026-06-01 | -9.20% | -8.21% | +0.03% |
| 브렌트유 | M | 85.40 | 2026-06-01 | -20.29% | -17.19% | +19.54% |

### FX

| 지표 | 주기 | 최신값 | 기준일 | 전기비 | 4W전비 | YoY비 |
| --- | --- | --- | --- | --- | --- | --- |
| USD/KRW | D | 1,487.44 | 2026-07-17 | +8.07 | -42.47 | - |
| USD/JPY | D | 162.39 | 2026-07-17 | +0.01 | +1.11 | - |
| USD/CNY | D | 6.78 | 2026-07-17 | -0.00 | +0.01 | - |

### 크립토

| 지표 | 주기 | 최신값 | 기준일 | 전기비 | 4W전비 | YoY비 |
| --- | --- | --- | --- | --- | --- | --- |
| 비트코인(USD) | D | 63,914 | 2026-07-18 | +0.03% | +7.46% | -37.51% |
| 이더리움(USD) | D | 1,841.04 | 2026-07-18 | +0.01% | +17.31% | -45.86% |

**비교 기간 범례**
- **전기비**: D=전일, W=전주, M=전월, Q=전분기, A=전년
- **중기비**: 4W전비 (D), 3M전비 (M) 등
- **YoY비**: D/W/M=1년전, Q=4분기전, A=3년전

### Instruction for Claude

- **본 파일은 AV 보조 레이어입니다.** 공식 분석은 fred_latest.md를 우선하세요.
- 크립토(BTC/ETH)는 공식 거시가 아닌 risk sentiment 보조입니다.
- BRENT는 FRED WTI(DCOILWTICO)와 교차 확인하세요.
- 값이 비어 있으면 해당 fetch가 실패했음을 의미합니다.