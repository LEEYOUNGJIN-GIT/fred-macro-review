# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-09-08 (oldest: 2026-07-17 ^VIX3M)
> ⚠ **Stale**: oldest data is 52d old (>5d) — fetch may be failing
> Generated: 2026-09-07 23:13:54 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 57.5000 | KOSPI YoY=+111.04%, KOSDAQ YoY=+3.96%, KOSPI 4W=+6.21% |
| 2 | Breadth | 🔵 중립 | 0.2843 | RSP/SPY=0.2843 (Ratio, 무차원), 4W Δ=-0.0003 |
| 3 | Risk-on/off | 🟢 risk-on | 1.9853 | SPHB/SPLV=1.9853 (Ratio, 무차원), 4W Δ=+0.0409 |
| 4 | VIX Term | 🟢 contango | 0.6972 | VIX3M=20.54, VIX/VIX3M=0.6972 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.08 |
| 5 | 섹터 로테이션 | 🟠 경계 | -11.7800 | XLK 4W=-0.37%, XLE 4W=+11.41%, XLK-XLE=-11.78%p, XLP 4W=-0.63% |
| 6 | 신용 방향 | 🔵 중립 | 0.7505 | HYG/LQD=0.7505 (Ratio, OAS 아님), 4W Δ=+0.0043 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 57.5
- **상세**: KOSPI YoY=+111.04%, KOSDAQ YoY=+3.96%, KOSPI 4W=+6.21%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.284345
- **상세**: RSP/SPY=0.2843 (Ratio, 무차원), 4W Δ=-0.0003
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.985282
- **상세**: SPHB/SPLV=1.9853 (Ratio, 무차원), 4W Δ=+0.0409
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.6972
- **상세**: VIX3M=20.54, VIX/VIX3M=0.6972 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-0.08
- **시리즈**: ^VIX3M, VIXCLS

### 🟠 섹터 로테이션 — 경계
- **값**: -11.78
- **상세**: XLK 4W=-0.37%, XLE 4W=+11.41%, XLK-XLE=-11.78%p, XLP 4W=-0.63%
- **시리즈**: XLK, XLE, XLP

### 🔵 신용 방향 — 중립
- **값**: 0.750474
- **상세**: HYG/LQD=0.7505 (Ratio, OAS 아님), 4W Δ=+0.0043
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*