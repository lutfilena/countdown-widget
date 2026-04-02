#!/usr/bin/env python3
"""Generate a countdown wallpaper for iPhone."""

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, date, timedelta
import math
import os
import sys

# Config
START_DATE = date(2026, 4, 6)  # Monday
TOTAL_DAYS = 56  # 8 weeks
GRID_COLS = 7   # 7 days per row (Mon-Sun)
GRID_ROWS = 8   # 8 weeks

# iPhone 15/16 Pro resolution
WIDTH = 1179
HEIGHT = 2556

# Colors
BG_COLOR = (10, 10, 10)
RED = (230, 57, 70)       # #E63946
OUTLINE = (51, 51, 51)    # #333
TEXT_WHITE = (255, 255, 255)

def generate_wallpaper(output_path=None):
    today = date.today()
    current_day = (today - START_DATE).days + 1
    current_day = max(0, min(current_day, TOTAL_DAYS + 1))
    
    end_date = START_DATE + timedelta(days=TOTAL_DAYS - 1)
    
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Grid dimensions
    square_size = 110
    gap = 10
    row_label_width = 60  # space for week numbers on the left
    grid_width = GRID_COLS * square_size + (GRID_COLS - 1) * gap
    grid_height = GRID_ROWS * square_size + (GRID_ROWS - 1) * gap
    total_width = row_label_width + grid_width
    
    start_x = (WIDTH - total_width) // 2 + row_label_width
    
    # Grid only — positioned to clear lock screen widgets
    start_y = (HEIGHT - grid_height) // 2 + 150
    
    # Draw row numbers (week numbers) on the left
    try:
        row_font = ImageFont.truetype("/System/Library/Fonts/SFCompact.ttf", 36)
    except:
        try:
            row_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
        except:
            row_font = ImageFont.load_default()
    
    for r in range(GRID_ROWS):
        label = str(r + 1)
        y = start_y + r * (square_size + gap)
        bbox = draw.textbbox((0, 0), label, font=row_font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        lx = start_x - row_label_width + (row_label_width - tw) // 2 - 5
        ly = y + (square_size - th) // 2
        draw.text((lx, ly), label, fill=(255, 255, 255, 120), font=row_font)
    
    # Draw grid
    for i in range(TOTAL_DAYS):
        row = i // GRID_COLS
        col = i % GRID_COLS
        day = i + 1
        
        x = start_x + col * (square_size + gap)
        y = start_y + row * (square_size + gap)
        
        if day < current_day:
            # Completed - solid red
            draw.rounded_rectangle([x, y, x + square_size, y + square_size], radius=8, fill=RED)
        elif day == current_day and current_day <= TOTAL_DAYS:
            # Today - red with glow effect
            glow_pad = 6
            draw.rounded_rectangle(
                [x - glow_pad, y - glow_pad, x + square_size + glow_pad, y + square_size + glow_pad],
                radius=12, fill=(230, 57, 70, 60)
            )
            draw.rounded_rectangle([x, y, x + square_size, y + square_size], radius=8, fill=RED)
        else:
            # Remaining - outline only
            draw.rounded_rectangle([x, y, x + square_size, y + square_size], radius=8, outline=OUTLINE, width=2)
        
        # Day number
        try:
            font = ImageFont.truetype("/System/Library/Fonts/SFCompact.ttf", 24)
        except:
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
            except:
                font = ImageFont.load_default()
        
        text = str(day)
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        tx = x + (square_size - tw) // 2
        ty = y + (square_size - th) // 2
        
        if day < current_day or day == current_day:
            draw.text((tx, ty), text, fill=(255, 255, 255, 220), font=font)
        else:
            draw.text((tx, ty), text, fill=(255, 255, 255, 60), font=font)
    
    if output_path is None:
        output_path = os.path.expanduser("~/.openclaw/workspace/countdown-wallpaper.png")
    
    img.save(output_path, "PNG", quality=95)
    print(f"✅ Wallpaper generated: {output_path}")
    print(f"   Day {current_day} of {TOTAL_DAYS} | Ends {end_date.strftime('%B %d, %Y')}")
    return output_path

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else None
    generate_wallpaper(out)
