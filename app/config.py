"""
app/config.py — application configuration.

Values are read from environment variables (12-factor); safe local defaults let
the app boot in development. Secrets (SECRET_KEY, DB, mail) must be set in
production via the environment (see .env.example / render.yaml).
"""
import os


def _bool(name, default="false"):
    return os.environ.get(name, default).strip().lower() in {"1", "true", "yes", "on"}


class Config:
    # --- Identity (exposed to templates as config.SITE_NAME / DEFAULT_OG_IMAGE) ---
    SITE_NAME = os.environ.get("SITE_NAME", "Royal Exotic Farms")
    SITE_URL = os.environ.get("SITE_URL", "http://localhost:5000")
    DEFAULT_OG_IMAGE = os.environ.get("DEFAULT_OG_IMAGE", "img/brand/og-default.jpg")

    # --- Organization contact (used by data/organization.py) ---
    ORG_LEGAL_NAME = os.environ.get("ORG_LEGAL_NAME", "Royal Exotic Farms")
    ORG_EMAIL = os.environ.get("ORG_EMAIL", "info@royalexoticfarms.com")
    ORG_PHONE = os.environ.get("ORG_PHONE", "+91 00000 00000")
    ORG_WHATSAPP = os.environ.get("ORG_WHATSAPP", "910000000000")  # digits only, wa.me
    ORG_ADDRESS = os.environ.get("ORG_ADDRESS", "India")
    ORG_COUNTRY = os.environ.get("ORG_COUNTRY", "IN")

    # --- Security ---
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None  # token valid for the session

    # --- Database ---
    _db = os.environ.get("DATABASE_URL", "sqlite:///royal_exotic_farms.db")
    # Render/Heroku provide postgres:// ; SQLAlchemy needs postgresql://
    if _db.startswith("postgres://"):
        _db = _db.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = _db
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True, "pool_recycle": 280}

    # --- Internationalization ---
    DEFAULT_LOCALE = os.environ.get("DEFAULT_LOCALE", "en")
    SUPPORTED_LOCALES = [c.strip() for c in os.environ.get("SUPPORTED_LOCALES", "en").split(",") if c.strip()]
    RTL_LOCALES = {"ar", "he", "fa", "ur"}
    BABEL_DEFAULT_LOCALE = DEFAULT_LOCALE
    BABEL_DEFAULT_TIMEZONE = os.environ.get("BABEL_DEFAULT_TIMEZONE", "Asia/Kolkata")
    BABEL_TRANSLATION_DIRECTORIES = os.environ.get("BABEL_TRANSLATION_DIRECTORIES", "../translations")

    # --- Mail (Flask-Mail) ---
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "localhost")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", "25"))
    MAIL_USE_TLS = _bool("MAIL_USE_TLS", "false")
    MAIL_USE_SSL = _bool("MAIL_USE_SSL", "false")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "no-reply@royalexoticfarms.com")
    MAIL_SUPPRESS_SEND = _bool("MAIL_SUPPRESS_SEND", "true")  # true in dev; false in prod
    # Where inquiry notifications are delivered:
    SUBMISSION_NOTIFY_EMAIL = os.environ.get("SUBMISSION_NOTIFY_EMAIL", ORG_EMAIL)
    SEND_ACK_EMAIL = _bool("SEND_ACK_EMAIL", "false")  # optional auto-acknowledgement to sender

    # --- Content ---
    INSIGHTS_CACHE = _bool("INSIGHTS_CACHE", "true")  # cache parsed markdown in memory

    # --- Security headers (Phase 5) ---
    # CSP is intentionally OFF outside production so the Werkzeug debugger's
    # inline assets keep working; ProductionConfig enables a conservative policy.
    CONTENT_SECURITY_POLICY = os.environ.get("CONTENT_SECURITY_POLICY")
    HSTS_SECONDS = int(os.environ.get("HSTS_SECONDS", "0"))


class ProductionConfig(Config):
    DEBUG = False
    MAIL_SUPPRESS_SEND = False
    PREFERRED_URL_SCHEME = "https"
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    # Conservative CSP. JSON-LD (ld+json) is a data block and is exempt from
    # script-src, so structured data is unaffected. 'unsafe-inline' is scoped to
    # style only (a few inline style attributes); scripts stay strict ('self').
    CONTENT_SECURITY_POLICY = os.environ.get(
        "CONTENT_SECURITY_POLICY",
        "default-src 'self'; base-uri 'self'; form-action 'self'; "
        "frame-ancestors 'none'; object-src 'none'; img-src 'self' data:; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; script-src 'self'; "
        "connect-src 'self'; media-src 'self'",
    )
    HSTS_SECONDS = int(os.environ.get("HSTS_SECONDS", "31536000"))


class DevelopmentConfig(Config):
    DEBUG = True
    INSIGHTS_CACHE = False


def get_config():
    env = os.environ.get("FLASK_ENV", "development").lower()
    return ProductionConfig if env == "production" else DevelopmentConfig
