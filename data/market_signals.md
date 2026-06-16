# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-06-16 (oldest: 2026-06-15 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-06-16 22:51:08 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 128.8000 | KOSPI YoY=+216.79%, KOSDAQ YoY=+40.81%, KOSPI 4W=+7.07% |
| 2 | Breadth | 🔵 중립 | 0.2828 | RSP/SPY=0.2828 (Ratio, 무차원), 4W Δ=+0.0082, 4W 상승=breadth 개선 |
| 3 | Risk-on/off | 🟢 강한 risk-on | 2.0389 | SPHB/SPLV=2.0389 (Ratio, 무차원), 4W Δ=+0.1891 |
| 4 | VIX Term | 🟢 contango | 0.9053 | VIX3M=19.53, VIX/VIX3M=0.9053 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-1.83 |
| 5 | 섹터 로테이션 | 🟢 확장 | 15.5500 | XLK 4W=+6.93%, XLE 4W=-8.62%, XLK-XLE=+15.55%p, XLP 4W=-0.36% |
| 6 | 신용 방향 | 🔵 중립 | 0.7334 | HYG/LQD=0.7334 (Ratio, OAS 아님), 4W Δ=-0.0044 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 128.8
- **상세**: KOSPI YoY=+216.79%, KOSDAQ YoY=+40.81%, KOSPI 4W=+7.07%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.282769
- **상세**: RSP/SPY=0.2828 (Ratio, 무차원), 4W Δ=+0.0082, 4W 상승=breadth 개선
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — 강한 risk-on
- **값**: 2.038926
- **상세**: SPHB/SPLV=2.0389 (Ratio, 무차원), 4W Δ=+0.1891
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.9053
- **상세**: VIX3M=19.53, VIX/VIX3M=0.9053 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-1.83
- **시리즈**: ^VIX3M, VIXCLS

### 🟢 섹터 로테이션 — 확장
- **값**: 15.55
- **상세**: XLK 4W=+6.93%, XLE 4W=-8.62%, XLK-XLE=+15.55%p, XLP 4W=-0.36%
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.733413
- **상세**: HYG/LQD=0.7334 (Ratio, OAS 아님), 4W Δ=-0.0044
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*