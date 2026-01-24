from __future__ import annotations

import os
import time
import uuid
from datetime import datetime
from time import perf_counter
from typing import Any, Dict

from flask import Blueprint, current_app, jsonify

from src.api.schemas import (
    HealthData,
    HealthResponse,
    RestaurantTypesData,
    RestaurantTypesResponse,
    make_error_response,
    make_response_metadata,
)
from src.services.analytics import compute_restaurant_type_summary


api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.get("/health")
def get_health():
    request_id = str(uuid.uuid4())
    start = perf_counter()

    data_loaded = current_app.config.get("RESTAURANTS_DF") is not None

    try:
        import psutil  # type: ignore

        process = psutil.Process(os.getpid())
        mem_mb = int(process.memory_info().rss / 1024 / 1024)
    except Exception:
        mem_mb = 0

    uptime_seconds = int(time.time() - current_app.config.get("START_TIME", time.time()))

    payload = HealthResponse(
        data=HealthData(
            status="healthy",
            uptime_seconds=uptime_seconds,
            memory_usage_mb=mem_mb,
            data_loaded=data_loaded,
        ),
        metadata=make_response_metadata(
            request_id=request_id, processing_time_ms=int((perf_counter() - start) * 1000)
        ),
    )

    return jsonify(payload.model_dump(mode="json"))


@api_bp.get("/restaurant-types")
def get_restaurant_types():
    request_id = str(uuid.uuid4())
    start = perf_counter()

    restaurants_df = current_app.config.get("RESTAURANTS_DF")
    if restaurants_df is None:
        return jsonify(
            make_error_response(
                request_id=request_id,
                processing_time_ms=int((perf_counter() - start) * 1000),
                error="Restaurant data not loaded",
            )
        ), 500

    try:
        result = compute_restaurant_type_summary(restaurants_df)

        payload = RestaurantTypesResponse(
            data=RestaurantTypesData(
                restaurant_types=[
                    {
                        "restaurant_type": item.restaurant_type,
                        "count": item.count,
                        "percentage": item.percentage,
                        "avg_rating": item.avg_rating,
                        "avg_cost_for_two": item.avg_cost_for_two,
                    }
                    for item in result.restaurant_types
                ],
                total_types=len(result.restaurant_types),
            ),
            metadata=make_response_metadata(
                request_id=request_id, processing_time_ms=int((perf_counter() - start) * 1000)
            ),
        )
        return jsonify(payload.model_dump(mode="json"))
    except Exception as exc:
        return jsonify(
            make_error_response(
                request_id=request_id,
                processing_time_ms=int((perf_counter() - start) * 1000),
                error=str(exc),
            )
        ), 500
