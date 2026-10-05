"""
Import every model here so that:
1. `from app.models import User, Post, ...` works cleanly elsewhere.
2. Flask-Migrate's autogenerate can discover all tables via db.metadata.
"""
from app.models.user import User, Profile, Session, UserRole
from app.models.post import Post, PostMedia, Hashtag, Like, post_hashtags
from app.models.comment import Comment, CommentLike
from app.models.social import Follow, Bookmark, Block, Report
from app.models.notification import Notification
from app.models.messaging import Conversation, ConversationMember, Message
from app.models.community import Community, CommunityMember
from app.models.study_resource import StudyResource, SUBJECT_CHOICES
from app.models.event import Event, EventAttendee

__all__ = [
    "User", "Profile", "Session", "UserRole",
    "Post", "PostMedia", "Hashtag", "Like", "post_hashtags",
    "Comment", "CommentLike",
    "Follow", "Bookmark", "Block", "Report",
    "Notification",
    "Conversation", "ConversationMember", "Message",
    "Community", "CommunityMember",
    "StudyResource", "SUBJECT_CHOICES",
    "Event", "EventAttendee",
]
