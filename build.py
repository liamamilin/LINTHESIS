#!/usr/bin/env python3
"""Generate the static site from data/content.json. Run: python3 build.py"""
import html
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
C = json.loads((ROOT / "data/content.json").read_text(encoding="utf-8"))
S = C["site"]
e = html.escape

NAV = [("works", "Works", "作品"), ("books", "Books", "书籍"), ("writing", "Writing", "文章"),
       ("lab", "Lab", "实验室"), ("about", "About", "关于")]


def page(path, title, body, depth, active="", desc=""):
    base = "../" * depth
    cur = ' aria-current="page"'
    nav = "".join(
        f'<a href="{base}{k}/"{cur if k == active else ""}>{en} <span lang="zh">{zh}</span></a>'
        for k, en, zh in NAV)
    desc = desc or f'{S["tagline_en"]} {S["tagline_zh"]}{S["intro"]}'
    doc = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="icon" href="{base}brand/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{base}css/brand.css">
<link rel="stylesheet" href="{base}css/site.css">
</head>
<body>
<div class="wrap">
<header class="top">
<a class="logo" href="{base}" aria-label="LINTHESIS 首页"><img src="{base}brand/linthesis-structure-horizontal.svg" alt="LINTHESIS"></a>
<nav aria-label="主导航">{nav}</nav>
<a class="ext" href="{S["github"]}">GitHub ↗</a>
</header>
<main>
{body}
</main>
<footer>
<img src="{base}brand/linthesis-structure-symbol.svg" alt="">
<span>{S["author"]} · A LINTHESIS Project</span>
<span class="sp">{S["tagline_en"]} {S["tagline_zh"]}</span>
</footer>
</div>
</body>
</html>
"""
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")


def tile(img, kind="shot"):
    if kind == "book":
        cls = "tile book png" if img.endswith(".png") else "tile book"
        return f'<div class="{cls}"><img src="{{b}}{img}" alt="" loading="lazy"></div>'
    return f'<div class="tile"><img src="{{b}}{img}" alt="" loading="lazy"></div>'


def card(href, img, title, meta, kind="shot", badge=""):
    b = f'<span class="badge">{e(badge)}</span>' if badge else ""
    return (f'<a class="card" href="{href}">{tile(img, kind)}'
            f'<div class="cap"><b>{e(title)}{b}</b><span>{e(meta)}</span></div></a>')


def sec(n, title, link=None, text="查看全部 →"):
    a = f'<a href="{link}">{text}</a>' if link else ""
    return f'<div class="sec-h"><span class="n">{n}</span><h2>{title}</h2>{a}</div>'


def fill(s, depth):
    return s.replace("{b}", "../" * depth)


def project_cards(depth, items=None):
    base = "../" * depth
    return "".join(
        card(f'{base}works/{p["slug"]}/', p["cover"], f'{p["title"]} · {p["zh"]}', f'{p["kind"]} · {p["status"]}')
        for p in (items or C["projects"]))


def book_cards(depth):
    base = "../" * depth
    out = ""
    for b in C["print_books"]:
        out += card(f'{base}books/{b["slug"]}/', b["cover"], f'《{b["title"]}》', f'{b["publisher"]} · {b["year"]}', "book")
    for b in C["ebooks"]:
        out += card(f'{base}books/{b["slug"]}/', b["cover"], f'《{b["title"]}》', f'电子书 · {b["status"]}')
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


# ---------- home ----------
home = f"""
<section class="hero">
<div class="stage"><span><i></i>01 / Thought</span><span>02 / Structure</span><span>03 / Form</span></div>
<h1>{S["tagline_en"]}</h1>
<p class="zh">{S["tagline_zh"]}</p>
<p class="lead">{S["intro"]}</p>
<div class="tags"><a href="works/">Software</a><a href="books/">Books</a><a href="writing/">Writing</a><a href="lab/">Experiments</a></div>
</section>
<section class="block">{sec("01", "Works 作品", "works/")}
<div class="grid">{project_cards(0)}</div></section>
<section class="block">{sec("02", "Books 书籍", "books/")}
<div class="grid four">{book_cards(0)}</div></section>
<section class="block">{sec("03", "Writing 在线长篇写作", "writing/")}
{series_html()}</section>
<section class="block">{sec("04", "Lab 实验室", "lab/")}
{lab_rows()}</section>
"""
page("index.html", f'{S["name"]} — {S["tagline_en"]}', fill(home, 0), 0)

# ---------- works ----------
body = f"""<div class="page-h"><h1>Works 作品</h1><p>我创造的软件、工具和网站。每一项都有自己的介绍、截图和访问入口。</p></div>
<section class="block"><div class="grid">{project_cards(1)}</div></section>"""
page("works/index.html", f"Works — {S['title_suffix']}", fill(body, 1), 1, "works")

for p in C["projects"]:
    meta = "".join(f"<div><dt>{k}</dt><dd>{e(v)}</dd></div>" for k, v in
                   [("状态", p["status"]), ("平台", p["platform"]), ("技术", p["tech"])])
    btns = "".join(f'<a class="btn{" primary" if i == 0 else ""}" href="{u}">{e(n)} ↗</a>' for i, (n, u) in enumerate(p["links"]))
    feats = "".join(f"<li>{e(f)}</li>" for f in p["features"])
    note = f'<h2>说明</h2><p class="note">{e(p["note"])}</p>' if p.get("note") else ""
    shots = "".join(f'<figure><img src="../../{g}" alt="{e(p["title"])} 截图" loading="lazy"></figure>' for g in p["gallery"])
    body = f"""<article class="detail">
<aside><p class="kicker">{e(p["kind"])}</p><h1>{e(p["title"])}</h1><p class="zh">{e(p["zh"])}</p>
<dl class="meta">{meta}</dl><div class="btns">{btns}</div></aside>
<div class="body"><p class="one">{e(p["one_liner"])}</p>
<h2>介绍</h2><p>{e(p["intro"])}</p>
<h2>核心功能</h2><ul>{feats}</ul>{note}
<h2>截图</h2><div class="shots">{shots}</div></div></article>"""
    page(f"works/{p['slug']}/index.html", f"{p['title']} — {S['title_suffix']}", body, 2, "works", p["one_liner"])

# ---------- books ----------
pb = "".join(card(f'../books/{b["slug"]}/', b["cover"], f'《{b["title"]}》', f'{b["publisher"]} · {b["year"]}', "book") for b in C["print_books"])
eb = "".join(card(f'../books/{b["slug"]}/', b["cover"], f'《{b["title"]}》', b["status"]) for b in C["ebooks"])
body = f"""<div class="page-h"><h1>Books 书籍</h1><p>已出版的纸质书，以及持续更新的在线教程。</p></div>
<section class="block">{sec("01", "出版 Published")}<div class="grid four">{pb}</div></section>
<section class="block">{sec("02", "在线教程 Online", "../writing/", "更多在线长篇 →")}<div class="grid">{eb}</div></section>"""
page("books/index.html", f"Books — {S['title_suffix']}", fill(body, 1), 1, "books")

for b in C["print_books"]:
    meta = [("作者", "米霖"), ("出版社", b["publisher"]), ("出版年份", str(b["year"]))]
    if b["isbn"]:
        meta.append(("ISBN", b["isbn"]))
    m = "".join(f"<div><dt>{k}</dt><dd>{e(v)}</dd></div>" for k, v in meta)
    png = " png" if b["cover"].endswith(".png") else ""
    body = f"""<article class="detail">
<aside><div class="cover-big{png}"><img src="../../{b["cover"]}" alt="《{e(b["title"])}》封面"></div>
<dl class="meta">{m}</dl><div class="btns"><a class="btn primary" href="{b["link"]}">出版社 / 购买页 ↗</a></div></aside>
<div class="body"><p class="kicker">BOOK / 出版</p><h1>{e(b["title"])}</h1>
<h2>简介</h2><p>{e(b["intro"])}</p></div></article>"""
    page(f"books/{b['slug']}/index.html", f"《{b['title']}》— {S['title_suffix']}", body, 2, "books", b["intro"])

for b in C["ebooks"]:
    meta = [("形式", "在线电子书"), ("状态", b["status"])]
    m = "".join(f"<div><dt>{k}</dt><dd>{e(v)}</dd></div>" for k, v in meta)
    body = f"""<article class="detail">
<aside><p class="kicker">BOOK / GUIDE</p><h1>{e(b["title"])}</h1><p class="zh">{e(b["sub"])}</p>
<dl class="meta">{m}</dl><div class="btns"><a class="btn primary" href="{b["link"]}">在线阅读 ↗</a></div></aside>
<div class="body"><h2>简介</h2><p>{e(b["intro"])}</p>
<h2>预览</h2><div class="shots"><figure><img src="../../{b["cover"]}" alt="《{e(b["title"])}》首页截图" loading="lazy"></figure></div></div></article>"""
    page(f"books/{b['slug']}/index.html", f"{b['title']} — {S['title_suffix']}", body, 2, "books", b["intro"])

# ---------- writing / lab / about ----------
body = f"""<div class="page-h"><h1>Writing 文章</h1><p>持续更新的在线长篇写作，按主题成系列。点开每个系列，进入对应的在线电子书。</p></div>
<section class="block">{series_html()}</section>
<section class="block"><p class="todo">短文与研究笔记栏目待补。</p></section>"""
page("writing/index.html", f"Writing — {S['title_suffix']}", body, 1, "writing")

body = f"""<div class="page-h"><h1>Lab 实验室</h1><p>尚在探索的想法、原型和实验项目。多数仍在演进，说明待补。</p></div>
<section class="block">{lab_rows()}</section>"""
page("lab/index.html", f"Lab — {S['title_suffix']}", body, 1, "lab")

body = f"""<div class="page-h"><h1>About 关于</h1></div>
<div class="about">
<p>{S["author"]}。写过四本关于 R 语言与统计分析的书，也把 AI 编码工具的使用经验写成在线教程，同时做自己想用的软件。</p>
<p>LINTHESIS 是这些创作共用的署名：把思考、知识与技术，变成可用的作品。{S["tagline_en"]} {S["tagline_zh"]}</p>
<div class="btns"><a class="btn primary" href="{S["github"]}">GitHub ↗</a></div>
<p class="todo">联系方式待补。</p></div>"""
page("about/index.html", f"About — {S['title_suffix']}", body, 1, "about")

print("built", len(list(ROOT.rglob("index.html"))), "pages")
