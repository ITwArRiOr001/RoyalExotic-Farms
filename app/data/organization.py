"""
app/data/organization.py — organization identity registry.

Returns the `org` object consumed across the templates and structured data.
Contact fields come from configuration (environment) so deployment can set real
values without code changes. Translatable descriptive strings resolve per-request.
"""
from flask import current_app
from flask_babel import gettext as _


def get_org():
    cfg = current_app.config
    return {
        "name": cfg["SITE_NAME"],
        "legal_name": cfg["ORG_LEGAL_NAME"],
        "url": cfg["SITE_URL"],
        "logo": "img/brand/logo.svg",
        "email": cfg["ORG_EMAIL"],
        "phone": cfg["ORG_PHONE"],
        "whatsapp_number": cfg["ORG_WHATSAPP"],
        "address": cfg["ORG_ADDRESS"],
        "country": cfg["ORG_COUNTRY"],
        "area_served": [
            _("United Arab Emirates"), _("Oman"), _("Saudi Arabia"),
            _("Qatar"), _("Kuwait"), _("Bahrain"),
        ],
        "same_as": [],  # add verified social/profile URLs here
        "founder_name": None,  # set the real name once confirmed (kept blank to avoid fabrication)
        "registration_line": _("Registered agricultural exporter based in India."),
        "hours": _("Monday–Saturday, 9:00 AM – 6:00 PM"),
        "timezone": _("IST (GMT+5:30)"),
        "response_time": _("1–2 business days"),
    }
