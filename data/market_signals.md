# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-10-16 (oldest: 2026-10-15 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-10-16 23:11:34 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 27.5700 | KOSPI YoY=+64.03%, KOSDAQ YoY=-8.90%, KOSPI 4W=-19.62% |
| 2 | Breadth | 🔵 중립 | 0.2805 | RSP/SPY=0.2805 (Ratio, 무차원), 4W Δ=+0.0028 |
| 3 | Risk-on/off | 🟢 risk-on | 1.8703 | SPHB/SPLV=1.8703 (Ratio, 무차원), 4W Δ=-0.1636 |
| 4 | VIX Term | 🟢 contango | 0.8229 | VIX3M=20.50, VIX/VIX3M=0.8229 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+2.26 |
| 5 | 섹터 로테이션 | 🟠 경계 | -9.8600 | XLK 4W=-3.12%, XLE 4W=+6.74%, XLK-XLE=-9.86%p, XLP 4W=+6.52%, 방어(XLP) > 기술 → risk-off 로테이션 |
| 6 | 신용 방향 | 🟠 긴축 | 0.7433 | HYG/LQD=0.7433 (Ratio, OAS 아님), 4W Δ=-0.0066 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 27.57
- **상세**: KOSPI YoY=+64.03%, KOSDAQ YoY=-8.90%, KOSPI 4W=-19.62%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.280498
- **상세**: RSP/SPY=0.2805 (Ratio, 무차원), 4W Δ=+0.0028
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.870301
- **상세**: SPHB/SPLV=1.8703 (Ratio, 무차원), 4W Δ=-0.1636
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.8229
- **상세**: VIX3M=20.50, VIX/VIX3M=0.8229 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+2.26
- **시리즈**: ^VIX3M, VIXCLS

### 🟠 섹터 로테이션 — 경계
- **값**: -9.86
- **상세**: XLK 4W=-3.12%, XLE 4W=+6.74%, XLK-XLE=-9.86%p, XLP 4W=+6.52%, 방어(XLP) > 기술 → risk-off 로테이션
- **시리즈**: XLK, XLE, XLP

### 🟠 신용 방향 — 긴축
- **값**: 0.743327
- **상세**: HYG/LQD=0.7433 (Ratio, OAS 아님), 4W Δ=-0.0066
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*