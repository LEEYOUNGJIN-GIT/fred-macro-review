# -*- coding: utf-8 -*-
"""회귀 계약: fred_fetch.py 의 fred_latest.csv / fred_latest.md 생성 결과가
골든 파일과 바이트 단위로 같아야 한다.

골든 파일(tests/golden/)은 시계열 저장 레이어 추가 **이전** 커밋의 fred_fetch.py 로
합성 응답을 처리해 만든 것이다. fred_fetch.py 를 수정하면 이 테스트가 출력 변화를 잡는다.
재생성(의도적 형식 변경 시에만): REGEN_GOLDEN=1 python -m pytest tests/test_golden_fred_fetch.py
"""
import importlib.util
import os
from datetime import datetime, timezone

import pytest

from tests.conftest import ROOT, FakeResponse
from tests.fixtures.fred_fixtures import golden_observations

GOLDEN = ROOT / "tests" / "golden"
FAIL_SERIES = "CCSA"   # 3회 실패 → 빈 행 경로


class _FrozenDatetime(datetime):
    @classmethod
    def now(cls, tz=None):
        return cls(2026, 10, 12, 0, 32, 1, tzinfo=timezone.utc)


def _load_fred_fetch(monkeypatch):
    monkeypatch.setenv("FRED_API_KEY", "golden-dummy-key")
    spec = importlib.util.spec_from_file_location("fred_fetch_golden", ROOT / "fred_fetch.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def render(tmp_path, monkeypatch):
    ff = _load_fred_fetch(monkeypatch)
    order = {sid: k for k, sid in enumerate(ff.REG)}

    def fake_get(url, params=None, timeout=None):
        sid = params["series_id"]
        if sid == FAIL_SERIES:
            r = FakeResponse(500, {"error_message": "synthetic"})
        else:
            r = FakeResponse(200, {"observations": golden_observations(
                sid, ff.REG[sid]["freq"], order[sid])})

        def raise_for_status():
            if r.status_code != 200:
                raise ff.requests.HTTPError(f"{r.status_code} Server Error")
        r.raise_for_status = raise_for_status
        return r

    monkeypatch.setattr(ff.requests, "get", fake_get)
    monkeypatch.setattr(ff.time, "sleep", lambda s: None)
    monkeypatch.setattr(ff, "datetime", _FrozenDatetime)
    monkeypatch.setattr(ff, "START_DATE", "2023-10-13")
    monkeypatch.setattr(ff, "END_DATE", "2026-10-12")

    all_data = ff.fetch_all_series(ff.REG)
    fact_md = ff.generate_fact_table(all_data, ff.REG)
    md = tmp_path / "fred_latest.md"
    csv = tmp_path / "fred_latest.csv"
    ff.write_markdown(fact_md, md)
    ff.save_csv(all_data, ff.REG, csv)
    return {"fred_latest.md": md.read_bytes(), "fred_latest.csv": csv.read_bytes()}


@pytest.mark.parametrize("name", ["fred_latest.csv", "fred_latest.md"])
def test_fred_fetch_output_matches_golden(tmp_path, monkeypatch, name):
    out = render(tmp_path, monkeypatch)
    golden = GOLDEN / name
    if os.environ.get("REGEN_GOLDEN") == "1":
        golden.write_bytes(out[name])
    assert golden.exists(), "골든 파일 없음"
    assert out[name] == golden.read_bytes()


def test_golden_csv_header_is_existing_contract():
    """기존 소비자(Fred_signals/Fred_regime/sync)가 쓰는 헤더 계약."""
    head = (GOLDEN / "fred_latest.csv").read_bytes().split(b"\n", 1)[0].decode("utf-8")
    assert head.startswith("﻿")
    assert head.lstrip("﻿").strip() == (
        "series_id,category,korean_name,english_name,frequency,unit,source,transform,"
        "latest_date,latest_value,chg_prev,chg_mid,chg_yoy,note")
    actual = (ROOT / "data" / "fred_latest.csv").read_bytes().split(b"\n", 1)[0]
    assert actual.decode("utf-8").strip() == head.strip()
