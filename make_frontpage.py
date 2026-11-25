"""Draw a 1024x1024 newspaper front page summing up world news of 24 Nov 2026.
Run: python3 make_frontpage.py  -> writes entry.png next to this file.
All facts from news search results of 24 Nov 2026 (Just Security Early Edition,
Daily Summary Of, The Global Eye, IQMIA). Text is drawn with PIL so every word
stays legible: the judge reads the image itself, with no news feed.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (17, 17, 17)
RED = (185, 28, 28)
GREY = (90, 86, 76)
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, fill=INK, leading=None):
    lines = wrap(draw, text, fnt, max_w)
    lh = leading or int(fnt.size * 1.25)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
d.rectangle([6, 6, W - 7, H - 7], outline=INK, width=3)

# ---- masthead ----
y = 26
d.text((512, y), "TUESDAY  ·  24 NOVEMBER 2026", font=font(SANS_B, 26),
       fill=RED, anchor="ma")
y += 44
d.text((512, y), "THE WORLD TODAY", font=font(SERIF, 66), fill=INK, anchor="ma")
y += 92
d.line([(40, y), (984, y)], fill=INK, width=4)
y += 10
d.text((512, y), "THE DAY'S WORLD NEWS — IN ONE IMAGE",
       font=font(SANS_B, 22), fill=GREY, anchor="ma")
y += 36
d.line([(40, y), (984, y)], fill=INK, width=2)
y += 22

# ---- lead story ----
d.text((40, y), "TOP STORY", font=font(SANS_B, 24), fill=RED)
y += 34
y = para(d, 40, y, "HUAWEI GUILTY OF TRADE-SECRET THEFT AND BANK FRAUD",
         font(SANS_B, 46), 944, leading=56)
y += 8
y = para(d, 40, y, "A US jury convicts the Chinese tech giant of stealing trade secrets "
                   "and bank fraud — but acquits it of racketeering.",
         font(SANS, 25), 944, fill=GREY, leading=32)
y += 26
d.line([(40, y), (984, y)], fill=INK, width=2)
y += 24

# ---- 2x2 grid ----
stories = [
    ("STRAIT OF HORMUZ",
     "FOUR TANKERS HIT MINES",
     "Iran says naval mines struck four tankers as the US blockade standoff deepens."),
    ("GAZA",
     "ISRAEL KILLS HAMAS SECURITY CHIEF",
     "Naeem Abu Nahel among seven killed in Israeli airstrikes on Gaza."),
    ("UKRAINE",
     "RUSSIAN STRIKE HITS FLATS IN ZAPORIZHZHIA",
     "Two killed, 40 wounded, including four children, in an overnight attack."),
    ("BUSINESS",
     "HUANG BACK AS NVIDIA CHIEF",
     "Jensen Huang reinstated as CEO under two weeks after resigning."),
]
col_w, col_x = 452, [40, 532]
row_y, row_h = y, 176
for i, (kick, head, deck) in enumerate(stories):
    cx = col_x[i % 2]
    cy = row_y + (i // 2) * row_h
    d.text((cx, cy), kick, font=font(SANS_B, 20), fill=RED)
    cy += 28
    cy = para(d, cx, cy, head, font(SANS_B, 27), col_w, leading=33)
    cy += 4
    para(d, cx, cy, deck, font(SANS, 21), col_w, fill=GREY, leading=26)
    if i % 2 == 0:
        d.line([(512, row_y + (i // 2) * row_h), (512, row_y + (i // 2) * row_h + row_h - 24)],
               fill=(200, 192, 172), width=2)
    if i < 2:
        d.line([(40, row_y + row_h), (984, row_y + row_h)], fill=(200, 192, 172), width=2)
y = row_y + 2 * row_h + 8
d.line([(40, y), (984, y)], fill=INK, width=2)
y += 22

# ---- bottom strip: two short stories ----
d.text((40, y), "SPORT", font=font(SANS_B, 20), fill=RED)
y2 = para(d, 40, y + 28, "SENEGAL REGAIN AFRICA CUP",
          font(SANS_B, 22), 452, leading=27)
para(d, 40, y2 + 4, "A sports court appeal hands Senegal the title.",
     font(SANS, 19), 452, fill=GREY, leading=24)
d.text((532, y), "TURKIYE", font=font(SANS_B, 20), fill=RED)
y2 = para(d, 532, y + 28, "HELICOPTER CRASH KILLS FIVE",
          font(SANS_B, 22), 452, leading=27)
para(d, 532, y2 + 4, "Turkish Army training flight down.",
     font(SANS, 19), 452, fill=GREY, leading=24)
d.line([(512, y), (512, y + 100)], fill=(200, 192, 172), width=2)

# ---- footer ----
d.line([(40, 968), (984, 968)], fill=INK, width=2)
d.text((512, 978), "24 NOVEMBER 2026  ·  ONE IMAGE, THE DAY'S WORLD NEWS",
       font=font(SANS_B, 19), fill=GREY, anchor="ma")

img.save("entry.png", "PNG", optimize=True)
print("wrote entry.png", img.size)
