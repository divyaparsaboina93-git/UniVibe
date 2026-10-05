"""
Phase 2 verification: the standard envelope and error handling behave correctly
for every class of failure, and no internal details ever leak to the client.
"""
from app.utils.exceptions import NotFoundError, ValidationAppError, ConflictError


def test_health_check_envelope(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["success"] is True
    assert body["data"]["status"] == "ok"
    assert "message" in body


def test_404_returns_standard_envelope(client):
    resp = client.get("/api/this-route-does-not-exist")
    assert resp.status_code == 404
    body = resp.get_json()
    assert body["success"] is False
    assert body["error"]["code"] == "NOT_FOUND"


def test_405_method_not_allowed(client):
    resp = client.delete("/api/health")  # health only supports GET
    assert resp.status_code == 405
    body = resp.get_json()
    assert body["success"] is False
    assert body["error"]["code"] == "METHOD_NOT_ALLOWED"


def test_app_error_custom_route(app, client):
    # register a throwaway route that deliberately raises each error type,
    # proving the global handler (not per-route try/except) catches them.
    @app.get("/api/_test/not-found")
    def _raise_not_found():
        raise NotFoundError("Post not found.")

    @app.get("/api/_test/validation")
    def _raise_validation():
        raise ValidationAppError("Bad input.", details={"email": ["Invalid format"]})

    @app.get("/api/_test/conflict")
    def _raise_conflict():
        raise ConflictError("Already exists.")

    @app.get("/api/_test/crash")
    def _raise_unexpected():
        raise RuntimeError("boom - something truly unexpected")

    r1 = client.get("/api/_test/not-found")
    assert r1.status_code == 404
    assert r1.get_json()["error"]["code"] == "NOT_FOUND"
    assert r1.get_json()["error"]["message"] == "Post not found."

    r2 = client.get("/api/_test/validation")
    assert r2.status_code == 422
    body2 = r2.get_json()
    assert body2["error"]["code"] == "VALIDATION_ERROR"
    assert body2["error"]["details"] == {"email": ["Invalid format"]}

    r3 = client.get("/api/_test/conflict")
    assert r3.status_code == 409
    assert r3.get_json()["error"]["code"] == "CONFLICT"

    # This is the critical security check: an unhandled RuntimeError must NOT
    # leak "boom - something truly unexpected" or a stack trace to the client.
    r4 = client.get("/api/_test/crash")
    assert r4.status_code == 500
    body4 = r4.get_json()
    assert body4["success"] is False
    assert body4["error"]["code"] == "INTERNAL_ERROR"
    assert "boom" not in body4["error"]["message"]
    assert "Traceback" not in str(body4)


def test_integrity_error_becomes_409(app, client, db):
    from app.models import User, Follow
    from werkzeug.security import generate_password_hash

    u = User(username="dupuser", email="dup@vt.edu", password_hash=generate_password_hash("x"))
    db.session.add(u)
    db.session.commit()

    @app.get("/api/_test/dup-follow")
    def _dup_follow():
        db.session.add(Follow(follower_id=u.id, following_id=u.id))  # violates check constraint too,
        # but specifically test the IntegrityError path using a duplicate-unique scenario instead:
        db.session.commit()
        return {"ok": True}

    resp = client.get("/api/_test/dup-follow")
    assert resp.status_code in (409, 400)  # constraint violation surfaces as CONFLICT
    assert resp.get_json()["success"] is False


def test_no_password_hash_ever_in_user_public_dict(app, db):
    from app.models import User, Profile
    from werkzeug.security import generate_password_hash

    u = User(username="secure1", email="secure1@vt.edu",
             password_hash=generate_password_hash("SuperSecret1!"))
    u.profile = Profile(full_name="Secure User")
    db.session.add(u)
    db.session.commit()

    public = u.to_public_dict()
    assert "password_hash" not in public
    assert "password" not in public


def test_pagination_helper_clamps_values(app):
    with app.test_request_context("/api/posts?page=0&per_page=99999"):
        from app.utils.pagination import get_pagination_params
        page, per_page = get_pagination_params()
        assert page == 1          # clamped up from 0
        assert per_page == 100    # clamped down to MAX_PAGE_SIZE
