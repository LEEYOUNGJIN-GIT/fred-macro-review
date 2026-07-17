# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-07-17 (oldest: 2026-07-16 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-07-17 21:44:21 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 62.6900 | KOSPI YoY=+123.31%, KOSDAQ YoY=+2.07%, KOSPI 4W=-24.75% |
| 2 | Breadth | 🔵 중립 | 0.2871 | RSP/SPY=0.2871 (Ratio, 무차원), 4W Δ=+0.0054, 4W 상승=breadth 개선 |
| 3 | Risk-on/off | 🟢 risk-on | 1.8407 | SPHB/SPLV=1.8407 (Ratio, 무차원), 4W Δ=-0.2188 |
| 4 | VIX Term | 🟢 contango | 0.7629 | VIX3M=20.54, VIX/VIX3M=0.7629 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.88 |
| 5 | 섹터 로테이션 | 🟠 경계 | -11.6500 | XLK 4W=-5.38%, XLE 4W=+6.27%, XLK-XLE=-11.65%p, XLP 4W=+2.51%, 방어(XLP) > 기술 → risk-off 로테이션 |
| 6 | 신용 방향 | 🟢 완화 | 0.7405 | HYG/LQD=0.7405 (Ratio, OAS 아님), 4W Δ=+0.0083 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 62.69
- **상세**: KOSPI YoY=+123.31%, KOSDAQ YoY=+2.07%, KOSPI 4W=-24.75%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.287062
- **상세**: RSP/SPY=0.2871 (Ratio, 무차원), 4W Δ=+0.0054, 4W 상승=breadth 개선
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.840669
- **상세**: SPHB/SPLV=1.8407 (Ratio, 무차원), 4W Δ=-0.2188
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.7629
- **상세**: VIX3M=20.54, VIX/VIX3M=0.7629 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.88
- **시리즈**: ^VIX3M, VIXCLS

### 🟠 섹터 로테이션 — 경계
- **값**: -11.65
- **상세**: XLK 4W=-5.38%, XLE 4W=+6.27%, XLK-XLE=-11.65%p, XLP 4W=+2.51%, 방어(XLP) > 기술 → risk-off 로테이션
- **시리즈**: XLK, XLE, XLP

### 🟢 신용 방향 — 완화
- **값**: 0.740517
- **상세**: HYG/LQD=0.7405 (Ratio, OAS 아님), 4W Δ=+0.0083
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*