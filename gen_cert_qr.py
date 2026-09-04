# -*- coding: utf-8 -*-
r"""
시공증명서 QR 생성기 (쉴드광택)
- 차대번호를 주면, 그 차 증명서를 홈페이지에서 바로 조회하는 딥링크 QR(PNG)을 만든다.
- 스캔하면 고객이 번호 입력 없이 자기 차 정품 시공 확인 페이지로 바로 이동.
사용:  py gen_cert_qr.py 232441 604689 ...     # 각 차대번호별 QR 생성
출력:  D:\shiled-line\blog\images\cert_qr\<vin>.png  (홈페이지에 함께 배포 가능)
"""
import sys, os
import qrcode

BASE_URL = 'https://www.shiled-line.com/certificates?vin='
OUT_DIR = r'D:\shiled-line\blog\images\cert_qr'

def make_qr(vin):
    url = BASE_URL + str(vin).strip()
    qr = qrcode.QRCode(
        version=None, error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10, border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, f'{vin}.png')
    img.save(path)
    return path, url

if __name__ == '__main__':
    vins = sys.argv[1:]
    if not vins:
        print('사용법: py gen_cert_qr.py <차대번호1> <차대번호2> ...')
        sys.exit(1)
    for vin in vins:
        path, url = make_qr(vin)
        print(f'  QR 생성: {path}')
        print(f'         → {url}')
