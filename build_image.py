#!/usr/bin/env python3
"""Build the 18 Nov 2026 front page: hero illustration + accurate headlines.
Deterministic: no timestamps, no randomness, no network. Output entry.png 1024x1024.
Run: python3 build_image.py
"""
from PIL import Image, ImageDraw, ImageFont
import os, textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, width):
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

W, H = 1024, 1024
PAPER = (245, 238, 220)
INK = (18, 24, 38)
RED = (178, 34, 28)
GOLD = (176, 132, 52)
GREY = (88, 88, 84)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 36

# Masthead
d.text((M, 22), "T H E   W O R L D   I N   O N E   I M A G E", font=font(SANS_B, 19), fill=RED)
d.text((M, 48), "18 NOVEMBER 2026", font=font(SERIF_B, 62), fill=INK)
d.text((M, 118), "Wednesday  •  Gulf strikes  •  Crimea Bridge  •  Shenzhen summit", font=font(SANS, 19), fill=GREY)
d.line([(M, 148), (W-M, 148)], fill=INK, width=3)
d.line([(M, 153), (W-M, 153)], fill=INK, width=1)

# Hero illustration, cropped to fill 1024x452
hero = Image.open(os.path.join(HERE, "media-generation-news-hero-20261118-0-1f0ad71b-be61-434b-9ec8-7abdd91db4b7.png")).convert("RGB")
hw, hh = hero.size
target_w, target_h = W - 2*M, 452
scale = max(target_w/hw, target_h/hh)
hero2 = hero.resize((int(hw*scale), int(hh*scale)), Image.LANCZOS)
x0 = (hero2.width - target_w)//2
y0 = (hero2.height - target_h)//2
img.paste(hero2.crop((x0, y0, x0+target_w, y0+target_h)), (M, 162))
d.rectangle([(M, 162), (W-M, 162+target_h)], outline=INK, width=2)
d.text((M, 622), "A day of strikes, a broken bridge and a summit in Shenzhen — the world on 18 November 2026.",
       font=font(SANS_I, 16), fill=GREY)

# Stories: (kicker, headline, summary)
stories = [
    ("GULF", "US strikes Qeshm Island;\nIran hits US bases",
     "Tehran fired drones at Bahrain and Kuwait after the US hit a missile site in the Strait of Hormuz."),
    ("UKRAINE", "Crimea Bridge hit again;\nspan falls into the sea",
     "Ukrainian drones and missiles struck the Kerch Bridge for a second day; part of it collapsed."),
    ("SUMMIT", "Xi and Putin meet in\nShenzhen before Trump",
     "The two leaders held talks a day before a planned three-way summit with the US president."),
    ("US SENATE", "Peltola wins Alaska;\nDemocrats take 56–44",
     "Mary Peltola beat Dan Sullivan, giving Democrats a projected 56–44 Senate majority."),
    ("ISRAEL", "Kahana elected Knesset\nspeaker in Netanyahu blow",
     "Parliament chose Matan Kahana, a win for PM-elect Gadi Eisenkot over Netanyahu's camp."),
    ("HEALTH & DISASTER", "Ebola surges in Congo;\nCyclone Xavier strikes",
     "DR Congo passed 11,000 Ebola cases; a Category 5 cyclone hit the Cook Islands; 19 died in a Russian plane crash."),
]

col_w = (W - 2*M - 28)//2
row_h = 112
top = 652
for i, (kick, head, summ) in enumerate(stories):
    col = i % 2
    row = i // 2
    x = M + col*(col_w+28)
    y = top + row*row_h
    d.text((x, y), kick, font=font(SANS_B, 15), fill=RED)
    yy = y + 22
    for line in head.split("\n"):
        d.text((x, yy), line, font=font(SERIF_B, 21), fill=INK)
        yy += 25
    # summary, wrapped to 2 lines max
    lines = wrap(d, summ, font(SANS, 15), col_w)[:2]
    for line in lines:
        d.text((x, yy), line, font=font(SANS, 15), fill=(52, 52, 48))
        yy += 19
    if row < 2:
        d.line([(x, y+row_h-14), (x+col_w, y+row_h-14)], fill=(200, 190, 165), width=1)

d.line([(M, 992), (W-M, 992)], fill=INK, width=1)
d.text((M, 1000), "Sources: Reuters · AP · AFP · Just Security — 18 Nov 2026", font=font(SANS, 13), fill=GREY)

out = os.path.join(HERE, "entry.png")
img.save(out, "PNG", optimize=True)
print(out, img.size, os.path.getsize(out), "bytes")
