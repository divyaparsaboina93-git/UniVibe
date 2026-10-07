import os
<<<<<<< HEAD
from flask import Flask
from app.config import config_by_name
from app.extensions import db, migrate, jwt, cors, limiter
from app.utils.logging_config import configure_logging
from app.utils.responses import success_response
from app.middleware.error_handlers import register_error_handlers
=======
from flask import Flask, jsonify
from app.config import config_by_name
from app.extensions import db, migrate, jwt, cors, limiter
>>>>>>> 2d6aefa64e6d5b3e399774414281a68da48193c3


def create_app(config_name=None):
    config_name = config_name or os.environ.get("FLASK_ENV", "development")
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

<<<<<<< HEAD
    configure_logging(app)

=======
>>>>>>> 2d6aefa64e6d5b3e399774414281a68da48193c3
    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
<<<<<<< HEAD
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
=======
    cors.init_app(app, resources={r"/api/*": {"origins": app.config["FRONTEND_URL"]}})
    limiter.init_app(app)

    # Import models so they're registered on db.metadata before migrate/create_all runs
    from app import models  # noqa: F401

    @app.get("/api/health")
    def health():
        return jsonify({"success": True, "data": {"status": "ok"}, "message": "UniVibe API is running"})
>>>>>>> 2d6aefa64e6d5b3e399774414281a68da48193c3

    return app
