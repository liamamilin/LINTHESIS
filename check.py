#!/usr/bin/env python3
"""Basic checks on the generated site: zh/en parity, internal links, asset paths.
Run after build.py: python3 check.py"""
import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).parent
SKIP = {"_work", "docs", ".git"}
errors = []


class Refs(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for k in ("href", "src", "poster"):
            if a.get(k):
                self.refs.append(a[k])


def pages(base):
    return sorted(p for p in base.rglob("index.html") if not SKIP & set(p.relative_to(ROOT).parts))


zh = {p.relative_to(ROOT) for p in pages(ROOT) if p.relative_to(ROOT).parts[0] != "en"}
en = {Path(*p.relative_to(ROOT / "en").parts) for p in pages(ROOT / "en")}
for miss in sorted(zh ^ en):
    errors.append(f"zh/en page mismatch: {miss}")

for page in pages(ROOT):
    p = Refs()
    p.feed(page.read_text(encoding="utf-8"))
    for ref in p.refs:
        u = urlparse(ref)
        if u.scheme or ref.startswith(("#", "mailto:")):
            continue
        target = (page.parent / unquote(u.path)).resolve()
        if target.is_dir():
            target /= "index.html"
        if not target.exists():
            errors.append(f"{page.relative_to(ROOT)}: broken ref {ref}")

# a project's call to action must be backed by a real link, never inferred from its status
cta = {}
for lang in ("content.json", "content.en.json"):
    for p in json.loads((ROOT / "data" / lang).read_text(encoding="utf-8"))["projects"]:
        hosts = [urlparse(u) for _, u in p["links"]]
        if p["cta"] == "try" and not any(h.netloc != "github.com" for h in hosts):
            errors.append(f"{p['slug']}: cta 'try' needs a live link, only has GitHub")
        if p["cta"] == "download" and not any("/releases" in h.path or h.path.endswith((".dmg", ".zip", ".pkg")) for h in hosts):
            errors.append(f"{p['slug']}: cta 'download' needs a release or installer link")
        if cta.setdefault(p["slug"], p["cta"]) != p["cta"]:
            errors.append(f"{p['slug']}: cta differs between zh and en")

for f in ("sitemap.xml", "404.html", "robots.txt"):
    if not (ROOT / f).exists():
        errors.append(f"missing {f}")

if errors:
    print("\n".join(errors))
    sys.exit(f"{len(errors)} problem(s)")
print(f"ok: {len(zh)} zh + {len(en)} en pages, links and assets resolve")
