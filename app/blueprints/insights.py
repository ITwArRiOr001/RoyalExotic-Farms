"""
app/blueprints/insights.py — insights (articles) routes.

index: lists articles + categories from the Markdown content store.
article: single article + related; 404 for unknown slug. Body is pre-sanitised
by the content loader before the template emits it with |safe.
"""
from flask import Blueprint, render_template, abort, current_app, g
from flask_babel import gettext as _
from ..seo import make_seo
from .. import content

bp = Blueprint("insights", __name__)


def _base_path():
    # project root (one level above the app package)
    import os
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _use_cache():
    return current_app.config.get("INSIGHTS_CACHE", True)


@bp.route("/insights")
def index():
    locale = g.lang
    base = _base_path()
    articles = content.all_articles(base, locale, _use_cache())
    cats = content.categories(base, locale, _use_cache())
    seo = make_seo(
        title=_("Insights"),
        description=_("Practical notes on products, Gulf markets, documentation, and exporting from India."),
    )
    return render_template("pages/insights/index.html", seo=seo, articles=articles, categories=cats)


@bp.route("/insights/<slug>")
def article(slug):
    locale = g.lang
    base = _base_path()
    art = content.get_article(base, locale, slug, _use_cache())
    if not art:
        abort(404)
    related = content.related_articles(base, locale, art, limit=3, use_cache=_use_cache())
    seo = make_seo(
        title=art["title"],
        description=art.get("description"),
        og_type="article",
        og_image=art.get("hero_image"),
    )
    return render_template("pages/insights/article.html", seo=seo, article=art, related_articles=related)
