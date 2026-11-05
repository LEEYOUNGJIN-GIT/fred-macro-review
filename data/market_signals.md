# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-11-05 (oldest: 2026-11-03 RSP)
> Freshness: OK (oldest 2d ≤ 5d)
> Generated: 2026-11-05 01:13:04 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🔵 중립 | 11.1500 | KOSPI YoY=+42.59%, KOSDAQ YoY=-20.30%, KOSPI 4W=-21.00% |
| 2 | Breadth | 🔵 중립 | 0.2907 | RSP/SPY=0.2907 (Ratio, 무차원), 4W Δ=+0.0181, 4W 상승=breadth 개선 |
| 3 | Risk-on/off | 🟢 risk-on | 1.7833 | SPHB/SPLV=1.7833 (Ratio, 무차원), 4W Δ=-0.4066 |
| 4 | VIX Term | 🟡 backwardation | 1.1080 | VIX3M=18.80, VIX/VIX3M=1.1080 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+1.08 |
| 5 | 섹터 로테이션 | 🟠 경계 | -17.2200 | XLK 4W=-12.62%, XLE 4W=+4.60%, XLK-XLE=-17.22%p, XLP 4W=+8.74%, 방어(XLP) > 기술 → risk-off 로테이션 |
| 6 | 신용 방향 | 🟠 긴축 | 0.7422 | HYG/LQD=0.7422 (Ratio, OAS 아님), 4W Δ=-0.0143 |

## 신호 상세

### 🔵 한국 주식 — 중립
- **값**: 11.15
- **상세**: KOSPI YoY=+42.59%, KOSDAQ YoY=-20.30%, KOSPI 4W=-21.00%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.290661
- **상세**: RSP/SPY=0.2907 (Ratio, 무차원), 4W Δ=+0.0181, 4W 상승=breadth 개선
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.783299
- **상세**: SPHB/SPLV=1.7833 (Ratio, 무차원), 4W Δ=-0.4066
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟡 VIX Term — backwardation
- **값**: 1.108
- **상세**: VIX3M=18.80, VIX/VIX3M=1.1080 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+1.08
- **시리즈**: ^VIX3M, VIXCLS

### 🟠 섹터 로테이션 — 경계
- **값**: -17.22
- **상세**: XLK 4W=-12.62%, XLE 4W=+4.60%, XLK-XLE=-17.22%p, XLP 4W=+8.74%, 방어(XLP) > 기술 → risk-off 로테이션
- **시리즈**: XLK, XLE, XLP

### 🟠 신용 방향 — 긴축
- **값**: 0.742191
- **상세**: HYG/LQD=0.7422 (Ratio, OAS 아님), 4W Δ=-0.0143
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*