# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-06-08 (oldest: 2026-06-05 ^KS11)
> Freshness: OK (oldest 3d ≤ 5d)
> Generated: 2026-06-08 22:21:38 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 127.1600 | KOSPI YoY=+214.63%, KOSDAQ YoY=+39.68%, KOSPI 4W=+10.51% |
| 2 | Breadth | 🔵 중립 | 0.2808 | RSP/SPY=0.2808 (Ratio, 무차원), 4W Δ=+0.0041 |
| 3 | Risk-on/off | 🟢 강한 risk-on | 2.0130 | SPHB/SPLV=2.0130 (Ratio, 무차원), 4W Δ=+0.0587 |
| 4 | VIX Term | 🟢 contango | 0.7407 | VIX3M=20.79, VIX/VIX3M=0.7407 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.29 |
| 5 | 섹터 로테이션 | 🔵 중립 | 0.2100 | XLK 4W=+4.93%, XLE 4W=+4.72%, XLK-XLE=+0.21%p, XLP 4W=-1.32% |
| 6 | 신용 방향 | 🔵 중립 | 0.7361 | HYG/LQD=0.7361 (Ratio, OAS 아님), 4W Δ=+0.0032 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 127.16
- **상세**: KOSPI YoY=+214.63%, KOSDAQ YoY=+39.68%, KOSPI 4W=+10.51%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.28085
- **상세**: RSP/SPY=0.2808 (Ratio, 무차원), 4W Δ=+0.0041
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — 강한 risk-on
- **값**: 2.012971
- **상세**: SPHB/SPLV=2.0130 (Ratio, 무차원), 4W Δ=+0.0587
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.7407
- **상세**: VIX3M=20.79, VIX/VIX3M=0.7407 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.29
- **시리즈**: ^VIX3M, VIXCLS

### 🔵 섹터 로테이션 — 중립
- **값**: 0.21
- **상세**: XLK 4W=+4.93%, XLE 4W=+4.72%, XLK-XLE=+0.21%p, XLP 4W=-1.32%
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.736073
- **상세**: HYG/LQD=0.7361 (Ratio, OAS 아님), 4W Δ=+0.0032
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*