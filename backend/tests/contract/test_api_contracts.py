from __future__ import annotations


def _assert_metadata(body):
    assert "metadata" in body
    assert "request_id" in body["metadata"]
    assert "processing_time_ms" in body["metadata"]
    assert "timestamp" in body["metadata"]


def test_contract_health(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["success"] is True
    assert "data" in body
    assert "status" in body["data"]
    _assert_metadata(body)


def test_contract_restaurant_types(client, app, sample_restaurants_df):
    app.config["RESTAURANTS_DF"] = sample_restaurants_df

    resp = client.get("/api/restaurant-types")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["success"] is True
    assert "restaurant_types" in body["data"]
    assert "total_types" in body["data"]
    _assert_metadata(body)


def test_contract_top_restaurants(client, app, sample_restaurants_df):
    df = sample_restaurants_df.copy()
    df["cuisines"] = ["A", "A", "B"]
    app.config["RESTAURANTS_DF"] = df

    resp = client.get("/api/top-restaurants")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["success"] is True
    assert "top_restaurants" in body["data"]
    assert "total_restaurants" in body["data"]
    _assert_metadata(body)


def test_contract_foodie_areas(client, app, sample_restaurants_df):
    df = sample_restaurants_df.copy()
    df["cuisines"] = ["A", "A", "B"]
    app.config["RESTAURANTS_DF"] = df

    resp = client.get("/api/foodie-areas")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["success"] is True
    assert "foodie_areas" in body["data"]
    assert "total_areas" in body["data"]
    _assert_metadata(body)


def test_contract_charts(client, app, sample_restaurants_df):
    app.config["RESTAURANTS_DF"] = sample_restaurants_df

    resp = client.get("/api/charts/restaurant-types-pie")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["success"] is True
    assert body["data"]["chart_type"] == "restaurant-types-pie"
    assert body["data"]["base64_image"]
    assert "width" in body["data"]
    assert "height" in body["data"]
    _assert_metadata(body)
