# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-06-02 (oldest: 2026-06-01 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-06-02 22:56:43 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 142.3400 | KOSPI YoY=+237.57%, KOSDAQ YoY=+47.11%, KOSPI 4W=+31.35% |
| 2 | Breadth | 🔵 중립 | 0.2765 | RSP/SPY=0.2765 (Ratio, 무차원), 4W Δ=-0.0043 |
| 3 | Risk-on/off | 🟢 강한 risk-on | 2.1383 | SPHB/SPLV=2.1383 (Ratio, 무차원), 4W Δ=+0.2969 |
| 4 | VIX Term | 🟢 contango | 0.7860 | VIX3M=19.49, VIX/VIX3M=0.7860 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-1.56 |
| 5 | 섹터 로테이션 | 🟢 확장 | 24.7200 | XLK 4W=+22.31%, XLE 4W=-2.41%, XLK-XLE=+24.72%p, XLP 4W=-2.05% |
| 6 | 신용 방향 | 🔵 중립 | 0.7336 | HYG/LQD=0.7336 (Ratio, OAS 아님), 4W Δ=-0.0026 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 142.34
- **상세**: KOSPI YoY=+237.57%, KOSDAQ YoY=+47.11%, KOSPI 4W=+31.35%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.276525
- **상세**: RSP/SPY=0.2765 (Ratio, 무차원), 4W Δ=-0.0043
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — 강한 risk-on
- **값**: 2.138331
- **상세**: SPHB/SPLV=2.1383 (Ratio, 무차원), 4W Δ=+0.2969
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.786
- **상세**: VIX3M=19.49, VIX/VIX3M=0.7860 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-1.56
- **시리즈**: ^VIX3M, VIXCLS

### 🟢 섹터 로테이션 — 확장
- **값**: 24.72
- **상세**: XLK 4W=+22.31%, XLE 4W=-2.41%, XLK-XLE=+24.72%p, XLP 4W=-2.05%
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.733566
- **상세**: HYG/LQD=0.7336 (Ratio, OAS 아님), 4W Δ=-0.0026
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*