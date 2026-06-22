# -*- coding: utf-8 -*-
"""
쉴드광택 블로거 자동 발행 스크립트
사용법:
  1) 처음 한 번: py blogger_post.py  → 구글 로그인 창이 뜸 → 허락
  2) 그 다음부터: HTML 파일 경로만 바꿔서 다시 실행하면 자동 발행

만든이: 자비스 (최한중 대표님 전용)
"""

import os
import sys

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# ───────────────────────────────────────────────
# 기본 설정 (대표님 정보가 이미 들어가 있습니다)
# ───────────────────────────────────────────────
BLOG_ID = "1250358417825670412"          # 쉴드광택 블로거 블로그 ID
SCOPES = ["https://www.googleapis.com/auth/blogger"]
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENT_SECRET = os.path.join(SCRIPT_DIR, "client_secret.json")
TOKEN_FILE = os.path.join(SCRIPT_DIR, "token.json")


def get_service():
    """구글 인증 처리. 처음엔 로그인 창, 이후엔 저장된 토큰 사용."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CLIENT_SECRET):
                print("[오류] client_secret.json 파일을 찾을 수 없습니다.")
                print("       이 스크립트와 같은 폴더에 두셨는지 확인해주세요.")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET, SCOPES)
            creds = flow.run_local_server(port=0)
        # 인증 정보 저장 (다음부턴 로그인 안 뜸)
        with open(TOKEN_FILE, "w", encoding="utf-8") as f:
            f.write(creds.to_json())

    return build("blogger", "v3", credentials=creds)


def publish_post(title, html_content, labels=None, draft=False):
    """블로거에 글 발행.
    draft=True 로 두면 '임시저장(초안)'으로만 올라가고 공개되지 않습니다.
    """
    service = get_service()
    body = {
        "kind": "blogger#post",
        "blog": {"id": BLOG_ID},
        "title": title,
        "content": html_content,
    }
    if labels:
        body["labels"] = labels

    result = service.posts().insert(
        blogId=BLOG_ID,
        body=body,
        isDraft=draft,
    ).execute()

    print("\n✅ 발행 완료!")
    print("   제목 :", result.get("title"))
    print("   주소 :", result.get("url"))
    if draft:
        print("   (초안으로 저장됨 - 블로거에서 직접 '게시' 눌러야 공개됩니다)")
    return result


# ───────────────────────────────────────────────
# ▼▼▼ 첫 테스트: 이 부분만 바꾸면 됩니다 ▼▼▼
# ───────────────────────────────────────────────
if __name__ == "__main__":
    test_title = "쉴드광택 블로그 연결 테스트"
    test_html = """
    <h2>안녕하세요, 쉴드광택입니다.</h2>
    <p>이 글은 자동 발행 시스템 연결 테스트입니다.</p>
    <p>어떤 차를 타냐보다 어떻게 타냐가 중요합니다~!</p>
    """

    # draft=True : 일단 '초안'으로 올려서 안전하게 확인합니다.
    publish_post(test_title, test_html, labels=["테스트"], draft=True)
