# Royal Exotic Farms — Phase 3B Architecture Lock
**Final Architectural Contract · Binding Before Template Generation**

*This is the governing contract for all template, content, and growth work. Once locked, components, section ordering, data schemas, workflows, and asset standards do not change ad hoc — additions follow the workflows below so the site scales for years without redesign or regression. No HTML is generated here; this document defines the rules every later phase must obey. Data schemas are expressed as field specifications, not code.*

---

## 1. Reusable Component Matrix

Every UI element resolves to one of these canonical components. **No page may invent a one-off variant of an existing component** — it parameterizes the locked component instead. This is the core duplication-control rule.

### Layout partials (include-based, global)

| Component | File | Parameters | Used by | Variants |
|---|---|---|---|---|
| Base shell | `base.html` | locale, page SEO config, blocks | all pages | — |
| Head/SEO | `partials/head_seo.html` | title, description, canonical, og_image, robots | all | indexable / noindex |
| Structured data | `partials/structured_data.html` | schema_type, schema_data | all | Organization / Product / Article / Breadcrumb |
| Analytics head | `partials/analytics_head.html` | — | all | — |
| Header | `partials/header.html` | nav_tree, locale, active | all | — |
| Nav | `partials/nav.html` | nav_tree, mode (desktop/mobile) | header | desktop / mobile-overlay |
| Language switcher | `partials/language_switcher.html` | locales, active | header | hidden (v1) / visible |
| Footer | `partials/footer.html` | nav_tree, certifications | all | — |
| WhatsApp button | `partials/whatsapp_button.html` | number, prefilled_message | all | sticky-mobile / discreet-desktop |
| Trust strip | `partials/trust_strip.html` | proof_items | home, product, markets, inquiry | — |
| Certifications section | `partials/certifications_section.html` | certifications, layout | home, about | full / compact |

### Component macros (import-based, parameterized)

| Macro | File | Parameters | Used by | Variants |
|---|---|---|---|---|
| `button` | `components/buttons.html` | label, href, variant, size, full_width, icon | all | primary / secondary / tertiary / on-dark |
| `section_opener` | `components/section_opener.html` | eyebrow, heading, lead, align | all | left / center |
| `product_card` | `components/cards.html` | product (data obj), featured | home, products index | standard / flagship-feature |
| `value_card` | `components/cards.html` | icon, title, body | home, about, process | — |
| `article_card` | `components/cards.html` | article (data obj) | insights | standard / featured |
| `certification_card` | `components/cards.html` | cert (data obj), mode | certs section, footer | full-card / badge |
| `cta_band` | `components/cta_band.html` | heading, primary_cta, secondary_cta, theme | most pages | light / dark |
| form field macros | `components/forms.html` | name, label, type, required, inputmode, autocomplete, error | all forms | input / textarea / select / consent / honeypot |

**Lock rules:**
- A new visual need first checks this matrix; only if nothing fits is a new component added *to the matrix* (not inline in a page).
- Component parameter signatures are stable; new parameters may be **added with safe defaults**, never renamed/removed.
- Cards always consume a **data object** (product, article, cert), never loose inline values — this is what makes content additions template-free.

---

## 2. Section Ordering Rules

Section order encodes the conversion psychology (trust before ask) and is locked per page. Reordering requires an explicit contract change.

**Universal ordering principles:**
1. **Hero / page intro always first** (positioning + primary CTA).
2. **Proof before the ask** — trust strip / track record / certifications appear *before* any form or hard CTA band.
3. **One primary CTA path per page**, reinforced at the closing band.
4. **Certifications** render where specified (home, about) and never above the hero.
5. **Closing CTA band is always last content block** before the footer.
6. New sections insert at **defined positions**, never arbitrarily (see §3).

**Locked canonical sequences:**

- **Home:** Hero → Trust strip → Flagship products → Why us → How we work → Markets → Founder note → Certifications → Social proof → Lead magnet → Closing CTA.
- **About:** Hero → Company overview → Honest model → Track record → Values → Founder teaser → Certifications → Compliance → CTA.
- **Founder:** Hero (photo) → Vision → Family values → Model note → Where we're heading → Commitment/signature → CTA.
- **Export Process:** Hero → Process steps → Quality → Documentation/compliance → Accountability → Track-record callout → CTA.
- **Markets:** Hero → Map → Current reach → Target markets → Advantages → Future reach → CTA.
- **Import Partner:** Hero → What partnership means → Who it's for → How it works → Model note → Qualifying form → Reassurance.
- **Export Inquiry:** Hero/reassurance → Trust strip → Form → What happens next → Alt contacts.
- **Contact:** Hero → Contact details → Form → Map → Quick links → Response commitment.
- **Products index:** Hero → Banana feature → Supporting products → Quality statement → Packaging/readiness → CTA.
- **Product detail:** Hero → Overview → Varieties/grades → Specs → Packaging → Availability → Quality/handling → Logistics → Reasons → Conversion band.
- **Insights index:** Hero → Featured → Article grid → Categories → Capture → CTA.
- **Insights article:** Title/meta → Hero image → Body → Inline CTA → Related → Share.

---

## 3. Content Expansion Rules

Components must absorb more (or less) content without breaking. These rules make every layout content-agnostic.

- **No fixed heights** on content containers; height derives from content. Min-heights only for hero/visual balance, never caps that clip.
- **Text never clips or truncates** silently. Cards wrap; long words break (`overflow-wrap`); headings use balanced wrapping.
- **Recommended content budgets** (guidance, not hard caps): eyebrow ≤ 4 words; section heading ≤ 8 words; card title ≤ 6 words; lead ≤ 2 sentences; card body ≤ 3 sentences. Longer content still renders safely but is discouraged for rhythm.
- **Lists/grids grow by item count** — adding cards reflows the grid (per the responsive grid rules), never requires markup changes; minimum/maximum columns are enforced by the grid, so 3 or 12 items both look intentional.
- **Optional sections degrade gracefully** — if a section's data is empty (e.g., no testimonials yet), the section is omitted cleanly, not left as an empty frame.
- **Sections are insert-at-defined-position only** (§2); a genuinely new section type is added to the contract with its fixed position before use.
- **One idea per section** is preserved as content grows — overflow goes to a new section or a sub-page, not a crowded block.

---

## 4. Product Addition Workflow

Adding a product is a **data + asset** operation. No template, route, or redesign change.

**Steps:**
1. Add an entry to `data/products.py` matching the schema below.
2. Place media in `static/img/products/{slug}/` per the naming/dimension standards (§9–10).
3. (Optional) attach a product spec sheet PDF under `static/docs/products/` if offered.
4. Done — the product auto-appears in: products index, its detail page at `/<lang>/products/{slug}`, the header Products dropdown, the homepage flagship grid (if `featured`), the sitemap, and structured data.

**Product data schema (locked fields):**

| Field | Type | Required | Notes |
|---|---|---|---|
| `slug` | string | yes | lowercase-hyphenated, stable, unique, never reused |
| `name` | i18n string | yes | display name |
| `featured` | boolean | yes | flagship flag (banana = true) |
| `order` | int | yes | sort priority |
| `summary` | i18n string | yes | short descriptor (card + meta) |
| `overview` | i18n text | yes | detail intro |
| `varieties` | list[obj] | optional | name + note |
| `specs` | list[{label,value}] | optional | renders table → stacked cards |
| `packaging` | list[obj] | optional | type + note + media key |
| `availability` | i18n string | optional | seasonality |
| `quality_notes` | i18n text | optional | honest handling |
| `logistics` | obj | optional | ports, incoterms (when confirmed) |
| `media` | obj | yes | hero, gallery[], packaging[] keys |
| `seo` | obj | yes | title, description, og_image |

**Honesty rule:** specs/availability must reflect verified data; no fabricated figures.

---

## 5. Certification Addition Workflow

Adding/activating a certification is a **data + file** operation.

**Steps:**
1. Add/edit an entry in `data/certifications.py` (schema below).
2. To activate documents: drop the PDF into `static/docs/certifications/` and set `document` to the filename.
3. Done — the card auto-appears in the homepage and About certifications sections and the footer badge row; Open/Download actions auto-enable when `document` is set; disabled "coming soon" state shows when null.

**Certification data schema (locked fields):**

| Field | Type | Required | Notes |
|---|---|---|---|
| `code` | string | yes | e.g., IEC, GST, APEDA, FSSAI |
| `label` | i18n string | yes | full name |
| `issuing_body` | i18n string | optional | authority |
| `status` | i18n string | yes | e.g., Registered / Certified |
| `document` | string\|null | yes | PDF filename in docs/certifications/, null until attached |
| `order` | int | yes | display order |
| `badge` | string | optional | logo asset key; placeholder if absent |

**Extensibility:** future certs (HACCP, ISO 22000, Halal, GLOBALG.A.P.) added as new entries only. **Honesty rule:** only real registrations, accurate status.

---

## 6. Market Addition Workflow

Markets are data-driven for the Markets page and homepage map.

**Steps:**
1. Add an entry to `data/markets.py` (schema below).
2. Done — appears in the markets list, map markers, and any "markets served" displays; sitemap unaffected (no new route).

**Market data schema (locked fields):**

| Field | Type | Required | Notes |
|---|---|---|---|
| `code` | string | yes | country/region code |
| `name` | i18n string | yes | display name |
| `status` | enum | yes | `served` (proven, e.g., Oman, Abu Dhabi) or `target` |
| `coords` | obj | optional | lat/lng for map marker |
| `order` | int | yes | display order |
| `note` | i18n string | optional | honest context |

**Honesty rule:** `served` only for markets actually exported to; everything else is `target`.

---

## 7. Insights Addition Workflow

Articles are the SEO/content engine and grow frequently; adding one must be friction-free and template-free.

**Steps:**
1. Add an article entry/file under `content/en/insights/` (and future `content/ar/insights/`) with the metadata schema below; body authored in structured markup (e.g., Markdown/structured content).
2. Place the article image in `static/img/insights/{slug}/`.
3. Done — appears in the insights index, gains a page at `/<lang>/insights/{slug}`, joins the sitemap, generates Article structured data, and surfaces in related-article lists by category.

**Article schema (locked fields):**

| Field | Type | Required | Notes |
|---|---|---|---|
| `slug` | string | yes | stable, unique, never reused |
| `title` | i18n string | yes | |
| `description` | i18n string | yes | meta + excerpt |
| `category` | enum | yes | Banana & Produce / Gulf Markets / Export & Compliance / Trade Guidance |
| `date` | date | yes | publish date |
| `author` | string | yes | |
| `hero_image` | media key | yes | 16:9 |
| `og_image` | media key | yes | 1200×630 |
| `featured` | boolean | optional | promotes to featured slot |
| `body` | structured content | yes | headings/paragraphs/quotes |

---

## 8. SEO Scalability Rules

SEO must scale automatically as products, articles, markets, and locales are added.

- **Every routable page MUST supply SEO config** (title, description, canonical, og_image, schema_type) via its data object — enforced; no page ships without it.
- **Slugs are permanent.** Lowercase, hyphenated, ASCII, descriptive, unique. **Never reuse or repurpose a slug**; if content is retired, 301-redirect rather than reassign.
- **Canonical URLs** are absolute and locale-correct; one canonical per page.
- **hreflang/alternates auto-generated** from `SUPPORTED_LOCALES` — adding `ar` auto-emits alternates for every page; `x-default` always present.
- **Structured data per type** is mandatory: Organization (global), Product (product pages), Article (insights), BreadcrumbList (nested pages).
- **Sitemap is generated, never hand-maintained** — built from static routes + product/article slugs × locales; new content auto-included.
- **No duplicate content / no thin pages** — each product/article has unique title + description; data-driven pages must have real content before publishing.
- **OG image required per page** (1200×630); falls back to a branded default only if unset.
- **Robots:** legal/error/success pages `noindex`; all marketing/content pages indexable.

---

## 9. Image Asset Standards

Locked so every image is consistent, performant, and swap-ready.

- **Formats:** serve AVIF/WebP with a JPEG/PNG fallback; logos/badges as SVG or transparent PNG.
- **Folders (by role):** `static/img/{brand|hero|products/{slug}|founder|markets|certifications|icons|insights/{slug}|placeholders}/`.
- **Naming convention:** `{role}-{slug}-{descriptor}-{width}.{ext}` (e.g., `product-banana-hero-1280.webp`, `founder-portrait-768.webp`). Lowercase, hyphenated.
- **Responsive sets:** every content image ships in multiple widths for `srcset` (see §10); browser selects smallest sufficient.
- **Alt text:** mandatory, descriptive, honest (never implies owned farms/cold storage); decorative images use empty alt.
- **Placeholders:** branded, ratio-locked, premium; same filename slot as the eventual real asset so replacement is a file swap. Tracked in the Image Replacement Map.
- **File-size budgets (per served size):** hero ≤ 300KB; product hero ≤ 150KB; gallery/packaging ≤ 120KB; article/thumbnail ≤ 80KB; badges ≤ 20KB. Compress before commit.
- **Color/treatment consistency:** product shots on neutral/white; atmospheric/hero images may carry the subtle deep-green overlay; matte aesthetic preserved.

---

## 10. Media Dimension Standards

Exact ratios and width sets per slot. Aspect-ratio containers reserve space (zero CLS).

| Slot | Aspect ratio | `srcset` widths (px) | Notes |
|---|---|---|---|
| Home hero (image) | 16:9 (or 21:9 band) | 640 / 960 / 1280 / 1920 / 2560 | green overlay; lightweight |
| Home hero (video) | 16:9 | 1920×1080 master | H.264/H.265 + WebM; ≤ ~10s loop; muted; poster required |
| Hero poster | 16:9 | 960 / 1280 / 1920 | still frame of video |
| Product hero | 16:9 | 480 / 768 / 1024 / 1280 | |
| Product gallery / packaging | 1:1 | 320 / 480 / 768 | |
| Founder portrait | 3:4 | 480 / 768 / 960 | photo only (no video) |
| Markets map | scalable (SVG preferred) | — | or 16:9 raster 960/1280/1920; sky-blue accents |
| Certification badge | 1:1 | 160 / 240 / 320 | SVG/transparent PNG |
| Article hero | 16:9 | 640 / 960 / 1280 | |
| Article thumbnail | 16:9 | 320 / 480 / 640 | |
| Open Graph image | 1.91:1 | 1200×630 | per page |
| Favicon set | square | 16 / 32 / 180 / 512 | + manifest |

**Video standard:** MP4 (H.264/H.265) + WebM fallback, muted, looped, `playsinline`, poster-gated, lazy beyond hero, ≤ a few MB optimized; reduced-motion + slow-connection users see poster only.

---

## 11. Future Growth Rules

The principles that keep the contract intact as the business expands.

1. **Data-driven, not template-driven.** Products, certifications, markets, articles, and navigation come from registries/content. Growth = data + assets, not new templates.
2. **Additive-only changes.** Component parameters and schema fields may be added with safe defaults; never renamed or removed. Breaking changes require a contract revision.
3. **Reserved blueprints stay reserved until launch.** The `services` blueprint (future sourcing/consulting) activates as a unit; existing routes are untouched.
4. **Locale-ready by default.** All new strings are translatable; all new layout uses logical properties; adding Arabic = catalog + `ar` in `SUPPORTED_LOCALES`, no structural change.
5. **Slugs and routes are permanent.** Retire via redirect, never reuse.
6. **Honesty is a permanent constraint.** No new content may claim owned infrastructure, fabricate specs/volumes, or display unheld certifications.
7. **New section types enter the contract first** (with a fixed ordering position) before any page uses them.
8. **Performance budgets are binding** on all new assets/pages (§9–10 and the responsive plan); effects never outrank performance.
9. **One component, one definition.** New UI parameterizes the matrix (§1) or extends it centrally — never a page-local fork.
10. **Every new routable page ships with complete SEO config and structured data** (§8) — no exceptions.

---

## Contract Status

✅ Reusable components — locked (§1)
✅ Section ordering — locked (§2)
✅ Content expansion behavior — locked (§3)
✅ Product / Certification / Market / Insights workflows — locked (§4–7)
✅ SEO scalability — locked (§8)
✅ Image & media standards — locked (§9–10)
✅ Future growth rules — locked (§11)

**This contract governs Phase 3B (HTML template generation) and all subsequent content and growth. Templates will be built to consume the locked components, schemas, and ordering above. No HTML has been generated.**

*Two items still pending confirmation from Phase 3A, as they affect the first templates built: (1) consultation form placement — surfaced on Contact/Export-Inquiry vs. its own page; (2) v1 persistence scope — Postgres/analytics persistence at launch vs. email-only with persistence deferred. Confirming these clears Phase 3B template generation to begin, mobile-first, starting with `base.html`, the shell, and mobile navigation.*
