from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ResponseMetadata(BaseModel):
    timestamp: datetime
    processing_time_ms: int = Field(ge=0)
    request_id: str


class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    metadata: ResponseMetadata


class RestaurantTypeSummaryModel(BaseModel):
    restaurant_type: str
    count: int = Field(ge=0)
    percentage: float = Field(ge=0, le=100)
    avg_rating: Optional[float] = Field(default=None, ge=0, le=5)
    avg_cost_for_two: Optional[int] = Field(default=None, ge=0)


class RestaurantTypesData(BaseModel):
    restaurant_types: List[RestaurantTypeSummaryModel]
    total_types: int = Field(ge=0)


class RestaurantTypesResponse(BaseModel):
    success: bool = True
    data: RestaurantTypesData
    metadata: ResponseMetadata


class TopRestaurantModel(BaseModel):
    name: str
    location: str
    rating: Optional[float] = Field(default=None, ge=0, le=5)
    votes: int = Field(ge=0)
    restaurant_type: str
    cuisines: List[str]
    rank: int = Field(ge=1, le=10)


class TopRestaurantsData(BaseModel):
    top_restaurants: List[TopRestaurantModel]
    total_restaurants: int = Field(ge=0)


class TopRestaurantsResponse(BaseModel):
    success: bool = True
    data: TopRestaurantsData
    metadata: ResponseMetadata


class FoodieAreaModel(BaseModel):
    area: str
    restaurant_count: int = Field(ge=0)
    avg_rating: Optional[float] = Field(default=None, ge=0, le=5)
    top_cuisines: List[str]
    restaurant_types: List[str]


class FoodieAreasData(BaseModel):
    foodie_areas: List[FoodieAreaModel]
    total_areas: int = Field(ge=0)


class FoodieAreasResponse(BaseModel):
    success: bool = True
    data: FoodieAreasData
    metadata: ResponseMetadata


class ChartData(BaseModel):
    chart_type: str
    title: str
    base64_image: str
    width: int = Field(ge=300, le=1200)
    height: int = Field(ge=200, le=800)


class ChartResponse(BaseModel):
    success: bool = True
    data: ChartData
    metadata: ResponseMetadata


class HealthData(BaseModel):
    status: str
    uptime_seconds: int = Field(ge=0)
    memory_usage_mb: int = Field(ge=0)
    data_loaded: bool


class HealthResponse(BaseModel):
    success: bool = True
    data: HealthData
    metadata: ResponseMetadata


class SearchResultName(BaseModel):
    name: str
    location: str
    restaurant_type: str
    rating: Optional[float] = Field(default=None, ge=0, le=5)
    votes: int = Field(ge=0)


class SearchResultType(BaseModel):
    restaurant_type: str
    count: int = Field(ge=0)
    avg_rating: Optional[float] = Field(default=None, ge=0, le=5)


class SearchResultArea(BaseModel):
    area: str
    restaurant_count: int = Field(ge=0)
    avg_rating: Optional[float] = Field(default=None, ge=0, le=5)


class SearchData(BaseModel):
    query: str
    mode: str
    results: List[Any]
    total_matches: int = Field(ge=0)


class SearchResponse(BaseModel):
    success: bool = True
    data: SearchData
    metadata: ResponseMetadata


def make_response_metadata(*, request_id: str, processing_time_ms: int) -> ResponseMetadata:
    return ResponseMetadata(timestamp=datetime.utcnow(), processing_time_ms=processing_time_ms, request_id=request_id)


def make_error_response(*, request_id: str, processing_time_ms: int, error: str) -> Dict[str, Any]:
    return ErrorResponse(error=error, metadata=make_response_metadata(request_id=request_id, processing_time_ms=processing_time_ms)).model_dump(mode="json")
