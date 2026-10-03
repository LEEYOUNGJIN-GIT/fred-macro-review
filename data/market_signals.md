# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-10-02 (oldest: 2026-09-30 ^HSI)
> Freshness: OK (oldest 3d ≤ 5d)
> Generated: 2026-10-03 00:05:31 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 53.5400 | KOSPI YoY=+102.09%, KOSDAQ YoY=+4.98%, KOSPI 4W=+1.98% |
| 2 | Breadth | 🔵 중립 | 0.2736 | RSP/SPY=0.2736 (Ratio, 무차원), 4W Δ=-0.0118, 4W 하락=대형주 쏠림 |
| 3 | Risk-on/off | 🟢 강한 risk-on | 2.1653 | SPHB/SPLV=2.1653 (Ratio, 무차원), 4W Δ=+0.2303 |
| 4 | VIX Term | 🟢 contango | 0.9073 | VIX3M=18.01, VIX/VIX3M=0.9073 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.59 |
| 5 | 섹터 로테이션 | 🟢 확장 | 10.9800 | XLK 4W=+7.87%, XLE 4W=-3.11%, XLK-XLE=+10.98%p, XLP 4W=-5.46% |
| 6 | 신용 방향 | 🔵 중립 | 0.7537 | HYG/LQD=0.7537 (Ratio, OAS 아님), 4W Δ=+0.0029 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 53.54
- **상세**: KOSPI YoY=+102.09%, KOSDAQ YoY=+4.98%, KOSPI 4W=+1.98%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.273564
- **상세**: RSP/SPY=0.2736 (Ratio, 무차원), 4W Δ=-0.0118, 4W 하락=대형주 쏠림
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — 강한 risk-on
- **값**: 2.165251
- **상세**: SPHB/SPLV=2.1653 (Ratio, 무차원), 4W Δ=+0.2303
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.9073
- **상세**: VIX3M=18.01, VIX/VIX3M=0.9073 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=+0.59
- **시리즈**: ^VIX3M, VIXCLS

### 🟢 섹터 로테이션 — 확장
- **값**: 10.98
- **상세**: XLK 4W=+7.87%, XLE 4W=-3.11%, XLK-XLE=+10.98%p, XLP 4W=-5.46%
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.7537
- **상세**: HYG/LQD=0.7537 (Ratio, OAS 아님), 4W Δ=+0.0029
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*