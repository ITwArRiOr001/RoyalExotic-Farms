"""
app/data/certifications.py — Certifications Data Layer.

Royal Exotic Farms' genuine Indian trade/business registrations. No status is
fabricated: each value is taken directly from the underlying certificate.

Certification shape (consumed by certification_card and the footer):
  { code, label, status, document, badge }
  document : path under static/ to a PUBLIC-SAFE copy, or None
             (None -> the card shows "Copy available on request")
  badge    : path under static/ (or None -> neutral placeholder badge)

[P1B] PUBLIC / PRIVATE SEPARATION
  Public : static/docs/certifications/public/*-public.pdf
           REDACTED derivatives of the authentic certificates. Each page was
           rasterised and the sensitive fields covered with opaque boxes on the
           pixels, then rebuilt as an image-only PDF — no hidden text layer or
           original metadata survives. Registration facts are unchanged. Each
           page carries a footer line: "Public copy — personal details redacted".
             IEC     : residential address (street/flat lines + PIN), handwritten
                       signature. District/state kept.
             APEDA   : date of birth, residential address, handwritten signature.
             ICEGATE : IP address used for registration.
             Udyam   : social category of entrepreneur, flat / building / block /
                       road / PIN. Town, district, state, business mobile and
                       business email kept.
  Private: the unredacted originals must NEVER be placed under static/ (Flask
           serves every file there). Keep them outside the repository.
           .gitignore blocks PDFs placed directly in static/docs/certifications/.

Ordered by export relevance for buyers: export authorisation first, then the
agri-export membership, customs registration, and the general MSME registration.
"""
from flask_babel import gettext as _

_PUBLIC = "docs/certifications/public/"


def get_certifications():
    return [
        {
            "code": "IEC",
            "label": _("Importer-Exporter Code (DGFT)"),
            "status": _("Issued 2024"),
            "document": _PUBLIC + "iec-public.pdf",
            "badge": None,
        },
        {
            "code": "APEDA",
            "label": _("APEDA Registered Exporter (RCMC)"),
            "status": _("Valid to 16 May 2029"),
            "document": _PUBLIC + "apeda-rcmc-public.pdf",
            "badge": None,
        },
        {
            "code": "ICEGATE",
            "label": _("ICEGATE Customs Registration"),
            "status": _("Registered"),
            "document": _PUBLIC + "icegate-public.pdf",
            "badge": None,
        },
        {
            "code": "Udyam",
            "label": _("Udyam / MSME Registration"),
            "status": _("Registered"),
            "document": _PUBLIC + "udyam-public.pdf",
            "badge": None,
        },
    ]
