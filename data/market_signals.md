# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-10-29 (oldest: 2026-10-27 RSP)
> Freshness: OK (oldest 2d ≤ 5d)
> Generated: 2026-10-29 00:32:34 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 24.4900 | KOSPI YoY=+60.79%, KOSDAQ YoY=-11.80%, KOSPI 4W=-12.52% |
| 2 | Breadth | 🔵 중립 | 0.2826 | RSP/SPY=0.2826 (Ratio, 무차원), 4W Δ=+0.0085, 4W 상승=breadth 개선 |
| 3 | Risk-on/off | 🟢 risk-on | 1.8875 | SPHB/SPLV=1.8875 (Ratio, 무차원), 4W Δ=-0.2494 |
| 4 | VIX Term | 🔵 중립 | 0.9568 | VIX3M=19.22, VIX/VIX3M=0.9568 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.85 |
| 5 | 섹터 로테이션 | 🟠 경계 | -13.4200 | XLK 4W=-2.58%, XLE 4W=+10.84%, XLK-XLE=-13.42%p, XLP 4W=+6.48%, 방어(XLP) > 기술 → risk-off 로테이션 |
| 6 | 신용 방향 | 🟠 긴축 | 0.7440 | HYG/LQD=0.7440 (Ratio, OAS 아님), 4W Δ=-0.0113 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 24.49
- **상세**: KOSPI YoY=+60.79%, KOSDAQ YoY=-11.80%, KOSPI 4W=-12.52%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.282618
- **상세**: RSP/SPY=0.2826 (Ratio, 무차원), 4W Δ=+0.0085, 4W 상승=breadth 개선
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.887518
- **상세**: SPHB/SPLV=1.8875 (Ratio, 무차원), 4W Δ=-0.2494
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🔵 VIX Term — 중립
- **값**: 0.9568
- **상세**: VIX3M=19.22, VIX/VIX3M=0.9568 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.85
- **시리즈**: ^VIX3M, VIXCLS

### 🟠 섹터 로테이션 — 경계
- **값**: -13.42
- **상세**: XLK 4W=-2.58%, XLE 4W=+10.84%, XLK-XLE=-13.42%p, XLP 4W=+6.48%, 방어(XLP) > 기술 → risk-off 로테이션
- **시리즈**: XLK, XLE, XLP

### 🟠 신용 방향 — 긴축
- **값**: 0.744008
- **상세**: HYG/LQD=0.7440 (Ratio, OAS 아님), 4W Δ=-0.0113
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*