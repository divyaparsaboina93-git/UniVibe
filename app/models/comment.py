from app.extensions import db
from app.models.mixins import TimestampMixin


class Comment(db.Model, TimestampMixin):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id", ondelete="CASCADE"),
                         nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"),
                         nullable=False, index=True)
    parent_comment_id = db.Column(db.Integer, db.ForeignKey("comments.id", ondelete="CASCADE"),
                                   nullable=True, index=True)  # null = top-level, set = reply

    text = db.Column(db.String(1000), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)

    replies = db.relationship(
        "Comment", backref=db.backref("parent", remote_side=[id]),
        cascade="all, delete-orphan", single_parent=True
    )
    likes = db.relationship("CommentLike", backref="comment", cascade="all, delete-orphan",
                             lazy="dynamic")

    def like_count(self):
        return self.likes.count()


class CommentLike(db.Model):
    __tablename__ = "comment_likes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"),
                         nullable=False, index=True)
    comment_id = db.Column(db.Integer, db.ForeignKey("comments.id", ondelete="CASCADE"),
                            nullable=False, index=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    __table_args__ = (
        db.UniqueConstraint("user_id", "comment_id", name="uq_commentlike_user_comment"),
    )
