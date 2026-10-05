import os
from flask import Flask
from app.config import config_by_name
from app.extensions import db, migrate, jwt, cors, limiter
from app.utils.logging_config import configure_logging
from app.utils.responses import success_response
from app.middleware.error_handlers import register_error_handlers


def create_app(config_name=None):
    config_name = config_name or os.environ.get("FLASK_ENV", "development")
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    configure_logging(app)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config["FRONTEND_URL"]}},
                   supports_credentials=True)
    limiter.init_app(app)

    from app.middleware.jwt_handlers import register_jwt_handlers
    register_jwt_handlers(jwt)

    # Import models so they're registered on db.metadata before migrate/create_all runs
    from app import models  # noqa: F401

    # Global error handling — every exception path returns the standard envelope
    register_error_handlers(app)

    # Route blueprints (scaffolded now, filled in over upcoming phases)
    from app.routes import register_blueprints
    register_blueprints(app)

    @app.get("/api/health")
    def health():
        return success_response(
            data={"status": "ok", "env": config_name},
            message="UniVibe API is running",
        )

    return app
