from __future__ import annotations

import base64
import io
from dataclasses import dataclass
from typing import List

from src.models.analytics import TopRestaurant


@dataclass(frozen=True, slots=True)
class ChartImage:
    title: str
    base64_image: str


def top_restaurants_bar_chart(
    top_restaurants: List[TopRestaurant], *, width: int = 800, height: int = 400
) -> ChartImage:
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as exc:  # pragma: no cover
        raise RuntimeError(
            "Chart generation requires matplotlib. Install it in your environment to use charts."
        ) from exc

    fig_w = max(3.0, width / 100.0)
    fig_h = max(2.0, height / 100.0)

    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=100)

    title = "Top Restaurants"
    ax.set_title(title)

    if not top_restaurants:
        ax.text(0.5, 0.5, "No data", ha="center", va="center")
        ax.set_axis_off()
    else:
        names = [f"#{r.rank} {r.name}" for r in top_restaurants]
        votes = [r.votes for r in top_restaurants]

        ax.barh(names[::-1], votes[::-1])
        ax.set_xlabel("Votes")

    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png")
    plt.close(fig)

    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return ChartImage(title=title, base64_image=b64)
