# Production & Launch Checklist — Royal Exotic Farms

Companion to `README-DEPLOY.md`. Work top to bottom; nothing here changes the
application, it validates it.

## 1. Pre-deploy (must pass)
- [ ] `migrations/` generated **and committed** (see README warning). Without it, tables aren't created.
- [ ] `base.html` reserved blocks wired: `main.css` `<link>` + fonts, and `main.js` `<script defer>` (the two snippets in README-DEPLOY.md). This is the only template edit and it is expected.
- [ ] Secrets set in Render (all `sync:false`): `SITE_URL`, `ORG_EMAIL`, `ORG_PHONE`, `ORG_WHATSAPP`, `MAIL_*`, `SUBMISSION_NOTIFY_EMAIL`.
- [ ] `FLASK_ENV=production` (set in `render.yaml`) → `ProductionConfig` active (DEBUG off, secure cookies, CSP+HSTS on).
- [ ] `SECRET_KEY` present (Render `generateValue`), stable across deploys.
- [ ] Static assets added per the Image Replacement Map (logo, OG image, product/insight art, icons, favicon, hero video). Broken media otherwise.
- [ ] `pip install -r requirements.txt` succeeds on Python 3.12.

## 2. Deploy
- [ ] Push to the connected GitHub branch → Render builds.
- [ ] `preDeployCommand` (`flask db upgrade`) succeeds — a failure blocks promotion (intended).
- [ ] Service reaches healthy via `/robots.txt`.

## 3. Post-deploy smoke test (2 minutes)
- [ ] `https://<domain>/` → 302 to `/en/` → home renders styled.
- [ ] View source: `<link rel="canonical">` and `og:url` are **https** (ProxyFix working).
- [ ] `/en/products`, a product detail, `/en/markets`, `/en/insights`, an article, `/en/about`, `/en/contact` all 200.
- [ ] Submit each form (contact, export inquiry, import partner) with valid data → redirects to `/en/thank-you` → row appears in `submissions` → notification email received.
- [ ] Submit with the honeypot (`website`) filled → treated as success, **no** DB row (spam path).
- [ ] `/sitemap.xml` lists https URLs for pages + products + articles; `/robots.txt` references the sitemap.
- [ ] `/en/does-not-exist` → styled 404 with `noindex`.
- [ ] Response headers present: `Content-Security-Policy`, `Strict-Transport-Security`, `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `Cross-Origin-Opener-Policy`.

## 4. Accessibility QA (WCAG 2.1 AA)
- [ ] Keyboard-only: skip link, full tab order, visible gold focus ring everywhere, mobile dialog traps + restores focus, Escape closes dialog/dropdown.
- [ ] `prefers-reduced-motion`: reveals/hero/sweep/media-fade all resolve to resting state (content visible).
- [ ] Screen reader spot check: one landmark set, single `<h1>` per page, form labels + error summary announced.
- [ ] Forced-colors (Windows High Contrast): borders/focus visible, hero text legible.
- [ ] Contrast: body/heading/gold-on-green combinations pass AA (gold restricted to large/decorative).

## 5. Performance (Lighthouse 95+ target)
- [ ] Mobile Lighthouse ≥ 95 Perf / 100 A11y / 100 Best-Practices / ~100 SEO on home + an article.
- [ ] LCP image not lazy-faded (hero/featured excluded by design); no CLS from images (width/height present).
- [ ] Fonts `display=swap`; CSS in `<head>`, JS `defer`.
- [ ] Cache-Control on css/js/svg = 30 days.

## 6. Cross-browser / device
- [ ] Chrome, Safari (incl. iOS), Firefox, Edge — latest.
- [ ] 320 / 375 / 768 / 1024 / 1440 / 1920 — no overflow, no horizontal scroll.
- [ ] RTL sanity (set a test `ar` locale later) — layout mirrors via logical properties.

## 7. Go / No-Go
- [ ] All "must pass" items green. Any red in sections 1–3 = **No-Go**.

## Ongoing (first week)
- [ ] Watch Render logs for errors/timeouts.
- [ ] Confirm inbound inquiry emails are arriving and not spam-filtered (SPF/DKIM on sender domain).
- [ ] Review `submissions` for real leads; review `analytics_events` volume.
