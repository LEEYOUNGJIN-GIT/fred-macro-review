# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-06-09 (oldest: 2026-06-08 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-06-09 22:19:04 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 108.0200 | KOSPI YoY=+188.74%, KOSDAQ YoY=+27.29%, KOSPI 4W=-0.08% |
| 2 | Breadth | 🔵 중립 | 0.2838 | RSP/SPY=0.2838 (Ratio, 무차원), 4W Δ=+0.0079, 4W 상승=breadth 개선 |
| 3 | Risk-on/off | 🟢 risk-on | 1.9680 | SPHB/SPLV=1.9680 (Ratio, 무차원), 4W Δ=+0.0057 |
| 4 | VIX Term | 🔵 중립 | 1.0094 | VIX3M=21.31, VIX/VIX3M=1.0094 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.07 |
| 5 | 섹터 로테이션 | 🔵 중립 | 1.2400 | XLK 4W=+1.62%, XLE 4W=+0.38%, XLK-XLE=+1.24%p, XLP 4W=+0.88% |
| 6 | 신용 방향 | 🔵 중립 | 0.7344 | HYG/LQD=0.7344 (Ratio, OAS 아님), 4W Δ=+0.0012 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 108.02
- **상세**: KOSPI YoY=+188.74%, KOSDAQ YoY=+27.29%, KOSPI 4W=-0.08%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.283821
- **상세**: RSP/SPY=0.2838 (Ratio, 무차원), 4W Δ=+0.0079, 4W 상승=breadth 개선
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.967952
- **상세**: SPHB/SPLV=1.9680 (Ratio, 무차원), 4W Δ=+0.0057
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🔵 VIX Term — 중립
- **값**: 1.0094
- **상세**: VIX3M=21.31, VIX/VIX3M=1.0094 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.07
- **시리즈**: ^VIX3M, VIXCLS

### 🔵 섹터 로테이션 — 중립
- **값**: 1.24
- **상세**: XLK 4W=+1.62%, XLE 4W=+0.38%, XLK-XLE=+1.24%p, XLP 4W=+0.88%
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.734434
- **상세**: HYG/LQD=0.7344 (Ratio, OAS 아님), 4W Δ=+0.0012
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*