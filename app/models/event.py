from app.extensions import db
from app.models.mixins import TimestampMixin


class Event(db.Model, TimestampMixin):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(2000))
    date = db.Column(db.Date, nullable=False, index=True)
    time = db.Column(db.Time, nullable=True)
    location = db.Column(db.String(255))

    organizer_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"),
                              nullable=False, index=True)
    community_id = db.Column(db.Integer, db.ForeignKey("communities.id", ondelete="SET NULL"),
                              nullable=True, index=True)

    image_url = db.Column(db.String(500))
    max_attendees = db.Column(db.Integer, nullable=True)  # null = unlimited
    is_cancelled = db.Column(db.Boolean, default=False, nullable=False)

    organizer = db.relationship("User")
    attendees = db.relationship("EventAttendee", backref="event", cascade="all, delete-orphan")

    def going_count(self):
        return sum(1 for a in self.attendees if a.status == "going")


class EventAttendee(db.Model):
    __tablename__ = "event_attendees"

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id", ondelete="CASCADE"),
                          nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"),
                         nullable=False, index=True)
    status = db.Column(db.String(20), default="interested", nullable=False)  # interested|going
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    user = db.relationship("User")

    __table_args__ = (
        db.UniqueConstraint("event_id", "user_id", name="uq_event_attendee"),
    )
