# -*- coding: utf-8 -*-
"""
쉴드광택 블로거 자동 발행 스크립트 (실전판 v5)
================================================
v5 변경점:
  - 파일명 없이 실행하면 blog 폴더의 '가장 최근 글'을 자동 선택
  - (v4 기능 유지) 라벨 자동부착, 메뉴/로고/footer 제거, 사진처리

사용법:
  py post_html.py                  → blog 폴더 가장 최근 글을 초안으로 발행
  py post_html.py --publish        → blog 폴더 가장 최근 글을 바로 공개 발행
  py post_html.py blog\파일명.html → 특정 파일 지정해서 발행 (기존 방식도 유지)

만든이: 자비스 (최한중 대표님 전용)
"""

import os
import re
import sys
import glob

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# ───────────────────────────────────────────────
# 기본 설정
# ───────────────────────────────────────────────
BLOG_ID = "1250358417825670412"
HOMEPAGE = "https://www.shiled-line.com"
BLOG_FOLDER = "blog"   # 글이 들어있는 폴더 (스크립트 기준 상대경로)
SCOPES = ["https://www.googleapis.com/auth/blogger"]
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENT_SECRET = os.path.join(SCRIPT_DIR, "client_secret.json")
TOKEN_FILE = os.path.join(SCRIPT_DIR, "token.json")
PUBLISHED_LOG = os.path.join(SCRIPT_DIR, "published.txt")  # 이미 올린 글 기록

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
    ("벤츠",        ["벤츠", "benz", "mercedes", "e350", "e클래스", "glc", "gle", "c클래스", "s클래스"]),
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
        return f'{attr}={quote}{HOMEPAGE}/{clean}{quote}'
    return re.sub(r'(src)=(["\'])([^"\']+)\2', repl, html, flags=re.IGNORECASE)


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


def publish(html_path, draft=True):
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
    result = service.posts().insert(blogId=BLOG_ID, body=post, isDraft=draft).execute()

    # 발행 기록 남기기 (어떤 파일 올렸는지)
    with open(PUBLISHED_LOG, "a", encoding="utf-8") as logf:
        logf.write(os.path.basename(full_path) + "\t" + (result.get("url") or "") + "\n")

    print("\n" + "=" * 50)
    print("✅ 발행 완료!")
    print(f"   파일 : {os.path.basename(full_path)}")
    print(f"   제목 : {result.get('title')}")
    print(f"   사진 : {img_count}장 (크기 자동조절)")
    print(f"   라벨 : {', '.join(labels)}")
    print(f"   주소 : {result.get('url')}")
    print("   상태 : " + ("초안(임시저장)" if draft else "공개 발행됨"))
    print("=" * 50)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    is_draft = "--publish" not in sys.argv

    if args:
        # 파일명을 직접 지정한 경우
        target = args[0]
    else:
        # 파일명 없으면 → 가장 최근 글 자동 선택
        target = find_latest_html()
        if not target:
            print("[오류] blog 폴더에서 글(html)을 찾지 못했습니다.")
            sys.exit(1)
        print(f"[자동선택] 가장 최근 글: {os.path.basename(target)}")

    publish(target, draft=is_draft)
