from __future__ import annotations


def test_health_endpoint(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["success"] is True
    assert body["data"]["status"] == "healthy"
    assert "request_id" in body["metadata"]


def test_restaurant_types_requires_loaded_data(app, client):
    app.config["RESTAURANTS_DF"] = None
    resp = client.get("/api/restaurant-types")
    assert resp.status_code == 500
    body = resp.get_json()
    assert body["success"] is False


def test_restaurant_types_success(app, client, sample_restaurants_df):
    app.config["RESTAURANTS_DF"] = sample_restaurants_df
    resp = client.get("/api/restaurant-types")
    assert resp.status_code == 200

    body = resp.get_json()
    assert body["success"] is True
    assert body["data"]["total_types"] == 2
    assert len(body["data"]["restaurant_types"]) == 2
