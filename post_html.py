# -*- coding: utf-8 -*-
"""
쉴드광택 블로거 자동 발행 스크립트 (실전판 v6)
================================================
v6 변경점:
  - `--all` : 아직 안 올린 글을 한 번에 전부 발행 (밀린 것 일괄)
              + 시차발행(1번 즉시, 2번 +2시간, 3번 +4시간 ...) = 블로거 예약발행
  - 영상: <video data-yt=...> 가 있으면 블로거엔 유튜브 임베드로 교체, 없으면 poster 사진
  - 사진/영상 경로(images/·compare/·videos/)를 전체 URL로 변환, poster도 변환

사용법:
  py post_html.py                  → 가장 최근 글을 초안으로 발행
  py post_html.py --publish        → 가장 최근 글을 바로 공개 발행
  py post_html.py blog\파일.html   → 특정 파일 초안 발행
  py post_html.py --all            → 안 올린 글 전부, 2시간 간격 예약발행

만든이: 자비스 (최한중 대표님 전용)
"""

import os
import re
import sys
import glob
from datetime import datetime, timedelta, timezone

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# ───────────────────────────────────────────────
# 기본 설정
# ───────────────────────────────────────────────
BLOG_ID = "1250358417825670412"
HOMEPAGE = "https://www.shiled-line.com"
BLOG_FOLDER = "blog"
SCOPES = ["https://www.googleapis.com/auth/blogger"]
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENT_SECRET = os.path.join(SCRIPT_DIR, "client_secret.json")
TOKEN_FILE = os.path.join(SCRIPT_DIR, "token.json")
PUBLISHED_LOG = os.path.join(SCRIPT_DIR, "published.txt")

IMG_STYLE = "max-width:100%;height:auto;display:block;margin:14px auto;"

ALWAYS_LABELS = ["쉴드광택", "작업일지"]
LABEL_RULES = [
    ("광택",        ["광택", "폴리싱", "스월", "잔기스", "컴파운드"]),
    ("유리막코팅",  ["유리막코팅", "유리막 코팅", "g-pro", "g-top", "f5"]),
    ("듀얼코팅",    ["듀얼코팅", "듀얼 코팅"]),
    ("트리플코팅",  ["트리플코팅", "트리플 코팅"]),
    ("도어몰딩복원", ["도어몰딩", "몰딩복원", "몰딩 복원", "알루미늄 몰딩"]),
    ("시트코팅",    ["시트코팅", "시트 코팅", "가죽코팅"]),
    ("PPF",         ["ppf", "보호필름"]),
    ("벤츠",        ["벤츠", "benz", "mercedes", "e350", "e클래스", "glc", "gle", "glb", "c클래스", "s클래스"]),
    ("BMW",         ["bmw", "x6", "x5", "5시리즈", "3시리즈"]),
    ("아우디",      ["아우디", "audi"]),
    ("포드",        ["포드", "ford", "f150", "f-150", "익스플로러"]),
    ("테슬라",      ["테슬라", "tesla"]),
    ("국산차",      ["현대", "기아", "제네시스", "그랜저", "쏘렌토", "g80"]),
    ("부산",        ["부산", "남구", "쉴드광택"]),
]
TITLE_ONLY_RULES = [("신차코팅", ["신차", "출고"])]


def find_latest_html():
    """blog 폴더에서 가장 최근 수정된 글 html 찾기 (index.html 제외)."""
    folder = os.path.join(SCRIPT_DIR, BLOG_FOLDER)
    files = glob.glob(os.path.join(folder, "*.html"))
    files = [f for f in files if os.path.basename(f).lower() != "index.html"]
    if not files:
        return None
    return max(files, key=os.path.getmtime)


def published_basenames():
    """published.txt에 기록된, 이미 블로거에 올린 글 파일명 집합."""
    done = set()
    if os.path.exists(PUBLISHED_LOG):
        with open(PUBLISHED_LOG, "r", encoding="utf-8") as f:
            for line in f:
                b = line.split("\t")[0].strip()
                if b:
                    done.add(b)
    return done


def find_unpublished_htmls():
    """아직 블로거에 안 올린 글들(오래된 순). index.html 제외."""
    folder = os.path.join(SCRIPT_DIR, BLOG_FOLDER)
    files = [f for f in glob.glob(os.path.join(folder, "*.html"))
             if os.path.basename(f).lower() != "index.html"]
    done = published_basenames()
    files = [f for f in files if os.path.basename(f) not in done]
    files.sort(key=os.path.getmtime)   # 오래된 것부터
    return files


def get_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CLIENT_SECRET):
                print("[오류] client_secret.json 파일을 찾을 수 없습니다.")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w", encoding="utf-8") as f:
            f.write(creds.to_json())
    return build("blogger", "v3", credentials=creds)


def detect_labels(title, full_text):
    tl, xl = title.lower(), full_text.lower()
    r = list(ALWAYS_LABELS)
    for lab, kws in LABEL_RULES:
        if any(k.lower() in xl for k in kws) and lab not in r:
            r.append(lab)
    for lab, kws in TITLE_ONLY_RULES:
        if any(k.lower() in tl for k in kws) and lab not in r:
            r.append(lab)
    return r


def extract_title(html):
    m = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    if m:
        t = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        if t:
            return t
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.IGNORECASE | re.DOTALL)
    if m:
        t = re.sub(r"<[^>]+>", " ", m.group(1)).strip()
        return re.sub(r"\s+", " ", t) or "쉴드광택 블로그 글"
    return "쉴드광택 블로그 글"


def extract_hero_heading(html):
    m = re.search(r'<header[^>]*class="[^"]*post-hero[^"]*"[^>]*>(.*?)</header>',
                  html, re.IGNORECASE | re.DOTALL)
    if not m:
        return ""
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", m.group(1), re.IGNORECASE | re.DOTALL)
    return f"<h2>{h1.group(1)}</h2>" if h1 else ""


def extract_article(html):
    m = re.search(r'<article[^>]*>(.*?)</article>', html, re.IGNORECASE | re.DOTALL)
    if m:
        return m.group(1)
    bm = re.search(r"<body[^>]*>(.*?)</body>", html, re.IGNORECASE | re.DOTALL)
    body = bm.group(1) if bm else html
    body = re.sub(r'<div[^>]*class="[^"]*site-top[^"]*"[^>]*>.*?</div>',
                  "", body, flags=re.IGNORECASE | re.DOTALL)
    body = re.sub(r'<footer[^>]*>.*?</footer>', "", body, flags=re.IGNORECASE | re.DOTALL)
    return body


def remove_back_links(html):
    return re.sub(r'<a[^>]*class="[^"]*back-link[^"]*"[^>]*>.*?</a>',
                  "", html, flags=re.IGNORECASE | re.DOTALL)


def fix_image_paths(html):
    def repl(match):
        attr, quote, path = match.group(1), match.group(2), match.group(3).strip()
        if path.startswith(("http://", "https://", "data:", "//")):
            return match.group(0)
        clean = path.lstrip("./").lstrip("/").replace("../", "")
        if clean.startswith("images/"):
            clean = "blog/" + clean
        elif clean.startswith("compare/"):
            clean = "blog/" + clean
        elif clean.startswith("videos/"):
            clean = "blog/" + clean
        return f'{attr}={quote}{HOMEPAGE}/{clean}{quote}'
    # src(이미지·영상·소스)와 poster(영상 썸네일) 경로를 절대주소로 변환
    return re.sub(r'(src|poster)=(["\'])([^"\']+)\2', repl, html, flags=re.IGNORECASE)


def make_images_responsive(html):
    def add_style(m):
        tag = m.group(0)
        sm = re.search(r'style=(["\'])(.*?)\1', tag, re.IGNORECASE)
        if sm:
            return tag[:sm.start()] + f'style="{sm.group(2).rstrip(";")};{IMG_STYLE}"' + tag[sm.end():]
        return re.sub(r'\s*/?>$', f' style="{IMG_STYLE}">', tag)
    return re.sub(r'<img\b[^>]*>', add_style, html, flags=re.IGNORECASE)


def strip_onerror(html):
    return re.sub(r'\s+onerror=(["\']).*?\1', "", html, flags=re.IGNORECASE)


def video_to_image_for_blogger(html):
    """블로거는 자체 호스팅 <video> 태그를 제거한다. 그래서 블로거로 보내는 본문에서만:
      1) <video>에 data-yt="유튜브ID"가 있으면 → 유튜브 iframe(실제 재생)으로 교체
      2) 없으면 poster 썸네일 사진으로 교체
      3) 둘 다 없으면 mp4 링크로 대체
    홈페이지 HTML은 손대지 않으므로 홈페이지는 자체 영상 그대로 재생된다."""
    def repl(m):
        tag = m.group(0)
        ytm = re.search(r'data-yt=(["\'])(.*?)\1', tag, re.IGNORECASE)
        if ytm and ytm.group(2).strip():
            vid = ytm.group(2).strip()
            return ('<div style="position:relative;padding-bottom:56.25%;height:0;margin:14px 0;">'
                    f'<iframe src="https://www.youtube.com/embed/{vid}" '
                    'style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;" '
                    'allowfullscreen></iframe></div>')
        pm = re.search(r'poster=(["\'])(.*?)\1', tag, re.IGNORECASE)
        if pm:
            return f'<img src="{pm.group(2)}" alt="확인세차 장면">'
        sm = re.search(r'<source[^>]*\ssrc=(["\'])(.*?)\1', tag, re.IGNORECASE)
        if sm:
            return f'<p><a href="{sm.group(2)}">▶ 영상 보기</a></p>'
        return ""
    return re.sub(r'<video\b[^>]*>.*?</video>', repl, html, flags=re.IGNORECASE | re.DOTALL)


def publish(html_path, draft=True, publish_at=None):
    full_path = html_path if os.path.isabs(html_path) else os.path.join(SCRIPT_DIR, html_path)
    if not os.path.exists(full_path):
        print(f"[오류] 파일을 찾을 수 없습니다: {full_path}")
        sys.exit(1)

    with open(full_path, "r", encoding="utf-8") as f:
        html = f.read()

    title = extract_title(html)
    plain_text = re.sub(r"<[^>]+>", " ", html)
    labels = detect_labels(title, plain_text)

    hero = extract_hero_heading(html)
    article = extract_article(html)
    body = hero + "\n" + article
    body = remove_back_links(body)
    body = strip_onerror(body)
    body = fix_image_paths(body)
    body = video_to_image_for_blogger(body)   # 블로거는 self-host 영상을 막으므로 유튜브/썸네일로 대체
    body = make_images_responsive(body)

    img_count = len(re.findall(r'<img\b', body, re.IGNORECASE))

    service = get_service()
    post = {
        "kind": "blogger#post",
        "blog": {"id": BLOG_ID},
        "title": title,
        "content": body,
        "labels": labels,
    }
    # publish_at(미래 시각)을 주면 블로거가 그 시각에 자동 공개(예약발행).
    # 지금 시각이면 즉시 공개. draft=False 여야 예약/공개가 동작한다.
    if publish_at:
        post["published"] = publish_at
    result = service.posts().insert(blogId=BLOG_ID, body=post, isDraft=draft).execute()

    with open(PUBLISHED_LOG, "a", encoding="utf-8") as logf:
        logf.write(os.path.basename(full_path) + "\t" + (result.get("url") or "") + "\n")

    print("\n" + "=" * 50)
    print("✅ 발행 완료!")
    print(f"   파일 : {os.path.basename(full_path)}")
    print(f"   제목 : {result.get('title')}")
    print(f"   사진 : {img_count}장 (크기 자동조절)")
    print(f"   라벨 : {', '.join(labels)}")
    print(f"   주소 : {result.get('url')}")
    if draft:
        status = "초안(임시저장)"
    elif publish_at:
        status = f"예약발행 → {publish_at} 에 자동 공개"
    else:
        status = "공개 발행됨"
    print("   상태 : " + status)
    print("=" * 50)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    is_draft = "--publish" not in sys.argv

    if "--all" in sys.argv:
        # 아직 안 올린 글 전부 발행 (밀린 것 일괄).
        # 시차발행: 1번=지금 즉시 공개, 2번=+2시간, 3번=+4시간 ... (블로거 예약발행)
        targets = find_unpublished_htmls()
        if not targets:
            print("[안내] 새로 발행할 글이 없습니다(모두 발행됨).")
            sys.exit(0)
        GAP_HOURS = 2
        KST = timezone(timedelta(hours=9))
        base = datetime.now(KST).replace(microsecond=0)
        print(f"[일괄·시차발행] 안 올린 글 {len(targets)}개를 {GAP_HOURS}시간 간격으로 공개 예약합니다.")
        for i, t in enumerate(targets):
            pub_at = (base + timedelta(hours=GAP_HOURS * i)).isoformat()
            publish(t, draft=False, publish_at=pub_at)
    elif args:
        publish(args[0], draft=is_draft)
    else:
        target = find_latest_html()
        if not target:
            print("[오류] blog 폴더에서 글(html)을 찾지 못했습니다.")
            sys.exit(1)
        print(f"[자동선택] 가장 최근 글: {os.path.basename(target)}")
        publish(target, draft=is_draft)
