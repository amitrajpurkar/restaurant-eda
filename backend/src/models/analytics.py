from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True)
class RestaurantTypeSummary:
    restaurant_type: str
    count: int
    percentage: float
    avg_rating: Optional[float]
    avg_cost_for_two: Optional[int]
