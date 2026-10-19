#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_outlook.py - data/macro_outlook.md 생성 (Claude 프로젝트 분석 컨텍스트용)

층 구분 (위로 갈수록 사실, 아래로 갈수록 불확실)
  1. 지표      수준·방향·가속도·10년 백분위. 판단 없음
  2. 상태      시장 내재 3축 이진 상태(10년 백분위+히스테리시스). 기존 Fred_regime.py의 2x2 레짐과는 다른 도구
  3. 시나리오  하락/횡보/상승 확률 범위. 근거 = 조건부 분포(순열검정+보정) + 워크포워드 검증 여부
  4. 채점      사전등록 예측의 실제 적중 (표본이 쌓이기 전에는 '표본 부족'이라고 쓴다)

사용법
    python macro/build_outlook.py            # data/macro_outlook.md 갱신
"""
from __future__ import annotations

import math
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import macro_lib as L  # noqa: E402
import conditional_dist as C  # noqa: E402
import checks as K  # noqa: E402
import backtest as B  # noqa: E402
import forecast as F  # noqa: E402

HNAME = {21: "1개월(21영업일)", 63: "3개월(63영업일)"}


def _fmt(x, nd=2):
    return "-" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{x:,.{nd}f}"


def _sgn(x, nd=2, unit=""):
    return "-" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{x:+,.{nd}f}{unit}"


def _chg(known: pd.Series, kind: str, n: int, back: int = 0) -> float:
    """known 시리즈의 (끝-back) 시점 대비 n영업일 변화."""
    if len(known) <= n + back:
        return float("nan")
    cur = known.iloc[-1 - back]
    prev = known.iloc[-1 - back - n]
    if pd.isna(cur) or pd.isna(prev):
        return float("nan")
    return float(np.log(cur / prev) * 100.0) if kind == "pct" else float(cur - prev)


def _pct_label(pan: dict, sid: str) -> str:
    cat = pan["cat"]
    p = pan["pct"][sid].dropna()
    if len(p):
        return f"{p.iloc[-1] * 100:.0f}% (10년)"
    obs = pan["raw"][sid]
    if len(obs) >= 250:                                                    # 이력이 짧은 시리즈는 표본을 명시
        yrs = (obs.index[-1] - obs.index[0]).days / 365.25
        return f"{(obs <= obs.iloc[-1]).mean() * 100:.0f}% (표본 {yrs:.1f}년·참고용)"
    return "-"


def _regime_quote(root: Path) -> str:
    p = root / "data" / "fred_regime.md"
    if not p.exists():
        return "기존 레짐 파일(data/fred_regime.md) 없음"
    t = p.read_text(encoding="utf-8")
    name = re.search(r"^### (.+)$", t.split("## 📊 현재 레짐")[-1], re.M)
    conf = re.search(r"\*\*신뢰도\*\*:\s*([^\n]+)", t)
    g = re.search(r"\*\*성장 점수\*\*:\s*([^\n]+)", t)
    i = re.search(r"\*\*인플레 점수\*\*:\s*([^\n]+)", t)
    return (f"{name.group(1).strip() if name else '?'} · 신뢰도 {conf.group(1).strip() if conf else '?'} · "
            f"성장 {g.group(1).strip() if g else '?'} · 인플레 {i.group(1).strip() if i else '?'}")


def _run_length(s: pd.Series) -> int:
    s = s.dropna()
    if s.empty:
        return 0
    cur, n = s.iloc[-1], 0
    for v in s.iloc[::-1]:
        if v != cur:
            break
        n += 1
    return n


def build(root: Path | None = None, today=None, n_perm: int | None = None) -> str:
    root = root or L.ROOT
    pan = L.build_panel(end=today)
    cat, cfg = pan["cat"], pan["cfg"]
    end = pan["cal"][-1]
    val = B.load_validation(cfg, root)
    chk = K.run_checks(today=end)
    errs = [c for c in chk if c["level"] == "ERROR"]
    warns = [c for c in chk if c["level"] == "WARN"]
    out = []
    w = out.append

    w("# 거시 시장 내재 전망 (macro_outlook)")
    w("")
    w(f"Generated: {end.date()} · 규칙 해시 `{L.config_hash()}` · 자동 생성 파일 (수동 편집 금지)")
    w("")
    w("> 읽는 법: ① 지표는 사실, ② 상태는 규칙 분류, ③ 시나리오는 확률 범위, ④ 채점은 사전등록 예측의 실제 결과다.")
    w("> 시나리오의 기본값은 기저율(약 1/3씩)이며, 워크포워드 검증을 통과한 (대상, 지평)만 신호를 반영한다.")
    w("> CPI 등 개정되는 월간 지표는 발표 시차·개정 때문에 조건부 분포에 쓰지 않는다 (지표 표 표시용 아님 - fred_latest.md 참조).")
    w("")

    # ── 0. 신선도 ──
    w("## 0. 데이터 신선도")
    w("")
    if errs:
        w(f"**[결함 {len(errs)}건]** " + "; ".join(f"{c['series']}: {c['msg']}" for c in errs))
        w("")
    if warns:
        w(f"[경고 {len(warns)}건] " + "; ".join(f"{c['series']}: {c['msg']}" for c in warns))
        w("")
    if not errs and not warns:
        w("결함·경고 없음.")
        w("")

    # ── 1. 지표 ──
    w("## 1. 지표 (수준 · 방향 · 가속도 · 위치)")
    w("")
    w("값은 '알려진 값'(발표 시차 반영) 기준이다. 변화는 diff형은 차이, pct형(환율·유가·지수)은 로그수익률 %다.")
    w("가속 = 최근 3개월 변화 - 그 직전 3개월 변화 (양수면 상승 쪽으로 속도가 붙는 중).")
    w("")
    w("| 지표 | 값 (최종 관측일) | 1개월 | 3개월 | 가속 | 위치 |")
    w("|---|---|---|---|---|---|")
    for sid, r in cat.iterrows():
        if "display" not in L.roles_of(cat, sid):
            continue
        kn = pan["known"][sid]
        raw = pan["raw"][sid]
        if raw.empty:
            w(f"| {r['name_kr']} | 미수집 (데이터 파일 없음) | - | - | - | - |")
            continue
        kind = r["chg"]
        unit = "%" if kind == "pct" else ""
        c1, c3, c3p = _chg(kn, kind, 21), _chg(kn, kind, 63), _chg(kn, kind, 63, back=63)
        acc = c3 - c3p if not (math.isnan(c3) or math.isnan(c3p)) else float("nan")
        lim = " †" if r["known_limit"] else ""
        w(f"| {r['name_kr']}{lim} | {_fmt(float(raw.iloc[-1]))} ({raw.index[-1].date()}) | {_sgn(c1, 2, unit)} | "
          f"{_sgn(c3, 2, unit)} | {_sgn(acc, 2, unit)} | {_pct_label(pan, sid)} |")
    lim_rows = [r for _, r in cat.iterrows() if r["known_limit"]]
    if lim_rows:
        w("")
        w("† " + " / ".join(f"{r['name_kr']}: {r['known_limit']}" for r in lim_rows))
    w("")

    # ── 2. 상태 ──
    w("## 2. 국면")
    w("")
    w(f"- **기존 레짐 (Fred_regime.py, 점수 기반 · 현재 스냅샷)**: {_regime_quote(root)}")
    w("- **시장 내재 상태 (아래, 10년 백분위 · 이력 검증용)**: 개정 없는 시장 일별 시리즈로만 정의해 과거 전 구간에 같은 규칙을 적용할 수 있다.")
    w("  두 도구는 입력이 달라 결론이 다를 수 있다. 다르다는 것 자체가 정보이므로 하나로 합치지 않는다.")
    w("")
    w("| 축 | 현재 상태 | 백분위 | 유지 일수 | 뒤집히는 조건 |")
    w("|---|---|---|---|---|")
    pc = cfg["percentile"]
    for ax, spec in cfg["axes"].items():
        st, ap = pan["axis_state"][ax], pan["axis_pct"][ax]
        cur = st.dropna().iloc[-1] if st.notna().any() else float("nan")
        name = spec["high"] if cur == 1 else spec["low"]
        if len(spec["series"]) == 1:
            sid = spec["series"][0]
            q = pc["hysteresis_lo"] if cur == 1 else pc["hysteresis_hi"]
            lvl = L.level_at_pct(pan["known"][sid], q, pc["window_bdays"])
            move = "아래로 내려가면" if cur == 1 else "위로 올라가면"
            flip = f"{cat.loc[sid, 'name_kr']}: 약 {lvl:,.2f} {move} '{spec['low'] if cur == 1 else spec['high']}'"
        else:
            q = pc["hysteresis_lo"] if cur == 1 else pc["hysteresis_hi"]
            comp = ", ".join(f"{cat.loc[s, 'name_kr']} {pan['pct'][s].dropna().iloc[-1] * 100:.0f}%" for s in spec["series"])
            flip = f"평균 백분위가 {q * 100:.0f}% {'이하로 내려가면' if cur == 1 else '이상으로 올라가면'} 전환 (현재 구성: {comp})"
        w(f"| {spec['label']} | {name} | {ap.dropna().iloc[-1] * 100:.0f}% | {_run_length(st)}영업일 | {flip} |")
    w("")
    w(f"상태 정의 구간: {pan['axis_state'].dropna().index[0].date()} ~ (후행 10년 창, 최소 5년 필요). "
      f"전환은 히스테리시스(상 {pc['hysteresis_hi']:.0%} / 하 {pc['hysteresis_lo']:.0%})를 쓴다.")
    w("")

    # ── 3. 시나리오 ──
    w("## 3. 방향 시나리오 (하락 / 횡보 / 상승)")
    w("")
    w("구간은 과거 전 표본 변화분의 3분위로 정의한다(기저율 약 1/3씩). 확률은 점이 아니라 범위(±10%p)다.")
    w("")
    n_tests = n_pass = 0
    details = []
    for sid in cfg["targets"]:
        kn = pan["known"][sid]
        raw = pan["raw"][sid]
        kind = cat.loc[sid, "chg"]
        unit = "%" if kind == "pct" else ""
        if raw.empty:
            w(f"### {cat.loc[sid, 'name_kr']} ({sid}) - 미수집")
            w("")
            w("데이터 파일이 없어 시나리오를 만들지 않았다 (수집기 실패 여부는 섹션 0 확인).")
            w("")
            continue
        w(f"### {cat.loc[sid, 'name_kr']} ({sid}) - 현재 {_fmt(float(raw.iloc[-1]))} ({raw.index[-1].date()}), 위치 {_pct_label(pan, sid)}")
        w("")
        w("| 지평 | 하락 | 횡보 | 상승 | 구간 경계 | 근거 |")
        w("|---|---|---|---|---|---|")
        notes = []
        for h in cfg["horizons_bdays"]:
            r = C.analyze_target(pan, sid, h, n_perm=n_perm)
            if "error" in r:
                w(f"| {HNAME[h]} | - | - | - | - | {r['error']} |")
                continue
            v = val.get((sid, h))
            validated = bool(v and v["validated"])
            shown = r["prob"] if validated else r["base"]
            rng = [(max(0, p - cfg["probability"]["range_halfwidth"]), min(1, p + cfg["probability"]["range_halfwidth"])) for p in shown]
            lo, hi = r["edges"]
            vtxt = ("검증 이력 없음(`backtest.py --save-summary` 필요)" if v is None else
                    f"워크포워드 BSS {v['bss'] * 100:+.2f}% (z {_fmt(v['z'])}, ~{v['end']})" + (f" - {v['note']}" if v["note"] else ""))
            if validated:
                basis = f"신호 반영: {r['adopted']['name']} · {vtxt}"
            else:
                basis = f"기저율 · 검증된 우위 없음 · {vtxt}"
            w(f"| {HNAME[h]} | {rng[0][0]:.0%}~{rng[0][1]:.0%} | {rng[1][0]:.0%}~{rng[1][1]:.0%} | "
              f"{rng[2][0]:.0%}~{rng[2][1]:.0%} | 하락 < {lo:+.2f}{unit} · 상승 > {hi:+.2f}{unit} | {basis} |")
            if r["adopted"] and not validated:
                notes.append(f"{HNAME[h]}: 표본 내 검정은 '{r['adopted']['name']}'을 통과했으나 워크포워드 검증 미통과 -> 참고만 "
                             f"(모형값 하락 {r['prob'][0]:.0%} / 횡보 {r['prob'][1]:.0%} / 상승 {r['prob'][2]:.0%})")
            for t in r["tests"]:
                if t.get("state") is None:
                    continue
                n_tests += 1
                n_pass += int(t["passes"])
            details.append((sid, h, r))
        w("")
        for n in notes:
            w(f"- {n}")
        if notes:
            w("")
    a_eff = cfg["test"]["family_alpha"] / 5
    exp = n_tests * a_eff
    w(f"전체 검정 {n_tests}건 중 보정 통과 {n_pass}건 (우연히 통과할 기대 건수 약 {exp:.1f}건). "
      + ("통과 건수가 우연 기대치를 크게 넘지만, 같은 대상·조건이 지평만 달라 반복되므로 독립 근거는 이보다 적다. "
         "표본 내 통과가 표본 외 우위를 뜻하지 않으므로 공식 확률은 워크포워드 검증을 따른다."
         if n_pass > 3 * max(exp, 0.5) else
         "통과 건수가 우연 기대치 수준이면 신호가 아니라 노이즈로 본다."))
    w("")
    w("**이 시나리오가 틀리는 조건**: (1) 위 2절의 상태가 뒤집히는 수준을 넘을 때 조건이 달라진다. "
      "(2) 과거 2007~2026에 없던 구조 변화(정책 체제 변경, 신규 쇼크)에는 과거 분포가 정보를 주지 못한다. "
      "(3) 기저율 시나리오는 '방향 예측 없음'을 뜻한다 - 확률이 1/3씩이라는 것은 정보가 없다는 정직한 표현이다.")
    w("")

    # ── 4. 채점 ──
    w("## 4. 사전등록 예측 채점")
    w("")
    log = F.load_log(F.log_path(cfg, root))
    if log.empty:
        w("등록된 예측 없음 (첫 등록은 `forecast.py register`).")
    else:
        res = log[log["status"] == "resolved"]
        w(f"등록 {len(log)}건 · 해소 {len(res)}건 · 대기 {int((log['status'] == 'pending').sum())}건"
          f" · 첫 해소 예정일 {log[log['status'] == 'pending']['resolve_on'].min() if (log['status'] == 'pending').any() else '-'}")
        w("")
        sc = F.score(root, cfg)
        if sc.empty:
            w("해소된 예측이 없어 점수를 낼 수 없다. 표본이 20건 미만이면 점수는 참고용이다.")
        else:
            w("BSS > 0이면 기저율보다 낫다. 공식 = 게이트 적용 확률, 모형 = 게이트 없이 조건부 분포가 낸 확률.")
            w("")
            w("| 대상 | 지평 | n | n_eff | BSS 공식 | BSS 모형 |")
            w("|---|---|---|---|---|---|")
            for _, r in sc.iterrows():
                w(f"| {r['series']} | {int(r['h'])} | {int(r['n'])} | {r['n_eff']} | {r['BSS_공식']:+.4f} | {r['BSS_모형']:+.4f} |")
            w("")
            w("n_eff가 20 미만인 행은 우연과 구분되지 않는다.")
        probs = F.verify(root, cfg)
        w("")
        w(f"로그 무결성: {'통과' if not probs else '결함 ' + '; '.join(probs)}")
    w("")

    # ── 부록 ──
    w("## 부록 A. 조건별 검정 상세 (시나리오 근거)")
    w("")
    w("n_eff = min(n / 지평, 상태 구간 수). p = 환형 시프트 순열검정. 통과 = p <= 보정 alpha 이고 n_eff >= "
      f"{cfg['test']['min_neff']}.")
    w("")
    w("| 대상 | 지평 | 조건 | 현재 상태 | n_eff | 하락/횡보/상승(과거) | p | 통과 |")
    w("|---|---|---|---|---|---|---|---|")
    for sid, h, r in details:
        for t in r["tests"]:
            if t.get("state") is None:
                continue
            pb = t["p_bins"]
            w(f"| {sid} | {h} | {t['name']} | {C.describe_state(pan, t['name'], t['state'])} | {t['n_eff']} | "
              f"{pb[0]:.0%}/{pb[1]:.0%}/{pb[2]:.0%} | {t['p_perm']:.3f} | {'통과' if t['passes'] else ''} |")
    w("")
    w("## 부록 B. 한계")
    w("")
    w("- 한국 일별 지표(국고채 3Y·10Y, KOSPI, 원/달러 매매기준율)는 ECOS에서 수집한다. 월간·분기 한국 지표(CPI, 기준금리, GDP 등)는 개정·발표 시차·표본 수 때문에 조건부 분포에 쓰지 않는다. DEXKOUS(FRED H.10, 발표 시차 8일)와 USDKRW_BOK(ECOS, 시차 1일)은 서로 다른 계열이며 각각 별도 대상이다.")
    w("- 신용 축은 하이일드 OAS(FRED 3년 제한)가 아니라 Baa-10Y 스프레드와 VIX를 쓴다.")
    w("- 발표 일정 달력은 자동화하지 않았다. 다음 발표일은 별도 확인이 필요하다.")
    w("- 과거 분포는 2007~2026 단일 시장 체제의 표본이다. 표본이 작은 상태(구간 수 한 자릿수)는 통계적 의미가 약하다.")
    return "\n".join(out) + "\n"


def main() -> int:
    text = build()
    path = L.DATA_DIR / "macro_outlook.md"
    path.write_text(text, encoding="utf-8")
    print(f"작성: {path.relative_to(L.ROOT)} ({len(text.splitlines())}줄)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
