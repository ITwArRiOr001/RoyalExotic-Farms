"""
app/seo.py — SEO Data Architecture.

make_seo() builds the per-page `seo` object the frozen head_seo.html partial
consumes: title, description, canonical, og_image, og_type, robots. Canonical
defaults to the current request URL; og_image falls back to config.DEFAULT_OG_IMAGE
inside the template. Returned as a plain dict (Jinja attribute access works and
`is defined` stays truthy for present-but-None keys).
"""
from flask import request


def make_seo(title=None, description=None, canonical=None,
             og_image=None, og_type="website", robots="index, follow"):
    return {
        "title": title,
        "description": description,
        "canonical": canonical or request.url,
        "og_image": og_image,
        "og_type": og_type,
        "robots": robots,
    }


def noindex_seo(title=None, description=None):
    return make_seo(title=title, description=description, robots="noindex, nofollow")
