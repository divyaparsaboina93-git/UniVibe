from app.extensions import db
from app.models.mixins import TimestampMixin

# many-to-many association: posts <-> hashtags
post_hashtags = db.Table(
    "post_hashtags",
    db.Column("post_id", db.Integer, db.ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True),
    db.Column("hashtag_id", db.Integer, db.ForeignKey("hashtags.id", ondelete="CASCADE"), primary_key=True),
)


class Post(db.Model, TimestampMixin):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"),
                           nullable=False, index=True)
    community_id = db.Column(db.Integer, db.ForeignKey("communities.id", ondelete="SET NULL"),
                              nullable=True, index=True)

    text = db.Column(db.String(2000), nullable=False, default="")
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)

    media = db.relationship("PostMedia", backref="post", cascade="all, delete-orphan",
                             order_by="PostMedia.order_index")
    hashtags = db.relationship("Hashtag", secondary=post_hashtags, backref="posts")
    comments = db.relationship("Comment", backref="post", cascade="all, delete-orphan",
                                lazy="dynamic")
    likes = db.relationship("Like", backref="post", cascade="all, delete-orphan", lazy="dynamic")
    bookmarks = db.relationship("Bookmark", backref="post", cascade="all, delete-orphan")

    __table_args__ = (
        db.Index("ix_posts_created_at", "created_at"),
    )

    def like_count(self):
        return self.likes.count()

    def comment_count(self):
        return self.comments.filter_by(is_deleted=False).count()


class PostMedia(db.Model):
    __tablename__ = "post_media"

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id", ondelete="CASCADE"),
                         nullable=False, index=True)
    url = db.Column(db.String(500), nullable=False)     # storage URL only — never a blob
    media_type = db.Column(db.String(20), nullable=False, default="image")  # image|video
    order_index = db.Column(db.Integer, default=0, nullable=False)


class Hashtag(db.Model):
    __tablename__ = "hashtags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)


class Like(db.Model):
    __tablename__ = "likes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"),
                         nullable=False, index=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id", ondelete="CASCADE"),
                         nullable=False, index=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    __table_args__ = (
        db.UniqueConstraint("user_id", "post_id", name="uq_like_user_post"),
    )
