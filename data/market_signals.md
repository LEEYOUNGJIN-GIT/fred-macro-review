# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-07-31 (oldest: 2026-07-30 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-07-31 21:59:21 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 27.0100 | KOSPI YoY=+75.22%, KOSDAQ YoY=-21.20%, KOSPI 4W=-32.64% |
| 2 | Breadth | 🔵 중립 | 0.2878 | RSP/SPY=0.2878 (Ratio, 무차원), 4W Δ=-0.0007 |
| 3 | Risk-on/off | 🟢 risk-on | 1.8346 | SPHB/SPLV=1.8346 (Ratio, 무차원), 4W Δ=-0.0959 |
| 4 | VIX Term | 🟡 backwardation | 1.0862 | VIX3M=19.02, VIX/VIX3M=1.0862 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.55 |
| 5 | 섹터 로테이션 | 🟠 경계 | -14.7900 | XLK 4W=-2.90%, XLE 4W=+11.89%, XLK-XLE=-14.79%p, XLP 4W=+0.07%, 방어(XLP) > 기술 → risk-off 로테이션 |
| 6 | 신용 방향 | 🟢 완화 | 0.7480 | HYG/LQD=0.7480 (Ratio, OAS 아님), 4W Δ=+0.0143 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 27.01
- **상세**: KOSPI YoY=+75.22%, KOSDAQ YoY=-21.20%, KOSPI 4W=-32.64%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.28782
- **상세**: RSP/SPY=0.2878 (Ratio, 무차원), 4W Δ=-0.0007
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.83458
- **상세**: SPHB/SPLV=1.8346 (Ratio, 무차원), 4W Δ=-0.0959
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟡 VIX Term — backwardation
- **값**: 1.0862
- **상세**: VIX3M=19.02, VIX/VIX3M=1.0862 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.55
- **시리즈**: ^VIX3M, VIXCLS

### 🟠 섹터 로테이션 — 경계
- **값**: -14.79
- **상세**: XLK 4W=-2.90%, XLE 4W=+11.89%, XLK-XLE=-14.79%p, XLP 4W=+0.07%, 방어(XLP) > 기술 → risk-off 로테이션
- **시리즈**: XLK, XLE, XLP

### 🟢 신용 방향 — 완화
- **값**: 0.748047
- **상세**: HYG/LQD=0.7480 (Ratio, OAS 아님), 4W Δ=+0.0143
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*