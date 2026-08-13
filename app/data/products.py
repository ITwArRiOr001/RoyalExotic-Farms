"""
app/data/products.py — Product Data Layer.

Single source of truth for the product range. Adding a product is data-only: the
products index, the data-driven detail page, and the inquiry product options all
update automatically. Copy is honest and indicative (specifications are confirmed
per order); no owned facilities, volumes, or unverified claims are implied.

Product shape (matches the frozen templates):
  slug, name, featured, order, category, summary, overview,
  varieties[{name,note}], specs[{label,value}], packaging[{type,note}],
  availability, quality_notes, media{card,hero}, image_alt
"""
from flask_babel import gettext as _


def get_products():
    return [
        {
            "slug": "banana",
            "name": _("Bananas"),
            "featured": True,
            "order": 1,
            "category": _("Fresh produce"),
            "summary": _("Our flagship export — fresh green bananas prepared for Gulf retail and wholesale buyers."),
            "overview": _("Bananas are our strongest and most established product. We source through vetted "
                          "supplier networks in India and coordinate grading, packing, and documentation so "
                          "each shipment arrives export-ready for the destination market."),
            "varieties": [
                {"name": _("Cavendish (green)"), "note": _("The primary export variety, shipped green for transit.")},
            ],
            "specs": [
                {"label": _("Form"), "value": _("Fresh, green, for ripening at destination")},
                {"label": _("Grading"), "value": _("Coordinated to buyer specification")},
                {"label": _("Packing"), "value": _("Standard export cartons")},
                {"label": _("Loading"), "value": _("Reefer container, temperature managed in transit")},
            ],
            "packaging": [
                {"type": _("Export cartons"), "note": _("Sized for retail and wholesale handling.")},
                {"type": _("Reefer container"), "note": _("Temperature managed through shipping.")},
            ],
            "availability": _("Available year-round, with volume and timing varying by season and destination. "
                              "Please confirm current availability for your market."),
            "quality_notes": _("Grading and quality are coordinated against your requirements, and each shipment "
                               "is checked before dispatch."),
            "media": {"card": "img/products/banana-4x3.svg", "hero": "img/products/banana-16x9.svg"},
            "image_alt": _("Fresh green export bananas in cartons"),
        },
        {
            "slug": "onion",
            "name": _("Onions"),
            "featured": False,
            "order": 2,
            "category": _("Fresh produce"),
            "summary": _("Fresh onions sourced and prepared for export to Gulf buyers."),
            "overview": _("A well-established supporting product with verified export activity to the Gulf. We "
                          "coordinate sourcing, grading, and documentation to buyer requirements."),
            "varieties": [
                {"name": _("Red onions"), "note": _("Common export grade; sizing to specification.")},
            ],
            "specs": [
                {"label": _("Form"), "value": _("Fresh, cured for export")},
                {"label": _("Grading"), "value": _("Sized and sorted to buyer specification")},
                {"label": _("Packing"), "value": _("Mesh bags or cartons as required")},
            ],
            "packaging": [
                {"type": _("Mesh bags"), "note": _("Common wholesale format.")},
                {"type": _("Cartons"), "note": _("Available on request.")},
            ],
            "availability": _("Availability varies by season and destination market — please contact us to confirm."),
            "quality_notes": _("Grading and sizing are coordinated to your requirements before dispatch."),
            "media": {"card": "img/products/onion-4x3.svg", "hero": "img/products/onion-16x9.svg"},
            "image_alt": _("Fresh export onions"),
        },
        {
            "slug": "coconut",
            "name": _("Coconuts"),
            "featured": False,
            "order": 3,
            "category": _("Fresh produce"),
            "summary": _("Coconuts sourced through our supplier networks for export buyers."),
            "overview": _("A supporting product in our range. We coordinate sourcing and export preparation to "
                          "buyer requirements."),
            "varieties": [
                {"name": _("Mature coconuts"), "note": _("Export grade; specification on request.")},
            ],
            "specs": [
                {"label": _("Form"), "value": _("Fresh, semi-husked or as specified")},
                {"label": _("Grading"), "value": _("To buyer specification")},
                {"label": _("Packing"), "value": _("Export cartons or as required")},
            ],
            "packaging": [
                {"type": _("Export cartons"), "note": _("Configured to order.")},
            ],
            "availability": _("Availability varies by season and destination — please contact us to confirm suitability."),
            "quality_notes": _("Quality is coordinated to your requirements ahead of dispatch."),
            "media": {"card": "img/products/coconut-4x3.svg", "hero": "img/products/coconut-16x9.svg"},
            "image_alt": _("Fresh export coconuts"),
        },
    ]


def get_product(slug):
    for p in get_products():
        if p["slug"] == slug:
            return p
    return None


def product_options():
    """Options for the export-inquiry product select (+ 'Other')."""
    opts = [{"value": p["slug"], "label": p["name"]} for p in get_products()]
    opts.append({"value": "other", "label": _("Other")})
    return opts


def product_choices():
    """(value, label) choices for WTForms validation."""
    return [(o["value"], str(o["label"])) for o in product_options()]
