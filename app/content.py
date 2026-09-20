"""
app/content.py — Insights Content Architecture.

Insights are authored as Markdown files with YAML front matter under
content/<locale>/insights/*.md. This loader parses front matter, renders the body
to HTML, and SANITISES it with a strict allow-list (bleach) before it reaches the
template's `article.body | safe`. Filenames are slugs.

Returned article dicts match the frozen template contract:
  slug, title, description, category, date, date_display, author, hero_image,
  thumbnail, image_alt, image_caption, read_time, featured, body(html)

PUBLISHING GATE — a Markdown file becomes a public article (index card, route,
sitemap entry) only if ALL of these hold; otherwise it is skipped and logged:
  - the filename (= URL slug) is lowercase kebab-case: ^[a-z0-9]+(-[a-z0-9]+)*$
  - the front matter parses
  - `title` is a non-empty string
  - `date` is a valid calendar date (YAML date or ISO "YYYY-MM-DD")
  - the Markdown body is non-empty
This stops an accidental empty/stray file (e.g. a stray "DFS.md") from creating a
broken public article. Media paths are NOT validated here; templates resolve
them via static_asset() and fall back safely (app/assets.py).
"""
import os
import re
import logging
import datetime
import frontmatter
import markdown as md
import bleach

log = logging.getLogger(__name__)

_CACHE = {}

_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

_ALLOWED_TAGS = list(bleach.sanitizer.ALLOWED_TAGS) + [
    "p", "h2", "h3", "h4", "pre", "hr", "br", "img", "figure", "figcaption",
    "blockquote", "ul", "ol", "li", "strong", "em", "table", "thead", "tbody",
    "tr", "th", "td", "span",
]
_ALLOWED_ATTRS = {
    "a": ["href", "title", "rel"],
    "img": ["src", "alt", "width", "height", "loading", "decoding"],
    "th": ["scope"],
    "span": ["class"],
}


def _dir(base_path, locale):
    return os.path.join(base_path, "content", locale, "insights")


def _fmt_date(value):
    if isinstance(value, (datetime.date, datetime.datetime)):
        return value.strftime("%d %b %Y")
    return str(value) if value else ""


def _render_body(text):
    html = md.markdown(text or "", extensions=["extra", "sane_lists", "smarty"])
    return bleach.clean(html, tags=_ALLOWED_TAGS, attributes=_ALLOWED_ATTRS, strip=True)


def _parse_date(value):
    """Return a datetime.date for a YAML date/datetime or ISO string, else None."""
    if isinstance(value, datetime.datetime):
        return value.date()
    if isinstance(value, datetime.date):
        return value
    if isinstance(value, str):
        try:
            return datetime.date.fromisoformat(value.strip())
        except ValueError:
            return None
    return None


def _validate(fname, slug, meta, body):
    """Return a list of reasons this file is NOT publishable (empty = valid)."""
    problems = []
    if not _SLUG_RE.match(slug):
        problems.append("filename is not a lowercase kebab-case slug")
    title = meta.get("title")
    if not isinstance(title, str) or not title.strip():
        problems.append("missing or empty 'title'")
    if _parse_date(meta.get("date")) is None:
        problems.append("missing or invalid 'date'")
    if not (body or "").strip():
        problems.append("empty body")
    return problems


def _load_dir(base_path, locale):
    directory = _dir(base_path, locale)
    articles = []
    if not os.path.isdir(directory):
        return articles
    for fname in sorted(os.listdir(directory)):
        if not fname.endswith(".md"):
            continue
        slug = os.path.splitext(fname)[0]
        path = os.path.join(directory, fname)
        try:
            post = frontmatter.load(path)
        except Exception as exc:  # malformed YAML / unreadable file
            log.warning("insights: skipped %s/%s — front matter could not be parsed (%s)",
                        locale, fname, exc)
            continue
        meta = post.metadata or {}
        problems = _validate(fname, slug, meta, post.content)
        if problems:
            log.warning("insights: skipped %s/%s — not publishable: %s",
                        locale, fname, "; ".join(problems))
            continue
        raw_date = _parse_date(meta.get("date"))
        articles.append({
            "slug": slug,
            "title": meta["title"].strip(),
            "description": meta.get("description"),
            "category": meta.get("category"),
            "date": raw_date.isoformat(),
            "date_display": _fmt_date(raw_date),
            "author": meta.get("author"),
            "hero_image": meta.get("hero_image"),
            "thumbnail": meta.get("thumbnail"),
            "image_alt": meta.get("image_alt"),
            # [P0A] Optional one-line caption (e.g. "Illustrative image").
            "image_caption": meta.get("image_caption"),
            "read_time": meta.get("read_time"),
            "featured": bool(meta.get("featured", False)),
            "body": _render_body(post.content),
        })
    articles.sort(key=lambda a: a["date"] or "", reverse=True)
    return articles


def all_articles(base_path, locale, use_cache=True):
    key = ("articles", locale)
    if use_cache and key in _CACHE:
        return _CACHE[key]
    data = _load_dir(base_path, locale)
    if use_cache:
        _CACHE[key] = data
    return data


def get_article(base_path, locale, slug, use_cache=True):
    for a in all_articles(base_path, locale, use_cache):
        if a["slug"] == slug:
            return a
    return None


def related_articles(base_path, locale, article, limit=3, use_cache=True):
    if not article:
        return []
    out = [a for a in all_articles(base_path, locale, use_cache)
           if a["slug"] != article["slug"] and a.get("category") == article.get("category")]
    return out[:limit]


def categories(base_path, locale, use_cache=True):
    seen, out = set(), []
    for a in all_articles(base_path, locale, use_cache):
        c = a.get("category")
        if c and c not in seen:
            seen.add(c)
            out.append({"slug": c.lower().replace(" ", "-"), "label": c})
    return out


def clear_cache():
    _CACHE.clear()
