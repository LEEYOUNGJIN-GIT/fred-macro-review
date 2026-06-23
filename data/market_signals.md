# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-06-23 (oldest: 2026-06-22 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-06-23 22:08:52 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 121.4700 | KOSPI YoY=+217.38%, KOSDAQ YoY=+25.57%, KOSPI 4W=+16.62% |
| 2 | Breadth | 🔵 중립 | 0.2848 | RSP/SPY=0.2848 (Ratio, 무차원), 4W Δ=+0.0081, 4W 상승=breadth 개선 |
| 3 | Risk-on/off | 🟢 강한 risk-on | 2.0275 | SPHB/SPLV=2.0275 (Ratio, 무차원), 4W Δ=+0.1099 |
| 4 | VIX Term | 🟢 contango | 0.7968 | VIX3M=21.06, VIX/VIX3M=0.7968 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+1.06 |
| 5 | 섹터 로테이션 | 🟢 확장 | 10.0200 | XLK 4W=+2.23%, XLE 4W=-7.79%, XLK-XLE=+10.02%p, XLP 4W=-0.59% |
| 6 | 신용 방향 | 🔵 중립 | 0.7334 | HYG/LQD=0.7334 (Ratio, OAS 아님), 4W Δ=-0.0030 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 121.47
- **상세**: KOSPI YoY=+217.38%, KOSDAQ YoY=+25.57%, KOSPI 4W=+16.62%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.284754
- **상세**: RSP/SPY=0.2848 (Ratio, 무차원), 4W Δ=+0.0081, 4W 상승=breadth 개선
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — 강한 risk-on
- **값**: 2.02749
- **상세**: SPHB/SPLV=2.0275 (Ratio, 무차원), 4W Δ=+0.1099
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.7968
- **상세**: VIX3M=21.06, VIX/VIX3M=0.7968 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+1.06
- **시리즈**: ^VIX3M, VIXCLS

### 🟢 섹터 로테이션 — 확장
- **값**: 10.02
- **상세**: XLK 4W=+2.23%, XLE 4W=-7.79%, XLK-XLE=+10.02%p, XLP 4W=-0.59%
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.733358
- **상세**: HYG/LQD=0.7334 (Ratio, OAS 아님), 4W Δ=-0.0030
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*