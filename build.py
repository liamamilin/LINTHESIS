#!/usr/bin/env python3
"""Generate the static site (zh at root, en under /en/) from data/content*.json.
Run: python3 build.py"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).parent
SITE_URL = "https://liamamilin.github.io/LINTHESIS/"
URLS = []
e = html.escape

UI = json.loads((ROOT / "data" / "ui.json").read_text(encoding="utf-8"))
NAV = [("works", "Works", "作品"), ("books", "Books", "书籍"), ("writing", "Writing", "文章"),
       ("lab", "Lab", "实验室"), ("about", "About", "关于")]

# set by build(lang)
C = S = T = None
LANG = "zh"
OFF = 0  # 1 when output lives under en/


def abase(depth):
    return "../" * (depth + OFF)


def lbase(depth):
    return "../" * depth


def page(path, title, body, depth, active="", desc=""):
    ab, lb = abase(depth), lbase(depth)
    cur = ' aria-current="page"'
    nav = "".join(
        f'<a href="{lb}{k}/"{cur if k == active else ""}>{en}' + (f' <span lang="zh">{zh}</span>' if T["nav_both"] else "") + "</a>"
        for k, en, zh in NAV)
    zh_tag = f' {S["tagline_zh"]}' if S["tagline_zh"] else ""
    desc = desc or f'{S["tagline_en"]}{zh_tag} {S["intro"]}'
    # language switch target: same page in the other language
    d = path[: -len("index.html")]
    if LANG == "zh":
        alt, alt_lang = f'{lb}en/{d}', "en"
    else:
        alt, alt_lang = f'{abase(depth)}{d}', "zh-CN"
    canon = f'{SITE_URL}{"en/" if LANG == "en" else ""}{d}'
    URLS.append((canon, f'{SITE_URL}{"" if LANG == "en" else "en/"}{d}'))
    doc = f"""<!doctype html>
<html lang="{T["html_lang"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="{alt_lang}" href="{alt}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="LINTHESIS">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE_URL}img/social-card.png">
<meta property="og:locale" content="{"en_US" if LANG == "en" else "zh_CN"}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{ab}brand/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{ab}css/brand.css">
<link rel="stylesheet" href="{ab}css/site.css">
</head>
<body>
<div class="wrap">
<header class="top">
<a class="logo" href="{lb}" aria-label="{T["home_label"]}"><img src="{ab}brand/linthesis-structure-horizontal.svg" alt="LINTHESIS"></a>
<nav aria-label="{T["nav_label"]}">{nav}</nav>
<a class="ext lang" href="{alt}" hreflang="{alt_lang}" lang="{alt_lang}" aria-label="{T["switch_label"]}">{T["switch"]}</a>
<a class="ext gh" href="{S["github"]}">GitHub ↗</a>
</header>
<main>
{body}
</main>
<footer>
<img src="{ab}brand/linthesis-structure-symbol.svg" alt="">
<span>{S["author"]} · {T["footer_extra"]}</span>
<a href="mailto:{S["email"]}">{S["email"]}</a>
<span class="sp">{S["tagline_en"]}{zh_tag}</span>
</footer>
</div>
</body>
</html>
"""
    out = ROOT / ("en" if LANG == "en" else "") / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")


def tile(img, kind="shot"):
    if kind == "book":
        cls = "tile book png" if img.endswith(".png") else "tile book"
        return f'<div class="{cls}"><img src="{{a}}{img}" alt="" loading="lazy"></div>'
    return f'<div class="tile"><img src="{{a}}{img}" alt="" loading="lazy"></div>'


def card(href, img, title, meta, kind="shot"):
    return (f'<a class="card" href="{href}">{tile(img, kind)}'
            f'<div class="cap"><b>{e(title)}</b><span>{e(meta)}</span></div></a>')


def sec(n, title, link=None, text=None):
    a = f'<a href="{link}">{text or T["view_all"]}</a>' if link else ""
    return f'<div class="sec-h"><span class="n">{n}</span><h2>{title}</h2>{a}</div>'


def fill(s, depth):
    return s.replace("{a}", abase(depth))


def bt(t):
    return T["title_book"].format(t=t)


def project_cards(depth):
    lb = lbase(depth)
    return "".join(
        card(f'{lb}works/{p["slug"]}/', p["cover"], f'{p["title"]} · {p["sub"]}', f'{p["kind"]} · {p["status"]}')
        for p in C["projects"])


def book_cards(depth, ebooks=True):
    lb = lbase(depth)
    out = ""
    for b in C["print_books"]:
        out += card(f'{lb}books/{b["slug"]}/', b["cover"], bt(b["title"]), f'{b["publisher"]} · {b["year"]}', "book")
    for b in C["ebooks"] if ebooks else []:
        out += card(f'{lb}books/{b["slug"]}/', b["cover"], bt(b["title"]), f'{T["online"]} · {b["status"]}')
    return out


def series_html(compact=False):
    if compact:
        return '<div class="series compact">' + "".join(
            f'<a href="writing/"><b>{e(s["name"])}</b><span>{T["series_count"].format(n=len(s["items"]))}</span></a>'
            for s in C["series"]) + "</div>"
    cols = ""
    for s in C["series"]:
        lis = "".join(f'<li><a href="{u}">{e(n)}</a></li>' for n, u in s["items"])
        cols += f'<div><h3>{e(s["name"])}</h3><ul>{lis}</ul></div>'
    return f'<div class="series">{cols}</div>'


def lab_rows(limit=None):
    return '<div class="rows lab">' + "".join(
        f'<a href="{u}"><div><b>{e(n)}</b><em>{e(d)}</em></div><span>GitHub ↗</span></a>' for n, u, d in C["lab"][:limit]) + "</div>"


def music_grid(ab):
    return '<div class="music">' + "".join(
        f'<figure><video controls playsinline preload="none" poster="{ab}img/music/{k}.jpg" src="{ab}video/music/{k}.mp4"></video>'
        f'<figcaption>{e(t)}</figcaption></figure>' for k, t in C["music"]) + "</div>"


def video_block(item, ab):
    return (f'<h2>{T["s_demo"]}</h2><div class="shots"><figure><video controls muted playsinline preload="metadata" '
            f'poster="{ab}{item["poster"]}" src="{ab}{item["video"]}"></video></figure></div>')


def meta_rows(rows):
    return "".join(f"<div><dt>{k}</dt><dd>{e(v)}</dd></div>" for k, v in rows)


def project(slug):
    return next(p for p in C["projects"] if p["slug"] == slug)


def home_works():
    """Selected work: one lead project, two secondary, the rest as a text list."""
    h = C["home"]
    lead, second = project(h["lead"]), [project(s) for s in h["secondary"]]
    rest = [p for p in C["projects"] if p["slug"] not in [h["lead"], *h["secondary"]]]
    nums = "".join(f'<div><b>{e(n)}</b><span>{e(t)}</span></div>' for n, t in lead.get("feature", {}).get("numbers", []))
    lead_html = (f'<a class="lead-card" href="works/{lead["slug"]}/"><div class="lead-shot"><img src="{abase(0)}{lead["cover"]}" alt="{e(lead["title"])}"></div>'
                 f'<div class="lead-info"><div><p class="kicker">{e(lead["kind"])} · {e(lead["status"])}</p><h3>{e(lead["title"])}<span>{e(lead["sub"])}</span></h3></div>'
                 f'<p>{e(lead["one_liner"])}</p><div class="nums">{nums}</div><span class="go">{T["open_project"]}</span></div></a>')
    sec_html = "".join(
        f'<a class="card wide" href="works/{p["slug"]}/"><div class="tile"><img src="{abase(0)}{p["cover"]}" alt="" loading="lazy"></div>'
        f'<div class="cap"><b>{e(p["title"])} · {e(p["sub"])}</b><span>{e(p["kind"])} · {e(p["status"])}</span><em>{e(p["one_liner"])}</em></div></a>'
        for p in second)
    more = " · ".join(f'<a href="works/{p["slug"]}/">{e(p["title"])}</a>' for p in rest)
    return (f'<section class="block roomy">{sec("01", T["h_selected"], "works/", T["all_works"])}{lead_html}'
            f'<div class="grid two">{sec_html}</div>'
            f'<p class="more"><span>{T["more_works"]}</span> {more} <a class="all" href="works/">{T["all_works"]}</a></p></section>')


def feature_detail(p, ab):
    """Editorial layout for projects that carry a `feature` block in the JSON."""
    f = p["feature"]
    btns = "".join(f'<a class="btn{" primary" if i == 0 else ""}" href="{u}">{e(n)} ↗</a>' for i, (n, u) in enumerate(p["links"]))
    meta = "".join(f"<div><dt>{k}</dt><dd>{e(v)}</dd></div>" for k, v in
                   [(T["k_status"], p["status"]), (T["k_platform"], p["platform"]), (T["k_tech"], p["tech"])])
    nums = "".join(f'<div><b>{e(n)}</b><span>{e(t)}</span></div>' for n, t in f["numbers"])
    walk = "".join(
        f'<figure class="step"><div class="step-img"><img src="{ab}{img}" alt="{e(p["title"])} · {e(name)}" loading="lazy"></div>'
        f'<figcaption><span class="n">{i:02d}</span><h3>{e(name)}</h3><p>{e(text)}</p><em>{e(cap)}</em></figcaption></figure>'
        for i, (img, name, text, cap) in enumerate(f["walk"], 1))
    use = "".join(f"<li>{e(x)}</li>" for x in f["use"])
    tech = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in f["tech"])
    video = (f'<div class="demo"><video controls muted playsinline preload="none" poster="{ab}{p["poster"]}" src="{ab}{p["video"]}"></video></div>'
             if p.get("video") else "")
    return f"""<article class="feature">
<header class="f-head"><nav class="crumbs" aria-label="breadcrumb"><a href="../">{T["h_works_short"]}</a> / <span>{e(p["title"])}</span></nav>
<p class="kicker">{e(p["kind"])}</p><h1>{e(p["title"])}</h1><p class="zh">{e(p["sub"])}</p>
<p class="one">{e(p["one_liner"])}</p><div class="btns">{btns}</div></header>
{video}
<div class="nums wide">{nums}</div>
<section class="f-sec"><h2>{T["f_what"]}</h2><div><p>{e(p["intro"])}</p></div></section>
<section class="f-sec"><h2>{T["f_problem"]}</h2><div><p>{e(f["problem"])}</p></div></section>
<section class="f-sec steps"><h2>{T["f_see"]}</h2><div class="walk">{walk}</div></section>
<section class="f-sec"><h2>{T["f_use"]}</h2><div><ul class="plain">{use}</ul></div></section>
<section class="f-sec"><h2>{T["f_tech"]}</h2><div><dl class="tech">{tech}</dl><dl class="meta">{meta}</dl></div></section>
<section class="f-cta"><h2>{T["f_cta"]}</h2><div class="btns">{btns}</div></section>
</article>"""


def generate():
    tl = S["tagline_zh"]
    zh_p = f'<p class="zh">{tl}</p>' if tl else ""
    stage = "".join(f"<span>{'<i></i>' if i == 0 else ''}{e(s)}</span>" for i, s in enumerate(T["hero_stage"]))
    ctas = "".join(f'<a class="btn{" primary" if i == 0 else ""}" href="{h}">{e(t)}</a>' for i, (h, t) in enumerate(T["hero_cta"]))
    home = f"""
<section class="hero">
<div class="stage">{stage}</div>
<h1>{S["tagline_en"]}</h1>
{zh_p}
<div class="hero-foot"><p class="lead">{S["intro"]}</p><div class="btns">{ctas}</div></div>
</section>
{home_works()}
<section class="block roomy">{sec("02", T["h_books"], "books/")}
<div class="grid four">{book_cards(0, ebooks=False)}</div>
<p class="more"><a href="books/">{T["books_count"].format(n=len(C["ebooks"]))}</a></p></section>
<section class="block roomy">{sec("03", T["h_writing"], "writing/")}
{series_html(compact=True)}</section>
<section class="block roomy">{sec("04", T["h_lab"], "lab/")}
{lab_rows(C["home"]["lab_count"])}</section>
"""
    page("index.html", f'{S["name"]} — {S["tagline_en"]}', fill(home, 0), 0)

    body = f"""<div class="page-h"><h1>{T["works_h"]}</h1><p>{T["works_p"]}</p></div>
<section class="block"><div class="grid">{project_cards(1)}</div></section>"""
    page("works/index.html", f"{T['works_h']} — {S['title_suffix']}", fill(body, 1), 1, "works")

    for p in C["projects"]:
        ab = abase(2)
        if p.get("feature"):
            page(f"works/{p['slug']}/index.html", f"{p['title']} — {S['title_suffix']}", feature_detail(p, ab), 2, "works", p["one_liner"])
            continue
        meta = meta_rows([(T["k_status"], p["status"]), (T["k_platform"], p["platform"]), (T["k_tech"], p["tech"])])
        btns = "".join(f'<a class="btn{" primary" if i == 0 else ""}" href="{u}">{e(n)} ↗</a>' for i, (n, u) in enumerate(p["links"]))
        feats = "".join(f"<li>{e(f)}</li>" for f in p["features"])
        note = f'<h2>{T["s_note"]}</h2><p class="note">{e(p["note"])}</p>' if p.get("note") else ""
        shots = "".join(f'<figure><img src="{ab}{g}" alt="{e(p["title"])} {T["shot_alt"]}" loading="lazy"></figure>' for g in p["gallery"])
        demo = video_block(p, ab) if p.get("video") else ""
        body = f"""<article class="detail">
<aside><nav class="crumbs" aria-label="breadcrumb"><a href="../">{T["h_works_short"]}</a> / <span>{e(p["title"])}</span></nav><p class="kicker">{e(p["kind"])}</p><h1>{e(p["title"])}</h1><p class="zh">{e(p["sub"])}</p>
<dl class="meta">{meta}</dl><div class="btns">{btns}</div></aside>
<div class="body"><p class="one">{e(p["one_liner"])}</p>
<h2>{T["s_intro"]}</h2><p>{e(p["intro"])}</p>
<h2>{T["s_feat"]}</h2><ul>{feats}</ul>{note}
{demo}<h2>{T["s_shots"]}</h2><div class="shots">{shots}</div></div></article>"""
        page(f"works/{p['slug']}/index.html", f"{p['title']} — {S['title_suffix']}", body, 2, "works", p["one_liner"])

    pb = "".join(card(f'{b["slug"]}/', b["cover"], bt(b["title"]), f'{b["publisher"]} · {b["year"]}', "book") for b in C["print_books"])
    eb = "".join(card(f'{b["slug"]}/', b["cover"], bt(b["title"]), b["status"]) for b in C["ebooks"])
    body = f"""<div class="page-h"><h1>{T["books_h"]}</h1><p>{T["books_p"]}</p></div>
<section class="block">{sec("01", T["books_pub"])}<div class="grid four">{pb}</div></section>
<section class="block">{sec("02", T["books_online"], "../writing/", T["books_more"])}<div class="grid">{eb}</div></section>"""
    page("books/index.html", f"{T['books_h']} — {S['title_suffix']}", fill(body, 1), 1, "books")

    for b in C["print_books"]:
        ab = abase(2)
        rows = [(T["k_author"], T["v_author"]), (T["k_pub"], b["publisher"]), (T["k_year"], str(b["year"]))]
        if b["isbn"]:
            rows.append((T["k_isbn"], b["isbn"]))
        rows.append((T["k_lang"], T["v_lang"]))
        png = " png" if b["cover"].endswith(".png") else ""
        sub = f'<p class="zh">{e(b["sub"])}</p>' if b.get("sub") else ""
        body = f"""<article class="detail">
<aside><nav class="crumbs" aria-label="breadcrumb"><a href="../">{T["h_books_short"]}</a> / <span>{e(bt(b["title"]))}</span></nav><div class="cover-big{png}"><img src="{ab}{b["cover"]}" alt="{e(bt(b["title"]))} {T["cover_alt"]}"></div>
<dl class="meta">{meta_rows(rows)}</dl><div class="btns"><a class="btn primary" href="{b["link"]}">{T["b_pub"]}</a></div></aside>
<div class="body"><p class="kicker">{T["kick_book"]}</p><h1>{e(b["title"])}</h1>{sub}
<h2>{T["s_blurb"]}</h2><p>{e(b["intro"])}</p></div></article>"""
        page(f"books/{b['slug']}/index.html", f"{bt(b['title'])} — {S['title_suffix']}", body, 2, "books", b["intro"])

    for b in C["ebooks"]:
        ab = abase(2)
        rows = [(T["k_format"], T["v_format"]), (T["k_status"], b["status"]), (T["k_lang"], T["v_lang"])]
        body = f"""<article class="detail">
<aside><nav class="crumbs" aria-label="breadcrumb"><a href="../">{T["h_books_short"]}</a> / <span>{e(b["title"])}</span></nav><p class="kicker">{T["kick_guide"]}</p><h1>{e(b["title"])}</h1><p class="zh">{e(b["sub"])}</p>
<dl class="meta">{meta_rows(rows)}</dl><div class="btns"><a class="btn primary" href="{b["link"]}">{T["b_read"]}</a></div></aside>
<div class="body"><h2>{T["s_blurb"]}</h2><p>{e(b["intro"])}</p>
{video_block(b, ab)}<h2>{T["s_home"]}</h2><div class="shots"><figure><img src="{ab}{b["cover"]}" alt="{e(b["title"])} {T["home_alt"]}" loading="lazy"></figure></div></div></article>"""
        page(f"books/{b['slug']}/index.html", f"{b['title']} — {S['title_suffix']}", body, 2, "books", b["intro"])

    body = f"""<div class="page-h"><h1>{T["writing_h"]}</h1><p>{T["writing_p"]}</p></div>
<section class="block">{series_html()}</section>"""
    page("writing/index.html", f"{T['writing_h']} — {S['title_suffix']}", body, 1, "writing")

    body = f"""<div class="page-h"><h1>{T["lab_h"]}</h1><p>{T["lab_p"]}</p></div>
<section class="block">{sec("01", T["music_h"])}<p class="music-p">{T["music_p"]}</p>{music_grid(abase(1))}</section>
<section class="block">{sec("02", T["repo_h"])}{lab_rows()}</section>"""
    page("lab/index.html", f"{T['lab_h']} — {S['title_suffix']}", body, 1, "lab")

    brand = T["about_brand"].format(en=S["tagline_en"], zh=S["tagline_zh"]).strip()

    def strength(n, label, alt, head, text, href, link):
        h = href if href.startswith("http") else f"{lbase(1)}{href}"
        return (f'<div class="strength"><p class="s-label"><span>{n}</span> {e(label)}'
                f'{" · " + e(alt) if alt else ""}</p><h2>{e(head)}</h2><p>{e(text)}</p><a href="{h}">{e(link)}</a></div>')

    cards = "".join(strength(*x) for x in T["strengths"])
    body = f"""<div class="page-h"><h1>{T["about_h"]}</h1></div>
<div class="about">
<p class="about-lead">{T["about_lead"]}</p>
<p class="about-intro">{T["about_intro"]}</p>
<div class="strengths">{cards}</div>
<p class="brand-line">{brand}</p>
<div class="btns"><a class="btn primary" href="{S["github"]}">GitHub ↗</a></div>
<p class="contact"><span>{T["about_contact"]}</span> <a href="mailto:{S["email"]}">{S["email"]}</a></p></div>"""
    page("about/index.html", f"{T['about_h']} — {S['title_suffix']}", body, 1, "about")


def build(lang):
    global C, S, T, LANG, OFF
    LANG, OFF = lang, 1 if lang == "en" else 0
    fn = "content.json" if lang == "zh" else "content.en.json"
    C = json.loads((ROOT / "data" / fn).read_text(encoding="utf-8"))
    S, T = C["site"], UI[lang]
    generate()


for lg in ("zh", "en"):
    build(lg)
(ROOT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    + "".join(f'<url><loc>{u}</loc><xhtml:link rel="alternate" hreflang="{"en" if "/en/" in a else "zh-CN"}" href="{a}"/></url>\n' for u, a in URLS)
    + "</urlset>\n", encoding="utf-8")
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}sitemap.xml\n", encoding="utf-8")
(ROOT / "404.html").write_text(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>404 — LINTHESIS</title><link rel="icon" href="/LINTHESIS/brand/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/LINTHESIS/css/brand.css"><link rel="stylesheet" href="/LINTHESIS/css/site.css"></head>
<body><div class="wrap"><header class="top"><a class="logo" href="/LINTHESIS/"><img src="/LINTHESIS/brand/linthesis-structure-horizontal.svg" alt="LINTHESIS"></a></header>
<main><div class="page-h"><h1>404</h1><p>这个页面不存在。 This page does not exist.</p>
<div class="btns" style="margin-top:24px"><a class="btn primary" href="/LINTHESIS/">首页</a><a class="btn" href="/LINTHESIS/en/">Home (English)</a></div></div></main></div></body></html>
""", encoding="utf-8")
n = len([f for f in ROOT.rglob("index.html") if "_work" not in f.parts])
print("built", n, "pages")
