# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-06-25 (oldest: 2026-06-24 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-06-25 22:17:29 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 102.6400 | KOSPI YoY=+190.10%, KOSDAQ YoY=+15.18%, KOSPI 4W=+5.26% |
| 2 | Breadth | 🔵 중립 | 0.2884 | RSP/SPY=0.2884 (Ratio, 무차원), 4W Δ=+0.0122, 4W 상승=breadth 개선 |
| 3 | Risk-on/off | 🟢 강한 risk-on | 2.0607 | SPHB/SPLV=2.0607 (Ratio, 무차원), 4W Δ=+0.0713 |
| 4 | VIX Term | 🔵 중립 | 0.9587 | VIX3M=20.33, VIX/VIX3M=0.9587 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.33 |
| 5 | 섹터 로테이션 | 🟢 확장 | 4.6000 | XLK 4W=+0.20%, XLE 4W=-4.40%, XLK-XLE=+4.60%p, XLP 4W=-0.07% |
| 6 | 신용 방향 | 🟠 긴축 | 0.7295 | HYG/LQD=0.7295 (Ratio, OAS 아님), 4W Δ=-0.0051 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 102.64
- **상세**: KOSPI YoY=+190.10%, KOSDAQ YoY=+15.18%, KOSPI 4W=+5.26%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.28837
- **상세**: RSP/SPY=0.2884 (Ratio, 무차원), 4W Δ=+0.0122, 4W 상승=breadth 개선
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — 강한 risk-on
- **값**: 2.060748
- **상세**: SPHB/SPLV=2.0607 (Ratio, 무차원), 4W Δ=+0.0713
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🔵 VIX Term — 중립
- **값**: 0.9587
- **상세**: VIX3M=20.33, VIX/VIX3M=0.9587 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.33
- **시리즈**: ^VIX3M, VIXCLS

### 🟢 섹터 로테이션 — 확장
- **값**: 4.6
- **상세**: XLK 4W=+0.20%, XLE 4W=-4.40%, XLK-XLE=+4.60%p, XLP 4W=-0.07%
- **시리즈**: XLK, XLE, XLP

### 🟠 신용 방향 — 긴축
- **값**: 0.729498
- **상세**: HYG/LQD=0.7295 (Ratio, OAS 아님), 4W Δ=-0.0051
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*