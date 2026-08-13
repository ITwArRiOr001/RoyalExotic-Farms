# Royal Exotic Farms — Phase 3B Implementation Plan: Responsive & Device Experience
**Mobile-First Responsive Architecture · Pre-Template Build Specification**

*This document updates the Phase 3B plan with a complete responsive architecture. It is a specification (breakpoints, fluid tokens, layout behavior, per-page plans) — no CSS, JavaScript, or template code is produced. Every page and component is defined mobile-first, then tablet, then desktop, so no separate mobile redesign is ever needed. Token values are design specifications to implement in Phase 3C styling.*

---

## 1. Responsive Philosophy & Priority Order

Mobile usability is **business-critical**, not cosmetic. Gulf importers, distributors, and procurement managers frequently first encounter Royal Exotic Farms via WhatsApp, Google Search, LinkedIn, and email links — overwhelmingly on phones. A broken or cramped mobile experience equals a lost lead before the company is ever evaluated.

**Build & decision priority:** (1) Mobile → (2) Laptop → (3) Desktop. Every component is designed at 320px first and *enhanced* upward. When a trade-off arises, mobile clarity and performance win over desktop visual flourish.

**Non-negotiable acceptance standard:** the site must feel native, professional, premium, and trustworthy on mobile, tablet, laptop, and desktop alike — one responsive build, no parallel mobile site.

---

## 2. Breakpoint System (mobile-first, min-width)

Designed to cover every device class in the brief. The build targets ranges, not single devices; the listed widths are conceptual QA checkpoints.

| Token | Min-width | Device class | QA checkpoints |
|---|---|---|---|
| `base` | 320px | Small phones (baseline — nothing breaks here) | 320, 360 |
| `sm` | 480px | Standard / large phones | 375, 390, 412, 430 |
| `md` | 768px | Tablets (portrait) | 768, 820 |
| `lg` | 1024px | Small laptops / tablet landscape | 1024, 1180 |
| `xl` | 1280px | Standard desktops | 1280, 1366, 1440 |
| `2xl` | 1536px | Large monitors | 1536, 1920, 2560 |

- **320px is the hard floor:** layouts must be complete and unbroken at 320px.
- **1920px+ is capped, not stretched:** content sits in a centered container so line lengths and layouts never sprawl on large monitors; only background bands run full-bleed.
- Breakpoints are *content-driven* — additional minor breakpoints may be added where a specific component needs to reflow, but the six above are the system.

---

## 3. Fluid Container System

- **Page container:** centered, `max-width: 1280px`, inline (left/right) padding `clamp(16px, 4vw, 32px)`, width `min(100% − inline padding, 1280px)`. Implemented with logical properties (`padding-inline`, `margin-inline`) for clean future RTL.
- **Full-bleed bands:** dark/anchor and hero sections span 100% viewport width with the inner content constrained to the page container — gives edge-to-edge color without overflow.
- **Prose container:** `max-width: 720px` for reading-width text blocks.
- **Overflow guard:** root and major wrappers carry `overflow-x: clip/hidden` as a safety net; no element may exceed `100%`/`100vw` width.

---

## 4. Responsive Typography (CSS `clamp()` tokens)

All headline/lead sizes are fluid via `clamp(min, preferred, max)` — scaling smoothly between 320px and large desktop with no abrupt jumps. Recommended token values (validate in 3C):

| Token | Min (mobile) | Max (desktop) | `clamp()` specification |
|---|---|---|---|
| `--text-display` | 2.25rem (36px) | 3.75rem (60px) | `clamp(2.25rem, 1.35rem + 4.5vw, 3.75rem)` |
| `--text-h1` | 1.875rem (30px) | 3rem (48px) | `clamp(1.875rem, 1.2rem + 3.4vw, 3rem)` |
| `--text-h2` | 1.5rem (24px) | 2.25rem (36px) | `clamp(1.5rem, 1.1rem + 2vw, 2.25rem)` |
| `--text-h3` | 1.375rem (22px) | 1.75rem (28px) | `clamp(1.375rem, 1.2rem + 0.9vw, 1.75rem)` |
| `--text-h4` | 1.125rem (18px) | 1.375rem (22px) | `clamp(1.125rem, 1rem + 0.6vw, 1.375rem)` |
| `--text-lead` | 1.0625rem (17px) | 1.25rem (20px) | `clamp(1.0625rem, 0.95rem + 0.6vw, 1.25rem)` |
| `--text-body` | 1rem (16px) | 1rem (16px) | fixed `1rem` (never below 16px — prevents mobile zoom) |
| `--text-small` | 0.875rem | 0.875rem | fixed |
| `--text-overline` | 0.75rem | 0.75rem | fixed (tracking 0.12em) |

- Body never drops below 16px (prevents iOS auto-zoom on focus and preserves readability).
- Line-height stays generous on mobile; line length capped at ~70 chars via the prose container.
- Headings use `text-wrap: balance` (where supported) to avoid awkward single-word last lines on narrow screens.

---

## 5. Responsive Spacing Tokens

Static 8px scale (from the design system) for component-internal spacing; **fluid tokens** for section rhythm so vertical pace scales with viewport:

| Token | Specification | Use |
|---|---|---|
| `--space-section` | `clamp(48px, 6vw, 128px)` | Major section padding-block |
| `--space-section-sm` | `clamp(40px, 5vw, 96px)` | Secondary section padding-block |
| `--space-gutter` | `clamp(16px, 2vw, 32px)` | Grid gutters |
| `--space-inline` | `clamp(16px, 4vw, 32px)` | Container inline padding |
| `--space-stack` | `clamp(16px, 2.5vw, 32px)` | Gaps between stacked blocks |

Fixed internal spacing (4–32px) remains for padding inside buttons, cards, and inputs to keep components crisp at every size.

---

## 6. Responsive Grid System

Grids are **intrinsically fluid** (auto-fitting) with explicit column caps, so they reflow without manual breakpoints and never collide:

| Grid | Mobile (base) | Tablet (md) | Desktop (xl) | Technique |
|---|---|---|---|---|
| Product cards | 1 col | 2 col | 3 col (banana feature spans wider) | `minmax(280px, 1fr)` auto-fit, capped |
| Value/why-us cards | 1 col | 2 col | 3–4 col | auto-fit minmax |
| Certification cards | 1 col | 2 col | 3 col | auto-fit minmax(260px) |
| Article cards | 1 col | 2 col | 3 col | auto-fit minmax(300px) |
| Process steps | vertical stack | 2 col or vertical | horizontal row | flex/grid, mirrors in RTL |
| Footer columns | stacked accordions | 2–3 col | 4–5 col | grid |
| Markets / map + text | stacked | stacked or 1:1 | side-by-side | grid `1fr` → `1fr 1fr` |

- No grid uses fixed pixel column widths; all use `fr`/`minmax` so they scale fluidly.
- Minimum card width (~260–300px) guarantees content never crushes; cards wrap to a new row instead of clipping.

---

## 7. Responsive Components

- **Cards:** fluid width within their grid track; ratio-locked media on top; padding `clamp`-scaled; hover effects (lift/scale) apply only on pointer-capable devices (`hover: hover`), disabled on touch to avoid sticky states.
- **Buttons:** min tap target 44×44px on all breakpoints; full-width on mobile where they are primary actions (forms, CTAs); inline-auto width on desktop. Labels never truncate.
- **Media containers:** wrap every image/video in an aspect-ratio container (see §12) so no layout shift at any width.
- **Tables → responsive layouts:** spec/data tables convert to stacked definition-style cards below `md` (see §10).
- **Section openers / CTA bands:** center-aligned and stacked on mobile; can left-align/space-out on desktop.

---

## 8. Mobile Navigation Architecture (designed first)

The mobile navigation is designed **before** desktop and must feel enterprise-grade — calm, spacious, premium — never crowded.

**Mobile (base–sm):**
- Slim sticky header: brand lockup (left) + a compact **Export Inquiry** action and a hamburger (right). Export Inquiry stays visible in the bar at all times.
- Tap hamburger → **full-screen overlay panel** (not a cramped dropdown): generous vertical spacing, large thumb-friendly link rows (≥48px height), one item per line, subtle dividers, premium type. Products expands inline (accordion) rather than a nested mini-menu.
- **Export Inquiry** rendered as a full-width primary (gold) button pinned near the top of the panel; **WhatsApp** and **Contact** pinned at the bottom — both always reachable.
- **Sticky bottom conversion bar** on content pages: persistent WhatsApp + Export Inquiry, thumb-zone placement, so a contact action is always one tap away.
- Language switcher slot present but hidden in v1.

**Tablet (md):** condensed horizontal nav if it fits without crowding; otherwise retains the overlay pattern. Export Inquiry button inline in the header.

**Desktop (lg+):** full horizontal nav with Products dropdown (soft fade), persistent Export Inquiry CTA, active-link gold underline. Bottom sticky bar not needed; header CTA + footer carry conversion.

Thumb-friendliness, spacing, and a single clear primary action drive the mobile nav — no horizontal scrolling, no cramped rows, no hidden critical links.

---

## 9. Forms — Mobile Optimization

All four forms (Contact, Consultation, Export Inquiry, Partnership) are built for natural mobile completion:

- **Single-column layout** at every breakpoint (multi-column only optional on desktop for short paired fields like first/last — never required).
- **Large fields & tap targets:** input height ≥48px, full-width, ample spacing; labels above fields (never placeholder-only).
- **Correct keyboard types** via input types/attributes: `email` → email keyboard, `tel` → numeric pad, `url`, `text` with appropriate `inputmode` and `autocomplete` tokens (name, organization, country, tel, email).
- **Minimal friction:** Export Inquiry stays short; only the Partnership form asks qualifying fields; product pre-fill reduces typing.
- **Inline validation** with clear, non-color-only error messaging; errors don't shift layout (reserved space).
- **Sticky/visible submit** on long forms; submit button full-width on mobile.
- No tiny selects where avoidable; country/product use large, accessible controls.

---

## 10. Product Specification Layout — Responsive

Spec data must stay readable and premium on phones and never force horizontal scrolling.

- **Desktop/tablet (md+):** clean two-column specification table (label / value) within the product page, enterprise-styled with hairline rows.
- **Mobile (base–sm):** the same data **reflows into stacked definition cards** — each spec as a label-over-value block (or paired rows) in a single column. No wide table, no horizontal scroll, no clipping.
- Implementation note: build spec data as a structured list rendered responsively (table semantics on wide, stacked blocks on narrow) — one data source, two presentations.
- Packaging options, varieties/grades, and logistics details follow the same stack-on-mobile pattern.
- Banana (flagship) carries the most spec depth and is the primary test case for this pattern.

---

## 11. Certification Cards — Responsive

- **Desktop (lg+):** 3-up grid of document cards; **Tablet (md):** 2-up; **Mobile (base):** single column, stacked.
- Cards retain their premium **document-card appearance** at every size: badge/placeholder, name + label, status pill, and the **Open** / **Download** actions.
- Actions remain large, tappable (≥44px), and clearly visible on mobile — never collapsed into hidden menus. When a PDF isn't yet attached, the disabled "coming soon" state still reads as a polished document card.
- Footer badge row wraps gracefully (1–2 per row on mobile) without overflow.

---

## 12. Media — Responsive Containers, Aspect Ratios, Performance

- **Aspect-ratio containers** wrap every image and video (hero 16:9/21:9, product 4:3/1:1, founder 3:4, thumbnails 16:9). Reserving the ratio prevents **layout shift (CLS)** before media loads.
- **Responsive images:** `srcset` + `sizes` with multiple widths and modern formats (AVIF/WebP with fallback); the browser fetches the smallest sufficient file — critical on mobile networks.
- **Lazy loading:** `loading="lazy"` and decode hints for below-the-fold media; hero is prioritized (preloaded/eager) but lightweight.
- **Hero video:** muted, looped, `playsinline`, with a **poster frame** shown immediately; on mobile and slow connections, the poster (a still) carries the experience while video defers — remains visually impressive without stalling load. Reduced-motion and slow-connection users get the poster, not autoplay.
- **No fixed-width media;** everything is `max-width: 100%` within its ratio container — no overflow, no collisions.

---

## 13. Performance Architecture (performance over effects)

Optimized for older office desktops, average Android phones, business laptops, and moderate connections. **Performance outranks visual effects** — any effect that risks jank is dropped.

- **Budgets (targets):** LCP < 2.5s on mid-tier mobile/3G-fast; CLS < 0.1; minimal main-thread blocking; lean total page weight (lazy-load everything non-critical).
- **CSS/JS discipline:** no heavy animation or scroll libraries; reveals via lightweight Intersection Observer; animations limited to `transform`/`opacity` (GPU-friendly).
- **Fonts:** preload primary weights, `font-display: swap`, subset; limited families/weights.
- **Images/video:** compressed, responsive, lazy, poster-gated (per §12).
- **Server:** gzip/Brotli (Flask-Compress), cache headers on static, optional fragment caching.
- **Progressive experience:** content and conversion paths work even before decorative JS loads; nothing critical depends on animation.
- **Reduced-motion:** honored globally.

---

## 14. Layout Integrity Rules (enforced across all breakpoints)

Direct mapping to the acceptance requirements — these are build rules, verified at every QA width:

| Rule | Enforcement |
|---|---|
| No horizontal scrolling | Fluid containers, `max-width:100%` media, overflow-x guard, no fixed widths |
| No layout breaking | Fluid grids (`fr`/`minmax`), mobile-first cascade |
| No overlapping components | Flow/grid layout, no absolute positioning for content, spacing tokens |
| No content clipping | Min card widths, wrapping over truncation, `text-wrap` care |
| No hidden important info | Critical content/CTAs never behind hover or off-canvas without access |
| No fixed-width sections | All sections fluid; only `max-width` caps, never fixed `width` |
| No viewport overflow | `min()`/`clamp()` widths, `box-sizing: border-box`, 100vw avoided in favor of 100% |
| No element collisions | Intrinsic grids with minimum track sizes; gap-based spacing |

---

## 15. Per-Page Responsive Layout Plans (Mobile → Tablet → Desktop)

For every page, the mobile layout is the design baseline; tablet and desktop are progressive enhancements of the same structure.

### Home
- **Hero — Mobile:** poster-first (video deferred), headline + lead stacked, full-width primary CTA, secondary text link below; compact height, content above fold. **Tablet:** larger type, video may play, CTA inline-auto. **Desktop:** full-bleed video band, content constrained left/center, dual CTA inline.
- **Trust strip — Mobile:** items stack or 2-up wrap, centered. **Tablet:** single row, 3 items. **Desktop:** single row with dividers.
- **Flagship products — Mobile:** 1 col, banana card first/featured full-width. **Tablet:** 2 col (banana spans top). **Desktop:** 3 col with banana feature emphasized.
- **Why us — Mobile:** 1 col stacked. **Tablet:** 2 col. **Desktop:** 3–4 col.
- **How we work — Mobile:** vertical step stack with connectors. **Tablet:** 2 col or vertical. **Desktop:** horizontal step row.
- **Markets — Mobile:** map above, text below (stacked), sky-blue accents. **Tablet/Desktop:** map + text side-by-side.
- **Founder note — Mobile:** portrait above, text below, centered. **Desktop:** portrait beside text.
- **Certifications — Mobile:** 1 col cards. **Tablet:** 2 col. **Desktop:** 3 col.
- **Lead magnet / closing CTA — Mobile:** stacked, full-width buttons. **Desktop:** centered band, inline buttons.

### About
- **Mobile:** sequential stacked sections (overview → model → track record → values 1-col → founder teaser → certifications 1-col → CTA), full-width CTAs. **Tablet:** values 2-col, certs 2-col, some media beside text. **Desktop:** values/certs 3-col, model and values with side-by-side media, generous whitespace.

### Founder
- **Mobile:** portrait placeholder top, vision/values/commitment stacked, signature, full-width CTA. **Tablet:** portrait beside intro. **Desktop:** larger portrait + text two-column hero, narrative in prose width. (Photo only — no video.)

### Export Process
- **Mobile:** vertical numbered step list with connectors; quality/compliance/accountability stacked; track-record callout; CTA. **Tablet:** steps 2-col or vertical with icons. **Desktop:** horizontal process timeline (mirrors under RTL), supporting blocks side-by-side.

### Markets We Serve
- **Mobile:** region map (sky-blue) full-width on top, current-reach + targets stacked, advantages list 1-col, CTA. **Tablet:** map + reach side-by-side, targets 2-col. **Desktop:** large map with markers, targets/advantages in multi-column, future-reach band.

### Become an Import Partner
- **Mobile:** value + audience + process stacked, then single-column qualifying form with large fields, full-width submit, WhatsApp fallback. **Tablet:** intro content 2-col, form single-column centered. **Desktop:** narrative left / sticky form right (or centered form), reassurance band.

### Export Inquiry
- **Mobile:** brief reassurance + trust strip, then single-column short form, full-width submit, "what happens next" stacked, alt contacts. **Tablet:** form centered, next-steps 3-up. **Desktop:** trust + form side-by-side or centered; next-steps row.

### Contact
- **Mobile:** contact details stacked (tap-to-call, tap WhatsApp, tap email), form single-column, map below, quick links. **Tablet:** details + form side-by-side begins. **Desktop:** details/map left, form right; quick links row.

### Products Index
- **Mobile:** banana feature full-width first, onion/coconut stacked, quality statement, CTA. **Tablet:** 2-col supporting cards. **Desktop:** banana feature + 3-col grid, packaging/quality bands.

### Product Detail (single template — banana/onion/coconut + future)
- **Mobile:** hero image (ratio container) + title + primary quote CTA, then overview, varieties, **specs as stacked definition cards** (no table scroll), packaging, availability, quality, logistics, sticky/visible "Request Quote" + WhatsApp. **Tablet:** specs as 2-col table, packaging 2-col. **Desktop:** hero split (media + summary), specs table, multi-column packaging/logistics, persistent quote CTA.

### Insights Index
- **Mobile:** featured article full-width, then 1-col article cards, category filter as scrollable chips (no overflow break), capture band. **Tablet:** 2-col grid. **Desktop:** featured + 3-col grid, sidebar/filter row.

### Insights Article
- **Mobile:** title/meta, hero image (ratio container), body in comfortable reading width, inline CTA, related cards 1-col. **Tablet:** related 2-col. **Desktop:** prose centered at reading width, related 3-col, share controls.

### Legal (Privacy, Terms) & Errors (404, 500)
- **All breakpoints:** single prose column, generous spacing, clear headings; error pages center content with a primary CTA back to home/inquiry. Fully fluid, nothing to break.

---

## 16. Responsive QA & Acceptance Checklist

Every page/component verified conceptually at: **320, 375, 412/430, 768, 1024, 1440, 1920**.

Per checkpoint, confirm:
- [ ] No horizontal scroll / no viewport overflow
- [ ] No overlap, collision, or clipping
- [ ] All critical content and CTAs visible and reachable
- [ ] Tap targets ≥44px; thumb-zone actions reachable on mobile
- [ ] Typography legible (≥16px body), fluid, no awkward wraps
- [ ] Grids reflow correctly (cards wrap, never crush)
- [ ] Spec tables become stacked cards on mobile
- [ ] Certification cards stack with actions accessible
- [ ] Media keeps aspect ratio; no layout shift; lazy below fold
- [ ] Forms single-column, correct keyboards, large fields
- [ ] Mobile nav full-screen, spacious, Export Inquiry + contact reachable
- [ ] Performance budget met (LCP, CLS) on mid-tier device/connection
- [ ] Reduced-motion honored; effects degrade gracefully

**Acceptance:** native, premium, trustworthy feel on mobile, tablet, laptop, and desktop — from one responsive build.

---

## 17. How This Updates the Phase 3B Plan & Design System

- The Phase 3A architecture is unchanged structurally; this layer governs **how every template and component behaves across breakpoints** and becomes binding acceptance criteria for Phase 3B (HTML) and Phase 3C (CSS).
- **Design system additions:** clamp-based typography tokens (§4), fluid spacing tokens (§5), the six-tier breakpoint system (§2), intrinsic grid rules (§6), and the layout-integrity rules (§14) extend the existing token set.
- **Template build order (3B) is mobile-first:** `base.html` + responsive shell and mobile navigation are built and verified at 320px **first**, then enhanced for tablet/desktop — never the reverse.
- All responsive layout uses **logical properties** so the future Arabic RTL version mirrors cleanly with no additional responsive work.

*End of Phase 3B responsive specification. Templates (Phase 3B build) and styling (Phase 3C) will be produced against this plan, mobile-first, with the per-page desktop/tablet/mobile behavior above as the contract.*
