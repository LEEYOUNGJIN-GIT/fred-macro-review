# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-11-27 (oldest: 2026-11-25 ^NDX)
> Freshness: OK (oldest 2d ≤ 5d)
> Generated: 2026-11-27 03:24:55 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟡 둔화 | -2.4200 | KOSPI YoY=+18.36%, KOSDAQ YoY=-23.19%, KOSPI 4W=-15.54% |
| 2 | Breadth | 🔵 균형 | 0.3010 | RSP/SPY=0.3010 (Ratio, 무차원), 4W Δ=+0.0195, 4W 상승=breadth 개선 |
| 3 | Risk-on/off | 🔵 중립 | 1.5513 | SPHB/SPLV=1.5513 (Ratio, 무차원), 4W Δ=-0.3742 |
| 4 | VIX Term | 🔵 중립 | 1.0027 | VIX3M=26.29, VIX/VIX3M=1.0027 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+7.07 |
| 5 | 섹터 로테이션 | 🟠 경계 | -7.4000 | XLK 4W=-18.43%, XLE 4W=-11.03%, XLK-XLE=-7.40%p, XLP 4W=+6.29%, 방어(XLP) > 기술 → risk-off 로테이션 |
| 6 | 신용 방향 | 🟠 긴축 | 0.7337 | HYG/LQD=0.7337 (Ratio, OAS 아님), 4W Δ=-0.0108 |

## 신호 상세

### 🟡 한국 주식 — 둔화
- **값**: -2.42
- **상세**: KOSPI YoY=+18.36%, KOSDAQ YoY=-23.19%, KOSPI 4W=-15.54%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 균형
- **값**: 0.301019
- **상세**: RSP/SPY=0.3010 (Ratio, 무차원), 4W Δ=+0.0195, 4W 상승=breadth 개선
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🔵 Risk-on/off — 중립
- **값**: 1.5513
- **상세**: SPHB/SPLV=1.5513 (Ratio, 무차원), 4W Δ=-0.3742
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🔵 VIX Term — 중립
- **값**: 1.0027
- **상세**: VIX3M=26.29, VIX/VIX3M=1.0027 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+7.07
- **시리즈**: ^VIX3M, VIXCLS

### 🟠 섹터 로테이션 — 경계
- **값**: -7.4
- **상세**: XLK 4W=-18.43%, XLE 4W=-11.03%, XLK-XLE=-7.40%p, XLP 4W=+6.29%, 방어(XLP) > 기술 → risk-off 로테이션
- **시리즈**: XLK, XLE, XLP

### 🟠 신용 방향 — 긴축
- **값**: 0.733723
- **상세**: HYG/LQD=0.7337 (Ratio, OAS 아님), 4W Δ=-0.0108
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*