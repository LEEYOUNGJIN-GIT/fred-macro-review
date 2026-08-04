# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-08-04 (oldest: 2026-08-03 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-08-04 22:06:01 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 42.3100 | KOSPI YoY=+94.89%, KOSDAQ YoY=-10.26%, KOSPI 4W=-22.64% |
| 2 | Breadth | 🔵 중립 | 0.2855 | RSP/SPY=0.2855 (Ratio, 무차원), 4W Δ=-0.0017 |
| 3 | Risk-on/off | 🟢 risk-on | 1.9504 | SPHB/SPLV=1.9504 (Ratio, 무차원), 4W Δ=+0.0510 |
| 4 | VIX Term | 🟢 contango | 0.8268 | VIX3M=19.34, VIX/VIX3M=0.8268 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.23 |
| 5 | 섹터 로테이션 | 🟡 둔화 | -2.7900 | XLK 4W=+4.31%, XLE 4W=+7.10%, XLK-XLE=-2.79%p, XLP 4W=+0.60% |
| 6 | 신용 방향 | 🟢 완화 | 0.7451 | HYG/LQD=0.7451 (Ratio, OAS 아님), 4W Δ=+0.0062 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 42.31
- **상세**: KOSPI YoY=+94.89%, KOSDAQ YoY=-10.26%, KOSPI 4W=-22.64%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.28552
- **상세**: RSP/SPY=0.2855 (Ratio, 무차원), 4W Δ=-0.0017
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.950386
- **상세**: SPHB/SPLV=1.9504 (Ratio, 무차원), 4W Δ=+0.0510
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.8268
- **상세**: VIX3M=19.34, VIX/VIX3M=0.8268 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.23
- **시리즈**: ^VIX3M, VIXCLS

### 🟡 섹터 로테이션 — 둔화
- **값**: -2.79
- **상세**: XLK 4W=+4.31%, XLE 4W=+7.10%, XLK-XLE=-2.79%p, XLP 4W=+0.60%
- **시리즈**: XLK, XLE, XLP

### 🟢 신용 방향 — 완화
- **값**: 0.745129
- **상세**: HYG/LQD=0.7451 (Ratio, OAS 아님), 4W Δ=+0.0062
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*