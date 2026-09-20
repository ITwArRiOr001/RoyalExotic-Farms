"""
app/data/products.py — Product Data Layer (single source of truth).

Adding or changing a product is data-only: the products index, the detail page,
the inquiry product options and structured data all update automatically.
Templates never hard-code product facts.

[P1B] BUYER-FIRST SHAPE
  slug, name, featured, order, category
  summary      short commercial description (cards, hero lead, meta description)
  facts        the commercial answers a buyer needs first, keyed:
                 form, stage, grade, packing, origin, availability, destination
  varieties    [{name, note, status}]   (see VARIETY STATUS below)
  specs        [{label, value}]  deeper, buyer-relevant specification rows that
               do NOT repeat `facts`
  media        {card, hero, illustrative, caption}
  image_alt

The detail page renders, in order (see hero_facts / snapshot_facts):
  hero summary  -> form, export stage, variety, availability
  snapshot      -> grade, packing, origin, destination requirements
  varieties     -> each variety with its status
  specifications-> `specs`
  order steps   -> order_steps()

TRUTH RULES
  * Anything not owner-confirmed is phrased "confirmed per order" rather than
    stated as a standing company capability (availability, transport,
    temperature, sourcing region, carton formats).
  * "Growing regions" rows are GENERAL agricultural geography, not REF's
    sourcing base.

VARIETY STATUS
  "sourcing_option"  recognised Indian variety / trade type relevant to export
                     orders; general facts only; supply confirmed per order.
  "supplied"         OWNER-CONFIRMED: REF currently supplies it. Change a
                     variety to "supplied" only after the owner confirms —
                     the hero, labels and templates update automatically.

MEDIA
  illustrative=True -> representative photograph; the caption is shown under the
  hero. Real photography: drop the file in, set illustrative=False, clear caption.
  OWNER ASSET NEEDED: a real photograph of mature-green export bananas.
"""
from flask_babel import gettext as _


# ------------------------------------------------------------------ labels ---
def variety_status_labels():
    return {
        "supplied": _("Currently supplied"),
        "sourcing_option": _("Sourcing option · confirmed per order"),
    }


def fact_labels():
    return {
        "form": _("Product form"),
        "stage": _("Export stage"),
        "variety": _("Variety"),
        "availability": _("Availability"),
        "grade": _("Grade"),
        "packing": _("Packing"),
        "origin": _("Origin"),
        "destination": _("Destination requirements"),
    }


# Shared phrasing — one wording everywhere, never a stronger claim.
def _availability():
    return _("Availability, volume and timing are confirmed per order and destination.")


def _origin():
    return _("India — sourced through our supplier network; origin and sourcing region "
             "confirmed per order.")


def _destination():
    return _("Documentation, labelling, packing and temperature requirements are confirmed "
             "for the destination market.")


def _transport():
    return _("Transport and temperature requirements are confirmed according to product, "
             "order and destination.")


# ---------------------------------------------------------------- products ---
def get_products():
    return [
        {
            "slug": "banana",
            "name": _("Bananas"),
            "featured": True,
            "order": 1,
            "category": _("Fresh produce"),
            "summary": _("Our flagship export — fresh green bananas prepared for Gulf retail and wholesale buyers."),
            "facts": {
                "form": _("Fresh Cavendish-type bananas"),
                "stage": _("Mature-green for long-distance transport, where the order requires; "
                           "ripened at destination"),
                "grade": _("To buyer specification — hand and finger size confirmed per order"),
                "packing": _("Export cartons; carton format and weight confirmed per order"),
                "origin": _origin(),
                "availability": _availability(),
                "destination": _destination(),
            },
            "varieties": [
                # General facts: Grand Naine is a Cavendish-subgroup cultivar behind
                # most bananas in world trade; "G-9" is the Indian trade name; widely
                # grown in Maharashtra. Never claim the "Jalgaon banana" GI for REF
                # supply without documented authorisation.
                # OWNER DECISION: set "supplied" once confirmed.
                {"name": _("Grand Naine (G-9)"),
                 "note": _("A Cavendish-group variety — the type behind most bananas in international "
                           "trade, and widely grown in Maharashtra."),
                 "status": "sourcing_option"},
            ],
            "specs": [
                {"label": _("Transport & temperature"), "value": _transport()},
                {"label": _("Quality check"), "value": _("Checked against the agreed specification before dispatch")},
                {"label": _("Packaging options"), "value": _("Export cartons sized for retail and wholesale handling")},
                {"label": _("Growing regions (general)"),
                 "value": _("Maharashtra — including Jalgaon district, one of India’s principal banana-growing "
                            "areas — and other established Indian growing regions")},
            ],
            "media": {
                "card": "img/products/banana-4x3.jpg",
                "hero": "img/products/banana-16x9.jpg",
                # The photograph shows ripe yellow fruit; export fruit ships mature-green.
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
            "summary": _("Fresh red onions sourced and prepared for export to Gulf buyers."),
            "facts": {
                "form": _("Fresh red onions"),
                "stage": _("Cured, dry-skinned bulbs prepared for export"),
                "grade": _("Sized and sorted to buyer specification — size range confirmed per order"),
                "packing": _("Mesh bags or cartons, as required by the order"),
                "origin": _origin(),
                "availability": _availability(),
                "destination": _destination(),
            },
            "varieties": [
                # "Nashik red" is a regional trade description (also "Niphad red"),
                # not a formal variety. "Lasalgaon onion" is a registered GI — never
                # used for REF supply unless certified. No dehydrated product.
                {"name": _("Nashik red onion"),
                 "note": _("A regional trade description for red onions from Nashik district, Maharashtra — "
                           "not a formal variety name."),
                 "status": "sourcing_option"},
                {"name": _("Agrifound Dark Red"),
                 "note": _("A kharif-season variety developed by NHRDF, Nashik: dark red, globular bulbs, "
                           "listed as suitable for export."),
                 "status": "sourcing_option"},
                {"name": _("Agrifound Light Red"),
                 "note": _("A rabi-season variety developed by NHRDF, Nashik: light red, globular bulbs."),
                 "status": "sourcing_option"},
            ],
            "specs": [
                {"label": _("Transport & temperature"), "value": _transport()},
                {"label": _("Quality check"), "value": _("Grading and sizing checked against the agreed specification before dispatch")},
                {"label": _("Packaging options"), "value": _("Mesh bags (common wholesale format); cartons on request")},
                {"label": _("Growing regions (general)"),
                 "value": _("Maharashtra — including Nashik district — and other Indian onion-growing regions")},
            ],
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
            "summary": _("Fresh mature coconuts sourced through our supplier networks for export buyers."),
            "facts": {
                "form": _("Fresh mature coconuts"),
                "stage": _("Semi-husked or as specified by the order"),
                "grade": _("Nut size and weight to buyer specification"),
                "packing": _("Export cartons or as required by the order"),
                "origin": _origin(),
                "availability": _availability(),
                "destination": _destination(),
            },
            "varieties": [
                # Coconut Development Board / CPCRI: WCT = common tall cultivar of the
                # west coast; ECT = traditional tall cultivar of the east coast.
                {"name": _("West Coast Tall"),
                 "note": _("The common traditional tall cultivar of India’s west coast."),
                 "status": "sourcing_option"},
                {"name": _("East Coast Tall"),
                 "note": _("A traditional tall cultivar of India’s east coast."),
                 "status": "sourcing_option"},
            ],
            "specs": [
                {"label": _("Transport & temperature"), "value": _transport()},
                {"label": _("Quality check"), "value": _("Checked against the agreed specification before dispatch")},
                {"label": _("Packaging options"), "value": _("Export cartons, configured to the order")},
                {"label": _("Growing regions (general)"), "value": _("India’s southern coconut-growing states")},
            ],
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


# ------------------------------------------------------- page view helpers ---
def _variety_summary(product):
    """One-line hero value derived from `varieties` + status (never duplicated)."""
    labels = variety_status_labels()
    vs = product.get("varieties") or []
    if not vs:
        return None
    supplied = [v["name"] for v in vs if v.get("status") == "supplied"]
    if supplied:
        return "{} — {}".format(", ".join(supplied), labels["supplied"].lower())
    return "{} — {}".format(", ".join(v["name"] for v in vs), labels["sourcing_option"].lower())


def _rows(product, keys):
    labels, facts = fact_labels(), product.get("facts") or {}
    rows = []
    for k in keys:
        value = _variety_summary(product) if k == "variety" else facts.get(k)
        if value:
            rows.append({"key": k, "label": labels[k], "value": value})
    return rows


def hero_facts(product):
    """Commercial summary beside the hero image."""
    return _rows(product, ["form", "stage", "variety", "availability"])


def snapshot_facts(product):
    """Commercial snapshot (does not repeat the hero summary)."""
    return _rows(product, ["grade", "packing", "origin", "destination"])


def order_steps():
    """How an order is handled — shared by every product page."""
    return [
        {"title": _("Requirement"), "text": _("Product, quantity, destination, grade and packing agreed with you.")},
        {"title": _("Sourcing"), "text": _("Supply arranged through our established supplier network.")},
        {"title": _("Specification & grading"), "text": _("Produce graded against the agreed specification.")},
        {"title": _("Packing"), "text": _("Packed in the format agreed for the order and destination.")},
        {"title": _("Documentation"), "text": _("Export documents prepared for the destination market.")},
        {"title": _("Dispatch"), "text": _("Shipment coordinated with logistics partners; you are kept informed.")},
    ]


# ------------------------------------------------------------ form options ---
def product_options():
    """Options for the export-inquiry product select (+ 'Other')."""
    opts = [{"value": p["slug"], "label": p["name"]} for p in get_products()]
    opts.append({"value": "other", "label": _("Other")})
    return opts


def product_choices():
    """(value, label) choices for WTForms validation."""
    return [(o["value"], str(o["label"])) for o in product_options()]
