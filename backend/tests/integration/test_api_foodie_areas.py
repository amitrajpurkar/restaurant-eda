from __future__ import annotations


def test_foodie_areas_requires_loaded_data(app, client):
    app.config["RESTAURANTS_DF"] = None
    resp = client.get("/api/foodie-areas")
    assert resp.status_code == 500
    body = resp.get_json()
    assert body["success"] is False


def test_foodie_areas_success_default(app, client, sample_restaurants_df):
    df = sample_restaurants_df.copy()
    df["cuisines"] = ["A", "A", "B"]
    app.config["RESTAURANTS_DF"] = df

    resp = client.get("/api/foodie-areas")
    assert resp.status_code == 200

    body = resp.get_json()
    assert body["success"] is True
    assert len(body["data"]["foodie_areas"]) >= 1
    assert body["data"]["total_areas"] >= 1


def test_foodie_areas_limit_validation(app, client, sample_restaurants_df):
    df = sample_restaurants_df.copy()
    df["cuisines"] = ["A", "A", "B"]
    app.config["RESTAURANTS_DF"] = df

    resp = client.get("/api/foodie-areas?limit=0")
    assert resp.status_code == 400

    resp = client.get("/api/foodie-areas?limit=999")
    assert resp.status_code == 400
