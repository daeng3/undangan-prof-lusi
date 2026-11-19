# -*- coding: utf-8 -*-
"""Menyiapkan aset undangan: potret teroptimasi + kartu pratinjau tautan (1200x630)."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SRC = "foto.png"
OUT_PORTRAIT = "assets/potret.jpg"
OUT_SHARE = "share.jpg"

os.makedirs("assets", exist_ok=True)

NAVY_TOP = (7, 22, 36)
NAVY_BOT = (17, 49, 70)
GOLD = (201, 164, 94)
GOLD_LIGHT = (232, 211, 162)
IVORY = (247, 242, 231)

FONT_DIR = r"C:\Windows\Fonts"
def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

geo = lambda s: font("georgia.ttf", s)
geob = lambda s: font("georgiab.ttf", s)
geoi = lambda s: font("georgiai.ttf", s)

# ---------- 1. Potret untuk halaman ----------
im = Image.open(SRC).convert("RGB")
w, h = im.size
# rasio 4:5, potong sedikit dari kiri/kanan bila perlu agar subjek tetap di tengah
target_ratio = 4 / 5
if w / h > target_ratio:
    new_w = int(h * target_ratio)
    left = (w - new_w) // 2
    im = im.crop((left, 0, left + new_w, h))
portrait = im.resize((900, 1125), Image.LANCZOS)
portrait.save(OUT_PORTRAIT, "JPEG", quality=86, optimize=True, progressive=True)
print("potret:", portrait.size, os.path.getsize(OUT_PORTRAIT))

# ---------- 2. Kartu pratinjau tautan ----------
W, H = 1200, 630
card = Image.new("RGB", (W, H), NAVY_TOP)
d = ImageDraw.Draw(card)

# gradien vertikal + glow emas di kanan atas
for y in range(H):
    t = y / (H - 1)
    d.line([(0, y), (W, y)], fill=tuple(int(NAVY_TOP[i] + (NAVY_BOT[i] - NAVY_TOP[i]) * t) for i in range(3)))
glow = Image.new("L", (W, H), 0)
gd = ImageDraw.Draw(glow)
gd.ellipse([W - 620, -380, W + 260, 500], fill=46)
glow = glow.filter(ImageFilter.GaussianBlur(90))
card = Image.composite(Image.new("RGB", (W, H), (120, 92, 44)), card, glow)
d = ImageDraw.Draw(card)

# bingkai tipis
d.rectangle([38, 38, W - 39, H - 39], outline=(120, 96, 55), width=1)
d.rectangle([48, 48, W - 49, H - 49], outline=(72, 60, 38), width=1)
# sudut aksen
for (cx, cy, dx, dy) in [(38, 38, 1, 1), (W - 39, 38, -1, 1), (38, H - 39, 1, -1), (W - 39, H - 39, -1, -1)]:
    d.line([(cx, cy + dy * 26), (cx, cy), (cx + dx * 26, cy)], fill=GOLD, width=2)

def tracked(draw, xy, text, fnt, fill, tracking=0):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking
    return x

# medali potret di kanan
med_c, med_r = (930, 315), 196
photo = Image.open(SRC).convert("RGB")
pw, ph = photo.size
box = (int(0.12 * pw), int(0.03 * ph), int(0.86 * pw), int(0.622 * ph))
photo = photo.crop(box)
side = min(photo.size)
photo = photo.crop(((photo.width - side) // 2, 0, (photo.width - side) // 2 + side, side))
photo = photo.resize((med_r * 2, med_r * 2), Image.LANCZOS)
mask = Image.new("L", (med_r * 2, med_r * 2), 0)
ImageDraw.Draw(mask).ellipse([0, 0, med_r * 2 - 1, med_r * 2 - 1], fill=255)
card.paste(photo, (med_c[0] - med_r, med_c[1] - med_r), mask)
d = ImageDraw.Draw(card)
d.ellipse([med_c[0] - med_r - 12, med_c[1] - med_r - 12, med_c[0] + med_r + 12, med_c[1] + med_r + 12], outline=GOLD, width=2)
d.ellipse([med_c[0] - med_r - 20, med_c[1] - med_r - 20, med_c[0] + med_r + 20, med_c[1] + med_r + 20], outline=(110, 90, 55), width=1)

# teks kiri
L = 96
tracked(d, (L, 104), "UNDANGAN PENGUKUHAN", geo(17), GOLD_LIGHT, 5.4)
d.line([(L, 146), (L + 58, 146)], fill=GOLD, width=2)
d.text((L - 4, 162), "Guru Besar", font=geo(72), fill=IVORY)
d.text((L - 2, 258), "Prof. Dr. apt.", font=geoi(31), fill=(214, 198, 168))
d.text((L - 3, 296), "Lusi Nurdianti, M.Si.", font=geob(39), fill=GOLD_LIGHT)
d.line([(L, 372), (L + 420, 372)], fill=(92, 78, 52), width=1)
d.text((L, 396), "Senin, 30 November 2026  ·  08.00 WIB", font=geob(21), fill=IVORY)
d.text((L, 432), "BTH Convention Hall  ·  Tasikmalaya", font=geo(19), fill=(196, 205, 208))
d.text((L, 512), "Universitas Bakti Tunas Husada", font=geo(17), fill=(150, 163, 168))

card.save(OUT_SHARE, "JPEG", quality=90, optimize=True, progressive=True)
print("share:", card.size, os.path.getsize(OUT_SHARE))

# pratinjau kecil untuk pemeriksaan visual
prev = card.copy()
prev.thumbnail((900, 900))
prev.save("_preview_share.jpg", "JPEG", quality=88)
