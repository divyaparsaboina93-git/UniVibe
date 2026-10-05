"""
search routes — Blueprint scaffold.
Endpoints for this domain are implemented in a later build phase (see
01-ARCHITECTURE-PLAN.md phase table). Registered now so the app structure,
URL prefixing, and blueprint wiring are correct from the start.
"""
from flask import Blueprint

bp = Blueprint("search", __name__, url_prefix="/api/search")
