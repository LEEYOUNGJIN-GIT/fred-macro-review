# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-09-03 (oldest: 2026-09-02 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-09-03 22:55:19 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 56.5300 | KOSPI YoY=+109.67%, KOSDAQ YoY=+3.39%, KOSPI 4W=+3.20% |
| 2 | Breadth | 🔵 중립 | 0.2846 | RSP/SPY=0.2846 (Ratio, 무차원), 4W Δ=+0.0002 |
| 3 | Risk-on/off | 🟢 risk-on | 1.9438 | SPHB/SPLV=1.9438 (Ratio, 무차원), 4W Δ=+0.0310 |
| 4 | VIX Term | 🟢 contango | 0.9380 | VIX3M=17.42, VIX/VIX3M=0.9380 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-2.15 |
| 5 | 섹터 로테이션 | 🟠 경계 | -10.7600 | XLK 4W=+0.35%, XLE 4W=+11.11%, XLK-XLE=-10.76%p, XLP 4W=+0.18% |
| 6 | 신용 방향 | 🔵 중립 | 0.7508 | HYG/LQD=0.7508 (Ratio, OAS 아님), 4W Δ=+0.0047 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 56.53
- **상세**: KOSPI YoY=+109.67%, KOSDAQ YoY=+3.39%, KOSPI 4W=+3.20%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.284608
- **상세**: RSP/SPY=0.2846 (Ratio, 무차원), 4W Δ=+0.0002
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.94378
- **상세**: SPHB/SPLV=1.9438 (Ratio, 무차원), 4W Δ=+0.0310
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.938
- **상세**: VIX3M=17.42, VIX/VIX3M=0.9380 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-2.15
- **시리즈**: ^VIX3M, VIXCLS

### 🟠 섹터 로테이션 — 경계
- **값**: -10.76
- **상세**: XLK 4W=+0.35%, XLE 4W=+11.11%, XLK-XLE=-10.76%p, XLP 4W=+0.18%
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.750806
- **상세**: HYG/LQD=0.7508 (Ratio, OAS 아님), 4W Δ=+0.0047
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*