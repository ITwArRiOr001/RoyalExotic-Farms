"""
app/blueprints/analytics.py — first-party analytics ingestion.

A single JSON endpoint receives lightweight events (pageview, form_start,
form_success, click) from static/js/main.js via navigator.sendBeacon. No
third-party tracker; storage is dashboard-ready. CSRF-exempt (same-origin
beacon, no state mutation beyond an append-only event log). Not locale-prefixed.
"""
from flask import Blueprint, request, jsonify, g
from ..extensions import db, csrf
from ..models import AnalyticsEvent

bp = Blueprint("analytics", __name__)

_ALLOWED = {"pageview", "form_start", "form_success", "click", "outbound"}


@bp.route("/track", methods=["POST"])
@csrf.exempt
def track():
    data = request.get_json(silent=True) or {}
    etype = str(data.get("type", ""))[:48]
    if etype not in _ALLOWED:
        return ("", 204)
    try:
        ev = AnalyticsEvent(
            type=etype,
            path=str(data.get("path", ""))[:500],
            referrer=str(data.get("referrer", ""))[:500],
            locale=getattr(g, "lang", None),
            session_id=str(data.get("sid", ""))[:64],
            meta=data.get("meta") if isinstance(data.get("meta"), dict) else None,
        )
        db.session.add(ev)
        db.session.commit()
    except Exception:
        db.session.rollback()
    return ("", 204)
