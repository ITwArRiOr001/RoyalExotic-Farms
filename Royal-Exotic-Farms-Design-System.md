# Royal Exotic Farms — Design System Specification
**Phase 3 — Visual Design System & UI/UX Standards**

*A build-ready design system. Every value below is concrete and tokenized so a development team can implement consistently across all pages without interpretation. The target feeling: a premium international trade house / logistics / commodity-trading firm — elegant, matte, intellectual, and trustworthy enough to earn an importer's confidence within seconds.*

---

## 1. Design Principles (the felt experience)

1. **Quiet luxury, not flash.** Refinement comes from space, restraint, and precision — never from gradients, glows, or motion tricks. If an effect draws attention to itself, remove it.
2. **Matte over glossy.** Flat, muted surfaces; soft low-contrast shadows; no shine, no heavy bevels, no glassmorphism.
3. **White carries the brand.** White and off-white dominate. Deep green anchors. Gold appears rarely and deliberately — its scarcity is what makes it read as premium.
4. **Hierarchy first.** Every screen has one clear focal point and one dominant action. The eye should always know where to go.
5. **Rhythm through consistency.** A single spacing system and type scale govern every page, creating an enterprise-grade sense of order.
6. **Trust is the aesthetic.** The design's job is credibility. Clean structure, honest imagery, and professional typography signal a serious company before a word is read.
7. **Calm motion.** Animation supports comprehension (reveal, focus, feedback) and never decorates for its own sake.

---

## 2. Color System

White-dominant, deep-green brand, sparing gold. All tokens defined as variables.

### Core tokens

| Token | Hex | Role |
|---|---|---|
| `--color-white` | `#FFFFFF` | Primary background, dominant surface |
| `--color-paper` | `#F6F7F4` | Alternating section background (soft warm white) |
| `--color-mist` | `#EDF0EC` | Subtle panel / card fill |
| `--color-green-900` | `#0A2C22` | Deepest green — footer, dark sections |
| `--color-green-800` | `#0E3B2E` | **Primary brand green** |
| `--color-green-700` | `#14463A` | Headings on light, hover states |
| `--color-green-600` | `#1B5443` | Secondary green elements |
| `--color-green-tint` | `#E7EEEA` | Green wash backgrounds, badges |
| `--color-gold` | `#C9A24B` | **Primary accent** — CTAs, key emphasis |
| `--color-gold-deep` | `#B8902F` | Gold hover / pressed |
| `--color-gold-tint` | `#F3ECD9` | Gold wash, subtle highlight backgrounds |
| `--color-ink` | `#1F2A28` | Primary body text |
| `--color-ink-muted` | `#5C6B66` | Secondary text, captions |
| `--color-line` | `#E3E7E3` | Borders, dividers, hairlines |
| `--color-line-strong` | `#CBD2CD` | Input borders, stronger dividers |

### Functional tokens (forms / feedback)

| Token | Hex | Role |
|---|---|---|
| `--color-success` | `#2E7D5B` | Valid input, success message |
| `--color-error` | `#B23A3A` | Validation error |
| `--color-focus` | `#C9A24B` | Focus ring (gold, 2px, offset) |

### Usage rules

- **White / paper backgrounds** for ~80% of all surfaces. Alternate `--color-white` and `--color-paper` between sections to create rhythm without lines.
- **Deep green** for: logo lockup, headings, the footer, occasional full-bleed "anchor" sections (e.g., a dark trust/CTA band), icon strokes.
- **Gold** is reserved — primary CTA buttons, a single key stat per section, thin divider accents, active nav indicator. Never large gold fills, never gold body text.
- **Dark sections** (green-900) used max 1–2 times per page (e.g., a CTA band or process section) for cadence and contrast.
- **Accessibility:** body text `--color-ink` on white passes WCAG AA. Gold (`#C9A24B`) on white is **decorative/large-text only** — never small gold body text on white. Gold buttons must use green-900 or white label text tested to AA (use green-900 text on gold for best contrast).

---

## 3. Typography System

Intellectual + corporate. Recommended pairing: a **refined serif for display** (premium, considered) with a **neutral grotesque sans for UI/body** (clean, modern, legible).

### Recommended families (with fallbacks)

- **Display / Headings (serif):** *Fraunces* or *Source Serif 4* (alternatives: *Libre Caslon Text*, *Spectral*). Fallback stack: `"Source Serif 4", "Georgia", serif`.
- **Body / UI (sans):** *Inter* or *Söhne*-style grotesque (alternatives: *Geist*, *IBM Plex Sans*). Fallback stack: `"Inter", -apple-system, "Segoe UI", sans-serif`.
- **Sans-only alternative** (if a single family is preferred for a more pure logistics/corporate feel): use *Inter* for both, with display weights at 600–700 and tighter tracking.

> Decision to confirm: serif-display pairing (intellectual, trade-house) vs. sans-only (cleaner, modern-logistics). Spec below assumes the serif + sans pairing; switching is a token-level change only.

### Type scale (base 16px = 1rem; modular ratio ≈ 1.25)

| Token | Size | Line-height | Weight | Tracking | Use |
|---|---|---|---|---|---|
| `--text-display` | 3.75rem (60px) | 1.05 | 600 serif | -0.01em | Hero headline (desktop) |
| `--text-h1` | 3rem (48px) | 1.1 | 600 serif | -0.01em | Page title |
| `--text-h2` | 2.25rem (36px) | 1.15 | 600 serif | -0.005em | Section heading |
| `--text-h3` | 1.75rem (28px) | 1.2 | 600 serif | 0 | Sub-section |
| `--text-h4` | 1.375rem (22px) | 1.3 | 600 sans | 0 | Card title |
| `--text-lead` | 1.25rem (20px) | 1.55 | 400 sans | 0 | Intro paragraphs |
| `--text-body` | 1rem (16px) | 1.65 | 400 sans | 0 | Body |
| `--text-small` | 0.875rem (14px) | 1.6 | 400 sans | 0 | Captions, meta |
| `--text-overline` | 0.75rem (12px) | 1.4 | 600 sans | 0.12em (uppercase) | Eyebrow labels |

### Rules

- **One eyebrow + one heading + one lead** per section opener (overline in gold or green, heading in green-700/800, lead in ink-muted).
- Body line length capped at **~70 characters** (max-width ~640–720px) for readability.
- Headings use serif; all UI, labels, buttons, and body use sans.
- Mobile scales: display → 2.5rem, h1 → 2.25rem, h2 → 1.75rem (fluid `clamp()` recommended).
- Never more than 2 weights of the serif in use (regular + semibold).

---

## 4. Spacing & Layout System

### Spacing scale (base unit = 8px)

`--space-1: 4px` · `--space-2: 8px` · `--space-3: 12px` · `--space-4: 16px` · `--space-5: 24px` · `--space-6: 32px` · `--space-7: 48px` · `--space-8: 64px` · `--space-9: 96px` · `--space-10: 128px`

### Section rhythm

- **Section vertical padding:** desktop `--space-10` (128px) top/bottom for major sections; `--space-9` (96px) for secondary; mobile reduces to `--space-8` (64px) / `--space-7` (48px).
- **Intra-section gaps:** `--space-6`–`--space-7` between heading group and content.
- **Generous whitespace is mandatory** — when in doubt, add space. Cramped layouts read as cheap.

### Grid & containers

- **Grid:** 12 columns, gutter `--space-5` (24px) mobile → `--space-6` (32px) desktop.
- **Container max-width:** `1280px`, centered, with `--space-5`/`--space-6` side padding.
- **Narrow content (prose) max-width:** `720px`.

### Breakpoints

| Name | Range |
|---|---|
| Mobile | `< 640px` (base, mobile-first) |
| Tablet | `640px – 1023px` |
| Desktop | `1024px – 1279px` |
| Wide | `≥ 1280px` |

---

## 5. Surface, Border, Radius & Elevation (matte finish)

- **Radius:** `--radius-sm: 4px` (inputs, buttons), `--radius-md: 8px` (cards), `--radius-lg: 12px` (feature panels/media). Corporate, not rounded-pill.
- **Borders:** 1px `--color-line` for cards/dividers; 1px `--color-line-strong` for inputs.
- **Shadows (soft, matte — low opacity, green-tinted, never gray-black):**
  - `--shadow-sm: 0 1px 2px rgba(14,59,46,0.05)`
  - `--shadow-md: 0 4px 16px rgba(14,59,46,0.06)`
  - `--shadow-lg: 0 12px 32px rgba(14,59,46,0.08)`
- **No glossy gradients, glows, or glass blur.** Surfaces are flat fills with subtle elevation only on interaction.
- **Dividers:** prefer whitespace and background-color change over visible lines; use hairlines (`--color-line`) sparingly.

---

## 6. Iconography & Imagery Style

- **Icons:** line-style (stroke ~1.5–2px), geometric, consistent set; logistics/trade motifs (container, ship, globe, route, document, handshake-of-trade). Green stroke default; gold only for active/featured. Never filled cartoon icons.
- **Imagery direction:** logistics/trade/commodity — ports, containers, world maps, clean produce on neutral backgrounds, documentation. **No** rustic farm, cartoon, or childish agriculture imagery.
- **Image treatment:** subtle deep-green duotone or low-opacity green overlay on hero/atmospheric images for brand cohesion and matte feel; product shots kept clean on neutral/white.
- **Placeholders:** branded, ratio-locked, premium neutral graphics with green overlay + thin gold accent — never broken boxes (full spec in the architecture document's Image Replacement Map). Placeholders must never imply owned farms/cold storage.

---

## 7. Component Library

### Buttons

| Variant | Style | Use |
|---|---|---|
| **Primary** | Gold fill (`--color-gold`), green-900 label, `--radius-sm`, padding 14px×28px, weight 600 | Export Inquiry, main conversions |
| **Secondary** | Transparent, 1.5px green-800 border, green-800 label | Secondary actions (e.g., Become an Import Partner) |
| **Tertiary / text** | No border, green-700 label, gold underline-on-hover | Inline links, "Read more" |
| **On-dark** | White or gold fill on green-900 sections | CTAs inside dark bands |

- **Hover:** primary → `--color-gold-deep` + 2px lift + `--shadow-md`, 200ms. Secondary → green-tint fill. Transition `background, transform, box-shadow`.
- **Focus:** 2px gold focus ring, 2px offset (keyboard visible).
- **Min tap target:** 44×44px.

### Cards (product / value / article)

- White fill, `--radius-md`, 1px `--color-line`, `--shadow-sm` at rest.
- Structure: ratio-locked media top → padding `--space-5` → eyebrow/title/excerpt → text-link CTA.
- **Hover:** lift 4px, shadow → `--shadow-md`, media subtle scale (1.03) within fixed frame, 250ms ease-out. Elegant, not bouncy.

### Navigation header

- White background, `--shadow-sm` on scroll, condenses height on scroll.
- Links: sans, `--text-small`/`--text-body`, green-800; active = gold underline (2px, animated width).
- Primary CTA (gold) right-aligned, persistent.
- Dropdown (Products): white panel, `--shadow-md`, `--radius-md`, soft fade+rise (150ms).

### Forms

- Inputs: white fill, 1px `--color-line-strong`, `--radius-sm`, padding 12px×16px, `--text-body`.
- Label above field, `--text-small`, weight 600, green-800.
- **Focus:** border → green-600, 2px gold focus ring.
- **Validation:** error border `--color-error` + inline message; success border `--color-success`. Inline, real-time-friendly.
- Single-column layout; large mobile fields; correct input types.

### Trust strip / badge

- Green-tint or paper background band, line icons + short proof text, gold hairline divider above/below. Used to surface Oman/Abu Dhabi track record and registrations.

### Section opener

- Eyebrow (overline, gold or green) → serif heading → lead paragraph (ink-muted) → optional CTA. Consistent across all sections.

### Footer

- Green-900 background, white/mist text, gold for active links and CTA; structured columns (per architecture doc), hairline gold divider, base bar with legal + registration line.

---

## 8. Motion & Interaction System

Subtle, premium, comprehension-supporting. **Respect `prefers-reduced-motion`** — disable transforms/reveals, keep instant states.

### Timing & easing

- **Durations:** micro (hover/focus) 150–200ms; content reveals 350–450ms; section transitions 400–600ms.
- **Easing:** standard `cubic-bezier(0.4, 0, 0.2, 1)`; entrances ease-out `cubic-bezier(0.16, 1, 0.3, 1)` for a soft settle.

### Patterns

- **Scroll reveal:** content fades in (opacity 0→1) + rises (translateY 16px→0), staggered ~60–80ms between sibling items. Trigger once when ~20% in viewport. Subtle only.
- **Hover lifts:** cards/buttons rise 2–4px with shadow increase; media inside cards scales ≤1.03 within a fixed frame (no layout shift).
- **Hover-to-play video** (logistics/export clips, where appropriate): muted, looped, autoplay paused at rest showing a poster frame; on hover (desktop) play softly; on tap (mobile) play, tap again to pause. Lazy-loaded, lightweight (compressed, short), never autoplay-with-sound, never blocks page load. Provide a static poster fallback and reduced-motion fallback (no auto-play).
- **Smooth scrolling:** native CSS `scroll-behavior: smooth` for anchor jumps; no heavy scroll-jacking libraries. Natural momentum preserved.
- **Section transitions:** achieved through whitespace + alternating backgrounds + reveal-on-scroll, not abrupt cuts or parallax gimmicks. Optionally a very subtle background-color crossfade between adjacent sections.
- **Nav underline:** active/hover underline animates width 200ms.
- **No** parallax overload, bouncing, spinning, looping decorative motion, or anything that competes with content.

---

## 9. Scroll & Storytelling Flow

- The homepage and key pages read as a **vertical narrative**: positioning → proof → products → how we work → markets → people → conversion. Each section's lead line invites the next scroll.
- **Visual flow devices:** alternating white/paper backgrounds, consistent section openers, occasional dark anchor band (green-900) for emphasis, and reveal-on-scroll to create a sense of unfolding.
- **One idea per section.** Avoid dense walls; let whitespace pace the story.
- **Persistent conversion:** header CTA always present; closing conversion band + sticky mobile WhatsApp/Inquiry ensure the path is never lost.

---

## 10. Mobile-First & Responsive Standards

- **Mobile-first build:** base styles target mobile; enhance upward.
- Sections stack single-column; multi-column grids collapse gracefully; spec tables become stacked cards or horizontally scrollable.
- Fluid type via `clamp()`; touch targets ≥44px; thumb-reachable primary actions.
- **Sticky mobile conversion bar:** WhatsApp + Export Inquiry pinned bottom.
- Hero prioritizes text + CTA above the fold; heavy media deferred/lightened on mobile.
- Hover-only interactions have tap equivalents; hover-to-play videos use tap on mobile.
- Forms: single column, large fields, correct keyboards, inline validation.

---

## 11. Accessibility Standards (WCAG 2.1 AA)

- **Contrast:** body text and interactive labels meet AA; gold restricted to large/decorative use on white; buttons tested (green-900 label on gold).
- **Focus visible:** 2px gold focus ring on all interactive elements; logical tab order.
- **Semantics:** proper heading order (one H1/page), landmarks, descriptive link text, ARIA only where needed.
- **Images:** honest, descriptive alt text on every image/placeholder.
- **Motion:** full `prefers-reduced-motion` support.
- **Forms:** labels tied to inputs, errors announced, no color-only error signaling.
- **Text scaling:** layout holds at 200% zoom.

---

## 12. Performance Standards (design-driven)

- **Mobile-first, fast LCP:** lightweight hero, deferred below-fold media.
- **Images:** responsive `srcset`, modern formats (WebP/AVIF), compression, lazy-loading below fold, explicit dimensions (no layout shift / good CLS).
- **Video:** compressed, short, lazy-loaded, poster frames, never autoplay-with-sound or render-blocking.
- **Fonts:** preload primary weights, `font-display: swap`, subset; limit to chosen families/weights.
- **Motion:** transform/opacity only (GPU-friendly); no layout-thrashing animations.
- **No heavy libraries** for scroll/motion; prefer CSS + lightweight Intersection Observer reveals.

---

## 13. Token Summary (handoff reference)

```
COLOR
  white #FFFFFF · paper #F6F7F4 · mist #EDF0EC
  green-900 #0A2C22 · green-800 #0E3B2E (brand) · green-700 #14463A
  green-600 #1B5443 · green-tint #E7EEEA
  gold #C9A24B (accent) · gold-deep #B8902F · gold-tint #F3ECD9
  ink #1F2A28 · ink-muted #5C6B66 · line #E3E7E3 · line-strong #CBD2CD
  success #2E7D5B · error #B23A3A · focus #C9A24B

TYPE  (serif display + sans body; sans-only alt available)
  display 60 · h1 48 · h2 36 · h3 28 · h4 22 · lead 20 · body 16 · small 14 · overline 12
  prose max-width 720px · body line-height 1.65

SPACE (8px base)
  4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 96 · 128
  section pad 128/96 desktop → 64/48 mobile

LAYOUT
  grid 12-col · container 1280 · gutter 24→32
  breakpoints: <640 / 640–1023 / 1024–1279 / ≥1280

RADIUS  sm 4 · md 8 · lg 12
SHADOW  sm 0 1px 2px /.05 · md 0 4px 16px /.06 · lg 0 12px 32px /.08  (green-tinted)
MOTION  micro 150–200ms · reveal 350–450ms · section 400–600ms
        ease standard cubic-bezier(.4,0,.2,1) · entrance cubic-bezier(.16,1,.3,1)
        reveal: fade + 16px rise, stagger 60–80ms · hover lift 2–4px · media scale ≤1.03
        respect prefers-reduced-motion
```

---

## Decisions to Confirm Before Build

1. **Typeface direction:** serif-display + sans pairing (intellectual trade-house) vs. sans-only (cleaner modern-logistics). Token-level switch only.
2. **Hover-to-play video:** confirm you'll source short logistics/export clips later (a reserved, poster-fallback slot is specced now).
3. **English-only vs. English + Arabic:** Arabic adds right-to-left layout mirroring to this system — best decided before build.

*This design system, combined with the Phase 2 architecture document, gives a development team everything needed to build consistent, premium, conversion-focused pages directly — no further visual interpretation required.*
