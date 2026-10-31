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

# links carry an explicit kind; the call to action follows from the kinds present, never from a URL's domain
KINDS = {"demo", "download", "source", "external"}
cta = {}
for lang in ("content.json", "content.en.json"):
    for p in json.loads((ROOT / "data" / lang).read_text(encoding="utf-8"))["projects"]:
        kinds = {l["kind"] for l in p["links"]}
        if not kinds <= KINDS:
            errors.append(f"{p['slug']}: unknown link kind {kinds - KINDS}")
        derived = "try" if "demo" in kinds else "download" if "download" in kinds else "follow"
        got = (p.get("cta", derived), sorted(kinds))
        if got[0] == "try" and "demo" not in kinds or got[0] == "download" and "download" not in kinds:
            errors.append(f"{p['slug']}: cta '{got[0]}' needs a link of that kind")
        if cta.setdefault(p["slug"], got) != got:
            errors.append(f"{p['slug']}: cta or link kinds differ between zh and en")

for f in ("sitemap.xml", "404.html", "robots.txt"):
    if not (ROOT / f).exists():
        errors.append(f"missing {f}")

if errors:
    print("\n".join(errors))
    sys.exit(f"{len(errors)} problem(s)")
print(f"ok: {len(zh)} zh + {len(en)} en pages, links and assets resolve")
