"""
app/blueprints/seo_bp.py — sitemap.xml and robots.txt.

Sitemap enumerates static routes + products + articles across every supported
locale (hreflang-friendly, grows automatically with locales/content). robots.txt
allows crawling and points at the sitemap. Not locale-prefixed.
"""
from flask import Blueprint, Response, url_for, current_app, request
from ..data.products import get_products
from .. import content
import os

bp = Blueprint("seo", __name__)

_STATIC_ENDPOINTS = [
    "main.home", "main.about", "main.export_process", "main.markets", "main.contact",
    "products.index", "insights.index",
    "forms.export_inquiry_page", "forms.import_partner_page",
    "main.privacy", "main.terms",
]


def _base_path():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@bp.route("/sitemap.xml")
def sitemap():
    locales = current_app.config["SUPPORTED_LOCALES"]
    urls = []

    def add(endpoint, **kw):
        for loc in locales:
            try:
                urls.append(url_for(endpoint, lang=loc, _external=True, **kw))
            except Exception:
                continue

    for ep in _STATIC_ENDPOINTS:
        add(ep)
    for p in get_products():
        add("products.detail", slug=p["slug"])
    for loc in locales:
        for a in content.all_articles(_base_path(), loc, use_cache=True):
            try:
                urls.append(url_for("insights.article", slug=a["slug"], lang=loc, _external=True))
            except Exception:
                continue

    items = "\n".join(f"  <url><loc>{u}</loc></url>" for u in sorted(set(urls)))
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           f"{items}\n</urlset>\n")
    return Response(xml, mimetype="application/xml")


@bp.route("/robots.txt")
def robots():
    sitemap_url = url_for("seo.sitemap", _external=True)
    body = f"User-agent: *\nAllow: /\nSitemap: {sitemap_url}\n"
    return Response(body, mimetype="text/plain")
