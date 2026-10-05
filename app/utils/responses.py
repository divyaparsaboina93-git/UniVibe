"""
Every API response follows the same envelope, per the project spec:

Success: {"success": true,  "data": {...}, "message": "..."}
Error:   {"success": false, "error": {"code": "...", "message": "...", "details": {...}}}

Routes should use these helpers instead of building raw jsonify() responses,
so the shape stays consistent across all ~60 endpoints.
"""
from flask import jsonify


def success_response(data=None, message="Success", status_code=200, meta=None):
    body = {"success": True, "data": data if data is not None else {}, "message": message}
    if meta is not None:
        body["meta"] = meta  # e.g. pagination info: {"page": 1, "per_page": 20, "total": 134}
    return jsonify(body), status_code


def error_response(code, message, status_code=400, details=None):
    error = {"code": code, "message": message}
    if details is not None:
        error["details"] = details
    return jsonify({"success": False, "error": error}), status_code


def paginated_response(items, page, per_page, total, message="Success"):
    return success_response(
        data=items,
        message=message,
        meta={
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": (total + per_page - 1) // per_page if per_page else 0,
            "has_next": page * per_page < total,
        },
    )
