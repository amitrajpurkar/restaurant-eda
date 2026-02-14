"""Integration tests for HTML pages — home dashboard + drill-down pages."""
from __future__ import annotations

import pytest
from flask.testing import FlaskClient

from src.app import create_app


@pytest.fixture()
def client() -> FlaskClient:
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


class TestHomePage:
    """T008: Home page renders dashboard with search panel and 3 tiles."""

    def test_home_returns_200(self, client: FlaskClient) -> None:
        resp = client.get("/")
        assert resp.status_code == 200

    def test_home_contains_dashboard_title(self, client: FlaskClient) -> None:
        resp = client.get("/")
        html = resp.data.decode()
        assert "Belangaru Restaurant Dashboard" in html

    def test_home_contains_search_form(self, client: FlaskClient) -> None:
        resp = client.get("/")
        html = resp.data.decode()
        assert "search" in html.lower()
        assert "<form" in html.lower() or "id=\"search" in html.lower()

    def test_home_contains_three_tile_links(self, client: FlaskClient) -> None:
        resp = client.get("/")
        html = resp.data.decode()
        assert "/top-restaurants" in html
        assert "/top-foodie-areas" in html
        assert "/top-restaurant-types" in html

    def test_home_contains_tile_titles(self, client: FlaskClient) -> None:
        resp = client.get("/")
        html = resp.data.decode()
        assert "Top 10 Restaurants" in html
        assert "Top 10 Foodie Areas" in html
        assert "Top 10 Restaurant Types" in html


class TestSearchUIFlow:
    """T009: Search form submits to /api/search, results area exists."""

    def test_home_has_search_input(self, client: FlaskClient) -> None:
        resp = client.get("/")
        html = resp.data.decode()
        assert 'id="search-query"' in html or 'name="q"' in html

    def test_home_has_mode_selector(self, client: FlaskClient) -> None:
        resp = client.get("/")
        html = resp.data.decode()
        assert "name" in html.lower()
        assert "type" in html.lower()
        assert "area" in html.lower()

    def test_home_has_results_area(self, client: FlaskClient) -> None:
        resp = client.get("/")
        html = resp.data.decode()
        assert 'id="search-results"' in html


class TestDrilldownRestaurantsPage:
    """T014: Drill-down page for top restaurants."""

    def test_returns_200(self, client: FlaskClient) -> None:
        resp = client.get("/top-restaurants")
        assert resp.status_code == 200

    def test_contains_chart_container(self, client: FlaskClient) -> None:
        resp = client.get("/top-restaurants")
        html = resp.data.decode()
        assert 'id="chart-container"' in html or "chart" in html.lower()

    def test_contains_items_grid(self, client: FlaskClient) -> None:
        resp = client.get("/top-restaurants")
        html = resp.data.decode()
        assert 'id="items-grid"' in html or "items" in html.lower()


class TestDrilldownFoodieAreasPage:
    """T015: Drill-down page for top foodie areas."""

    def test_returns_200(self, client: FlaskClient) -> None:
        resp = client.get("/top-foodie-areas")
        assert resp.status_code == 200

    def test_contains_chart_container(self, client: FlaskClient) -> None:
        resp = client.get("/top-foodie-areas")
        html = resp.data.decode()
        assert 'id="chart-container"' in html or "chart" in html.lower()

    def test_contains_items_grid(self, client: FlaskClient) -> None:
        resp = client.get("/top-foodie-areas")
        html = resp.data.decode()
        assert 'id="items-grid"' in html or "items" in html.lower()


class TestDrilldownRestaurantTypesPage:
    """T016: Drill-down page for top restaurant types."""

    def test_returns_200(self, client: FlaskClient) -> None:
        resp = client.get("/top-restaurant-types")
        assert resp.status_code == 200

    def test_contains_chart_container(self, client: FlaskClient) -> None:
        resp = client.get("/top-restaurant-types")
        html = resp.data.decode()
        assert 'id="chart-container"' in html or "chart" in html.lower()

    def test_contains_items_grid(self, client: FlaskClient) -> None:
        resp = client.get("/top-restaurant-types")
        html = resp.data.decode()
        assert 'id="items-grid"' in html or "items" in html.lower()


class TestNavigationBackToDashboard:
    """T023: All drill-down pages contain a link to / with text 'Belangaru Restaurant Dashboard'."""

    def test_restaurants_has_dashboard_link(self, client: FlaskClient) -> None:
        resp = client.get("/top-restaurants")
        html = resp.data.decode()
        assert "Belangaru Restaurant Dashboard" in html
        assert 'href="/"' in html or "href=\"/\"" in html

    def test_foodie_areas_has_dashboard_link(self, client: FlaskClient) -> None:
        resp = client.get("/top-foodie-areas")
        html = resp.data.decode()
        assert "Belangaru Restaurant Dashboard" in html
        assert 'href="/"' in html or "href=\"/\"" in html

    def test_restaurant_types_has_dashboard_link(self, client: FlaskClient) -> None:
        resp = client.get("/top-restaurant-types")
        html = resp.data.decode()
        assert "Belangaru Restaurant Dashboard" in html
        assert 'href="/"' in html or "href=\"/\"" in html
