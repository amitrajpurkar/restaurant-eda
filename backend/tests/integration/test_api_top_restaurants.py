from __future__ import annotations


def test_top_restaurants_invalid_sort_by(client, app, sample_restaurants_df):
    sample_restaurants_df = sample_restaurants_df.copy()
    sample_restaurants_df["cuisines"] = "North Indian"
    app.config["RESTAURANTS_DF"] = sample_restaurants_df

    resp = client.get("/api/top-restaurants?sort_by=invalid")
    assert resp.status_code == 400
    body = resp.get_json()
    assert body["success"] is False


def test_top_restaurants_invalid_limit(client, app, sample_restaurants_df):
    sample_restaurants_df = sample_restaurants_df.copy()
    sample_restaurants_df["cuisines"] = "North Indian"
    app.config["RESTAURANTS_DF"] = sample_restaurants_df

    resp = client.get("/api/top-restaurants?limit=100")
    assert resp.status_code == 400


def test_top_restaurants_success_default(client, app, sample_restaurants_df):
    sample_restaurants_df = sample_restaurants_df.copy()
    sample_restaurants_df["cuisines"] = ["A", "A", "B"]
    app.config["RESTAURANTS_DF"] = sample_restaurants_df

    resp = client.get("/api/top-restaurants")
    assert resp.status_code == 200

    body = resp.get_json()
    assert body["success"] is True
    assert body["data"]["total_restaurants"] == 3
    assert len(body["data"]["top_restaurants"]) >= 1


def test_top_restaurants_rating_sort(client, app, sample_restaurants_df):
    sample_restaurants_df = sample_restaurants_df.copy()
    sample_restaurants_df["cuisines"] = ["A", "A", "B"]
    app.config["RESTAURANTS_DF"] = sample_restaurants_df

    resp = client.get("/api/top-restaurants?sort_by=rating&limit=2")
    assert resp.status_code == 200

    body = resp.get_json()
    assert body["success"] is True
    assert len(body["data"]["top_restaurants"]) == 2
