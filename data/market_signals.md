# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-05-28 (oldest: 2026-05-27 ^NDX)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-05-28 07:12:49 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 131.4400 | KOSPI YoY=+212.25%, KOSDAQ YoY=+50.62%, KOSPI 4W=+23.74% |
| 2 | Breadth | 🔵 중립 | 0.2765 | RSP/SPY=0.2765 (Ratio, 무차원), 4W Δ=-0.0056, 4W 하락=대형주 쏠림 |
| 3 | Risk-on/off | 🟢 risk-on | 1.9882 | SPHB/SPLV=1.9882 (Ratio, 무차원), 4W Δ=+0.2099 |
| 4 | VIX Term | 🟢 contango | 0.8746 | VIX3M=19.45, VIX/VIX3M=0.8746 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-1.04 |
| 5 | 섹터 로테이션 | 🟢 확장 | 18.0900 | XLK 4W=+16.84%, XLE 4W=-1.25%, XLK-XLE=+18.09%p, XLP 4W=+1.81% |
| 6 | 신용 방향 | 🔵 중립 | 0.7356 | HYG/LQD=0.7356 (Ratio, OAS 아님), 4W Δ=+0.0013 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 131.44
- **상세**: KOSPI YoY=+212.25%, KOSDAQ YoY=+50.62%, KOSPI 4W=+23.74%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.276484
- **상세**: RSP/SPY=0.2765 (Ratio, 무차원), 4W Δ=-0.0056, 4W 하락=대형주 쏠림
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.988176
- **상세**: SPHB/SPLV=1.9882 (Ratio, 무차원), 4W Δ=+0.2099
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.8746
- **상세**: VIX3M=19.45, VIX/VIX3M=0.8746 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-1.04
- **시리즈**: ^VIX3M, VIXCLS

### 🟢 섹터 로테이션 — 확장
- **값**: 18.09
- **상세**: XLK 4W=+16.84%, XLE 4W=-1.25%, XLK-XLE=+18.09%p, XLP 4W=+1.81%
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.73561
- **상세**: HYG/LQD=0.7356 (Ratio, OAS 아님), 4W Δ=+0.0013
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*