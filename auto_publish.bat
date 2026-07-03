@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
cd /d D:\shiled-line

echo [auto_publish] 1/4 YouTube upload...
py upload_videos.py --all

echo [auto_publish] 2/4 GitHub push...
git add -A
git commit -m "auto: new blog posts"
git push

echo [auto_publish] 3/4 wait 90s for homepage/image propagation...
powershell -NoProfile -Command "Start-Sleep -Seconds 90"

echo [auto_publish] 4/4 Blogger publish...
py post_html.py --all

echo [auto_publish] done.
