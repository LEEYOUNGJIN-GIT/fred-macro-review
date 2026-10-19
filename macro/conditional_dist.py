#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
conditional_dist.py - 조건부 분포(3층): "지금과 같은 상태였던 과거에 이 지표는 이후 어떻게 움직였나"

핵심은 계산이 아니라 '정직하게 구분 불가라고 말하는 것'이다.
  - 겹치는 창(지평 63영업일을 매일 다시 잼)과 상태의 지속성 때문에 표본 수가 부풀려져 보인다.
    -> 유효 표본 n_eff = min(n/지평, 상태 구간 수)
  - 유의성은 환형 시프트 순열검정: 상태 라벨 전체를 무작위로 밀어(자기상관 보존) 만든 귀무분포와 비교
  - 조건을 여러 개 검정하면 우연히 유의한 것이 나온다 -> Bonferroni (alpha / 조건 수)
  - 보정을 통과하지 못하면 확률은 기저율(전체 표본 3분위 = 약 1/3씩)로 되돌린다
  - 보정을 통과해도 n_eff에 따라 기저율 쪽으로 수축: w = n_eff / (n_eff + K)

조건 5종(대상 지표마다): 축 3개 각각 / 대상 자신의 수준(평균회귀) / 3축 결합 셀
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import macro_lib as L  # noqa: E402

BIN_LABELS = ["하락", "횡보", "상승"]


def _episodes(mask: np.ndarray) -> int:
    """True가 이어진 구간(연속 run)의 개수."""
    if not mask.any():
        return 0
    return int(mask[0]) + int((mask[1:] & ~mask[:-1]).sum())


def perm_pvalue(mask: np.ndarray, rank: np.ndarray, h: int, n_perm: int, rng) -> float:
    """상태 라벨을 환형으로 밀어 만든 귀무분포 대비 |조건부 평균순위 - 0.5|의 양측 p값."""
    n = len(mask)
    if mask.sum() == 0 or mask.sum() == n:
        return float("nan")
    stat = abs(rank[mask].mean() - 0.5)
    lo, hi = max(h, 1), max(n - h, h + 1)       # 너무 작은 이동은 원 라벨과 거의 같아 제외
    shifts = rng.integers(lo, hi, size=n_perm)
    ge = 0
    for k in shifts:
        m = np.roll(mask, int(k))
        if abs(rank[m].mean() - 0.5) >= stat - 1e-12:
            ge += 1
    return (ge + 1) / (n_perm + 1)


def analyze_target(panel: dict, sid: str, h: int, n_perm: int | None = None, seed: int | None = None,
                   asof=None) -> dict:
    """asof를 주면 그 시점까지 알 수 있었던 정보만으로 분석한다(백테스트용).
    패널의 상태·백분위·known 값은 모두 인과적(과거만 사용)이므로 전체 패널을 잘라 써도 같은 결과다
    (tests/test_macro.py의 절단 불변성 테스트가 보증). 단 fwd는 미래 값을 쓰므로
    asof 이후에 결과가 확정되는 마지막 h행은 반드시 비운다."""
    cfg, cat = panel["cfg"], panel["cat"]
    tcfg, pcfg, perc = cfg["test"], cfg["probability"], cfg["percentile"]
    n_perm = n_perm or tcfg["n_perm"]
    order = list(cfg["axes"].keys())
    known = panel["known"][sid]
    fwd = L.forward_change(known, cat.loc[sid, "chg"], h)

    # 조건 후보: 상태 시리즈들 (달력 전체 길이)
    conds = {f"축:{cfg['axes'][ax]['label']}": panel["axis_state"][ax] for ax in order}
    # 대상이 어떤 축의 유일한 구성 시리즈면 '자기수준'은 그 축과 같은 검정이다 -> 중복 제거(보정이 부당하게 엄격해진다)
    if not any(spec["series"] == [sid] for spec in cfg["axes"].values()):
        conds["자기수준"] = L.hysteresis(panel["pct"][sid], perc["hysteresis_lo"], perc["hysteresis_hi"])
    conds["3축결합"] = L.cell_code(panel["axis_state"], order)

    frame = pd.DataFrame({"fwd": fwd, **conds})
    if asof is not None:
        frame = frame.loc[:pd.Timestamp(asof)].copy()
        frame.iloc[-h:, frame.columns.get_loc("fwd")] = np.nan     # 결과가 asof 이후에 확정되는 행
    current = frame[list(conds)].iloc[-1]                   # 가장 최근 달력일의 상태 (fwd는 아직 미정)
    sample = frame.dropna()                                  # 모든 조건이 동시에 정의된 공통 표본
    out = {"series": sid, "horizon": h, "n_sample": int(len(sample)), "tests": [], "adopted": None,
           "asof": str(frame.index[-1].date())}
    if len(sample) < 500:
        out["error"] = f"공통 표본 {len(sample)}일 - 분석 불가"
        return out

    lo_e, hi_e = sample["fwd"].quantile([1 / 3, 2 / 3])
    out["edges"] = (float(lo_e), float(hi_e))
    fv = sample["fwd"].to_numpy()
    base = np.array([(fv < lo_e).mean(), ((fv >= lo_e) & (fv <= hi_e)).mean(), (fv > hi_e).mean()])
    out["base"] = base.tolist()
    rank = sample["fwd"].rank(pct=True).to_numpy()
    rng = np.random.default_rng(seed if seed is not None else 1000 + h)

    m_family = len(conds)
    alpha = tcfg["family_alpha"] / m_family
    out["alpha_corrected"] = alpha
    for name in conds:
        cur = current[name]
        if pd.isna(cur):
            out["tests"].append({"name": name, "state": None, "note": "현재 상태 미정"})
            continue
        mask = (sample[name] == cur).to_numpy()
        n = int(mask.sum())
        epi = _episodes(mask)
        n_eff = min(n / h, epi)
        cond_fv = fv[mask]
        pb = np.array([(cond_fv < lo_e).mean(), ((cond_fv >= lo_e) & (cond_fv <= hi_e)).mean(),
                       (cond_fv > hi_e).mean()]) if n else base
        p = perm_pvalue(mask, rank, h, n_perm, rng)
        out["tests"].append({
            "name": name, "state": float(cur), "n": n, "episodes": epi, "n_eff": round(float(n_eff), 1),
            "p_bins": pb.tolist(), "rank_mean": float(rank[mask].mean()) if n else float("nan"),
            "p_perm": float(p), "passes": bool(p <= alpha and n_eff >= tcfg["min_neff"]),
        })

    passed = [t for t in out["tests"] if t.get("passes")]
    if passed:
        best = min(passed, key=lambda t: t["p_perm"])
        w = best["n_eff"] / (best["n_eff"] + pcfg["shrink_k"])
        prob = base + w * (np.array(best["p_bins"]) - base)
        out["adopted"] = {"name": best["name"], "weight": float(w)}
    else:
        prob = base
    hw = pcfg["range_halfwidth"]
    out["prob"] = prob.tolist()
    out["prob_range"] = [(float(max(0, x - hw)), float(min(1, x + hw))) for x in prob]
    return out


def describe_state(panel: dict, name: str, state: float | None) -> str:
    if state is None or pd.isna(state):
        return "미정"
    cfg = panel["cfg"]
    for ax, spec in cfg["axes"].items():
        if name == f"축:{spec['label']}":
            return spec["high"] if state == 1 else spec["low"]
    if name == "자기수준":
        return "자기 10년 분포 상위" if state == 1 else "자기 10년 분포 하위"
    if name == "3축결합":
        order = list(cfg["axes"].keys())
        bits = [int(state) >> (len(order) - 1 - i) & 1 for i in range(len(order))]
        return " / ".join(cfg["axes"][ax]["high" if b else "low"] for ax, b in zip(order, bits))
    return str(state)


if __name__ == "__main__":
    pan = L.build_panel()
    for sid in pan["cfg"]["targets"]:
        for h in pan["cfg"]["horizons_bdays"]:
            r = analyze_target(pan, sid, h)
            print(sid, h, "표본", r["n_sample"], "채택", r["adopted"], "확률",
                  [round(x, 2) for x in r.get("prob", [])])
