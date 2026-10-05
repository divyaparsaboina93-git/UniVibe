import enum
import uuid
from app.extensions import db
from app.models.mixins import TimestampMixin, utcnow


class UserRole(str, enum.Enum):
    STUDENT = "student"
    MODERATOR = "moderator"
    ADMIN = "admin"


class User(db.Model, TimestampMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.STUDENT, nullable=False)

    is_active = db.Column(db.Boolean, default=True, nullable=False)      # False = deactivated/suspended
    is_verified = db.Column(db.Boolean, default=False, nullable=False)   # email verification
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)    # soft delete

    # Relationships
    profile = db.relationship(
        "Profile", backref="user", uselist=False, cascade="all, delete-orphan"
    )
    posts = db.relationship("Post", backref="author", lazy="dynamic",
                             foreign_keys="Post.author_id")
    comments = db.relationship("Comment", backref="author", lazy="dynamic")
    sessions = db.relationship("Session", backref="user", cascade="all, delete-orphan")

    def to_public_dict(self):
        """Safe representation — NEVER includes password_hash."""
        p = self.profile
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role.value if self.role else None,
            "is_verified": self.is_verified,
            "full_name": p.full_name if p else None,
            "avatar_url": p.avatar_url if p else None,
            "college": p.college if p else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<User {self.username}>"


class Profile(db.Model, TimestampMixin):
    __tablename__ = "profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"),
        unique=True, nullable=False, index=True
    )

    full_name = db.Column(db.String(100), nullable=False)
    avatar_url = db.Column(db.String(500))
    cover_url = db.Column(db.String(500))
    bio = db.Column(db.String(300))

    college = db.Column(db.String(150))
    department = db.Column(db.String(150))
    academic_year = db.Column(db.String(30))   # e.g. "2nd Year", "Freshman"
    skills = db.Column(db.JSON, default=list)  # list[str]; JSON type works on both Postgres and SQLite (tests)
    website = db.Column(db.String(255))

    is_private = db.Column(db.Boolean, default=False, nullable=False)
    who_can_message = db.Column(db.String(20), default="everyone")   # everyone|followers|nobody
    who_can_follow = db.Column(db.String(20), default="everyone")    # everyone|approval_required


class Session(db.Model):
    """Refresh-token session, so logout / 'log out all devices' is real, not just client-side."""
    __tablename__ = "sessions"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"),
                         nullable=False, index=True)
    refresh_token_hash = db.Column(db.String(255), nullable=False)
    device_info = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)
    expires_at = db.Column(db.DateTime(timezone=True), nullable=False)
    revoked = db.Column(db.Boolean, default=False, nullable=False)
