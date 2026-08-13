"""
app/emails.py — Email Notification Architecture.

On a valid submission the site emails the company inbox (and, optionally, an
acknowledgement to the sender). Sending is best-effort: a mail failure is logged
but never blocks persistence or the user's confirmation — the buyer still gets a
success page and the record is safely stored.

For higher volume, move send() to a background worker/queue; the call site
(forms blueprint) does not need to change.
"""
import logging
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


def send_submission_emails(submission):
    site = current_app.config["SITE_NAME"]
    label = _LABELS.get(submission.kind, "Submission")
    to_admin = current_app.config["SUBMISSION_NOTIFY_EMAIL"]

    # 1) Notify the company.
    try:
        msg = Message(subject=f"[{site}] New {label} from {submission.name}",
                      recipients=[to_admin], reply_to=submission.email)
        msg.body = _render(_ADMIN_BODY, s=submission, site=site, label=label,
                           ts=submission.created_at.strftime("%Y-%m-%d %H:%M"))
        mail.send(msg)
    except Exception:  # pragma: no cover - best effort
        log.exception("Failed to send admin notification for submission %s", getattr(submission, "id", "?"))

    # 2) Optional acknowledgement to the sender.
    if current_app.config.get("SEND_ACK_EMAIL"):
        try:
            ack = Message(subject=f"{site} — we received your message", recipients=[submission.email])
            ack.body = _render(_ACK_BODY, s=submission, site=site, label=label)
            mail.send(ack)
        except Exception:  # pragma: no cover
            log.exception("Failed to send acknowledgement for submission %s", getattr(submission, "id", "?"))
