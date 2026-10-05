from app.extensions import db

SUBJECT_CHOICES = [
    "Programming", "DBMS", "Operating Systems", "Computer Networks",
    "Theory of Computation", "Data Structures", "Artificial Intelligence",
    "Data Analytics", "Other",
]


class StudyResource(db.Model):
    __tablename__ = "study_resources"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(1000))
    subject = db.Column(db.String(50), nullable=False, index=True)

    file_url = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(20))
    uploaded_by = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"),
                             nullable=False, index=True)

    download_count = db.Column(db.Integer, default=0, nullable=False)
    is_removed = db.Column(db.Boolean, default=False, nullable=False)

    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), index=True)

    uploader = db.relationship("User")
