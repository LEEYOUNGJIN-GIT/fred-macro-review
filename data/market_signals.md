# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-07-27 (oldest: 2026-07-24 ^KS11)
> Freshness: OK (oldest 3d ≤ 5d)
> Generated: 2026-07-27 21:59:20 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 52.0800 | KOSPI YoY=+110.68%, KOSDAQ YoY=-6.53%, KOSPI 4W=-25.08% |
| 2 | Breadth | 🔵 중립 | 0.2911 | RSP/SPY=0.2911 (Ratio, 무차원), 4W Δ=+0.0026 |
| 3 | Risk-on/off | 🟢 risk-on | 1.8292 | SPHB/SPLV=1.8292 (Ratio, 무차원), 4W Δ=-0.1609 |
| 4 | VIX Term | 🟢 contango | 0.9257 | VIX3M=20.20, VIX/VIX3M=0.9257 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.63 |
| 5 | 섹터 로테이션 | 🟠 경계 | -12.1600 | XLK 4W=-3.76%, XLE 4W=+8.40%, XLK-XLE=-12.16%p, XLP 4W=+0.77%, 방어(XLP) > 기술 → risk-off 로테이션 |
| 6 | 신용 방향 | 🟢 완화 | 0.7442 | HYG/LQD=0.7442 (Ratio, OAS 아님), 4W Δ=+0.0160 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 52.08
- **상세**: KOSPI YoY=+110.68%, KOSDAQ YoY=-6.53%, KOSPI 4W=-25.08%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.291142
- **상세**: RSP/SPY=0.2911 (Ratio, 무차원), 4W Δ=+0.0026
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.829189
- **상세**: SPHB/SPLV=1.8292 (Ratio, 무차원), 4W Δ=-0.1609
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.9257
- **상세**: VIX3M=20.20, VIX/VIX3M=0.9257 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.63
- **시리즈**: ^VIX3M, VIXCLS

### 🟠 섹터 로테이션 — 경계
- **값**: -12.16
- **상세**: XLK 4W=-3.76%, XLE 4W=+8.40%, XLK-XLE=-12.16%p, XLP 4W=+0.77%, 방어(XLP) > 기술 → risk-off 로테이션
- **시리즈**: XLK, XLE, XLP

### 🟢 신용 방향 — 완화
- **값**: 0.744249
- **상세**: HYG/LQD=0.7442 (Ratio, OAS 아님), 4W Δ=+0.0160
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*