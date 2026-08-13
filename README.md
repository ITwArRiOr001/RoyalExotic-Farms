# Royal Exotic Farms

Enterprise B2B export website — an India-based agricultural export & trading
company (bananas, onions, coconuts) serving Gulf importers. Flask + Jinja +
PostgreSQL, mobile-first, RTL-ready, first-party analytics, no third-party
trackers.

## Stack
Flask (app-factory + blueprints) · SQLAlchemy + Flask-Migrate · Flask-WTF ·
Flask-Babel (locale-prefixed routes, Arabic-ready) · Flask-Mail · gunicorn ·
vanilla JS (progressive enhancement) · token-based CSS design system.

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env                 # fill in values
flask --app wsgi db init             # first time only
flask --app wsgi db migrate -m "initial"
flask --app wsgi db upgrade
flask --app wsgi run --debug
```
Open http://localhost:5000/ → redirects to `/en/`.

## Documentation
- **README-DEPLOY.md** — run/deploy details + the two `base.html` wiring lines.
- **PRODUCTION-CHECKLIST.md** — pre/post-deploy, QA, launch validation.
- **SECURITY.md** — security posture + hardening roadmap.
- **MONITORING.md** — logging, error monitoring, backups, runbook.
- `Royal-Exotic-Farms-*.md` — design/architecture references (phases 1–3).

## Deploy (Render + GitHub)
Connect the repo to Render; `render.yaml` provisions Postgres + the web
service, runs `flask db upgrade` as a pre-deploy step, and starts
`gunicorn -c gunicorn.conf.py wsgi:app`. Commit `migrations/` before the first
deploy and set the `sync:false` secrets in the Render dashboard.

## Layout
```
app/           factory, blueprints, data registries, i18n, forms, models
templates/     Jinja (base, pages, partials, components) — frozen
static/        css/ (design system) + js/main.js + img/ video/ (assets)
content/       Markdown insights
translations/  Babel catalogs (Arabic later)
```
