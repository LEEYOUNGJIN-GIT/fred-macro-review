# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-10-23 (oldest: 2026-10-21 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-10-22 23:48:13 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 27.2000 | KOSPI YoY=+61.60%, KOSDAQ YoY=-7.20%, KOSPI 4W=-14.59% |
| 2 | Breadth | 🔵 중립 | 0.2856 | RSP/SPY=0.2856 (Ratio, 무차원), 4W Δ=+0.0116, 4W 상승=breadth 개선 |
| 3 | Risk-on/off | 🟢 risk-on | 1.7972 | SPHB/SPLV=1.7972 (Ratio, 무차원), 4W Δ=-0.3367 |
| 4 | VIX Term | 🟢 contango | 0.9165 | VIX3M=20.12, VIX/VIX3M=0.9165 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+1.69 |
| 5 | 섹터 로테이션 | 🟠 경계 | -14.2900 | XLK 4W=-6.35%, XLE 4W=+7.94%, XLK-XLE=-14.29%p, XLP 4W=+10.15%, 방어(XLP) > 기술 → risk-off 로테이션 |
| 6 | 신용 방향 | 🟠 긴축 | 0.7394 | HYG/LQD=0.7394 (Ratio, OAS 아님), 4W Δ=-0.0157 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 27.2
- **상세**: KOSPI YoY=+61.60%, KOSDAQ YoY=-7.20%, KOSPI 4W=-14.59%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.285643
- **상세**: RSP/SPY=0.2856 (Ratio, 무차원), 4W Δ=+0.0116, 4W 상승=breadth 개선
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.797164
- **상세**: SPHB/SPLV=1.7972 (Ratio, 무차원), 4W Δ=-0.3367
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.9165
- **상세**: VIX3M=20.12, VIX/VIX3M=0.9165 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+1.69
- **시리즈**: ^VIX3M, VIXCLS

### 🟠 섹터 로테이션 — 경계
- **값**: -14.29
- **상세**: XLK 4W=-6.35%, XLE 4W=+7.94%, XLK-XLE=-14.29%p, XLP 4W=+10.15%, 방어(XLP) > 기술 → risk-off 로테이션
- **시리즈**: XLK, XLE, XLP

### 🟠 신용 방향 — 긴축
- **값**: 0.739356
- **상세**: HYG/LQD=0.7394 (Ratio, OAS 아님), 4W Δ=-0.0157
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*