#!/usr/bin/env python3
"""Generate the static site (zh at root, en under /en/) from data/content*.json.
Run: python3 build.py"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).parent
e = html.escape

UI = {
    "zh": dict(
        html_lang="zh-CN", bt=("《", "》"), nav_both=True, switch="EN", switch_label="English version",
        home_label="LINTHESIS 首页", nav_label="主导航",
        h_works="Works 作品", h_books="Books 书籍", h_writing="Writing 在线长篇写作", h_lab="Lab 实验室",
        view_all="查看全部 →",
        works_h="Works 作品", works_p="我创造的软件、工具和网站。每一项都有自己的介绍、截图和访问入口。",
        books_h="Books 书籍", books_p="已出版的纸质书，以及持续更新的在线教程。",
        books_pub="出版 Published", books_online="在线教程 Online", books_more="更多在线长篇 →",
        writing_h="Writing 文章", writing_p="持续更新的在线长篇写作，按主题成系列。点开每个系列，进入对应的在线电子书。",
        writing_todo="短文与研究笔记栏目待补。",
        lab_h="Lab 实验室", lab_p="尚在探索的想法、原型和实验项目。多数仍在演进，说明待补。",
        about_h="About 关于",
        about_lead="我长期做数据分析，现在把更多时间放在 AI 与软件开发上。",
        about_p1="早些年，我的实践和写作集中在数据科学、机器学习和统计：写过四本关于 R 语言与统计分析的书，也把 Python、数据仓库、A/B 测试、指标体系这些做法整理成在线教程。",
        about_p2="现在，我更感兴趣的是 AI、区块链、软件开发、商业与创业。这些方向有一个共同点：它们都在把想法变成能运行、能被使用的东西。所以我开始自己动手做软件，并把使用 AI 编码工具的经验写成《驾驭 Codex》《驾驭 Claude》。",
        then_h="过去", now_h="现在",
        then_items=["数据科学", "机器学习", "统计"],
        now_items=["AI", "区块链", "软件开发", "商业", "创业"],
        then_link=("books/", "看这几本书 →"), now_link=("works/", "看我做的软件 →"),
        do_h="我做什么",
        do_rows=[("Software", "原生 macOS 应用、工作流和网站", "works/"), ("Books", "出版的书，和在线教程", "books/"), ("Writing", "按主题成系列的在线长篇", "writing/")],
        about_brand="LINTHESIS 是这些创作共用的署名：把思考、知识与技术，变成可用的作品。{en} {zh}",
        about_todo="联系方式待补。",
        k_status="状态", k_platform="平台", k_tech="技术", k_author="作者", k_pub="出版社", k_year="出版年份",
        k_isbn="ISBN", k_format="形式", k_lang="语言", v_format="在线电子书", v_lang="中文", v_author="米霖",
        s_intro="介绍", s_feat="核心功能", s_note="说明", s_demo="演示", s_shots="截图", s_blurb="简介", s_home="首页",
        b_pub="出版社 / 购买页 ↗", b_read="在线阅读 ↗", shot_alt="截图", cover_alt="封面", home_alt="首页截图",
        kick_book="BOOK / 出版", kick_guide="BOOK / GUIDE", gh="GitHub ↗", hero_tags=True,
        online="电子书", footer_extra="A LINTHESIS Project", title_book="《{t}》",
    ),
    "en": dict(
        html_lang="en", bt=("", ""), nav_both=False, switch="中文", switch_label="中文版",
        home_label="LINTHESIS home", nav_label="Main navigation",
        h_works="Works", h_books="Books", h_writing="Writing: long-form online", h_lab="Lab",
        view_all="View all →",
        works_h="Works", works_p="Software, tools and websites I have made. Each has its own write-up, screenshots and links.",
        books_h="Books", books_p="Published print books, and online guides that keep growing.",
        books_pub="Published", books_online="Online guides", books_more="More long-form online →",
        writing_h="Writing", writing_p="Long-form writing published online, grouped into series. Each link opens the matching online book. The books themselves are in Chinese.",
        writing_todo="Short essays and research notes: coming.",
        lab_h="Lab", lab_p="Ideas, prototypes and experiments still being explored. Most are evolving; descriptions to come.",
        about_h="About",
        about_lead="I spent years in data analysis. Now I spend more of my time on AI and software.",
        about_p1="Earlier on, my practice and writing centered on data science, machine learning and statistics. I wrote four books on R and statistical analysis, and turned Python, data warehousing, A/B testing and metric systems into online guides.",
        about_p2="What interests me now is AI, blockchain, software development, business and entrepreneurship. They share one thing: each turns an idea into something that runs and gets used. So I started building software myself, and wrote up what I learned from AI coding tools as Mastering Codex and Mastering Claude.",
        then_h="Before", now_h="Now",
        then_items=["Data science", "Machine learning", "Statistics"],
        now_items=["AI", "Blockchain", "Software development", "Business", "Entrepreneurship"],
        then_link=("books/", "See the books →"), now_link=("works/", "See the software →"),
        do_h="What I make",
        do_rows=[("Software", "Native macOS apps, workflows and websites", "works/"), ("Books", "Published books and online guides", "books/"), ("Writing", "Long-form online writing, grouped into series", "writing/")],
        about_brand="LINTHESIS is the shared byline for all of this: turning thought, knowledge and technology into work that is usable. {en}",
        about_todo="Contact details to come.",
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
    doc = f"""<!doctype html>
<html lang="{T["html_lang"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="alternate" hreflang="{alt_lang}" href="{alt}">
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
    return '<div class="rows">' + "".join(
        f'<a href="{u}"><b>{e(n)}</b><span>GitHub ↗</span></a>' for n, u in C["lab"]) + "</div>"


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
<aside><p class="kicker">{e(p["kind"])}</p><h1>{e(p["title"])}</h1><p class="zh">{e(p["sub"])}</p>
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
<aside><div class="cover-big{png}"><img src="{ab}{b["cover"]}" alt="{e(bt(b["title"]))} {T["cover_alt"]}"></div>
<dl class="meta">{meta_rows(rows)}</dl><div class="btns"><a class="btn primary" href="{b["link"]}">{T["b_pub"]}</a></div></aside>
<div class="body"><p class="kicker">{T["kick_book"]}</p><h1>{e(b["title"])}</h1>{sub}
<h2>{T["s_blurb"]}</h2><p>{e(b["intro"])}</p></div></article>"""
        page(f"books/{b['slug']}/index.html", f"{bt(b['title'])} — {S['title_suffix']}", body, 2, "books", b["intro"])

    for b in C["ebooks"]:
        ab = abase(2)
        rows = [(T["k_format"], T["v_format"]), (T["k_status"], b["status"]), (T["k_lang"], T["v_lang"])]
        body = f"""<article class="detail">
<aside><p class="kicker">{T["kick_guide"]}</p><h1>{e(b["title"])}</h1><p class="zh">{e(b["sub"])}</p>
<dl class="meta">{meta_rows(rows)}</dl><div class="btns"><a class="btn primary" href="{b["link"]}">{T["b_read"]}</a></div></aside>
<div class="body"><h2>{T["s_blurb"]}</h2><p>{e(b["intro"])}</p>
{video_block(b, ab)}<h2>{T["s_home"]}</h2><div class="shots"><figure><img src="{ab}{b["cover"]}" alt="{e(b["title"])} {T["home_alt"]}" loading="lazy"></figure></div></div></article>"""
        page(f"books/{b['slug']}/index.html", f"{b['title']} — {S['title_suffix']}", body, 2, "books", b["intro"])

    body = f"""<div class="page-h"><h1>{T["writing_h"]}</h1><p>{T["writing_p"]}</p></div>
<section class="block">{series_html()}</section>
<section class="block"><p class="todo">{T["writing_todo"]}</p></section>"""
    page("writing/index.html", f"{T['writing_h']} — {S['title_suffix']}", body, 1, "writing")

    body = f"""<div class="page-h"><h1>{T["lab_h"]}</h1><p>{T["lab_p"]}</p></div>
<section class="block">{lab_rows()}</section>"""
    page("lab/index.html", f"{T['lab_h']} — {S['title_suffix']}", body, 1, "lab")

    brand = T["about_brand"].format(en=S["tagline_en"], zh=S["tagline_zh"]).strip()
    chips = lambda items: "".join(f"<li>{e(i)}</li>" for i in items)
    do_rows = "".join(f'<a href="{lbase(1)}{href}"><b>{e(k)}</b><span>{e(v)}</span></a>' for k, v, href in T["do_rows"])
    body = f"""<div class="page-h"><h1>{T["about_h"]}</h1></div>
<div class="about">
<p class="about-lead">{T["about_lead"]}</p>
<p>{T["about_p1"]}</p>
<p>{T["about_p2"]}</p>
<div class="then-now">
<div><h3>{T["then_h"]}</h3><ul class="chips">{chips(T["then_items"])}</ul><a href="{lbase(1)}{T["then_link"][0]}">{T["then_link"][1]}</a></div>
<div><h3>{T["now_h"]}</h3><ul class="chips">{chips(T["now_items"])}</ul><a href="{lbase(1)}{T["now_link"][0]}">{T["now_link"][1]}</a></div>
</div>
<h3 class="sub-h">{T["do_h"]}</h3>
<div class="rows">{do_rows}</div>
<p class="brand-line">{brand}</p>
<div class="btns"><a class="btn primary" href="{S["github"]}">GitHub ↗</a></div>
<p class="todo">{T["about_todo"]}</p></div>"""
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
n = len([f for f in ROOT.rglob("index.html") if "_work" not in f.parts])
print("built", n, "pages")
