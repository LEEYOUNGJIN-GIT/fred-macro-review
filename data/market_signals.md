# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-10-21 (oldest: 2026-10-16 ^HSI)
> Freshness: OK (oldest 4d ≤ 5d)
> Generated: 2026-10-20 23:34:12 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 32.2500 | KOSPI YoY=+68.43%, KOSDAQ YoY=-3.93%, KOSPI 4W=-12.97% |
| 2 | Breadth | 🔵 중립 | 0.2807 | RSP/SPY=0.2807 (Ratio, 무차원), 4W Δ=+0.0055, 4W 상승=breadth 개선 |
| 3 | Risk-on/off | 🟢 risk-on | 1.8968 | SPHB/SPLV=1.8968 (Ratio, 무차원), 4W Δ=-0.2389 |
| 4 | VIX Term | 🟡 backwardation | 1.0527 | VIX3M=18.99, VIX/VIX3M=1.0527 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+1.38 |
| 5 | 섹터 로테이션 | 🟠 경계 | -15.5400 | XLK 4W=-5.52%, XLE 4W=+10.02%, XLK-XLE=-15.54%p, XLP 4W=+6.07%, 방어(XLP) > 기술 → risk-off 로테이션 |
| 6 | 신용 방향 | 🔵 중립 | 0.7443 | HYG/LQD=0.7443 (Ratio, OAS 아님), 4W Δ=-0.0042 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 32.25
- **상세**: KOSPI YoY=+68.43%, KOSDAQ YoY=-3.93%, KOSPI 4W=-12.97%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.280684
- **상세**: RSP/SPY=0.2807 (Ratio, 무차원), 4W Δ=+0.0055, 4W 상승=breadth 개선
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.896834
- **상세**: SPHB/SPLV=1.8968 (Ratio, 무차원), 4W Δ=-0.2389
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟡 VIX Term — backwardation
- **값**: 1.0527
- **상세**: VIX3M=18.99, VIX/VIX3M=1.0527 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+1.38
- **시리즈**: ^VIX3M, VIXCLS

### 🟠 섹터 로테이션 — 경계
- **값**: -15.54
- **상세**: XLK 4W=-5.52%, XLE 4W=+10.02%, XLK-XLE=-15.54%p, XLP 4W=+6.07%, 방어(XLP) > 기술 → risk-off 로테이션
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.744333
- **상세**: HYG/LQD=0.7443 (Ratio, OAS 아님), 4W Δ=-0.0042
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*