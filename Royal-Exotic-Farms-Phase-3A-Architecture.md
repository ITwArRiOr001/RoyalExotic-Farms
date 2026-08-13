# Royal Exotic Farms — Phase 3A: Project Architecture & HTML Foundation Plan
**Flask Application Architecture · Implementation Blueprint for Phase 3B+**

*This document defines the complete development architecture. It contains no CSS, no JavaScript, no backend logic, no page content, and no marketing copy — only structure, routing, inheritance, and the implementation plan that later phases will build against. File trees and dependency lists are structural references, not code. Everything is designed so future Arabic, future products, and future sourcing services can be added without restructuring, and so certification PDFs attach cleanly later.*

---

## 1. Architectural Approach (governing decisions)

- **App factory pattern** (`create_app`) — clean config separation, testability, and reliable Render deployment.
- **Blueprints** for modular, low-duplication organization — each domain isolated, future modules drop in without touching others.
- **Locale-prefixed routing** (`/en/...`, future `/ar/...`) wired now; English-only content.
- **Data-driven product & certification pages** — adding a product or certificate is a *data* change, never a template/redesign change.
- **Template inheritance + Jinja macros** — one base, shared partials, reusable component macros; duplication minimized.
- **Reserved (registered-later) services blueprint** for future sourcing/consulting.
- **Dashboard-ready persistence** — form submissions and analytics events modeled now for a future dashboard.

---

## 2. Complete File Tree

```
royal-exotic-farms/
├── app/
│   ├── __init__.py                 # create_app(): config, extensions, blueprint + error handlers, babel locale selector
│   ├── config.py                   # BaseConfig, DevConfig, ProdConfig (env-driven)
│   ├── extensions.py               # singletons: db, migrate, babel, mail, csrf, limiter, compress
│   ├── i18n.py                     # SUPPORTED_LOCALES, DEFAULT_LOCALE, locale resolver, lang URL converter
│   │
│   ├── blueprints/
│   │   ├── main/
│   │   │   ├── __init__.py         # bp = Blueprint('main', ...)
│   │   │   └── routes.py           # home, about, founder, export-process, markets, contact (GET), legal
│   │   ├── products/
│   │   │   ├── __init__.py
│   │   │   └── routes.py           # products index + detail (data-driven by slug)
│   │   ├── insights/
│   │   │   ├── __init__.py
│   │   │   └── routes.py           # insights index + article
│   │   ├── forms/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py           # GET form pages (export-inquiry, import-partner) + POST handlers (all 4 forms)
│   │   │   └── forms.py            # WTForms classes (Contact, Consultation, ExportInquiry, Partnership)
│   │   ├── analytics/
│   │   │   ├── __init__.py
│   │   │   └── routes.py           # /api/track (visitor/click/form events) — dashboard-ready
│   │   ├── seo/
│   │   │   ├── __init__.py
│   │   │   └── routes.py           # /sitemap.xml, /robots.txt
│   │   └── services/               # RESERVED — future sourcing/consulting (scaffolded, NOT registered in v1)
│   │       ├── __init__.py
│   │       └── routes.py
│   │
│   ├── models/                     # SQLAlchemy models (dashboard-ready persistence)
│   │   ├── __init__.py
│   │   ├── submission.py           # FormSubmission (type, payload, locale, source, timestamp, status)
│   │   └── event.py                # AnalyticsEvent (event_type, path, ref, meta, session, timestamp)
│   │
│   ├── data/                       # structured registries = single source of truth (no marketing copy)
│   │   ├── navigation.py           # nav tree (drives header + footer; one source)
│   │   ├── products.py             # product registry: slug, name, flagship flag, spec keys, media keys, order
│   │   ├── certifications.py       # cert registry: code, label, status, document (nullable), order
│   │   └── markets.py              # served + target markets registry
│   │
│   ├── content/                    # locale-ready structured content store (authored later, not now)
│   │   ├── en/                     # English content lives here
│   │   └── ar/                     # RESERVED, empty — future Arabic
│   │
│   ├── templates/
│   │   ├── base.html               # root layout: <html lang/dir>, head, header, {% block content %}, footer, scripts
│   │   ├── partials/
│   │   │   ├── head_seo.html        # title, meta, canonical, OG, Twitter, hreflang
│   │   │   ├── structured_data.html # JSON-LD (Organization + per-page schema block)
│   │   │   ├── analytics_head.html  # GA4 / tag slot + event bootstrap hook
│   │   │   ├── header.html
│   │   │   ├── nav.html
│   │   │   ├── language_switcher.html  # built, hidden in v1
│   │   │   ├── footer.html
│   │   │   ├── whatsapp_button.html    # sticky mobile / discreet desktop
│   │   │   ├── trust_strip.html
│   │   │   └── certifications_section.html  # reused on home + about
│   │   ├── components/              # Jinja MACROS (reusable, parameterized)
│   │   │   ├── buttons.html          # primary/secondary/tertiary/on-dark
│   │   │   ├── cards.html            # product_card, value_card, article_card, certification_card
│   │   │   ├── forms.html            # field, textarea, select, consent, errors, honeypot
│   │   │   ├── section_opener.html   # eyebrow + heading + lead
│   │   │   └── cta_band.html
│   │   ├── pages/
│   │   │   ├── home.html
│   │   │   ├── about.html
│   │   │   ├── founder.html
│   │   │   ├── export_process.html
│   │   │   ├── markets.html
│   │   │   ├── import_partner.html
│   │   │   ├── export_inquiry.html
│   │   │   ├── contact.html
│   │   │   ├── privacy.html
│   │   │   └── terms.html
│   │   ├── products/
│   │   │   ├── index.html            # overview
│   │   │   └── detail.html           # SINGLE template for ALL products (future-proof)
│   │   ├── insights/
│   │   │   ├── index.html
│   │   │   └── article.html
│   │   ├── forms/
│   │   │   └── success.html          # post-submit confirmation
│   │   └── errors/
│   │       ├── 404.html
│   │       └── 500.html
│   │
│   ├── static/
│   │   ├── css/                     # built in Phase 3B+ (not now)
│   │   ├── js/                      # built in Phase 3B+ (not now)
│   │   ├── fonts/                   # display + body; reserved Arabic font slot
│   │   ├── img/
│   │   │   ├── brand/  hero/  products/  founder/  markets/  certifications/  icons/  placeholders/
│   │   ├── video/
│   │   │   └── hero/                # hero montage + poster frame
│   │   ├── docs/
│   │   │   └── certifications/      # PDF attachments added later (IEC, GST, APEDA, FSSAI, …)
│   │   └── favicon/
│   │
│   └── translations/
│       ├── en/LC_MESSAGES/messages.po(.mo)
│       └── ar/LC_MESSAGES/          # RESERVED, empty — future Arabic catalog
│
├── migrations/                      # Flask-Migrate (generated)
├── tests/
├── babel.cfg                        # Babel string-extraction config
├── requirements.txt
├── wsgi.py                          # gunicorn entrypoint -> create_app()
├── render.yaml                      # Render deployment manifest
├── Procfile                         # alt process declaration
├── .env.example
├── .gitignore
└── README.md
```

---

## 3. Route Architecture

All page routes carry a locale prefix via a `<lang>` URL converter restricted to `SUPPORTED_LOCALES` (v1: `en`; future: `en, ar`). Non-locale utility routes (api, sitemap, robots, static) are locale-agnostic.

| Method | Path | Endpoint | Template | Notes |
|---|---|---|---|---|
| GET | `/` | (redirect) | — | 302 → `/en/` (default locale) |
| GET | `/<lang>/` | `main.home` | pages/home.html | Homepage |
| GET | `/<lang>/about` | `main.about` | pages/about.html | |
| GET | `/<lang>/founder` | `main.founder` | pages/founder.html | |
| GET | `/<lang>/export-process` | `main.export_process` | pages/export_process.html | |
| GET | `/<lang>/markets` | `main.markets` | pages/markets.html | |
| GET | `/<lang>/contact` | `main.contact` | pages/contact.html | Form posts to forms bp |
| GET | `/<lang>/privacy` | `main.privacy` | pages/privacy.html | |
| GET | `/<lang>/terms` | `main.terms` | pages/terms.html | |
| GET | `/<lang>/products` | `products.index` | products/index.html | Lists from data/products.py |
| GET | `/<lang>/products/<slug>` | `products.detail` | products/detail.html | Data-driven; 404 if slug unknown |
| GET | `/<lang>/insights` | `insights.index` | insights/index.html | |
| GET | `/<lang>/insights/<slug>` | `insights.article` | insights/article.html | |
| GET | `/<lang>/export-inquiry` | `forms.export_inquiry_page` | pages/export_inquiry.html | Pre-fills product via query param |
| GET | `/<lang>/import-partner` | `forms.import_partner_page` | pages/import_partner.html | |
| POST | `/<lang>/submit/contact` | `forms.submit_contact` | → forms/success.html | |
| POST | `/<lang>/submit/consultation` | `forms.submit_consultation` | → forms/success.html | |
| POST | `/<lang>/submit/export-inquiry` | `forms.submit_export_inquiry` | → forms/success.html | |
| POST | `/<lang>/submit/partner` | `forms.submit_partner` | → forms/success.html | |
| POST | `/api/track` | `analytics.track` | — (JSON) | Visitor/click/form events |
| GET | `/sitemap.xml` | `seo.sitemap` | (XML) | Generated from registries + locales |
| GET | `/robots.txt` | `seo.robots` | (text) | |
| — | `/<lang>/services[/...]` | `services.*` | — | **RESERVED**, not registered in v1 |

**Locale guard:** unknown `<lang>` → redirect to default locale (or 404). The `<lang>` converter is the single switch that activates Arabic later.

---

## 4. Blueprint Architecture (recommended)

Blueprints chosen so each future expansion is additive:

- **`main`** — static/marketing pages (home, about, founder, export-process, markets, contact, legal).
- **`products`** — overview + data-driven detail; new products require only a `data/products.py` entry.
- **`insights`** — blog listing + article template; SEO content engine; future home for trade-guidance content.
- **`forms`** — all four form pages and POST handlers + WTForms definitions; isolates validation, spam protection, email, persistence.
- **`analytics`** — `/api/track` ingestion endpoint; dashboard-ready event capture.
- **`seo`** — sitemap and robots generation.
- **`services`** — RESERVED future sourcing/consulting; scaffolded but **not registered** in v1, so it ships when ready without touching existing routes.

All locale-prefixed blueprints are registered under the `<lang>` prefix centrally in `create_app`, keeping locale logic in one place.

---

## 5. Template Architecture & Inheritance

**Inheritance hierarchy:**

```
base.html
 ├── pages/*.html            (extend base, fill content block)
 ├── products/index.html     (extend base)
 ├── products/detail.html    (extend base; one template, all products)
 ├── insights/index.html     (extend base)
 ├── insights/article.html   (extend base)
 ├── forms/success.html      (extend base)
 └── errors/404.html, 500.html (extend base)
```

**`base.html` blocks (defined, filled by children):**
- `{% block title %}`, `{% block meta %}` (via head_seo partial), `{% block structured_data %}`
- `{% block content %}` (page body)
- `{% block page_scripts %}` (per-page script hooks, populated later)

**Partials** (`{% include %}`): head_seo, structured_data, analytics_head, header, nav, language_switcher, footer, whatsapp_button, trust_strip, certifications_section.

**Components** (`{% import %}` macros): buttons, cards (product/value/article/certification), forms (fields/consent/honeypot/errors), section_opener, cta_band. Macros are the primary duplication-avoidance mechanism — every card and form field renders through one definition.

**Future-proofing built in:** product detail is a *single* template; certifications render via *one* macro over a data list; nav renders from *one* registry into both header and footer.

---

## 6. Base Template Strategy

`base.html` owns the global shell: `<!doctype>`, `<html lang dir>` (locale-driven), `<head>` (SEO partial + structured data + analytics slot + font preloads + CSS link reserved), skip-link for a11y, `header` include, main content block, `footer` include, sticky `whatsapp_button` include, and a deferred scripts block. The `lang`/`dir` attributes derive from the active locale so RTL activates with no template edits. Every page inherits this shell; pages never redefine head, header, or footer.

---

## 7. Shared Component Strategy

| Component | Type | Used by |
|---|---|---|
| section_opener (eyebrow/heading/lead) | macro | all pages |
| buttons (primary/secondary/tertiary/on-dark) | macro | all pages |
| product_card | macro | home, products index |
| value_card | macro | home, about, why-us sections |
| article_card | macro | insights index, related articles |
| certification_card (open/download actions) | macro | certifications_section (home + about), footer |
| form field / consent / honeypot / error | macro | all four forms |
| trust_strip | partial | home, product pages, markets, inquiry |
| certifications_section | partial | home, about |
| cta_band | macro | most pages |
| whatsapp_button | partial | global (base) |
| nav / footer | partial (from navigation registry) | global (base) |

One definition per component; pages compose them. Adding a product card or certification card never requires new markup — only new data.

---

## 8. Header Architecture

Rendered from `data/navigation.py` (single source). Structure: brand lockup (links home) · primary nav (Home, About, Products dropdown, Export Process, Markets, Become an Import Partner, Insights, Contact) · persistent **Export Inquiry** CTA · language switcher slot (present, hidden in v1). Products dropdown is generated from the product registry (flagship flagged). Mobile: hamburger → full-screen panel with Export Inquiry at top, WhatsApp pinned. The header is a partial included by `base.html`; locale-aware so links resolve to the active locale prefix automatically.

---

## 9. Footer Architecture

Rendered from the same navigation registry. Columns: Company (identity + registration line) · Explore · Products · Work With Us (Export Inquiry, Import Partner, Contact) · Contact & Connect. Includes a compact **certification badges** row (certification_card in badge mode) and a base bar with Privacy/Terms + locale-aware links. Single partial, included globally; collapses to accordions on mobile.

---

## 10. SEO Architecture

- **`head_seo.html`** partial: per-page `<title>`, meta description, canonical URL, Open Graph (type/title/description/image/url/site_name), Twitter card, and **hreflang** alternates. v1 emits `en` (and `x-default`); the hreflang list is generated from `SUPPORTED_LOCALES`, so Arabic alternates appear automatically when `ar` activates.
- **`structured_data.html`** partial: JSON-LD — global `Organization` (name, logo, contact, country) on every page, plus a per-page schema block (`Product` on product pages, `Article` on insights articles, `BreadcrumbList` where relevant).
- **Per-page SEO data** passed from routes (title, description, canonical, og_image, schema type) — defined as page config, not hard-coded in templates.
- **`seo` blueprint:** dynamic `sitemap.xml` (built from static routes + product/insight slugs × locales) and `robots.txt`.
- Semantic HTML, single H1 per page, descriptive link text, image alt text — enforced at template level.

---

## 11. Internationalization Architecture

- **Flask-Babel** initialized in `extensions.py`; locale resolved from the URL `<lang>` segment in `i18n.py` (`SUPPORTED_LOCALES`, `DEFAULT_LOCALE='en'`).
- **All display strings via translation functions** (`{% trans %}` / `_()`) — no hard-coded copy in templates. (Strings are authored in Phase 3B; the *mechanism* is mandated now.)
- **Catalogs:** `translations/en/LC_MESSAGES/messages.po` active; `translations/ar/` scaffolded empty.
- **`babel.cfg`** configured to extract strings from templates and Python.
- **URL strategy:** locale prefix on all page routes; `/` redirects to default locale.
- **Locale-aware formatting** (dates/numbers) via Babel.
- Activation later = add `ar` to `SUPPORTED_LOCALES`, populate the `ar` catalog, reveal the language switcher — no structural change.

---

## 12. Future Arabic / RTL Architecture

- `<html lang dir>` is locale-driven in `base.html`; `ar` → `dir="rtl"` with zero template edits.
- **CSS will use logical properties** (mandated in the design system) so layout mirrors automatically under RTL — recorded here as a binding constraint for Phase 3B styling.
- **Direction-aware components:** nav, process timeline, route diagrams, and directional icons designed to mirror under `[dir="rtl"]`.
- **Reserved Arabic font slot** in `static/fonts/` mapped to existing type tokens; not loaded in v1.
- **Language switcher** built and hidden in v1; reveals on Arabic launch.
- Content store (`content/ar/`) and translation catalog (`translations/ar/`) reserved and empty.

---

## 13. Static Asset Architecture

- Namespaced under `static/`: `css/`, `js/`, `fonts/`, `img/` (subfoldered by purpose), `video/`, `docs/`, `favicon/`.
- **Cache-busting:** asset versioning (query-string hash or build manifest) planned for production; static served efficiently on Render (WhiteNoise/compressed).
- CSS/JS folders exist now but are populated in Phase 3B+.
- Fonts: display + body families with the reserved Arabic slot; preloaded primary weights.

---

## 14. Image & Video Asset Architecture

- **Image folders by role:** brand, hero, products, founder, markets, certifications, icons, placeholders.
- **Ratio-locked slots** per the design system (hero 16:9/21:9, product 4:3/1:1, founder 3:4, thumbnails 16:9); responsive `srcset` + modern formats planned; lazy-loading below fold; explicit dimensions for CLS.
- **Placeholders** are branded and swap-ready; the **Image Replacement Map** (internal) tracks each slot → intended real asset.
- **Hero video:** `static/video/hero/` holds the montage (logistics, container terminals, cargo ships, export operations, agricultural products, packaging/shipment prep) + poster frame; muted/looped/autoplay, lazy-loaded, poster + reduced-motion fallback. **No founder video** anywhere.
- Honesty guardrail: no media implies owned farms/cold storage.

---

## 15. Certification PDF Architecture

- **Registry:** `data/certifications.py` holds each certificate: `code` (IEC, GST, APEDA, FSSAI, …), `label`, `status`, `document` (filename or URL, **nullable**), `order`.
- **Storage:** PDFs live in `static/docs/certifications/`; added later by dropping the file and setting `document` in the registry.
- **`certification_card` macro** renders name/label/status + **Open** (new tab, `rel="noopener"`) and **Download** actions. When `document` is null, actions render in a disabled "document coming soon" state — never broken links. Attaching a PDF auto-enables the actions (data-only change).
- **Placements:** certifications_section partial on Home and About; badge row in Footer — all reading the same registry.
- Extensible to future certs (HACCP, ISO 22000, Halal, GLOBALG.A.P.) by adding registry entries only.
- Honesty: only real registrations displayed; accurate statuses.

---

## 16. Form Architecture

- **Four forms** (Flask-WTF + WTForms) in `blueprints/forms/forms.py`: `ContactForm`, `ConsultationForm`, `ExportInquiryForm`, `PartnershipForm` (the qualifying, high-intent form).
- **Rendering:** via shared `forms.html` field macros — consistent markup, labels tied to inputs, inline errors, single-column.
- **Pages:** Export Inquiry and Import Partner are full pages; Contact form on the Contact page; Consultation form surfaced on Contact/Export-Inquiry contexts (dedicated route reserved if later promoted).
- **Submission flow:** POST → server-side validation → spam checks → persist (`FormSubmission`) → send notification email → render `forms/success.html` (with next-steps) → fire analytics `form_submit` event.
- **Spam protection:** CSRF (Flask-WTF), honeypot field, rate limiting (Flask-Limiter); optional captcha hook reserved.
- **Email:** Flask-Mail; automatic notification to the company + confirmation to the submitter; templated.
- **Product pre-fill:** Export Inquiry reads a `product` query param from product-page CTAs.
- **Validation/security:** server-side authoritative; input sanitization; safe handling per requirements.

---

## 17. Analytics-Ready Architecture

- **`analytics` blueprint** exposes `POST /api/track` to ingest events; client script (Phase 3B) posts page views, CTA clicks, and form starts/submits.
- **`AnalyticsEvent` model:** `event_type` (page_view | click | form_start | form_submit), `path`, `referrer`, `meta` (JSON), `session_id`, `locale`, `timestamp`.
- **`FormSubmission` model** doubles as conversion data.
- **Dashboard-ready:** events/submissions persisted in the DB (SQLite dev / Postgres prod) for a future internal dashboard; schema designed for it now.
- **Tag slot:** `analytics_head.html` reserves a GA4 / Tag Manager insertion point (kept separate so server-side and client-side tracking coexist).
- Privacy: consent-aware design; no PII in event meta.

---

## 18. Recommended Flask Extensions

| Extension | Purpose |
|---|---|
| Flask-Babel | i18n / future Arabic + locale formatting |
| Flask-WTF + WTForms | Forms, validation, CSRF |
| Flask-Mail | Automatic email notifications |
| Flask-SQLAlchemy | Persistence (submissions, analytics) — dashboard-ready |
| Flask-Migrate (Alembic) | DB migrations |
| Flask-Limiter | Rate limiting / spam protection |
| Flask-Compress | Gzip/Brotli responses (performance) |
| Flask-Talisman *(optional)* | Security headers / HTTPS enforcement |
| Flask-Caching *(optional)* | Page/fragment caching (performance) |
| python-dotenv | Env config loading |
| email-validator | Email field validation |
| WhiteNoise | Efficient static serving on Render |
| Gunicorn | WSGI server for Render |

---

## 19. Recommended `requirements.txt` Dependencies

*Pin exact versions at install time; the list below is the recommended dependency set (verify latest stable when provisioning).*

```
Flask
Flask-Babel
Flask-WTF
WTForms
email-validator
Flask-Mail
Flask-SQLAlchemy
Flask-Migrate
Flask-Limiter
Flask-Compress
Flask-Talisman          # optional, recommended for prod
Flask-Caching           # optional
python-dotenv
Babel
gunicorn
whitenoise
psycopg2-binary         # Postgres driver (Render prod)
```

*(Werkzeug, Jinja2, itsdangerous, click install transitively with Flask.)*

---

## 20. Complete HTML Page List

| File | Route | Parent template | Purpose | Shared components used | SEO role |
|---|---|---|---|---|---|
| `pages/home.html` | `/<lang>/` | base.html | Positioning + proof + flagship + conversion hub | header, footer, whatsapp, trust_strip, section_opener, product_card, value_card, certifications_section, cta_band, buttons, structured_data | Primary SEO landing; Organization schema; brand + core keyword targets |
| `pages/about.html` | `/<lang>/about` | base.html | Honest company model, track record, values, compliance | section_opener, value_card, certifications_section, trust_strip, cta_band, buttons | Company/brand authority page |
| `pages/founder.html` | `/<lang>/founder` | base.html | Founder vision, family-business trust (photo only, no video) | section_opener, buttons, cta_band | Trust/E-E-A-T signal; Person schema (optional) |
| `pages/export_process.html` | `/<lang>/export-process` | base.html | Transparent sourcing→shipping process | section_opener, value_card, trust_strip, cta_band, buttons | Process/intent keywords; HowTo schema (optional) |
| `pages/markets.html` | `/<lang>/markets` | base.html | Gulf track record + target markets (sky-blue map visuals) | section_opener, trust_strip, cta_band, buttons | Geo/market keyword targets |
| `pages/import_partner.html` | `/<lang>/import-partner` | base.html | Long-term partnership; qualifying lead form | section_opener, forms macros, buttons, whatsapp | High-intent conversion page |
| `pages/export_inquiry.html` | `/<lang>/export-inquiry` | base.html | Primary lead capture (product pre-fill) | trust_strip, forms macros, buttons, whatsapp | Primary conversion page |
| `pages/contact.html` | `/<lang>/contact` | base.html | Verifiable identity + contact form + map | forms macros, buttons, whatsapp | LocalBusiness/contact schema |
| `pages/privacy.html` | `/<lang>/privacy` | base.html | Privacy policy | (minimal) | Legal/trust; noindex optional |
| `pages/terms.html` | `/<lang>/terms` | base.html | Terms | (minimal) | Legal/trust; noindex optional |
| `products/index.html` | `/<lang>/products` | base.html | Product range, banana flagship feature | section_opener, product_card, trust_strip, cta_band, buttons | Product hub; ItemList schema |
| `products/detail.html` | `/<lang>/products/<slug>` | base.html | Single template for banana/onion/coconut + future products | section_opener, trust_strip, forms CTA, buttons, whatsapp, structured_data | Per-product SEO; Product schema; deepest for banana |
| `insights/index.html` | `/<lang>/insights` | base.html | Blog listing (SEO engine) | section_opener, article_card, cta_band | Content hub; Blog schema |
| `insights/article.html` | `/<lang>/insights/<slug>` | base.html | Article template | section_opener, article_card (related), cta_band, structured_data | Long-tail SEO; Article schema |
| `forms/success.html` | (rendered after POST) | base.html | Submission confirmation + next steps | buttons, whatsapp | noindex |
| `errors/404.html` | (error handler) | base.html | Not found | buttons | noindex |
| `errors/500.html` | (error handler) | base.html | Server error | buttons | noindex |
| *(reserved)* `pages/services/*` | `/<lang>/services...` | base.html | Future sourcing/consulting | section_opener, value_card, cta_band | Added at launch only |

---

## 21. Render Deployment Architecture

- **Entrypoint:** `wsgi.py` exposing `app = create_app()`; served by **Gunicorn**.
- **`render.yaml`:** web service (Python), build command (install requirements, compile Babel catalogs, run migrations), start command (`gunicorn wsgi:app`), plus a **Postgres** instance for prod persistence.
- **Static:** served via WhiteNoise (compressed, cached) so Render needs no separate static host.
- **Config:** env-driven (`ProdConfig`) — `SECRET_KEY`, `DATABASE_URL`, mail credentials, allowed hosts; templated in `.env.example`.
- **HTTPS/security headers:** via Flask-Talisman (prod).
- Clean separation of dev (SQLite) vs prod (Postgres) keeps local builds simple and deployment reliable.

---

## 22. How the Architecture Satisfies the Future-Proofing Mandate

- **Future Arabic without restructuring** → locale-prefixed routes + externalized strings + logical-property CSS + `lang/dir` switch + reserved catalog/font/switcher.
- **Future products without redesign** → single `products/detail.html` driven by `data/products.py`; new product = data entry.
- **Future sourcing services without restructuring** → reserved `services` blueprint, registered at launch only.
- **Certification PDFs attached later** → registry with nullable `document`; cards auto-enable on attachment; PDFs drop into `static/docs/certifications/`.
- **Clean Render deployment** → app factory + Gunicorn + WhiteNoise + env config + render.yaml.
- **Proper inheritance / minimal duplication** → one base, shared partials, macro components, single nav/product/cert registries.

---

*End of Phase 3A. This architecture is the build contract for Phase 3B (HTML templates), Phase 3C (CSS/design-system implementation), and subsequent phases (JS, Flask logic, forms, analytics, deployment). No code has been generated; every later phase builds against the structure defined here.*
