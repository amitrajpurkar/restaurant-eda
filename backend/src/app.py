from __future__ import annotations

import sys

import os
import logging
import json
import time
from pathlib import Path
from typing import Optional

from flask import Flask, g, jsonify, render_template, request

if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.api.routes import api_bp
from src.services.data_loader import load_zomato_csv


def _load_dotenv(dotenv_path: Path) -> None:
    if not dotenv_path.exists():
        return
    try:
        for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value
    except Exception:
        return


def _configure_logging() -> None:
    root = logging.getLogger()
    if root.handlers:
        return
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    root.addHandler(handler)
    root.setLevel(logging.INFO)


def create_app() -> Flask:
    repo_root = Path(__file__).resolve().parents[2]
    frontend_dir = repo_root / "frontend"

    _load_dotenv(repo_root / "backend" / ".env")
    _configure_logging()

    app = Flask(
        __name__,
        template_folder=str(frontend_dir / "templates"),
        static_folder=str(frontend_dir / "static"),
        static_url_path="/static",
    )

    app.config["START_TIME"] = time.time()

    data_path = os.environ.get("DATA_FILE_PATH")
    if data_path is None:
        backend_data = repo_root / "backend" / "data" / "zomato.csv"
        repo_data = repo_root / "data" / "zomato.csv"
        if backend_data.exists():
            data_path = str(backend_data)
        else:
            data_path = str(repo_data)

    restaurants_df = None
    try:
        loaded = load_zomato_csv(data_path)
        restaurants_df = loaded.restaurants_df
    except Exception:
        restaurants_df = None

    app.config["RESTAURANTS_DF"] = restaurants_df

    app.register_blueprint(api_bp)

    @app.before_request
    def _before_request():
        g.request_id = request.headers.get("X-Request-ID") or os.urandom(16).hex()
        g.start_time = time.time()

        logging.getLogger(__name__).info(
            json.dumps(
                {
                    "event": "request.start",
                    "request_id": g.request_id,
                    "method": request.method,
                    "path": request.path,
                }
            )
        )

    @app.after_request
    def _after_request(response):
        duration_ms = int((time.time() - getattr(g, "start_time", time.time())) * 1000)
        response.headers["X-Request-ID"] = getattr(g, "request_id", "")
        response.headers["X-Processing-Time-ms"] = str(duration_ms)

        logging.getLogger(__name__).info(
            json.dumps(
                {
                    "event": "request.end",
                    "request_id": getattr(g, "request_id", ""),
                    "method": request.method,
                    "path": request.path,
                    "status_code": response.status_code,
                    "processing_time_ms": duration_ms,
                }
            )
        )
        return response

    @app.errorhandler(Exception)
    def _handle_unexpected_error(exc: Exception):
        request_id = getattr(g, "request_id", os.urandom(16).hex())
        duration_ms = int((time.time() - getattr(g, "start_time", time.time())) * 1000)

        logging.getLogger(__name__).error(
            json.dumps(
                {
                    "event": "request.error",
                    "request_id": request_id,
                    "path": request.path,
                    "error": str(exc),
                }
            )
        )

        return (
            jsonify(
                {
                    "success": False,
                    "error": "Internal server error",
                    "metadata": {
                        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        "processing_time_ms": duration_ms,
                        "request_id": request_id,
                    },
                }
            ),
            500,
        )

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/top-restaurants")
    def drilldown_restaurants():
        return render_template("drilldown_restaurants.html")

    @app.get("/top-foodie-areas")
    def drilldown_foodie_areas():
        return render_template("drilldown_foodie_areas.html")

    @app.get("/top-restaurant-types")
    def drilldown_restaurant_types():
        return render_template("drilldown_restaurant_types.html")

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("FLASK_PORT", "5000"))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() in {"1", "true", "yes"}
    app.run(host="127.0.0.1", port=port, debug=debug)
