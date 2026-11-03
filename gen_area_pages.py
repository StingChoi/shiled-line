# -*- coding: utf-8 -*-
r"""
지역·브랜드 랜딩 페이지 생성 스크립트
================================================================
  /suyeong   수영구 광택 · 유리막코팅
  /namcheon  남천동 광택 · 유리막코팅
  /benz      벤츠 광택 · 유리막코팅

왜 따로 페이지를 두는가:
  홈·서비스 페이지는 "부산 남구"로만 적혀 있어서 "수영구 광택",
  "남천동 유리막코팅" 같은 지역 질의에 걸릴 페이지가 아예 없었다.
  검색·AI는 질의와 페이지를 1:1로 맞추기 때문에, 지역·브랜드마다
  고유 URL과 고유 본문이 있어야 한다.

왜 손으로 쓰지 않고 생성 스크립트인가:
  (1) 머리말(head)·내비·푸터가 다른 정적 페이지와 어긋나지 않게 한 곳에서 찍는다.
  (2) 벤츠 시공 기록 편수와 최신 사례 카드를 blog/ 에서 실측해 채운다.
      블로그가 매일 늘어나므로 숫자를 손으로 적으면 바로 거짓이 된다.

주의: 이 세 파일은 전부 생성물이다. 직접 고치지 말고 이 스크립트를 고칠 것.

수동 실행:  py gen_area_pages.py
자동 실행:  auto_publish.bat (gen_sitemap.py 앞)
"""
import os
import re
import glob
import io

import gen_latest_posts as glp   # parse_post() / esc() 재사용

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://www.shiled-line.com"

esc = glp.esc


def jstr(s):
    """JSON 문자열 리터럴. 따옴표·역슬래시만 막으면 되는 평문이다."""
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


# ============================================================
# 공통 머리말 / 내비 / 푸터 — 다른 정적 페이지(services.html 등)와 같아야 한다
# ============================================================

VERIFY = """    <!-- 검색엔진 소유권 확인 (구글 서치콘솔 / 네이버 서치어드바이저) -->
    <meta name="google-site-verification" content="Ru7VeQMpSigzDYdqgSxIhsKfPYTR-iEX_G2yENgZiRI" />
    <meta name="naver-site-verification" content="35ed6235f2c34e1b8e38d6664740b26e7099e94f" />"""

FONTS = """    <!-- Google Fonts: Inter and Noto Sans KR -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link
        href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap"
        rel="stylesheet">

    <link rel="stylesheet" href="assets/css/style.css?v=20260903">"""

# 사업체 스키마. areaServed 는 지역 페이지 신설과 함께 "부산" 한 줄에서
# 실제 상권(남구·수영구·해운대구 + 동 단위)으로 넓혔다 — 다른 페이지도 같은 값이다.
BUSINESS_SCHEMA = """<!-- ============================================================
     쉴드광택 사업체 스키마 (JSON-LD)  ※ 모든 페이지 <head>에 공통 적용
     ------------------------------------------------------------
     우편번호(48529)·geo 좌표는 유엔로 220(대연동 565-10, 대원관)
     실측값으로 확정 완료. sameAs는 유튜브·네이버블로그·인스타·블로거 반영.
     ============================================================ -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": ["AutoRepair", "LocalBusiness"],
      "@id": "https://www.shiled-line.com/#business",
      "name": "쉴드광택",
      "alternateName": "Shield Gloss",
      "legalName": "쉴드랩",
      "url": "https://www.shiled-line.com/",
      "image": "https://www.shiled-line.com/assets/images/shiled_badge_v2.png",
      "logo": "https://www.shiled-line.com/assets/images/shiled_badge_v2.png",
      "telephone": "+82-10-3384-1850",
      "slogan": "어떤 차를 타냐보다 어떻게 타냐가 중요합니다",
      "description": "부산 남구에 위치한 자동차 광택·유리막코팅 전문점. 16년간 유리막코팅제(F5·G-PRO·G-TOP)를 직접 개발·제조해온 코팅제 개발자가 직접 시공합니다. 메르세데스-벤츠 부산 남천점 공식 협력 업체. 쉴드광택은 Benz & BMW & 테슬라 전문점입니다.",
      "priceRange": "₩₩₩",
      "currenciesAccepted": "KRW",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "유엔로220 1층",
        "addressLocality": "남구",
        "addressRegion": "부산",
        "postalCode": "48529",
        "addressCountry": "KR"
      },
      "geo": {
        "@type": "GeoCoordinates",
        "latitude": 35.129811,
        "longitude": 129.100345
      },
      "areaServed": [
        { "@type": "City", "name": "부산광역시" },
        { "@type": "AdministrativeArea", "name": "부산 남구" },
        { "@type": "AdministrativeArea", "name": "부산 수영구" },
        { "@type": "AdministrativeArea", "name": "부산 해운대구" },
        { "@type": "Place", "name": "남천동" },
        { "@type": "Place", "name": "광안동" },
        { "@type": "Place", "name": "민락동" },
        { "@type": "Place", "name": "수영동" },
        { "@type": "Place", "name": "망미동" },
        { "@type": "Place", "name": "대연동" },
        { "@type": "Place", "name": "용호동" }
      ],
      "openingHoursSpecification": [
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
          "opens": "09:00",
          "closes": "18:00"
        },
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": "Saturday",
          "opens": "09:00",
          "closes": "16:00"
        }
      ],
      "founder": { "@id": "https://www.shiled-line.com/#choi" },
      "sameAs": [
        "https://www.youtube.com/@stingchoi5171",
        "https://blog.naver.com/shiledgt",
        "https://www.instagram.com/sting_choi",
        "https://shieldgloss.blogspot.com",
        "https://map.naver.com/p/entry/place/2024246792",
        "http://pf.kakao.com/_xexfYVX"
      ]
    },
    {
      "@type": "Person",
      "@id": "https://www.shiled-line.com/#choi",
      "name": "최한중",
      "jobTitle": "대표 / 코팅제 개발자",
      "worksFor": { "@id": "https://www.shiled-line.com/#business" },
      "alumniOf": { "@type": "CollegeOrUniversity", "name": "부경대학교 화학공학과" },
      "description": "화학공학을 전공한 자동차 유리막코팅제 개발자이자 16년 경력의 현장 시공자. F5·G-PRO·G-TOP 코팅제를 직접 개발·제조하여 시공한다."
    }
  ]
}
</script>"""

NAV = """    <!-- Header / GNB -->
    <header class="header" id="header">
        <div class="container header-inner">
            <a href="/" class="logo">
                <img src="assets/images/shiled_badge_v2.png" alt="쉴드광택 로고" class="header-logo-img">
                <span class="header-logo-text">쉴드광택</span>
            </a>

            <nav class="gnb">
                <ul class="nav-list">
                    <li><a href="/about" class="nav-link">회사소개</a></li>
                    <li><a href="/products" class="nav-link">제품소개</a></li>
                    <li><a href="/price" class="nav-link">서비스 단가</a></li>
                    <li><a href="/services" class="nav-link">서비스소개</a></li>
                    <li><a href="/certificates" class="nav-link">시공증명서</a></li>
                    <li><a href="/partners" class="nav-link">전문점 소개</a></li>
                    <li><a href="/coating-layers" class="nav-link">코팅 원리</a></li>
                    <li><a href="/faq" class="nav-link">자주 묻는 질문</a></li>
                    <li><a href="/blog/" class="nav-link">작업 일지</a></li>
                </ul>
            </nav>

            <button class="mobile-menu-btn" aria-label="메뉴 열기">
                <span></span>
                <span></span>
                <span></span>
            </button>
        </div>
    </header>"""

FOOT = """    <!-- Global Audio Player -->
    <!-- 로고송(풀버전 3:17). preload="none" — 🎵 버튼을 누르기 전에는 내려받지 않는다. -->
    <audio id="bg-audio" loop preload="none">
        <source src="assets/logo.mp3" type="audio/mpeg">
    </audio>
    <button id="audio-toggle-btn" class="audio-toggle" aria-label="음악 재생/일시정지">
        🎵
    </button>

    <!-- Footer -->
    <footer class="footer">
        <div class="container footer-inner">
            <div class="footer-info">
                <h3>쉴드광택 (SHIELD GLOSS)</h3>
                <p style="color:var(--primary); font-weight:700;">쉴드광택은 Benz &amp; BMW &amp; 테슬라 전문점입니다.</p>
                <p>대표: 최한중</p>
                <p>주소: 부산 남구 유엔로 220, 대원관 1층(대연동)</p>
                <p>예약 및 문의: <a href="tel:01033841850" class="gradient-text">010-3384-1850</a></p>
                <p>
                    <a href="http://pf.kakao.com/_xexfYVX" target="_blank" rel="noopener noreferrer" class="gradient-text">카카오톡 채널</a>
                    &nbsp;·&nbsp;
                    <a href="https://map.naver.com/p/entry/place/2024246792" target="_blank" rel="noopener noreferrer" class="gradient-text">네이버 플레이스</a>
                    &nbsp;·&nbsp;
                    <a href="https://blog.naver.com/shiledgt" target="_blank" rel="noopener noreferrer" class="gradient-text">블로그</a>
                </p>
                <p style="margin-top:0.9rem;">시공 지역 안내:
                    <a href="/suyeong" class="gradient-text">수영구</a>&nbsp;·&nbsp;<a href="/namcheon" class="gradient-text">남천동</a>&nbsp;·&nbsp;<a href="/daeyeon" class="gradient-text">대연동</a>&nbsp;·&nbsp;<a href="/benz" class="gradient-text">벤츠</a>&nbsp;·&nbsp;<a href="/bmw" class="gradient-text">BMW</a>
                </p>
                <p style="margin-top:0.4rem;">알아두면 좋은 정보:
                    <a href="/info/" class="gradient-text">코팅 선택 가이드</a>
                </p>
                <div style="margin-top:1.25rem; line-height:1.7; opacity:0.6;">
                    <p style="margin:0; font-size:0.78rem;">상호: 쉴드광택(쉴드랩)&nbsp;|&nbsp;대표: 최한중</p>
                    <p style="margin:0; font-size:0.78rem;">사업자등록번호: 298-21-01391</p>
                    <p style="margin:0; font-size:0.78rem;">통신판매업신고: 제 2026-부산남구-0466 호</p>
                    <p style="margin:0; font-size:0.78rem;">사업장 소재지: 부산광역시 남구 유엔로 220, 대원관 1층(대연동)</p>
                </div>
            </div>
            <div class="footer-bottom">
                &copy; <span id="year"></span> Shield Gloss. All rights reserved.
            </div>
        </div>
    </footer>

    <!-- Firebase SDKs (v8 compat) -->
    <script src="https://www.gstatic.com/firebasejs/8.10.1/firebase-app.js"></script>
    <script src="https://www.gstatic.com/firebasejs/8.10.1/firebase-auth.js"></script>
    <script src="https://www.gstatic.com/firebasejs/8.10.1/firebase-firestore.js"></script>

    <!-- Application Scripts -->
    <script src="assets/js/firebase-config.js"></script>
    <script src="assets/js/stats-counter.js" defer></script>
    <script src="assets/js/pages.js?v=1.3"></script>
    <script src="assets/js/app.js?v=1.4"></script>
</body>

</html>"""

# 지역 페이지 전용 스타일. style.css 를 건드리면 전 페이지의 캐시 버스터를 같이
# 올려야 하므로, 이 세 페이지에서만 쓰는 것은 페이지 안에 둔다(services.html 과 같은 방식).
AREA_CSS = """            <style>
                .ar-wrap{max-width:900px;margin:0 auto;}
                .ar-lead{font-size:clamp(15px,2.2vw,18px);line-height:1.85;color:#D7DCE1;margin:0 0 2.8rem;}
                .ar-lead b{color:#fff;font-weight:700;}
                .ar-block{margin:0 0 3rem;}
                .ar-block > h2{font-size:clamp(20px,3vw,26px);margin:0 0 1.1rem;}
                .ar-block h3{font-size:clamp(16px,2.4vw,19px);margin:0 0 .5rem;}
                .ar-block p{color:#B9C0C7;line-height:1.85;margin:0 0 .9rem;}
                .ar-block p:last-child{margin-bottom:0;}
                .ar-block p b{color:#fff;}
                .ar-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(255px,1fr));gap:1rem;}
                .ar-card{background:rgba(255,255,255,.025);border:1px solid var(--border-light);
                         border-radius:12px;padding:1.5rem;transition:border-color .25s ease;}
                .ar-card:hover{border-color:var(--border-gold);}
                .ar-table{width:100%;border-collapse:collapse;font-size:.95rem;}
                .ar-table th,.ar-table td{padding:.85rem .7rem;border-bottom:1px solid var(--border-light);
                                          text-align:left;vertical-align:top;color:#B9C0C7;line-height:1.7;}
                .ar-table thead th{color:#fff;font-weight:700;white-space:nowrap;}
                .ar-table tbody th{color:#fff;font-weight:700;white-space:nowrap;}
                .ar-table td b{color:#fff;}
                .ar-tags{display:flex;flex-wrap:wrap;gap:.5rem;margin:0;padding:0;list-style:none;}
                .ar-tags li{margin:0;}
                .ar-tags li a,.ar-tags li span{display:inline-block;padding:.42rem .85rem;border-radius:999px;
                    border:1px solid var(--border-light);background:rgba(255,255,255,.03);
                    font-size:.86rem;color:#C9D0D7;text-decoration:none;}
                .ar-tags li a:hover{border-color:var(--primary);color:#fff;}
                .ar-faq{border-top:1px solid var(--border-light);padding-top:1.2rem;margin-top:1.2rem;}
                .ar-faq:first-of-type{border-top:0;padding-top:0;margin-top:0;}
                .ar-cta{display:flex;gap:.5rem;flex-wrap:wrap;margin-top:1.3rem;}
                @media (max-width:680px){
                    .ar-table thead{display:none;}
                    .ar-table th,.ar-table td{display:block;border-bottom:0;padding:.2rem 0;}
                    .ar-table tbody tr{display:block;border-bottom:1px solid var(--border-light);padding:.95rem 0;}
                }
            </style>"""


def head(slug, title, desc, keywords, extra_schema):
    return """<!DOCTYPE html>
<html lang="ko">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

{verify}

    <title>{title}</title>
    <meta name="description" content="{desc}">
    <meta name="keywords" content="{keywords}">
    <link rel="canonical" href="{base}/{slug}" />
    <meta property="og:type" content="website" />
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{desc}" />
    <meta property="og:url" content="{base}/{slug}" />
    <meta property="og:image" content="{base}/assets/images/before-after/e300-rear-after.jpg" />
    <meta property="og:site_name" content="쉴드광택" />
    <meta property="og:locale" content="ko_KR" />

{fonts}
{business}
{extra}

<script src="/assets/js/analytics.js" defer></script>
</head>

<body>

{nav}
""".format(verify=VERIFY, title=esc(title), desc=esc(desc), keywords=esc(keywords),
           base=BASE, slug=slug, fonts=FONTS, business=BUSINESS_SCHEMA,
           extra=extra_schema, nav=NAV)


def page_schema(slug, name, desc, service_type, area_names, faqs):
    """페이지 고유 스키마: 빵부스러기 + 서비스(지역 포함) + 자주 묻는 질문."""
    areas = ",\n        ".join(
        '{ "@type": "Place", "name": %s }' % jstr(a) for a in area_names)
    faq_items = ",\n      ".join(
        """{
        "@type": "Question",
        "name": %s,
        "acceptedAnswer": { "@type": "Answer", "text": %s }
      }""" % (jstr(q), jstr(a)) for q, a in faqs)
    return """<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "BreadcrumbList",
      "@id": "{base}/{slug}#breadcrumb",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "쉴드광택", "item": "{base}/" }},
        {{ "@type": "ListItem", "position": 2, "name": {name}, "item": "{base}/{slug}" }}
      ]
    }},
    {{
      "@type": "Service",
      "@id": "{base}/{slug}#service",
      "name": {name},
      "serviceType": {stype},
      "description": {desc},
      "provider": {{ "@id": "https://www.shiled-line.com/#business" }},
      "url": "{base}/{slug}",
      "areaServed": [
        {areas}
      ]
    }},
    {{
      "@type": "FAQPage",
      "@id": "{base}/{slug}#faq",
      "mainEntity": [
      {faqs}
      ]
    }}
  ]
}}
</script>""".format(base=BASE, slug=slug, name=jstr(name), stype=jstr(service_type),
                    desc=jstr(desc), areas=areas, faqs=faq_items)


def tags_html(items):
    """items: (라벨, 링크 또는 None) 목록."""
    out = ['            <ul class="ar-tags">']
    for label, href in items:
        if href:
            out.append('                <li><a href="%s">%s</a></li>' % (href, esc(label)))
        else:
            out.append('                <li><span>%s</span></li>' % esc(label))
    out.append('            </ul>')
    return "\n".join(out)


def faq_html(faqs):
    return "\n".join(
        """                <div class="ar-faq">
                    <h3>%s</h3>
                    <p>%s</p>
                </div>""" % (esc(q), esc(a)) for q, a in faqs)


def cta_html(extra_line=""):
    return """            <div class="ar-block">
                <div class="glass-card">
                    <h2 style="margin-top:0;">예약 · 상담</h2>
                    {extra}<p><b>주소</b> · 부산 남구 유엔로 220, 대원관 1층(대연동)</p>
                    <p><b>영업시간</b> · 평일 09:00–18:00 / 토요일 09:00–16:00 (일요일 휴무)</p>
                    <p><b>예약·문의</b> · 010-3384-1850</p>
                    <div class="ar-cta">
                        <a href="tel:01033841850" class="btn btn-primary">📞 전화로 예약하기</a>
                        <a href="http://pf.kakao.com/_xexfYVX/chat" target="_blank" rel="noopener noreferrer" class="btn" style="background:#FEE500; color:#3C1E1E;">💬 카카오톡 상담</a>
                        <a href="/price" class="btn btn-outline">시공 단가표 보기</a>
                    </div>
                </div>
            </div>""".format(extra=extra_line)


def wrap(slug, title, desc, keywords, schema, h1, kicker, body):
    return (head(slug, title, desc, keywords, schema)
            + """
    <main id="app">

        <div class="page-header">
            <h1 class="page-title">{h1}</h1>
            <p class="page-desc">{kicker}</p>
        </div>
        <section class="section" style="padding-top:0;">
            <div class="container">
{css}
                <div class="ar-wrap">
{body}
                </div>
            </div>
        </section>

    </main>

{foot}
""".format(h1=esc(h1), kicker=esc(kicker), css=AREA_CSS, body=body, foot=FOOT))


# ============================================================
# 블로그 실측 — 사례 카드 / 벤츠 모델별 기록 편수
# ============================================================

def load_posts():
    files = [f for f in glob.glob(os.path.join(ROOT, 'blog', '*.html'))
             if os.path.basename(f) != 'index.html'
             and 'zztest' not in os.path.basename(f)]
    posts = []
    for f in files:
        p = glp.parse_post(f)
        if p:
            p['slug'] = os.path.basename(f)[:-5]
            posts.append(p)
    posts.sort(key=lambda p: (p['date'], p['slug']), reverse=True)
    return posts


def cards_html(posts):
    out = ['            <div class="post-grid">']
    for p in posts:
        out.append("""                <a class="post-card" href="/{url}">
                    <span class="pc-thumb" style="background-image:url('{thumb}')" aria-hidden="true"></span>
                    <span class="pc-body">
                        <span class="pc-tag">{tag}</span>
                        <span class="pc-title">{headline}</span>
                        <span class="pc-date">{date}</span>
                    </span>
                </a>""".format(url=p['url'], thumb=esc(p['thumb']), tag=esc(p['tag']),
                               headline=esc(p['headline']), date=esc(p['date_txt'])))
    out.append('            </div>')
    return "\n".join(out)


# 벤츠 모델 계열. 위에서부터 먼저 걸리는 쪽으로 분류하므로 순서를 바꾸면 안 된다
# (gls·glc·gle·gla·glb 가 g450 패턴보다 먼저 와야 한다).
BENZ_GROUPS = [
    ('마이바흐',       r'^maybach',      '마이바흐 S580'),
    ('GLS',           r'^gls',           'GLS400 · GLS450 · GLS580 · GLS63'),
    ('GLC',           r'^glc',           'GLC300 · GLC300 쿠페'),
    ('GLE',           r'^gle',           'GLE350 · GLE450 · GLE53'),
    ('GLA · GLB',     r'^gl[ab]',        'GLA250 · GLB250'),
    ('G클래스',        r'^g\d|^g63',      'G450 · G63'),
    ('S클래스',        r'^s\d',           'S350 · S450 · S500 · S560 · S580'),
    ('E클래스',        r'^e\d|^amg-e',    'E200 · E220 · E300 · E350 · E450 · AMG E53'),
    ('CLE · CLS',     r'^cl[es]',        'CLE200 · CLE450 · CLE53 · CLS300'),
    ('C클래스',        r'^c\d',           'C200 · C300'),
    ('EQ (전기차)',    r'^eq',            'EQA250 · EQB300 · EQE350 SUV · EQS450 SUV'),
    ('AMG GT',        r'^gt\d|^amg-gt',  'AMG GT55 · GT63'),
    ('A · B클래스',    r'^[ab]\d',        'A220 · B200'),
]

# BMW 모델 계열. i 시리즈(i4·i5·iX3)가 X 시리즈보다 먼저 와야 iX3 가 X 로 새지 않는다.
BMW_GROUPS = [
    ('i 시리즈 (전기차)', r'^i[x\d]',      'i4 · i5 · iX3'),
    ('X 시리즈',         r'^x',            'X1 · X2 · X3 · X5 · X6 · X7 · XM'),
    ('5 시리즈',         r'^5\d\d',        '520i · 523d · 523e · 530i · 530e'),
    ('3 · 4 시리즈',     r'^[34]\d\d',     '320i · 340i'),
    ('7 · 8 시리즈',     r'^[78]\d\d|^m8', '740i · 740d · M850i'),
    ('1 · 2 시리즈',     r'^[12]\d\d',     '120 · 220 · 220i'),
]


def model_tail(slug, brand):
    """파일명에서 브랜드 앞부분을 떼어내 모델 토큰만 남긴다.
       benz-e300-... / 20260710-bmw-520i-... 둘 다 처리한다."""
    return re.sub(r'^.*?' + brand + r'-', '', slug.lower())


def brand_stats(posts, brand, groups):
    """작업 일지에 공개된 해당 브랜드 시공 기록을 모델 계열별로 집계한다."""
    mine = [p for p in posts if brand in p['slug'].lower()]
    counts = {}
    for p in mine:
        tail = model_tail(p['slug'], brand)
        for label, pat, _eg in groups:
            if re.match(pat, tail):
                counts[label] = counts.get(label, 0) + 1
                break
    rows = [(label, eg, counts[label])
            for label, _pat, eg in groups if counts.get(label)]
    rows.sort(key=lambda r: r[2], reverse=True)
    return mine, rows


def model_table(rows):
    out = ['            <table class="ar-table">',
           '                <thead><tr><th scope="col">모델 계열</th>'
           '<th scope="col">주요 차종</th><th scope="col">공개된 시공 기록</th></tr></thead>',
           '                <tbody>']
    for label, eg, n in rows:
        out.append('                    <tr><th scope="row">%s</th><td>%s</td><td><b>%d건</b></td></tr>'
                   % (esc(label), esc(eg), n))
    out += ['                </tbody>', '            </table>']
    return "\n".join(out)


def pick_variety(posts, limit, brand='benz'):
    """모델이 겹치지 않게 골라 최근 사례를 보여준다(같은 차종만 줄줄이 나오지 않게)."""
    seen, out = set(), []
    for p in posts:
        key = model_tail(p['slug'], brand).split('-')[0]
        if key in seen:
            continue
        seen.add(key)
        out.append(p)
        if len(out) == limit:
            break
    return out


# ============================================================
# 페이지 본문
# ============================================================

def build_suyeong(posts):
    slug = 'suyeong'
    title = '수영구 광택·유리막코팅 | 남천동·광안동·민락동 차로 10분 | 쉴드광택'
    desc = ('부산 수영구 자동차 광택·유리막코팅. 남천동에서 차로 10분, 광안동·민락동·수영동·망미동에서도 '
            '15분 안쪽입니다. 16년간 유리막코팅제 F5·G-PRO·G-TOP을 직접 개발해 온 사람이 직접 시공합니다. '
            '메르세데스-벤츠 부산 남천점 공식 협력업체 · 예약 010-3384-1850')
    keywords = ('수영구 광택, 수영구 유리막코팅, 남천동 유리막코팅, 남천동 광택, 광안동 유리막코팅, '
                '민락동 광택, 수영동 유리막코팅, 망미동 광택, 벤츠 광택, 벤츠 유리막코팅, '
                '부산 수영구 신차코팅, 부산 유막제거, 쉴드광택')
    faqs = [
        ('수영구에서 쉴드광택까지 얼마나 걸립니까?',
         '남천동에서 차로 약 10분, 광안동·민락동·수영동·망미동에서 15분 안쪽입니다. 쉴드광택은 남구 대연동 '
         '유엔로 220 대원관 1층에 있어 수영구와 구 경계를 맞대고 있습니다. 광안대교·수영교 어느 쪽으로 '
         '오셔도 신호 몇 개 차이입니다.'),
        ('차를 맡기고 가야 합니까, 기다려도 됩니까?',
         '시공 항목에 따라 다릅니다. 신차 유리막코팅은 도포 후 경화 시간이 필요해 보통 하루 맡기시는 쪽을 '
         '권합니다. 광택이 들어가면 작업 범위에 따라 더 걸립니다. 예약하실 때 차종과 원하시는 항목을 '
         '말씀해 주시면 걸리는 시간을 먼저 알려드립니다.'),
        ('광안리·민락 쪽에 세워두는 차인데 뭐가 더 필요합니까?',
         '바다 가까이 세워두는 차는 염분과 바다 물때가 쌓입니다. 이 경우 발수·방오에 특화된 G-TOP 쪽이 '
         '관리가 편하고, 이미 자리를 잡은 물때·유리 스케일은 코팅 전에 제거부터 해야 합니다. '
         '유막제거·초발수를 같이 보시는 분이 많습니다.'),
        ('가격은 어디서 볼 수 있습니까?',
         '시공 단가표를 금액까지 전부 공개해 두었습니다. 차급 7단계별 금액이 그대로 적혀 있고, 차종을 '
         '고르면 예상 금액이 바로 나오는 계산기도 있습니다.'),
    ]
    schema = page_schema(
        slug, '수영구 자동차 광택·유리막코팅', desc, '자동차 유리막코팅 · 광택',
        ['부산 수영구', '남천동', '광안동', '민락동', '수영동', '망미동', '부산 남구'], faqs)

    body = """                <p class="ar-lead">쉴드광택은 <b>부산 남구 대연동 유엔로 220</b>에 있습니다.
                    수영구와 구 경계를 맞대고 있어 <b>남천동에서 차로 10분</b>, 광안동·민락동·수영동·망미동에서도
                    15분 안쪽입니다. 16년간 유리막코팅제를 직접 개발·제조해 온 사람이 다른 사람 손에 넘기지 않고
                    직접 시공합니다.</p>

            <div class="ar-block">
                <h2>수영구 어디서 오셔도 15분 안쪽입니다</h2>
{roads}
            </div>

            <div class="ar-block">
                <h2>수영구 차량에서 특히 자주 보는 것</h2>
                <p>같은 부산이라도 차를 어디에 세워두는지에 따라 도장면에 남는 흔적이 다릅니다.
                    수영구는 바다와 가까워서 아래 세 가지 상담이 특히 많습니다.</p>
                <div class="ar-cards">
                    <div class="ar-card">
                        <h3>염분과 바다 물때</h3>
                        <p>광안리·민락 수변에 세워두는 차는 바닷바람에 실려 온 염분이 도장면과 유리에 말라붙습니다.
                            물때가 자리를 잡으면 세차로는 안 지워지고, 그 위에 코팅을 올리면 오염을 덮어버립니다.
                            <a href="/services#oilfilm" class="gradient-text">유막제거·초발수</a>부터 보셔야 하는 경우입니다.</p>
                    </div>
                    <div class="ar-card">
                        <h3>야간 운전과 유막</h3>
                        <p>광안대교·수영강변을 야간에 자주 달리시면 앞유리 유막이 바로 체감됩니다.
                            맞은편 빛이 번져 보이고 비 오는 날 와이퍼가 지나간 자리가 흐려집니다.
                            유리 쪽은 도장면과 따로 봐야 하는 작업입니다.</p>
                    </div>
                    <div class="ar-card">
                        <h3>지하주차장 차량의 잔기스</h3>
                        <p>지하에 세워 비·햇빛을 덜 맞는 차는 워터스팟보다 <b>잔기스(스월)</b>가 문제가 됩니다.
                            특히 검정 차는 조명이 지나갈 때마다 거미줄처럼 드러납니다.
                            <a href="/services#polish" class="gradient-text">광택으로 도장면을 정리한 뒤</a> 코팅을 올리는 순서가 맞습니다.</p>
                    </div>
                </div>
            </div>

            <div class="ar-block">
                <h2>수영구에서 많이 찾으시는 시공</h2>
                <table class="ar-table">
                    <thead><tr><th scope="col">시공</th><th scope="col">어떤 경우에</th></tr></thead>
                    <tbody>
                        <tr>
                            <th scope="row"><a href="/services#coating" class="gradient-text">신차 유리막코팅</a></th>
                            <td>남천동 전시장에서 신차를 받은 직후. 주행 전·비닐 떼기 전의 도장면이 가장 깨끗할 때라
                                연마를 최소로 하고 코팅만 올릴 수 있습니다.</td>
                        </tr>
                        <tr>
                            <th scope="row"><a href="/services#polish" class="gradient-text">광택 + 듀얼코팅</a></th>
                            <td>이미 타던 차. 잔기스·스월·물때를 광택으로 걷어낸 뒤 코팅을 두 층으로 올립니다.
                                검정·무광 계열에서 차이가 가장 크게 보입니다.</td>
                        </tr>
                        <tr>
                            <th scope="row"><a href="/services#oilfilm" class="gradient-text">유막제거 · 초발수</a></th>
                            <td>야간 주행 시 빛 번짐, 비 오는 날 와이퍼 자국. 유리 스케일까지 제거하고 발수를 올립니다.</td>
                        </tr>
                        <tr>
                            <th scope="row"><a href="/services#moulding" class="gradient-text">알루미늄 몰딩 복원</a></th>
                            <td>도어 몰딩이 하얗게 일어난 차량. 부품 교체 대신 복원으로 잡습니다.</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="ar-block">
                <h2>수영구 고객이 쉴드광택을 고르는 이유</h2>
                <div class="ar-cards">
                    <div class="ar-card">
                        <h3>코팅제를 직접 만듭니다</h3>
                        <p>남의 제품을 사다 바르는 곳이 아닙니다. 화학공학을 전공한 대표가 16년간
                            <a href="/products" class="gradient-text">F5·G-PRO·G-TOP</a>을 직접 개발·제조해 왔습니다.
                            차 상태에 맞는 제품을 고를 수 있는 이유입니다.</p>
                    </div>
                    <div class="ar-card">
                        <h3>시공증명서를 발급합니다</h3>
                        <p>모든 시공 차량에 <b>차대번호와 코팅제 시리얼</b>이 기재된
                            <a href="/certificates" class="gradient-text">시공증명서</a>를 발급합니다.
                            무엇을 몇 층 올렸는지 기록으로 남습니다.</p>
                    </div>
                    <div class="ar-card">
                        <h3>벤츠 부산 남천점 공식 협력업체</h3>
                        <p>메르세데스-벤츠 부산 남천점의 공식 협력업체입니다. 남천동에서 신차를 인수하고
                            바로 넘어오시는 분들이 많습니다.
                            <a href="/benz" class="gradient-text">벤츠 차량 안내 →</a></p>
                    </div>
                </div>
            </div>

            <div class="ar-block">
                <h2>최근 작업 일지</h2>
                <p>시공한 차량은 사진과 함께 작업 일지로 남깁니다. 비슷한 차종·색상을 찾아보시면
                    결과를 미리 가늠하실 수 있습니다.</p>
{cards}
                <div class="ar-cta">
                    <a href="/blog/" class="btn btn-outline">작업 일지 전체 보기 →</a>
                </div>
            </div>

            <div class="ar-block">
                <h2>자주 묻는 질문</h2>
{faq}
                <div class="ar-cta">
                    <a href="/faq" class="btn btn-outline">전체 FAQ 보기 →</a>
                </div>
            </div>

            <div class="ar-block">
                <h2>찾으시는 키워드</h2>
{tags}
            </div>

{cta}""".format(
        roads="""                <table class="ar-table">
                    <thead><tr><th scope="col">출발지</th><th scope="col">오시는 길</th></tr></thead>
                    <tbody>
                        <tr>
                            <th scope="row">남천동</th>
                            <td>남천역·삼익비치 기준 <b>차로 약 10분</b>. 벤츠 부산 남천점 공식 협력업체라
                                전시장에서 신차 인수 후 바로 입고하시는 경우가 가장 많습니다.
                                <a href="/namcheon" class="gradient-text">남천동 안내 →</a></td>
                        </tr>
                        <tr>
                            <th scope="row">광안동 · 민락동</th>
                            <td>광안리 해변로에서 <b>차로 약 15분</b>. 수변 주차 차량이 많아 염분·물때 상담이 잦습니다.</td>
                        </tr>
                        <tr>
                            <th scope="row">수영동 · 망미동</th>
                            <td>수영역·망미역 기준 <b>차로 약 15분</b>. 아파트 지하주차장 보관 차량이 많아
                                워터스팟보다 잔기스 제거 비중이 큽니다.</td>
                        </tr>
                        <tr>
                            <th scope="row">주소</th>
                            <td>부산 남구 유엔로 220, 대원관 1층(대연동) · 평일 09:00–18:00 / 토 09:00–16:00</td>
                        </tr>
                    </tbody>
                </table>""",
        cards=cards_html(posts[:6]),
        faq=faq_html(faqs),
        tags=tags_html([
            ('수영구 광택', None),
            ('수영구 유리막코팅', None),
            ('남천동 유리막코팅', '/namcheon'),
            ('남천동 광택', '/namcheon'),
            ('광안동 유리막코팅', None),
            ('민락동 광택', None),
            ('수영동 유리막코팅', None),
            ('망미동 광택', None),
            ('벤츠 광택', '/benz'),
            ('벤츠 유리막코팅', '/benz'),
            ('부산 신차코팅', '/services#coating'),
            ('부산 유막제거', '/services#oilfilm'),
            ('시공 단가표', '/price'),
        ]),
        cta=cta_html())

    return slug, wrap(slug, title, desc, keywords, schema,
                      '수영구 자동차 광택 · 유리막코팅', 'SUYEONG-GU · BUSAN', body)


def build_namcheon(posts, benz):
    slug = 'namcheon'
    title = '남천동 광택·유리막코팅 | 벤츠 부산 남천점 공식 협력업체 | 쉴드광택'
    desc = ('부산 남천동 자동차 광택·유리막코팅. 메르세데스-벤츠 부산 남천점 공식 협력업체로, 남천동에서 '
            '차로 10분입니다. 신차 인수 당일 F5·G-PRO·G-TOP 유리막코팅. 차대번호가 기재된 시공증명서 발급 '
            '· 예약 010-3384-1850')
    keywords = ('남천동 유리막코팅, 남천동 광택, 남천동 신차코팅, 수영구 유리막코팅, 수영구 광택, '
                '벤츠 남천점 코팅, 벤츠 유리막코팅, 벤츠 광택, 삼익비치 광택, 부산 신차 유리막코팅, 쉴드광택')
    faqs = [
        ('남천동에서 얼마나 걸립니까?',
         '남천역·삼익비치 기준 차로 약 10분입니다. 쉴드광택은 남구 대연동 유엔로 220 대원관 1층으로, '
         '남천동과는 구 경계 하나 차이입니다.'),
        ('벤츠 남천점에서 신차를 받았습니다. 바로 가면 됩니까?',
         '그렇게 오시는 분이 가장 많습니다. 메르세데스-벤츠 부산 남천점 공식 협력업체라 인수 당일 바로 '
         '입고하실 수 있습니다. 전시장에서 차를 받으시면 전화로 시간만 맞춰 주십시오.'),
        ('신차를 왜 받은 날 바로 코팅하는 것이 좋습니까?',
         '주행 전, 비닐을 떼기 전의 도장면이 가장 깨끗합니다. 이 상태면 연마를 거의 하지 않고 코팅만 '
         '올릴 수 있습니다. 몇 달 타고 오시면 잔기스와 오염을 먼저 걷어내야 해서 광택 공정이 추가됩니다.'),
        ('남천동 아파트 지하주차장에 세워둡니다. 어떤 코팅이 맞습니까?',
         '지하 보관 차량은 비·햇빛을 덜 맞는 대신 잔기스가 쌓이기 쉽습니다. 색감과 광이 목적이면 F5, '
         '단단함이 목적이면 G-PRO, 발수·방오가 목적이면 G-TOP 쪽입니다. 차 상태를 보고 조합을 '
         '권해 드립니다.'),
    ]
    schema = page_schema(
        slug, '남천동 자동차 광택·유리막코팅', desc, '자동차 유리막코팅 · 광택',
        ['남천동', '부산 수영구', '광안동', '부산 남구'], faqs)

    body = """                <p class="ar-lead">쉴드광택은 <b>메르세데스-벤츠 부산 남천점 공식 협력업체</b>입니다.
                    남천동에서 차로 10분, 남구 대연동 유엔로 220 대원관 1층에 있습니다.
                    남천점에서 신차를 인수하고 그대로 넘어오시는 분들이 가장 많습니다.</p>

            <div class="ar-block">
                <h2>신차 인수 당일 코팅이 가장 유리합니다</h2>
                <p>유리막코팅은 <b>도장면이 깨끗할 때</b> 올려야 제 성능이 납니다.
                    출고 직후, 주행 전·보호 비닐을 떼기 전의 도장면이 그 차가 평생 가질 가장 좋은 상태입니다.
                    이때라면 연마를 거의 하지 않고 코팅만 올릴 수 있습니다.</p>
                <p>반대로 몇 달 타고 오시면 세차 과정에서 생긴 잔기스와 물때를 먼저 걷어내야 하므로
                    <b>광택 공정이 추가</b>됩니다. 같은 코팅을 올려도 손이 더 가고 시간도 더 걸립니다.
                    남천점에서 차를 받으시는 날 전화 한 통으로 시간만 맞춰 주시면 됩니다.</p>
                <div class="ar-cta">
                    <a href="tel:01033841850" class="btn btn-primary">📞 010-3384-1850</a>
                    <a href="/coating-layers" class="btn btn-outline">코팅이 올라가는 순서 보기 →</a>
                </div>
            </div>

            <div class="ar-block">
                <h2>남천동 차량은 이런 조건에 놓입니다</h2>
                <div class="ar-cards">
                    <div class="ar-card">
                        <h3>바다가 가깝습니다</h3>
                        <p>광안리와 맞닿아 있어 바닷바람에 실린 염분이 도장면과 유리에 말라붙습니다.
                            발수·방오에 특화된 <a href="/products#gtop" class="gradient-text">G-TOP</a>이
                            관리 부담을 줄여 줍니다.</p>
                    </div>
                    <div class="ar-card">
                        <h3>지상·지하 주차가 섞여 있습니다</h3>
                        <p>삼익비치처럼 지상 주차 비중이 큰 단지는 워터스팟과 열에 의한 고착이,
                            지하 주차 단지는 잔기스가 주로 문제입니다. 같은 동네라도 처방이 갈립니다.</p>
                    </div>
                    <div class="ar-card">
                        <h3>검정·흰색 수입차 비중이 큽니다</h3>
                        <p>검정은 잔기스가 드러나고 흰색은 오염 경계가 드러납니다.
                            검정 차는 <a href="/services#polish" class="gradient-text">광택으로 도장면을 정리한 뒤</a>
                            코팅을 올리는 순서를 권합니다.</p>
                    </div>
                </div>
            </div>

            <div class="ar-block">
                <h2>남천동에서 받으실 수 있는 시공</h2>
                <table class="ar-table">
                    <thead><tr><th scope="col">시공</th><th scope="col">내용</th></tr></thead>
                    <tbody>
                        <tr><th scope="row"><a href="/services#coating" class="gradient-text">신차 유리막코팅</a></th>
                            <td>F5 · G-PRO · G-TOP 중 차량 상태와 목적에 맞춰 선택. 1코트 / 2코트 / 프리미엄 풀코팅.</td></tr>
                        <tr><th scope="row"><a href="/services#polish" class="gradient-text">광택 + 듀얼코팅</a></th>
                            <td>타던 차의 잔기스·스월·물때를 걷어낸 뒤 코팅 2층 마무리.</td></tr>
                        <tr><th scope="row"><a href="/services#moulding" class="gradient-text">알루미늄 도어몰딩 복원</a></th>
                            <td>하얗게 일어난 몰딩을 교체 대신 복원. 벤츠 E클래스에서 특히 수요가 많습니다.</td></tr>
                        <tr><th scope="row"><a href="/services#seat" class="gradient-text">가죽 시트코팅</a></th>
                            <td>신차 시트에 오염·이염이 자리 잡기 전에 처리.</td></tr>
                        <tr><th scope="row"><a href="/services#oilfilm" class="gradient-text">유막제거 · 초발수</a></th>
                            <td>야간 빛 번짐, 비 오는 날 와이퍼 자국 개선.</td></tr>
                    </tbody>
                </table>
                <div class="ar-cta">
                    <a href="/price" class="btn btn-outline">차급별 금액 전체 보기 →</a>
                </div>
            </div>

            <div class="ar-block">
                <h2>남천점에서 넘어온 벤츠 시공 기록</h2>
                <p>남천점 인수 차량을 포함해 작업 일지에 공개한 벤츠 시공 기록이
                    <b>{benz_n}건</b>입니다. 차종과 색상별로 어떻게 마무리되는지 사진으로 확인하실 수 있습니다.</p>
{cards}
                <div class="ar-cta">
                    <a href="/benz" class="btn btn-outline">벤츠 차량 전용 안내 →</a>
                    <a href="/blog/" class="btn btn-outline">작업 일지 전체 보기 →</a>
                </div>
            </div>

            <div class="ar-block">
                <h2>자주 묻는 질문</h2>
{faq}
            </div>

            <div class="ar-block">
                <h2>찾으시는 키워드</h2>
{tags}
            </div>

{cta}""".format(
        benz_n=len(benz),
        cards=cards_html(pick_variety(benz, 4)),
        faq=faq_html(faqs),
        tags=tags_html([
            ('남천동 유리막코팅', None),
            ('남천동 광택', None),
            ('남천동 신차코팅', None),
            ('수영구 유리막코팅', '/suyeong'),
            ('수영구 광택', '/suyeong'),
            ('벤츠 남천점 코팅', '/benz'),
            ('벤츠 유리막코팅', '/benz'),
            ('벤츠 광택', '/benz'),
            ('도어몰딩 복원', '/services#moulding'),
            ('시공증명서 조회', '/certificates'),
            ('시공 단가표', '/price'),
        ]),
        cta=cta_html(
            '<p><b>벤츠 부산 남천점에서 오시는 경우</b> · 인수 당일 바로 입고 가능합니다. '
            '전화로 시간만 맞춰 주십시오.</p>\n                    '))

    return slug, wrap(slug, title, desc, keywords, schema,
                      '남천동 자동차 광택 · 유리막코팅', 'NAMCHEON-DONG · BUSAN', body)


def build_benz(benz, rows):
    slug = 'benz'
    total = len(benz)
    title = '벤츠 유리막코팅·광택 | 부산 남천점 공식 협력업체 · 시공기록 %d건 공개 | 쉴드광택' % total
    desc = ('메르세데스-벤츠 부산 남천점 공식 협력업체. 작업 일지에 공개한 벤츠 유리막코팅·광택 시공 기록 '
            '%d건. E클래스·S클래스·GLC·GLE·G클래스·마이바흐까지 차종별 사례와 차급별 금액을 공개합니다. '
            '부산 남구 유엔로 220 · 예약 010-3384-1850' % total)
    keywords = ('벤츠 광택, 벤츠 유리막코팅, 벤츠 신차코팅, 벤츠 남천점 코팅, E클래스 유리막코팅, '
                'S클래스 광택, GLC 유리막코팅, GLE 신차코팅, G클래스 코팅, 마이바흐 광택, '
                '부산 벤츠 코팅, 남천동 유리막코팅, 쉴드광택')
    faqs = [
        ('벤츠 공식 협력업체가 맞습니까?',
         '메르세데스-벤츠 부산 남천점의 공식 협력업체입니다. 남천점에서 신차를 인수하신 분들이 당일 바로 '
         '입고하시는 경우가 가장 많습니다.'),
        ('제 벤츠는 어느 차급으로 계산됩니까?',
         'C클래스·CLA·GLA·GLB는 수입중형, E클래스·CLE·GLC 이상은 수입대형으로 봅니다. 단가표에 7개 차급 '
         '금액이 전부 공개되어 있고, 차종을 고르면 예상 금액이 바로 나오는 계산기도 있습니다.'),
        ('검정 벤츠인데 잔기스가 계속 보입니다. 코팅만 하면 됩니까?',
         '아닙니다. 코팅은 도장면을 덮는 것이라 이미 난 잔기스는 그대로 갇힙니다. 광택으로 도장면을 먼저 '
         '정리한 뒤 코팅을 올리는 순서가 맞습니다. 옵시디언 블랙 같은 어두운 색은 이 차이가 가장 크게 '
         '보이는 색입니다.'),
        ('E클래스 도어 몰딩이 하얗게 일어났습니다. 교체해야 합니까?',
         '복원으로 잡히는 경우가 많습니다. 알루미늄 몰딩 복원은 쉴드광택의 시공 항목이고, 부품 교체보다 '
         '부담이 적습니다. 상태를 보고 복원 가능 여부를 먼저 알려드립니다.'),
        ('시공 내역이 기록으로 남습니까?',
         '모든 시공 차량에 차대번호와 코팅제 시리얼이 기재된 시공증명서를 발급합니다. 차량별로 조회하실 '
         '수 있습니다.'),
    ]
    schema = page_schema(
        slug, '벤츠 유리막코팅·광택 시공', desc, '메르세데스-벤츠 유리막코팅 · 광택',
        ['부산광역시', '부산 남구', '부산 수영구', '남천동'], faqs)

    body = """                <p class="ar-lead">쉴드광택은 <b>메르세데스-벤츠 부산 남천점 공식 협력업체</b>입니다.
                    작업 일지에 사진과 함께 공개한 벤츠 시공 기록만 <b>{total}건</b>입니다.
                    E클래스부터 마이바흐까지, 차종·색상별로 어떻게 마무리됐는지 전부 열어 두었습니다.</p>

            <div class="ar-block">
                <h2>모델 계열별 공개된 시공 기록</h2>
                <p>아래 숫자는 홈페이지 작업 일지에 공개된 글을 모델 계열별로 집계한 것입니다
                    (발행 시점 자동 집계).</p>
{table}
                <div class="ar-cta">
                    <a href="/blog/" class="btn btn-outline">작업 일지 전체 보기 →</a>
                </div>
            </div>

            <div class="ar-block">
                <h2>벤츠에서 특히 자주 보는 세 가지</h2>
                <div class="ar-cards">
                    <div class="ar-card">
                        <h3>어두운 색 도장의 잔기스</h3>
                        <p>옵시디언 블랙 같은 어두운 색은 조명이 지나갈 때마다 거미줄 같은 스월이 드러납니다.
                            코팅은 도장면을 덮는 것이라 이미 난 기스는 갇혀 버립니다.
                            <a href="/services#polish" class="gradient-text">광택으로 먼저 정리</a>한 뒤
                            코팅을 올리는 순서여야 합니다.</p>
                    </div>
                    <div class="ar-card">
                        <h3>알루미늄 도어몰딩 백화</h3>
                        <p>E클래스 계열에서 특히 많이 보이는 증상입니다. 몰딩이 하얗게 일어나면
                            부품 교체를 떠올리시지만, <a href="/services#moulding" class="gradient-text">복원으로 잡히는</a>
                            경우가 많습니다.</p>
                    </div>
                    <div class="ar-card">
                        <h3>신차 출고 직후가 가장 좋은 때</h3>
                        <p>주행 전·보호 비닐을 떼기 전 도장면이 그 차의 최고 상태입니다.
                            이때 코팅을 올리면 연마를 거의 하지 않습니다.
                            <a href="/namcheon" class="gradient-text">남천점에서 인수 당일 바로</a> 오시는 분이 많습니다.</p>
                    </div>
                </div>
            </div>

            <div class="ar-block">
                <h2>벤츠 차급과 금액</h2>
                <p>시공 금액은 차급으로 정해집니다. 벤츠는 대략 아래와 같이 나뉩니다.
                    금액은 <a href="/price" class="gradient-text">단가표</a>에 7개 차급 전부 공개되어 있고,
                    차종을 고르면 예상 금액이 바로 나오는 계산기도 있습니다.</p>
                <table class="ar-table">
                    <thead><tr><th scope="col">차급</th><th scope="col">해당 모델</th></tr></thead>
                    <tbody>
                        <tr><th scope="row">수입중형</th><td>C클래스 · CLA · GLA · GLB</td></tr>
                        <tr><th scope="row">수입대형</th><td>E클래스 · CLE · CLS · GLC · GLE · GLS · S클래스 · G클래스 · 마이바흐</td></tr>
                    </tbody>
                </table>
                <div class="ar-cta">
                    <a href="/price" class="btn btn-primary">차급별 금액 보기 →</a>
                </div>
            </div>

            <div class="ar-block">
                <h2>어떤 코팅제를 올리는가</h2>
                <p>쉴드광택은 코팅제를 사다 쓰지 않고 <b>직접 개발·제조</b>합니다. 목적에 따라 제품이 갈립니다.</p>
                <table class="ar-table">
                    <thead><tr><th scope="col">제품</th><th scope="col">특화</th></tr></thead>
                    <tbody>
                        <tr><th scope="row"><a href="/products#f5" class="gradient-text">F5</a></th>
                            <td>색감의 깊이와 글로시함. 검정·유채색 도장에서 차이가 큽니다.</td></tr>
                        <tr><th scope="row"><a href="/products#gpro" class="gradient-text">G-PRO</a></th>
                            <td>경도가 높은 하드코팅. 스크래치 내성과 내구성.</td></tr>
                        <tr><th scope="row"><a href="/products#gtop" class="gradient-text">G-TOP</a></th>
                            <td>발수·방오. 물때와 오염 부착을 줄입니다.</td></tr>
                    </tbody>
                </table>
                <div class="ar-cta">
                    <a href="/coating-layers" class="btn btn-outline">층이 올라가는 순서 보기 →</a>
                    <a href="/certificates" class="btn btn-outline">내 차 시공증명서 조회 →</a>
                </div>
            </div>

            <div class="ar-block">
                <h2>모델별 시공 사례</h2>
                <p>차종이 겹치지 않게 최근 기록을 골랐습니다.</p>
{cards}
            </div>

            <div class="ar-block">
                <h2>자주 묻는 질문</h2>
{faq}
                <div class="ar-cta">
                    <a href="/faq" class="btn btn-outline">전체 FAQ 보기 →</a>
                </div>
            </div>

            <div class="ar-block">
                <h2>찾으시는 키워드</h2>
{tags}
            </div>

{cta}""".format(
        total=total,
        table=model_table(rows),
        cards=cards_html(pick_variety(benz, 8)),
        faq=faq_html(faqs),
        tags=tags_html([
            ('벤츠 광택', None),
            ('벤츠 유리막코팅', None),
            ('벤츠 신차코팅', None),
            ('벤츠 남천점 코팅', '/namcheon'),
            ('E클래스 유리막코팅', None),
            ('S클래스 광택', None),
            ('GLC 유리막코팅', None),
            ('GLE 신차코팅', None),
            ('G클래스 코팅', None),
            ('마이바흐 광택', None),
            ('남천동 유리막코팅', '/namcheon'),
            ('수영구 광택', '/suyeong'),
            ('시공 단가표', '/price'),
        ]),
        cta=cta_html(
            '<p><b>벤츠 부산 남천점 공식 협력업체</b> · 신차 인수 당일 입고 가능합니다.</p>\n                    '))

    return slug, wrap(slug, title, desc, keywords, schema,
                      '벤츠 유리막코팅 · 광택', 'MERCEDES-BENZ · BUSAN', body)


def build_bmw(bmw, rows):
    slug = 'bmw'
    total = len(bmw)
    title = 'BMW 유리막코팅·광택 | 부산 · 5시리즈·X시리즈 시공기록 %d건 공개 | 쉴드광택' % total
    desc = ('부산 BMW 유리막코팅·광택 전문. 작업 일지에 공개한 BMW 시공 기록 %d건 — 520i·530i·X3·X5·X6·'
            '740i·i4·i5·iX3. 16년 경력 코팅제 개발자가 F5·G-PRO·G-TOP으로 직접 시공합니다. '
            '부산 남구 유엔로 220 · 예약 010-3384-1850' % total)
    keywords = ('BMW 광택, BMW 유리막코팅, BMW 신차코팅, 5시리즈 유리막코팅, 520i 광택, '
                'X5 유리막코팅, X3 신차코팅, 3시리즈 광택, 740i 코팅, i4 코팅, iX3 코팅, '
                '부산 BMW 코팅, 수입차 유리막코팅, 쉴드광택')
    faqs = [
        ('제 BMW는 어느 차급으로 계산됩니까?',
         '3시리즈·1시리즈·2시리즈·X1·X2는 수입중형, 5시리즈·7시리즈·8시리즈·X3 이상은 수입대형으로 '
         '봅니다. 단가표에 7개 차급 금액이 전부 공개되어 있고, 차종을 고르면 예상 금액이 바로 나오는 '
         '계산기도 있습니다.'),
        ('샤도우라인 하이그로시 트림에도 기스가 납니다. 같이 되나요?',
         '광택이 들어가는 범위에 맞춰 함께 봅니다. 피아노블랙 계열 트림은 도장면보다 무르고 잔기스가 '
         '유난히 잘 보이는 자리라, 어디까지 손댈 수 있는지는 상태를 보고 먼저 말씀드립니다.'),
        ('알파인 화이트인데 광택이 필요합니까?',
         '흰색은 잔기스가 잘 안 보이는 대신 오염 경계와 철분·물때가 드러납니다. 신차라면 연마 없이 '
         '코팅만 올리는 쪽이 맞고, 타던 차라면 기스보다 오염 제거에 공정을 씁니다. 색에 따라 처방이 '
         '달라집니다.'),
        ('i4·i5·iX3 같은 전기차도 됩니까?',
         '됩니다. 도장면 작업은 내연기관차와 다르지 않습니다. 충전 포트 주변처럼 물이 들어가면 안 되는 '
         '자리를 따로 양생하고 작업합니다.'),
        ('시공 내역이 기록으로 남습니까?',
         '모든 시공 차량에 차대번호와 코팅제 시리얼이 기재된 시공증명서를 발급합니다. 차량별로 조회하실 '
         '수 있습니다.'),
    ]
    schema = page_schema(
        slug, 'BMW 유리막코팅·광택 시공', desc, 'BMW 유리막코팅 · 광택',
        ['부산광역시', '부산 남구', '부산 수영구', '부산 해운대구'], faqs)

    body = """                <p class="ar-lead">부산에서 BMW 유리막코팅·광택을 찾으신다면, 작업 일지에 사진과 함께
                    공개한 BMW 시공 기록이 <b>{total}건</b> 있습니다. 5시리즈와 X시리즈가 가장 많고,
                    7·8시리즈와 i 시리즈 전기차까지 들어와 있습니다. 코팅제를 직접 개발·제조하는 사람이
                    직접 시공합니다.</p>

            <div class="ar-block">
                <h2>모델 계열별 공개된 시공 기록</h2>
                <p>아래 숫자는 홈페이지 작업 일지에 공개된 글을 모델 계열별로 집계한 것입니다
                    (발행 시점 자동 집계).</p>
{table}
                <div class="ar-cta">
                    <a href="/blog/" class="btn btn-outline">작업 일지 전체 보기 →</a>
                </div>
            </div>

            <div class="ar-block">
                <h2>BMW에서 특히 자주 보는 세 가지</h2>
                <div class="ar-cards">
                    <div class="ar-card">
                        <h3>하이그로시 블랙 트림</h3>
                        <p>샤도우라인·M 패키지의 피아노블랙 트림은 도장면보다 무르고, 잔기스가 유난히 잘
                            보이는 자리입니다. 그릴 테두리와 창틀 몰딩이 먼저 티가 납니다. 어디까지 손댈 수
                            있는지는 상태를 보고 먼저 말씀드립니다.</p>
                    </div>
                    <div class="ar-card">
                        <h3>어두운 색 도장의 스월</h3>
                        <p>카본 블랙·소피스토 그레이 같은 어두운 색은 조명 아래서 거미줄 같은 잔기스가
                            드러납니다. 코팅은 도장면을 덮는 것이라 이미 난 기스는 갇혀 버립니다.
                            <a href="/services#polish" class="gradient-text">광택으로 먼저 정리</a>한 뒤
                            코팅을 올리는 순서여야 합니다.</p>
                    </div>
                    <div class="ar-card">
                        <h3>i 시리즈 전기차</h3>
                        <p>도장면 작업 자체는 내연기관차와 다르지 않습니다. 다만 충전 포트 주변처럼 물이
                            들어가면 안 되는 자리를 따로 양생하고 작업합니다.
                            i4 · i5 · iX3 모두 시공 기록이 있습니다.</p>
                    </div>
                </div>
            </div>

            <div class="ar-block">
                <h2>BMW 차급과 금액</h2>
                <p>시공 금액은 차급으로 정해집니다. BMW는 대략 아래와 같이 나뉩니다.
                    금액은 <a href="/price" class="gradient-text">단가표</a>에 7개 차급 전부 공개되어 있고,
                    차종을 고르면 예상 금액이 바로 나오는 계산기도 있습니다.</p>
                <table class="ar-table">
                    <thead><tr><th scope="col">차급</th><th scope="col">해당 모델</th></tr></thead>
                    <tbody>
                        <tr><th scope="row">수입중형</th><td>1 · 2 · 3 · 4 시리즈 · X1 · X2</td></tr>
                        <tr><th scope="row">수입대형</th><td>5 · 7 · 8 시리즈 · X3 · X5 · X6 · X7 · XM · i5</td></tr>
                    </tbody>
                </table>
                <div class="ar-cta">
                    <a href="/price" class="btn btn-primary">차급별 금액 보기 →</a>
                </div>
            </div>

            <div class="ar-block">
                <h2>어떤 코팅제를 올리는가</h2>
                <p>쉴드광택은 코팅제를 사다 쓰지 않고 <b>직접 개발·제조</b>합니다. 목적에 따라 제품이 갈립니다.</p>
                <table class="ar-table">
                    <thead><tr><th scope="col">제품</th><th scope="col">특화</th></tr></thead>
                    <tbody>
                        <tr><th scope="row"><a href="/products#f5" class="gradient-text">F5</a></th>
                            <td>색감의 깊이와 글로시함. 카본 블랙 같은 어두운 색에서 차이가 큽니다.</td></tr>
                        <tr><th scope="row"><a href="/products#gpro" class="gradient-text">G-PRO</a></th>
                            <td>경도가 높은 하드코팅. 스크래치 내성과 내구성.</td></tr>
                        <tr><th scope="row"><a href="/products#gtop" class="gradient-text">G-TOP</a></th>
                            <td>발수·방오. 물때와 오염 부착을 줄입니다.</td></tr>
                    </tbody>
                </table>
                <div class="ar-cta">
                    <a href="/coating-layers" class="btn btn-outline">층이 올라가는 순서 보기 →</a>
                    <a href="/certificates" class="btn btn-outline">내 차 시공증명서 조회 →</a>
                </div>
            </div>

            <div class="ar-block">
                <h2>모델별 시공 사례</h2>
                <p>차종이 겹치지 않게 최근 기록을 골랐습니다.</p>
{cards}
            </div>

            <div class="ar-block">
                <h2>자주 묻는 질문</h2>
{faq}
                <div class="ar-cta">
                    <a href="/faq" class="btn btn-outline">전체 FAQ 보기 →</a>
                </div>
            </div>

            <div class="ar-block">
                <h2>찾으시는 키워드</h2>
{tags}
            </div>

{cta}""".format(
        total=total,
        table=model_table(rows),
        cards=cards_html(pick_variety(bmw, 8, 'bmw')),
        faq=faq_html(faqs),
        tags=tags_html([
            ('BMW 광택', None),
            ('BMW 유리막코팅', None),
            ('BMW 신차코팅', None),
            ('5시리즈 유리막코팅', None),
            ('X5 유리막코팅', None),
            ('X3 신차코팅', None),
            ('3시리즈 광택', None),
            ('i4 · i5 코팅', None),
            ('부산 수입차 코팅', '/services#coating'),
            ('벤츠 유리막코팅', '/benz'),
            ('수영구 광택', '/suyeong'),
            ('대연동 광택', '/daeyeon'),
            ('시공 단가표', '/price'),
        ]),
        cta=cta_html())

    return slug, wrap(slug, title, desc, keywords, schema,
                      'BMW 유리막코팅 · 광택', 'BMW · BUSAN', body)


def build_daeyeon(posts):
    slug = 'daeyeon'
    title = '대연동 광택·유리막코팅 | 유엔로 220 대원관 1층 | 쉴드광택'
    desc = ('부산 대연동 자동차 광택·유리막코팅. 유엔로 220 대원관 1층, 유엔기념공원 맞은편입니다. '
            '용호동·문현동·감만동·우암동에서도 10분 안쪽. 16년 경력 코팅제 개발자가 F5·G-PRO·G-TOP으로 '
            '직접 시공합니다 · 예약 010-3384-1850')
    keywords = ('대연동 광택, 대연동 유리막코팅, 대연동 신차코팅, 용호동 광택, 문현동 유리막코팅, '
                '감만동 광택, 우암동 유리막코팅, 유엔로 광택, 경성대 부경대 광택, 대연동 세차 코팅, '
                '쉴드광택')
    faqs = [
        ('정확히 어디에 있습니까?',
         '부산 남구 유엔로 220, 대원관 1층입니다. 대연동이고 유엔기념공원 바로 근처입니다. '
         '내비게이션에 "쉴드광택" 또는 "유엔로 220"으로 찍으시면 됩니다.'),
        ('그냥 지나가다 들러서 봐주실 수 있습니까?',
         '차 상태를 보고 무엇이 필요한지 말씀드리는 것은 들러주시면 됩니다. 다만 시공은 차를 세워두고 '
         '하는 작업이라 일정이 잡혀 있을 때가 많습니다. 전화 한 통 주시고 오시면 기다리지 않으십니다.'),
        ('대연동에서 주차는 어떻게 합니까?',
         '작업장 앞에 차를 대실 수 있습니다. 상담만 보실 때도 잠깐 대 두시면 됩니다.'),
        ('용호동·문현동에서도 가깝습니까?',
         '용호동·문현동·감만동·우암동 모두 차로 10분 안쪽입니다. 남구 안이라면 어디서 오셔도 멀다고 '
         '할 거리가 아닙니다.'),
    ]
    schema = page_schema(
        slug, '대연동 자동차 광택·유리막코팅', desc, '자동차 유리막코팅 · 광택',
        ['대연동', '용호동', '문현동', '감만동', '우암동', '부산 남구'], faqs)

    body = """                <p class="ar-lead">쉴드광택 작업장이 <b>대연동에 있습니다.</b>
                    부산 남구 유엔로 220, 대원관 1층 — 유엔기념공원 근처입니다.
                    동네 차는 멀리 맡길 이유가 없습니다. 차 상태만 보여주셔도 무엇이 필요한지
                    그 자리에서 말씀드립니다.</p>

            <div class="ar-block">
                <h2>오시는 길</h2>
                <table class="ar-table">
                    <thead><tr><th scope="col">항목</th><th scope="col">내용</th></tr></thead>
                    <tbody>
                        <tr><th scope="row">주소</th>
                            <td><b>부산 남구 유엔로 220, 대원관 1층(대연동)</b><br>
                                내비게이션에 "쉴드광택" 또는 "유엔로 220"</td></tr>
                        <tr><th scope="row">영업시간</th>
                            <td>평일 09:00–18:00 / 토요일 09:00–16:00 · 일요일 휴무</td></tr>
                        <tr><th scope="row">주차</th>
                            <td>작업장 앞에 대실 수 있습니다. 상담만 보실 때도 잠깐 대 두시면 됩니다.</td></tr>
                        <tr><th scope="row">가까운 동네</th>
                            <td>용호동 · 문현동 · 감만동 · 우암동 모두 차로 10분 안쪽.
                                <a href="/suyeong" class="gradient-text">수영구</a>·<a href="/namcheon" class="gradient-text">남천동</a>에서도 10~15분입니다.</td></tr>
                    </tbody>
                </table>
            </div>

            <div class="ar-block">
                <h2>가까우면 뭐가 다른가</h2>
                <div class="ar-cards">
                    <div class="ar-card">
                        <h3>차를 직접 보고 정합니다</h3>
                        <p>사진으로는 잔기스 깊이가 안 보입니다. 가까우시면 차를 한 번 보여주시고 정하면
                            됩니다. 광택이 필요한 차인지, 코팅만 올리면 되는 차인지는 조명 아래서 봐야
                            압니다.</p>
                    </div>
                    <div class="ar-card">
                        <h3>맡기고 걸어가실 수 있습니다</h3>
                        <p>유리막코팅은 도포 후 경화 시간이 필요해 보통 하루 맡기시게 됩니다.
                            동네면 차를 두고 걸어가셨다가 다음 날 찾아가시면 됩니다.</p>
                    </div>
                    <div class="ar-card">
                        <h3>시공 후에도 봐 드립니다</h3>
                        <p>코팅은 올리고 끝이 아닙니다. 몇 달 지나 발수가 어떤지, 어디가 상했는지
                            지나는 길에 들러 보여주시면 확인해 드립니다.</p>
                    </div>
                </div>
            </div>

            <div class="ar-block">
                <h2>대연동에서 받으실 수 있는 시공</h2>
                <table class="ar-table">
                    <thead><tr><th scope="col">시공</th><th scope="col">내용</th></tr></thead>
                    <tbody>
                        <tr><th scope="row"><a href="/services#coating" class="gradient-text">신차 유리막코팅</a></th>
                            <td>F5 · G-PRO · G-TOP 중 차량 상태와 목적에 맞춰 선택.</td></tr>
                        <tr><th scope="row"><a href="/services#polish" class="gradient-text">광택 + 듀얼코팅</a></th>
                            <td>타던 차의 잔기스·스월·물때를 걷어낸 뒤 코팅 2층 마무리.</td></tr>
                        <tr><th scope="row"><a href="/services#oilfilm" class="gradient-text">유막제거 · 초발수</a></th>
                            <td>야간 빛 번짐, 비 오는 날 와이퍼 자국.</td></tr>
                        <tr><th scope="row"><a href="/services#moulding" class="gradient-text">알루미늄 도어몰딩 복원</a></th>
                            <td>하얗게 일어난 몰딩을 교체 대신 복원.</td></tr>
                        <tr><th scope="row"><a href="/services#seat" class="gradient-text">가죽 시트코팅</a></th>
                            <td>오염·이염이 자리 잡기 전에 처리.</td></tr>
                        <tr><th scope="row"><a href="/services#ac" class="gradient-text">에바크리닝</a></th>
                            <td>에어컨에서 냄새가 올라올 때.</td></tr>
                    </tbody>
                </table>
                <div class="ar-cta">
                    <a href="/price" class="btn btn-outline">차급별 금액 전체 보기 →</a>
                </div>
            </div>

            <div class="ar-block">
                <h2>여기서 만든 코팅제로 시공합니다</h2>
                <p>남의 제품을 사다 바르는 곳이 아닙니다. 화학공학을 전공한 대표가 16년간
                    <a href="/products" class="gradient-text">F5 · G-PRO · G-TOP</a>을 직접 개발·제조해 왔습니다.
                    모든 시공 차량에 차대번호와 코팅제 시리얼이 기재된
                    <a href="/certificates" class="gradient-text">시공증명서</a>를 발급합니다.</p>
                <div class="ar-cta">
                    <a href="/coating-layers" class="btn btn-outline">코팅이 올라가는 순서 보기 →</a>
                    <a href="/about" class="btn btn-outline">회사 소개 →</a>
                </div>
            </div>

            <div class="ar-block">
                <h2>최근 작업 일지</h2>
{cards}
                <div class="ar-cta">
                    <a href="/blog/" class="btn btn-outline">작업 일지 전체 보기 →</a>
                </div>
            </div>

            <div class="ar-block">
                <h2>자주 묻는 질문</h2>
{faq}
            </div>

            <div class="ar-block">
                <h2>찾으시는 키워드</h2>
{tags}
            </div>

{cta}""".format(
        cards=cards_html(posts[:6]),
        faq=faq_html(faqs),
        tags=tags_html([
            ('대연동 광택', None),
            ('대연동 유리막코팅', None),
            ('대연동 신차코팅', None),
            ('용호동 광택', None),
            ('문현동 유리막코팅', None),
            ('감만동 광택', None),
            ('우암동 유리막코팅', None),
            ('수영구 광택', '/suyeong'),
            ('남천동 유리막코팅', '/namcheon'),
            ('벤츠 광택', '/benz'),
            ('BMW 유리막코팅', '/bmw'),
            ('시공 단가표', '/price'),
        ]),
        cta=cta_html())

    return slug, wrap(slug, title, desc, keywords, schema,
                      '대연동 자동차 광택 · 유리막코팅', 'DAEYEON-DONG · BUSAN', body)


def main():
    posts = load_posts()
    if not posts:
        print('[gen_area_pages] 블로그 글을 찾지 못했습니다. 페이지를 건드리지 않습니다.')
        return
    benz, benz_rows = brand_stats(posts, 'benz', BENZ_GROUPS)
    bmw, bmw_rows = brand_stats(posts, 'bmw', BMW_GROUPS)
    if not benz or not bmw:
        print('[gen_area_pages] 브랜드 글을 찾지 못했습니다. 페이지를 건드리지 않습니다.')
        return

    pages = [
        build_suyeong(posts),
        build_namcheon(posts, benz),
        build_daeyeon(posts),
        build_benz(benz, benz_rows),
        build_bmw(bmw, bmw_rows),
    ]
    for slug, html in pages:
        out = os.path.join(ROOT, slug + '.html')
        io.open(out, 'w', encoding='utf-8', newline='\n').write(html)
        print('[gen_area_pages] %-13s %6d bytes' % (slug + '.html', len(html.encode('utf-8'))))

    print('[gen_area_pages] 전체 글 %d편 기준' % len(posts))
    for name, rows, n in (('벤츠', benz_rows, len(benz)), ('BMW', bmw_rows, len(bmw))):
        print('  %s %d건' % (name, n))
        for label, _eg, c in rows:
            print('     %-16s %3d' % (label, c))


if __name__ == '__main__':
    main()
