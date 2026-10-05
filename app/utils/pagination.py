from flask import request

DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


def get_pagination_params():
    """Reads ?page=&per_page= from the query string with sane, clamped defaults.
    Never trusts the client for an unbounded per_page (protects against someone
    requesting 1,000,000 rows in one call)."""
    try:
        page = max(1, int(request.args.get("page", 1)))
    except (TypeError, ValueError):
        page = 1
    try:
        per_page = int(request.args.get("per_page", DEFAULT_PAGE_SIZE))
    except (TypeError, ValueError):
        per_page = DEFAULT_PAGE_SIZE
    per_page = max(1, min(per_page, MAX_PAGE_SIZE))
    return page, per_page


def paginate_query(query, page, per_page):
    """Applies LIMIT/OFFSET at the DB level (never loads the full table into memory)."""
    total = query.order_by(None).count()  # order_by(None) avoids issues counting ordered queries
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    return items, total
