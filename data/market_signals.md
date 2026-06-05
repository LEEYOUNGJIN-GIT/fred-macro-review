# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-06-05 (oldest: 2026-06-04 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-06-05 22:14:53 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 137.0600 | KOSPI YoY=+229.05%, KOSDAQ YoY=+45.07%, KOSPI 4W=+24.54% |
| 2 | Breadth | 🔵 중립 | 0.2818 | RSP/SPY=0.2818 (Ratio, 무차원), 4W Δ=+0.0036 |
| 3 | Risk-on/off | 🟢 risk-on | 1.9495 | SPHB/SPLV=1.9495 (Ratio, 무차원), 4W Δ=+0.0478 |
| 4 | VIX Term | 🟢 contango | 0.7360 | VIX3M=21.82, VIX/VIX3M=0.7360 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+1.47 |
| 5 | 섹터 로테이션 | 🟢 확장 | 3.1800 | XLK 4W=+6.25%, XLE 4W=+3.07%, XLK-XLE=+3.18%p, XLP 4W=-0.64% |
| 6 | 신용 방향 | 🔵 중립 | 0.7343 | HYG/LQD=0.7343 (Ratio, OAS 아님), 4W Δ=+0.0009 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 137.06
- **상세**: KOSPI YoY=+229.05%, KOSDAQ YoY=+45.07%, KOSPI 4W=+24.54%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.281784
- **상세**: RSP/SPY=0.2818 (Ratio, 무차원), 4W Δ=+0.0036
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.949503
- **상세**: SPHB/SPLV=1.9495 (Ratio, 무차원), 4W Δ=+0.0478
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.736
- **상세**: VIX3M=21.82, VIX/VIX3M=0.7360 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+1.47
- **시리즈**: ^VIX3M, VIXCLS

### 🟢 섹터 로테이션 — 확장
- **값**: 3.18
- **상세**: XLK 4W=+6.25%, XLE 4W=+3.07%, XLK-XLE=+3.18%p, XLP 4W=-0.64%
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.734307
- **상세**: HYG/LQD=0.7343 (Ratio, OAS 아님), 4W Δ=+0.0009
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*