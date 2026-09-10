# -*- coding: utf-8 -*-
"""블로그 글마다 '이 시공에 쓴 것' 줄을 단다 — 제품 페이지·서비스 페이지로 가는 링크.

관련 시공 사례(글↔글)는 이미 있는데, 글에서 제품·서비스 소개로 내려가는
길이 없었다. 검색으로 들어온 사람이 "F5가 뭔데?"를 물을 곳이 없던 셈이다.
슬러그와 제목에서 코팅제·시공 종류를 읽어 알맞은 항목 앵커로 보낸다.

재실행 안전: 이미 줄이 있는 글은 건너뛴다.
"""
import io, re, glob, sys, os

PRODUCT = {   # 키워드 → (앵커, 표시문구). 앞에 있는 것이 우선.
    'gtop':   ('/products#gtop', 'G-TOP 유리막코팅제'),
    'g-top':  ('/products#gtop', 'G-TOP 유리막코팅제'),
    'gpro':   ('/products#gpro', 'G-PRO 유리막코팅제'),
    'g-pro':  ('/products#gpro', 'G-PRO 유리막코팅제'),
    'f5':     ('/products#f5',   'F5 유리막코팅제'),
    'ralu':   ('/products#ralu', 'R-Alu 몰딩 복원코팅제'),
    'r-alu':  ('/products#ralu', 'R-Alu 몰딩 복원코팅제'),
}
MULTI = ('dual', 'triple', '듀얼', '트리플')   # 둘 이상 겹칠 땐 라인업 전체로

SERVICE = [   # (판별 키워드들, 앵커, 표시문구). 위에서부터 첫 매치.
    (('softtop', 'soft-top', 'cabrio', '소프트탑'),       '/services#softtop',  '소프트탑 코팅'),
    (('seat', '시트코팅', '시트 코팅'),                   '/services#seat',     '가죽 시트 코팅'),
    (('moulding', 'molding', 'ralu', '몰딩'),             '/services#moulding', '알루미늄 몰딩 복원'),
    (('oilfilm', 'oil-film', 'glass', '유막'),            '/services#oilfilm',  '유막 제거'),
    (('overspray', 'polish', '광택', '스월', '오버스프레이'), '/services#polish', '프리미엄 광택'),
    (('coating', '코팅'),                                 '/services#coating',  '유리막 코팅'),
]

MARK = 'class="rl-used"'

def pick(slug, title):
    # 제목 끝의 '| 쉴드광택' 브랜드 접미사는 판별에서 뺀다.
    # 안 빼면 모든 글이 '광택'에 걸려 전부 프리미엄 광택으로 분류된다.
    title = re.sub(r'\s*\|[^|]*쉴드광택\s*$', '', title)   # '| 쉴드광택', '| 부산 쉴드광택' 둘 다
    hay = (slug + ' ' + title).lower()
    prod = None
    if any(k in hay for k in MULTI):
        prod = ('/products', 'F5·G-PRO·G-TOP 라인업')
    else:
        for k, v in PRODUCT.items():
            if k in hay:
                prod = v; break
    svc = None
    for keys, href, label in SERVICE:
        if any(k in hay for k in keys):
            svc = (href, label); break
    if svc and svc[0].endswith('#moulding') and not prod:
        prod = PRODUCT['ralu']          # 몰딩 복원은 곧 R-Alu 시공이다
    return prod, svc

def main():
    done = skipped = noprod = 0
    for f in sorted(glob.glob('blog/*.html')):
        if os.path.basename(f) == 'index.html': continue
        s = io.open(f, encoding='utf-8').read()
        if MARK in s: skipped += 1; continue
        m = re.search(r'<title>([^<]*)', s)
        title = m.group(1) if m else ''
        slug = os.path.basename(f)[:-5]
        prod, svc = pick(slug, title)
        parts = []
        if prod: parts.append('<a href="%s">%s</a>' % prod)
        else: noprod += 1
        if svc:  parts.append('<a href="%s">%s</a>' % svc)
        if not parts: continue
        line = ('        <p class="rl-used"><span>이 시공에 쓴 것</span> '
                + ' <em>&middot;</em> '.join(parts) + '</p>\n')
        # 관련 시공 사례 목록(</ul>) 바로 뒤, 박스 닫히기 전에 넣는다
        s2, c = re.subn(r'(<div class="related">.*?</ul>\n)', lambda mm: mm.group(1) + line, s, count=1, flags=re.S)
        if not c:
            print('  !! related 블록 없음:', f); continue
        io.open(f, 'w', encoding='utf-8').write(s2); done += 1
    print('[link_products] 삽입 %d / 이미 있음 %d / 제품 못 정한 글 %d' % (done, skipped, noprod))

if __name__ == '__main__':
    sys.exit(main())
