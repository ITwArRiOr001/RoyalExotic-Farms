"""
app/blueprints/main.py — core content routes.

home, about, founder (redirect into About), export_process, markets, contact,
privacy, terms. Each builds an honest per-page seo object; contact also supplies
an (unbound) ContactForm for CSRF + empty render (posts to forms.submit_contact).
"""
from flask import Blueprint, render_template, redirect, url_for
from flask_babel import gettext as _
from ..seo import make_seo
from ..forms import ContactForm

bp = Blueprint("main", __name__)


@bp.route("/")
def home():
    seo = make_seo(
        title=None,  # home uses the bare site name
        description=_("Royal Exotic Farms is an India-based agricultural export and trading company "
                      "supplying bananas, onions, and coconuts to Gulf importers."),
    )
    return render_template("pages/home.html", seo=seo)


@bp.route("/about")
def about():
    seo = make_seo(
        title=_("About Us"),
        description=_("An honest look at how Royal Exotic Farms operates: an asset-light export and "
                      "trading company sourcing through established supplier networks."),
    )
    return render_template("pages/about.html", seo=seo)


@bp.route("/founder")
def founder():
    # No standalone founder page exists; send visitors to the About founder section.
    return redirect(url_for("main.about") + "#about-founder")


@bp.route("/export-process")
def export_process():
    seo = make_seo(
        title=_("Export Process"),
        description=_("A clear, documented export process — sourcing, quality coordination, "
                      "documentation, and delivery — handled on your behalf."),
    )
    return render_template("pages/export_process.html", seo=seo)


@bp.route("/markets")
def markets():
    from ..data.markets import get_markets
    seo = make_seo(
        title=_("Markets"),
        description=_("Where Royal Exotic Farms exports today — including Oman and Abu Dhabi — and the "
                      "markets we are developing through trusted relationships."),
    )
    return render_template("pages/markets.html", seo=seo, markets=get_markets())


@bp.route("/contact")
def contact():
    seo = make_seo(
        title=_("Contact"),
        description=_("Contact Royal Exotic Farms by WhatsApp, email, or the enquiry form. "
                      "A real person will respond."),
    )
    return render_template("pages/contact.html", seo=seo, form=ContactForm())


@bp.route("/privacy")
def privacy():
    seo = make_seo(title=_("Privacy Policy"),
                   description=_("How Royal Exotic Farms handles the information you provide."))
    return render_template("pages/privacy.html", seo=seo)


@bp.route("/terms")
def terms():
    seo = make_seo(title=_("Terms of Use"),
                   description=_("Terms for using the Royal Exotic Farms website."))
    return render_template("pages/terms.html", seo=seo)
