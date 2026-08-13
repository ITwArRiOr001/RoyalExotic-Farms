# Royal Exotic Farms — Final Confirmed Requirements & Integration
**Pre–Phase 3 Sign-Off · Locked Build Specification**

*This document confirms that all decisions provided have been integrated into the project's architecture and design system. It supersedes the open "decisions to confirm" in the prior two documents and serves as the single source of truth going into Phase 3 development. Everything below is locked unless explicitly noted.*

---

## 0. Integration Confirmation Checklist

| Requirement | Status | Where integrated |
|---|---|---|
| Internationalization readiness (English v1, future Arabic + RTL) | ✅ Integrated | §1 — routes, folders, templates, CSS strategy |
| Brand balance: 65% Enterprise / 35% Luxury | ✅ Integrated | §2 — design calibration |
| Color refinement: add subtle sky-blue secondary accent | ✅ Integrated | §3 — new tokens + usage rules |
| Hero video composition (logistics + agri + packaging montage) | ✅ Integrated | §4 — media direction |
| Founder video removed; founder photo placeholders kept | ✅ Integrated | §4 — and Founder page wireframe updated |
| Certifications system on Home, About, Footer | ✅ Integrated | §5 — placements |
| Certification cards with future PDF / open / download actions | ✅ Integrated | §5 — component + data model |
| Cert placeholders: IEC, GST, APEDA, FSSAI, future | ✅ Integrated | §5 |
| UX priorities (spacing, rhythm, storytelling, mobile-first, speed, trust) | ✅ Carried + reinforced | Phase 2 & Phase 3 docs, reaffirmed §6 |
| "Real export company, not a template" standard | ✅ Governing principle | All phases |

**Result: All confirmed decisions are integrated. The project is ready for Phase 3 development.**

---

## 1. Internationalization (i18n) Readiness — English v1, Future Arabic/RTL

**Principle:** Build English-only now, but structure everything so an Arabic (RTL) version can be added later with **no redesign and no refactor** — only translation content and locale activation.

### Routing & URL structure

- Use **locale-prefixed routes** from day one: English serves at `/en/...` with `/` redirecting to `/en/`. Future Arabic activates at `/ar/...` with zero route changes.
- Example: `/en/products/banana` today → `/ar/products/banana` later. Slugs remain stable; only content differs.
- A `lang` URL parameter or path segment drives locale; a language switcher is **architected but hidden** in v1 (single locale), revealed when Arabic launches.

### Backend (Flask) structure

- Use **Flask-Babel** (or equivalent) for i18n from the start.
- Message catalogs scaffolded now: `translations/en/LC_MESSAGES/messages.po` (+ compiled `.mo`); `translations/ar/` directory created empty/ready.
- **All user-facing strings wrapped in translation functions** (`gettext`/`_()`) — no hard-coded display text anywhere in templates. This is the most important rule: retrofitting strings later is the costly part, so it's done now.
- Locale-aware formatting for dates, numbers, and any future currency via Babel.
- Recommended folder structure:

```
/app
  /templates        # all strings via _() , no hardcoded copy
  /static
    /css
    /js
    /img
  /content          # structured content (per-locale ready)
    /en
    /ar             # empty, ready
  /translations
    /en/LC_MESSAGES/messages.po(.mo)
    /ar/LC_MESSAGES/   # scaffolded, empty
  routes.py          # locale-prefixed blueprint
  i18n.py            # locale selection, default 'en'
```

### Frontend / CSS strategy for clean future RTL

- Set `<html lang="en" dir="ltr">` now; future Arabic flips to `lang="ar" dir="rtl"` — a single attribute change the layout responds to.
- **Use CSS logical properties everywhere** instead of physical ones: `margin-inline`, `padding-inline`, `inset-inline-start/end`, `text-align: start/end`, `border-inline`. This makes the entire layout mirror automatically under `dir="rtl"`.
- Avoid hard-coded `left`/`right` in layout; avoid directional assumptions in fl/grid where it matters.
- **Direction-aware icons:** arrows, chevrons, route/flow diagrams, and the process timeline must be built to mirror under RTL (use logical positioning or `[dir="rtl"]` transforms).
- Typography system reserves a **future Arabic font stack** slot (e.g., a refined Arabic family) mapped to the same type-scale tokens — not loaded in v1.
- Numerals: keep Western numerals in v1; Arabic-locale numeral handling reserved.

**v1 deliverable:** fully English, but every string externalized, every layout direction-agnostic, every route locale-prefixed. **Do not author Arabic content yet.**

---

## 2. Brand Balance — 65% Enterprise / 35% Luxury

This calibrates the existing design system's expression. The system is unchanged structurally; the *dial* is set.

**Enterprise (65%) — the dominant register:**
- Structured grids, data/credibility emphasis, clear information hierarchy, restrained palette, precise spacing, professional density on capability/spec/cert sections.
- Voice: measured, factual, defensible (matches the "honest claims" rule).
- Trust devices (certifications, track record, process, markets) carry visual weight.

**Luxury (35%) — the refinement layer:**
- Expressed through **whitespace, typographic refinement, the matte finish, and sparing gold** — not through ornamentation.
- Applied to hero, founder/brand-story, and closing conversion moments where emotional trust matters.

**Practical calibration rules:**
- When a section choice is ambiguous, **default to the enterprise treatment** (clarity, structure) and add luxury only as finish (space, type, a single gold accent).
- Gold and decorative flourish stay scarce; structure and legibility lead.
- This balance also resolves the typeface question (see §7): a clean, corporate base with a refined display layer.

---

## 3. Color System Refinement — Sky-Blue Secondary Accent Added

White stays dominant, deep green stays primary, gold stays the premium accent. A **subtle, muted sky blue** joins as a **secondary** accent — never competing with green.

### New tokens (added to the design system)

| Token | Hex | Role |
|---|---|---|
| `--color-sky` | `#6E97B8` | Muted sky blue — secondary accent |
| `--color-sky-deep` | `#4E7A9B` | Deeper blue for emphasis/lines |
| `--color-sky-tint` | `#EAF1F6` | Light blue wash for backgrounds/highlights |

### Usage rules (blue stays secondary)

- **Permitted uses only:** world maps and trade-route visuals, the Markets section, trust/credibility sections, and subtle background highlights (`--color-sky-tint` washes).
- **Never** for primary CTAs (gold), primary headings (green), or large dominant fills.
- Blue must always be visually subordinate to green on any screen where both appear — green leads brand identity; blue supports the global-trade/route storytelling.
- Keep blue muted and matte (in keeping with the matte aesthetic); no bright, saturated, or glossy blue.
- Accessibility: blue used decoratively or for large elements; if used for any text, verify AA contrast on its background.

**Updated hierarchy:** White (dominant) → Deep Green (primary brand) → Gold (premium accent, scarce) → Sky Blue (secondary, trade/trust contexts only).

---

## 4. Media Direction

### Hero video (homepage)

- **Composition — a single cinematic montage combining:** international logistics, container terminals, cargo ships, export operations, agricultural products, and packaging/shipment preparation. Sequence should move from global trade scale → product → shipment readiness, reinforcing "credible export house."
- **Technical:** muted, looped, autoplay (no sound), with a high-quality **poster frame** shown before/instead of playback; lazy-loaded and compressed; never render-blocking; static-poster + `prefers-reduced-motion` fallback (no autoplay). Deep-green low-opacity overlay for brand cohesion and text legibility over the footage.
- **Placeholder now:** reserved hero-video slot with branded poster placeholder, ratio-locked (16:9 / 21:9), swap-ready for real footage.

### Founder media

- **Founder video is removed** — no founder video anywhere on the site.
- **Founder photo placeholders remain** on the Founder Story page and the homepage founder note (professional portrait, 3:4 ratio, swap-ready).
- *Wireframe update:* the Founder Story page hero is now a **photo** treatment only; any prior video reference there is void.

### Other video

- The hover-to-play logistics/export clips (defined in the design system) remain permitted on relevant sections (e.g., process), with poster fallbacks and mobile tap behavior — these are distinct from, and do not include, any founder footage.

---

## 5. Certifications & Registrations System

A first-class trust component, present in three placements, with cards engineered for future document attachment.

### Placements

1. **Homepage** — dedicated Certifications & Registrations section (within or adjacent to the trust band).
2. **About page** — fuller Certifications & Registrations section.
3. **Footer** — compact certification badges row.

### Certification card — component spec

Each card supports document actions **now in structure, populated later**:

- **Fields (data model):**
  - `name` (e.g., "IEC", "GST", "APEDA", "FSSAI")
  - `full_label` (e.g., "Import Export Code")
  - `issuing_body` (optional)
  - `status` (e.g., "Registered" / "Certified")
  - `document_url` (nullable — null in v1)
  - `actions_enabled` (boolean, derived from `document_url` presence)
- **Visual:** white card, `--radius-md`, 1px `--color-line`, certification logo/badge placeholder (green/gold line style), name + label, status pill (green-tint).
- **Actions per card (built now, inert until a document exists):**
  - **Open document** — opens the attached PDF in a new tab (`target="_blank"`, `rel="noopener"`).
  - **Download document** — downloads the PDF.
  - When `document_url` is null: actions render **disabled/"document coming soon"** state — never broken links. Enabling is purely a data change (attach PDF → actions activate automatically).
- **Accessibility:** action buttons labeled ("Open IEC certificate (PDF)"), keyboard accessible, focus-visible.

### Placeholders to prepare (v1)

- **IEC** (Import Export Code)
- **GST**
- **APEDA**
- **FSSAI**
- **Future certifications** — the section/grid must accept additional cards with no layout change (e.g., HACCP, ISO 22000, Halal, GLOBALG.A.P.) by adding data entries only.

**Honesty rule:** only display registrations/certifications the company actually holds; status labels must be accurate. Document actions go live only when real PDFs are attached.

---

## 6. User Experience Priorities (reaffirmed & binding)

These remain governing acceptance criteria for Phase 3:

- Exceptional spacing and visual rhythm (8px system, generous section padding — §4 of design system).
- Premium storytelling layout with smooth, scroll-encouraging flow (vertical narrative, reveal-on-scroll).
- Enterprise-level UI/UX standards (consistent components, clear hierarchy).
- High trust and credibility (track record, certifications, founder presence, honest model).
- Clean navigation and obvious conversion paths (persistent Export Inquiry + WhatsApp).
- Mobile-first execution (sticky conversion bar, single-column, touch targets).
- Fast loading performance (lazy media, modern image formats, minimal libraries, font discipline).

**Final standard (non-negotiable):** the site must read as a *real international export company with proven business credibility* — never as a template-based agricultural website.

---

## 7. Resolved Decisions (previously open)

- **Internationalization:** ✅ English v1, i18n-ready, future Arabic/RTL clean — locked (§1).
- **Sky-blue accent:** ✅ added as secondary token — locked (§3).
- **Founder video:** ✅ excluded; founder photo placeholders retained (§4).
- **Hero video composition:** ✅ defined (§4).
- **Typeface direction:** recommended resolution given 65/35 enterprise-luxury — a **clean corporate sans as the base** with a **refined serif used selectively for display/brand moments** (hero, founder, section openers). This keeps the dominant feel enterprise while the serif delivers the 35% luxury at key emotional points. *Confirm this if you'd like; otherwise it stands as the working direction.*

### Still genuinely open (not blocking, needed to populate, not to build)

- Verified product data (banana/onion/coconut specs, MOQ, packaging, varieties), Incoterms & payment terms, ports used.
- Exact registrations/certifications held + real certificate PDFs (for card activation).
- Real photography per the Image Replacement Map; hero video footage.
- Confirmed contact details, WhatsApp number, stated response-time commitment.

---

## 8. Document Change Log

**Phase 2 — Architecture & Wireframe Plan:**
- Founder Story page hero changed to **photo-only** (founder video removed).
- Certifications & Registrations confirmed on Homepage, About, and Footer with document-action-ready cards (IEC, GST, APEDA, FSSAI, + extensible).
- Hero video slot defined with the confirmed logistics/agri/packaging montage composition.
- All routes/templates/content folders now specified as **locale-prefixed and i18n-ready**.

**Phase 3 — Design System:**
- Added **sky-blue secondary token set** (`--color-sky`, `--color-sky-deep`, `--color-sky-tint`) with strict "secondary, never overpower green" usage rules.
- Color hierarchy updated to four tiers (white → green → gold → blue).
- Brand expression calibrated to **65% enterprise / 35% luxury**.
- Added **CSS logical-properties mandate** and direction-aware component rules for clean future RTL.
- Added **Certification Card** to the component library with document open/download action spec and disabled-until-attached state.
- Reserved future Arabic font-stack slot mapped to existing type tokens.

---

## 9. Phase 3 Readiness Sign-Off

✅ Business strategy — locked (Phases 1–2)
✅ Information architecture & wireframes — locked, updated
✅ Design system & tokens — locked, updated (blue, balance, i18n, certs, media)
✅ Internationalization architecture — defined, English-only v1
✅ Certification system — defined, document-ready
✅ Media direction — hero video defined, founder video excluded

**All confirmed requirements are integrated. The project is cleared to begin Phase 3 development on the locked specifications above.** Outstanding items in §7 are *content to populate*, not *decisions to make*, and do not block build.
