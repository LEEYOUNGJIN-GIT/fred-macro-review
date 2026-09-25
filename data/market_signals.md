# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-09-25 (oldest: 2026-09-23 ^KS11)
> Freshness: OK (oldest 2d ≤ 5d)
> Generated: 2026-09-25 23:44:37 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 57.5000 | KOSPI YoY=+113.63%, KOSDAQ YoY=+1.38%, KOSPI 4W=+4.01% |
| 2 | Breadth | 🔵 중립 | 0.2737 | RSP/SPY=0.2737 (Ratio, 무차원), 4W Δ=-0.0131, 4W 하락=대형주 쏠림 |
| 3 | Risk-on/off | 🟢 강한 risk-on | 2.1473 | SPHB/SPLV=2.1473 (Ratio, 무차원), 4W Δ=+0.1546 |
| 4 | VIX Term | 🟢 contango | 0.7925 | VIX3M=17.93, VIX/VIX3M=0.7925 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.37 |
| 5 | 섹터 로테이션 | 🟢 확장 | 3.9900 | XLK 4W=+4.18%, XLE 4W=+0.19%, XLK-XLE=+3.99%p, XLP 4W=-2.92% |
| 6 | 신용 방향 | 🟢 완화 | 0.7544 | HYG/LQD=0.7544 (Ratio, OAS 아님), 4W Δ=+0.0070 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 57.5
- **상세**: KOSPI YoY=+113.63%, KOSDAQ YoY=+1.38%, KOSPI 4W=+4.01%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.273689
- **상세**: RSP/SPY=0.2737 (Ratio, 무차원), 4W Δ=-0.0131, 4W 하락=대형주 쏠림
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — 강한 risk-on
- **값**: 2.147265
- **상세**: SPHB/SPLV=2.1473 (Ratio, 무차원), 4W Δ=+0.1546
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.7925
- **상세**: VIX3M=17.93, VIX/VIX3M=0.7925 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.37
- **시리즈**: ^VIX3M, VIXCLS

### 🟢 섹터 로테이션 — 확장
- **값**: 3.99
- **상세**: XLK 4W=+4.18%, XLE 4W=+0.19%, XLK-XLE=+3.99%p, XLP 4W=-2.92%
- **시리즈**: XLK, XLE, XLP

### 🟢 신용 방향 — 완화
- **값**: 0.754384
- **상세**: HYG/LQD=0.7544 (Ratio, OAS 아님), 4W Δ=+0.0070
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*