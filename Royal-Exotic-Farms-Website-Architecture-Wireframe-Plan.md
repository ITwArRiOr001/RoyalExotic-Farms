# Royal Exotic Farms — Website Architecture & Wireframe Planning Document
**Phase 2 — UX Architecture, Wireframes & Build Specification**

*Prepared as a build-ready specification. A design agency or development team can construct the full website directly from this document. No visual mockups are required to begin layout; every page is defined by purpose, user journey, section order, content hierarchy, CTA hierarchy, trust elements, and placeholder media requirements.*

---

## Foundational Design System (applies to every page)

**Brand model:** Registered Indian agricultural **export & trading company** that sources through established supplier networks. Honest positioning — never implies ownership of farms or cold storage. Real track record: exports of bananas and onions to **Oman and Abu Dhabi**. Banana is the **flagship**. Family-owned, relationship-driven. Future (not yet launched) expansion into global sourcing and trade consulting.

**Aesthetic:** Premium international trade house / logistics / commodity-trade feel. NOT a farm site. No rustic, cartoon, or childish agriculture styling.

**Color system**
- Base / dominant: **White** (`#FFFFFF`) and soft off-white (`#F7F8F6`) for sections.
- Primary brand: **Deep green** (recommended `#0E3B2E` to `#14463A` range).
- Accent: **Gold** (recommended `#C9A24B` / `#B8902F`), used sparingly — CTAs, dividers, key figures, hairlines.
- Text: charcoal/slate (`#1F2A28`) for body; deep green for headings.

**Typography**
- Headlines: refined serif OR strong geometric sans (intellectual, corporate). Single consistent display family.
- Body: clean, highly legible sans-serif.
- No decorative, handwritten, or playful fonts anywhere.

**Layout language**
- Generous whitespace, structured 12-column grid, max content width ~1200–1280px.
- Logistics-inspired motifs: container/port imagery, world-map graphics, supply-chain line diagrams, clean product shots on neutral backgrounds.
- Subtle motion only: fade-ins, gentle reveals on scroll, soft hover states. No flashy effects.

**Global conversion components (present site-wide)**
- Header CTA button: **"Export Inquiry"** (gold).
- Secondary nav entry: **"Become an Import Partner."**
- Sticky **WhatsApp** quick-contact button (mobile bottom-right; desktop discreet).
- Footer with full company identity and all conversion links.

**Global trust strip** (reusable band, placed on most pages): "Exporting to the Gulf — including Oman & Abu Dhabi · Registered & licensed Indian exporter · Banana-led specialization."

---

## 1. Complete Website Sitemap

```
HOME (/)
│
├── ABOUT US (/about)
│       └── (links to) Founder Story
│
├── FOUNDER STORY (/founder)
│
├── PRODUCTS (/products)                 ← overview
│       ├── BANANA (/products/banana)    ← flagship, deepest page
│       ├── ONION (/products/onion)
│       └── COCONUT (/products/coconut)
│
├── EXPORT PROCESS / HOW WE WORK (/export-process)
│
├── MARKETS WE SERVE (/markets)
│
├── BECOME AN IMPORT PARTNER (/import-partner)   ← high-intent conversion
│
├── EXPORT INQUIRY (/export-inquiry)             ← primary conversion
│
├── INSIGHTS / BLOG (/insights)
│       └── Article template (/insights/{slug})
│
├── CONTACT (/contact)
│
└── LEGAL
        ├── Privacy Policy (/privacy)
        └── Terms (/terms)

RESERVED (future, architected but NOT launched):
└── SOURCING & TRADE SERVICES (/services)
        ├── Global Sourcing
        ├── Supplier Identification
        ├── Import Consultation
        └── Trade Guidance
```

**Conversion assets (not pages):** Company + Product Profile PDF (lead magnet), Image Replacement Map (internal), auto-confirmation emails.

---

## 2. Navigation Structure

**Primary header (left to right):**
`Logo` | Home · About · Products (dropdown) · Export Process · Markets We Serve · Become an Import Partner · Insights · Contact | **[Export Inquiry]** (gold button)

- **Products dropdown:** Banana (flagged "Flagship") · Onion · Coconut · View All Products.
- "About" hover/secondary reveals: Our Story · Founder · How We Work (Export Process).
- Max 2 levels deep. "Become an Import Partner" sits in the main bar to elevate the relationship path.
- Future "Services" is intentionally absent from nav until launch.

**Sticky behavior:** header condenses on scroll; Export Inquiry button always visible.

**Mobile nav:** hamburger → full-screen panel, vertical list, Export Inquiry as a full-width gold button at top of the panel, WhatsApp link pinned at bottom.

---

## 3. Homepage Wireframe (/)

**Purpose:** Establish "real, credible, honest export company with a Gulf track record" within the first screen, then route every visitor toward an inquiry or partnership conversation.

**User journey:** Land → grasp positioning (trade house, not farm) → see proof (Oman/Abu Dhabi, registrations) → recognize flagship (banana) → understand how the trading model works → trust the family/founder → convert via Export Inquiry, Partner, or WhatsApp.

**Sections (top to bottom):**

1. **Hero**
   - Content: Headline ("A trusted Indian export partner connecting quality agricultural products with the Gulf and beyond"), supporting line referencing reliability + family business, primary CTA **[Export Inquiry]**, secondary text-link **[Become an Import Partner]**.
   - Media: full-width logistics-inspired placeholder (port/containers/world-trade visual with deep-green overlay).
   - CTA hierarchy: Primary = Export Inquiry; Secondary = Import Partner.

2. **Trust / Credibility Bar**
   - Content: honest proof points — "Exporting to the Gulf incl. Oman & Abu Dhabi," "Registered & licensed Indian exporter," "Banana-led specialization."
   - Trust elements: certification/registration badges (placeholder slots), small flag/market markers.

3. **Flagship Products**
   - Content: 3 product cards. **Banana featured larger/first** ("Our Flagship"), Onion + Coconut as supporting cards. Each card: image placeholder, name, one-line descriptor, link.
   - CTA: card → product page.

4. **Why Royal Exotic Farms**
   - Content: 3–4 value pillars — Reliable network sourcing · Proven export experience · Transparent operations · Accountable family ownership. Each with icon (line-style, logistics motif) + short copy.
   - Purpose: convert positioning into reasons-to-trust.

5. **How We Work (Export Process snapshot)**
   - Content: horizontal step diagram — Sourcing → Quality Coordination → Documentation & Compliance → Shipping & Delivery. Frames the trading model as a strength.
   - CTA: **[See Our Full Process]** → Export Process page.

6. **Markets We Serve**
   - Content: stylized world/region map highlighting Gulf; honest note on current reach (Oman, Abu Dhabi) and growth ambition.
   - CTA: **[Markets We Serve]**.

7. **Founder / Family-Business Note**
   - Content: short trust statement in founder's voice (vision: connecting Indian agriculture with global markets), founder portrait **placeholder**, signature.
   - CTA: **[Read Our Story]** → Founder page.

8. **Social Proof / Trust**
   - Content: testimonial placeholders (importer quotes), partner/market logos placeholder, repeat-relationship statement.

9. **Lead Magnet**
   - Content: "Download our Company & Product Profile" — short capture (name, company, country, email).
   - CTA: **[Download Profile]**.

10. **Closing Conversion Band**
    - Content: confident closing line; dual CTA **[Export Inquiry]** + **[WhatsApp Us]**.

11. **Footer** (see Section 16).

**CTA hierarchy (page-level):** Primary = Export Inquiry (hero + closing). Secondary = Become an Import Partner. Tertiary = WhatsApp, Profile download, section deep-links.

**Trust elements:** Oman/Abu Dhabi proof, registrations, founder presence, testimonials, transparent process, honest market statement.

**Placeholder media:** hero trade visual; 3 product images; 4 pillar icons; process diagram; region map; founder portrait; 3–4 testimonial avatars/logos. All branded, ratio-locked, swap-ready.

---

## 4. About Us Wireframe (/about)

**Purpose:** Explain *who the company is and how it honestly operates* (trading/sourcing model), reinforcing credibility and family-business trust.

**User journey:** Curious/serious buyer → understands the company is a legitimate, accountable export house → reassured by honest model + track record → moves toward inquiry or founder story.

**Sections:**
1. **Page hero** — "About Royal Exotic Farms," one-line positioning.
2. **Company overview** — registered Indian export & trading company; what we do (source and export quality agricultural products); banana-led.
3. **Our model (honest)** — clearly states sourcing through established supplier networks; frames it as buyer value (we manage India's fragmented supply so you don't). Explicitly avoids farm/cold-storage ownership claims.
4. **Track record** — exports to Oman and Abu Dhabi; Gulf focus; growth path.
5. **Values band** — Trust · Professionalism · Reliability · Long-term relationships · Family ownership (icon + line each).
6. **Founder teaser** — short, links to Founder Story page.
7. **Registrations & compliance** — held registrations/licenses (placeholder badges), honest framing.
8. **CTA band** — **[Export Inquiry]** + **[Become an Import Partner]**.

**Content hierarchy:** Who we are → how we honestly operate → proof → values → people → compliance → convert.
**CTA hierarchy:** Primary Export Inquiry; Secondary Founder Story / Import Partner.
**Trust elements:** honest model statement, track record, registrations, values, founder link.
**Placeholder media:** corporate/trade hero image, model/process supporting graphic, value icons, registration badges, founder thumbnail.

---

## 5. Founder Story Page Wireframe (/founder)

**Purpose:** Humanize the brand and provide a named, accountable face — the strongest personal-trust device, also the foundation for future consulting.

**User journey:** Trust-seeking buyer → reads vision and values → feels personal accountability → converts with higher confidence.

**Sections:**
1. **Hero** — founder portrait **placeholder** (professional, neutral/corporate backdrop), name, title, one-line vision.
2. **The vision** — narrative: building a respected export company connecting Indian agriculture with global markets; honesty and reliability as principles.
3. **Family-business values** — why family ownership means personal accountability for every shipment.
4. **A note on how we work** — brief reiteration of the honest sourcing/trading model in the founder's voice.
5. **Where we're heading** — restrained mention of future ambition (sourcing/trade guidance) framed as a natural extension — does not overshadow export.
6. **Personal commitment / signature** — direct "you work with the people who answer for the work" statement + signature graphic.
7. **CTA band** — **[Start a Conversation]** → Export Inquiry, plus **[WhatsApp]**.

**Content hierarchy:** Person → vision → values → model → future → commitment → convert.
**CTA hierarchy:** Primary Export Inquiry; Secondary WhatsApp.
**Trust elements:** real person, vision clarity, accountability language, restrained honesty about future plans.
**Placeholder media:** founder portrait (primary), optional secondary candid/working placeholder, signature graphic.

---

## 6. Products Overview Page Wireframe (/products)

**Purpose:** Present the product range with banana clearly flagship, route buyers to detailed product pages and inquiry.

**User journey:** Buyer scanning capability → identifies relevant product → clicks through to specs → inquires.

**Sections:**
1. **Hero** — "Our Products," positioning line (quality, sourced reliably, export-ready).
2. **Flagship feature — Banana** — large feature block: image placeholder, why it's the flagship, key descriptors, **[Explore Banana Exports]**.
3. **Supporting products** — Onion + Coconut cards with image, short descriptor, link.
4. **Quality & handling statement** — honest summary of quality coordination across the network (no facility-ownership claims).
5. **Packaging & export readiness** — general note on packaging/grading/documentation suited to Gulf buyers.
6. **CTA band** — **[Export Inquiry]** + **[Download Product Profile]**.

**Content hierarchy:** Range overview → flagship → supporting → quality → readiness → convert.
**CTA hierarchy:** Primary Export Inquiry; Secondary product deep-links / profile download.
**Trust elements:** quality coordination statement, export-readiness, flagship clarity.
**Placeholder media:** banana feature image, onion + coconut images, packaging/handling graphic.

---

## 7. Banana Product Page Wireframe (/products/banana) — FLAGSHIP (deepest page)

**Purpose:** The most developed product page; converts banana-interested importers with depth and confidence.

**User journey:** Banana buyer → sees variety/grade/specs/packaging/availability → trusts capability → submits Export Inquiry pre-filled to banana.

**Sections:**
1. **Hero** — "Banana Exports," flagship badge, hero image placeholder, primary **[Request Banana Quote]**.
2. **Overview** — banana as flagship category; sourcing strength via network.
3. **Varieties & grades** — variety (e.g., Cavendish/Grand Naine — to confirm), grade tiers (placeholders for verified specs).
4. **Specifications table** — size, grade, weight/box, maturity standards (build table; populate with verified data).
5. **Packaging options** — carton specs, labeling, export packaging (image placeholders).
6. **Availability / seasonality** — supply continuity note.
7. **Quality & handling** — honest quality-coordination process; documentation/phytosanitary handling.
8. **Logistics** — ports/Incoterms (FOB/CIF as confirmed), lead-time framing.
9. **Why source banana from us** — reliability, track record, accountability.
10. **Conversion band** — **[Request Banana Quote]** (pre-tags product) + **[WhatsApp]**.

**Content hierarchy:** Hero → overview → varieties → specs → packaging → availability → quality → logistics → reasons → convert.
**CTA hierarchy:** Primary Banana-tagged Export Inquiry; Secondary WhatsApp.
**Trust elements:** detailed specs, honest handling/logistics, track record callback, flagship depth.
**Placeholder media:** hero banana visual, variety images, packaging shots, logistics/container image, spec table (data placeholder).

---

## 8. Onion Product Page Wireframe (/products/onion)

**Purpose:** Solid secondary product page; convert onion buyers; reinforce real onion export track record (Oman/Abu Dhabi).

**User journey:** Onion buyer → specs/packaging/availability → inquiry.

**Sections:**
1. **Hero** — "Onion Exports," image placeholder, **[Request Onion Quote]**.
2. **Overview** — sourcing strength; proven onion export experience (honest).
3. **Varieties & sizes** — variety, sizing/grading (placeholder specs).
4. **Specifications table** — size, packing, quality standards.
5. **Packaging options** — mesh/bags/cartons (image placeholders).
6. **Availability** — supply continuity.
7. **Quality & handling** — honest coordination + documentation.
8. **Conversion band** — onion-tagged **[Export Inquiry]** + **[WhatsApp]**.

**Content hierarchy / CTA hierarchy:** as Banana, lighter depth.
**Trust elements:** proven onion exports, specs, honest handling.
**Placeholder media:** hero, variety images, packaging shots, spec table placeholder.

---

## 9. Coconut Product Page Wireframe (/products/coconut)

**Purpose:** Secondary product page; convert coconut buyers; show range breadth.

**User journey:** Coconut buyer → type/specs/packaging → inquiry.

**Sections:**
1. **Hero** — "Coconut Exports," image placeholder, **[Request Coconut Quote]**.
2. **Overview** — sourcing capability.
3. **Types** — semi-husked / husked / tender (confirm offering).
4. **Specifications table** — size/weight/packing.
5. **Packaging options** — export packaging (placeholders).
6. **Availability** — year-round framing.
7. **Quality & handling** — honest coordination.
8. **Conversion band** — coconut-tagged **[Export Inquiry]** + **[WhatsApp]**.

**Content / CTA hierarchy:** as Onion.
**Trust elements:** specs, honest handling, range credibility.
**Placeholder media:** hero, type images, packaging shots, spec table placeholder.

---

## 10. Export Process Page Wireframe (/export-process) — "How We Work"

**Purpose:** Turn the trading/sourcing model into a transparent, confidence-building process — the key page for honestly explaining the non-farm model.

**User journey:** Risk-averse buyer → understands each step is controlled and documented → trust rises → inquires.

**Sections:**
1. **Hero** — "How We Work," line on transparent, reliable export process.
2. **Process step diagram** — Sourcing (network) → Quality Coordination → Packaging & Grading → Documentation & Compliance → Logistics & Shipping → Delivery & Support. Each step: icon, short copy.
3. **Quality assurance** — how quality is coordinated across suppliers honestly (no owned-facility claims).
4. **Documentation & compliance** — export docs, phytosanitary, certifications handled.
5. **Communication & accountability** — response commitment, single accountable point of contact (family business).
6. **Track record callout** — Oman/Abu Dhabi as proof the process works.
7. **CTA band** — **[Export Inquiry]** + **[Become an Import Partner]**.

**Content hierarchy:** Process → quality → compliance → accountability → proof → convert.
**CTA hierarchy:** Primary Export Inquiry; Secondary Import Partner.
**Trust elements:** transparent steps, compliance detail, accountability, real track record.
**Placeholder media:** process icons/diagram, compliance/documents graphic, logistics image.

---

## 11. Markets We Serve Page Wireframe (/markets)

**Purpose:** Anchor the real Gulf track record honestly and frame expansion ambition.

**User journey:** Buyer checks geographic fit/credibility → sees real markets served → confident to engage.

**Sections:**
1. **Hero** — "Markets We Serve," Gulf-first positioning.
2. **Region map** — stylized map highlighting Gulf; markers for Oman and Abu Dhabi (proven), broader Gulf as target.
3. **Current reach (honest)** — explicit, truthful statement of where the company has exported.
4. **Target markets** — UAE, Saudi Arabia, Qatar, Kuwait, Oman, Bahrain; rationale (import-dependent, India proximity advantage).
5. **Why buyers choose an Indian partner** — freight time, cost, supply scale, reliability.
6. **Future reach** — international ambition framed honestly.
7. **CTA band** — **[Export Inquiry]** + **[Become an Import Partner]**.

**Content hierarchy:** Map → current reach → targets → advantages → future → convert.
**CTA hierarchy:** Primary Export Inquiry; Secondary Import Partner.
**Trust elements:** honest current reach, real markets, logical advantages.
**Placeholder media:** region map graphic, flag/market markers, optional shipping route visual.

---

## 12. Become An Import Partner Page Wireframe (/import-partner)

**Purpose:** Frame a long-term sourcing relationship (not a one-off sale); capture the highest-quality leads.

**User journey:** Distributor/importer seeking an ongoing India partner → sees relationship value → completes a qualifying partnership form.

**Sections:**
1. **Hero** — "Build a long-term sourcing partnership with Royal Exotic Farms."
2. **What partnership means** — consistent supply coordination, flagship banana priority, transparent dealing, named accountable team.
3. **Who this is for** — importers, distributors, retail procurement, re-exporters, cold storage operators.
4. **How partnership works** — onboarding → understanding requirements → ongoing supply → support.
5. **Honest model note** — reiterate sourcing-through-networks value.
6. **Partnership inquiry form** (high-intent, qualifying): Name · Company · Country · Product lines of interest · Estimated volume · Order frequency · Target market · Message · consent. Spam protection.
7. **Reassurance** — response commitment + WhatsApp alternative.

**Content hierarchy:** Value → audience → process → honesty → qualifying form → reassurance.
**CTA hierarchy:** Primary = submit partnership form; Secondary = WhatsApp.
**Trust elements:** relationship framing, accountability, honest model, clear process.
**Placeholder media:** partnership/handshake-of-trade (logistics-styled, not cliché) hero, process icons.

---

## 13. Export Inquiry Page Wireframe (/export-inquiry) — PRIMARY CONVERSION

**Purpose:** The main lead-capture page; low-friction, high-trust.

**User journey:** Ready buyer → minimal friction → submits inquiry → receives auto-confirmation.

**Sections:**
1. **Hero** — "Request an Export Inquiry," reassurance subline (response time).
2. **Trust strip** — Oman/Abu Dhabi, registrations (keeps confidence high beside the form).
3. **Inquiry form** (short): Name · Company · Country · Product interest (Banana/Onion/Coconut/Other, pre-fillable from product pages) · Quantity (optional) · Message · consent checkbox. Validation + spam protection (honeypot/captcha). No account creation.
4. **What happens next** — 3-step expectation (we review → we respond within stated time → we discuss terms/samples).
5. **Alternative contact** — WhatsApp + email + phone.

**Content hierarchy:** Reassure → trust → form → expectations → alternatives.
**CTA hierarchy:** Primary = submit; Secondary = WhatsApp.
**Trust elements:** track-record strip, response promise, clear next steps, secure handling note.
**Placeholder media:** light supporting trade visual only (form is the focus).

---

## 14. Contact Page Wireframe (/contact)

**Purpose:** Provide verifiable identity and multiple contact channels — itself a trust signal.

**User journey:** Buyer verifying legitimacy → finds real address, channels → contacts or inquires.

**Sections:**
1. **Hero** — "Contact Royal Exotic Farms."
2. **Contact details** — registered company name, physical address, phone, WhatsApp, email, business hours (with timezone — helpful for Gulf buyers).
3. **General contact form** — Name · Company · Country · Subject · Message · consent.
4. **Map** — office location (placeholder/embed).
5. **Quick links** — Export Inquiry · Become an Import Partner.
6. **Response commitment** — stated reply window.

**Content hierarchy:** Identity/channels → form → location → quick paths.
**CTA hierarchy:** Primary = WhatsApp / form submit; Secondary = Export Inquiry.
**Trust elements:** real identity, address, map, response promise.
**Placeholder media:** map embed/placeholder, optional office image placeholder.

---

## 15. Blog / Insights Page Wireframe (/insights)

**Purpose:** SEO engine + thought leadership; future home for trade-guidance content that previews the consulting expansion.

**User journey:** Searcher/buyer → reads credible trade content → trust + organic discovery → enters funnel.

**Sections (listing page):**
1. **Hero** — "Insights — Export & Trade Knowledge."
2. **Featured article** — large card.
3. **Article grid** — image, title, excerpt, category, date.
4. **Categories/filter** — Banana & Produce · Gulf Markets · Export & Compliance · Trade Guidance (seeds future consulting).
5. **Newsletter / profile capture** — email capture.
6. **CTA band** — **[Export Inquiry]**.

**Article template (/insights/{slug}):** title, meta (date, author, read time), hero image placeholder, structured body (H2/H3), pull quotes, related articles, inline CTA to Export Inquiry, share. Built for SEO (structured data, clean headings).

**Content hierarchy:** Featured → grid → categories → capture → convert.
**CTA hierarchy:** Primary Export Inquiry; Secondary newsletter.
**Trust elements:** expertise demonstrated, professional tone, consistency.
**Placeholder media:** featured + article thumbnails (ratio-locked), author avatar placeholder.

---

## 16. Footer Architecture

**Structure (4–5 columns + base bar):**
- **Column 1 — Company:** logo, one-line positioning, registered company name, brief honest descriptor.
- **Column 2 — Explore:** Home · About · Founder · Export Process · Markets.
- **Column 3 — Products:** Banana (Flagship) · Onion · Coconut.
- **Column 4 — Work With Us:** Export Inquiry · Become an Import Partner · Contact.
- **Column 5 — Contact & Connect:** address, phone, WhatsApp, email, social placeholders.
- **Base bar:** © Royal Exotic Farms · Privacy Policy · Terms · "Registered Indian export & trading company."

**Trust elements in footer:** registration line, real contact details, certification badge placeholders (honest), Export Inquiry CTA repeated.

**Notes:** consistent across all pages; mobile collapses columns into stacked accordions or sections.

---

## 17. Mobile Experience Strategy

Mobile-first is essential — Gulf buyers frequently browse and message on mobile.

- **Performance:** mobile-first, fast LCP; compressed responsive images; lazy-loading below the fold.
- **Navigation:** hamburger → full-screen menu; Export Inquiry as full-width gold button at top; WhatsApp pinned.
- **Sticky conversion:** persistent bottom bar or floating buttons — **WhatsApp** + **Export Inquiry** always reachable.
- **Tap targets:** large, spaced; thumb-friendly.
- **Forms:** single-column, large fields, correct input types/keyboards, minimal fields, inline validation.
- **Content:** sections stack logically; tables (specs) become scrollable/stacked cards; process diagrams reflow vertically.
- **Hero:** lighter media weight on mobile; text + CTA prioritized above the fold.
- **WhatsApp deep link:** prefilled message ("Hello Royal Exotic Farms, I'd like to inquire about…").
- **Accessibility:** sufficient contrast (white/deep-green/gold tested for WCAG AA), scalable text, focus states, alt text on all media.

---

## 18. Image & Video Placeholder Strategy

Given limited real photography, all media must look intentional and premium — never broken or "image here."

- **Placeholder style:** branded neutral imagery or clean abstract/geometric trade-themed graphics with subtle deep-green overlay and gold hairline accents; consistent ratios per slot.
- **Honesty guardrail:** placeholders must NEVER imply owned farms/cold storage. Use shipping/logistics/produce-on-neutral visuals and honest captions.
- **Ratio-locked slots:** every image area defined by fixed aspect ratio so real photos drop in with zero redesign (hero 16:9 / 21:9; product 4:3 or 1:1; founder portrait 3:4; thumbnails 16:9).
- **Priority capture list (for the founder over time):** founder portrait → product shots (banana first) → packaging/cartons → shipment/container photos → office. 
- **Video (future-ready):** reserve a homepage/process video slot (muted autoplay loop placeholder) for a future company/process film; lazy-loaded, never blocks load.
- **Image Replacement Map (internal deliverable):** documented table — each slot's ID, page, ratio, purpose, and the real photo intended to replace it.
- **Alt text:** every placeholder ships with descriptive, honest alt text for SEO + accessibility.

---

## 19. Lead Generation Funnel Mapping

**Top of funnel (awareness):** Organic search (SEO product/market keywords), Insights articles, social → land on Home / Product / Market pages.

**Mid funnel (consideration):** Trust building via About, Founder, Export Process, Markets, track record (Oman/Abu Dhabi), certifications. Lead magnet (Company & Product Profile) captures not-yet-ready buyers (email).

**Bottom funnel (conversion):** Three routed paths —
1. **Export Inquiry** (primary) — from every product page + header + closing bands.
2. **Become an Import Partner** (high-intent, qualifying) — for long-term relationships.
3. **WhatsApp / Contact** — fast, preferred channel.

**Funnel map by intent:**
- *Quick/transactional buyer (re-exporter)* → WhatsApp / Export Inquiry.
- *Cautious first-timer* → Founder + Export Process → Export Inquiry.
- *Compliance-driven retail* → Certifications + Profile download → Export Inquiry.
- *Long-term distributor* → Become an Import Partner.

**Post-conversion:** auto-confirmation email → founder/sales follow-up within stated window → samples/terms discussion → first order → repeat-relationship nurture (availability/price email updates). Dashboard-ready tracking: visitor, form submission, click, source — captured per submission.

---

## 20. Conversion Optimization Recommendations

1. **Trust before the ask** — never place a form before proof; track record + registrations precede every conversion point.
2. **Single dominant CTA per screen** — Export Inquiry (gold) is unmistakable; avoid competing equal-weight buttons.
3. **Pre-fill product context** — product-page CTAs pass the product into the inquiry form to reduce friction and improve lead quality.
4. **WhatsApp prominence** — Gulf buyers convert faster on WhatsApp; keep it persistent with a prefilled message.
5. **Response-time promise** — stated reply window beside every form reduces abandonment.
6. **Short forms** — only essential fields on Export Inquiry; richer qualifying fields only on Partner form (where higher intent justifies friction).
7. **Lead magnet** — Company & Product Profile captures early-stage buyers' emails for nurture.
8. **Honest specificity** — concrete, defensible claims (Oman/Abu Dhabi, registrations) outperform superlatives and build durable trust.
9. **Auto-confirmation + clear next steps** — manage expectations immediately after submission.
10. **Speed & mobile** — fast load and frictionless mobile forms directly lift conversion.
11. **Founder presence** — personal accountability raises confidence at decision points.
12. **Analytics-driven iteration** — track form starts vs. completions, drop-off fields, source-to-inquiry, CTA click rates; optimize the weakest step. Define success as *qualified inquiry rate*, not raw traffic.
13. **Friction-free trust pages** — make About / Founder / Process easy to reach from the funnel; they are conversion *enablers*, not detours.
14. **Accessibility = conversion** — AA contrast, keyboard/focus support, alt text widen reach and signal professionalism.

---

## Build Notes for the Development Team

- **Stack alignment (per project brief):** HTML/CSS/JS frontend, Python Flask backend; four forms (Contact, Consultation, Export Inquiry, Partnership) with secure handling, validation, spam protection, and automatic email notifications; analytics architecture (visitor/form/click tracking) built dashboard-ready; SEO baseline (metadata, Open Graph, structured data, sitemap).
- **Scalability:** product pages use one shared template (new products plug in); reserved `/services` section architected (not launched) for future sourcing/consulting.
- **Honesty compliance:** no copy or imagery may claim owned farms or cold storage, or overstate volume/reach. Every claim must be verifiable.
- **Outstanding data to populate (carry-over from discovery):** verified banana/onion/coconut specs, MOQs, packaging, varieties; Incoterms & payment terms; ports used; exact registrations to display; real photography (per Image Replacement Map); confirmed contact details, WhatsApp number, and response-time commitment; language requirement (English / English+Arabic).

*End of Phase 2 — Architecture & Wireframe Planning Document.*
