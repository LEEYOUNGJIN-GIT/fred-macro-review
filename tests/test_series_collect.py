# -*- coding: utf-8 -*-
"""scripts/fred_series_collect.py fixture 기반 테스트 (네트워크 없음)."""
import math
from datetime import datetime, timezone

import pandas as pd
import pytest

import fred_series_collect as fsc
from tests.conftest import ROOT, SENTINEL_KEY, FakeSession

NOW = datetime(2026, 10, 12, 21, 40, 0, tzinfo=timezone.utc)
NOW2 = datetime(2026, 10, 13, 21, 40, 0, tzinfo=timezone.utc)


def run(series, ids, out, now=NOW, vintages=False, session=None, **kw):
    session = session or FakeSession(series, **kw)
    client = fsc.FredClient(SENTINEL_KEY, session=session, sleep=lambda s: None)
    failures = fsc.collect(ids, out, client, now=now, vintages=vintages,
                           vintage_series=["UNRATE"] if vintages else None)
    return failures, session


def snapshot(root):
    return {p.relative_to(root).as_posix(): p.read_bytes()
            for p in sorted(root.rglob("*")) if p.is_file()}


def read_series(out, sid):
    return pd.read_csv(out / "fred" / f"{sid}.csv", dtype={"date": str},
                       keep_default_na=False, na_values=[""])


# ── 레지스트리 ──

def test_registry_loaded_without_import_and_types_complete():
    reg = fsc.load_registry()
    ids = fsc.registry_series_ids(reg)
    assert len(reg) == 102 and len(ids) == 99
    assert "COPPER_GOLD_RATIO" not in ids
    assert {"DFII10", "DEXKOUS"} <= set(ids)
    missing = [s for s in ids if s not in fsc.SERIES_TYPE]
    assert missing == []
    assert set(fsc.SERIES_TYPE.values()) <= fsc.SERIES_TYPES
    assert set(fsc.VINTAGE_SERIES) <= set(ids)


# ── 백필 / 결측 / 비어 있지 않음 ──

def test_backfill_dfii10_dexkous_nonempty(tmp_path, fixture_series):
    failures, _ = run(fixture_series, ["DFII10", "DEXKOUS"], tmp_path)
    assert failures == []
    for sid in ("DFII10", "DEXKOUS"):
        p = tmp_path / "fred" / f"{sid}.csv"
        assert p.exists() and p.stat().st_size > 1000
        df = read_series(tmp_path, sid)
        assert list(df.columns) == ["date", "value"]
        assert df["value"].notna().sum() > 2500
        assert len(df) == len(fixture_series[sid]["observations"])


def test_missing_values_preserved_not_filled(tmp_path, fixture_series):
    run(fixture_series, ["DFII10"], tmp_path)
    df = read_series(tmp_path, "DFII10")
    dots = {o["date"] for o in fixture_series["DFII10"]["observations"] if o["value"] == "."}
    assert dots, "fixture 에 결측이 있어야 한다"
    got = set(df[df["value"].isna()]["date"])
    assert got == dots
    raw = (tmp_path / "fred" / "DFII10.csv").read_text(encoding="utf-8")
    assert "2025-12-25,\n" in raw          # 빈 칸으로 저장
    assert ",." not in raw and "nan" not in raw.lower()


def test_full_history_request_on_backfill(tmp_path, fixture_series):
    _, session = run(fixture_series, ["CPIAUCSL"], tmp_path)
    obs_req = [p for u, p in session.requests if u.endswith("/observations")]
    assert obs_req and "observation_start" not in obs_req[0]
    assert obs_req[0]["sort_order"] == "asc" and "units" not in obs_req[0]
    assert "realtime_start" not in obs_req[0]


def test_pagination(tmp_path, fixture_series):
    failures, session = run(fixture_series, ["DFII10"], tmp_path, page_limit=1000)
    assert failures == []
    obs_req = [p for u, p in session.requests if u.endswith("/observations")]
    assert len(obs_req) == math.ceil(len(fixture_series["DFII10"]["observations"]) / 1000)
    assert len(read_series(tmp_path, "DFII10")) == len(fixture_series["DFII10"]["observations"])


# ── 증분 / 멱등 / 개정 ──

def test_incremental_refetches_last_12(tmp_path, fixture_series):
    run(fixture_series, ["CPIAUCSL"], tmp_path)
    dates = [o["date"] for o in fixture_series["CPIAUCSL"]["observations"]]
    fixture_series["CPIAUCSL"]["observations"].append({"date": "2026-09-01", "value": "330.5"})
    _, session = run(fixture_series, ["CPIAUCSL"], tmp_path, now=NOW2)
    obs_req = [p for u, p in session.requests if u.endswith("/observations")]
    assert obs_req[0]["observation_start"] == dates[-12]
    df = read_series(tmp_path, "CPIAUCSL")
    assert df["date"].iloc[-1] == "2026-09-01" and df["value"].iloc[-1] == 330.5
    assert not (tmp_path / "_revisions.csv").exists()


def test_idempotent_same_response_twice(tmp_path, fixture_series):
    ids = ["DFII10", "DEXKOUS", "CPIAUCSL", "CPIAUCNS"]
    run(fixture_series, ids, tmp_path)
    first = snapshot(tmp_path)
    run(fixture_series, ids, tmp_path)          # 같은 응답, 같은 시각
    assert snapshot(tmp_path) == first
    assert not (tmp_path / "_revisions.csv").exists()


def test_series_files_unchanged_on_rerun_even_if_clock_moves(tmp_path, fixture_series):
    run(fixture_series, ["DEXKOUS"], tmp_path)
    before = (tmp_path / "fred" / "DEXKOUS.csv").read_bytes()
    run(fixture_series, ["DEXKOUS"], tmp_path, now=NOW2)
    assert (tmp_path / "fred" / "DEXKOUS.csv").read_bytes() == before


def test_revision_detected_and_logged(tmp_path, fixture_series):
    run(fixture_series, ["CPIAUCSL"], tmp_path)
    obs = fixture_series["CPIAUCSL"]["observations"]
    target = obs[-3]
    old = float(target["value"])
    target["value"] = f"{old + 0.5:.3f}"
    run(fixture_series, ["CPIAUCSL"], tmp_path, now=NOW2)
    rev = pd.read_csv(tmp_path / "_revisions.csv", dtype=str, keep_default_na=False)
    assert list(rev.columns) == ["series_id", "date", "old", "new", "detected_at"]
    assert len(rev) == 1
    r = rev.iloc[0]
    assert (r["series_id"], r["date"]) == ("CPIAUCSL", target["date"])
    assert float(r["old"]) == old and float(r["new"]) == float(target["value"])
    assert r["detected_at"] == "2026-10-13T21:40:00Z"
    df = read_series(tmp_path, "CPIAUCSL").set_index("date")
    assert df.loc[target["date"], "value"] == float(target["value"])
    # 같은 개정을 다시 처리해도 중복 기록되지 않는다
    run(fixture_series, ["CPIAUCSL"], tmp_path, now=NOW2)
    assert len(pd.read_csv(tmp_path / "_revisions.csv")) == 1


def test_missing_to_value_is_a_revision(tmp_path, fixture_series):
    obs = fixture_series["CPIAUCSL"]["observations"]
    obs[-2]["value"] = "."
    run(fixture_series, ["CPIAUCSL"], tmp_path)
    obs[-2]["value"] = "320.000"
    run(fixture_series, ["CPIAUCSL"], tmp_path, now=NOW2)
    rev = pd.read_csv(tmp_path / "_revisions.csv", dtype=str, keep_default_na=False)
    assert rev.iloc[0]["old"] == "" and float(rev.iloc[0]["new"]) == 320.0


def test_revision_outside_window_not_seen(tmp_path, fixture_series):
    """재조회 구간(최근 12개) 밖의 개정은 증분에서 조회되지 않는다(문서화된 한계)."""
    run(fixture_series, ["CPIAUCSL"], tmp_path)
    fixture_series["CPIAUCSL"]["observations"][-13]["value"] = "1.000"
    run(fixture_series, ["CPIAUCSL"], tmp_path, now=NOW2)
    assert not (tmp_path / "_revisions.csv").exists()


# ── 메타 / 스키마 / SA·NSA ──

def test_meta_schema_contract(tmp_path, fixture_series):
    ids = ["DFII10", "DEXKOUS", "CPIAUCSL", "CPIAUCNS", "BAMLH0A0HYM2"]
    run(fixture_series, ids, tmp_path)
    meta = pd.read_csv(tmp_path / "fred_meta.csv", dtype=str, keep_default_na=False)
    assert list(meta.columns) == fsc.META_COLUMNS
    assert list(meta["series_id"]) == ids
    assert set(meta["series_type"]) <= fsc.SERIES_TYPES
    assert set(meta["vintage"]) <= {"Y", "N"}
    assert (meta["seasonal_adjustment"] != "").all()
    assert pd.to_numeric(meta["years_available"]).dtype == "float64"
    m = meta.set_index("series_id")
    assert m.loc["DEXKOUS", "series_type"] == "fx"
    assert m.loc["DFII10", "series_type"] == "rate"
    assert m.loc["CPIAUCSL", "vintage"] == "Y" and m.loc["DFII10", "vintage"] == "N"
    assert m.loc["DFII10", "probed_at"] == "2026-10-12T21:40:00Z"
    df = pd.read_csv(tmp_path / "fred" / "DFII10.csv", keep_default_na=False, na_values=[""])
    assert df["value"].dtype == "float64"


def test_seasonal_adjustment_taken_from_fred_meta(tmp_path, fixture_series):
    fixture_series["CPIAUCSL"]["meta"]["seasonal_adjustment_short"] = "SAAR-TEST"
    run(fixture_series, ["CPIAUCSL"], tmp_path)
    meta = pd.read_csv(tmp_path / "fred_meta.csv", dtype=str)
    assert meta.iloc[0]["seasonal_adjustment"] == "SAAR-TEST"   # 추정하지 않고 응답값 그대로


def test_sa_nsa_pair_stored_separately(tmp_path, fixture_series):
    run(fixture_series, ["CPIAUCSL", "CPIAUCNS"], tmp_path)
    sa = read_series(tmp_path, "CPIAUCSL")
    nsa = read_series(tmp_path, "CPIAUCNS")
    assert list(sa["date"]) == list(nsa["date"])
    assert not (sa["value"].values == nsa["value"].values).all()
    m = pd.read_csv(tmp_path / "fred_meta.csv", dtype=str).set_index("series_id")
    assert m.loc["CPIAUCSL", "seasonal_adjustment"] == "SA"
    assert m.loc["CPIAUCNS", "seasonal_adjustment"] == "NSA"
    assert m.loc["CPIAUCNS", "series_type"] == m.loc["CPIAUCSL", "series_type"] == "price_index"


def test_short_history_flag_uses_stored_data_not_meta_start(tmp_path, fixture_series):
    run(fixture_series, ["BAMLH0A0HYM2", "DFII10"], tmp_path)
    m = pd.read_csv(tmp_path / "fred_meta.csv", dtype=str).set_index("series_id")
    assert m.loc["BAMLH0A0HYM2", "observation_start"] == "1996-12-31"
    assert float(m.loc["BAMLH0A0HYM2", "years_available"]) < 10
    assert m.loc["BAMLH0A0HYM2", "short_history"] == "True"
    assert m.loc["DFII10", "short_history"] == "False"


# ── 실패 격리 / 재시도 ──

def test_partial_failure_isolated(tmp_path, fixture_series, capsys):
    fixture_series["DEXKOUS"]["errors"] = [400]
    failures, session = run(fixture_series, ["DFII10", "DEXKOUS", "NOPE", "CPIAUCSL"], tmp_path)
    assert [f[0] for f in failures] == ["DEXKOUS", "NOPE"]
    assert (tmp_path / "fred" / "DFII10.csv").exists()
    assert (tmp_path / "fred" / "CPIAUCSL.csv").exists()
    assert not (tmp_path / "fred" / "DEXKOUS.csv").exists()
    # 4xx 는 재시도 없음: DEXKOUS 요청은 1회
    assert sum(1 for _, p in session.requests if p.get("series_id") == "DEXKOUS") == 1
    fsc.print_failures(failures)
    out = capsys.readouterr().out
    assert "| DEXKOUS | series |" in out and "실패 2건" in out


def test_failed_series_keeps_previous_files_and_meta(tmp_path, fixture_series):
    run(fixture_series, ["DFII10", "CPIAUCSL"], tmp_path)
    before = snapshot(tmp_path)
    fixture_series["DFII10"]["errors"] = [404]
    failures, _ = run(fixture_series, ["DFII10", "CPIAUCSL"], tmp_path)
    assert [f[0] for f in failures] == ["DFII10"]
    assert snapshot(tmp_path) == before


def test_retry_on_429_and_5xx_with_backoff(tmp_path, fixture_series):
    fixture_series["DFII10"]["errors"] = [429, 503, "raise"]
    sleeps = []
    session = FakeSession(fixture_series)
    client = fsc.FredClient(SENTINEL_KEY, session=session, sleep=sleeps.append, delay=0)
    failures = fsc.collect(["DFII10"], tmp_path, client, now=NOW)
    assert failures == []
    assert [s for s in sleeps if s] == [2.0, 4.0, 8.0]


def test_5xx_exhausts_retries(tmp_path, fixture_series):
    fixture_series["DFII10"]["errors"] = [500] * 10
    failures, session = run(fixture_series, ["DFII10"], tmp_path)
    assert failures and failures[0][0] == "DFII10" and "HTTP 500" in failures[0][2]
    assert len(session.requests) == fsc.MAX_RETRIES


def test_main_exit_codes(tmp_path, fixture_series, api_key, monkeypatch):
    ok = fsc.main(["--out", str(tmp_path), "--series", "DFII10"],
                  session=FakeSession(fixture_series), sleep=lambda s: None, now=NOW)
    assert ok == 0
    bad = fsc.main(["--out", str(tmp_path), "--series", "DFII10", "NOPE"],
                   session=FakeSession(fixture_series), sleep=lambda s: None, now=NOW)
    assert bad == 1
    monkeypatch.delenv("FRED_API_KEY")
    assert fsc.main(["--out", str(tmp_path)]) == 2


# ── 키 노출 없음 ──

def test_api_key_never_exposed(tmp_path, fixture_series, api_key, capsys):
    fixture_series["DFII10"]["errors"] = [500] * 10          # 에러 메시지에 URL+키 포함
    fixture_series["DEXKOUS"]["errors"] = ["raise"] * 10     # 예외 문자열에 키 포함
    fixture_series["CPIAUCSL"]["errors"] = [403]
    rc = fsc.main(["--out", str(tmp_path), "--series", "DFII10", "DEXKOUS",
                   "CPIAUCSL", "CPIAUCNS", "--vintages"],
                  session=FakeSession(fixture_series), sleep=lambda s: None, now=NOW)
    assert rc == 1
    cap = capsys.readouterr()
    assert SENTINEL_KEY not in cap.out and SENTINEL_KEY not in cap.err
    assert "api_key=***" in cap.out                            # 마스킹되어 남는다
    for name, data in snapshot(tmp_path).items():
        assert SENTINEL_KEY.encode() not in data, name


def test_redact():
    s = f"https://x/y?series_id=A&api_key={SENTINEL_KEY}&file_type=json"
    assert SENTINEL_KEY not in fsc.redact(s)
    assert SENTINEL_KEY not in fsc.redact(f"key {SENTINEL_KEY}", SENTINEL_KEY)


def test_no_key_literal_in_repo_sources():
    """저장소 소스에 FRED 키 형태(32자리 소문자 hex)가 하드코딩되지 않았는지."""
    import re
    pat = re.compile(rb"api_key\s*[=:]\s*['\"]?[0-9a-f]{32}")
    for p in list(ROOT.glob("*.py")) + list((ROOT / "scripts").glob("*.py")) + \
            list((ROOT / ".github" / "workflows").glob("*.yml")):
        assert not pat.search(p.read_bytes()), p


# ── vintage ──

def test_vintages_off_by_default(tmp_path, fixture_series):
    run(fixture_series, ["UNRATE"], tmp_path)
    assert not (tmp_path / "fred_vintage").exists()


def test_vintages_written(tmp_path, fixture_series):
    failures, session = run(fixture_series, ["UNRATE"], tmp_path, vintages=True)
    assert failures == []
    v = pd.read_csv(tmp_path / "fred_vintage" / "UNRATE.csv", dtype=str)
    assert list(v.columns) == ["date", "value", "realtime_start", "realtime_end"]
    assert len(v) == len(fixture_series["UNRATE"]["vintage"])
    assert (v["realtime_start"] <= v["realtime_end"]).all()
    vreq = [p for _, p in session.requests if "realtime_start" in p]
    assert vreq[0]["observation_start"] == "2016-01-01"   # VINTAGE_YEARS=10 제한
    assert vreq[0]["realtime_end"] == "9999-12-31"


# ── 워크플로 계약 ──

def test_sync_workflow_does_not_upload_series():
    text = (ROOT / ".github" / "workflows" / "sync_claude_project.yml").read_text(encoding="utf-8")
    assert "data/series" not in text


def test_series_workflow_commits_only_data_series():
    text = (ROOT / ".github" / "workflows" / "fred_series_daily.yml").read_text(encoding="utf-8")
    adds = [l.strip() for l in text.splitlines() if l.strip().startswith("git add")]
    assert adds and all(a.split()[2].startswith("data/series") for a in adds)
    assert "concurrency:" in text and "pull --rebase" in text
