from __future__ import annotations

import time
import uuid
from time import perf_counter
from typing import Any, Dict

from flask import Blueprint, current_app, g, jsonify, request

from src.api.schemas import (
    ChartData,
    ChartResponse,
    FoodieAreasData,
    FoodieAreasResponse,
    HealthData,
    HealthResponse,
    RestaurantTypesData,
    RestaurantTypesResponse,
    TopRestaurantsData,
    TopRestaurantsResponse,
    make_error_response,
    make_response_metadata,
)
from src.services.analytics import (
    get_foodie_areas_cached,
    get_restaurant_type_summary_cached,
    get_top_restaurants_cached,
)
from src.utils.charts import foodie_areas_bar_chart, restaurant_types_pie_chart, top_restaurants_bar_chart


api_bp = Blueprint("api", __name__, url_prefix="/api")


def _get_cache() -> Dict[str, Any]:
    cache = current_app.config.setdefault("API_CACHE", {})
    if isinstance(cache, dict):
        return cache
    current_app.config["API_CACHE"] = {}
    return current_app.config["API_CACHE"]


def _cache_get(key: str) -> Any | None:
    cache = _get_cache()
    item = cache.get(key)
    if not item:
        return None
    ts = item.get("ts")
    ttl = item.get("ttl")
    if not isinstance(ts, (int, float)) or not isinstance(ttl, (int, float)):
        return None
    if time.time() - ts > ttl:
        cache.pop(key, None)
        return None
    return item.get("value")


def _cache_set(key: str, value: Any, *, ttl: int = 300) -> None:
    cache = _get_cache()
    cache[key] = {"ts": time.time(), "ttl": ttl, "value": value}


@api_bp.get("/health")
def get_health():
    request_id = getattr(g, "request_id", str(uuid.uuid4()))
    start = perf_counter()

    data_loaded = current_app.config.get("RESTAURANTS_DF") is not None

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
    request_id = getattr(g, "request_id", str(uuid.uuid4()))
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
        result = get_restaurant_type_summary_cached(restaurants_df)

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


@api_bp.get("/charts/<chart_type>")
def get_chart(chart_type: str):
    request_id = getattr(g, "request_id", str(uuid.uuid4()))
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

    width_raw = request.args.get("width", "800")
    height_raw = request.args.get("height", "400")

    try:
        width = int(width_raw)
        height = int(height_raw)
    except ValueError:
        return jsonify(
            make_error_response(
                request_id=request_id,
                processing_time_ms=int((perf_counter() - start) * 1000),
                error="Invalid parameter: width and height must be integers",
            )
        ), 400

    if width < 300 or width > 1200 or height < 200 or height > 800:
        return jsonify(
            make_error_response(
                request_id=request_id,
                processing_time_ms=int((perf_counter() - start) * 1000),
                error="Invalid parameter: width must be 300-1200 and height must be 200-800",
            )
        ), 400

    valid_types = {"restaurant-types-pie", "top-restaurants-bar", "foodie-areas-bar"}
    if chart_type not in valid_types:
        return jsonify(
            make_error_response(
                request_id=request_id,
                processing_time_ms=int((perf_counter() - start) * 1000),
                error=f"Chart type '{chart_type}' not found",
            )
        ), 404

    cache_key = f"chart:{chart_type}:{width}:{height}"  # intentionally not including data hash
    cached = _cache_get(cache_key)
    if cached is not None:
        payload = ChartResponse(
            data=ChartData(**cached),
            metadata=make_response_metadata(
                request_id=request_id, processing_time_ms=int((perf_counter() - start) * 1000)
            ),
        )
        return jsonify(payload.model_dump(mode="json"))

    try:
        if chart_type == "restaurant-types-pie":
            analytics_key = "analytics:restaurant-types"
            result = _cache_get(analytics_key)
            if result is None:
                result = get_restaurant_type_summary_cached(restaurants_df)
                _cache_set(analytics_key, result, ttl=300)
            chart = restaurant_types_pie_chart(result.restaurant_types, width=width, height=height)
        elif chart_type == "top-restaurants-bar":
            analytics_key = "analytics:top-restaurants"
            result = _cache_get(analytics_key)
            if result is None:
                result = get_top_restaurants_cached(restaurants_df)
                _cache_set(analytics_key, result, ttl=300)
            chart = top_restaurants_bar_chart(result.top_restaurants, width=width, height=height)
        else:
            analytics_key = "analytics:foodie-areas"
            result = _cache_get(analytics_key)
            if result is None:
                result = get_foodie_areas_cached(restaurants_df)
                _cache_set(analytics_key, result, ttl=300)
            chart = foodie_areas_bar_chart(result.foodie_areas, width=width, height=height)

        chart_payload = {
            "chart_type": chart_type,
            "title": chart.title,
            "base64_image": chart.base64_image,
            "width": width,
            "height": height,
        }
        _cache_set(cache_key, chart_payload, ttl=300)

        payload = ChartResponse(
            data=ChartData(**chart_payload),
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


@api_bp.get("/foodie-areas")
def get_foodie_areas():
    request_id = getattr(g, "request_id", str(uuid.uuid4()))
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

    if limit < 1 or limit > 20:
        return jsonify(
            make_error_response(
                request_id=request_id,
                processing_time_ms=int((perf_counter() - start) * 1000),
                error="Invalid parameter: limit must be between 1 and 20",
            )
        ), 400

    try:
        result = get_foodie_areas_cached(restaurants_df, limit=limit)  # type: ignore[arg-type]

        payload = FoodieAreasResponse(
            data=FoodieAreasData(
                foodie_areas=[
                    {
                        "area": item.area,
                        "restaurant_count": item.restaurant_count,
                        "avg_rating": item.avg_rating,
                        "top_cuisines": item.top_cuisines,
                        "restaurant_types": item.restaurant_types,
                    }
                    for item in result.foodie_areas
                ],
                total_areas=result.total_areas,
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
    request_id = getattr(g, "request_id", str(uuid.uuid4()))
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
        result = get_top_restaurants_cached(restaurants_df, limit=limit, sort_by=sort_by)  # type: ignore[arg-type]

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
