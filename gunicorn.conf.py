"""
gunicorn.conf.py — production WSGI server configuration.

Run with:  gunicorn -c gunicorn.conf.py wsgi:app

Why this file exists (Phase 5 audit):
  * BINDS TO $PORT — Render assigns the port via $PORT and routes to it. The
    previous inline command used gunicorn's default (:8000) and would fail
    Render's health check. This is the one change required for the app to
    receive traffic at all.
  * worker_tmp_dir=/dev/shm — Render's container disk can stall gunicorn's
    heartbeat file and trigger spurious worker timeouts; /dev/shm is in-memory.
  * max_requests (+jitter) — recycles workers periodically to bound memory
    growth from any long-running process leaks.
  * forwarded_allow_ips="*" — trust the platform proxy for X-Forwarded-* (works
    with the ProxyFix middleware in the app factory).
  * access/error logs to stdout/stderr — captured by Render's log stream.
"""
import multiprocessing
import os

# Networking — Render provides $PORT.
bind = "0.0.0.0:" + os.environ.get("PORT", "10000")

# Concurrency — WEB_CONCURRENCY lets you tune per plan without code changes.
# Default is conservative for the starter plan's memory budget.
workers = int(os.environ.get("WEB_CONCURRENCY", "3"))
threads = int(os.environ.get("GUNICORN_THREADS", "1"))
worker_class = os.environ.get("GUNICORN_WORKER_CLASS", "sync")

# Reliability
timeout = int(os.environ.get("GUNICORN_TIMEOUT", "60"))
graceful_timeout = 30
keepalive = 5
worker_tmp_dir = "/dev/shm"

# Recycle workers to bound memory usage over time.
max_requests = int(os.environ.get("GUNICORN_MAX_REQUESTS", "1000"))
max_requests_jitter = int(os.environ.get("GUNICORN_MAX_REQUESTS_JITTER", "100"))

# Proxy / logging
forwarded_allow_ips = "*"
accesslog = "-"
errorlog = "-"
loglevel = os.environ.get("GUNICORN_LOG_LEVEL", "info")

# Do not enable preload_app with the current lazy DB engine unless a post_fork
# pool dispose is added; keeping it off avoids any fork/connection sharing risk.
preload_app = False
