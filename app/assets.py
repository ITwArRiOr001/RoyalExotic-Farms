"""
app/assets.py — Static asset resolution.

Data modules (products, articles, config) reference media by path. Templates must
never emit a request for a file that does not exist (a broken-image icon, or a
404 in the network log). `static_asset(path)` returns the path unchanged when the
file exists under the static folder, otherwise None, so every media slot can fall
back to the semantic "image unavailable" treatment in components/cards.html
instead of a misleading substitute photograph.

Registered as a Jinja global. Results are cached per path in production;
recomputed per call when TEMPLATES_AUTO_RELOAD / debug is on so newly added
assets appear without a restart.
"""
import os
from functools import lru_cache

from flask import current_app


@lru_cache(maxsize=512)
def _exists_cached(static_folder, path):
    return _exists(static_folder, path)


def _exists(static_folder, path):
    full = os.path.normpath(os.path.join(static_folder, path))
    # Refuse anything that resolves outside the static folder.
    if not full.startswith(os.path.normpath(static_folder) + os.sep):
        return False
    return os.path.isfile(full)


def static_asset(path):
    """Return `path` if it names an existing file under static/, else None."""
    if not path or not isinstance(path, str) or "://" in path:
        return None
    path = path.lstrip("/")
    folder = current_app.static_folder
    if current_app.debug or current_app.config.get("TEMPLATES_AUTO_RELOAD"):
        return path if _exists(folder, path) else None
    return path if _exists_cached(folder, path) else None


def init_app(app):
    app.jinja_env.globals["static_asset"] = static_asset
