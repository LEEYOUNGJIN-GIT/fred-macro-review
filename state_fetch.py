#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
국면 상태 계산 (state layer)
──────────────────────────────
expert_view 시장 갱신이 매일 쓰는 시세표와 국면 6개 지표를 같은 방식으로 계산한다.

• 시세: Yahoo chart API(B), Binance(B), 업비트(B)
• 금리·스프레드: FRED CSV(A). 접근이 안 되면 저장소의 data/macro/obs/*.csv(같은 FRED 원자료)로 대체
• 티커 하나가 실패해도 멈추지 않는다. 실패한 값은 N/A로 쓰고 실패 목록을 파일 머리에 적는다
• 핵심 입력(^GSPC, IEF, KRW=X)이 모두 실패하면 exit 1
• 외부 패키지 없이 표준 라이브러리만 쓴다(예약 작업 세션에서 바로 실행하기 위해)

사용: python3 state_fetch.py [--out DIR]   (기본 DIR = ./data)
출력: DIR/state_latest.md, DIR/state_latest.json
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import math
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OBS_DIR = BASE_DIR / "data" / "macro" / "obs"
KST = timezone(timedelta(hours=9))
UA = {"User-Agent": "Mozilla/5.0"}

# (티커, 표시 이름, 통화)  통화가 USD면 원화 기준 일간 변화를 함께 계산한다
YAHOO = [
    ("^GSPC", "S&P500", "USD"),
    ("^IXIC", "나스닥 종합", "USD"),
    ("^NDX", "나스닥100", "USD"),
    ("^SOX", "SOX(반도체)", "USD"),
    ("RSP", "S&P500 동일가중(RSP)", "USD"),
    ("^KS11", "KOSPI", "KRW"),
    ("^KQ11", "KOSDAQ", "KRW"),
    ("005930.KS", "삼성전자", "KRW"),
    ("000660.KS", "SK하이닉스", "KRW"),
    ("^VIX", "VIX", "IDX"),
    ("^VIX3M", "VIX3M", "IDX"),
    ("IEF", "미 7-10년 국채(IEF)", "USD"),
    ("TLT", "미 20년+ 국채(TLT)", "USD"),
    ("HYG", "하이일드(HYG)", "USD"),
    ("VNQ", "미 리츠(VNQ)", "USD"),
    ("SCHD", "미 배당(SCHD)", "USD"),
    ("GLD", "금(GLD)", "USD"),
    ("CL=F", "WTI 근월물", "USD"),
    ("KRW=X", "원/달러", "FX"),
    ("DX-Y.NYB", "달러지수", "IDX"),
    ("BRL=X", "USD/BRL", "FX"),
]
FRED = [
    ("DGS2", "미 2년"), ("DGS10", "미 10년"), ("DGS30", "미 30년"),
    ("DFII10", "미 10년 실질(DFII10)"), ("T10YIE", "10년 기대인플레(T10YIE)"),
    ("BAMLH0A0HYM2", "HY OAS"), ("BAA10Y", "Baa-10Y"), ("VIXCLS", "VIX(FRED)"),
]
CORE = {"^GSPC", "IEF", "KRW=X"}


# ── 수집 ──────────────────────────────────────────────

def _get(url: str, timeout: int = 20, tries: int = 3) -> bytes:
    last = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as exc:  # noqa: BLE001
            last = exc
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(str(last))


def fetch_yahoo(ticker: str) -> tuple[list[tuple[str, float]], dict]:
    """일봉 종가 2년치. 오름차순 [(YYYY-MM-DD, close)]. 마지막 봉은 장중일 수 있다."""
    url = ("https://query2.finance.yahoo.com/v8/finance/chart/"
           + urllib.parse.quote(ticker) + "?range=2y&interval=1d")
    js = json.loads(_get(url))
    res = js["chart"]["result"][0]
    tz = res.get("meta", {}).get("exchangeTimezoneName")
    gmtoff = res.get("meta", {}).get("gmtoffset", 0)
    out = []
    for ts, c in zip(res.get("timestamp") or [], res["indicators"]["quote"][0].get("close") or []):
        if c is None:
            continue
        d = datetime.fromtimestamp(ts + gmtoff, tz=timezone.utc).strftime("%Y-%m-%d")
        if out and out[-1][0] == d:
            out[-1] = (d, float(c))
        else:
            out.append((d, float(c)))
    meta = res.get("meta", {})
    reg = (meta.get("currentTradingPeriod") or {}).get("regular") or {}
    now_ts = time.time()
    today_local = datetime.fromtimestamp(now_ts + gmtoff, tz=timezone.utc).strftime("%Y-%m-%d")
    intraday = bool(out) and out[-1][0] == today_local and reg.get("start", 0) <= now_ts < reg.get("end", 0)
    return out, {"tz": tz, "intraday": intraday}


_FRED_DOWN = False


def fetch_fred(sid: str) -> tuple[list[tuple[str, float]], str]:
    """FRED CSV. 실패하면 저장소 data/macro/obs/<sid>.csv로 대체. (관측, 출처표기)
    첫 실패 뒤에는 원격을 다시 시도하지 않는다(접근 차단 환경에서 시간 낭비 방지)."""
    global _FRED_DOWN
    try:
        if _FRED_DOWN:
            raise RuntimeError("FRED 접근 불가")
        raw = _get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}", timeout=15, tries=2).decode()
        src = "FRED CSV"
    except Exception:  # noqa: BLE001
        _FRED_DOWN = True
        p = OBS_DIR / f"{sid}.csv"
        if not p.exists():
            return [], "N/A"
        raw = p.read_text(encoding="utf-8")
        src = "FRED(저장소 사본)"
    rows = []
    for r in csv.DictReader(io.StringIO(raw)):
        keys = list(r.keys())
        d, v = r[keys[0]], r[keys[1]]
        try:
            rows.append((d, float(v)))
        except (TypeError, ValueError):
            continue
    rows.sort()
    return rows, src


def fetch_crypto() -> dict:
    out = {}
    try:
        k = json.loads(_get("https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=400"))
        closes = [(datetime.fromtimestamp(x[0] / 1000, tz=timezone.utc).strftime("%Y-%m-%d"), float(x[4])) for x in k[:-1]]
        flag, thr = tail_flag(closes)
        out["btc_tail_1pct"], out["btc_tail_thr"] = flag, thr
        out["btc_prev_chg"] = ret_n(closes, 1)
        out["btc_prev_close"] = float(k[-2][4])
        out["btc_last"] = float(k[-1][4])
        out["btc_prev_date"] = datetime.fromtimestamp(k[-2][0] / 1000, tz=timezone.utc).strftime("%Y-%m-%d")
    except Exception as exc:  # noqa: BLE001
        out["btc_error"] = str(exc)[:80]
    try:
        t = json.loads(_get("https://api.upbit.com/v1/ticker?markets=KRW-USDT,KRW-BTC"))
        for x in t:
            out[x["market"]] = float(x["trade_price"])
    except Exception as exc:  # noqa: BLE001
        out["upbit_error"] = str(exc)[:80]
    return out


# ── 계산 ──────────────────────────────────────────────

def pct(a, b):
    return None if a is None or b in (None, 0) else (a / b - 1) * 100


def ret_n(s, n):
    return pct(s[-1][1], s[-1 - n][1]) if len(s) > n else None


def diff_n(s, n):
    return s[-1][1] - s[-1 - n][1] if len(s) > n else None


def daily_returns(s):
    return {s[i][0]: s[i][1] / s[i - 1][1] - 1 for i in range(1, len(s)) if s[i - 1][1]}


def corr(xs, ys):
    n = len(xs)
    if n < 10:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    sx = math.sqrt(sum((a - mx) ** 2 for a in xs))
    sy = math.sqrt(sum((b - my) ** 2 for b in ys))
    return None if sx == 0 or sy == 0 else sxy / (sx * sy)


def percentile_rank(values, v):
    return None if not values else sum(1 for x in values if x <= v) / len(values) * 100


def tail_flag(s, window=252):
    """마지막 일간 변화의 절댓값이 직전 1년 분포의 상위 1%인가."""
    if len(s) < window + 2:
        return None, None
    ch = [abs(s[i][1] / s[i - 1][1] - 1) for i in range(len(s) - window - 1, len(s) - 1)]
    thr = sorted(ch)[int(len(ch) * 0.99) - 1]
    last = abs(s[-1][1] / s[-2][1] - 1)
    return last > thr, thr * 100


def tail_flag_level(s, window=252):
    """수준 변화(VIX pt, OAS %p) 기준 상위 1%."""
    if len(s) < window + 2:
        return None, None
    ch = [abs(s[i][1] - s[i - 1][1]) for i in range(len(s) - window - 1, len(s) - 1)]
    thr = sorted(ch)[int(len(ch) * 0.99) - 1]
    return abs(s[-1][1] - s[-2][1]) > thr, thr


def sma(s, n):
    return sum(v for _, v in s[-n:]) / n if len(s) >= n else None


def fmt(v, nd=2, sign=False, unit=""):
    if v is None:
        return "N/A"
    return (f"{v:+,.{nd}f}" if sign else f"{v:,.{nd}f}") + unit


def build(out_dir: Path) -> int:
    now = datetime.now(KST)
    y, ymeta, failed = {}, {}, []
    for t, _, _ in YAHOO:
        try:
            y[t], ymeta[t] = fetch_yahoo(t)
            if len(y[t]) < 30:
                raise RuntimeError("관측 부족")
        except Exception as exc:  # noqa: BLE001
            y.pop(t, None)
            failed.append(f"{t}({str(exc)[:40]})")
    f, fsrc = {}, {}
    for sid, _ in FRED:
        f[sid], fsrc[sid] = fetch_fred(sid)
        if not f[sid]:
            failed.append(f"FRED {sid}")
    crypto = fetch_crypto()

    if all(c not in y for c in CORE):
        print("::error::핵심 입력(^GSPC, IEF, KRW=X) 전부 실패")
        return 1

    fx = y.get("KRW=X")
    fx_ret = daily_returns(fx) if fx else {}

    # 시세표
    rows = []
    for t, name, cur in YAHOO:
        s = y.get(t)
        if not s:
            rows.append({"ticker": t, "name": name, "value": None})
            continue
        r1 = ret_n(s, 1)
        krw = None
        if cur == "USD" and r1 is not None and s[-1][0] in fx_ret:
            krw = ((1 + r1 / 100) * (1 + fx_ret[s[-1][0]]) - 1) * 100
        flag, thr = tail_flag(s) if t in ("^GSPC", "^IXIC", "^KS11", "KRW=X", "BRL=X") else (None, None)
        if t == "^VIX":
            flag, thr = tail_flag_level(s)
        rows.append({
            "ticker": t, "name": name, "value": s[-1][1], "date": s[-1][0],
            "prev_date": s[-2][0] if len(s) > 1 else None,
            "chg_1d": (diff_n(s, 1) if t in ("^VIX", "^VIX3M") else r1),
            "chg_unit": "pt" if t in ("^VIX", "^VIX3M") else "%",
            "chg_1d_krw": krw, "ret_20d": ret_n(s, 20), "ret_63d": ret_n(s, 63),
            "tail_1pct": flag, "tail_thr": thr,
            "intraday": ymeta.get(t, {}).get("intraday", False),
        })
    frows = []
    for sid, name in FRED:
        s = f.get(sid) or []
        if not s:
            frows.append({"id": sid, "name": name, "value": None})
            continue
        flag, thr = tail_flag_level(s) if sid in ("BAMLH0A0HYM2", "DGS10") else (None, None)
        frows.append({"id": sid, "name": name, "value": s[-1][1], "date": s[-1][0],
                      "chg_1d": diff_n(s, 1), "chg_21": diff_n(s, 21), "chg_63": diff_n(s, 63),
                      "src": fsrc[sid], "tail_1pct": flag, "tail_thr": thr})

    # 국면 6개
    st = {}
    sp, ief = y.get("^GSPC"), y.get("IEF")
    if sp and ief:
        rs, ri = daily_returns(sp), daily_returns(ief)
        common = sorted(set(rs) & set(ri))[-63:]
        st["corr63"] = corr([rs[d] for d in common], [ri[d] for d in common])
        st["corr63_date"] = common[-1] if common else None
    if sp and y.get("RSP"):
        st["sp_rsp_20"] = (ret_n(sp, 20) or 0) - (ret_n(y["RSP"], 20) or 0)
        st["sp_rsp_63"] = (ret_n(sp, 63) or 0) - (ret_n(y["RSP"], 63) or 0)
    if sp and y.get("^SOX"):
        st["sox_sp_20"] = (ret_n(y["^SOX"], 20) or 0) - (ret_n(sp, 20) or 0)
        st["sox_sp_63"] = (ret_n(y["^SOX"], 63) or 0) - (ret_n(sp, 63) or 0)
    d10 = f.get("DFII10") or []
    if d10:
        cut = (datetime.strptime(d10[-1][0], "%Y-%m-%d") - timedelta(days=3652)).strftime("%Y-%m-%d")
        hist = [v for d, v in d10 if d >= cut]
        st["dfii10_pctile_10y"] = percentile_rank(hist, d10[-1][1])
        st["dfii10_hist_from"] = next((d for d, _ in d10 if d >= cut), None)
    vix = y.get("^VIX")
    if vix:
        st["vix_pctile_1y"] = percentile_rank([v for _, v in vix[-252:]], vix[-1][1])
    if vix and y.get("^VIX3M"):
        st["vix_minus_vix3m"] = vix[-1][1] - y["^VIX3M"][-1][1]
    for t, k in (("^GSPC", "sp"), ("^KS11", "kospi"), ("^IXIC", "ixic")):
        s = y.get(t)
        if s and len(s) >= 200:
            hi = max(v for _, v in s[-252:])
            st[f"{k}_dd_252"] = pct(s[-1][1], hi)
            st[f"{k}_vs_200dma"] = pct(s[-1][1], sma(s, 200))
    if fx:
        st["krw_1w"], st["krw_1m"], st["krw_3m"] = ret_n(fx, 5), ret_n(fx, 21), ret_n(fx, 63)
    if y.get("DX-Y.NYB"):
        st["dxy_1m"], st["dxy_3m"] = ret_n(y["DX-Y.NYB"], 21), ret_n(y["DX-Y.NYB"], 63)
    if y.get("HYG"):
        st["hyg_1m"], st["hyg_3m"] = ret_n(y["HYG"], 21), ret_n(y["HYG"], 63)
    if fx and "KRW-USDT" in crypto:
        st["usdt_premium"] = pct(crypto["KRW-USDT"], fx[-1][1])

    payload = {"generated_kst": now.strftime("%Y-%m-%d %H:%M"), "failed": failed,
               "prices": rows, "fred": frows, "state": st, "crypto": crypto}
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "state_latest.json").write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    (out_dir / "state_latest.md").write_text(render_md(payload), encoding="utf-8")
    print(f"state_latest 작성: 실패 {len(failed)}건 {failed}")
    return 0


def render_md(p: dict) -> str:
    st = p["state"]
    L = ["# 국면 상태 (state layer)\n",
         f"생성: {p['generated_kst']} KST | 시세 Yahoo·Binance·업비트(B), 금리·스프레드 FRED(A)",
         "값 옆 (장중)은 정규장이 진행 중인 미확정 값이다. 원화 기준 변화는 같은 날짜의 KRW=X 일간 변화로 근사한다.",
         f"실패: {', '.join(p['failed']) if p['failed'] else '없음'}\n",
         "## 국면 6개\n",
         "| 국면 | 지표 | 값 |", "| --- | --- | --- |",
         f"| 1. 주식-채권 상관 | S&P500·IEF 일간수익률 63거래일 상관 | {fmt(st.get('corr63'))} ({st.get('corr63_date') or '-'}) |",
         f"| 2. 쏠림 | S&P500-RSP 상대수익 20일 / 63일 | {fmt(st.get('sp_rsp_20'), sign=True, unit='%p')} / {fmt(st.get('sp_rsp_63'), sign=True, unit='%p')} |",
         f"| 2. 쏠림 | SOX-S&P500 상대수익 20일 / 63일 | {fmt(st.get('sox_sp_20'), sign=True, unit='%p')} / {fmt(st.get('sox_sp_63'), sign=True, unit='%p')} |",
         f"| 3. 실질금리 | DFII10 10년 백분위 (표본 시작 {st.get('dfii10_hist_from') or '-'}) | {fmt(st.get('dfii10_pctile_10y'), 0, unit='%')} |",
         f"| 4. 신용 | HYG 1개월 / 3개월 | {fmt(st.get('hyg_1m'), sign=True, unit='%')} / {fmt(st.get('hyg_3m'), sign=True, unit='%')} |",
         f"| 5. 변동성 | VIX 1년 백분위 / VIX-VIX3M | {fmt(st.get('vix_pctile_1y'), 0, unit='%')} / {fmt(st.get('vix_minus_vix3m'), sign=True)} (양수=역전) |",
         f"| 5. 추세 | S&P500 252일 고점 대비 / 200일선 대비 | {fmt(st.get('sp_dd_252'), 1, unit='%')} / {fmt(st.get('sp_vs_200dma'), 1, sign=True, unit='%')} |",
         f"| 5. 추세 | 나스닥 종합 252일 고점 대비 / 200일선 대비 | {fmt(st.get('ixic_dd_252'), 1, unit='%')} / {fmt(st.get('ixic_vs_200dma'), 1, sign=True, unit='%')} |",
         f"| 5. 추세 | KOSPI 252일 고점 대비 / 200일선 대비 | {fmt(st.get('kospi_dd_252'), 1, unit='%')} / {fmt(st.get('kospi_vs_200dma'), 1, sign=True, unit='%')} |",
         f"| 6. 원화 | 원/달러 1주 / 1개월 / 3개월 (+는 원화 약세) | {fmt(st.get('krw_1w'), sign=True, unit='%')} / {fmt(st.get('krw_1m'), sign=True, unit='%')} / {fmt(st.get('krw_3m'), sign=True, unit='%')} |",
         f"| 6. 원화 | 달러지수 1개월 / 3개월 | {fmt(st.get('dxy_1m'), sign=True, unit='%')} / {fmt(st.get('dxy_3m'), sign=True, unit='%')} |",
         "\n## 시세표\n",
         "| 항목 | 값 | 기준일 | 일간 | 원화 기준 일간 | 20일 | 63일 | 1년 상위 1% 변동 |",
         "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for r in p["prices"]:
        if r.get("value") is None:
            L.append(f"| {r['name']} | N/A | - | - | - | - | - | - |")
            continue
        tail = "-" if r["tail_1pct"] is None else (f"예(경계 {r['tail_thr']:.2f})" if r["tail_1pct"] else "아니오")
        st_mark = " (장중)" if r.get("intraday") else ""
        L.append(f"| {r['name']} | {fmt(r['value'])}{st_mark} | {r['date']} | {fmt(r['chg_1d'], sign=True, unit=r['chg_unit'])} "
                 f"| {fmt(r['chg_1d_krw'], sign=True, unit='%')} | {fmt(r['ret_20d'], 1, sign=True, unit='%')} "
                 f"| {fmt(r['ret_63d'], 1, sign=True, unit='%')} | {tail} |")
    L += ["\n## 금리·스프레드 (FRED)\n",
          "| 항목 | 값 | 기준일 | 전일 | 1개월(21관측) | 3개월(63관측) | 출처 | 1년 상위 1% 변동 |",
          "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for r in p["fred"]:
        if r.get("value") is None:
            L.append(f"| {r['name']} | N/A | - | - | - | - | - | - |")
            continue
        tail = "-" if r["tail_1pct"] is None else (f"예(경계 {r['tail_thr']:.2f})" if r["tail_1pct"] else "아니오")
        L.append(f"| {r['name']} | {fmt(r['value'])} | {r['date']} | {fmt(r['chg_1d'], sign=True)} "
                 f"| {fmt(r['chg_21'], sign=True)} | {fmt(r['chg_63'], sign=True)} | {r['src']} | {tail} |")
    c = p["crypto"]
    L += ["\n## 디지털자산\n",
          f"- BTC/USDT 전일 확정 종가 {fmt(c.get('btc_prev_close'), 0)} ({c.get('btc_prev_date', '-')}, 일간 {fmt(c.get('btc_prev_chg'), sign=True, unit='%')}, "
          f"1년 상위 1% 변동 {'-' if c.get('btc_tail_1pct') is None else ('예' if c['btc_tail_1pct'] else '아니오')}), 현재 {fmt(c.get('btc_last'), 0)} (Binance, UTC 일봉)",
          f"- 업비트 KRW-BTC {fmt(c.get('KRW-BTC'), 0)}, KRW-USDT {fmt(c.get('KRW-USDT'), 0)}",
          f"- 테더 원화 프리미엄(업비트 KRW-USDT / Yahoo 원/달러) {fmt(st.get('usdt_premium'), sign=True, unit='%')}"]
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(BASE_DIR / "data"))
    sys.exit(build(Path(ap.parse_args().out)))
