from app.extensions import db


class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"),
                              nullable=False, index=True)
    actor_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"),
                          nullable=True)  # who triggered it (null for system notifications)

    # follow|like|comment|reply|share|message|community_invite|event_update
    type = db.Column(db.String(30), nullable=False)

    # what it's about, e.g. object_type="post", object_id=42
    object_type = db.Column(db.String(30), nullable=True)
    object_id = db.Column(db.Integer, nullable=True)

    is_read = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    recipient = db.relationship("User", foreign_keys=[recipient_id])
    actor = db.relationship("User", foreign_keys=[actor_id])

    __table_args__ = (
        db.Index("ix_notifications_recipient_read", "recipient_id", "is_read"),
    )
