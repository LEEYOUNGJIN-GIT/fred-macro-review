# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-06-12 (oldest: 2026-06-11 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-06-12 22:20:27 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 113.7800 | KOSPI YoY=+190.77%, KOSDAQ YoY=+36.79%, KOSPI 4W=+1.58% |
| 2 | Breadth | 🔵 중립 | 0.2853 | RSP/SPY=0.2853 (Ratio, 무차원), 4W Δ=+0.0131, 4W 상승=breadth 개선 |
| 3 | Risk-on/off | 🟢 risk-on | 1.9972 | SPHB/SPLV=1.9972 (Ratio, 무차원), 4W Δ=+0.0576 |
| 4 | VIX Term | 🟡 backwardation | 1.0834 | VIX3M=20.51, VIX/VIX3M=1.0834 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.34 |
| 5 | 섹터 로테이션 | 🟢 확장 | 3.8500 | XLK 4W=+2.95%, XLE 4W=-0.90%, XLK-XLE=+3.85%p, XLP 4W=+0.99% |
| 6 | 신용 방향 | 🔵 중립 | 0.7333 | HYG/LQD=0.7333 (Ratio, OAS 아님), 4W Δ=-0.0013 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 113.78
- **상세**: KOSPI YoY=+190.77%, KOSDAQ YoY=+36.79%, KOSPI 4W=+1.58%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.285339
- **상세**: RSP/SPY=0.2853 (Ratio, 무차원), 4W Δ=+0.0131, 4W 상승=breadth 개선
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.99718
- **상세**: SPHB/SPLV=1.9972 (Ratio, 무차원), 4W Δ=+0.0576
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟡 VIX Term — backwardation
- **값**: 1.0834
- **상세**: VIX3M=20.51, VIX/VIX3M=1.0834 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.34
- **시리즈**: ^VIX3M, VIXCLS

### 🟢 섹터 로테이션 — 확장
- **값**: 3.85
- **상세**: XLK 4W=+2.95%, XLE 4W=-0.90%, XLK-XLE=+3.85%p, XLP 4W=+0.99%
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.733327
- **상세**: HYG/LQD=0.7333 (Ratio, OAS 아님), 4W Δ=-0.0013
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*