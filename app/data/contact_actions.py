"""
app/data/contact_actions.py — resolved quick-contact registry.

Per the Batch 2 hardening pass, the template RENDERS ONLY: this layer builds the
final hrefs (url_for for endpoints, fully assembled wa.me / mailto) so the
template never constructs business URLs. Returns an ordered list of dicts:
  { type, label, href, icon, primary, new_tab, aria_label }
Invalid/again-missing channels are simply omitted.
"""
from urllib.parse import quote
from flask import url_for
from flask_babel import gettext as _


def build_contact_actions(org, whatsapp_message=None):
    actions = []

    wa = (org or {}).get("whatsapp_number")
    if wa:
        href = f"https://wa.me/{wa}"
        if whatsapp_message:
            href += f"?text={quote(whatsapp_message)}"
        actions.append({
            "type": "whatsapp", "label": _("WhatsApp"), "href": href,
            "icon": "whatsapp.svg", "primary": False, "new_tab": True,
            "aria_label": _("Contact us on WhatsApp"),
        })

    actions.append({
        "type": "inquiry", "label": _("Export Inquiry"),
        "href": url_for("forms.export_inquiry_page"),
        "icon": "leaf.svg", "primary": True, "new_tab": False,
        "aria_label": _("Start an export inquiry"),
    })

    email = (org or {}).get("email")
    if email:
        actions.append({
            "type": "email", "label": _("Email"), "href": f"mailto:{email}",
            "icon": "email.svg", "primary": False, "new_tab": False,
            "aria_label": _("Email us"),
        })

    return actions
