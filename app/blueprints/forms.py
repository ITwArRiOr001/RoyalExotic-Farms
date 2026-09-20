"""
app/blueprints/forms.py — Form Submission & Inquiry Processing Architecture.

GET pages render the approved form templates with an (unbound) WTForms instance.
POST handlers validate, enforce the honeypot, persist a Submission, send the
notification email (best effort), then Post/Redirect/Get to the confirmation page.
On validation failure the originating page re-renders with field errors (HTTP 422)
so nothing is lost.

[P0] Reliability contract — an inquiry can never silently disappear:
  * persistence and notification are attempted independently (a DB failure no
    longer prevents the email; an email failure never loses the stored record);
  * if the notification is not delivered, the complete lead is written to the
    application error log (Render log stream) as a last-resort record;
  * if NEITHER persistence NOR notification succeeded, the buyer is NOT shown a
    success page — the form re-renders with their data intact, an explicit
    error and the direct contact channels (HTTP 503);
  * an expired/missing CSRF token (e.g. a tab left open overnight) re-renders
    the same form with the buyer's data intact instead of a bare 400 page.

Confirmation: forms.success renders templates/pages/inquiry_success.html — the
one functional confirmation state added to complete the flow (approved components
only, noindex). No new sitemap page or component is introduced.
"""
from flask import (Blueprint, render_template, request, redirect, url_for, g, current_app)
import logging
from flask_babel import gettext as _
from flask_wtf.csrf import CSRFError
from ..extensions import db
from ..seo import make_seo, noindex_seo
from ..models import Submission
from ..emails import send_submission_emails, lead_summary
from ..forms import ExportInquiryForm, PartnershipForm, ContactForm
from ..data.products import product_options, product_choices

bp = Blueprint("forms", __name__)
log = logging.getLogger(__name__)


# ----------------------------------------------------------------- helpers ----
def _is_spam():
    # Honeypot field is named 'website' by the template macro; bots fill it.
    return bool((request.form.get("website") or "").strip())


def _persist_and_notify(kind, form, **extra):
    """Store the submission and notify the company.

    Returns True when the lead is safe in at least one durable channel
    (database row and/or delivered notification email); False when both failed.
    """
    s = Submission(
        kind=kind, locale=getattr(g, "lang", None),
        name=form.name.data, company=getattr(form, "company", None) and form.company.data,
        email=form.email.data, phone=form.phone.data, country=form.country.data,
        message=form.message.data, consent=bool(form.consent.data),
        ip=(request.headers.get("X-Forwarded-For", request.remote_addr) or "").split(",")[0].strip(),
        user_agent=request.headers.get("User-Agent", "")[:400],
        **extra,
    )

    persisted = False
    try:
        db.session.add(s)
        db.session.commit()
        persisted = True
    except Exception:
        log.exception("Failed to persist %s submission", kind)
        try:
            db.session.rollback()
        except Exception:
            pass

    delivered = False
    try:
        delivered = send_submission_emails(s)
    except Exception:
        log.exception("Notification step raised for %s submission", kind)

    if not delivered:
        # Last-resort durable record: the full lead in the error log stream.
        try:
            body = lead_summary(s)
        except Exception:
            body = f"name={s.name!r} email={s.email!r} company={s.company!r} message={s.message!r}"
        log.error("LEAD NOT EMAILED (persisted=%s) — %s submission follows:\n%s",
                  persisted, kind, body)

    return persisted or delivered


def _delivery_failed(form):
    """Attach a form-level error explaining that nothing was received."""
    form.form_errors.append(_(
        "Sorry — we could not receive your message just now. Nothing has been sent. "
        "Please try again in a few minutes, or contact us directly using the email "
        "or phone number shown on this page."))


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
        title=_("Request Export Details"),
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
        if _persist_and_notify(
            "inquiry", form,
            product=form.product.data, quantity=form.quantity.data,
            consultation=bool(form.consultation.data),
        ):
            return _success("inquiry")
        _delivery_failed(form)
        status = 503
    else:
        status = 422
    seo = make_seo(title=_("Request Export Details"))
    return render_template("pages/export_inquiry.html", seo=seo, form=form,
                           product_options=product_options()), status


@bp.route("/import-partner/submit", methods=["POST"])
def submit_partner():
    form = PartnershipForm()
    if _is_spam():
        return _success("partner")
    if form.validate_on_submit():
        if _persist_and_notify(
            "partner", form,
            product_lines=form.product_lines.data, volume=form.volume.data,
            frequency=form.frequency.data, target_market=form.target_market.data,
        ):
            return _success("partner")
        _delivery_failed(form)
        status = 503
    else:
        status = 422
    seo = make_seo(title=_("Become an Import Partner"))
    return render_template("pages/import_partner.html", seo=seo, form=form), status


@bp.route("/contact/submit", methods=["POST"])
def submit_contact():
    form = ContactForm()
    if _is_spam():
        return _success("contact")
    if form.validate_on_submit():
        if _persist_and_notify("contact", form, enquiry_type=form.enquiry_type.data):
            return _success("contact")
        _delivery_failed(form)
        status = 503
    else:
        status = 422
    seo = make_seo(title=_("Contact"))
    return render_template("pages/contact.html", seo=seo, form=form), status


# ------------------------------------------------------ CSRF expiry recovery ----
_CSRF_RECOVERY = {
    "forms.submit_export_inquiry": ("pages/export_inquiry.html", ExportInquiryForm, "Request Export Details"),
    "forms.submit_partner": ("pages/import_partner.html", PartnershipForm, "Become an Import Partner"),
    "forms.submit_contact": ("pages/contact.html", ContactForm, "Contact"),
}


@bp.app_errorhandler(CSRFError)
def csrf_error(e):
    """Re-render the originating form with the buyer's data intact.

    A stale token (session expired, tab left open) previously produced a bare
    400 page and the typed message was lost. The re-rendered form carries a
    fresh token, so the buyer can simply press submit again.
    """
    if not hasattr(g, "lang"):
        g.lang = current_app.config["DEFAULT_LOCALE"]
    target = _CSRF_RECOVERY.get(request.endpoint)
    log.warning("CSRF validation failed on %s: %s", request.endpoint, getattr(e, "description", e))
    if not target:
        from ..seo import noindex_seo as _noindex
        return render_template("errors/404.html", seo=_noindex(title=_("Page not found"))), 400
    template, form_cls, title = target
    form = form_cls()  # binds request.form, so every typed value is preserved
    if hasattr(form, "product"):
        form.product.choices = product_choices()
    form.form_errors.append(_(
        "Your session expired before the form was sent, so nothing has been submitted yet. "
        "Your details are still below — please check them and submit again."))
    extra = {"product_options": product_options()} if template.endswith("export_inquiry.html") else {}
    return render_template(template, seo=make_seo(title=_(title)), form=form, **extra), 400


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
