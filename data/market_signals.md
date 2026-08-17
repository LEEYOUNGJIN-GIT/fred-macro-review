# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-08-17 (oldest: 2026-08-14 ^KS11)
> Freshness: OK (oldest 3d ≤ 5d)
> Generated: 2026-08-17 21:19:10 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 65.5300 | KOSPI YoY=+123.69%, KOSDAQ YoY=+7.38%, KOSPI 4W=+2.31% |
| 2 | Breadth | 🔵 중립 | 0.2857 | RSP/SPY=0.2857 (Ratio, 무차원), 4W Δ=-0.0005 |
| 3 | Risk-on/off | 🟢 강한 risk-on | 2.0018 | SPHB/SPLV=2.0018 (Ratio, 무차원), 4W Δ=+0.1539 |
| 4 | VIX Term | 🟢 contango | 0.7684 | VIX3M=19.04, VIX/VIX3M=0.7684 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.53 |
| 5 | 섹터 로테이션 | 🔵 중립 | 0.3000 | XLK 4W=+8.31%, XLE 4W=+8.01%, XLK-XLE=+0.30%p, XLP 4W=-0.21% |
| 6 | 신용 방향 | 🟢 완화 | 0.7532 | HYG/LQD=0.7532 (Ratio, OAS 아님), 4W Δ=+0.0099 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 65.53
- **상세**: KOSPI YoY=+123.69%, KOSDAQ YoY=+7.38%, KOSPI 4W=+2.31%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.285749
- **상세**: RSP/SPY=0.2857 (Ratio, 무차원), 4W Δ=-0.0005
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — 강한 risk-on
- **값**: 2.001848
- **상세**: SPHB/SPLV=2.0018 (Ratio, 무차원), 4W Δ=+0.1539
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.7684
- **상세**: VIX3M=19.04, VIX/VIX3M=0.7684 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.53
- **시리즈**: ^VIX3M, VIXCLS

### 🔵 섹터 로테이션 — 중립
- **값**: 0.3
- **상세**: XLK 4W=+8.31%, XLE 4W=+8.01%, XLK-XLE=+0.30%p, XLP 4W=-0.21%
- **시리즈**: XLK, XLE, XLP

### 🟢 신용 방향 — 완화
- **값**: 0.753169
- **상세**: HYG/LQD=0.7532 (Ratio, OAS 아님), 4W Δ=+0.0099
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*