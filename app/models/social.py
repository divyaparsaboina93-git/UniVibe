from app.extensions import db


class Follow(db.Model):
    __tablename__ = "follows"

    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"),
                             nullable=False, index=True)
    following_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"),
                              nullable=False, index=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    follower = db.relationship("User", foreign_keys=[follower_id],
                                backref=db.backref("following_links", lazy="dynamic"))
    following = db.relationship("User", foreign_keys=[following_id],
                                 backref=db.backref("follower_links", lazy="dynamic"))

    __table_args__ = (
        db.UniqueConstraint("follower_id", "following_id", name="uq_follow_pair"),
        db.CheckConstraint("follower_id != following_id", name="ck_no_self_follow"),
    )


class Bookmark(db.Model):
    __tablename__ = "bookmarks"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"),
                         nullable=False, index=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id", ondelete="CASCADE"),
                         nullable=False, index=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    __table_args__ = (
        db.UniqueConstraint("user_id", "post_id", name="uq_bookmark_user_post"),
    )


class Block(db.Model):
    __tablename__ = "blocks"

    id = db.Column(db.Integer, primary_key=True)
    blocker_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"),
                            nullable=False, index=True)
    blocked_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"),
                            nullable=False, index=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    __table_args__ = (
        db.UniqueConstraint("blocker_id", "blocked_id", name="uq_block_pair"),
        db.CheckConstraint("blocker_id != blocked_id", name="ck_no_self_block"),
    )


class Report(db.Model):
    __tablename__ = "reports"

    id = db.Column(db.Integer, primary_key=True)
    reporter_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"),
                             nullable=False, index=True)

    target_type = db.Column(db.String(20), nullable=False)   # post|comment|user|community|message
    target_id = db.Column(db.Integer, nullable=False)

    reason = db.Column(db.String(30), nullable=False)  # spam|harassment|hate|inappropriate|fake_account|other
    details = db.Column(db.String(500))

    status = db.Column(db.String(20), default="pending", nullable=False)  # pending|reviewed|resolved|rejected
    reviewed_by = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    resolved_at = db.Column(db.DateTime(timezone=True), nullable=True)

    __table_args__ = (
        db.Index("ix_reports_target", "target_type", "target_id"),
        db.Index("ix_reports_status", "status"),
    )
