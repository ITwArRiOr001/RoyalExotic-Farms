"""
app/data/navigation.py — navigation registry.

Builds the `nav` object (primary menu, persistent CTA, footer columns) with
translated labels. Endpoints only — url_for() runs in the templates, so the
locale prefix is injected automatically. Item shape supports optional children
(dropdowns); the current site is intentionally flat.
"""
from flask_babel import gettext as _


def build_nav():
    return {
        "primary": [
            {"label": _("Home"), "endpoint": "main.home", "children": []},
            {"label": _("Products"), "endpoint": "products.index", "children": []},
            {"label": _("Export Process"), "endpoint": "main.export_process", "children": []},
            {"label": _("Markets"), "endpoint": "main.markets", "children": []},
            {"label": _("Insights"), "endpoint": "insights.index", "children": []},
            {"label": _("About"), "endpoint": "main.about", "children": []},
            {"label": _("Contact"), "endpoint": "main.contact", "children": []},
        ],
        "cta": {"label": _("Export Inquiry"), "endpoint": "forms.export_inquiry_page"},
        "footer": [
            {"heading": _("Company"), "links": [
                {"label": _("About"), "endpoint": "main.about"},
                {"label": _("Export Process"), "endpoint": "main.export_process"},
                {"label": _("Markets"), "endpoint": "main.markets"},
                {"label": _("Insights"), "endpoint": "insights.index"},
            ]},
            {"heading": _("Products"), "links": [
                {"label": _("All Products"), "endpoint": "products.index"},
                {"label": _("Become an Import Partner"), "endpoint": "forms.import_partner_page"},
            ]},
            {"heading": _("Get Started"), "links": [
                {"label": _("Export Inquiry"), "endpoint": "forms.export_inquiry_page"},
                {"label": _("Contact"), "endpoint": "main.contact"},
            ]},
        ],
    }
