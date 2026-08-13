"""
app/i18n.py — Internationalization Architecture.

Implements the locale-prefixed routing contract from Phase 3A:
  - Every content blueprint is mounted under /<lang>/...
  - url_value_preprocessor pops `lang` from the matched values and pins g.lang.
  - url_defaults auto-injects the active `lang` into url_for() so templates never
    pass it explicitly (they call url_for('main.home') and get /en/).
  - Babel selects the active locale from g.lang.
  - text_dir + alternate_urls (hreflang) are derived for the templates.

Adding Arabic later is configuration-only: add "ar" to SUPPORTED_LOCALES and
provide translations/ar — no route or template edits (RTL already implemented).
"""
from flask import g, request, redirect, url_for, abort, current_app
from .extensions import babel


def select_locale():
    return getattr(g, "lang", current_app.config["DEFAULT_LOCALE"])


def text_direction(locale):
    return "rtl" if locale in current_app.config["RTL_LOCALES"] else "ltr"


def alternate_urls():
    """Absolute URL of the current view in every supported locale (hreflang)."""
    urls = {}
    endpoint = request.endpoint
    if not endpoint:
        return urls
    view_args = dict(request.view_args or {})
    view_args.pop("lang", None)
    for loc in current_app.config["SUPPORTED_LOCALES"]:
        try:
            urls[loc] = url_for(endpoint, lang=loc, _external=True, **view_args)
        except Exception:
            continue
    return urls


def init_app(app):
    supported = app.config["SUPPORTED_LOCALES"]
    default = app.config["DEFAULT_LOCALE"]

    babel.init_app(app, locale_selector=select_locale)

    @app.before_request
    def _default_lang():
        # Ensures g.lang exists even for non-prefixed routes and error handlers.
        if not hasattr(g, "lang"):
            g.lang = default

    @app.url_value_preprocessor
    def _pull_lang(endpoint, values):
        if values and "lang" in values:
            lang = values.pop("lang")
            if lang not in supported:
                abort(404)
            g.lang = lang

    @app.url_defaults
    def _inject_lang(endpoint, values):
        if "lang" in values or not endpoint:
            return
        try:
            if current_app.url_map.is_endpoint_expecting(endpoint, "lang"):
                values["lang"] = getattr(g, "lang", default)
        except Exception:
            pass

    @app.route("/")
    def _root_redirect():
        # Land visitors on the default locale home.
        return redirect(url_for("main.home", lang=default))
