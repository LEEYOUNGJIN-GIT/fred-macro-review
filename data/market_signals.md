# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-09-10 (oldest: 2026-09-09 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-09-10 22:52:53 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 62.4100 | KOSPI YoY=+121.25%, KOSDAQ YoY=+3.57%, KOSPI 4W=+11.13% |
| 2 | Breadth | 🔵 중립 | 0.2813 | RSP/SPY=0.2813 (Ratio, 무차원), 4W Δ=-0.0049 |
| 3 | Risk-on/off | 🟢 risk-on | 1.9700 | SPHB/SPLV=1.9700 (Ratio, 무차원), 4W Δ=-0.0122 |
| 4 | VIX Term | 🟢 contango | 0.7968 | VIX3M=19.73, VIX/VIX3M=0.7968 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.16 |
| 5 | 섹터 로테이션 | 🟠 경계 | -8.3200 | XLK 4W=-1.93%, XLE 4W=+6.39%, XLK-XLE=-8.32%p, XLP 4W=-2.34% |
| 6 | 신용 방향 | 🔵 중립 | 0.7534 | HYG/LQD=0.7534 (Ratio, OAS 아님), 4W Δ=+0.0041 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 62.41
- **상세**: KOSPI YoY=+121.25%, KOSDAQ YoY=+3.57%, KOSPI 4W=+11.13%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.28129
- **상세**: RSP/SPY=0.2813 (Ratio, 무차원), 4W Δ=-0.0049
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.970001
- **상세**: SPHB/SPLV=1.9700 (Ratio, 무차원), 4W Δ=-0.0122
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.7968
- **상세**: VIX3M=19.73, VIX/VIX3M=0.7968 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.16
- **시리즈**: ^VIX3M, VIXCLS

### 🟠 섹터 로테이션 — 경계
- **값**: -8.32
- **상세**: XLK 4W=-1.93%, XLE 4W=+6.39%, XLK-XLE=-8.32%p, XLP 4W=-2.34%
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.753354
- **상세**: HYG/LQD=0.7534 (Ratio, OAS 아님), 4W Δ=+0.0041
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*