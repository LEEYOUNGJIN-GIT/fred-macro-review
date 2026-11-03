# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-11-03 (oldest: 2026-11-02 ^NDX)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-11-03 02:43:46 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🔵 중립 | 14.4400 | KOSPI YoY=+47.30%, KOSDAQ YoY=-18.42%, KOSPI 4W=-18.32% |
| 2 | Breadth | 🔵 중립 | 0.2925 | RSP/SPY=0.2925 (Ratio, 무차원), 4W Δ=+0.0200, 4W 상승=breadth 개선 |
| 3 | Risk-on/off | 🟢 risk-on | 1.7429 | SPHB/SPLV=1.7429 (Ratio, 무차원), 4W Δ=-0.4497 |
| 4 | VIX Term | 🟢 contango | 0.8991 | VIX3M=21.60, VIX/VIX3M=0.8991 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+3.60 |
| 5 | 섹터 로테이션 | 🟠 경계 | -19.2800 | XLK 4W=-13.29%, XLE 4W=+5.99%, XLK-XLE=-19.28%p, XLP 4W=+12.08%, 방어(XLP) > 기술 → risk-off 로테이션 |
| 6 | 신용 방향 | 🟠 긴축 | 0.7414 | HYG/LQD=0.7414 (Ratio, OAS 아님), 4W Δ=-0.0146 |

## 신호 상세

### 🔵 한국 주식 — 중립
- **값**: 14.44
- **상세**: KOSPI YoY=+47.30%, KOSDAQ YoY=-18.42%, KOSPI 4W=-18.32%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.292488
- **상세**: RSP/SPY=0.2925 (Ratio, 무차원), 4W Δ=+0.0200, 4W 상승=breadth 개선
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.742931
- **상세**: SPHB/SPLV=1.7429 (Ratio, 무차원), 4W Δ=-0.4497
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.8991
- **상세**: VIX3M=21.60, VIX/VIX3M=0.8991 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+3.60
- **시리즈**: ^VIX3M, VIXCLS

### 🟠 섹터 로테이션 — 경계
- **값**: -19.28
- **상세**: XLK 4W=-13.29%, XLE 4W=+5.99%, XLK-XLE=-19.28%p, XLP 4W=+12.08%, 방어(XLP) > 기술 → risk-off 로테이션
- **시리즈**: XLK, XLE, XLP

### 🟠 신용 방향 — 긴축
- **값**: 0.741394
- **상세**: HYG/LQD=0.7414 (Ratio, OAS 아님), 4W Δ=-0.0146
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*