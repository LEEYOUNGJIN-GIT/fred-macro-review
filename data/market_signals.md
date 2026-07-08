# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-07-09 (oldest: 2026-07-07 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-07-08 22:00:34 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 75.2300 | KOSPI YoY=+146.32%, KOSDAQ YoY=+4.14%, KOSPI 4W=-5.44% |
| 2 | Breadth | 🔵 중립 | 0.2847 | RSP/SPY=0.2847 (Ratio, 무차원), 4W Δ=+0.0042 |
| 3 | Risk-on/off | 🟢 risk-on | 1.9185 | SPHB/SPLV=1.9185 (Ratio, 무차원), 4W Δ=-0.0958 |
| 4 | VIX Term | 🟢 contango | 0.8001 | VIX3M=19.46, VIX/VIX3M=0.8001 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.23 |
| 5 | 섹터 로테이션 | 🔵 중립 | 2.6000 | XLK 4W=-1.39%, XLE 4W=-3.99%, XLK-XLE=+2.60%p, XLP 4W=+2.29%, 방어(XLP) > 기술 → risk-off 로테이션 |
| 6 | 신용 방향 | 🔵 중립 | 0.7399 | HYG/LQD=0.7399 (Ratio, OAS 아님), 4W Δ=+0.0046 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 75.23
- **상세**: KOSPI YoY=+146.32%, KOSDAQ YoY=+4.14%, KOSPI 4W=-5.44%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.284679
- **상세**: RSP/SPY=0.2847 (Ratio, 무차원), 4W Δ=+0.0042
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.918534
- **상세**: SPHB/SPLV=1.9185 (Ratio, 무차원), 4W Δ=-0.0958
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.8001
- **상세**: VIX3M=19.46, VIX/VIX3M=0.8001 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.23
- **시리즈**: ^VIX3M, VIXCLS

### 🔵 섹터 로테이션 — 중립
- **값**: 2.6
- **상세**: XLK 4W=-1.39%, XLE 4W=-3.99%, XLK-XLE=+2.60%p, XLP 4W=+2.29%, 방어(XLP) > 기술 → risk-off 로테이션
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.739853
- **상세**: HYG/LQD=0.7399 (Ratio, OAS 아님), 4W Δ=+0.0046
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*