"""
app/data/markets.py — Markets Data Layer.

Conservative and honest: 'served' lists only verified current export activity;
'target' markets are framed as relationships in development, never as presence.
Edit here as reach genuinely grows.

Market shape: { code, name, status('served'|'target'), note, order }
"""
from flask_babel import gettext as _


def get_markets():
    return [
        {"code": "OM", "name": _("Oman"), "status": "served", "order": 1,
         "note": _("Bananas and onions")},
        {"code": "AE-AZ", "name": _("Abu Dhabi, UAE"), "status": "served", "order": 2,
         "note": _("Bananas and onions")},

        {"code": "SA", "name": _("Saudi Arabia"), "status": "target", "order": 3,
         "note": _("Building relationships")},
        {"code": "QA", "name": _("Qatar"), "status": "target", "order": 4,
         "note": _("Building relationships")},
        {"code": "KW", "name": _("Kuwait"), "status": "target", "order": 5,
         "note": _("Building relationships")},
    ]
