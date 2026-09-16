"""
app/data/certifications.py — Certifications Data Layer.

Populated with Royal Exotic Farms' genuine Indian trade/business registrations.
Every entry corresponds to a real document placed under
static/docs/certifications/. No status is fabricated: each value is taken
directly from the underlying certificate.

Certification shape (matches certification_card): { code, label, status, document, badge }
  document : filename in static/docs/certifications/ (or None -> "Document coming soon")
  badge    : path under static/ (or None -> neutral placeholder img/placeholders/cert-badge.svg)

Ordered by export relevance for buyers: export authorisation first, then the
agri-export membership, customs registration, and the general MSME registration.
"""
from flask_babel import gettext as _


def get_certifications():
    return [
        {
            "code": "IEC",
            "label": _("Importer-Exporter Code (DGFT)"),
            "status": _("Issued 2024"),
            "document": "dgft-iec.pdf",
            "badge": None,
        },
        {
            "code": "APEDA",
            "label": _("APEDA Registered Exporter (RCMC)"),
            "status": _("Valid to 16 May 2029"),
            "document": "apeda-rcmc.pdf",
            "badge": None,
        },
        {
            "code": "ICEGATE",
            "label": _("ICEGATE Customs Registration"),
            "status": _("Registered"),
            "document": "icegate-registration.pdf",
            "badge": None,
        },
        {
            "code": "Udyam",
            "label": _("Udyam / MSME Registration"),
            "status": _("Registered"),
            "document": "udyam-registration.pdf",
            "badge": None,
        },
    ]
