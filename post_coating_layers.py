# -*- coding: utf-8 -*-
"""
블로거(shieldgloss.blogspot.com)에 '유리막코팅 층 구조' 글을 발행한다.

단면도는 이미지가 아니라 인라인 스타일 HTML로 그린다.
→ 외부 이미지 호스팅이 필요 없고, 블로거 템플릿 안에서 바로 렌더링된다.

사용법:
  py post_coating_layers.py           # 초안(draft)으로 올림
  py post_coating_layers.py --publish # 바로 공개 발행
"""
import sys
from blogger_post import publish_post

# ─────────────────────────────────────────── 층 색 (어두운 바탕에 미리 합성한 값)
C = {
    "gtop":   ("#10646A", "#E8EBEE", "#9FD9DC"),   # 배경, 이름색, 역할색
    "f5":     ("#624B29", "#E8EBEE", "#E0BE8B"),
    "gpro":   ("#414D5A", "#E8EBEE", "#B3C2D1"),
    "clear":  ("#2A3138", "#E8EBEE", "#A9B3BD"),
    "base":   ("#0D1015", "#E8EBEE", "#8892A0"),
    "primer": ("#494540", "#FFFFFF", "#D8D2C9"),
    "steel":  ("#6E767E", "#FFFFFF", "#E2E6EA"),
}

LAYER_META = {
    "gtop": ("G-TOP", "발수 · 방오"),
    "f5":   ("F5", "색감 · 광택"),
    "gpro": ("G-PRO", "경도 · 스크래치 내성"),
}

SUBSTRATE = [
    ("clear",  "클리어코트", "투명 보호층", 40),
    ("base",   "베이스",     "차량 색상",   46),
    ("primer", "프라이머",   "밀착 · 방청", 30),
    ("steel",  "철판",       "차체",       36),
]


def band(key, name, role, h, top_line=True):
    bg, nc, rc = C[key]
    bt = "border-top:1px solid rgba(255,255,255,.18);" if top_line else ""
    return (
        f'<div style="display:flex;align-items:center;justify-content:space-between;'
        f'padding:0 14px;height:{h}px;background:{bg};{bt}box-sizing:border-box;">'
        f'<span style="font-size:12px;font-weight:700;color:{nc};letter-spacing:.04em;">{name}</span>'
        f'<span style="font-size:11px;color:{rc};">{role}</span>'
        f"</div>"
    )


def diagram(stack, title):
    """stack = 아래에서 위 순서. 그림은 위에서 아래로 그린다."""
    rows = []
    # 공기
    rows.append(
        '<div style="height:34px;background:#0C0E11;display:flex;align-items:center;'
        'padding:0 14px;box-sizing:border-box;">'
        '<span style="font-size:11px;color:#6B7480;">공기</span></div>'
    )
    # 코팅층 (위에서부터)
    for key in reversed(stack):
        nm, role = LAYER_META[key]
        rows.append(band(key, nm, role, 40))
    # 도장 구조
    for key, nm, role, h in SUBSTRATE:
        rows.append(band(key, nm, role, h))

    return (
        '<div style="margin:22px 0;">'
        f'<p style="margin:0 0 8px;font-size:13px;font-weight:700;color:#0B8E94;">{title}</p>'
        '<div style="border-radius:10px;overflow:hidden;max-width:520px;'
        'box-shadow:0 6px 20px rgba(0,0,0,.18);">'
        + "".join(rows)
        + "</div></div>"
    )


P = 'style="margin:0 0 6px;line-height:1.85;font-size:15.5px;color:#222;"'
H = 'style="margin:34px 0 12px;font-size:19px;font-weight:800;color:#14171B;line-height:1.4;"'
SPACER = '<p style="margin:0 0 14px;">&nbsp;</p>'


def build():
    b = []
    a = b.append

    # ── 도입 (Hook)
    a(f"<p {P}>유리막코팅 문의를 받다 보면 가장 많이 듣는 말이 있습니다.</p>")
    a(f'<p {P}>"코팅 한 번 발라주시면 되죠?"</p>')
    a(SPACER)
    a(f"<p {P}>사실은 다릅니다.</p>")
    a(f"<p {P}>유리막코팅은 한 번 바르는 작업이 아닙니다.</p>")
    a(f"<p {P}><b>역할이 서로 다른 층을, 정해진 순서로 쌓는 작업</b>입니다.</p>")
    a(SPACER)
    a(f"<p {P}>그래서 오늘은 도장면 단면을 그려놓고 설명드리겠습니다.</p>")
    a(f"<p {P}>싱글코팅 3종, 듀얼코팅, 트리플코팅이 각각 어떻게 올라가는지 보시면</p>")
    a(f"<p {P}>왜 가격과 결과가 갈리는지 바로 이해되실 겁니다.</p>")

    # ── 도장면 구조
    a(f"<h2 {H}>자동차 도장면은 원래 어떻게 생겼나요?</h2>")
    a(f"<p {P}>코팅 이야기를 하기 전에 바닥부터 봐야 합니다.</p>")
    a(f"<p {P}>출고된 차의 도장면은 이렇게 4겹입니다.</p>")
    a(diagram([], "무코팅 · 출고 상태의 도장면"))
    a(f"<p {P}>맨 아래가 <b>철판</b>입니다.</p>")
    a(f"<p {P}>그 위에 녹을 막고 밀착을 돕는 <b>프라이머</b>.</p>")
    a(f"<p {P}>차의 색을 내는 <b>베이스</b>.</p>")
    a(f"<p {P}>가장 바깥에 투명한 <b>클리어코트</b>가 덮여 있습니다.</p>")
    a(SPACER)
    a(f"<p {P}>여기서 중요한 건 마지막 줄입니다.</p>")
    a(f"<p {P}>코팅을 하지 않으면 <b>클리어코트가 가장 바깥층</b>입니다.</p>")
    a(f"<p {P}>세차할 때 생기는 잔기스, 새똥, 워터스팟.</p>")
    a(f"<p {P}>전부 이 면이 직접 받아냅니다.</p>")

    # ── 싱글
    a(f"<h2 {H}>싱글코팅 3종은 뭐가 다른가요?</h2>")
    a(f"<p {P}>쉴드에서 쓰는 코팅제는 세 가지입니다.</p>")
    a(f"<p {P}>전부 직접 개발하고 제조한 제품이고, 각각 잘하는 게 다릅니다.</p>")

    a(diagram(["gpro"], "싱글 · G-PRO — 경도"))
    a(f"<p {P}><b>G-PRO</b>는 경도가 높은 하드코팅입니다.</p>")
    a(f"<p {P}>스크래치를 도장면 대신 받아내는 역할입니다.</p>")
    a(f"<p {P}>세차 잔기스가 걱정되시면 이 층이 답입니다.</p>")

    a(diagram(["f5"], "싱글 · F5 — 색감"))
    a(f"<p {P}><b>F5</b>는 색감의 깊이와 글로시함에 특화돼 있습니다.</p>")
    a(f"<p {P}>빛이 표면에서 흩어지지 않고 안쪽까지 들어갔다 반사됩니다.</p>")
    a(f"<p {P}>검정 계열에서 차이가 제일 크게 보입니다.</p>")

    a(diagram(["gtop"], "싱글 · G-TOP — 발수"))
    a(f"<p {P}><b>G-TOP</b>은 발수와 방오 담당입니다.</p>")
    a(f"<p {P}>물이 넓게 퍼지지 않고 구슬처럼 맺혀 흘러내립니다.</p>")
    a(f"<p {P}>물때와 오염이 눌어붙는 걸 줄여 줍니다.</p>")

    # ── 듀얼
    a(f"<h2 {H}>듀얼코팅은 어떤 조합인가요?</h2>")
    a(diagram(["gpro", "gtop"], "듀얼코팅 · G-PRO + G-TOP"))
    a(f"<p {P}><b>G-PRO로 바닥을 다지고, G-TOP으로 마감</b>합니다.</p>")
    a(f"<p {P}>아래층이 스크래치를 받아냅니다.</p>")
    a(f"<p {P}>바깥층이 물과 오염을 막습니다.</p>")
    a(SPACER)
    a(f"<p {P}>보호 위주로 실용적으로 가시려는 분께 맞습니다.</p>")

    # ── 트리플
    a(f"<h2 {H}>트리플코팅은 뭐가 더 올라가나요?</h2>")
    a(diagram(["gpro", "f5", "gtop"], "트리플코팅 · G-PRO + F5 + G-TOP"))
    a(f"<p {P}>듀얼 사이에 <b>F5</b>가 한 겹 더 들어갑니다.</p>")
    a(f"<p {P}>순서를 보시면 역할이 명확합니다.</p>")
    a(SPACER)
    a(f"<p {P}>경도는 <b>아래</b>에서.</p>")
    a(f"<p {P}>색감은 <b>가운데</b>에서.</p>")
    a(f"<p {P}>발수는 <b>바깥</b>에서.</p>")
    a(SPACER)
    a(f"<p {P}>각 층이 자기 자리에서 자기 일만 합니다.</p>")
    a(f"<p {P}>내구성·색감·발수를 전부 최대치로 원하시면 트리플입니다.</p>")

    # ── 전처리 (핵심 메시지)
    a(f"<h2 {H}>그런데 층보다 중요한 게 있습니다</h2>")
    a(f"<p {P}>여기까지가 코팅층 이야기였습니다.</p>")
    a(f"<p {P}>그런데 유리막코팅의 결과를 실제로 가르는 건 따로 있습니다.</p>")
    a(f"<p {P}><b>그 아래 도장면</b>입니다.</p>")
    a(SPACER)
    a(f"<p {P}>위 그림에서 코팅층이 얹히는 자리를 보십시오.</p>")
    a(f"<p {P}>클리어코트 표면입니다.</p>")
    a(f"<p {P}>이 면을 전처리와 광택으로 평탄하게 만들지 않으면 어떻게 될까요.</p>")
    a(SPACER)
    a(f"<p {P}>오염과 잔기스를 그대로 덮은 채 코팅이 굳습니다.</p>")
    a(f"<p {P}>광택은 잠깐 살아 보입니다.</p>")
    a(f"<p {P}>하지만 손상은 그 아래 그대로 남습니다.</p>")
    a(SPACER)
    a(f"<p {P}>저가 시공의 위험이 여기 있습니다.</p>")
    a(f"<p {P}>단가를 맞추려면 줄일 수 있는 건 전처리 시간뿐이기 때문입니다.</p>")

    # ── 마무리
    a(f"<h2 {H}>정리하면</h2>")
    a(f"<p {P}>· 유리막코팅은 한 겹이 아니라 <b>역할이 다른 층을 순서대로</b> 쌓는 작업입니다.</p>")
    a(f"<p {P}>· 순서는 경도(G-PRO) → 색감(F5) → 발수(G-TOP)입니다.</p>")
    a(f"<p {P}>· 듀얼은 보호 위주, 트리플은 색감까지 잡는 풀옵션입니다.</p>")
    a(f"<p {P}>· 무엇을 올리든 <b>도장면 정리가 먼저</b>입니다.</p>")
    a(SPACER)
    a(f"<p {P}>쉴드광택은 코팅제를 직접 개발하고 제조합니다.</p>")
    a(f"<p {P}>그래서 어떤 도장면에 어떤 층을 어떤 순서로 올릴지 판단해서 시공합니다.</p>")

    # ── 인터랙티브 링크 + CTA
    a(
        '<div style="margin:30px 0;padding:20px 22px;background:#F3F4F1;'
        'border:1px solid #E4E6E1;border-radius:12px;">'
        f'<p style="margin:0 0 8px;font-size:15px;font-weight:800;color:#14171B;">'
        "조합을 직접 바꿔보실 수 있습니다</p>"
        f'<p style="margin:0 0 12px;font-size:14.5px;line-height:1.7;color:#5C636B;">'
        "홈페이지에 단면도를 올려뒀습니다. 버튼으로 조합을 바꾸면 "
        "물·스크래치·빛이 닿을 때 어떻게 달라지는지 함께 보실 수 있습니다.</p>"
        '<p style="margin:0;font-size:15px;">'
        '<a href="https://www.shiled-line.com/coating-layers.html" '
        'style="color:#0B8E94;font-weight:800;text-decoration:none;">'
        "→ 유리막코팅 단면 구조 보러 가기</a></p>"
        "</div>"
    )

    a(
        '<div style="margin:24px 0 8px;padding:20px 22px;background:#14171B;'
        'border-radius:12px;color:#fff;">'
        '<p style="margin:0 0 10px;font-size:12px;letter-spacing:.16em;'
        'color:#13C2C9;font-weight:700;">방문 및 견적 문의</p>'
        '<p style="margin:0 0 4px;font-size:15.5px;line-height:1.7;">'
        "쉴드광택 (Shield Gloss)<br>부산 남구 유엔로220 1층</p>"
        '<p style="margin:10px 0 0;font-size:17px;font-weight:800;">'
        '<a href="tel:010-3384-1850" style="color:#fff;text-decoration:none;">'
        "010-3384-1850</a></p>"
        '<p style="margin:14px 0 0;font-size:13.5px;color:#9AA3AC;">'
        "평일 09:00–18:00 · 토 10:00–16:00 · 일요일 휴무</p>"
        "</div>"
    )

    a(f'<p style="margin:22px 0 0;font-size:14px;color:#5C636B;">'
      "어떤 차를 타냐보다 어떻게 타냐가 중요합니다~!</p>")

    return "\n".join(b)


TITLE = "유리막코팅 원리｜싱글·듀얼·트리플 층 구조 완전정리 (부산 대연동)"
LABELS = ["유리막코팅", "부산 유리막코팅", "트리플코팅", "듀얼코팅",
          "대연동 유리막코팅", "코팅원리", "쉴드광택"]


if __name__ == "__main__":
    draft = "--publish" not in sys.argv
    html = build()
    print("본문 길이: %d자" % len(html))
    publish_post(TITLE, html, labels=LABELS, draft=draft)
