"""
Custom exceptions for expected, "normal" failure conditions (bad input, not found,
unauthorized, etc). Routes/services raise these; the global error handler in
app/middleware/error_handlers.py converts them into the standard JSON envelope
with the right HTTP status code.

Unhandled exceptions (real bugs) are caught separately and turned into a generic
500 response that never leaks internals to the client.
"""


class AppError(Exception):
    status_code = 400
    code = "APP_ERROR"

    def __init__(self, message="An error occurred", code=None, status_code=None, details=None):
        super().__init__(message)
        self.message = message
        self.code = code or self.code
        self.status_code = status_code or self.status_code
        self.details = details  # optional extra machine-readable info (e.g. field errors)


class ValidationAppError(AppError):
    status_code = 422
    code = "VALIDATION_ERROR"


class NotFoundError(AppError):
    status_code = 404
    code = "NOT_FOUND"


class UnauthorizedError(AppError):
    status_code = 401
    code = "UNAUTHORIZED"


class ForbiddenError(AppError):
    status_code = 403
    code = "FORBIDDEN"


class ConflictError(AppError):
    status_code = 409
    code = "CONFLICT"


class RateLimitedError(AppError):
    status_code = 429
    code = "RATE_LIMITED"
