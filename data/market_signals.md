# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-06-26 (oldest: 2026-06-25 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-06-26 22:06:43 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 111.9900 | KOSPI YoY=+208.51%, KOSDAQ YoY=+15.47%, KOSPI 4W=+8.53% |
| 2 | Breadth | 🔵 중립 | 0.2885 | RSP/SPY=0.2885 (Ratio, 무차원), 4W Δ=+0.0129, 4W 상승=breadth 개선 |
| 3 | Risk-on/off | 🟢 risk-on | 1.9864 | SPHB/SPLV=1.9864 (Ratio, 무차원), 4W Δ=-0.0433 |
| 4 | VIX Term | 🟢 contango | 0.9255 | VIX3M=20.13, VIX/VIX3M=0.9255 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.13 |
| 5 | 섹터 로테이션 | 🔵 중립 | 1.8200 | XLK 4W=-2.96%, XLE 4W=-4.78%, XLK-XLE=+1.82%p, XLP 4W=+1.03%, 방어(XLP) > 기술 → risk-off 로테이션 |
| 6 | 신용 방향 | 🔵 중립 | 0.7290 | HYG/LQD=0.7290 (Ratio, OAS 아님), 4W Δ=-0.0043 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 111.99
- **상세**: KOSPI YoY=+208.51%, KOSDAQ YoY=+15.47%, KOSPI 4W=+8.53%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.288495
- **상세**: RSP/SPY=0.2885 (Ratio, 무차원), 4W Δ=+0.0129, 4W 상승=breadth 개선
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.986404
- **상세**: SPHB/SPLV=1.9864 (Ratio, 무차원), 4W Δ=-0.0433
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.9255
- **상세**: VIX3M=20.13, VIX/VIX3M=0.9255 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.13
- **시리즈**: ^VIX3M, VIXCLS

### 🔵 섹터 로테이션 — 중립
- **값**: 1.82
- **상세**: XLK 4W=-2.96%, XLE 4W=-4.78%, XLK-XLE=+1.82%p, XLP 4W=+1.03%, 방어(XLP) > 기술 → risk-off 로테이션
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.729041
- **상세**: HYG/LQD=0.7290 (Ratio, OAS 아님), 4W Δ=-0.0043
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*