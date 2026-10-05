from app.extensions import db


class Conversation(db.Model):
    __tablename__ = "conversations"

    id = db.Column(db.Integer, primary_key=True)
    is_group = db.Column(db.Boolean, default=False, nullable=False)
    title = db.Column(db.String(100), nullable=True)  # only used for group conversations
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    members = db.relationship("ConversationMember", backref="conversation",
                               cascade="all, delete-orphan")
    messages = db.relationship("Message", backref="conversation",
                                cascade="all, delete-orphan", lazy="dynamic",
                                order_by="Message.created_at")


class ConversationMember(db.Model):
    __tablename__ = "conversation_members"

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey("conversations.id", ondelete="CASCADE"),
                                 nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"),
                         nullable=False, index=True)
    joined_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    user = db.relationship("User")

    __table_args__ = (
        db.UniqueConstraint("conversation_id", "user_id", name="uq_conversation_member"),
    )


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey("conversations.id", ondelete="CASCADE"),
                                 nullable=False, index=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"),
                           nullable=False, index=True)

    text = db.Column(db.String(2000), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)

    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), index=True)
    read_at = db.Column(db.DateTime(timezone=True), nullable=True)

    sender = db.relationship("User")
