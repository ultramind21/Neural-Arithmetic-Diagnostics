#!/usr/bin/env python3
"""Generate repository overview diagram as PNG."""

from PIL import Image, ImageDraw, ImageFont
import os

# Image dimensions
WIDTH = 1400
HEIGHT = 700
MARGIN = 60

# Colors
BG_COLOR = (245, 245, 245)  # Light gray
BLOCK1_COLOR = (200, 230, 255)  # Light blue
BLOCK2_COLOR = (200, 255, 220)  # Light green
BLOCK3_COLOR = (255, 240, 200)  # Light orange
TEXT_COLOR = (40, 40, 40)  # Dark gray
ARROW_COLOR = (80, 80, 80)  # Dark gray

# Create image
img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(img)

# Try to use a system font, fall back to default
try:
    title_font = ImageFont.truetype("arial.ttf", 36)
    subtitle_font = ImageFont.truetype("arial.ttf", 18)
    block_title_font = ImageFont.truetype("arial.ttf", 22)
    block_subtitle_font = ImageFont.truetype("arial.ttf", 14)
    block_text_font = ImageFont.truetype("arial.ttf", 12)
    arrow_label_font = ImageFont.truetype("arial.ttf", 11)
    footer_font = ImageFont.truetype("arial.ttf", 13)
except:
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()
    block_title_font = ImageFont.load_default()
    block_subtitle_font = ImageFont.load_default()
    block_text_font = ImageFont.load_default()
    arrow_label_font = ImageFont.load_default()
    footer_font = ImageFont.load_default()

# Draw title
title_text = "Neural-Arithmetic-Diagnostics"
subtitle_text = "Research → Audit → Diagnostic Framework"

title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
title_width = title_bbox[2] - title_bbox[0]
title_x = (WIDTH - title_width) // 2

draw.text((title_x, 20), title_text, fill=TEXT_COLOR, font=title_font)
draw.text((title_x + 20, 62), subtitle_text, fill=TEXT_COLOR, font=subtitle_font)

# Block dimensions
block_width = 280
block_height = 280
block_y = 140

# Block 1 position
block1_x = MARGIN
block1_y = block_y

# Block 2 position (middle)
block2_x = (WIDTH - block_width) // 2
block2_y = block_y

# Block 3 position (right)
block3_x = WIDTH - block_width - MARGIN
block3_y = block_y

def draw_block(x, y, width, height, bg_color, title, subtitle, points):
    """Draw a colored block with title and bullet points."""
    # Draw background rectangle
    draw.rectangle([x, y, x + width, y + height], fill=bg_color, outline=TEXT_COLOR, width=2)
    
    # Draw title
    draw.text((x + 15, y + 15), title, fill=TEXT_COLOR, font=block_title_font)
    
    # Draw subtitle (italicized appearance with different color)
    draw.text((x + 15, y + 45), subtitle, fill=(100, 100, 100), font=block_subtitle_font)
    
    # Draw bullet points
    point_y = y + 85
    for point in points:
        draw.text((x + 20, point_y), f"• {point}", fill=TEXT_COLOR, font=block_text_font)
        point_y += 35

# Draw the three blocks
draw_block(
    block1_x, block1_y, block_width, block_height,
    BLOCK1_COLOR,
    "Projects 1–3",
    "Original Research Line",
    [
        "Arithmetic learning",
        "Killer-test results",
        "Historical closures"
    ]
)

draw_block(
    block2_x, block2_y, block_width, block_height,
    BLOCK2_COLOR,
    "Audit (Phases 1–6)",
    "Verification Layer",
    [
        "Source checks",
        "Semantics checks",
        "Metric checks",
        "Locked caveats"
    ]
)

draw_block(
    block3_x, block3_y, block_width, block_height,
    BLOCK3_COLOR,
    "Project 4",
    "Post-Audit Framework",
    [
        "Stable baselines",
        "Diagnostic scorecard",
        "Intervention testing",
        "Robustness analysis"
    ]
)

# Draw arrows between blocks
arrow_y = block_y + block_height // 2

# Arrow 1: Block1 -> Block2
arrow1_start_x = block1_x + block_width + 5
arrow1_end_x = block2_x - 5
arrow1_y = arrow_y

# Draw arrow line and head
draw.line([(arrow1_start_x, arrow1_y), (arrow1_end_x, arrow1_y)], fill=ARROW_COLOR, width=3)
# Arrow head
arrow_size = 12
draw.polygon(
    [(arrow1_end_x, arrow1_y),
     (arrow1_end_x - arrow_size, arrow1_y - arrow_size // 2),
     (arrow1_end_x - arrow_size, arrow1_y + arrow_size // 2)],
    fill=ARROW_COLOR
)

# Arrow label 1
label1_text = "research"
label1_bbox = draw.textbbox((0, 0), label1_text, font=arrow_label_font)
label1_width = label1_bbox[2] - label1_bbox[0]
label1_x = (arrow1_start_x + arrow1_end_x - label1_width) // 2
draw.text((label1_x, arrow1_y - 25), label1_text, fill=ARROW_COLOR, font=arrow_label_font)

# Arrow 2: Block2 -> Block3
arrow2_start_x = block2_x + block_width + 5
arrow2_end_x = block3_x - 5
arrow2_y = arrow_y

draw.line([(arrow2_start_x, arrow2_y), (arrow2_end_x, arrow2_y)], fill=ARROW_COLOR, width=3)
# Arrow head
draw.polygon(
    [(arrow2_end_x, arrow2_y),
     (arrow2_end_x - arrow_size, arrow2_y - arrow_size // 2),
     (arrow2_end_x - arrow_size, arrow2_y + arrow_size // 2)],
    fill=ARROW_COLOR
)

# Arrow label 2
label2_text = "verification"
label2_bbox = draw.textbbox((0, 0), label2_text, font=arrow_label_font)
label2_width = label2_bbox[2] - label2_bbox[0]
label2_x = (arrow2_start_x + arrow2_end_x - label2_width) // 2
draw.text((label2_x, arrow2_y - 25), label2_text, fill=ARROW_COLOR, font=arrow_label_font)

# Draw footer text
footer_text = "High arithmetic accuracy is not sufficient evidence of robust reasoning."
footer_bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
footer_width = footer_bbox[2] - footer_bbox[0]
footer_x = (WIDTH - footer_width) // 2
draw.text((footer_x, HEIGHT - 40), footer_text, fill=TEXT_COLOR, font=footer_font)

# Add a horizontal line above footer
draw.line([(MARGIN, HEIGHT - 55), (WIDTH - MARGIN, HEIGHT - 55)], fill=(200, 200, 200), width=1)

# Save the image
output_dir = r"d:\Music\Project 03 Abacus\soroban_project\assets"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "repository_overview.png")
img.save(output_path, "PNG")

print(f"✓ Diagram created successfully: {output_path}")
print(f"  Dimensions: {WIDTH}x{HEIGHT} pixels")
print(f"  Format: PNG")
