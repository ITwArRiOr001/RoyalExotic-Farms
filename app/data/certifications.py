"""
app/data/certifications.py — Certifications Data Layer.

Populated with Royal Exotic Farms' genuine Indian trade/business registrations.
Every entry corresponds to a real document placed under
static/docs/certifications/. No status is fabricated: each value is taken
directly from the underlying certificate.

Certification shape (matches certification_card): { code, label, status, document, badge }
  document : filename in static/docs/certifications/ (or None -> "Document coming soon")
  badge    : path under static/ (or None -> neutral placeholder img/placeholders/cert-badge.svg)

[P0] PRIVACY: the four original PDFs were REMOVED from static/ (they were
publicly downloadable from every page). The APEDA RCMC showed the proprietor's
date of birth and residential address, the IEC showed the residential address,
and the ICEGATE print-out showed the IP address used for registration. Every
`document` is therefore None, and the card reads "Copy available on request".
To publish again, place a REDACTED copy under static/docs/certifications/ and
set its filename here (OWNER DECISION — see Phase-0 report).

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
            "document": None,
            "badge": None,
        },
        {
            "code": "APEDA",
            "label": _("APEDA Registered Exporter (RCMC)"),
            "status": _("Valid to 16 May 2029"),
            "document": None,
            "badge": None,
        },
        {
            "code": "ICEGATE",
            "label": _("ICEGATE Customs Registration"),
            "status": _("Registered"),
            "document": None,
            "badge": None,
        },
        {
            "code": "Udyam",
            "label": _("Udyam / MSME Registration"),
            "status": _("Registered"),
            "document": None,
            "badge": None,
        },
    ]
