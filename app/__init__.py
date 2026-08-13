"""
app/__init__.py — Application Factory & Blueprint Architecture.

create_app() wires configuration, extensions, i18n (locale-prefixed routing),
context processors, error handlers, and blueprints. Content blueprints mount
under /<lang>; SEO and analytics mount at the root (not locale-prefixed).
"""
import os
import logging
from flask import Flask, request
from werkzeug.middleware.proxy_fix import ProxyFix

from .config import get_config
from .extensions import db, migrate, babel, mail, csrf
from . import i18n, context_processors, errors


def create_app(config_object=None):
    # templates/ and static/ live at the project root, beside the app package.
    app = Flask(
        __name__,
        template_folder=os.path.join(os.pardir, "templates"),
        static_folder=os.path.join(os.pardir, "static"),
    )
    app.config.from_object(config_object or get_config())

    # Behind Render's TLS-terminating proxy: trust one hop of X-Forwarded-* so
    # request.scheme/host/remote_addr are correct — this makes url_for(_external)
    # emit https canonicals/OG/sitemap URLs and logs the real client IP.
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)

    _init_logging(app)

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    csrf.init_app(app)

    # i18n (also registers root redirect + url lang injection) + globals + errors
    i18n.init_app(app)
    context_processors.init_app(app)
    errors.init_app(app)

    _register_blueprints(app)
    _security_headers(app)

    return app


def _register_blueprints(app):
    from .blueprints.main import bp as main_bp
    from .blueprints.products import bp as products_bp
    from .blueprints.insights import bp as insights_bp
    from .blueprints.forms import bp as forms_bp
    from .blueprints.analytics import bp as analytics_bp
    from .blueprints.seo_bp import bp as seo_bp

    # Locale-prefixed content blueprints
    for bp in (main_bp, products_bp, insights_bp, forms_bp):
        app.register_blueprint(bp, url_prefix="/<lang>")

    # Root-level utility blueprints (no locale prefix)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(seo_bp)

    # Ensure models are imported so migrations detect them.
    from . import models  # noqa: F401


def _security_headers(app):
    @app.after_request
    def set_headers(resp):
        resp.headers.setdefault("X-Content-Type-Options", "nosniff")
        resp.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
        resp.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        resp.headers.setdefault("Permissions-Policy", "geolocation=(), microphone=(), camera=()")
        resp.headers.setdefault("Cross-Origin-Opener-Policy", "same-origin")
        csp = app.config.get("CONTENT_SECURITY_POLICY")
        if csp:
            resp.headers.setdefault("Content-Security-Policy", csp)
        hsts = app.config.get("HSTS_SECONDS", 0)
        if hsts and request.is_secure:
            resp.headers.setdefault("Strict-Transport-Security", f"max-age={hsts}; includeSubDomains")
        # Long-cache fingerprinted static assets; keep HTML fresh.
        if resp.mimetype in {"text/css", "application/javascript", "image/svg+xml"}:
            resp.headers.setdefault("Cache-Control", "public, max-age=2592000")
        return resp


def _init_logging(app):
    if not app.debug:
        logging.basicConfig(level=logging.INFO,
                            format="%(asctime)s %(levelname)s %(name)s: %(message)s")
