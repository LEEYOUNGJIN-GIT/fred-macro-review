# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-05-29 (oldest: 2026-05-28 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-05-29 22:25:03 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 131.4400 | KOSPI YoY=+212.25%, KOSDAQ YoY=+50.62%, KOSPI 4W=+23.74% |
| 2 | Breadth | 🔵 중립 | 0.2761 | RSP/SPY=0.2761 (Ratio, 무차원), 4W Δ=-0.0070, 4W 하락=대형주 쏠림 |
| 3 | Risk-on/off | 🟢 강한 risk-on | 2.0778 | SPHB/SPLV=2.0778 (Ratio, 무차원), 4W Δ=+0.2680 |
| 4 | VIX Term | 🟢 contango | 0.8730 | VIX3M=18.66, VIX/VIX3M=0.8730 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-1.42 |
| 5 | 섹터 로테이션 | 🟢 확장 | 25.3900 | XLK 4W=+19.76%, XLE 4W=-5.63%, XLK-XLE=+25.39%p, XLP 4W=-1.66% |
| 6 | 신용 방향 | 🔵 중립 | 0.7344 | HYG/LQD=0.7344 (Ratio, OAS 아님), 4W Δ=-0.0031 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 131.44
- **상세**: KOSPI YoY=+212.25%, KOSDAQ YoY=+50.62%, KOSPI 4W=+23.74%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.276055
- **상세**: RSP/SPY=0.2761 (Ratio, 무차원), 4W Δ=-0.0070, 4W 하락=대형주 쏠림
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — 강한 risk-on
- **값**: 2.077828
- **상세**: SPHB/SPLV=2.0778 (Ratio, 무차원), 4W Δ=+0.2680
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.873
- **상세**: VIX3M=18.66, VIX/VIX3M=0.8730 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-1.42
- **시리즈**: ^VIX3M, VIXCLS

### 🟢 섹터 로테이션 — 확장
- **값**: 25.39
- **상세**: XLK 4W=+19.76%, XLE 4W=-5.63%, XLK-XLE=+25.39%p, XLP 4W=-1.66%
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.734364
- **상세**: HYG/LQD=0.7344 (Ratio, OAS 아님), 4W Δ=-0.0031
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*