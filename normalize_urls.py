# -*- coding: utf-8 -*-
"""발행 직전 URL 표기를 통일한다.

사이트의 정본 주소는 확장자 없는 형태다(/price, /blog/글주소).
canonical·사이트맵은 그렇게 맞춰놨는데, 새 글이 만들어질 때
구조화데이터(JSON-LD)에 `.html`이 다시 섞여 들어오는 일이 있었다.
셋이 서로 다른 주소를 말하면 검색엔진이 어느 쪽이 정본인지 헷갈린다.

`.html` -> 확장자 없는 주소로의 308 리디렉션은 그대로 둔다.
밖에서 걸어둔 옛 링크를 살려두기 위해서다. 여기서 고치는 건
우리가 직접 '이게 정본이다'라고 말하는 자리뿐이다.
"""
import io, re, glob, sys

SKIP = ('blog_bak_',)          # 백업본은 건드리지 않는다
FIELDS = r'@id|url|mainEntityOfPage|item'
PAT = re.compile(
    r'("(?:%s)"\s*:\s*"https://www\.shiled-line\.com/[^"]*?)\.html(?=["#])' % FIELDS)
CANON = re.compile(
    r'(rel="canonical"\s+href="https://www\.shiled-line\.com/[^"]*?)\.html(?=")')

def main():
    files = [f for f in glob.glob('*.html') + glob.glob('blog/*.html')
             if not any(s in f for s in SKIP)]
    hits = 0
    for f in files:
        s = io.open(f, encoding='utf-8').read()
        s2, a = PAT.subn(r'\1', s)
        s2, b = CANON.subn(r'\1', s2)
        if a or b:
            io.open(f, 'w', encoding='utf-8').write(s2)
            hits += a + b
            print('  %s: %d곳' % (f, a + b))
    print('[normalize_urls] %d곳 정리' % hits)
    return 0

if __name__ == '__main__':
    sys.exit(main())
