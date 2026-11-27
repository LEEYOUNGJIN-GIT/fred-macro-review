# -*- coding: utf-8 -*-
"""공용 fixture. 네트워크를 쓰지 않는다.

tests/fixtures/fred_fixtures.py 가 만드는 응답은 FRED 형식을 흉내 낸 **합성 데이터**다.
실제 FRED 관측값이 아니며 data/series/ 에 기록되지 않는다(테스트는 tmp_path 사용).
"""
import copy
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT))

from tests.fixtures.fred_fixtures import build_series  # noqa: E402

_SERIES = build_series()

SENTINEL_KEY = "SENTINELKEY0123456789abcdef"


class FakeResponse:
    def __init__(self, status_code, payload=None, text=""):
        self.status_code = status_code
        self._payload = payload
        self.text = text or (json.dumps(payload) if payload is not None else "")

    def json(self):
        if self._payload is None:
            raise ValueError("no json")
        return self._payload


class FakeSession:
    """FRED series / series/observations 엔드포인트를 흉내 낸다.

    series: {series_id: {"meta": {...}, "observations": [...],
                          "vintage": [...], "errors": [status, ...]}}
    errors 의 상태코드는 호출마다 앞에서부터 소비된다.
    """

    def __init__(self, series, page_limit=None):
        self.series = series
        self.page_limit = page_limit
        self.requests = []

    def get(self, url, params=None, timeout=None):
        params = dict(params or {})
        self.requests.append((url, params))
        sid = params.get("series_id")
        spec = self.series.get(sid)
        if spec is None:
            return FakeResponse(400, {"error_code": 400,
                                      "error_message": "Bad Request.  The series does not exist."})
        errors = spec.setdefault("errors", [])
        if errors:
            status = errors.pop(0)
            if status == "raise":
                import requests
                raise requests.ConnectionError(
                    f"Max retries exceeded with url: {url}?api_key={params.get('api_key')}")
            return FakeResponse(status, {"error_code": status,
                                         "error_message": f"boom for url {url}?api_key={params.get('api_key')}"})
        if url.endswith("/series"):
            return FakeResponse(200, {"seriess": [spec["meta"]]})
        if "realtime_start" in params:
            obs = list(spec.get("vintage", []))
        else:
            obs = list(spec["observations"])
        start = params.get("observation_start")
        if start:
            obs = [o for o in obs if o["date"] >= start]
        count = len(obs)
        offset = int(params.get("offset", 0))
        limit = int(params.get("limit", 100000))
        if self.page_limit:
            limit = min(limit, self.page_limit)
        return FakeResponse(200, {"count": count, "offset": offset, "limit": limit,
                                  "observations": obs[offset:offset + limit]})


@pytest.fixture
def fixture_series():
    """테스트마다 수정 가능한 사본."""
    return copy.deepcopy(_SERIES)


@pytest.fixture
def api_key(monkeypatch):
    monkeypatch.setenv("FRED_API_KEY", SENTINEL_KEY)
    return SENTINEL_KEY
