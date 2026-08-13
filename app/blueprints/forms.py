"""
app/blueprints/forms.py — Form Submission & Inquiry Processing Architecture.

GET pages render the approved form templates with an (unbound) WTForms instance.
POST handlers validate, enforce the honeypot, persist a Submission, send the
notification email (best effort), then Post/Redirect/Get to the confirmation page.
On validation failure the originating page re-renders with field errors (HTTP 422)
so nothing is lost.

Confirmation: forms.success renders templates/pages/inquiry_success.html — the
one functional confirmation state added to complete the flow (approved components
only, noindex). No new sitemap page or component is introduced.
"""
from flask import (Blueprint, render_template, request, redirect, url_for, g, current_app)
from flask_babel import gettext as _
from ..extensions import db
from ..seo import make_seo, noindex_seo
from ..models import Submission
from ..emails import send_submission_emails
from ..forms import ExportInquiryForm, PartnershipForm, ContactForm
from ..data.products import product_options, product_choices

bp = Blueprint("forms", __name__)


# ----------------------------------------------------------------- helpers ----
def _is_spam():
    # Honeypot field is named 'website' by the template macro; bots fill it.
    return bool((request.form.get("website") or "").strip())


def _persist_and_notify(kind, form, **extra):
    s = Submission(
        kind=kind, locale=getattr(g, "lang", None),
        name=form.name.data, company=getattr(form, "company", None) and form.company.data,
        email=form.email.data, phone=form.phone.data, country=form.country.data,
        message=form.message.data, consent=bool(form.consent.data),
        ip=(request.headers.get("X-Forwarded-For", request.remote_addr) or "").split(",")[0].strip(),
        user_agent=request.headers.get("User-Agent", "")[:400],
        **extra,
    )
    db.session.add(s)
    db.session.commit()
    send_submission_emails(s)
    return s


def _success(kind):
    return redirect(url_for("forms.success", type=kind))


# ------------------------------------------------------------------- pages ----
@bp.route("/export-inquiry")
def export_inquiry_page():
    form = ExportInquiryForm()
    form.product.choices = product_choices()
    # Prefill product from ?product= (e.g. arriving from a product page).
    prefill = request.args.get("product")
    if prefill and not form.product.data:
        form.product.data = prefill
    seo = make_seo(
        title=_("Export Inquiry"),
        description=_("Request an export inquiry. Tell us your product and requirements and we will respond promptly."),
    )
    return render_template("pages/export_inquiry.html", seo=seo, form=form, product_options=product_options())


@bp.route("/import-partner")
def import_partner_page():
    form = PartnershipForm()
    seo = make_seo(
        title=_("Become an Import Partner"),
        description=_("Build a long-term sourcing partnership with Royal Exotic Farms."),
    )
    return render_template("pages/import_partner.html", seo=seo, form=form)


# ------------------------------------------------------------- submissions ----
@bp.route("/export-inquiry/submit", methods=["POST"])
def submit_export_inquiry():
    form = ExportInquiryForm()
    form.product.choices = product_choices()
    if _is_spam():
        return _success("inquiry")
    if form.validate_on_submit():
        _persist_and_notify(
            "inquiry", form,
            product=form.product.data, quantity=form.quantity.data,
            consultation=bool(form.consultation.data),
        )
        return _success("inquiry")
    seo = make_seo(title=_("Export Inquiry"))
    return render_template("pages/export_inquiry.html", seo=seo, form=form,
                           product_options=product_options()), 422


@bp.route("/import-partner/submit", methods=["POST"])
def submit_partner():
    form = PartnershipForm()
    if _is_spam():
        return _success("partner")
    if form.validate_on_submit():
        _persist_and_notify(
            "partner", form,
            product_lines=form.product_lines.data, volume=form.volume.data,
            frequency=form.frequency.data, target_market=form.target_market.data,
        )
        return _success("partner")
    seo = make_seo(title=_("Become an Import Partner"))
    return render_template("pages/import_partner.html", seo=seo, form=form), 422


@bp.route("/contact/submit", methods=["POST"])
def submit_contact():
    form = ContactForm()
    if _is_spam():
        return _success("contact")
    if form.validate_on_submit():
        _persist_and_notify("contact", form, enquiry_type=form.enquiry_type.data)
        return _success("contact")
    seo = make_seo(title=_("Contact"))
    return render_template("pages/contact.html", seo=seo, form=form), 422


# ----------------------------------------------------------------- success ----
@bp.route("/thank-you")
def success():
    kind = request.args.get("type", "inquiry")
    headings = {
        "inquiry": _("Thank you — your inquiry has been received"),
        "partner": _("Thank you — your partnership request has been received"),
        "contact": _("Thank you — your message has been received"),
    }
    seo = noindex_seo(title=_("Thank you"))
    return render_template(
        "pages/inquiry_success.html",
        seo=seo,
        success_heading=headings.get(kind, headings["inquiry"]),
    )
