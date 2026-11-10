# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-11-10 (oldest: 2026-11-09 ^NDX)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-11-10 03:05:28 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟡 둔화 | 1.0000 | KOSPI YoY=+28.31%, KOSDAQ YoY=-26.30%, KOSPI 4W=-13.23% |
| 2 | Breadth | 🔵 중립 | 0.2935 | RSP/SPY=0.2935 (Ratio, 무차원), 4W Δ=+0.0196, 4W 상승=breadth 개선 |
| 3 | Risk-on/off | 🟢 risk-on | 1.7420 | SPHB/SPLV=1.7420 (Ratio, 무차원), 4W Δ=-0.3345 |
| 4 | VIX Term | 🟡 backwardation | 1.2297 | VIX3M=20.85, VIX/VIX3M=1.2297 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+2.92 |
| 5 | 섹터 로테이션 | 🟠 경계 | -6.8100 | XLK 4W=-12.98%, XLE 4W=-6.17%, XLK-XLE=-6.81%p, XLP 4W=+7.68%, 방어(XLP) > 기술 → risk-off 로테이션 |
| 6 | 신용 방향 | 🟠 긴축 | 0.7405 | HYG/LQD=0.7405 (Ratio, OAS 아님), 4W Δ=-0.0129 |

## 신호 상세

### 🟡 한국 주식 — 둔화
- **값**: 1.0
- **상세**: KOSPI YoY=+28.31%, KOSDAQ YoY=-26.30%, KOSPI 4W=-13.23%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.293547
- **상세**: RSP/SPY=0.2935 (Ratio, 무차원), 4W Δ=+0.0196, 4W 상승=breadth 개선
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.742002
- **상세**: SPHB/SPLV=1.7420 (Ratio, 무차원), 4W Δ=-0.3345
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟡 VIX Term — backwardation
- **값**: 1.2297
- **상세**: VIX3M=20.85, VIX/VIX3M=1.2297 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+2.92
- **시리즈**: ^VIX3M, VIXCLS

### 🟠 섹터 로테이션 — 경계
- **값**: -6.81
- **상세**: XLK 4W=-12.98%, XLE 4W=-6.17%, XLK-XLE=-6.81%p, XLP 4W=+7.68%, 방어(XLP) > 기술 → risk-off 로테이션
- **시리즈**: XLK, XLE, XLP

### 🟠 신용 방향 — 긴축
- **값**: 0.740518
- **상세**: HYG/LQD=0.7405 (Ratio, OAS 아님), 4W Δ=-0.0129
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*