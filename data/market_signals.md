# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-11-06 (oldest: 2026-11-05 ^KS11)
> Freshness: OK (oldest 2d ≤ 5d)
> Generated: 2026-11-07 00:32:39 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🔵 중립 | 6.7100 | KOSPI YoY=+36.59%, KOSDAQ YoY=-23.18%, KOSPI 4W=-20.87% |
| 2 | Breadth | 🔵 중립 | 0.2938 | RSP/SPY=0.2938 (Ratio, 무차원), 4W Δ=+0.0202, 4W 상승=breadth 개선 |
| 3 | Risk-on/off | 🔵 중립 | 1.6713 | SPHB/SPLV=1.6713 (Ratio, 무차원), 4W Δ=-0.4699 |
| 4 | VIX Term | 🟡 backwardation | 1.1455 | VIX3M=24.60, VIX/VIX3M=1.1455 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+6.83 |
| 5 | 섹터 로테이션 | 🟠 경계 | -11.8000 | XLK 4W=-17.12%, XLE 4W=-5.32%, XLK-XLE=-11.80%p, XLP 4W=+7.97%, 방어(XLP) > 기술 → risk-off 로테이션 |
| 6 | 신용 방향 | 🟠 긴축 | 0.7388 | HYG/LQD=0.7388 (Ratio, OAS 아님), 4W Δ=-0.0153 |

## 신호 상세

### 🔵 한국 주식 — 중립
- **값**: 6.71
- **상세**: KOSPI YoY=+36.59%, KOSDAQ YoY=-23.18%, KOSPI 4W=-20.87%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.29383
- **상세**: RSP/SPY=0.2938 (Ratio, 무차원), 4W Δ=+0.0202, 4W 상승=breadth 개선
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🔵 Risk-on/off — 중립
- **값**: 1.671263
- **상세**: SPHB/SPLV=1.6713 (Ratio, 무차원), 4W Δ=-0.4699
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟡 VIX Term — backwardation
- **값**: 1.1455
- **상세**: VIX3M=24.60, VIX/VIX3M=1.1455 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+6.83
- **시리즈**: ^VIX3M, VIXCLS

### 🟠 섹터 로테이션 — 경계
- **값**: -11.8
- **상세**: XLK 4W=-17.12%, XLE 4W=-5.32%, XLK-XLE=-11.80%p, XLP 4W=+7.97%, 방어(XLP) > 기술 → risk-off 로테이션
- **시리즈**: XLK, XLE, XLP

### 🟠 신용 방향 — 긴축
- **값**: 0.738831
- **상세**: HYG/LQD=0.7388 (Ratio, OAS 아님), 4W Δ=-0.0153
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*