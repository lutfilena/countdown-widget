#!/usr/bin/env python3
"""Generate a countdown wallpaper for iPhone."""

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, date, timedelta
import math
import os
import sys

# Config
START_DATE = date(2026, 4, 1)
TOTAL_DAYS = 50
GRID_COLS = 5  # 5 columns, 10 rows for 50 days

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
    
    # Grid dimensions — same overall width as before (~952px)
    grid_rows = math.ceil(TOTAL_DAYS / GRID_COLS)
    square_size = 120
    gap = 10
    grid_width = GRID_COLS * square_size + (GRID_COLS - 1) * gap
    grid_height = grid_rows * square_size + (grid_rows - 1) * gap
    
    start_x = (WIDTH - grid_width) // 2
    
    # Load fonts early for text measurement
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/SFCompact.ttf", 48)
        sub_font = ImageFont.truetype("/System/Library/Fonts/SFCompact.ttf", 24)
    except:
        try:
            title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
            sub_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
        except:
            title_font = ImageFont.load_default()
            sub_font = ImageFont.load_default()
    
    # Day label
    if current_day <= 0:
        day_text = "STARTS SOON"
    elif current_day > TOTAL_DAYS:
        day_text = "✅ COMPLETED"
    else:
        day_text = f"DAY {current_day} OF {TOTAL_DAYS}"
    
    end_text = f"Ends {end_date.strftime('%B %d, %Y')}"
    
    # Header height: title + end date + progress bar + spacing
    header_height = 48 + 15 + 24 + 20 + 6 + 40  # title + gap + subtitle + gap + bar + gap before grid
    
    # Position everything: header + grid centered together
    total_height = header_height + grid_height
    top_y = (HEIGHT - total_height) // 2 + 100
    
    # Draw header text ABOVE grid
    bbox = draw.textbbox((0, 0), day_text, font=title_font)
    tw = bbox[2] - bbox[0]
    draw.text(((WIDTH - tw) // 2, top_y), day_text, fill=TEXT_WHITE, font=title_font)
    
    bbox = draw.textbbox((0, 0), end_text, font=sub_font)
    tw = bbox[2] - bbox[0]
    draw.text(((WIDTH - tw) // 2, top_y + 48 + 15), end_text, fill=(255, 255, 255, 100), font=sub_font)
    
    # Progress bar
    bar_y = top_y + 48 + 15 + 24 + 20
    bar_width = grid_width
    bar_height = 6
    bar_x = start_x
    draw.rounded_rectangle([bar_x, bar_y, bar_x + bar_width, bar_y + bar_height], radius=3, fill=(26, 26, 26))
    pct = min(current_day / TOTAL_DAYS, 1.0)
    fill_width = int(bar_width * pct)
    if fill_width > 0:
        draw.rounded_rectangle([bar_x, bar_y, bar_x + fill_width, bar_y + bar_height], radius=3, fill=RED)
    
    # Grid starts below header
    start_y = bar_y + 6 + 40
    
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
