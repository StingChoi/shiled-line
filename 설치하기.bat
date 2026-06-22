@echo off
chcp 65001 >nul
echo ============================================
echo  쉴드광택 블로거 - 필요한 프로그램 설치
echo ============================================
echo.
echo 잠시만 기다려주세요. 자동으로 설치됩니다...
echo.
py -m pip install --upgrade google-auth-oauthlib google-api-python-client
echo.
echo ============================================
echo  설치 완료! 이제 발행 스크립트를 쓸 수 있습니다.
echo ============================================
pause
