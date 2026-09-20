"""
app/data/organization.py — organization identity registry.

Returns the `org` object consumed across the templates and structured data.
Contact fields come from configuration (environment) so deployment can set real
values without code changes. Translatable descriptive strings resolve per-request.

[P0] Truth guard: contact values that look like placeholders (all-zero phone or
WhatsApp numbers, a bare country name as an "address", example/test email
domains) are dropped here, so a stale environment variable can never publish
dummy data on the page or in JSON-LD. A dropped field simply isn't rendered
(every template already guards these fields with {% if %}).
"""
import logging
import re

from flask import current_app, has_request_context, request
from flask_babel import gettext as _

from .markets import get_markets

log = logging.getLogger(__name__)

_PLACEHOLDER_ADDRESSES = {"india", "in", "address", "tbd", "n/a", "-"}
_PLACEHOLDER_EMAIL_DOMAINS = {"example.com", "example.org", "test.com", "domain.com"}
_warned = set()


def _warn_once(kind, value):
    if (kind, value) not in _warned:
        _warned.add((kind, value))
        log.warning("Ignoring placeholder-looking %s value from configuration: %r", kind, value)


def _digits(value):
    return re.sub(r"\D", "", value or "")


def _clean_phone(value):
    """Drop numbers whose subscriber part is missing or all zeros."""
    value = (value or "").strip()
    d = _digits(value)
    subscriber = d[2:] if d.startswith("91") and len(d) > 10 else d
    if len(subscriber) < 8 or set(subscriber) == {"0"}:
        if value:
            _warn_once("phone/WhatsApp", value)
        return ""
    return value


def _clean_whatsapp(value):
    return _digits(_clean_phone(value))  # wa.me requires digits only


def _clean_email(value):
    value = (value or "").strip()
    if not value or "@" not in value:
        return ""
    if value.rsplit("@", 1)[1].lower() in _PLACEHOLDER_EMAIL_DOMAINS:
        _warn_once("email", value)
        return ""
    return value


def _clean_address(value):
    value = (value or "").strip()
    if value.lower() in _PLACEHOLDER_ADDRESSES:
        if value:
            _warn_once("address", value)
        return ""
    return value


def _site_url(cfg):
    url = (cfg.get("SITE_URL") or "").strip().rstrip("/")
    if url and "localhost" not in url and "127.0.0.1" not in url:
        return url
    # Fall back to the origin the visitor actually used (correct behind ProxyFix).
    if has_request_context():
        return request.url_root.rstrip("/")
    return url


def _area_served():
    """schema.org areaServed = markets actually served today.

    Derived from app/data/markets.py (the single source of truth) so structured
    data can never claim more than the Markets page: 'target' markets are
    relationships in development, not areas served, and markets absent from the
    data (e.g. Bahrain) are never emitted.
    """
    return [m["name"] for m in sorted(get_markets(), key=lambda m: m["order"])
            if m["status"] == "served"]


def get_org():
    cfg = current_app.config
    return {
        "name": cfg["SITE_NAME"],
        "legal_name": cfg["ORG_LEGAL_NAME"],
        "url": _site_url(cfg),
        "logo": "img/brand/logo.svg",
        "email": _clean_email(cfg["ORG_EMAIL"]),
        "phone": _clean_phone(cfg["ORG_PHONE"]),
        "whatsapp_number": _clean_whatsapp(cfg["ORG_WHATSAPP"]),
        "address": _clean_address(cfg["ORG_ADDRESS"]),
        "region": (cfg.get("ORG_REGION") or "").strip(),
        "country": cfg["ORG_COUNTRY"],
        "area_served": _area_served(),
        "same_as": [],  # add verified social/profile URLs here
        "founder_name": None,  # set the real name once confirmed (kept blank to avoid fabrication)
        # [P0] Replaces the vague "Registered agricultural exporter based in
        # India." with facts stated on the APEDA RCMC (registered as Merchant
        # Exporter) and every registration document (Maharashtra, India).
        "registration_line": _("APEDA-registered merchant exporter based in Maharashtra, India."),
        "hours": _("Monday–Saturday, 9:00 AM – 6:00 PM"),
        # [P0] Rendered inside parentheses by templates; was "IST (GMT+5:30)",
        # which produced "(IST (GMT+5:30))".
        "timezone": _("IST, GMT+5:30"),
        "response_time": _("1–2 business days"),
    }
