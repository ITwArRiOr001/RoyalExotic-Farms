"""
app/data/certifications.py — Certifications Data Layer.

HONESTY-FIRST DEFAULT: this returns an EMPTY list. The certifications sections
and footer badges render nothing until real, verified credentials are entered —
the site never displays a certification the company does not hold. Populate the
list below (uncomment / edit) only after each item is confirmed, then add the
badge image under static/img/certifications/ and the PDF under
static/docs/certifications/.

Certification shape (matches certification_card): { code, label, status, document, badge }
  document : filename in static/docs/certifications/ (or None -> "Document coming soon")
  badge    : filename in static/img/certifications/ (or None -> placeholder)
"""
from flask_babel import gettext as _


def get_certifications():
    # Return [] until credentials are verified. Example entries a client would
    # typically hold as an Indian agricultural exporter (enable ONLY when true):
    #
    # return [
    #     {"code": "IEC", "label": _("Importer-Exporter Code (DGFT)"),
    #      "status": _("Registered"), "document": None, "badge": None},
    #     {"code": "APEDA", "label": _("APEDA Registered Exporter"),
    #      "status": _("Registered"), "document": None, "badge": None},
    # ]
    return []
