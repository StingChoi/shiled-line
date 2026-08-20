# -*- coding: utf-8 -*-
r"""
홈페이지 "최신 작업 일지" 카드 자동 생성 스크립트
================================================================
blog/*.html 을 스캔해 최신 글 N편을 카드 HTML로 만들어 index.html 에 심는다.
gen_sitemap.py 와 같은 자리(auto_publish.bat)에서 호출하면 발행할 때마다 홈이 자동 갱신된다.

왜 JS가 아니라 빌드 시점에 심는가:
  홈 콘텐츠는 크롤러·AI가 읽어야 한다. JS로 나중에 그리면 안 읽힌다.
  (2026-07-06 2단계에서 홈 전체를 정적 HTML로 옮긴 것과 같은 이유)

수동 실행:  py gen_latest_posts.py
"""
import os
import re
import glob
import io

ROOT  = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(ROOT, 'index.html')
COUNT = 6                                   # 홈에 노출할 글 수

START = '<!-- LATEST_POSTS:START (gen_latest_posts.py 가 자동 생성 — 직접 고치지 말 것) -->'
END   = '<!-- LATEST_POSTS:END -->'


def read(p):
    return io.open(p, encoding='utf-8').read()


def parse_post(fp):
    """블로그 글 1편에서 카드에 필요한 정보를 뽑는다. 하나라도 없으면 None."""
    s = read(fp)

    m_title = re.search(r'<title>([^<]+)</title>', s)
    m_img   = re.search(r'og:image"\s+content="([^"]+)"', s)
    m_desc  = re.search(r'og:description"\s+content="([^"]+)"', s)
    m_date  = re.search(r'"datePublished"\s*:\s*"([^"]+)"', s)
    if not (m_title and m_img and m_desc and m_date):
        return None

    raw = m_title.group(1).strip()

    # 꼬리 브랜드 제거: "... | 부산 쉴드광택" / "... | 쉴드광택"
    raw = re.sub(r'\s*\|\s*(부산\s*)?쉴드광택\s*$', '', raw)

    # "부산 유리막코팅｜E300 F5 신차 후기" → 키워드 / 헤드라인
    if '｜' in raw:
        tag, headline = [x.strip() for x in raw.split('｜', 1)]
    else:
        tag, headline = '작업 일지', raw

    # og:image 는 절대주소 → 홈(루트)에서 쓸 상대경로로
    thumb = re.sub(r'^https?://(www\.)?shiled-line\.com/', '', m_img.group(1))

    date = m_date.group(1).strip()           # 2026-08-15
    try:
        y, mth, d = date.split('-')
        date_txt = f'{y}. {int(mth)}. {int(d)}.'
    except ValueError:
        date_txt = date

    return {
        'url':      'blog/' + os.path.basename(fp),
        'tag':      tag,
        'headline': headline,
        'summary':  m_desc.group(1).strip(),
        'thumb':    thumb,
        'date':     date,
        'date_txt': date_txt,
    }


def esc(t):
    return (t.replace('&', '&amp;').replace('<', '&lt;')
             .replace('>', '&gt;').replace('"', '&quot;'))


def build_cards(posts):
    out = [START, '                <div class="post-grid">']
    for p in posts:
        out.append(f'''                    <a class="post-card" href="/{p['url']}">
                        <span class="pc-thumb" style="background-image:url('{esc(p['thumb'])}')" aria-hidden="true"></span>
                        <span class="pc-body">
                            <span class="pc-tag">{esc(p['tag'])}</span>
                            <span class="pc-title">{esc(p['headline'])}</span>
                            <span class="pc-date">{esc(p['date_txt'])}</span>
                            <span class="pc-sum">{esc(p['summary'])}</span>
                        </span>
                    </a>''')
    out.append('                </div>')
    out.append('                ' + END)
    return '\n'.join(out)


def main():
    files = [f for f in glob.glob(os.path.join(ROOT, 'blog', '*.html'))
             if os.path.basename(f) not in ('index.html',)
             and 'zztest' not in os.path.basename(f)]

    posts = [p for p in (parse_post(f) for f in files) if p]
    # 발행일 내림차순, 같은 날이면 파일명 역순으로 안정 정렬
    posts.sort(key=lambda p: (p['date'], p['url']), reverse=True)
    latest = posts[:COUNT]

    if not latest:
        print('[gen_latest_posts] 블로그 글을 찾지 못했습니다. index.html 을 건드리지 않습니다.')
        return

    block = build_cards(latest)
    s = read(INDEX)

    if START in s and END in s:
        s = re.sub(re.escape(START) + r'.*?' + re.escape(END), lambda _: block, s, flags=re.S)
    else:
        print('[gen_latest_posts] index.html 에 마커가 없습니다. 먼저 마커를 넣어주세요.')
        print(f'  {START}')
        print(f'  {END}')
        return

    io.open(INDEX, 'w', encoding='utf-8').write(s)

    print(f'[gen_latest_posts] index.html updated: 최신 {len(latest)}편 (전체 {len(posts)}편 중)')
    for p in latest:
        print(f'   {p["date"]}  {p["tag"]}｜{p["headline"][:34]}')


if __name__ == '__main__':
    main()
