"""
Flask-JWT-Extended requires its callbacks to be registered on the JWTManager
instance directly (they don't go through Flask's normal @app.errorhandler).
Registered here so unauthorized/expired/invalid token responses match the
same {"success": false, "error": {...}} envelope as everything else in the app.
Actual token issuing/validation logic (login, refresh, blocklist) is built in
the Authentication phase — this only standardizes the failure responses.
"""
from app.utils.responses import error_response


def register_jwt_handlers(jwt):

    @jwt.unauthorized_loader
    def missing_token(reason):
        return error_response("UNAUTHORIZED", "Authentication is required for this action.", 401)

    @jwt.invalid_token_loader
    def invalid_token(reason):
        return error_response("INVALID_TOKEN", "The provided authentication token is invalid.", 401)

    @jwt.expired_token_loader
    def expired_token(jwt_header, jwt_payload):
        return error_response("TOKEN_EXPIRED", "Your session has expired. Please log in again.", 401)

    @jwt.revoked_token_loader
    def revoked_token(jwt_header, jwt_payload):
        return error_response("TOKEN_REVOKED", "This session has been logged out.", 401)

    @jwt.needs_fresh_token_loader
    def needs_fresh_token(jwt_header, jwt_payload):
        return error_response("FRESH_TOKEN_REQUIRED", "Please re-authenticate to continue.", 401)
