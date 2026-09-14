# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-09-15 (oldest: 2026-09-11 ^KS11)
> Freshness: OK (oldest 3d ≤ 5d)
> Generated: 2026-09-14 23:38:57 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 59.9300 | KOSPI YoY=+116.88%, KOSDAQ YoY=+2.98%, KOSPI 4W=+1.42% |
| 2 | Breadth | 🔵 중립 | 0.2826 | RSP/SPY=0.2826 (Ratio, 무차원), 4W Δ=-0.0044 |
| 3 | Risk-on/off | 🟢 risk-on | 1.9376 | SPHB/SPLV=1.9376 (Ratio, 무차원), 4W Δ=-0.0514 |
| 4 | VIX Term | 🟢 contango | 0.9253 | VIX3M=19.28, VIX/VIX3M=0.9253 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.29 |
| 5 | 섹터 로테이션 | 🟠 경계 | -7.2500 | XLK 4W=-3.02%, XLE 4W=+4.23%, XLK-XLE=-7.25%p, XLP 4W=-1.94%, 방어(XLP) > 기술 → risk-off 로테이션 |
| 6 | 신용 방향 | 🔵 중립 | 0.7529 | HYG/LQD=0.7529 (Ratio, OAS 아님), 4W Δ=+0.0028 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 59.93
- **상세**: KOSPI YoY=+116.88%, KOSDAQ YoY=+2.98%, KOSPI 4W=+1.42%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.282581
- **상세**: RSP/SPY=0.2826 (Ratio, 무차원), 4W Δ=-0.0044
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.937551
- **상세**: SPHB/SPLV=1.9376 (Ratio, 무차원), 4W Δ=-0.0514
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.9253
- **상세**: VIX3M=19.28, VIX/VIX3M=0.9253 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.29
- **시리즈**: ^VIX3M, VIXCLS

### 🟠 섹터 로테이션 — 경계
- **값**: -7.25
- **상세**: XLK 4W=-3.02%, XLE 4W=+4.23%, XLK-XLE=-7.25%p, XLP 4W=-1.94%, 방어(XLP) > 기술 → risk-off 로테이션
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.752924
- **상세**: HYG/LQD=0.7529 (Ratio, OAS 아님), 4W Δ=+0.0028
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*