# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-10-08 (oldest: 2026-10-06 RSP)
> Freshness: OK (oldest 2d ≤ 5d)
> Generated: 2026-10-08 00:39:11 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 49.8900 | KOSPI YoY=+96.97%, KOSDAQ YoY=+2.81%, KOSPI 4W=+1.48% |
| 2 | Breadth | 🔵 중립 | 0.2725 | RSP/SPY=0.2725 (Ratio, 무차원), 4W Δ=-0.0101, 4W 하락=대형주 쏠림 |
| 3 | Risk-on/off | 🟢 강한 risk-on | 2.1856 | SPHB/SPLV=2.1856 (Ratio, 무차원), 4W Δ=+0.1783 |
| 4 | VIX Term | 🟢 contango | 0.8758 | VIX3M=17.72, VIX/VIX3M=0.8758 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-1.15 |
| 5 | 섹터 로테이션 | 🟢 확장 | 8.6400 | XLK 4W=+7.65%, XLE 4W=-0.99%, XLK-XLE=+8.64%p, XLP 4W=-2.00% |
| 6 | 신용 방향 | 🟢 완화 | 0.7565 | HYG/LQD=0.7565 (Ratio, OAS 아님), 4W Δ=+0.0065 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 49.89
- **상세**: KOSPI YoY=+96.97%, KOSDAQ YoY=+2.81%, KOSPI 4W=+1.48%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.272536
- **상세**: RSP/SPY=0.2725 (Ratio, 무차원), 4W Δ=-0.0101, 4W 하락=대형주 쏠림
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — 강한 risk-on
- **값**: 2.185557
- **상세**: SPHB/SPLV=2.1856 (Ratio, 무차원), 4W Δ=+0.1783
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.8758
- **상세**: VIX3M=17.72, VIX/VIX3M=0.8758 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-1.15
- **시리즈**: ^VIX3M, VIXCLS

### 🟢 섹터 로테이션 — 확장
- **값**: 8.64
- **상세**: XLK 4W=+7.65%, XLE 4W=-0.99%, XLK-XLE=+8.64%p, XLP 4W=-2.00%
- **시리즈**: XLK, XLE, XLP

### 🟢 신용 방향 — 완화
- **값**: 0.756511
- **상세**: HYG/LQD=0.7565 (Ratio, OAS 아님), 4W Δ=+0.0065
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*