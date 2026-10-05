import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/univibe"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-jwt-secret-change-me")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES_MIN", 15))
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(os.environ.get("JWT_REFRESH_TOKEN_EXPIRES_DAYS", 30))
    )
    JWT_TOKEN_LOCATION = ["headers"]

    UPLOADS_DIR = os.environ.get("UPLOADS_DIR", os.path.join(BASE_DIR, "uploads"))
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB hard cap per request
    ALLOWED_IMAGE_TYPES = {"png", "jpg", "jpeg", "gif", "webp"}
    ALLOWED_DOCUMENT_TYPES = {"pdf", "doc", "docx", "ppt", "pptx", "txt", "zip"}

    STORAGE_BACKEND = os.environ.get("STORAGE_BACKEND", "local")  # local | s3
    S3_BUCKET = os.environ.get("S3_BUCKET")
    S3_ACCESS_KEY = os.environ.get("S3_ACCESS_KEY")
    S3_SECRET_KEY = os.environ.get("S3_SECRET_KEY")

    FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:5173")

    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

    RATELIMIT_STORAGE_URI = os.environ.get("RATELIMIT_STORAGE_URI", "memory://")


class DevConfig(BaseConfig):
    DEBUG = True


class TestConfig(BaseConfig):
    TESTING = True
    # Tests use SQLite in-memory for speed/isolation ONLY — production always uses Postgres.
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)


class ProdConfig(BaseConfig):
    DEBUG = False


config_by_name = {
    "development": DevConfig,
    "testing": TestConfig,
    "production": ProdConfig,
}
