from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True, slots=True)
class RestaurantTypeSummary:
    restaurant_type: str
    count: int
    percentage: float
    avg_rating: Optional[float]
    avg_cost_for_two: Optional[int]


@dataclass(frozen=True, slots=True)
class TopRestaurant:
    name: str
    location: str
    rating: Optional[float]
    votes: int
    restaurant_type: str
    cuisines: List[str]
    rank: int
