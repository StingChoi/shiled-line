# -*- coding: utf-8 -*-
"""
쉴드광택 - 블로그 영상 유튜브 자동 업로드 + data-yt 주입 (v1)
================================================================
무엇을 하나:
  - blog 폴더의 '가장 최근 글'(또는 지정한 글)에서 <video> 태그를 찾는다.
  - 그 영상의 로컬 mp4(<source src="videos/...">)가 있고, 아직 유튜브에 안 올린
    (data-yt 속성이 없는) 영상이면 → 유튜브에 업로드한다.
  - 업로드해서 받은 영상 ID를 글 HTML의 <video ...> 에 data-yt="ID" 로 박아 넣는다.
  - 그래서 다음 단계인 post_html.py(블로거 발행)가 이 ID로 유튜브 임베드를 만든다.
  - 재실행해도 이미 data-yt가 있는 영상은 건너뛴다(중복 업로드 방지).

쓰는 법:
  py upload_videos.py                 → 가장 최근 글의 영상 업로드
  py upload_videos.py blog\파일.html  → 특정 글의 영상 업로드

최초 1회: 'YouTube Data API v3' 사용 설정 + 브라우저 로그인(youtube.upload 권한) 필요.
          (유튜브_최초설정.md 참고)
"""
import os
import re
import sys
import glob

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BLOG_FOLDER = os.path.join(SCRIPT_DIR, "blog")
CLIENT_SECRET = os.path.join(SCRIPT_DIR, "client_secret.json")
YT_TOKEN = os.path.join(SCRIPT_DIR, "token_youtube.json")   # 블로거 토큰과 별도
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

HOMEPAGE = "https://www.shiled-line.com"
PRIVACY = "public"        # 공개. 미등록으로 바꾸려면 "unlisted"
CATEGORY_AUTOS = "2"      # 유튜브 카테고리: 자동차 및 차량


def get_service():
    creds = None
    if os.path.exists(YT_TOKEN):
        creds = Credentials.from_authorized_user_file(YT_TOKEN, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CLIENT_SECRET):
                print("[오류] client_secret.json 을 찾을 수 없습니다.")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(YT_TOKEN, "w", encoding="utf-8") as f:
            f.write(creds.to_json())
    return build("youtube", "v3", credentials=creds)


def find_latest_html():
    files = [f for f in glob.glob(os.path.join(BLOG_FOLDER, "*.html"))
             if os.path.basename(f).lower() != "index.html"]
    return max(files, key=os.path.getmtime) if files else None


def extract_title(html):
    m = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    if m:
        return re.sub(r"<[^>]+>", "", m.group(1)).strip()
    return "쉴드광택 작업 영상"


def upload_one(yt, filepath, title, description):
    body = {
        "snippet": {
            "title": title[:100],
            "description": description,
            "categoryId": CATEGORY_AUTOS,
        },
        "status": {
            "privacyStatus": PRIVACY,
            "selfDeclaredMadeForKids": False,
        },
    }
    media = MediaFileUpload(filepath, chunksize=-1, resumable=True)
    request = yt.videos().insert(part="snippet,status", body=body, media_body=media)
    response = None
    while response is None:
        _, response = request.next_chunk()
    return response["id"]


def process_html(full):
    if not os.path.exists(full):
        print(f"[오류] 파일을 찾을 수 없습니다: {full}")
        return

    with open(full, "r", encoding="utf-8") as f:
        html = f.read()

    post_title = extract_title(html)

    # <video>...</video> 블록과 그 뒤를 따라오는 figcap(설명) 함께 찾기
    video_blocks = list(re.finditer(r"<video\b[^>]*>.*?</video>", html, re.IGNORECASE | re.DOTALL))
    if not video_blocks:
        print("[안내] 이 글에는 영상(<video>)이 없습니다. 업로드할 것이 없습니다.")
        return

    yt = None
    n = 0
    new_html = html
    uploaded = 0
    for m in video_blocks:
        n += 1
        tag = m.group(0)

        # 이미 유튜브에 올린 영상이면 건너뜀
        if re.search(r'data-yt=(["\'])\s*\S', tag, re.IGNORECASE):
            print(f"  [{n}] 이미 유튜브에 올라간 영상 → 건너뜀")
            continue

        # 로컬 mp4 경로 찾기
        sm = re.search(r'<source[^>]*\ssrc=(["\'])(.*?)\1', tag, re.IGNORECASE)
        if not sm:
            print(f"  [{n}] mp4 소스가 없어 건너뜀")
            continue
        rel = sm.group(2).lstrip("./").lstrip("/")
        local = os.path.join(SCRIPT_DIR, "blog", rel) if rel.startswith("videos/") \
            else os.path.join(SCRIPT_DIR, rel)
        if not os.path.exists(local):
            print(f"  [{n}] mp4 파일을 못 찾음: {local} → 건너뜀")
            continue

        # 제목/설명 만들기 (뒤따라오는 figcap을 설명에 활용)
        after = html[m.end():m.end() + 300]
        cap = re.search(r'<p[^>]*class="[^"]*figcap[^"]*"[^>]*>(.*?)</p>', after, re.IGNORECASE | re.DOTALL)
        cap_text = re.sub(r"<[^>]+>", "", cap.group(1)).strip() if cap else ""
        vid_title = f"{post_title} (영상 {n})"
        desc = (f"{post_title}\n{cap_text}\n\n"
                f"부산 쉴드광택 · 자동차 광택 & 유리막코팅\n"
                f"{HOMEPAGE}\n예약·상담 010-3384-1850")

        if yt is None:
            yt = get_service()
        print(f"  [{n}] 유튜브 업로드 중: {os.path.basename(local)} ...")
        vid_id = upload_one(yt, local, vid_title, desc)
        print(f"      완료 → https://youtu.be/{vid_id}")

        # 원본 tag 의 <video 바로 뒤에 data-yt 삽입
        new_tag = re.sub(r"<video\b", f'<video data-yt="{vid_id}"', tag, count=1, flags=re.IGNORECASE)
        new_html = new_html.replace(tag, new_tag, 1)
        uploaded += 1

    if uploaded:
        with open(full, "w", encoding="utf-8") as f:
            f.write(new_html)
        print(f"\n[완료] {uploaded}개 영상 업로드 + 글에 연결했습니다: {os.path.basename(full)}")
    else:
        print("\n[안내] 새로 올린 영상이 없습니다.")


def main():
    if "--all" in sys.argv:
        files = [f for f in glob.glob(os.path.join(BLOG_FOLDER, "*.html"))
                 if os.path.basename(f).lower() != "index.html"]
        files.sort(key=os.path.getmtime)   # 오래된 것부터
        if not files:
            print("[안내] blog 폴더에 글이 없습니다.")
            return
        for full in files:
            process_html(full)
    else:
        one = next((a for a in sys.argv[1:] if not a.startswith("--")), None) or find_latest_html()
        if not one:
            print("[안내] blog 폴더에서 글(html)을 찾지 못했습니다.")
            return
        full = one if os.path.isabs(one) else os.path.join(SCRIPT_DIR, one)
        process_html(full)


if __name__ == "__main__":
    main()
