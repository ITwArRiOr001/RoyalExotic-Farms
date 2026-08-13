"""
app/content.py — Insights Content Architecture.

Insights are authored as Markdown files with YAML front matter under
content/<locale>/insights/*.md. This loader parses front matter, renders the body
to HTML, and SANITISES it with a strict allow-list (bleach) before it reaches the
template's `article.body | safe`. Filenames are slugs.

Returned article dicts match the frozen template contract:
  slug, title, description, category, date, date_display, author, hero_image,
  thumbnail, image_alt, read_time, featured, body(html)
"""
import os
import datetime
import frontmatter
import markdown as md
import bleach

_CACHE = {}

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


def _load_dir(base_path, locale):
    directory = _dir(base_path, locale)
    articles = []
    if not os.path.isdir(directory):
        return articles
    for fname in os.listdir(directory):
        if not fname.endswith(".md"):
            continue
        slug = os.path.splitext(fname)[0]
        post = frontmatter.load(os.path.join(directory, fname))
        meta = post.metadata or {}
        raw_date = meta.get("date")
        articles.append({
            "slug": slug,
            "title": meta.get("title", slug.replace("-", " ").title()),
            "description": meta.get("description"),
            "category": meta.get("category"),
            "date": str(raw_date) if raw_date else None,
            "date_display": _fmt_date(raw_date),
            "author": meta.get("author"),
            "hero_image": meta.get("hero_image"),
            "thumbnail": meta.get("thumbnail"),
            "image_alt": meta.get("image_alt"),
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
