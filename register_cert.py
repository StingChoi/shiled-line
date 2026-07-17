# -*- coding: utf-8 -*-
"""
시공증명서 Firestore 등록 스크립트 (쉴드광택 대연점)
- 서비스 계정 키: firebase-admin-key.json (gitignore 차단됨)
- 기본은 DRY-RUN(등록 안 함). 실제 등록은 --commit 플래그.
- 중복 방지: 같은 (vin_number + coating_type) 조합이 이미 있으면 건너뜀.

매니페스트(JSON) 형식: [{vin_number, car_type, coating, install_date, branch?, note?}, ...]
coating 값은 아래 COATING_MAP의 짧은 키(F5, G-Pro, G-Top, 듀얼, 트리플, 시트코팅)를 쓴다.
사용:  py register_cert.py <manifest.json>            # dry-run
       py register_cert.py <manifest.json> --commit   # 실제 등록
"""
import sys, io, json
import firebase_admin
from firebase_admin import credentials, firestore

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

KEY_FILE = 'firebase-admin-key.json'
DEFAULT_BRANCH = '쉴드 대연점'
REGISTER_UID = 'cowork-auto'  # 자동 등록 표식(추적용)
CUTOFF_DATE = '2026-07-14'    # 이 날짜 이전 시공건은 등록 안 함(기존 데이터 충돌 방지)

# 기존 DB 표기 관례에 맞춘 코팅종류 문자열
COATING_MAP = {
    'F5':    'F5 도장채도 향상',
    'G-Pro': 'G-Pro 도장경도 향상',
    'G-Top': 'G-Top 발수력 및 슈팅력 향상',
    '듀얼':   'G-Pro+G-Top 도장 경도+발수력 향상',
    '트리플': 'G-Pro+F5+G-Top 도장 경도+채도+발수력 향상',
    '시트코팅': 'SeatCoat 시트오염보호코팅',
}

def main():
    if len(sys.argv) < 2:
        print('사용법: py register_cert.py <manifest.json> [--commit]')
        sys.exit(1)
    manifest_path = sys.argv[1]
    commit = '--commit' in sys.argv

    with io.open(manifest_path, encoding='utf-8') as f:
        jobs = json.load(f)

    cred = credentials.Certificate(KEY_FILE)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    col = db.collection('certificates')

    print('=' * 78)
    print('모드:', '★ 실제 등록 (--commit) ★' if commit else 'DRY-RUN (등록 안 함, 미리보기)')
    print('=' * 78)

    to_write, skipped = [], []
    for j in jobs:
        vin = str(j['vin_number']).strip()
        coating_full = COATING_MAP.get(j['coating'], j['coating'])
        branch = j.get('branch', DEFAULT_BRANCH)
        # 컷오프: CUTOFF_DATE 이전 시공건은 등록 안 함(기존 데이터 충돌 방지)
        if str(j['install_date']) < CUTOFF_DATE:
            skipped.append((j, f'{CUTOFF_DATE} 이전 작업 → 등록 제외'))
            continue
        # 중복 검사: 같은 vin_number 중 같은 coating_type 이 있으면 skip
        existing = list(col.where('vin_number', '==', vin).stream())
        dup = [d for d in existing if d.to_dict().get('coating_type') == coating_full]
        rec = {
            'branch': branch,
            'vin_number': vin,
            'car_type': j['car_type'],
            'coating_type': coating_full,
            'install_date': j['install_date'],
        }
        if dup:
            skipped.append((j, '이미 등록됨(중복)'))
        else:
            to_write.append((j, rec))

    # 미리보기 출력
    print('\n[등록 예정]')
    print('-' * 78)
    for j, rec in to_write:
        print(f"  차대번호 {rec['vin_number']:>7} | {rec['car_type']:<12} | {rec['coating_type']}")
        print(f"           시공일 {rec['install_date']} | {rec['branch']} | ({j.get('src','')})")
        if j.get('note'):
            print(f"           ⚠ {j['note']}")
    if skipped:
        print('\n[건너뜀]')
        print('-' * 78)
        for j, why in skipped:
            print(f"  차대번호 {str(j['vin_number']):>7} | {j['car_type']:<12} | {why}")

    print('\n' + '-' * 78)
    print(f"등록 예정 {len(to_write)}건, 건너뜀 {len(skipped)}건")

    if not commit:
        print('\n※ DRY-RUN입니다. 실제로 아무것도 등록하지 않았습니다.')
        print('  확정하려면:  py register_cert.py', manifest_path, '--commit')
        return

    # 실제 등록 (+ QR 자동 생성)
    try:
        from gen_cert_qr import make_qr
    except Exception:
        make_qr = None
    print('\n등록 진행...')
    done = 0
    qr_done = set()
    for j, rec in to_write:
        rec['uid'] = REGISTER_UID
        rec['createdAt'] = firestore.SERVER_TIMESTAMP
        col.add(rec)
        done += 1
        print(f"  ✅ {rec['vin_number']} {rec['car_type']} {rec['coating_type']}")
        # 같은 차대번호는 QR 한 번만 생성
        if make_qr and rec['vin_number'] not in qr_done:
            try:
                path, _ = make_qr(rec['vin_number'])
                qr_done.add(rec['vin_number'])
                print(f"     QR: {path}")
            except Exception as e:
                print(f"     (QR 생성 실패: {e})")
    print(f"\n완료: {done}건 등록, QR {len(qr_done)}개 생성.")

if __name__ == '__main__':
    main()
