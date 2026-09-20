"""
app/emails.py — Email Notification Architecture.

On a valid submission the site emails the company inbox (and, optionally, an
acknowledgement to the sender). Sending is best-effort: a mail failure is logged
but never blocks persistence or the user's confirmation — the buyer still gets a
success page and the record is safely stored.

[P0] send_submission_emails() now RETURNS whether the company notification was
actually handed to the mail server (False when sending failed, when no
recipient is configured, or when MAIL_SUPPRESS_SEND is on). The forms
blueprint uses this to guarantee an inquiry can never silently disappear: if
the notification is not delivered, the full lead is written to the error log,
and if neither persistence nor notification succeeded the buyer is told so
instead of being shown a false "thank you".

For higher volume, move send() to a background worker/queue; the call site
(forms blueprint) does not need to change.
"""
import logging
from datetime import datetime
from flask import current_app, render_template_string
from flask_mail import Message
from .extensions import mail

log = logging.getLogger(__name__)

_LABELS = {"inquiry": "Export Inquiry", "partner": "Partnership Request", "contact": "Contact Message"}

_ADMIN_BODY = """New {{ label }} — {{ site }}

Received: {{ ts }} UTC
Kind: {{ s.kind }}
Locale: {{ s.locale }}

Name: {{ s.name }}
Company: {{ s.company or '-' }}
Email: {{ s.email }}
Phone: {{ s.phone or '-' }}
Country: {{ s.country or '-' }}
{% if s.enquiry_type %}Enquiry type: {{ s.enquiry_type }}
{% endif %}{% if s.product %}Product: {{ s.product }}
{% endif %}{% if s.quantity %}Quantity: {{ s.quantity }}
{% endif %}{% if s.consultation %}Consultation requested: yes
{% endif %}{% if s.product_lines %}Product lines: {{ s.product_lines }}
{% endif %}{% if s.volume %}Volume: {{ s.volume }}
{% endif %}{% if s.frequency %}Frequency: {{ s.frequency }}
{% endif %}{% if s.target_market %}Target market: {{ s.target_market }}
{% endif %}
Message:
{{ s.message or '-' }}

—
IP: {{ s.ip }}
Agent: {{ s.user_agent }}
"""

_ACK_BODY = """Dear {{ s.name }},

Thank you for contacting {{ site }}. We have received your {{ label|lower }} and a
member of our team will respond, typically within 1–2 business days.

This is an automated confirmation — there is no need to reply.

Kind regards,
{{ site }}
"""


def _render(tmpl, **ctx):
    return render_template_string(tmpl, **ctx)


def lead_summary(submission):
    """Plain-text rendering of a submission (used for the admin email and as the
    last-resort log record when the email could not be delivered)."""
    site = current_app.config["SITE_NAME"]
    label = _LABELS.get(submission.kind, "Submission")
    ts = (submission.created_at or datetime.utcnow()).strftime("%Y-%m-%d %H:%M")
    return _render(_ADMIN_BODY, s=submission, site=site, label=label, ts=ts)


def send_submission_emails(submission):
    """Send the company notification (+ optional acknowledgement).

    Returns True only if the company notification was handed to the mail server.
    """
    site = current_app.config["SITE_NAME"]
    label = _LABELS.get(submission.kind, "Submission")
    to_admin = (current_app.config.get("SUBMISSION_NOTIFY_EMAIL") or "").strip()
    delivered = False

    # 1) Notify the company.
    if not to_admin:
        log.error("SUBMISSION_NOTIFY_EMAIL is not configured; notification for submission %s not sent",
                  getattr(submission, "id", "?"))
    elif current_app.config.get("MAIL_SUPPRESS_SEND"):
        log.warning("MAIL_SUPPRESS_SEND is on; notification for submission %s was not sent",
                    getattr(submission, "id", "?"))
    else:
        try:
            msg = Message(subject=f"[{site}] New {label} from {submission.name}",
                          recipients=[to_admin], reply_to=submission.email)
            msg.body = lead_summary(submission)
            mail.send(msg)
            delivered = True
        except Exception:  # pragma: no cover - best effort
            log.exception("Failed to send admin notification for submission %s", getattr(submission, "id", "?"))

    # 2) Optional acknowledgement to the sender.
    if current_app.config.get("SEND_ACK_EMAIL") and not current_app.config.get("MAIL_SUPPRESS_SEND"):
        try:
            ack = Message(subject=f"{site} — we received your message", recipients=[submission.email])
            ack.body = _render(_ACK_BODY, s=submission, site=site, label=label)
            mail.send(ack)
        except Exception:  # pragma: no cover
            log.exception("Failed to send acknowledgement for submission %s", getattr(submission, "id", "?"))

    return delivered
