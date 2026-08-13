"""
app/blueprints/products.py — product routes.

index: full range (templates partition featured vs supporting).
detail: single data-driven page; 404 for an unknown slug. Product schema on the
page carries no pricing/offers (not an ecommerce site).
"""
from flask import Blueprint, render_template, abort
from flask_babel import gettext as _
from ..seo import make_seo
from ..data.products import get_products, get_product

bp = Blueprint("products", __name__)


@bp.route("/products")
def index():
    seo = make_seo(
        title=_("Products"),
        description=_("Bananas (our flagship), onions, and coconuts — sourced through established "
                     "supplier networks and prepared for export to Gulf buyers."),
    )
    return render_template("pages/products/index.html", seo=seo, products=get_products())


@bp.route("/products/<slug>")
def detail(slug):
    product = get_product(slug)
    if not product:
        abort(404)
    seo = make_seo(
        title=product["name"],
        description=product.get("summary"),
        og_type="product",
        og_image=(product.get("media") or {}).get("hero"),
    )
    return render_template("pages/products/detail.html", seo=seo, product=product)
