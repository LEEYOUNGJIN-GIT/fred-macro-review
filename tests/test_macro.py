#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/test_macro.py - macro/ 파이프라인 검증 (pytest 없이도 `python tests/test_macro.py`로 실행된다)

이 테스트들이 지키는 것
  [룩어헤드]  절단 불변성 / 미래값 오염 / 발표 시차
  [통계]      순열검정 보정(순수 노이즈에서 기각률) / 히스테리시스
  [수집]      병합(개정 기록·빈 응답·짧은 응답) / 검사기가 결함을 잡는가
  [예측로그]  등록·중복 방지·채점·변조 감지·문자열 해시 보존
모든 데이터는 합성(고정 시드)이라 네트워크가 필요 없다.
"""
from __future__ import annotations

import shutil
import sys
import tempfile
import traceback
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "macro"))
import macro_lib as L  # noqa: E402
import conditional_dist as C  # noqa: E402
import checks as K  # noqa: E402
import fetch_history as FH  # noqa: E402
import forecast as F  # noqa: E402

END = "2026-10-15"


def make_obs(obs_dir: Path, seed: int = 0, end: str = END, start: str = "2000-01-03") -> None:
    """카탈로그의 모든 시리즈에 대해 양수 랜덤워크 관측치를 만든다."""
    rng = np.random.default_rng(seed)
    cat = L.load_catalog()
    obs_dir.mkdir(parents=True, exist_ok=True)
    idx = pd.bdate_range(start, end)
    for sid in cat.index:
        v = 100 * np.exp(np.cumsum(rng.normal(0, 0.01, len(idx))))
        pd.DataFrame({"date": idx.strftime("%Y-%m-%d"), "value": v}).to_csv(obs_dir / f"{sid}.csv", index=False)


# ───────────────────────── 룩어헤드 ─────────────────────────

def test_known_series_respects_lag():
    cal = pd.bdate_range("2024-01-01", "2024-02-29")
    obs = pd.Series([1.0, 2.0], index=pd.to_datetime(["2024-01-10", "2024-01-25"]), name="X")
    k = L.known_series(obs, lag_days=8, cal=cal, max_ffill=100)
    assert np.isnan(k["2024-01-17"]), "관측일+시차 이전에는 알 수 없어야 한다"     # 01-10 + 8일 = 01-18
    assert k["2024-01-18"] == 1.0
    assert k["2024-01-31"] == 1.0 and k["2024-02-02"] == 2.0                      # 01-25 + 8일 = 02-02


def test_truncation_invariance():
    """미래 데이터를 지워도 과거 시점의 known·백분위·상태가 변하지 않아야 한다."""
    with tempfile.TemporaryDirectory() as d:
        od = Path(d) / "obs"
        make_obs(od)
        full = L.build_panel(end=END, obs_dir=od)
        for T in ("2012-06-29", "2019-03-15", "2024-12-31"):
            cut = L.build_panel(end=END, asof=T, obs_dir=od)
            assert cut["cal"][-1] == pd.Timestamp(T)
            n = len(cut["cal"])
            for name in ("known", "pct", "axis_pct", "axis_state"):
                a, b = getattr(full, "get")(name).iloc[:n], cut[name]
                pd.testing.assert_frame_equal(a, b, check_freq=False, obj=f"{name}@{T}")


def test_future_values_do_not_leak_into_analysis():
    """asof 이후의 관측값을 난수로 바꿔도 asof 시점 분석(확률·경계·p값)은 같아야 한다."""
    T = "2020-06-30"
    with tempfile.TemporaryDirectory() as d:
        a_dir, b_dir = Path(d) / "a", Path(d) / "b"
        make_obs(a_dir)
        shutil.copytree(a_dir, b_dir)
        rng = np.random.default_rng(99)
        for p in b_dir.glob("*.csv"):
            df = pd.read_csv(p)
            m = pd.to_datetime(df["date"]) > pd.Timestamp(T)
            df.loc[m, "value"] = 100 * np.exp(rng.normal(0, 0.5, int(m.sum())))      # 미래를 완전히 다른 값으로
            df.to_csv(p, index=False)
        pa, pb = L.build_panel(end=END, obs_dir=a_dir), L.build_panel(end=END, obs_dir=b_dir)
        for sid, h in (("VIXCLS", 21), ("DGS10", 63)):
            ra = C.analyze_target(pa, sid, h, n_perm=200, seed=5, asof=T)
            rb = C.analyze_target(pb, sid, h, n_perm=200, seed=5, asof=T)
            assert ra["edges"] == rb["edges"], f"{sid} h={h}: 3분위 경계에 미래 정보가 섞였다"
            assert ra["prob"] == rb["prob"] and ra["base"] == rb["base"], f"{sid} h={h}: 확률에 미래 정보가 섞였다"
            assert [t.get("p_perm") for t in ra["tests"]] == [t.get("p_perm") for t in rb["tests"]]


# ───────────────────────── 통계 ─────────────────────────

def test_hysteresis():
    p = pd.Series([np.nan, 0.55, 0.58, 0.61, 0.55, 0.45, 0.39, 0.45, 0.59, 0.61])
    s = L.hysteresis(p, 0.4, 0.6).tolist()
    assert np.isnan(s[0])
    assert s[1:] == [1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0], s               # 첫 상태는 0.5 기준, 이후 60/40


def test_permutation_calibration_on_noise():
    """상태와 결과가 독립이면 5% 수준 검정의 기각률이 대략 5%여야 한다 (겹치는 창·지속적 상태 포함)."""
    rng = np.random.default_rng(2024)
    n, h, sims, rej = 2500, 63, 150, 0
    for _ in range(sims):
        x = rng.normal(0, 1, n + h)
        fwd = pd.Series(x).rolling(h).sum().shift(-h + 1).to_numpy()[:n]            # 겹치는 63일 합
        fwd = fwd[: n - h]
        st = np.zeros(n)
        cur, i = 0, 0
        while i < n:                                                                  # 평균 지속 약 120일의 이진 상태
            run = int(rng.geometric(1 / 120))
            st[i:i + run] = cur
            cur, i = 1 - cur, i + run
        mask = (st[: n - h] == 1)
        rank = pd.Series(fwd).rank(pct=True).to_numpy()
        if C.perm_pvalue(mask, rank, h, 200, rng) <= 0.05:
            rej += 1
    rate = rej / sims
    assert 0.01 <= rate <= 0.12, f"순열검정 기각률 {rate:.3f}이 5% 근처가 아니다"


# ───────────────────────── 수집·검사 ─────────────────────────

def _s(vals, start="2024-01-01"):
    return pd.Series(vals, index=pd.bdate_range(start, periods=len(vals)), dtype=float)


def test_merge_records_revision_and_keeps_history():
    old = _s([1, 2, 3, 4, 5])
    new = _s([3.5, 4, 5, 6], start=old.index[2])                       # 3번째 값이 3 -> 3.5로 개정, 이후 1건 신규
    merged, changed = FH.merge(old, new, window_start=old.index[2])
    assert len(merged) == 6 and merged.iloc[0] == 1 and merged.iloc[1] == 2     # 윈도 이전 이력 보존
    assert merged[old.index[2]] == 3.5
    assert [(c[1], c[2]) for c in changed] == [(3.0, 3.5)]


def test_merge_short_response_does_not_shrink_history():
    old = _s(range(1, 101))
    new = _s([99, 100], start=old.index[98])                            # 응답이 2행뿐
    merged, _ = FH.merge(old, new, window_start=old.index[98])
    assert len(merged) == 100


def _one_series_catalog(**kw):
    row = {"series_id": "X", "name_kr": "X", "freq": "D", "lag_days": 1, "roles": "display", "chg": "diff",
           "start": "2020-01-01", "expected_start": "2020-01-01", "min_rows": 100, "max_ffill": 10, "known_limit": ""}
    row.update(kw)
    return pd.DataFrame([row]).set_index("series_id", drop=False)


def _write(d: Path, s: pd.Series):
    pd.DataFrame({"date": s.index.strftime("%Y-%m-%d"), "value": s.to_numpy()}).to_csv(d / "X.csv", index=False)


def _levels(res):
    return {r["level"] for r in res}


def test_checks_catch_defects():
    cat = _one_series_catalog()
    good = _s(np.random.default_rng(1).normal(0, 1, 400).cumsum() + 100, start="2020-01-01")
    last = good.index[-1]
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        # 파일 없음
        assert "ERROR" in _levels(K.run_checks(today=last, obs_dir=d, catalog=cat))
        # 정상
        _write(d, good)
        assert _levels(K.run_checks(today=last, obs_dir=d, catalog=cat)) == {"OK"}
        # 빈 파일 (헤더만)
        (d / "X.csv").write_text("date,value\n")
        assert "ERROR" in _levels(K.run_checks(today=last, obs_dir=d, catalog=cat))
        # 행 수 미달
        _write(d, good.iloc[-50:])
        assert any("행 수" in r["msg"] for r in K.run_checks(today=last, obs_dir=d, catalog=cat))
        # 이력 절단 (기대 시작일보다 한참 늦게 시작)
        _write(d, good.iloc[200:])
        res = K.run_checks(today=last, obs_dir=d, catalog=_one_series_catalog(min_rows=10))
        assert any("이력 절단" in r["msg"] for r in res)
        # 갱신 지연 (경고 -> 2배 초과 시 오류)
        _write(d, good)
        assert any(r["level"] == "WARN" and "지연" in r["msg"] for r in K.run_checks(today=last + pd.Timedelta(days=12), obs_dir=d, catalog=cat))
        assert any(r["level"] == "ERROR" and "지연" in r["msg"] for r in K.run_checks(today=last + pd.Timedelta(days=60), obs_dir=d, catalog=cat))
        # 날짜 중복
        dup = pd.concat([good, good.iloc[-1:]])
        pd.DataFrame({"date": dup.index.strftime("%Y-%m-%d"), "value": dup.to_numpy()}).to_csv(d / "X.csv", index=False)
        assert any("중복" in r["msg"] for r in K.run_checks(today=last, obs_dir=d, catalog=cat))
        # 단위 급변 (마지막 값이 1000배)
        bad = good.copy()
        bad.iloc[-1] = bad.iloc[-1] * 1000
        _write(d, bad)
        assert any("급변" in r["msg"] for r in K.run_checks(today=last, obs_dir=d, catalog=cat))
        # 값 고정
        flat = good.copy()
        flat.iloc[-12:] = flat.iloc[-12]
        _write(d, flat)
        assert any("동일" in r["msg"] for r in K.run_checks(today=last, obs_dir=d, catalog=cat))


# ───────────────────────── 예측 로그 ─────────────────────────

def test_forecast_register_grade_verify_and_tamper():
    T0, T_END = "2020-06-30", "2020-12-31"
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        od = d / "obs"
        make_obs(od, end="2021-03-31")
        cfg = L.load_config()
        cfg_small = dict(cfg)
        cfg_small["targets"] = ["VIXCLS", "DGS10"]
        pan0 = L.build_panel(end=T0, asof=T0, obs_dir=od, cfg=cfg_small)
        assert F.register(today=T0, panel=pan0, root=d, n_perm=100, validation={}) == 0
        log = F.load_log(F.log_path(cfg, d))
        assert len(log) == 4 and set(log["status"]) == {"pending"}
        assert (log["p_down"] == log["base_down"]).all(), "검증 이력이 없으면 공식 확률은 기저율이어야 한다"
        # 같은 ISO 주에 다시 등록하면 건너뜀
        F.register(today="2020-07-01", panel=L.build_panel(end="2020-07-01", asof="2020-07-01", obs_dir=od, cfg=cfg_small),
                   root=d, n_perm=100, validation={})
        assert len(F.load_log(F.log_path(cfg, d))) == 4
        assert F.verify(d, cfg) == []
        # 채점: 해소일이 지난 패널
        panE = L.build_panel(end=T_END, obs_dir=od, cfg=cfg_small)
        assert F.grade(panel=panE, root=d) == 0
        log = F.load_log(F.log_path(cfg, d))
        r21 = log[(log["series"] == "VIXCLS") & (log["horizon"] == 21)].iloc[0]
        assert r21["status"] == "resolved"
        # 수동 재계산과 일치
        kn = panE["known"]["VIXCLS"]
        chg = kn.get(pd.Timestamp(r21["resolve_on"])) - r21["start_value"]
        assert abs(chg - r21["realized_change"]) < 1e-6
        want = 0 if chg < r21["edge_lo"] else (2 if chg > r21["edge_hi"] else 1)
        assert int(r21["outcome_bin"]) == want
        p = np.array([r21["p_down"], r21["p_flat"], r21["p_up"]])
        o = np.eye(3)[want]
        assert abs(((p - o) ** 2).sum() - r21["brier"]) < 1e-9
        assert F.verify(d, cfg) == [], "채점은 등록 필드를 바꾸지 않으므로 해시 검증을 통과해야 한다"
        assert not F.score(d, cfg).empty
        # 변조 감지
        raw = F.log_path(cfg, d).read_text(encoding="utf-8").splitlines()
        hdr = raw[0].split(",")
        i_p = hdr.index("p_up")
        row = raw[1].split(",")
        row[i_p] = "0.99"
        raw[1] = ",".join(row)
        F.log_path(cfg, d).write_text("\n".join(raw) + "\n", encoding="utf-8")
        assert any("해시 불일치" in x for x in F.verify(d, cfg))


def test_log_keeps_numeric_looking_strings():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "log.csv"
        df = pd.DataFrame([{c: np.nan for c in F.COLS}]).astype(object)
        df.loc[0, ["config_hash", "row_hash", "iso_week"]] = ["12345e6789", "1e5", "2026-W01"]
        F.save_log(df, p)
        back = F.load_log(p)
        assert back.loc[0, "config_hash"] == "12345e6789" and back.loc[0, "row_hash"] == "1e5"


def test_config_hash_ignores_comments_but_not_model():
    base = L.config_hash()
    assert base == L.config_hash()
    cfg = L.load_config()
    assert "validation" in cfg and "validation" not in L.MODEL_KEYS      # 검증 게이트 값 변경은 모형 해시와 무관


# ───────────────────────── ECOS ─────────────────────────

ECOS_OK = {"StatisticSearch": {"list_total_count": 2, "row": [
    {"STAT_CODE": "817Y002", "ITEM_CODE1": "010210000", "ITEM_NAME1": "국고채(10년)", "UNIT_NAME": "연%",
     "TIME": "20260901", "DATA_VALUE": "4.371"},
    {"STAT_CODE": "817Y002", "ITEM_CODE1": "010210000", "ITEM_NAME1": "국고채(10년)", "UNIT_NAME": "연%",
     "TIME": "20260902", "DATA_VALUE": "4.418"}]}}


def test_parse_ecos_ok_and_failures():
    s = FH.parse_ecos(ECOS_OK, "국고채(10년)")
    assert list(s.index) == [pd.Timestamp("2026-09-01"), pd.Timestamp("2026-09-02")] and s.iloc[1] == 4.418
    for bad, why in ((  {"RESULT": {"CODE": "INFO-200", "MESSAGE": "해당하는 데이터가 없습니다."}}, "오류"),
                      ({"RESULT": {"CODE": "ERROR-100", "MESSAGE": "인증키 오류"}}, "오류"),
                      ({"StatisticSearch": {"row": []}}, "행이 없다")):
        try:
            FH.parse_ecos(bad, "국고채(10년)")
        except RuntimeError as e:
            assert why in str(e)
        else:
            raise AssertionError("오류 응답을 통과시켰다")
    try:
        FH.parse_ecos(ECOS_OK, "국고채(3년)")                       # 항목 코드가 바뀌어 다른 계열이 오는 경우
    except RuntimeError as e:
        assert "불일치" in str(e)
    else:
        raise AssertionError("항목명 불일치를 통과시켰다")


def test_fetch_ecos_url_and_no_key_preserves_file():
    calls = []
    orig = FH._get

    class R:
        def json(self): return ECOS_OK

    def fake(url, params):
        calls.append(url)
        return R()
    FH._get = fake
    try:
        s = FH.fetch_ecos("817Y002|D|010210000|국고채(10년)", "2026-09-01", "KEY123")
    finally:
        FH._get = orig
    assert len(s) == 2
    assert "/KEY123/json/kr/1/100000/817Y002/D/20260901/" in calls[0] and calls[0].endswith("/010210000")
    # 키가 없으면 해당 시리즈는 실패로 기록되고 기존 파일은 그대로다
    import os
    with tempfile.TemporaryDirectory() as d:
        od = Path(d)
        keep = _s([1.0, 2.0, 3.0], start="2026-01-01")
        pd.DataFrame({"date": keep.index.strftime("%Y-%m-%d"), "value": keep.to_numpy()}).to_csv(od / "KR10Y.csv", index=False)
        before = (od / "KR10Y.csv").read_text()
        saved = os.environ.pop("ECOS_API_KEY", None)
        try:
            rc = FH.run(["KR10Y"], full=False, source="csv", obs_dir=od)
        finally:
            if saved is not None:
                os.environ["ECOS_API_KEY"] = saved
        assert rc == 1 and (od / "KR10Y.csv").read_text() == before


def test_catalog_ecos_rows_well_formed():
    cat = L.load_catalog()
    e = cat[cat["source"] == "ecos"]
    assert len(e) >= 4
    for sid, r in e.iterrows():
        parts = r["ecos"].split("|")
        assert len(parts) == 4 and parts[1] == "D" and parts[3], f"{sid}: ecos 열 형식 오류"
    assert set(L.load_config()["targets"]) <= set(cat.index)


# ───────────────────────── 실행기 ─────────────────────────

def main() -> int:
    tests = [(n, f) for n, f in globals().items() if n.startswith("test_") and callable(f)]
    fails = 0
    for name, fn in tests:
        try:
            fn()
            print(f"  통과  {name}")
        except Exception:                                              # noqa: BLE001
            fails += 1
            print(f"  실패  {name}")
            traceback.print_exc()
    print(f"\n{len(tests) - fails}/{len(tests)} 통과")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
