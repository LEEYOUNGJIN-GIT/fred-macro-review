# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-09-22 (oldest: 2026-09-18 ^KS11)
> Freshness: OK (oldest 3d ≤ 5d)
> Generated: 2026-09-21 23:45:21 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 58.5200 | KOSPI YoY=+115.10%, KOSDAQ YoY=+1.94%, KOSPI 4W=-0.27% |
| 2 | Breadth | 🔵 중립 | 0.2750 | RSP/SPY=0.2750 (Ratio, 무차원), 4W Δ=-0.0153, 4W 하락=대형주 쏠림 |
| 3 | Risk-on/off | 🟢 강한 risk-on | 2.0998 | SPHB/SPLV=2.0998 (Ratio, 무차원), 4W Δ=+0.1240 |
| 4 | VIX Term | 🟢 contango | 0.8540 | VIX3M=18.08, VIX/VIX3M=0.8540 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.42 |
| 5 | 섹터 로테이션 | 🟢 확장 | 8.1500 | XLK 4W=+6.30%, XLE 4W=-1.85%, XLK-XLE=+8.15%p, XLP 4W=-4.73% |
| 6 | 신용 방향 | 🔵 중립 | 0.7487 | HYG/LQD=0.7487 (Ratio, OAS 아님), 4W Δ=-0.0020 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 58.52
- **상세**: KOSPI YoY=+115.10%, KOSDAQ YoY=+1.94%, KOSPI 4W=-0.27%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.274958
- **상세**: RSP/SPY=0.2750 (Ratio, 무차원), 4W Δ=-0.0153, 4W 하락=대형주 쏠림
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — 강한 risk-on
- **값**: 2.099751
- **상세**: SPHB/SPLV=2.0998 (Ratio, 무차원), 4W Δ=+0.1240
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.854
- **상세**: VIX3M=18.08, VIX/VIX3M=0.8540 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.42
- **시리즈**: ^VIX3M, VIXCLS

### 🟢 섹터 로테이션 — 확장
- **값**: 8.15
- **상세**: XLK 4W=+6.30%, XLE 4W=-1.85%, XLK-XLE=+8.15%p, XLP 4W=-4.73%
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.748692
- **상세**: HYG/LQD=0.7487 (Ratio, OAS 아님), 4W Δ=-0.0020
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*