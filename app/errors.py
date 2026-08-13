"""
app/errors.py — Error Handling Architecture.

404 and 500 render the approved error templates inside the normal shell. Both
guarantee g.lang is set (audit CF-06) and pass a noindex seo object. The 500
handler rolls back any open DB session and never leaks technical detail.
"""
from flask import render_template, g, current_app
from flask_babel import gettext as _
from .extensions import db
from .seo import noindex_seo


def init_app(app):
    @app.errorhandler(404)
    def not_found(e):
        if not hasattr(g, "lang"):
            g.lang = current_app.config["DEFAULT_LOCALE"]
        seo = noindex_seo(title=_("Page not found"))
        return render_template("errors/404.html", seo=seo), 404

    @app.errorhandler(500)
    def server_error(e):
        try:
            db.session.rollback()
        except Exception:
            pass
        if not hasattr(g, "lang"):
            g.lang = current_app.config["DEFAULT_LOCALE"]
        seo = noindex_seo(title=_("Something went wrong"))
        return render_template("errors/500.html", seo=seo), 500
