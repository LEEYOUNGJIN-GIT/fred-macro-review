# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-10-16 (oldest: 2026-10-14 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-10-15 23:29:36 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 34.8800 | KOSPI YoY=+73.11%, KOSDAQ YoY=-3.35%, KOSPI 4W=-14.57% |
| 2 | Breadth | 🔵 중립 | 0.2786 | RSP/SPY=0.2786 (Ratio, 무차원), 4W Δ=-0.0008 |
| 3 | Risk-on/off | 🟢 risk-on | 1.9585 | SPHB/SPLV=1.9585 (Ratio, 무차원), 4W Δ=-0.0351 |
| 4 | VIX Term | 🟢 contango | 0.8259 | VIX3M=18.49, VIX/VIX3M=0.8259 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.06 |
| 5 | 섹터 로테이션 | 🟠 경계 | -3.1200 | XLK 4W=+0.72%, XLE 4W=+3.84%, XLK-XLE=-3.12%p, XLP 4W=+4.50%, 방어(XLP) > 기술 → risk-off 로테이션 |
| 6 | 신용 방향 | 🔵 중립 | 0.7452 | HYG/LQD=0.7452 (Ratio, OAS 아님), 4W Δ=-0.0033 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 34.88
- **상세**: KOSPI YoY=+73.11%, KOSDAQ YoY=-3.35%, KOSPI 4W=-14.57%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.278573
- **상세**: RSP/SPY=0.2786 (Ratio, 무차원), 4W Δ=-0.0008
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.958486
- **상세**: SPHB/SPLV=1.9585 (Ratio, 무차원), 4W Δ=-0.0351
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.8259
- **상세**: VIX3M=18.49, VIX/VIX3M=0.8259 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.06
- **시리즈**: ^VIX3M, VIXCLS

### 🟠 섹터 로테이션 — 경계
- **값**: -3.12
- **상세**: XLK 4W=+0.72%, XLE 4W=+3.84%, XLK-XLE=-3.12%p, XLP 4W=+4.50%, 방어(XLP) > 기술 → risk-off 로테이션
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.745217
- **상세**: HYG/LQD=0.7452 (Ratio, OAS 아님), 4W Δ=-0.0033
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*