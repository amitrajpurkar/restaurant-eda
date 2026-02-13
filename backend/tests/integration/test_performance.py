from __future__ import annotations

import time


def test_api_response_time_under_threshold(app, client, sample_restaurants_df):
    app.config["RESTAURANTS_DF"] = sample_restaurants_df

    start = time.perf_counter()
    resp = client.get("/api/restaurant-types")
    elapsed_ms = (time.perf_counter() - start) * 1000

    assert resp.status_code == 200
    # Keep this threshold generous to avoid flaky tests on slower dev machines.
    assert elapsed_ms < 500
