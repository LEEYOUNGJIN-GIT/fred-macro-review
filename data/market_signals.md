# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-05-28 (oldest: 2026-05-27 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-05-28 22:29:15 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 132.4700 | KOSPI YoY=+211.63%, KOSDAQ YoY=+53.32%, KOSPI 4W=+27.07% |
| 2 | Breadth | 🔵 중립 | 0.2760 | RSP/SPY=0.2760 (Ratio, 무차원), 4W Δ=-0.0057, 4W 하락=대형주 쏠림 |
| 3 | Risk-on/off | 🟢 강한 risk-on | 2.0284 | SPHB/SPLV=2.0284 (Ratio, 무차원), 4W Δ=+0.2435 |
| 4 | VIX Term | 🟢 contango | 0.8901 | VIX3M=19.11, VIX/VIX3M=0.8901 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-2.08 |
| 5 | 섹터 로테이션 | 🟢 확장 | 20.9500 | XLK 4W=+17.43%, XLE 4W=-3.52%, XLK-XLE=+20.95%p, XLP 4W=+1.82% |
| 6 | 신용 방향 | 🔵 중립 | 0.7343 | HYG/LQD=0.7343 (Ratio, OAS 아님), 4W Δ=-0.0017 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 132.47
- **상세**: KOSPI YoY=+211.63%, KOSDAQ YoY=+53.32%, KOSPI 4W=+27.07%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.275974
- **상세**: RSP/SPY=0.2760 (Ratio, 무차원), 4W Δ=-0.0057, 4W 하락=대형주 쏠림
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — 강한 risk-on
- **값**: 2.028387
- **상세**: SPHB/SPLV=2.0284 (Ratio, 무차원), 4W Δ=+0.2435
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.8901
- **상세**: VIX3M=19.11, VIX/VIX3M=0.8901 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-2.08
- **시리즈**: ^VIX3M, VIXCLS

### 🟢 섹터 로테이션 — 확장
- **값**: 20.95
- **상세**: XLK 4W=+17.43%, XLE 4W=-3.52%, XLK-XLE=+20.95%p, XLP 4W=+1.82%
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.734304
- **상세**: HYG/LQD=0.7343 (Ratio, OAS 아님), 4W Δ=-0.0017
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*