# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-08-13 (oldest: 2026-08-12 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-08-13 21:37:31 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 54.5100 | KOSPI YoY=+102.15%, KOSDAQ YoY=+6.87%, KOSPI 4W=-4.05% |
| 2 | Breadth | 🔵 중립 | 0.2863 | RSP/SPY=0.2863 (Ratio, 무차원), 4W Δ=-0.0001 |
| 3 | Risk-on/off | 🟢 risk-on | 1.9877 | SPHB/SPLV=1.9877 (Ratio, 무차원), 4W Δ=+0.1267 |
| 4 | VIX Term | 🟢 contango | 0.8211 | VIX3M=18.61, VIX/VIX3M=0.8211 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.96 |
| 5 | 섹터 로테이션 | 🔵 중립 | 0.3700 | XLK 4W=+7.46%, XLE 4W=+7.09%, XLK-XLE=+0.37%p, XLP 4W=+0.22% |
| 6 | 신용 방향 | 🟢 완화 | 0.7489 | HYG/LQD=0.7489 (Ratio, OAS 아님), 4W Δ=+0.0060 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 54.51
- **상세**: KOSPI YoY=+102.15%, KOSDAQ YoY=+6.87%, KOSPI 4W=-4.05%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.28633
- **상세**: RSP/SPY=0.2863 (Ratio, 무차원), 4W Δ=-0.0001
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.987669
- **상세**: SPHB/SPLV=1.9877 (Ratio, 무차원), 4W Δ=+0.1267
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.8211
- **상세**: VIX3M=18.61, VIX/VIX3M=0.8211 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.96
- **시리즈**: ^VIX3M, VIXCLS

### 🔵 섹터 로테이션 — 중립
- **값**: 0.37
- **상세**: XLK 4W=+7.46%, XLE 4W=+7.09%, XLK-XLE=+0.37%p, XLP 4W=+0.22%
- **시리즈**: XLK, XLE, XLP

### 🟢 신용 방향 — 완화
- **값**: 0.74885
- **상세**: HYG/LQD=0.7489 (Ratio, OAS 아님), 4W Δ=+0.0060
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*