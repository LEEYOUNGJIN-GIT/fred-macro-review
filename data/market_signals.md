# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-11-19 (oldest: 2026-11-17 RSP)
> Freshness: OK (oldest 2d ≤ 5d)
> Generated: 2026-11-19 02:10:05 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟡 둔화 | -1.5100 | KOSPI YoY=+24.09%, KOSDAQ YoY=-27.11%, KOSPI 4W=-12.89% |
| 2 | Breadth | 🔵 중립 | 0.2946 | RSP/SPY=0.2946 (Ratio, 무차원), 4W Δ=+0.0139, 4W 상승=breadth 개선 |
| 3 | Risk-on/off | 🔵 중립 | 1.6471 | SPHB/SPLV=1.6471 (Ratio, 무차원), 4W Δ=-0.2497 |
| 4 | VIX Term | 🔵 중립 | 1.0482 | VIX3M=24.29, VIX/VIX3M=1.0482 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+5.57 |
| 5 | 섹터 로테이션 | 🟠 경계 | -5.1800 | XLK 4W=-11.96%, XLE 4W=-6.78%, XLK-XLE=-5.18%p, XLP 4W=+4.23%, 방어(XLP) > 기술 → risk-off 로테이션 |
| 6 | 신용 방향 | 🔵 중립 | 0.7459 | HYG/LQD=0.7459 (Ratio, OAS 아님), 4W Δ=+0.0025 |

## 신호 상세

### 🟡 한국 주식 — 둔화
- **값**: -1.51
- **상세**: KOSPI YoY=+24.09%, KOSDAQ YoY=-27.11%, KOSPI 4W=-12.89%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.294577
- **상세**: RSP/SPY=0.2946 (Ratio, 무차원), 4W Δ=+0.0139, 4W 상승=breadth 개선
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🔵 Risk-on/off — 중립
- **값**: 1.647097
- **상세**: SPHB/SPLV=1.6471 (Ratio, 무차원), 4W Δ=-0.2497
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🔵 VIX Term — 중립
- **값**: 1.0482
- **상세**: VIX3M=24.29, VIX/VIX3M=1.0482 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+5.57
- **시리즈**: ^VIX3M, VIXCLS

### 🟠 섹터 로테이션 — 경계
- **값**: -5.18
- **상세**: XLK 4W=-11.96%, XLE 4W=-6.78%, XLK-XLE=-5.18%p, XLP 4W=+4.23%, 방어(XLP) > 기술 → risk-off 로테이션
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.745863
- **상세**: HYG/LQD=0.7459 (Ratio, OAS 아님), 4W Δ=+0.0025
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*