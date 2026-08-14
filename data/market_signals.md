# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-08-14 (oldest: 2026-08-13 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-08-14 21:18:50 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 58.4500 | KOSPI YoY=+109.94%, KOSDAQ YoY=+6.97%, KOSPI 4W=-6.47% |
| 2 | Breadth | 🔵 중립 | 0.2869 | RSP/SPY=0.2869 (Ratio, 무차원), 4W Δ=+0.0048 |
| 3 | Risk-on/off | 🟢 risk-on | 1.9852 | SPHB/SPLV=1.9852 (Ratio, 무차원), 4W Δ=+0.1411 |
| 4 | VIX Term | 🟢 contango | 0.7882 | VIX3M=18.46, VIX/VIX3M=0.7882 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-1.11 |
| 5 | 섹터 로테이션 | 🔵 중립 | 0.8800 | XLK 4W=+8.21%, XLE 4W=+7.33%, XLK-XLE=+0.88%p, XLP 4W=+1.06% |
| 6 | 신용 방향 | 🟢 완화 | 0.7511 | HYG/LQD=0.7511 (Ratio, OAS 아님), 4W Δ=+0.0110 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 58.45
- **상세**: KOSPI YoY=+109.94%, KOSDAQ YoY=+6.97%, KOSPI 4W=-6.47%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.286949
- **상세**: RSP/SPY=0.2869 (Ratio, 무차원), 4W Δ=+0.0048
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.985202
- **상세**: SPHB/SPLV=1.9852 (Ratio, 무차원), 4W Δ=+0.1411
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.7882
- **상세**: VIX3M=18.46, VIX/VIX3M=0.7882 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-1.11
- **시리즈**: ^VIX3M, VIXCLS

### 🔵 섹터 로테이션 — 중립
- **값**: 0.88
- **상세**: XLK 4W=+8.21%, XLE 4W=+7.33%, XLK-XLE=+0.88%p, XLP 4W=+1.06%
- **시리즈**: XLK, XLE, XLP

### 🟢 신용 방향 — 완화
- **값**: 0.751131
- **상세**: HYG/LQD=0.7511 (Ratio, OAS 아님), 4W Δ=+0.0110
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*