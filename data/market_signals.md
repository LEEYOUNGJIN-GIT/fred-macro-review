# Market 보조 신호 대시보드

> **보조지표 신호 — fred_signals.md / fred_regime.md의 보완**
> - 공식 매크로 신호 18개·2x2 레짐: FRED 레이어만 사용
> - Ratio 신호: 무차원, 전기/YoY 방향만 해석 (절대값 기준 없음)
> - market_fetch 실패 시 본 파일 갱신 없음
> Data as-of: 2026-09-02 (oldest: 2026-09-01 ^KS11)
> Freshness: OK (oldest 1d ≤ 5d)
> Generated: 2026-09-02 22:55:58 UTC

## 신호 요약

| # | 신호 | 상태 | 값 | 핵심 요약 |
|---|------|------|-----|----------|
| 1 | 한국 주식 | 🟢 견조 | 59.0300 | KOSPI YoY=+115.15%, KOSDAQ YoY=+2.91%, KOSPI 4W=+3.64% |
| 2 | Breadth | 🔵 중립 | 0.2857 | RSP/SPY=0.2857 (Ratio, 무차원), 4W Δ=+0.0002 |
| 3 | Risk-on/off | 🟢 risk-on | 1.9330 | SPHB/SPLV=1.9330 (Ratio, 무차원), 4W Δ=-0.0210 |
| 4 | VIX Term | 🟢 contango | 0.8415 | VIX3M=17.73, VIX/VIX3M=0.8415 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-1.84 |
| 5 | 섹터 로테이션 | 🟠 경계 | -15.3600 | XLK 4W=-1.77%, XLE 4W=+13.59%, XLK-XLE=-15.36%p, XLP 4W=+0.19%, 방어(XLP) > 기술 → risk-off 로테이션 |
| 6 | 신용 방향 | 🟢 완화 | 0.7509 | HYG/LQD=0.7509 (Ratio, OAS 아님), 4W Δ=+0.0067 |

## 신호 상세

### 🟢 한국 주식 — 견조
- **값**: 59.03
- **상세**: KOSPI YoY=+115.15%, KOSDAQ YoY=+2.91%, KOSPI 4W=+3.64%
- **시리즈**: ^KS11, ^KQ11

### 🔵 Breadth — 중립
- **값**: 0.285692
- **상세**: RSP/SPY=0.2857 (Ratio, 무차원), 4W Δ=+0.0002
- **시리즈**: MARKET_BREADTH, RSP, SPY

### 🟢 Risk-on/off — risk-on
- **값**: 1.93303
- **상세**: SPHB/SPLV=1.9330 (Ratio, 무차원), 4W Δ=-0.0210
- **시리즈**: MARKET_RISK_ON, SPHB, SPLV

### 🟢 VIX Term — contango
- **값**: 0.8415
- **상세**: VIX3M=17.73, VIX/VIX3M=0.8415 (FRED VIXCLS/^VIX3M), VIX3M 4W Δ=-1.84
- **시리즈**: ^VIX3M, VIXCLS

### 🟠 섹터 로테이션 — 경계
- **값**: -15.36
- **상세**: XLK 4W=-1.77%, XLE 4W=+13.59%, XLK-XLE=-15.36%p, XLP 4W=+0.19%, 방어(XLP) > 기술 → risk-off 로테이션
- **시리즈**: XLK, XLE, XLP

### 🟢 신용 방향 — 완화
- **값**: 0.750926
- **상세**: HYG/LQD=0.7509 (Ratio, OAS 아님), 4W Δ=+0.0067
- **시리즈**: HYG_LQD_RATIO, HYG, LQD

---
*Market Layer v1 — 보조 신호 6개. 공식 거시: fred_signals.md*