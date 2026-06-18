# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-06-18 (oldest: 2026-06-17 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-06-18 22:53:25 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 128.7400 | KOSPI YoY=+219.91%, KOSDAQ YoY=+37.56%, KOSPI 4W=+17.94% |
| 2 | Breadth | 🔵 중립 | 0.2812 | RSP/SPY=0.2812 (Ratio, 무차원), 4W Δ=+0.0062, 4W 상승=breadth 개선 |
| 3 | Risk-on/off | 🟢 강한 risk-on | 2.1212 | SPHB/SPLV=2.1212 (Ratio, 무차원), 4W Δ=+0.2497 |
| 4 | VIX Term | 🟢 contango | 0.8385 | VIX3M=19.57, VIX/VIX3M=0.8385 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-1.79 |
| 5 | 섹터 로테이션 | 🟢 확장 | 18.1500 | XLK 4W=+8.07%, XLE 4W=-10.08%, XLK-XLE=+18.15%p, XLP 4W=-2.60% |
| 6 | 신용 방향 | 🟠 긴축 | 0.7336 | HYG/LQD=0.7336 (Ratio, OAS 아님), 4W Δ=-0.0052 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 128.74
- **상세**: KOSPI YoY=+219.91%, KOSDAQ YoY=+37.56%, KOSPI 4W=+17.94%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.281169
- **상세**: RSP/SPY=0.2812 (Ratio, 무차원), 4W Δ=+0.0062, 4W 상승=breadth 개선
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — 강한 risk-on
- **값**: 2.12122
- **상세**: SPHB/SPLV=2.1212 (Ratio, 무차원), 4W Δ=+0.2497
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.8385
- **상세**: VIX3M=19.57, VIX/VIX3M=0.8385 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-1.79
- **시리즈**: ^VIX3M, VIXCLS

### 🟢 섹터 로테이션 — 확장
- **값**: 18.15
- **상세**: XLK 4W=+8.07%, XLE 4W=-10.08%, XLK-XLE=+18.15%p, XLP 4W=-2.60%
- **시리즈**: XLK, XLE, XLP

### 🟠 신용 방향 — 긴축
- **값**: 0.733566
- **상세**: HYG/LQD=0.7336 (Ratio, OAS 아님), 4W Δ=-0.0052
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*