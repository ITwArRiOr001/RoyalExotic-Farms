# Monitoring, Logging & Backups — Royal Exotic Farms

## Logging (in place)
- App logs at INFO in production (`_init_logging`); email-send failures are logged with stack traces but never block a submission.
- Gunicorn access + error logs stream to stdout/stderr (`gunicorn.conf.py`) → captured by Render's log viewer.
- Sufficient for launch. For searchable/retained logs, forward Render logs to a drain (e.g. Logtail/Datadog).

## Error monitoring (recommended)
Add Sentry for captured exceptions with request context. Minimal, additive — no
architecture change:
```
# requirements.txt:  sentry-sdk[flask]
# app/__init__.py, top of create_app(), before returning app:
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
dsn = os.environ.get("SENTRY_DSN")
if dsn and not app.debug:
    sentry_sdk.init(dsn=dsn, integrations=[FlaskIntegration()],
                    traces_sample_rate=0.1, send_default_pii=False)
```
Set `SENTRY_DSN` in Render. `send_default_pii=False` keeps submitter data out of traces.

## Uptime & health
- Render health check hits `/robots.txt` (no DB, always 200).
- Add an external uptime monitor (UptimeRobot/BetterStack) on `/` and `/en/` for independent alerting.

## Business signal monitoring
- **Leads:** `submissions` table is the source of truth. Verify the notification email path weekly; the DB row is the fallback if email fails.
- **Engagement:** `analytics_events` (pageview/form_start/form_success/click/outbound) is dashboard-ready. Build a simple internal dashboard later (out of scope for launch).

## Database backups
- **Render Postgres (starter):** automated daily backups are included; confirm retention in the dashboard and test a restore once before launch.
- For point-in-time recovery and longer retention, upgrade the Postgres plan.
- Before risky migrations, take a manual snapshot.

## Operational runbook (quick)
- **500s spike:** check Render logs / Sentry; `errors.py` already rolls back the DB session on 500.
- **DB connection errors:** `pool_pre_ping` + `pool_recycle=280` handle dropped idle connections; if persistent, check Postgres connection limits vs `WEB_CONCURRENCY`.
- **Emails not arriving:** verify `MAIL_*` secrets, `MAIL_SUPPRESS_SEND=false`, and sender-domain SPF/DKIM; leads are still safe in `submissions`.
- **`/track` flooding:** apply the rate-limit plan in `SECURITY.md`.
