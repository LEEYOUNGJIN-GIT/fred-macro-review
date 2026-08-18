# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-08-18 (oldest: 2026-08-14 ^KS11)
> Freshness: OK (oldest 4d ≤ 5d)
> Generated: 2026-08-18 21:16:41 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 65.5300 | KOSPI YoY=+123.69%, KOSDAQ YoY=+7.38%, KOSPI 4W=+2.31% |
| 2 | Breadth | 🔵 중립 | 0.2864 | RSP/SPY=0.2864 (Ratio, 무차원), 4W Δ=+0.0021 |
| 3 | Risk-on/off | 🟢 risk-on | 1.9267 | SPHB/SPLV=1.9267 (Ratio, 무차원), 4W Δ=+0.0120 |
| 4 | VIX Term | 🟢 contango | 0.7395 | VIX3M=19.27, VIX/VIX3M=0.7395 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.30 |
| 5 | 섹터 로테이션 | 🟠 경계 | -6.1700 | XLK 4W=+2.68%, XLE 4W=+8.85%, XLK-XLE=-6.17%p, XLP 4W=+1.81% |
| 6 | 신용 방향 | 🟢 완화 | 0.7514 | HYG/LQD=0.7514 (Ratio, OAS 아님), 4W Δ=+0.0064 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 65.53
- **상세**: KOSPI YoY=+123.69%, KOSDAQ YoY=+7.38%, KOSPI 4W=+2.31%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.28639
- **상세**: RSP/SPY=0.2864 (Ratio, 무차원), 4W Δ=+0.0021
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.92674
- **상세**: SPHB/SPLV=1.9267 (Ratio, 무차원), 4W Δ=+0.0120
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.7395
- **상세**: VIX3M=19.27, VIX/VIX3M=0.7395 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.30
- **시리즈**: ^VIX3M, VIXCLS

### 🟠 섹터 로테이션 — 경계
- **값**: -6.17
- **상세**: XLK 4W=+2.68%, XLE 4W=+8.85%, XLK-XLE=-6.17%p, XLP 4W=+1.81%
- **시리즈**: XLK, XLE, XLP

### 🟢 신용 방향 — 완화
- **값**: 0.751417
- **상세**: HYG/LQD=0.7514 (Ratio, OAS 아님), 4W Δ=+0.0064
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*