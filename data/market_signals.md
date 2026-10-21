# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-10-22 (oldest: 2026-10-20 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-10-21 23:51:24 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 26.5900 | KOSPI YoY=+60.68%, KOSDAQ YoY=-7.50%, KOSPI 4W=-17.34% |
| 2 | Breadth | 🔵 중립 | 0.2802 | RSP/SPY=0.2802 (Ratio, 무차원), 4W Δ=+0.0050 |
| 3 | Risk-on/off | 🟢 risk-on | 1.9317 | SPHB/SPLV=1.9317 (Ratio, 무차원), 4W Δ=-0.1992 |
| 4 | VIX Term | 🔵 중립 | 0.9850 | VIX3M=18.72, VIX/VIX3M=0.9850 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.61 |
| 5 | 섹터 로테이션 | 🟠 경계 | -12.7600 | XLK 4W=-3.48%, XLE 4W=+9.28%, XLK-XLE=-12.76%p, XLP 4W=+5.68%, 방어(XLP) > 기술 → risk-off 로테이션 |
| 6 | 신용 방향 | 🟠 긴축 | 0.7459 | HYG/LQD=0.7459 (Ratio, OAS 아님), 4W Δ=-0.0058 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 26.59
- **상세**: KOSPI YoY=+60.68%, KOSDAQ YoY=-7.50%, KOSPI 4W=-17.34%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.280226
- **상세**: RSP/SPY=0.2802 (Ratio, 무차원), 4W Δ=+0.0050
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.931715
- **상세**: SPHB/SPLV=1.9317 (Ratio, 무차원), 4W Δ=-0.1992
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🔵 VIX Term — 중립
- **값**: 0.985
- **상세**: VIX3M=18.72, VIX/VIX3M=0.9850 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.61
- **시리즈**: ^VIX3M, VIXCLS

### 🟠 섹터 로테이션 — 경계
- **값**: -12.76
- **상세**: XLK 4W=-3.48%, XLE 4W=+9.28%, XLK-XLE=-12.76%p, XLP 4W=+5.68%, 방어(XLP) > 기술 → risk-off 로테이션
- **시리즈**: XLK, XLE, XLP

### 🟠 신용 방향 — 긴축
- **값**: 0.745858
- **상세**: HYG/LQD=0.7459 (Ratio, OAS 아님), 4W Δ=-0.0058
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*