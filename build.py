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

UI = {
    "zh": dict(
        html_lang="zh-CN", bt=("《", "》"), nav_both=True, switch="EN", switch_label="English version",
        h_works_short="作品", h_books_short="书籍", home_label="LINTHESIS 首页", nav_label="主导航",
        h_works="Works 作品", h_books="Books 书籍", h_writing="Writing 在线长篇写作", h_lab="Lab 实验室",
        view_all="查看全部 →",
        works_h="Works 作品", works_p="我创造的软件、工具和网站。每一项都有自己的介绍、截图和访问入口。",
        books_h="Books 书籍", books_p="已出版的纸质书，以及持续更新的在线教程。",
        books_pub="出版 Published", books_online="在线教程 Online", books_more="更多在线长篇 →",
        writing_h="Writing 文章", writing_p="持续更新的在线长篇写作，按主题成系列。点开每个系列，进入对应的在线电子书。",
        writing_todo="短文与研究笔记栏目待补。",
        music_h="AI 音乐", music_p="用 AI 创作的歌曲和 MV，这里放了其中几首。", repo_h="开源实验",
        lab_h="Lab 实验室", lab_p="尚在探索的想法、原型和实验项目，状态不一，多数仍在演进。",
        about_h="About 关于",
        about_lead="想清楚，写下来，做出来，再分享出去。",
        about_intro="我早期做数据科学、机器学习和统计，写过四本关于 R 与统计分析的书；现在更感兴趣的是 AI、区块链、软件开发、商业与创业。方向在变，做事的方式没变：先把问题想明白，再用文字和作品讲清楚，最后公开出来。",
        strengths=[
            ("01", "认知", "Cognition", "先理解，再动手。", "我花很多时间研究思考本身：怎样观察一个问题，怎样拆解结构，怎样做判断。这些想法被整理成《认知语言工程》，以及自我、人际、结构等系列。", "writing/", "看这些系列 →"),
            ("02", "写作", "Writing", "把复杂的东西讲清楚。", "四本已出版的书，加上 100 多本在线电子书，从 R 与统计，到 AI、架构与语言，持续更新。", "books/", "看我的书 →"),
            ("03", "创造", "Creating", "把想法做成能用的东西。", "原生 macOS 应用、本地工作流、设计系统图鉴……我自己做软件，也用 AI 编码工具把它们做出来，并把方法写成教程。", "works/", "看我做的软件 →"),
            ("04", "分享", "Sharing", "做出来的，公开出来。", "电子书在线阅读，项目代码公开在 GitHub，过程和方法也一并写出来，希望能帮到走在同一条路上的人。", "https://github.com/liamamilin", "GitHub ↗"),
        ],
        about_brand="LINTHESIS 是这些创作共用的署名：把思考、知识与技术，变成可用的作品。{en} {zh}",
        about_contact="联系我",
        k_status="状态", k_platform="平台", k_tech="技术", k_author="作者", k_pub="出版社", k_year="出版年份",
        k_isbn="ISBN", k_format="形式", k_lang="语言", v_format="在线电子书", v_lang="中文", v_author="米霖",
        s_intro="介绍", s_feat="核心功能", s_note="说明", s_demo="演示", s_shots="截图", s_blurb="简介", s_home="首页",
        b_pub="出版社 / 购买页 ↗", b_read="在线阅读 ↗", shot_alt="截图", cover_alt="封面", home_alt="首页截图",
        kick_book="BOOK / 出版", kick_guide="BOOK / GUIDE", gh="GitHub ↗", hero_tags=True,
        online="电子书", footer_extra="A LINTHESIS Project", title_book="《{t}》",
    ),
    "en": dict(
        html_lang="en", bt=("", ""), nav_both=False, switch="中文", switch_label="中文版",
        h_works_short="Works", h_books_short="Books", home_label="LINTHESIS home", nav_label="Main navigation",
        h_works="Works", h_books="Books", h_writing="Writing: long-form online", h_lab="Lab",
        view_all="View all →",
        works_h="Works", works_p="Software, tools and websites I have made. Each has its own write-up, screenshots and links.",
        books_h="Books", books_p="Published print books, and online guides that keep growing.",
        books_pub="Published", books_online="Online guides", books_more="More long-form online →",
        writing_h="Writing", writing_p="Long-form writing published online, grouped into series. Each link opens the matching online book. The books themselves are in Chinese.",
        writing_todo="Short essays and research notes: coming.",
        music_h="AI Music", music_p="Songs and music videos made with AI. A small selection is here.", repo_h="Open-source experiments",
        lab_h="Lab", lab_p="Ideas, prototypes and experiments still being explored. They are at different stages, and most are still evolving.",
        about_h="About",
        about_lead="Think it through, write it down, build it, and share it.",
        about_intro="I started in data science, machine learning and statistics, and wrote four books on R and statistical analysis. What interests me now is AI, blockchain, software development, business and entrepreneurship. The subject has changed; the way I work has not: understand the problem first, explain it with words and with things that work, then put it out in the open.",
        strengths=[
            ("01", "Cognition", "认知", "Understand first, then build.", "I spend a lot of time studying thinking itself: how to look at a problem, take a structure apart, and make a judgment. Those ideas became Cognitive Language Engineering and the series on self, people and structure.", "writing/", "See the series →"),
            ("02", "Writing", "写作", "Make the complicated clear.", "Four published books and more than a hundred online books, from R and statistics to AI, architecture and language, still growing.", "books/", "See the books →"),
            ("03", "Creating", "创造", "Turn ideas into things that work.", "Native macOS apps, local workflows, a visual index of design systems. I build the software myself, with AI coding tools, and write the method up as guides.", "works/", "See the software →"),
            ("04", "Sharing", "分享", "What I make, I put out in the open.", "Books you can read online, code public on GitHub, and the process and method written down too, in the hope it helps others on the same road.", "https://github.com/liamamilin", "GitHub ↗"),
        ],
        about_brand="LINTHESIS is the shared byline for all of this: turning thought, knowledge and technology into work that is usable. {en}",
        about_contact="Get in touch",
        k_status="Status", k_platform="Platform", k_tech="Stack", k_author="Author", k_pub="Publisher", k_year="Year",
        k_isbn="ISBN", k_format="Format", k_lang="Language", v_format="Online book", v_lang="Chinese", v_author="Mi Lin",
        s_intro="About", s_feat="Features", s_note="Note", s_demo="Demo", s_shots="Screenshots", s_blurb="Description", s_home="Home page",
        b_pub="Publisher page ↗", b_read="Read online ↗", shot_alt="screenshot", cover_alt="cover", home_alt="home page screenshot",
        kick_book="BOOK / PUBLISHED", kick_guide="BOOK / GUIDE", gh="GitHub ↗", hero_tags=True,
        online="Online book", footer_extra="A LINTHESIS Project", title_book="{t}",
    ),
}
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


def book_cards(depth):
    lb = lbase(depth)
    out = ""
    for b in C["print_books"]:
        out += card(f'{lb}books/{b["slug"]}/', b["cover"], bt(b["title"]), f'{b["publisher"]} · {b["year"]}', "book")
    for b in C["ebooks"]:
        out += card(f'{lb}books/{b["slug"]}/', b["cover"], bt(b["title"]), f'{T["online"]} · {b["status"]}')
    return out


def series_html():
    cols = ""
    for s in C["series"]:
        lis = "".join(f'<li><a href="{u}">{e(n)}</a></li>' for n, u in s["items"])
        cols += f'<div><h3>{e(s["name"])}</h3><ul>{lis}</ul></div>'
    return f'<div class="series">{cols}</div>'


def lab_rows():
    return '<div class="rows lab">' + "".join(
        f'<a href="{u}"><div><b>{e(n)}</b><em>{e(d)}</em></div><span>GitHub ↗</span></a>' for n, u, d in C["lab"]) + "</div>"


def music_grid(ab):
    return '<div class="music">' + "".join(
        f'<figure><video controls playsinline preload="none" poster="{ab}img/music/{k}.jpg" src="{ab}video/music/{k}.mp4"></video>'
        f'<figcaption>{e(t)}</figcaption></figure>' for k, t in C["music"]) + "</div>"


def video_block(item, ab):
    return (f'<h2>{T["s_demo"]}</h2><div class="shots"><figure><video controls muted playsinline preload="metadata" '
            f'poster="{ab}{item["poster"]}" src="{ab}{item["video"]}"></video></figure></div>')


def meta_rows(rows):
    return "".join(f"<div><dt>{k}</dt><dd>{e(v)}</dd></div>" for k, v in rows)


def generate():
    tl = S["tagline_zh"]
    zh_p = f'<p class="zh">{tl}</p>' if tl else ""
    home = f"""
<section class="hero">
<div class="stage"><span><i></i>01 / Thought</span><span>02 / Structure</span><span>03 / Form</span></div>
<h1>{S["tagline_en"]}</h1>
{zh_p}
<p class="lead">{S["intro"]}</p>
<div class="tags"><a href="works/">Software</a><a href="books/">Books</a><a href="writing/">Writing</a><a href="lab/">Experiments</a></div>
</section>
<section class="block">{sec("01", T["h_works"], "works/")}
<div class="grid">{project_cards(0)}</div></section>
<section class="block">{sec("02", T["h_books"], "books/")}
<div class="grid four">{book_cards(0)}</div></section>
<section class="block">{sec("03", T["h_writing"], "writing/")}
{series_html()}</section>
<section class="block">{sec("04", T["h_lab"], "lab/")}
{lab_rows()}</section>
"""
    page("index.html", f'{S["name"]} — {S["tagline_en"]}', fill(home, 0), 0)

    body = f"""<div class="page-h"><h1>{T["works_h"]}</h1><p>{T["works_p"]}</p></div>
<section class="block"><div class="grid">{project_cards(1)}</div></section>"""
    page("works/index.html", f"{T['works_h']} — {S['title_suffix']}", fill(body, 1), 1, "works")

    for p in C["projects"]:
        ab = abase(2)
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
