# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-07-09 (oldest: 2026-07-08 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-07-09 22:16:21 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 67.4700 | KOSPI YoY=+135.32%, KOSDAQ YoY=-0.37%, KOSPI 4W=-6.26% |
| 2 | Breadth | 🔵 중립 | 0.2840 | RSP/SPY=0.2840 (Ratio, 무차원), 4W Δ=+0.0006 |
| 3 | Risk-on/off | 🟢 risk-on | 1.9819 | SPHB/SPLV=1.9819 (Ratio, 무차원), 4W Δ=+0.0126 |
| 4 | VIX Term | 🟢 contango | 0.8494 | VIX3M=18.99, VIX/VIX3M=0.8494 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.24 |
| 5 | 섹터 로테이션 | 🟢 확장 | 6.4500 | XLK 4W=+2.66%, XLE 4W=-3.79%, XLK-XLE=+6.45%p, XLP 4W=-0.38% |
| 6 | 신용 방향 | 🟢 완화 | 0.7404 | HYG/LQD=0.7404 (Ratio, OAS 아님), 4W Δ=+0.0068 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 67.47
- **상세**: KOSPI YoY=+135.32%, KOSDAQ YoY=-0.37%, KOSPI 4W=-6.26%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.284019
- **상세**: RSP/SPY=0.2840 (Ratio, 무차원), 4W Δ=+0.0006
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.981854
- **상세**: SPHB/SPLV=1.9819 (Ratio, 무차원), 4W Δ=+0.0126
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.8494
- **상세**: VIX3M=18.99, VIX/VIX3M=0.8494 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.24
- **시리즈**: ^VIX3M, VIXCLS

### 🟢 섹터 로테이션 — 확장
- **값**: 6.45
- **상세**: XLK 4W=+2.66%, XLE 4W=-3.79%, XLK-XLE=+6.45%p, XLP 4W=-0.38%
- **시리즈**: XLK, XLE, XLP

### 🟢 신용 방향 — 완화
- **값**: 0.740414
- **상세**: HYG/LQD=0.7404 (Ratio, OAS 아님), 4W Δ=+0.0068
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*