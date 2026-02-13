from __future__ import annotations


def test_charts_invalid_type(app, client, sample_restaurants_df):
    app.config["RESTAURANTS_DF"] = sample_restaurants_df

    resp = client.get("/api/charts/invalid")
    assert resp.status_code == 404
    body = resp.get_json()
    assert body["success"] is False


def test_charts_valid_restaurant_types_pie(app, client, sample_restaurants_df):
    app.config["RESTAURANTS_DF"] = sample_restaurants_df

    resp = client.get("/api/charts/restaurant-types-pie?width=800&height=400")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["success"] is True
    assert body["data"]["chart_type"] == "restaurant-types-pie"
    assert body["data"]["base64_image"]


def test_charts_size_validation(app, client, sample_restaurants_df):
    app.config["RESTAURANTS_DF"] = sample_restaurants_df

    resp = client.get("/api/charts/restaurant-types-pie?width=1&height=1")
    assert resp.status_code == 400
