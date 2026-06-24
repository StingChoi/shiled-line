@echo off
chcp 949 >nul
cd /d D:\shiled-line

echo ============================================================
echo    shiled gwangtaek - homepage + YouTube + Blogger 한방 발행
echo ============================================================
echo.
echo  [1/4] 영상을 유튜브에 올리고 글에 연결합니다 (밀린 것 전부)...
echo        (영상 없으면 자동으로 넘어갑니다)
echo.

py upload_videos.py --all

echo.
echo  [2/4] 홈페이지에 올립니다 (GitHub Push)...
echo.

git add -A
git commit -m "auto: new blog posts"
git push

echo.
echo  [3/4] 홈페이지에 사진/영상이 반영되길 기다립니다 (90초)...
echo.

timeout /t 90 /nobreak

echo.
echo  [4/4] 안 올린 글을 블로거에 시차 예약발행합니다...
echo        (1번 즉시 공개, 2번 +2시간, 3번 +4시간 ... 블로거가 자동 공개)
echo.

py post_html.py --all

echo.
echo ============================================================
echo   끝났습니다!
echo   - 홈페이지 : 1~2분 내 www.shiled-line.com/blog 반영
echo   - 유튜브   : 위에 뜬 주소 확인
echo   - 블로거   : 1번은 바로 공개, 나머지는 예약시각에 자동 공개
echo ============================================================
echo.
pause
