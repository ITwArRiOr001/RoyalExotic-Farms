"""
app/data/products.py — Product Data Layer.

Single source of truth for the product range. Adding a product is data-only: the
products index, the data-driven detail page, and the inquiry product options all
update automatically. Copy is honest and indicative (specifications are confirmed
per order); no owned facilities, volumes, or unverified claims are implied.

Product shape (consumed by the templates):
  slug, name, featured, order, category, summary, overview,
  varieties[{name, note, status}], specs[{label, value}], packaging[{type, note}],
  availability, quality_notes, media{card, hero, illustrative, caption}, image_alt

[P0A] VARIETY STATUS — every variety carries an explicit `status` so general
agricultural knowledge is never presented as a company-specific claim:

  "sourcing_option"  A recognised Indian variety / trade type relevant to export
                     orders. Facts in `note` are GENERAL (sourced from public
                     agricultural references, see the Phase-0A report). Whether
                     Royal Exotic Farms supplies it is confirmed per order.
  "supplied"         Owner-confirmed: Royal Exotic Farms currently supplies it.
                     Change a variety to "supplied" ONLY after the owner confirms.

VARIETY_STATUS_LABELS below holds the buyer-facing wording for each status.

"Growing regions" rows state general geography (where the crop is commercially
grown in India), not where REF sources; the sourcing region is confirmed per
order until the owner confirms a standing sourcing region.

MEDIA — `illustrative: True` means the photograph is representative, not a
picture of REF's own product/shipment; the detail page shows `caption` under the
hero. Replacing it with real photography is a file drop + setting
`illustrative: False` (and clearing `caption`).
"""
from flask_babel import gettext as _


def variety_status_labels():
    return {
        "supplied": _("Currently supplied"),
        "sourcing_option": _("Sourcing option · confirmed per order"),
    }


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
                # General facts: Grand Naine is a Cavendish-subgroup cultivar and the
                # cultivar behind most Cavendish bananas in world trade; "G-9" is the
                # common Indian trade/tissue-culture name. Maharashtra's Jalgaon
                # district is India's largest banana district. Do NOT claim the
                # "Jalgaon banana" GI for REF supply unless certified.
                # OWNER DECISION: set status "supplied" once confirmed as REF's
                # standard export variety.
                {"name": _("Grand Naine (G-9)"),
                 "note": _("A Cavendish-group variety — the type behind most bananas in international trade, "
                           "and widely grown in Maharashtra. Shipped mature-green for ripening at destination."),
                 "status": "sourcing_option"},
            ],
            "specs": [
                {"label": _("Product"), "value": _("Fresh Cavendish-type bananas")},
                {"label": _("Export stage"), "value": _("Mature-green, harvested before ripening for long-distance "
                                                        "transport; ripened at destination")},
                {"label": _("Grading"), "value": _("Coordinated to buyer specification (hand and finger size "
                                                   "confirmed per order)")},
                {"label": _("Packing"), "value": _("Standard export cartons; carton weight confirmed per order")},
                {"label": _("Loading"), "value": _("Reefer container, temperature managed in transit")},
                {"label": _("Growing regions"), "value": _("Maharashtra (including Jalgaon district) and other "
                                                           "established Indian growing regions; sourcing region "
                                                           "confirmed per order")},
            ],
            "packaging": [
                {"type": _("Export cartons"), "note": _("Sized for retail and wholesale handling.")},
                {"type": _("Reefer container"), "note": _("Temperature managed through shipping.")},
            ],
            # OWNER DECISION: "year-round" is owner-provided, not independently verified.
            "availability": _("Available year-round, with volume and timing varying by season and destination. "
                              "Please confirm current availability for your market."),
            "quality_notes": _("Grading and quality are coordinated against your requirements, and each shipment "
                               "is checked before dispatch."),
            "media": {
                "card": "img/products/banana-4x3.jpg",
                "hero": "img/products/banana-16x9.jpg",
                # The current photograph shows ripe yellow fruit; export fruit ships
                # mature-green. Replace with a real green-banana photograph (OWNER).
                "illustrative": True,
                "caption": _("Illustrative image. Export bananas are shipped mature-green and ripen at destination."),
            },
            "image_alt": _("Illustrative photograph of bananas on banana leaves"),
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
                # "Nashik red" is a regional trade description (also "Niphad red"),
                # not a formal variety. "Lasalgaon onion" is a registered GI —
                # never describe REF supply as GI unless certified.
                {"name": _("Nashik red onion"),
                 "note": _("A regional trade description for red onions from Nashik district, Maharashtra — "
                           "not a formal variety name."),
                 "status": "sourcing_option"},
                # NHRDF variety; NHB lists it as kharif, dark red, globular, suitable for export.
                {"name": _("Agrifound Dark Red"),
                 "note": _("A kharif-season variety developed by NHRDF, Nashik: dark red, globular bulbs, "
                           "listed as suitable for export."),
                 "status": "sourcing_option"},
                # NHRDF variety; NHB lists it as rabi (primary), light red, globular.
                {"name": _("Agrifound Light Red"),
                 "note": _("A rabi-season variety developed by NHRDF, Nashik: light red, globular bulbs."),
                 "status": "sourcing_option"},
            ],
            "specs": [
                {"label": _("Product"), "value": _("Fresh red onions, cured for export")},
                {"label": _("Grading"), "value": _("Sized and sorted to buyer specification (size range confirmed "
                                                   "per order)")},
                {"label": _("Packing"), "value": _("Mesh bags or cartons as required")},
                {"label": _("Growing regions"), "value": _("Maharashtra (including Nashik district) and other Indian "
                                                           "onion-growing regions; sourcing region confirmed per order")},
            ],
            "packaging": [
                {"type": _("Mesh bags"), "note": _("Common wholesale format.")},
                {"type": _("Cartons"), "note": _("Available on request.")},
            ],
            "availability": _("Availability varies by season and destination market — please contact us to confirm."),
            "quality_notes": _("Grading and sizing are coordinated to your requirements before dispatch."),
            "media": {
                "card": "img/products/onion-4x3.jpg",
                "hero": "img/products/onion-16x9.jpg",
                "illustrative": True,
                "caption": _("Illustrative image"),
            },
            "image_alt": _("Illustrative photograph of red onions"),
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
                # Coconut Development Board / CPCRI: WCT is the common tall cultivar
                # of India's west coast; ECT a traditional tall cultivar of the east
                # coast. Not claimed as REF's standard cultivars.
                {"name": _("West Coast Tall"),
                 "note": _("The common traditional tall cultivar of India’s west coast."),
                 "status": "sourcing_option"},
                {"name": _("East Coast Tall"),
                 "note": _("A traditional tall cultivar of India’s east coast."),
                 "status": "sourcing_option"},
            ],
            "specs": [
                {"label": _("Product"), "value": _("Fresh mature coconuts")},
                {"label": _("Form"), "value": _("Semi-husked or as specified")},
                {"label": _("Grading"), "value": _("Nut size and weight to buyer specification")},
                {"label": _("Packing"), "value": _("Export cartons or as required")},
                {"label": _("Growing regions"), "value": _("India’s southern coconut-growing states; sourcing region "
                                                           "confirmed per order")},
            ],
            "packaging": [
                {"type": _("Export cartons"), "note": _("Configured to order.")},
            ],
            "availability": _("Availability varies by season and destination — please contact us to confirm suitability."),
            "quality_notes": _("Quality is coordinated to your requirements ahead of dispatch."),
            "media": {
                "card": "img/products/coconut-4x3.jpg",
                "hero": "img/products/coconut-16x9.jpg",
                "illustrative": True,
                "caption": _("Illustrative image"),
            },
            "image_alt": _("Illustrative photograph of husked coconuts"),
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
