"""
Registers Flask error handlers so EVERY error path in the app — expected
(AppError subclasses), framework-level (404/405/400 from Werkzeug), validation
(Marshmallow), or truly unexpected (any other Exception) — returns the same
JSON envelope shape and never leaks stack traces / internals to the client.

Unexpected errors are logged server-side with full detail; the client only
ever sees a generic "Something went wrong" message + an INTERNAL_ERROR code.
"""
import logging
from marshmallow import ValidationError as MarshmallowValidationError
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.utils.exceptions import AppError
from app.utils.responses import error_response

logger = logging.getLogger("univibe")


def register_error_handlers(app):

    @app.errorhandler(AppError)
    def handle_app_error(err):
        return error_response(err.code, err.message, err.status_code, err.details)

    @app.errorhandler(MarshmallowValidationError)
    def handle_marshmallow_validation(err):
        # err.messages is a dict like {"email": ["Not a valid email address."]}
        return error_response("VALIDATION_ERROR", "Invalid input.", 422, details=err.messages)

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(err):
        from app.extensions import db
        db.session.rollback()
        logger.warning("IntegrityError: %s", err)
        # Most common cause in this app: a UNIQUE/CHECK constraint (dup like, dup follow, etc.)
        return error_response(
            "CONFLICT",
            "This action conflicts with existing data (e.g. duplicate entry).",
            409,
        )

    @app.errorhandler(SQLAlchemyError)
    def handle_db_error(err):
        from app.extensions import db
        db.session.rollback()
        logger.error("Database error: %s", err, exc_info=True)
        return error_response("DATABASE_ERROR", "A database error occurred.", 500)

    @app.errorhandler(404)
    def handle_404(err):
        return error_response("NOT_FOUND", "The requested resource was not found.", 404)

    @app.errorhandler(405)
    def handle_405(err):
        return error_response("METHOD_NOT_ALLOWED", "This HTTP method is not allowed here.", 405)

    @app.errorhandler(400)
    def handle_400(err):
        return error_response("BAD_REQUEST", "The request could not be understood.", 400)

    @app.errorhandler(413)
    def handle_413(err):
        return error_response(
            "PAYLOAD_TOO_LARGE", "The uploaded file or request body is too large.", 413
        )

    @app.errorhandler(429)
    def handle_429(err):
        return error_response(
            "RATE_LIMITED", "Too many requests. Please slow down and try again shortly.", 429
        )

    @app.errorhandler(HTTPException)
    def handle_http_exception(err):
        # Catch-all for any other Werkzeug HTTP exception not explicitly listed above
        return error_response(
            err.name.upper().replace(" ", "_"), err.description or err.name, err.code
        )

    @app.errorhandler(Exception)
    def handle_unexpected_error(err):
        # Last resort: something we didn't anticipate. Log full detail server-side,
        # tell the client nothing beyond "something went wrong".
        logger.error("Unhandled exception: %s", err, exc_info=True)
        return error_response(
            "INTERNAL_ERROR", "Something went wrong. Please try again.", 500
        )
