# -*- coding: utf-8 -*-
r"""
홈페이지 카운터용 집계값 갱신 (Firestore  stats/summary)
================================================================
홈페이지가 '누적 시공 N대'를 표시하려면 숫자 하나가 필요하다.
그런데 certificates 컬렉션을 프론트에서 통째로 읽으면
문서 3천 개를 매 방문마다 읽게 되어 무료 한도가 하루 15방문에 소진된다.
(게다가 사이트가 쓰는 Firebase v8 은 count() 집계를 지원하지 않는다.)

그래서 관리자 SDK로 미리 세어 stats/summary 문서 하나에 적어둔다.
홈페이지는 그 문서 1건만 읽는다. 방문당 읽기 1회.

증명서를 삭제하는 경우가 있으므로 증감이 아니라 매번 다시 센다. 값이 어긋나지 않는다.

사용
  py update_stats.py            # 다시 세어 저장
  py update_stats.py --show     # 저장된 값만 확인
"""
import sys

import firebase_admin
from firebase_admin import credentials, firestore

KEY = 'firebase-admin-key.json'
DOC = ('stats', 'summary')


def client():
    if not firebase_admin._apps:
        firebase_admin.initialize_app(credentials.Certificate(KEY))
    return firestore.client()


def main():
    db = client()
    ref = db.collection(DOC[0]).document(DOC[1])

    if '--show' in sys.argv:
        snap = ref.get()
        print(snap.to_dict() if snap.exists else '(아직 없음)')
        return

    agg = db.collection('certificates').count().get()
    n = agg[0][0].value

    ref.set({
        'certCount': n,
        'updatedAt': firestore.SERVER_TIMESTAMP,
    }, merge=True)

    print(f'[update_stats] stats/summary.certCount = {n:,}')


if __name__ == '__main__':
    main()
