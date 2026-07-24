# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-07-24 (oldest: 2026-07-23 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-07-24 21:59:08 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 61.0100 | KOSPI YoY=+122.95%, KOSDAQ YoY=-0.93%, KOSPI 4W=-16.22% |
| 2 | Breadth | 🔵 중립 | 0.2890 | RSP/SPY=0.2890 (Ratio, 무차원), 4W Δ=+0.0007 |
| 3 | Risk-on/off | 🟢 risk-on | 1.8286 | SPHB/SPLV=1.8286 (Ratio, 무차원), 4W Δ=-0.2359 |
| 4 | VIX Term | 🟢 contango | 0.8113 | VIX3M=20.51, VIX/VIX3M=0.8113 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.94 |
| 5 | 섹터 로테이션 | 🟠 경계 | -14.9300 | XLK 4W=-4.71%, XLE 4W=+10.22%, XLK-XLE=-14.93%p, XLP 4W=+0.23%, 방어(XLP) > 기술 → risk-off 로테이션 |
| 6 | 신용 방향 | 🟢 완화 | 0.7458 | HYG/LQD=0.7458 (Ratio, OAS 아님), 4W Δ=+0.0172 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 61.01
- **상세**: KOSPI YoY=+122.95%, KOSDAQ YoY=-0.93%, KOSPI 4W=-16.22%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.289026
- **상세**: RSP/SPY=0.2890 (Ratio, 무차원), 4W Δ=+0.0007
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.828605
- **상세**: SPHB/SPLV=1.8286 (Ratio, 무차원), 4W Δ=-0.2359
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.8113
- **상세**: VIX3M=20.51, VIX/VIX3M=0.8113 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.94
- **시리즈**: ^VIX3M, VIXCLS

### 🟠 섹터 로테이션 — 경계
- **값**: -14.93
- **상세**: XLK 4W=-4.71%, XLE 4W=+10.22%, XLK-XLE=-14.93%p, XLP 4W=+0.23%, 방어(XLP) > 기술 → risk-off 로테이션
- **시리즈**: XLK, XLE, XLP

### 🟢 신용 방향 — 완화
- **값**: 0.745835
- **상세**: HYG/LQD=0.7458 (Ratio, OAS 아님), 4W Δ=+0.0172
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*