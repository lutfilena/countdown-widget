#!/bin/bash
# Generate wallpaper and push to GitHub Pages
cd /Users/louie/Projects/countdown-widget
python3 scripts/generate-wallpaper.py docs/wallpaper.png
DAY=$(python3 -c "from datetime import date; d=(date.today()-date(2026,4,6)).days+1; print(max(0,min(d,56)))")
git add docs/wallpaper.png
git commit -m "wallpaper: day ${DAY} of 56" --allow-empty
git push origin main
