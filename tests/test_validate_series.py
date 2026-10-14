# -*- coding: utf-8 -*-
"""scripts/validate_series.py 테스트."""
from datetime import datetime, timezone

import fred_series_collect as fsc
import validate_series as vs
from tests.conftest import SENTINEL_KEY, FakeSession

NOW = datetime(2026, 10, 12, 21, 40, tzinfo=timezone.utc)


def build(tmp_path, fixture_series, ids=("DFII10", "DEXKOUS", "CPIAUCSL", "CPIAUCNS",
                                          "BAMLH0A0HYM2", "UNRATE")):
    client = fsc.FredClient(SENTINEL_KEY, session=FakeSession(fixture_series),
                            sleep=lambda s: None)
    assert fsc.collect(list(ids), tmp_path, client, now=NOW, vintages=True,
                       vintage_series=["UNRATE"]) == []
    return tmp_path


def test_valid_output_passes(tmp_path, fixture_series):
    errs, n = vs.validate(build(tmp_path, fixture_series))
    assert errs == [] and n == 6


def test_empty_root_passes(tmp_path):
    assert vs.validate(tmp_path) == ([], 0)


def test_main_exit_code(tmp_path, fixture_series, capsys):
    build(tmp_path, fixture_series)
    assert vs.main(["--root", str(tmp_path), "--short-report"]) == 0
    out = capsys.readouterr().out
    assert "| BAMLH0A0HYM2 |" in out and "| DFII10 |" not in out


def test_detects_unsorted_and_duplicate(tmp_path, fixture_series):
    root = build(tmp_path, fixture_series)
    p = root / "fred" / "DFII10.csv"
    lines = p.read_text().splitlines()
    lines.insert(5, lines[3])                    # 중복 + 비정렬
    p.write_text("\n".join(lines) + "\n")
    errs, _ = vs.validate(root)
    assert any("중복 날짜" in e for e in errs)
    assert any("오름차순 아님" in e for e in errs)
    assert vs.main(["--root", str(root)]) == 1


def test_detects_bad_header_value_and_date(tmp_path, fixture_series):
    root = build(tmp_path, fixture_series)
    (root / "fred" / "DEXKOUS.csv").write_text("date,val\n2020-01-01,1\n")
    p = root / "fred" / "DFII10.csv"
    p.write_text(p.read_text().replace("2025-12-25,", "2025-12-25,.", 1))
    q = root / "fred" / "CPIAUCSL.csv"
    q.write_text(q.read_text().replace("2026-08-01,", "2026-08-15,", 1))
    errs, _ = vs.validate(root)
    assert any("DEXKOUS.csv: 헤더" in e for e in errs)
    assert any("DFII10.csv: 숫자 아닌 값" in e for e in errs)
    assert any("CPIAUCSL.csv: M 시리즈인데 기간 첫날" in e for e in errs)


def test_detects_meta_problems(tmp_path, fixture_series):
    root = build(tmp_path, fixture_series)
    m = root / "fred_meta.csv"
    m.write_text(m.read_text().replace(",fx,", ",currency,", 1))
    (root / "fred" / "ORPHAN.csv").write_text("date,value\n2020-01-01,1.0\n")
    errs, _ = vs.validate(root)
    assert any("series_type='currency'" in e for e in errs)
    assert any("ORPHAN 시리즈 파일은 있으나 메타 행 없음" in e for e in errs)


def test_detects_vintage_problems(tmp_path, fixture_series):
    root = build(tmp_path, fixture_series)
    p = root / "fred_vintage" / "UNRATE.csv"
    lines = p.read_text().splitlines()
    d, v, rs, re_ = lines[1].split(",")
    lines[1] = ",".join([d, v, re_, rs]) if re_ != "9999-12-31" else lines[1]
    lines.append(lines[2])
    p.write_text("\n".join(lines) + "\n")
    errs, _ = vs.validate(root)
    assert any("realtime_start > realtime_end" in e for e in errs)
    assert any("중복" in e for e in errs)
