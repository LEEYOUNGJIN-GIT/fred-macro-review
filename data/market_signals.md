# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-10-15 (oldest: 2026-10-13 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-10-14 23:35:03 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 35.5200 | KOSPI YoY=+73.82%, KOSDAQ YoY=-2.78%, KOSPI 4W=-14.41% |
| 2 | Breadth | 🔵 중립 | 0.2756 | RSP/SPY=0.2756 (Ratio, 무차원), 4W Δ=-0.0056, 4W 하락=대형주 쏠림 |
| 3 | Risk-on/off | 🟢 risk-on | 1.9670 | SPHB/SPLV=1.9670 (Ratio, 무차원), 4W Δ=+0.0144 |
| 4 | VIX Term | 🟢 contango | 0.8095 | VIX3M=18.79, VIX/VIX3M=0.8095 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.94 |
| 5 | 섹터 로테이션 | 🟡 둔화 | -2.6000 | XLK 4W=+3.65%, XLE 4W=+6.25%, XLK-XLE=-2.60%p, XLP 4W=+3.96%, 방어(XLP) > 기술 → risk-off 로테이션 |
| 6 | 신용 방향 | 🔵 중립 | 0.7482 | HYG/LQD=0.7482 (Ratio, OAS 아님), 4W Δ=-0.0025 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 35.52
- **상세**: KOSPI YoY=+73.82%, KOSDAQ YoY=-2.78%, KOSPI 4W=-14.41%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.275585
- **상세**: RSP/SPY=0.2756 (Ratio, 무차원), 4W Δ=-0.0056, 4W 하락=대형주 쏠림
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.966981
- **상세**: SPHB/SPLV=1.9670 (Ratio, 무차원), 4W Δ=+0.0144
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.8095
- **상세**: VIX3M=18.79, VIX/VIX3M=0.8095 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.94
- **시리즈**: ^VIX3M, VIXCLS

### 🟡 섹터 로테이션 — 둔화
- **값**: -2.6
- **상세**: XLK 4W=+3.65%, XLE 4W=+6.25%, XLK-XLE=-2.60%p, XLP 4W=+3.96%, 방어(XLP) > 기술 → risk-off 로테이션
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.748198
- **상세**: HYG/LQD=0.7482 (Ratio, OAS 아님), 4W Δ=-0.0025
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*