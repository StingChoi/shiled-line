# -*- coding: utf-8 -*-
"""
sitemap.xml 자동 생성 스크립트.
blog/ 폴더의 실제 HTML 글을 스캔해서 항상 최신 sitemap.xml을 만든다.
auto_publish.bat 의 'git add -A' 앞에서 호출하면 발행 때마다 sitemap이 갱신된다.

수동 실행:  py gen_sitemap.py
"""
import os
import glob
import datetime

BASE_URL = "https://www.shiled-line.com"
ROOT = os.path.dirname(os.path.abspath(__file__))

# (파일경로, URL경로, changefreq, priority)
FIXED_PAGES = [
    ("index.html",      "/",          "weekly",  "1.0"),
    ("faq.html",        "/faq.html",  "monthly", "0.7"),
    ("blog/index.html", "/blog/",     "daily",   "0.8"),
]


def lastmod(path):
    ts = os.path.getmtime(path)
    return datetime.date.fromtimestamp(ts).isoformat()


def url_block(loc, mod, freq, prio):
    return (
        "  <url>\n"
        f"    <loc>{loc}</loc>\n"
        f"    <lastmod>{mod}</lastmod>\n"
        f"    <changefreq>{freq}</changefreq>\n"
        f"    <priority>{prio}</priority>\n"
        "  </url>\n"
    )


def main():
    lines = ['<?xml version="1.0" encoding="UTF-8"?>\n']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')

    count = 0
    # 고정 페이지
    for rel, urlpath, freq, prio in FIXED_PAGES:
        fpath = os.path.join(ROOT, rel)
        if os.path.exists(fpath):
            lines.append(url_block(BASE_URL + urlpath, lastmod(fpath), freq, prio))
            count += 1

    # 블로그 개별 글 (index.html / 테스트 파일 제외)
    posts = sorted(glob.glob(os.path.join(ROOT, "blog", "*.html")))
    for fpath in posts:
        name = os.path.basename(fpath)
        if name == "index.html" or "zztest" in name:
            continue
        loc = f"{BASE_URL}/blog/{name}"
        lines.append(url_block(loc, lastmod(fpath), "monthly", "0.6"))
        count += 1

    lines.append('</urlset>\n')

    out = os.path.join(ROOT, "sitemap.xml")
    with open(out, "w", encoding="utf-8") as f:
        f.write("".join(lines))

    print(f"[gen_sitemap] sitemap.xml updated: {count} URLs")


if __name__ == "__main__":
    main()
