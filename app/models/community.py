from app.extensions import db
from app.models.mixins import TimestampMixin


class Community(db.Model, TimestampMixin):
    __tablename__ = "communities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False, index=True)
    description = db.Column(db.String(500))
    image_url = db.Column(db.String(500))
    creator_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"),
                            nullable=True)
    is_removed = db.Column(db.Boolean, default=False, nullable=False)  # admin moderation

    creator = db.relationship("User", foreign_keys=[creator_id])
    members = db.relationship("CommunityMember", backref="community",
                               cascade="all, delete-orphan")
    posts = db.relationship("Post", backref="community", lazy="dynamic")
    events = db.relationship("Event", backref="community", lazy="dynamic")

    def member_count(self):
        return len(self.members)


class CommunityMember(db.Model):
    __tablename__ = "community_members"

    id = db.Column(db.Integer, primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey("communities.id", ondelete="CASCADE"),
                              nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"),
                         nullable=False, index=True)
    role = db.Column(db.String(20), default="member", nullable=False)  # owner|moderator|member
    joined_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    user = db.relationship("User")

    __table_args__ = (
        db.UniqueConstraint("community_id", "user_id", name="uq_community_member"),
    )
