#!/bin/bash
# Generate wallpaper and push to GitHub Pages
cd /Users/louie/Projects/countdown-widget
python3 scripts/generate-wallpaper.py docs/wallpaper.png
git add docs/wallpaper.png
git commit -m "wallpaper: day $(python3 -c "from datetime import date; print((date.today() - date(2026,2,22)).days + 1)")" --allow-empty
git push origin main
