"""Integration tests for the /api/search endpoint."""
from __future__ import annotations

import pytest
from flask.testing import FlaskClient

from src.app import create_app


@pytest.fixture()
def client() -> FlaskClient:
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


class TestSearchEndpointValidation:
    def test_missing_q_returns_400(self, client: FlaskClient) -> None:
        resp = client.get("/api/search?mode=name")
        assert resp.status_code == 400

    def test_missing_mode_returns_400(self, client: FlaskClient) -> None:
        resp = client.get("/api/search?q=toit")
        assert resp.status_code == 400

    def test_invalid_mode_returns_400(self, client: FlaskClient) -> None:
        resp = client.get("/api/search?q=toit&mode=invalid")
        assert resp.status_code == 400

    def test_empty_q_returns_400(self, client: FlaskClient) -> None:
        resp = client.get("/api/search?q=&mode=name")
        assert resp.status_code == 400

    def test_whitespace_only_q_returns_400(self, client: FlaskClient) -> None:
        resp = client.get("/api/search?q=%20%20&mode=name")
        assert resp.status_code == 400

    def test_too_long_q_returns_400(self, client: FlaskClient) -> None:
        long_q = "a" * 201
        resp = client.get(f"/api/search?q={long_q}&mode=name")
        assert resp.status_code == 400


class TestSearchEndpointSuccess:
    def test_search_by_name_returns_200(self, client: FlaskClient) -> None:
        resp = client.get("/api/search?q=a&mode=name")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["success"] is True
        assert "data" in data
        assert data["data"]["mode"] == "name"
        assert "results" in data["data"]
        assert "total_matches" in data["data"]

    def test_search_by_type_returns_200(self, client: FlaskClient) -> None:
        resp = client.get("/api/search?q=cafe&mode=type")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["success"] is True
        assert data["data"]["mode"] == "type"

    def test_search_by_area_returns_200(self, client: FlaskClient) -> None:
        resp = client.get("/api/search?q=a&mode=area")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["success"] is True
        assert data["data"]["mode"] == "area"

    def test_search_results_capped_at_10(self, client: FlaskClient) -> None:
        resp = client.get("/api/search?q=a&mode=name")
        assert resp.status_code == 200
        data = resp.get_json()
        assert len(data["data"]["results"]) <= 10


class TestSearchEndpointEmptyResults:
    def test_no_match_returns_empty_results(self, client: FlaskClient) -> None:
        resp = client.get("/api/search?q=zzzznonexistent&mode=name")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["data"]["total_matches"] == 0
        assert data["data"]["results"] == []


class TestSearchEndpointResponseShape:
    def test_response_has_metadata(self, client: FlaskClient) -> None:
        resp = client.get("/api/search?q=a&mode=name")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "metadata" in data
        assert "request_id" in data["metadata"]
        assert "processing_time_ms" in data["metadata"]
        assert "timestamp" in data["metadata"]
