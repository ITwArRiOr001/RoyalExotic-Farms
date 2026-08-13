"""
app/context_processors.py — Context Processor Architecture.

Injects the site-wide context every template expects (nav, org, certifications,
contact_actions, whatsapp_message, now_year, current_locale, text_dir,
supported_locales, alternate_urls). Runs per request so translation and url_for
resolve for the active locale. Route-supplied kwargs (seo, products, form, ...)
override these.
"""
from datetime import datetime
from flask import g, current_app
from flask_babel import gettext as _
from . import i18n
from .data.organization import get_org
from .data.navigation import build_nav
from .data.contact_actions import build_contact_actions
from .data.certifications import get_certifications


def init_app(app):
    @app.context_processor
    def inject_globals():
        org = get_org()
        whatsapp_message = _("Hello Royal Exotic Farms, I would like to enquire about your export products.")
        try:
            contact_actions = build_contact_actions(org, whatsapp_message)
        except Exception:
            contact_actions = []
        locale = getattr(g, "lang", current_app.config["DEFAULT_LOCALE"])
        return {
            "org": org,
            "nav": build_nav(),
            "certifications": get_certifications(),
            "contact_actions": contact_actions,
            "whatsapp_message": whatsapp_message,
            "now_year": datetime.utcnow().year,
            "current_locale": locale,
            "text_dir": i18n.text_direction(locale),
            "supported_locales": current_app.config["SUPPORTED_LOCALES"],
            "alternate_urls": i18n.alternate_urls(),
        }
