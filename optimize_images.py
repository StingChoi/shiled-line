# -*- coding: utf-8 -*-
r"""
assets/images 최적화 — 리사이즈 + JPG 재압축 + WebP 생성
================================================================
왜 필요했나
  원본이 폰에서 바로 넣은 4080x3060 짜리가 섞여 있어 한 장에 1.2MB씩 나갔다.
  화면에서는 길어야 1600px 로 보이는데 4080px 를 내려받게 하고 있었다.
  모바일에서 3초를 넘기면 이탈이 급증하고, 페이지 속도는 검색 순위에도 들어간다.

무엇을 하나
  1) 긴 변을 MAX_EDGE 로 줄인다 (이미 작으면 건드리지 않는다)
  2) JPG 를 품질 82 · 프로그레시브로 다시 저장한다
  3) 같은 이름의 .webp 를 만든다 (품질 80)
     → HTML 에서 <picture> 로 webp 를 먼저 주고 jpg 를 폴백으로 남긴다

주의
  · 원본을 덮어쓴다. 되돌리려면 git 이력에서 꺼내면 된다.
  · price_list.jpg 는 표에 글자가 있어 줄이지 않는다(가독성 우선, 품질만 올림).
  · 이미 최적화된 파일은 건너뛴다(--force 로 강제).

사용
  py optimize_images.py --dry-run     무엇을 얼마나 줄일지 미리보기
  py optimize_images.py               실제 실행
"""
import os
import sys
import argparse

from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'images')
MAX_EDGE = 1600
JPG_Q = 82
WEBP_Q = 80
SKIP_RESIZE = {'price_list.jpg'}          # 글자가 있는 이미지는 줄이지 않는다
MIN_BYTES = 60 * 1024                     # 60KB 미만은 손대지 않는다


def walk():
    for base, _, files in os.walk(ROOT):
        for f in files:
            if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                yield os.path.join(base, f)


def human(n):
    return f'{n / 1024:,.0f}KB'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--force', action='store_true')
    a = ap.parse_args()

    before_total = after_total = webp_total = 0
    touched = skipped = 0

    for path in sorted(walk()):
        name = os.path.basename(path)
        size0 = os.path.getsize(path)
        before_total += size0

        if size0 < MIN_BYTES and not a.force:
            after_total += size0
            skipped += 1
            continue

        try:
            im = Image.open(path)
        except Exception as e:
            print(f'  ! 열기 실패 {name}: {e}')
            after_total += size0
            continue

        im = im.convert('RGB')
        w0, h0 = im.size

        if name not in SKIP_RESIZE and max(w0, h0) > MAX_EDGE:
            r = MAX_EDGE / max(w0, h0)
            im = im.resize((round(w0 * r), round(h0 * r)), Image.LANCZOS)

        webp_path = os.path.splitext(path)[0] + '.webp'

        if a.dry_run:
            print(f'  {name:34s} {w0}x{h0} → {im.size[0]}x{im.size[1]}  {human(size0)}')
            after_total += size0
            continue

        # JPG/PNG 는 확장자 유지한 채 다시 저장
        if path.lower().endswith('.png'):
            im.save(path, 'PNG', optimize=True)
        else:
            im.save(path, 'JPEG', quality=JPG_Q, optimize=True, progressive=True)
        im.save(webp_path, 'WEBP', quality=WEBP_Q, method=5)

        size1 = os.path.getsize(path)
        sizew = os.path.getsize(webp_path)
        after_total += size1
        webp_total += sizew
        touched += 1
        print(f'  {name:34s} {w0}x{h0}→{im.size[0]}x{im.size[1]}  '
              f'{human(size0)} → {human(size1)} / webp {human(sizew)}')

    print()
    print(f'  처리 {touched}개 / 건너뜀 {skipped}개')
    print(f'  원본 합계 {before_total/1048576:.1f}MB → JPG {after_total/1048576:.1f}MB'
          + ('' if a.dry_run else f' (+ WebP {webp_total/1048576:.1f}MB)'))
    if not a.dry_run and before_total:
        print(f'  WebP 기준 절감률 {100 * (1 - (webp_total or after_total) / before_total):.0f}%')


if __name__ == '__main__':
    main()
