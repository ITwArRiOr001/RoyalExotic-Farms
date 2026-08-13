# Royal Exotic Farms — Run & Deploy

## Project layout
```
├── app/                    # application package (factory, blueprints, data, i18n)
│   ├── __init__.py         # create_app()
│   ├── config.py extensions.py i18n.py seo.py context_processors.py errors.py
│   ├── models.py forms.py emails.py content.py
│   ├── blueprints/         # main, products, insights, forms, analytics, seo_bp
│   └── data/               # organization, navigation, contact_actions, products, markets, certifications
├── templates/              # FROZEN Jinja templates (Phases 1–3)
├── static/                 # css/ (Phase 3C) + js/main.js (Phase 4A) + img/ video/ (assets pending)
├── content/en/insights/    # Markdown articles
├── translations/           # Babel catalogs (Arabic later)
├── wsgi.py requirements.txt babel.cfg render.yaml .env.example
```

## Local development
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env            # edit values
flask --app wsgi db init        # first time only
flask --app wsgi db migrate -m "initial"
flask --app wsgi db upgrade
flask --app wsgi run --debug
```
Visit http://localhost:5000/ → redirects to /en/.

## Two wiring lines (paste into the reserved blocks in templates/base.html)
The foundation reserved these two empty blocks for exactly this phase. Filling
them is the only edit required to activate styles + interactions:

```jinja
{% block stylesheets %}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" as="style"
        href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,600&display=swap">
  <link rel="stylesheet"
        href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,600&display=swap">
  <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
{% endblock %}

{% block scripts %}
  <script defer src="{{ url_for('static', filename='js/main.js') }}"></script>
{% endblock %}
```
(`display=swap` = fast first paint; `defer` keeps JS off the critical path.)

## Assets still to add (Image Replacement Map)
The app runs now, but media shows as broken/placeholder until these are added
under `static/`:
- `img/brand/logo.svg`, `img/brand/logo-light.svg`, `img/brand/og-default.jpg`
- `img/products/*.svg`, `img/insights/*.svg`, `img/founder/*`, `img/markets/*`
- `img/icons/*.svg` (whatsapp, email, leaf, …), `favicon/*`, `video/hero/*`
- `docs/certifications/*.pdf` + `img/certifications/*` (only once certs are verified)

## Deploy (Render)
`render.yaml` provisions Postgres + the web service. It runs `flask db upgrade`
as a **preDeployCommand** (once per release, before promotion) and starts
`gunicorn -c gunicorn.conf.py wsgi:app` (binds to `$PORT`). Health check:
`/robots.txt`. Set the `sync:false` secrets in the dashboard.

> **Critical:** commit the generated `migrations/` folder to the repo before the
> first deploy. `db upgrade` only applies migrations that exist in the repo — if
> `migrations/` is missing, no tables are created and the app errors on first
> query. Generate locally once: `flask --app wsgi db init && flask --app wsgi db
> migrate -m "initial" && flask --app wsgi db upgrade`, then commit.

Optional env overrides: `WEB_CONCURRENCY` (worker count), `HSTS_SECONDS`,
`CONTENT_SECURITY_POLICY`, `SEND_ACK_EMAIL`.
```

## Notes
- Certifications default to an empty list (honest). Populate `app/data/certifications.py` only after each credential is verified.
- Analytics events are stored first-party in `analytics_events` (dashboard-ready); no third-party tracker.
- Arabic is configuration-only later: add `ar` to `SUPPORTED_LOCALES` + provide the catalog.
