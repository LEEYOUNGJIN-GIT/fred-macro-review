# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-06-22 (oldest: 2026-06-18 ^HSI)
> Freshness: OK (oldest 4d ≤ 5d)
> Generated: 2026-06-22 22:43:34 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 121.7300 | KOSPI YoY=+216.99%, KOSDAQ YoY=+26.48%, KOSPI 4W=+25.57% |
| 2 | Breadth | 🔵 중립 | 0.2816 | RSP/SPY=0.2816 (Ratio, 무차원), 4W Δ=+0.0053, 4W 상승=breadth 개선 |
| 3 | Risk-on/off | 🟢 강한 risk-on | 2.1404 | SPHB/SPLV=2.1404 (Ratio, 무차원), 4W Δ=+0.2405 |
| 4 | VIX Term | 🟢 contango | 0.9332 | VIX3M=19.76, VIX/VIX3M=0.9332 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.24 |
| 5 | 섹터 로테이션 | 🟢 확장 | 16.1600 | XLK 4W=+7.59%, XLE 4W=-8.57%, XLK-XLE=+16.16%p, XLP 4W=-2.93% |
| 6 | 신용 방향 | 🔵 중립 | 0.7349 | HYG/LQD=0.7349 (Ratio, OAS 아님), 4W Δ=-0.0028 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 121.73
- **상세**: KOSPI YoY=+216.99%, KOSDAQ YoY=+26.48%, KOSPI 4W=+25.57%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.281586
- **상세**: RSP/SPY=0.2816 (Ratio, 무차원), 4W Δ=+0.0053, 4W 상승=breadth 개선
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — 강한 risk-on
- **값**: 2.14036
- **상세**: SPHB/SPLV=2.1404 (Ratio, 무차원), 4W Δ=+0.2405
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.9332
- **상세**: VIX3M=19.76, VIX/VIX3M=0.9332 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.24
- **시리즈**: ^VIX3M, VIXCLS

### 🟢 섹터 로테이션 — 확장
- **값**: 16.16
- **상세**: XLK 4W=+7.59%, XLE 4W=-8.57%, XLK-XLE=+16.16%p, XLP 4W=-2.93%
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.734878
- **상세**: HYG/LQD=0.7349 (Ratio, OAS 아님), 4W Δ=-0.0028
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*