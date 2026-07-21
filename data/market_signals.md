# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-07-21 (oldest: 2026-07-17 ^N225)
> Freshness: OK (oldest 4d ≤ 5d)
> Generated: 2026-07-21 21:59:08 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 54.6400 | KOSPI YoY=+112.99%, KOSDAQ YoY=-3.70%, KOSPI 4W=-28.02% |
| 2 | Breadth | 🔵 중립 | 0.2843 | RSP/SPY=0.2843 (Ratio, 무차원), 4W Δ=+0.0027 |
| 3 | Risk-on/off | 🟢 risk-on | 1.9147 | SPHB/SPLV=1.9147 (Ratio, 무차원), 4W Δ=-0.2296 |
| 4 | VIX Term | 🔵 중립 | 0.9581 | VIX3M=19.59, VIX/VIX3M=0.9581 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.02 |
| 5 | 섹터 로테이션 | 🟠 경계 | -14.1300 | XLK 4W=-5.92%, XLE 4W=+8.21%, XLK-XLE=-14.13%p, XLP 4W=+2.29%, 방어(XLP) > 기술 → risk-off 로테이션 |
| 6 | 신용 방향 | 🟢 완화 | 0.7454 | HYG/LQD=0.7454 (Ratio, OAS 아님), 4W Δ=+0.0114 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 54.64
- **상세**: KOSPI YoY=+112.99%, KOSDAQ YoY=-3.70%, KOSPI 4W=-28.02%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.284332
- **상세**: RSP/SPY=0.2843 (Ratio, 무차원), 4W Δ=+0.0027
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.914697
- **상세**: SPHB/SPLV=1.9147 (Ratio, 무차원), 4W Δ=-0.2296
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🔵 VIX Term — 중립
- **값**: 0.9581
- **상세**: VIX3M=19.59, VIX/VIX3M=0.9581 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.02
- **시리즈**: ^VIX3M, VIXCLS

### 🟠 섹터 로테이션 — 경계
- **값**: -14.13
- **상세**: XLK 4W=-5.92%, XLE 4W=+8.21%, XLK-XLE=-14.13%p, XLP 4W=+2.29%, 방어(XLP) > 기술 → risk-off 로테이션
- **시리즈**: XLK, XLE, XLP

### 🟢 신용 방향 — 완화
- **값**: 0.745438
- **상세**: HYG/LQD=0.7454 (Ratio, OAS 아님), 4W Δ=+0.0114
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*