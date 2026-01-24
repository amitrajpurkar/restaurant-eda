from __future__ import annotations

import sys

import os
import time
from pathlib import Path
from typing import Optional

from flask import Flask, render_template

if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.api.routes import api_bp
from src.services.data_loader import load_zomato_csv


def create_app() -> Flask:
    repo_root = Path(__file__).resolve().parents[2]
    frontend_dir = repo_root / "frontend"

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

    @app.get("/")
    def index():
        return render_template("index.html")

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("FLASK_PORT", "5000"))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() in {"1", "true", "yes"}
    app.run(host="127.0.0.1", port=port, debug=debug)
