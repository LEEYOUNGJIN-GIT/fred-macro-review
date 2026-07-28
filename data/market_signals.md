# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-07-28 (oldest: 2026-07-27 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-07-28 21:57:18 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 54.2000 | KOSPI YoY=+112.73%, KOSDAQ YoY=-4.32%, KOSPI 4W=-24.35% |
| 2 | Breadth | 🔵 중립 | 0.2938 | RSP/SPY=0.2938 (Ratio, 무차원), 4W Δ=+0.0063, 4W 상승=breadth 개선 |
| 3 | Risk-on/off | 🟢 risk-on | 1.7830 | SPHB/SPLV=1.7830 (Ratio, 무차원), 4W Δ=-0.2071 |
| 4 | VIX Term | 🟢 contango | 0.9355 | VIX3M=19.86, VIX/VIX3M=0.9355 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.29 |
| 5 | 섹터 로테이션 | 🟠 경계 | -15.1700 | XLK 4W=-7.72%, XLE 4W=+7.45%, XLK-XLE=-15.17%p, XLP 4W=+2.77%, 방어(XLP) > 기술 → risk-off 로테이션 |
| 6 | 신용 방향 | 🟢 완화 | 0.7434 | HYG/LQD=0.7434 (Ratio, OAS 아님), 4W Δ=+0.0152 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 54.2
- **상세**: KOSPI YoY=+112.73%, KOSDAQ YoY=-4.32%, KOSPI 4W=-24.35%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.293834
- **상세**: RSP/SPY=0.2938 (Ratio, 무차원), 4W Δ=+0.0063, 4W 상승=breadth 개선
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.782993
- **상세**: SPHB/SPLV=1.7830 (Ratio, 무차원), 4W Δ=-0.2071
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.9355
- **상세**: VIX3M=19.86, VIX/VIX3M=0.9355 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.29
- **시리즈**: ^VIX3M, VIXCLS

### 🟠 섹터 로테이션 — 경계
- **값**: -15.17
- **상세**: XLK 4W=-7.72%, XLE 4W=+7.45%, XLK-XLE=-15.17%p, XLP 4W=+2.77%, 방어(XLP) > 기술 → risk-off 로테이션
- **시리즈**: XLK, XLE, XLP

### 🟢 신용 방향 — 완화
- **값**: 0.743424
- **상세**: HYG/LQD=0.7434 (Ratio, OAS 아님), 4W Δ=+0.0152
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*