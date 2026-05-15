#!/usr/bin/env python3
"""Generate OG card PNGs for every entry in _plays/ + a home card for /plays/.

Reads frontmatter from each _plays/*.md file, draws a 1200x630 card with:
- Brand bar at top (orange/red)
- Eyebrow: category in uppercase
- Headline: play title (wrapped, max 4 lines)
- Footer: coachdeforest.com/plays/{slug}/

Output: /assets/og/plays/{slug}.png + /assets/og/plays/index.png

Run locally before committing — Jekyll/GitHub Actions doesn't have Pillow.
"""
import re
import sys
from pathlib import Path
try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Pillow not installed — pip install Pillow")
    sys.exit(1)

REPO = Path(__file__).resolve().parent.parent
PLAYS_DIR = REPO / "_plays"
OUT_DIR = REPO / "assets" / "og" / "plays"
OUT_DIR.mkdir(parents=True, exist_ok=True)

W, H = 1200, 630
BG = (12, 14, 20)
ACCENT = (217, 119, 6)  # warm orange to match the brand
ACCENT_HOVER = (245, 158, 11)
TEXT = (255, 255, 255)
DIM = (170, 170, 180)


def load_font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Helvetica.ttc",
        f"/System/Library/Fonts/Supplemental/Arial{'Bold' if bold else ''}.ttf",
        f"/System/Library/Fonts/Supplemental/Arial {'Bold' if bold else 'Regular'}.ttf",
        f"/usr/share/fonts/truetype/dejavu/DejaVuSans{'-Bold' if bold else ''}.ttf",
    ]
    for p in candidates:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except OSError:
                continue
    return ImageFont.load_default()


def wrap(draw, text, font, max_width):
    words = text.split()
    lines, cur = [], []
    for w in words:
        test = " ".join(cur + [w])
        if draw.textlength(test, font=font) <= max_width:
            cur.append(w)
        else:
            if cur:
                lines.append(" ".join(cur))
            cur = [w]
    if cur:
        lines.append(" ".join(cur))
    return lines


def draw_card(out_path, eyebrow, headline, footer):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # Accent bars top + bottom
    d.rectangle([0, 0, W, 10], fill=ACCENT)
    d.rectangle([0, H - 10, W, H], fill=ACCENT)
    # Brand
    d.text((60, 40), "COACH DEFOREST", font=load_font(28, bold=True), fill=ACCENT)
    # Eyebrow
    if eyebrow:
        d.text((60, 135), eyebrow.upper(), font=load_font(28, bold=True), fill=ACCENT_HOVER)
    # Headline (wrap max 4 lines)
    headline_font = load_font(76, bold=True)
    lines = wrap(d, headline, headline_font, W - 120)
    if len(lines) > 4:
        lines = lines[:3] + [lines[3].split()[0] + " …"]
    line_h = 90
    start_y = (H - line_h * len(lines)) // 2 + 20
    for i, ln in enumerate(lines):
        d.text((60, start_y + i * line_h), ln, font=headline_font, fill=TEXT)
    # Footer
    if footer:
        d.text((60, H - 80), footer, font=load_font(28), fill=DIM)
    img.save(out_path, "PNG", optimize=True)


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith("  "):
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm


count = 0
for md in sorted(PLAYS_DIR.glob("*.md")):
    fm = parse_frontmatter(md.read_text(encoding="utf-8"))
    slug = md.stem
    title = fm.get("title", slug)
    category = fm.get("category", "Basketball play")
    footer = f"coachdeforest.com/plays/{slug}/"
    out = OUT_DIR / f"{slug}.png"
    draw_card(out, category, title, footer)
    count += 1
    print(f"  {slug}.png")

# Plays directory home card
draw_card(
    OUT_DIR / "index.png",
    "Plays Directory",
    "Basketball Plays — A Coaching Library",
    "coachdeforest.com/plays/",
)
count += 1
print(f"  index.png\n\n{count} cards generated → {OUT_DIR}")
