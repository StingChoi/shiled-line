# -*- coding: utf-8 -*-
r"""정보성 글 페이지 생성 스크립트 (/info/)

작업 일지(/blog/)는 "무슨 차를 시공했다"는 기록이고, 여기 /info/ 는
"코팅을 어떻게 고르느냐"를 설명하는 정보성 글이다. 검색·AI가 묻는 질문의
성격이 달라서 분리했다.

원고 계약(Aside·Codex와 공유):
  원고는 `info/_src/<슬러그>.html` 에 <article> 조각으로 둔다.
  첫 줄들의 주석에서 제목·메타설명을 읽는다.
      <!-- 제목: ... -->
      <!-- 메타 설명(...): ... -->
  날짜는 파일 mtime 을 쓴다.

주의: `info/*.html` 은 전부 생성물이다. 직접 고치지 말고 `_src` 원고를 고칠 것.

수동 실행:  py gen_info_pages.py
자동 실행:  auto_publish.bat (gen_sitemap.py 앞)
"""
import os
import re
import glob
import io
import datetime

import gen_area_pages as gap   # 공통 머리말·내비·푸터 재사용

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'info', '_src')
OUT = os.path.join(ROOT, 'info')
BASE = gap.BASE
esc = gap.esc


def up(block):
    """루트용 상대경로(assets/...)를 /info/ 하위에서도 맞게 고친다."""
    return (block.replace('href="assets/', 'href="../assets/')
                 .replace('src="assets/', 'src="../assets/')
                 .replace('src="assets/images', 'src="../assets/images'))


CSS = """            <style>
                .ia{max-width:760px;margin:0 auto;}
                .ia-meta{color:#8A9199;font-size:.9rem;margin:0 0 2rem;}
                .ia article h1{font-size:clamp(23px,3.6vw,33px);line-height:1.35;margin:0 0 1.4rem;}
                .ia article h2{font-size:clamp(19px,2.8vw,24px);margin:2.6rem 0 1rem;
                               padding-top:1.6rem;border-top:1px solid var(--border-light);}
                .ia article h3{font-size:clamp(16px,2.3vw,18px);margin:1.8rem 0 .5rem;}
                .ia article p{color:#B9C0C7;line-height:1.9;margin:0 0 1.1rem;}
                .ia article p strong,.ia article li strong{color:#fff;}
                .ia article ul{color:#B9C0C7;line-height:1.9;padding-left:1.2rem;margin:0 0 1.1rem;}
                .ia article li{margin-bottom:.5rem;}
                .ia article a{color:var(--primary);}
                .ia article table{width:100%;border-collapse:collapse;font-size:.93rem;margin:0 0 1.4rem;}
                .ia article th,.ia article td{padding:.8rem .7rem;border-bottom:1px solid var(--border-light);
                                              text-align:left;vertical-align:top;color:#B9C0C7;line-height:1.7;}
                .ia article thead th{color:#fff;font-weight:700;}
                .ia-cta{display:flex;gap:.5rem;flex-wrap:wrap;margin-top:2.5rem;
                        padding-top:1.8rem;border-top:1px solid var(--border-light);}
                @media (max-width:680px){
                    .ia article thead{display:none;}
                    .ia article th,.ia article td{display:block;border-bottom:0;padding:.2rem 0;}
                    .ia article tbody tr{display:block;border-bottom:1px solid var(--border-light);padding:.95rem 0;}
                }
            </style>"""


def parse(fp):
    s = io.open(fp, encoding='utf-8').read()
    m_t = re.search(r'<!--\s*제목:\s*(.+?)\s*-->', s)
    m_d = re.search(r'<!--\s*메타 설명[^:]*:\s*(.+?)\s*-->', s)
    m_a = re.search(r'<article>.*</article>', s, re.S)
    if not (m_t and m_d and m_a):
        return None
    slug = os.path.basename(fp)[:-5]
    return {
        'slug': slug,
        'title': m_t.group(1),
        'desc': m_d.group(1),
        'body': m_a.group(0),
        'date': datetime.date.fromtimestamp(os.path.getmtime(fp)).isoformat(),
    }


def article_schema(p):
    return """<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "BreadcrumbList",
      "@id": "{base}/info/{slug}#breadcrumb",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "쉴드광택", "item": "{base}/" }},
        {{ "@type": "ListItem", "position": 2, "name": "정보", "item": "{base}/info/" }},
        {{ "@type": "ListItem", "position": 3, "name": {title}, "item": "{base}/info/{slug}" }}
      ]
    }},
    {{
      "@type": "Article",
      "@id": "{base}/info/{slug}#article",
      "headline": {title},
      "description": {desc},
      "datePublished": "{date}",
      "dateModified": "{date}",
      "inLanguage": "ko-KR",
      "author": {{ "@id": "https://www.shiled-line.com/#choi" }},
      "publisher": {{ "@id": "https://www.shiled-line.com/#business" }},
      "mainEntityOfPage": {{ "@type": "WebPage", "@id": "{base}/info/{slug}" }}
    }}
  ]
}}
</script>""".format(base=BASE, slug=p['slug'], title=gap.jstr(p['title']),
                    desc=gap.jstr(p['desc']), date=p['date'])


def head(slug, title, desc, keywords, extra):
    return """<!DOCTYPE html>
<html lang="ko">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

{verify}

    <title>{title}</title>
    <meta name="description" content="{desc}">
    <meta name="keywords" content="{keywords}">
    <link rel="canonical" href="{base}/info/{slug}" />
    <meta property="og:type" content="article" />
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{desc}" />
    <meta property="og:url" content="{base}/info/{slug}" />
    <meta property="og:site_name" content="쉴드광택" />
    <meta property="og:locale" content="ko_KR" />

{fonts}
{business}
{extra}

<script src="/assets/js/analytics.js" defer></script>
</head>

<body>

{nav}
""".format(verify=gap.VERIFY, title=esc(title), desc=esc(desc), keywords=esc(keywords),
           base=BASE, slug=slug, fonts=up(gap.FONTS), business=gap.BUSINESS_SCHEMA,
           extra=extra, nav=up(gap.NAV))


def build_article(p):
    kw = '유리막코팅 가격, 유리막코팅 비용, 부산 유리막코팅, 코팅 가격 차이, 쉴드광택'
    page = head(p['slug'], p['title'] + ' | 쉴드광택', p['desc'], kw, article_schema(p))
    page += """
    <main id="app">

        <section class="section" style="padding-top:7rem;">
            <div class="container">
{css}
                <div class="ia">
                    <p class="ia-meta"><a href="/info/" class="gradient-text">정보</a> · {date}</p>
{body}
                    <div class="ia-cta">
                        <a href="/price" class="btn btn-primary">차급별 단가표 보기 →</a>
                        <a href="tel:01033841850" class="btn btn-outline">📞 010-3384-1850</a>
                        <a href="http://pf.kakao.com/_xexfYVX/chat" target="_blank" rel="noopener noreferrer" class="btn" style="background:#FEE500; color:#3C1E1E;">💬 카카오톡 상담</a>
                    </div>
                </div>
            </div>
        </section>

    </main>

{foot}
""".format(css=CSS, date=p['date'].replace('-', '. ') + '.', body=p['body'], foot=up(gap.FOOT))
    return page


def build_index(posts):
    title = '정보 | 유리막코팅·광택을 고르기 전에 알아둘 것 | 쉴드광택'
    desc = ('유리막코팅과 광택을 고르기 전에 알아두면 좋은 내용을 16년간 코팅제를 직접 개발해 온 '
            '쉴드광택 대표가 정리했습니다. 가격 차이, 코팅제 선택, 시공 순서 등.')
    rows = []
    for p in posts:
        rows.append("""                    <a class="post-card" href="/info/{slug}">
                        <span class="pc-body">
                            <span class="pc-tag">정보</span>
                            <span class="pc-title">{title}</span>
                            <span class="pc-date">{date}</span>
                            <span class="pc-sum">{desc}</span>
                        </span>
                    </a>""".format(slug=p['slug'], title=esc(p['title']),
                                   date=esc(p['date'].replace('-', '. ') + '.'),
                                   desc=esc(p['desc'])))

    schema = """<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "@id": "{base}/info/",
  "name": "정보",
  "description": {desc},
  "inLanguage": "ko-KR",
  "isPartOf": {{ "@id": "https://www.shiled-line.com/#website" }},
  "publisher": {{ "@id": "https://www.shiled-line.com/#business" }}
}}
</script>""".format(base=BASE, desc=gap.jstr(desc))

    page = head('', title, desc, '유리막코팅 정보, 광택 정보, 부산 유리막코팅, 쉴드광택', schema)
    page = page.replace('href="%s/info/"' % BASE, 'href="%s/info/"' % BASE)
    page += """
    <main id="app">

        <div class="page-header">
            <h1 class="page-title">정보</h1>
            <p class="page-desc">BEFORE YOU CHOOSE</p>
        </div>
        <section class="section" style="padding-top:0;">
            <div class="container">
                <div style="max-width:760px;margin:0 auto 2.5rem;">
                    <p class="text-muted" style="line-height:1.9;">코팅을 고르기 전에 알아두면 좋은 내용을 정리합니다.
                        시공한 차량 기록은 <a href="/blog/" class="gradient-text">작업 일지</a>에 따로 있습니다.</p>
                </div>
                <div class="post-grid">
{rows}
                </div>
            </div>
        </section>

    </main>

{foot}
""".format(rows='\n'.join(rows), foot=up(gap.FOOT))
    return page


def main():
    srcs = sorted(glob.glob(os.path.join(SRC, '*.html')))
    posts = [p for p in (parse(f) for f in srcs) if p]
    if not posts:
        print('[gen_info_pages] info/_src 에 원고가 없습니다. 아무것도 만들지 않습니다.')
        return
    posts.sort(key=lambda p: (p['date'], p['slug']), reverse=True)

    for p in posts:
        out = os.path.join(OUT, p['slug'] + '.html')
        io.open(out, 'w', encoding='utf-8', newline='\n').write(build_article(p))
        print('[gen_info_pages] info/%-32s %s' % (p['slug'] + '.html', p['title'][:36]))

    idx = os.path.join(OUT, 'index.html')
    io.open(idx, 'w', encoding='utf-8', newline='\n').write(build_index(posts))
    print('[gen_info_pages] info/index.html (%d편)' % len(posts))


if __name__ == '__main__':
    main()
