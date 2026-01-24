from __future__ import annotations

import os
import time
import uuid
from datetime import datetime
from time import perf_counter
from typing import Any, Dict

from flask import Blueprint, current_app, jsonify, request

from src.api.schemas import (
    HealthData,
    HealthResponse,
    RestaurantTypesData,
    RestaurantTypesResponse,
    TopRestaurantsData,
    TopRestaurantsResponse,
    make_error_response,
    make_response_metadata,
)
from src.services.analytics import compute_restaurant_type_summary, compute_top_restaurants


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


@api_bp.get("/top-restaurants")
def get_top_restaurants():
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

    limit_raw = request.args.get("limit", "10")
    sort_by = request.args.get("sort_by", "votes")

    try:
        limit = int(limit_raw)
    except ValueError:
        return jsonify(
            make_error_response(
                request_id=request_id,
                processing_time_ms=int((perf_counter() - start) * 1000),
                error="Invalid parameter: limit must be an integer",
            )
        ), 400

    if limit < 1 or limit > 10:
        return jsonify(
            make_error_response(
                request_id=request_id,
                processing_time_ms=int((perf_counter() - start) * 1000),
                error="Invalid parameter: limit must be between 1 and 10",
            )
        ), 400

    if sort_by not in {"votes", "rating"}:
        return jsonify(
            make_error_response(
                request_id=request_id,
                processing_time_ms=int((perf_counter() - start) * 1000),
                error="Invalid parameter: sort_by must be one of: votes, rating",
            )
        ), 400

    try:
        result = compute_top_restaurants(restaurants_df, limit=limit, sort_by=sort_by)  # type: ignore[arg-type]

        payload = TopRestaurantsResponse(
            data=TopRestaurantsData(
                top_restaurants=[
                    {
                        "name": item.name,
                        "location": item.location,
                        "rating": item.rating,
                        "votes": item.votes,
                        "restaurant_type": item.restaurant_type,
                        "cuisines": item.cuisines,
                        "rank": item.rank,
                    }
                    for item in result.top_restaurants
                ],
                total_restaurants=result.total_restaurants,
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
