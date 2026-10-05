import os
from flask import Flask, jsonify
from app.config import config_by_name
from app.extensions import db, migrate, jwt, cors, limiter


def create_app(config_name=None):
    config_name = config_name or os.environ.get("FLASK_ENV", "development")
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config["FRONTEND_URL"]}})
    limiter.init_app(app)

    # Import models so they're registered on db.metadata before migrate/create_all runs
    from app import models  # noqa: F401

    @app.get("/api/health")
    def health():
        return jsonify({"success": True, "data": {"status": "ok"}, "message": "UniVibe API is running"})

    return app
