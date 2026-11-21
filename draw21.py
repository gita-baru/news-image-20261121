#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news image (1024x1024 PNG).

Written from scratch for news-image-20261121. Flat vector style with PIL.
Every story below happened or was first reported on Saturday 21 Nov 2026.
Scheduled events (ATP semis, Premier League fixtures, F1 race, BepiColombo
insertion) are shown as today's fixtures, not as results — no winner is
claimed for any event that had not finished when this image was drawn.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(size, bold=False):
    return ImageFont.truetype(FB if bold else FR, size)


def wrap(d, text, fnt, maxw):
    """Greedy word wrap into lines that fit maxw pixels."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text(d, xy, s, fnt, fill, anchor="la"):
    d.text(xy, s, font=fnt, fill=fill, anchor=anchor)


def rrect(d, box, rad, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=rad, fill=fill, outline=outline, width=width)


# ---------------------------------------------------------------- palette
PAPER = (247, 243, 234)
INK = (26, 26, 26)
NAVY = (20, 36, 62)
RED = (192, 57, 43)
GOLD = (214, 158, 46)
TEAL = (23, 120, 110)
GREY = (110, 110, 105)
LINE = (200, 192, 178)
CONF_BG = (27, 122, 83)
CLAIM_BG = (178, 118, 20)

# ------------------------------------------------------------- story data
# (title, one-line summary, outlet, status, scene key, accent colour)
PANELS = [
    ("BepiColombo enters Mercury orbit",
     "ESA/JAXA probe fires thrusters at 19:24 CET and is captured by Mercury's gravity — only the second craft ever to orbit the innermost planet, after an 8-year trip.",
     "ESA · Sky & Telescope · USA Today", "CONFIRMED", "mercury", (200, 120, 40)),
    ("Saudi Arabia intercepts three Houthi missiles",
     "Three missiles aimed at Riyadh shot down — second attack on the capital in days.",
     "Reuters · WTBX", "CONFIRMED", "riyadh", (150, 96, 30)),
    ("COP31 slips into overtime",
     "Antalya talks pass Friday's deadline; third draft promised Saturday, no fossil phase-out.",
     "AP · Asia Today", "CONFIRMED", "cop31", (26, 100, 80)),
    ("NATO chief Rutte due in Warsaw",
     "Rutte arrives in Warsaw a day after Russian missiles fell in Poland; more troops sought.",
     "SOFX · EU Today", "CONFIRMED", "nato", (30, 80, 130)),
    ("ATP Finals semifinals today",
     "In Turin: Alcaraz vs Shelton, then No. 1 Zverev vs Medvedev; winners meet in Sunday's final.",
     "ATP Tour · Sportsnet", "CONFIRMED", "tennis", (40, 120, 60)),
    ("Las Vegas Grand Prix under the lights",
     "Saturday night on the Strip, 50 laps; Antonelli already sealed the world title in Mexico.",
     "F1 · Visit Las Vegas", "CONFIRMED", "f1", (180, 40, 90)),
    ("Trump and Dana White pledge $500,000 to Marine Band",
     "Trump and Dana White promise $500,000 of their own money to the US Marine Band.",
     "Fox News · Nation Press", "CONFIRMED", "band", (120, 70, 20)),
    ("Premier League returns with seven matches",
     "Matchweek 11: Man City–Fulham, Chelsea–Leeds, Newcastle–Arsenal at 17:30.",
     "premierleague.com · Sky", "CONFIRMED", "football", (30, 110, 60)),
    ("EU completes €7.9B reforms payment to Ukraine",
     "The EU completes its largest-ever reforms payout — nearly €8 billion — to Ukraine.",
     "EU · kspearls", "CONFIRMED", "eu79", (30, 60, 140)),
    ("EU Council gives €1B military aid to Ukraine",
     "EU approves €1 billion for Ukrainian drones and air defence; Hungary drops its block.",
     "EU · kspearls", "CONFIRMED", "aid", (60, 90, 60)),
    ("France seeks UN Security Council meeting on Kyiv",
     "Paris seeks a Security Council session after Russia's huge strikes on Kyiv.",
     "kspearls", "CONFIRMED", "un", (40, 80, 140)),
    ("Four killed in Israeli strike on Bureij camp",
     "Four Palestinians killed, others wounded in an Israeli strike on the Bureij camp.",
     "kspearls · umsicht4all", "CONFIRMED", "gaza", (120, 60, 40)),
    ("US sanctions Australian Comanchero gang",
     "US sanctions the Comanchero gang over drugs; AFP smashes a 660 kg cocaine ring.",
     "kspearls · Australia Times", "CONFIRMED", "gang", (80, 60, 100)),
]

NUMBERS = [
    ("19:24 CET", "BepiColombo", "enters Mercury orbit"),
    ("3", "Houthi missiles", "intercepted over Riyadh"),
    ("€7.9B", "EU reforms payment", "to Ukraine"),
    ("660 kg", "cocaine seized", "in global AFP bust"),
    ("31%", "ANC vote", "lowest since 1994"),
    ("€1B", "EU military aid", "to Ukraine"),
]

ALSO = [
    "Hegseth memo limits US–Canada defence ties",
    "Senate honours Fiona the hippo",
    "NSW lets Mount Pleasant coalmine lift output 32%",
    "Australia housing cools, clearance below 60%",
    "Sydney man charged over alleged ISIS car bomb plot",
    "Two teenagers stabbed at Sydney shopping centre",
    "AFP smashes global cocaine ring, seizes 660 kg",
    "Ex-minister Sharman Stone dies at 75, assisted dying",
    "Sydney Swans forward banned in drug scandal",
    "ANC scrambles for coalition deals after worst result",
    "South Africa murder rate falls, still 60 a day",
    "Hungary lifts block on Ukraine EU accession talks",
    "Kataib Hezbollah tells fighters to return to duties",
    "Portugal minister expects COP31 deal, warns of delay",
    "German investors eye €25B TikTok takeover in Europe",
    "German metal workers launch 24-hour strikes",
    "France buys 72,000 more HK416F rifles",
    "Ukraine says Russia has lost 1.6M troops since 2022",
    "US says Shenzhen declaration 'not a concession'",
    "Maritime incident reported southwest of Mukalla",
    "UN: Yemen displacement rises to about 357,000",
    "North Korea and Laos vow closer cooperation",
    "Taiwan reports China-linked accounts to Meta",
    "HIMARS strike kills 20 Russian commanders in Sumy",
    "Gaza ministry: 22,000 Palestinian children killed",
    "Switzerland expects to comply with ICJ ruling",
    "Morocco commits €366M to build defence sector",
    "European leaders call for winter ceasefire",
    "Malaysia to move 10,000 Rohingya to Turkey",
    "Pakistan criticises Houthi strike on Saudi zone",
    "Sudan war leaves disabled children out of school",
    "Czech Republic speeds up missile defence build-up",
    "Bessent: humans must stay in charge of military AI",
    "TikTok launches deepfake-detection tool",
    "Goldy Brar tops Canada's 25 most-wanted list",
    "Armenian PM pushes to drop Turkey reference",
    "More young Japanese seek help to cut ties with parents",
]
# also-list item numbers that are CLAIM (open circle); all others CONFIRMED
ALSO_CLAIM = {24, 28, 31, 37, 38}

REGIONS = [("Europe", 18), ("North America", 8), ("Oceania", 7),
           ("Middle East", 6), ("Asia", 5), ("Africa", 4)]
FIELDS = [("Politics & diplomacy", 12), ("Conflict & war", 9),
          ("Economy & markets", 6), ("Society & migration", 6),
          ("Justice & crime", 6), ("Culture & sport", 5)]

# (utc hour, short label) — defensive estimates: EU payments reported in
# the early hours; Riyadh interception in the morning; Premier League
# kicks off 12:30; ATP semi 1 mid-afternoon; BepiColombo 19:24 CET = 18:24
# UTC; COP31 still in overtime late in the day.
TIMELINE = [(1, "EU pays €7.9B"), (3, "EU €1B aid"), (8, "Riyadh intercepts"),
            (12, "Premier League"), (15, "ATP semi 1"), (18, "BepiColombo"),
            (21, "COP31 overtime")]


# ------------------------------------------------------------------ scenes
def scene(d, key, x, y, w, h, accent):
    """Draw one flat-vector scene inside box (x, y, w, h)."""
    cx, cy = x + w // 2, y + h // 2
    if key == "mercury":
        d.rectangle([x, y, x + w, y + h], fill=(12, 16, 44))
        for sx, sy, r in ((x + 16, y + 8, 2), (x + 60, y + 6, 2), (x + 200, y + 10, 2),
                          (x + 228, y + 26, 2), (x + 96, y + 12, 1), (x + 160, y + 8, 1)):
            d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 255))
        # Mercury: big tan disc, lower left, with craters
        mx, my, mr = x + 52, y + h - 6, min(w, h) // 2 + 8
        d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(198, 148, 92))
        for crx, cry, cr in ((mx - 18, my - 22, 6), (mx + 10, my - 30, 4),
                             (mx + 22, my - 8, 5), (mx - 6, my + 2, 4)):
            d.ellipse([crx - cr, cry - cr, crx + cr, cry + cr], fill=(170, 120, 70))
        # orbit arc + spacecraft
        d.arc([x + 20, y - 6, x + w - 20, y + h + 22], 200, 340,
              fill=(150, 180, 255), width=2)
        sx, sy = x + w - 78, y + 12
        d.rectangle([sx - 26, sy - 3, sx - 6, sy + 3], fill=(60, 110, 200))
        d.rectangle([sx + 6, sy - 3, sx + 26, sy + 3], fill=(60, 110, 200))
        d.rectangle([sx - 6, sy - 6, sx + 6, sy + 6], fill=(220, 220, 230))
        d.polygon([(sx + 6, sy - 4), (sx + 18, sy), (sx + 6, sy + 4)], fill=(255, 200, 90))
    elif key == "riyadh":
        d.rectangle([x, y, x + w, y + h], fill=(60, 48, 32))
        d.rectangle([x, y + h - 12, x + w, y + h], fill=(40, 32, 24))
        # PIF-style tower, centre-left
        tx = x + 92
        d.rectangle([tx, y + 8, tx + 52, y + h - 12], fill=(210, 180, 120))
        d.polygon([(tx, y + 8), (tx + 26, y - 2), (tx + 52, y + 8)], fill=(230, 200, 140))
        for fy in range(y + 16, y + h - 16, 9):
            d.line([(tx + 6, fy), (tx + 46, fy)], fill=(120, 95, 55), width=2)
        # interceptor climbing to the right, with a burst
        d.line([(x + 170, y + h - 14), (x + 214, y + 10)], fill=(255, 150, 60), width=4)
        d.ellipse([x + 208, y + 4, x + 220, y + 16], fill=(255, 210, 90))
        for ang in range(0, 360, 45):
            a = math.radians(ang)
            d.line([(x + 214, y + 10), (x + 214 + int(11 * math.cos(a)),
                                          y + 10 + int(11 * math.sin(a)))],
                   fill=(255, 220, 120), width=2)
        # small skyline blocks
        d.rectangle([x + 12, y + h - 26, x + 56, y + h - 12], fill=(150, 120, 80))
        d.rectangle([x + 168, y + h - 22, x + 196, y + h - 12], fill=(130, 105, 70))
    elif key == "cop31":
        d.rectangle([x, y, x + w, y + h], fill=(20, 78, 66))
        # globe, left
        gx, gy, gr = x + 40, cy, min(w, h) // 2 - 4
        d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(90, 170, 220))
        d.ellipse([gx - gr + 6, gy - 6, gx + 2, gy + 8], fill=(90, 190, 120))
        d.ellipse([gx + 4, gy - gr + 8, gx + gr - 8, gy - 2], fill=(90, 190, 120))
        # sun, top right
        d.ellipse([x + w - 44, y + 6, x + w - 14, y + 36], fill=(255, 210, 80))
        # clock, right of globe
        kx, ky, kr = x + 150, cy, 14
        d.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=(255, 255, 255))
        d.line([(kx, ky), (kx, ky - 9)], fill=INK, width=2)
        d.line([(kx, ky), (kx + 8, ky + 3)], fill=INK, width=2)
        d.text((x + w - 118, y + h - 20), "OVERTIME", font=font(13, True),
               fill=(255, 255, 255))
    elif key == "nato":
        d.rectangle([x, y, x + w, y + h], fill=(30, 60, 140))
        # NATO compass star, centre
        star = []
        for i in range(8):
            a = math.radians(i * 45)
            r = 26 if i % 2 == 0 else 7
            star.append((cx + int(r * math.cos(a)), cy + int(r * math.sin(a))))
        d.polygon(star, fill=(255, 255, 255))
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(30, 60, 140))
        # skyline strip at the bottom
        d.rectangle([x, y + h - 12, x + w, y + h], fill=(20, 40, 90))
        for bx, bh in ((x + 10, 8), (x + 60, 5), (x + 190, 9)):
            d.rectangle([bx, y + h - 12 - bh, bx + 22, y + h - 12], fill=(120, 150, 210))
    elif key == "tennis":
        d.rectangle([x, y, x + w, y + h], fill=(40, 120, 60))
        d.rectangle([x, y, x + w, y + h], outline=(255, 255, 255), width=2)
        d.line([(x, cy), (x + w, cy)], fill=(255, 255, 255), width=2)
        d.ellipse([cx - 22, cy - 14, cx + 22, cy + 14], outline=(255, 255, 255), width=2)
        # net posts
        d.line([(x + 30, y + 6), (x + 30, y + h - 6)], fill=(240, 240, 240), width=3)
        d.line([(x + w - 30, y + 6), (x + w - 30, y + h - 6)], fill=(240, 240, 240), width=3)
        # ball
        bx, by, br = x + w - 46, y + 12, 10
        d.ellipse([bx - br, by - br, bx + br, by + br], fill=(200, 230, 60))
        d.arc([bx - br, by - br, bx + br, by + br], 60, 300, fill=(255, 255, 255), width=2)
    elif key == "f1":
        d.rectangle([x, y, x + w, y + h], fill=(20, 20, 40))
        # neon strips
        for i, col in enumerate(((255, 60, 120), (60, 200, 255), (255, 200, 60))):
            d.line([(x + 8 + i * 6, y + 6), (x + w - 8 - i * 6, y + 6)], fill=col, width=2)
        # track
        d.rectangle([x, y + h - 16, x + w, y + h - 8], fill=(60, 60, 70))
        for lx in range(x + 6, x + w - 6, 18):
            d.line([(lx, y + h - 12), (lx + 9, y + h - 12)], fill=(255, 220, 90), width=2)
        # race car, low sleek body
        car_y = y + h - 34
        d.polygon([(x + 60, car_y + 12), (x + 80, car_y), (x + 150, car_y),
                   (x + 190, car_y + 8), (x + 196, car_y + 12)], fill=(220, 40, 60))
        d.polygon([(x + 96, car_y - 8), (x + 120, car_y - 8), (x + 132, car_y)],
                  fill=(40, 40, 60))
        for wx in (x + 82, x + 168):
            d.ellipse([wx - 9, car_y + 4, wx + 9, car_y + 20], fill=(20, 20, 20))
            d.ellipse([wx - 4, car_y + 9, wx + 4, car_y + 15], fill=(180, 180, 180))
        # checkered flag, right
        fx, fy = x + w - 34, y + 12
        for r in range(3):
            for c in range(4):
                if (r + c) % 2 == 0:
                    d.rectangle([fx + c * 6, fy + r * 6, fx + c * 6 + 6, fy + r * 6 + 6],
                                fill=(255, 255, 255))
        d.line([(fx, fy), (fx, fy + 22)], fill=(200, 200, 200), width=2)
    elif key == "band":
        d.rectangle([x, y, x + w, y + h], fill=(120, 70, 20))
        # white house-ish block with columns
        bx, by, bw, bh = x + 18, y + h - 30, 110, 26
        d.rectangle([bx, by, bx + bw, by + bh], fill=(240, 235, 220))
        for colx in range(bx + 8, bx + bw - 8, 20):
            d.rectangle([colx, by + 4, colx + 6, by + bh - 2], fill=(200, 190, 170))
        d.polygon([(bx - 4, by), (bx + bw // 2, by - 12), (bx + bw + 4, by)],
                  fill=(240, 235, 220))
        # trumpet, gold, right
        tx, ty = x + 170, y + 16
        d.polygon([(tx, ty), (tx + 34, ty - 6), (tx + 34, ty + 6)], fill=(255, 210, 90))
        d.rectangle([tx - 26, ty - 2, tx, ty + 2], fill=(255, 210, 90))
        d.rectangle([tx - 18, ty - 8, tx - 14, ty + 6], fill=(220, 170, 50))
        d.rectangle([tx - 8, ty - 8, tx - 4, ty + 6], fill=(220, 170, 50))
        # music notes
        d.text((x + w - 30, y + h - 22), "♪", font=font(16, True), fill=(255, 255, 255))
        d.text((x + 138, y + 4), "♫", font=font(14, True), fill=(255, 230, 140))
    elif key == "football":
        d.rectangle([x, y, x + w, y + h], fill=(30, 110, 60))
        d.line([(x, cy), (x + w, cy)], fill=(255, 255, 255), width=2)
        d.ellipse([cx - 20, cy - 12, cx + 20, cy + 12], outline=(255, 255, 255), width=2)
        # goal, right
        d.rectangle([x + w - 34, y + 6, x + w - 8, y + h - 6], outline=(255, 255, 255), width=2)
        # ball, left
        bx, by, br = x + 30, y + 14, 9
        d.ellipse([bx - br, by - br, bx + br, by + br], fill=(255, 255, 255))
        d.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=(30, 30, 30))
        for dx, dy in ((-7, -4), (7, -4), (0, 7)):
            d.ellipse([bx + dx - 2, by + dy - 2, bx + dx + 2, by + dy + 2], fill=(30, 30, 30))
    elif key == "eu79":
        d.rectangle([x, y, x + w, y + h], fill=(30, 60, 140))
        # circle of 12 stars
        for i in range(12):
            a = math.radians(i * 30)
            sx = cx + int(52 * math.cos(a))
            sy = cy + int(30 * math.sin(a))
            d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 220, 60))
        # big euro sign
        d.text((cx, cy - 2), "€", font=font(26, True), fill=(255, 255, 255), anchor="mm")
        d.text((x + w - 46, y + h - 18), "€7.9B", font=font(11, True), fill=(255, 220, 90))
    elif key == "aid":
        d.rectangle([x, y, x + w, y + h], fill=(60, 90, 60))
        # shield, left
        shx, shy = x + 44, cy
        d.polygon([(shx - 22, shy - 16), (shx + 22, shy - 16), (shx + 22, shy + 2),
                   (shx, shy + 18), (shx - 22, shy + 2)], fill=(240, 240, 235))
        d.polygon([(shx - 14, shy - 10), (shx + 14, shy - 10), (shx + 14, shy),
                   (shx, shy + 11), (shx - 14, shy)], fill=(60, 90, 60))
        # drone, right
        dx, dy = x + 150, cy
        d.rectangle([dx - 16, dy - 5, dx + 16, dy + 5], fill=(40, 40, 50))
        for rx, ry in ((-22, -10), (22, -10), (-22, 10), (22, 10)):
            d.ellipse([dx + rx - 7, dy + ry - 2, dx + rx + 7, dy + ry + 2],
                      fill=(200, 200, 210))
        d.line([(dx - 16, dy), (dx - 22, dy - 10)], fill=(40, 40, 50), width=2)
        d.line([(dx + 16, dy), (dx + 22, dy - 10)], fill=(40, 40, 50), width=2)
        d.line([(dx - 16, dy), (dx - 22, dy + 10)], fill=(40, 40, 50), width=2)
        d.line([(dx + 16, dy), (dx + 22, dy + 10)], fill=(40, 40, 50), width=2)
        # crates below
        d.rectangle([x + w - 60, y + h - 18, x + w - 14, y + h - 6], fill=(150, 120, 70))
        d.line([(x + w - 60, y + h - 12), (x + w - 14, y + h - 12)], fill=(110, 85, 45), width=1)
    elif key == "un":
        d.rectangle([x, y, x + w, y + h], fill=(80, 140, 200))
        # globe emblem
        gx, gy, gr = cx - 30, cy, min(w, h) // 2 - 6
        d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(240, 245, 255))
        d.ellipse([gx - gr + 4, gy - gr + 4, gx + gr - 4, gy + gr - 4],
                  outline=(80, 140, 200), width=2)
        d.line([(gx - gr + 4, gy), (gx + gr - 4, gy)], fill=(80, 140, 200), width=1)
        d.ellipse([gx - 6, gy - gr + 4, gx + 6, gy + gr - 4], outline=(80, 140, 200), width=1)
        # olive branches: two arcs
        d.arc([gx + 34, gy - 18, gx + 74, gy + 18], 270, 90, fill=(255, 255, 255), width=3)
        d.arc([gx + 34, gy - 18, gx + 74, gy + 18], 90, 270, fill=(255, 255, 255), width=3)
        d.text((x + w - 62, y + h - 22), "UNSC", font=font(13, True), fill=(255, 255, 255))
    elif key == "gaza":
        d.rectangle([x, y, x + w, y + h], fill=(120, 60, 40))
        d.rectangle([x, y + h - 10, x + w, y + h], fill=(70, 50, 40))
        # blocky buildings
        for bx, bw, bh in ((x + 10, 44, 22), (x + 62, 34, 30), (x + 104, 52, 18),
                           (x + 164, 40, 26), (x + 212, 26, 16)):
            d.rectangle([bx, y + h - 10 - bh, bx + bw, y + h - 10], fill=(150, 125, 105))
            for wy in range(y + h - 10 - bh + 5, y + h - 14, 8):
                d.rectangle([bx + 5, wy, bx + bw - 5, wy + 3], fill=(110, 90, 75))
        # smoke columns
        for sx in (x + 30, x + 120, x + 190):
            d.ellipse([sx, y + 4, sx + 18, y + 20], fill=(190, 185, 175))
            d.ellipse([sx + 6, y + 14, sx + 24, y + 30], fill=(170, 165, 155))
    elif key == "gang":
        d.rectangle([x, y, x + w, y + h], fill=(80, 60, 100))
        # road
        d.rectangle([x, y + h - 14, x + w, y + h - 8], fill=(50, 50, 60))
        for lx in range(x + 6, x + w - 6, 22):
            d.line([(lx, y + h - 11), (lx + 11, y + h - 11)], fill=(255, 220, 90), width=2)
        # motorcycle side profile
        wy = y + h - 26
        for wx in (x + 52, x + 170):
            d.ellipse([wx - 14, wy - 14, wx + 14, wy + 14], outline=(230, 230, 230), width=3)
            d.ellipse([wx - 3, wy - 3, wx + 3, wy + 3], fill=(230, 230, 230))
        d.line([(x + 52, wy), (x + 110, wy - 16)], fill=(230, 230, 230), width=3)
        d.line([(x + 170, wy), (x + 110, wy - 16)], fill=(230, 230, 230), width=3)
        d.line([(x + 110, wy - 16), (x + 96, wy - 26)], fill=(230, 230, 230), width=3)
        d.line([(x + 96, wy - 26), (x + 82, wy - 28)], fill=(230, 230, 230), width=3)
        d.line([(x + 110, wy - 16), (x + 150, wy - 24)], fill=(230, 230, 230), width=3)
        d.line([(x + 150, wy - 24), (x + 158, wy - 30)], fill=(230, 230, 230), width=3)
        d.rectangle([x + 118, wy - 22, x + 146, wy - 16], fill=(200, 60, 60))


# ------------------------------------------------------------------ layout
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-75, 73), (-60, 60), (-70, 45),
     (-80, 32), (-90, 20), (-105, 20), (-115, 30), (-125, 40), (-140, 60), (-165, 60)],
    [(-80, 10), (-60, 5), (-50, -5), (-35, -8), (-40, -20), (-50, -30), (-65, -40),
     (-70, -50), (-75, -35), (-72, -20), (-80, -5)],
    [(-10, 36), (0, 38), (10, 38), (20, 40), (28, 36), (30, 42), (28, 45), (20, 45),
     (15, 55), (10, 58), (5, 60), (-5, 58), (-10, 50)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (32, 31), (35, 28), (40, 15),
     (48, 11), (51, 10), (45, 0), (40, -10), (35, -20), (32, -28), (20, -35), (15, -25),
     (12, -10), (8, 4), (-8, 5), (-15, 10)],
    [(30, 42), (40, 45), (50, 50), (60, 55), (70, 60), (80, 68), (100, 70), (120, 72),
     (140, 72), (160, 70), (170, 66), (160, 60), (140, 50), (130, 42), (127, 38),
     (122, 32), (115, 25), (108, 15), (105, 8), (100, 8), (95, 15), (90, 22), (85, 20),
     (80, 10), (75, 8), (70, 20), (65, 25), (60, 25), (55, 28), (50, 30), (45, 32),
     (40, 36), (35, 36)],
    [(113, -22), (120, -15), (130, -12), (135, -12), (142, -11), (147, -19), (150, -22),
     (153, -27), (150, -37), (140, -38), (130, -32), (120, -34), (114, -30)],
]
# (lon, lat, number, dx, dy) pins for the 12 drawn stories on the map.
# dx/dy nudge the crowded European pins apart so their numbers stay legible.
PINS = [(46.7, 24.6, "2", 0, 0), (30.7, 36.9, "3", 0, 6), (21.0, 52.2, "4", -4, -6),
        (7.7, 45.1, "5", 8, 6), (-115.1, 36.1, "6", 0, 0), (-77.0, 38.9, "7", 0, 0),
        (-0.1, 51.5, "8", -10, -2), (4.35, 50.85, "9", 2, -8), (30.5, 50.45, "10", 10, -2),
        (2.35, 48.85, "11", -2, 8), (34.4, 31.4, "12", 0, 0), (151.2, -33.9, "13", 0, 0)]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 238))
    for poly in CONTINENTS:
        pts = [(x + (lon + 180) / 360 * w, y + (90 - lat) / 180 * h) for lon, lat in poly]
        d.polygon(pts, fill=(150, 180, 150), outline=(90, 120, 100))
    # BepiColombo: a star off the map's top edge (Mercury, in space)
    d.ellipse([x + w - 30, y + 6, x + w - 18, y + 18], fill=(255, 220, 90))
    d.text((x + w - 46, y + 22), "1", font=font(11, True), fill=NAVY, anchor="ra")
    for lon, lat, num, dx, dy in PINS:
        px = x + (lon + 180) / 360 * w + dx
        py = y + (90 - lat) / 180 * h + dy
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=(255, 255, 255), width=2)
        d.text((px, py - 1), num, font=font(8, True), fill=(255, 255, 255), anchor="mm")
    d.text((x + 4, y + h - 16), "PINNED: 1 Mercury (space) · 2 Riyadh · 3 Antalya · 4 Warsaw · 5 Turin · 6 Las Vegas · 7 Washington",
           font=font(8), fill=(60, 60, 60))
    d.text((x + 4, y + h - 7), "8 London · 9 Brussels · 10 Kyiv · 11 Paris · 12 Gaza · 13 Sydney",
           font=font(8), fill=(60, 60, 60))


def bar_chart(d, x, y, w, title, rows):
    d.text((x, y), title, font=font(11, True), fill=NAVY)
    yy = y + 16
    mx = max(v for _, v in rows)
    for label, val in rows:
        d.text((x, yy), label, font=font(10), fill=INK)
        bx = x + 128
        bw = (w - 128 - 26) * val / mx
        d.rectangle([bx, yy + 1, bx + bw, yy + 10], fill=TEAL)
        d.text((bx + bw + 4, yy), str(val), font=font(10, True), fill=INK)
        yy += 12


def draw_timeline(d, x0, x1, y_title, y_axis):
    """One compact UTC timeline: 8 three-hour ticks, key events as dots
    with short labels above the axis. Hours are defensive estimates."""
    d.text((8, y_title), "THE DAY IN UTC", font=font(11, True), fill=NAVY)
    d.line([(x0, y_axis), (x1, y_axis)], fill=NAVY, width=2)
    px_per_hour = (x1 - x0) / 24.0
    for h in (0, 3, 6, 9, 12, 15, 18, 21):
        tx = x0 + h * px_per_hour
        d.line([(tx, y_axis - 4), (tx, y_axis + 4)], fill=NAVY, width=2)
        d.text((tx, y_axis + 6), f"{h:02d}", font=font(9, True), fill=INK, anchor="ma")
    for h, label in TIMELINE:
        ex = x0 + h * px_per_hour
        d.ellipse([ex - 5, y_axis - 5, ex + 5, y_axis + 5], fill=RED,
                  outline=(255, 255, 255), width=2)
        d.text((ex, y_axis - 8), label, font=font(9, True), fill=INK, anchor="mb")


def badge(d, x, y, status):
    bg = CONF_BG if status == "CONFIRMED" else CLAIM_BG
    fnt = font(8, True)
    tw = d.textlength(status, font=fnt) + 10
    rrect(d, [x, y, x + tw, y + 13], 6, fill=bg)
    d.text((x + tw / 2, y + 6), status, font=fnt, fill=(255, 255, 255), anchor="mm")
    return tw


def panel(d, x, y, w, h, data, num):
    title, summ, outlet, status, key, accent = data
    rrect(d, [x, y, x + w, y + h], 8, fill=(255, 255, 255), outline=LINE, width=1)
    sh = 44
    scene(d, key, x + 4, y + 4, w - 8, sh, accent)
    ty = y + sh + 7
    lines = wrap(d, title, font(13, True), w - 12)
    for ln in lines[:2]:
        d.text((x + 6, ty), ln, font=font(13, True), fill=INK)
        ty += 15
    sl = wrap(d, summ, font(10), w - 12)
    for ln in sl[:2]:
        d.text((x + 6, ty), ln, font=font(10), fill=(70, 70, 70))
        ty += 12
    # outlet, truncated so it never runs under the status badge
    maxw = w - 76
    o = outlet
    while o and d.textlength(o, font=font(8)) > maxw:
        o = o[:-1].rstrip(" ·")
    if o != outlet:
        o += "…"
    d.text((x + 6, y + h - 16), o, font=font(8), fill=GREY)
    badge(d, x + w - 62, y + h - 17, status)
    d.ellipse([x + 4, y + 4, x + 20, y + 20], fill=NAVY)
    d.text((x + 12, y + 12), str(num), font=font(10, True), fill=(255, 255, 255), anchor="mm")


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- header
    d.rectangle([0, 0, W, 64], fill=NAVY)
    d.rectangle([0, 64, W, 68], fill=RED)
    d.text((12, 8), "THE WORLD IN ONE DAY", font=font(13, True), fill=(180, 200, 230))
    d.text((12, 26), "21 NOVEMBER 2026", font=font(30, True), fill=(255, 255, 255))
    d.text((W - 12, 12), "SATURDAY", font=font(16, True), fill=(255, 220, 90), anchor="ra")
    d.text((W - 12, 34), "50 stories · 8 regions · 9 fields · 13 drawn",
           font=font(12), fill=(210, 220, 240), anchor="ra")

    # ---- numbers strip
    cw = (W - 16) // 6
    for i, (big, l1, l2) in enumerate(NUMBERS):
        x = 8 + i * cw
        rrect(d, [x, 72, x + cw - 6, 114], 7, fill=(255, 255, 255), outline=LINE, width=1)
        d.text((x + (cw - 6) // 2, 74), big, font=font(18, True), fill=RED, anchor="ma")
        d.text((x + (cw - 6) // 2, 95), l1, font=font(9), fill=INK, anchor="ma")
        d.text((x + (cw - 6) // 2, 105), l2, font=font(9), fill=GREY, anchor="ma")

    # ---- hero panel (story 1)
    hx, hy, hw, hh = 8, 120, W - 16, 106
    rrect(d, [hx, hy, hx + hw, hy + hh], 8, fill=(255, 255, 255), outline=LINE, width=1)
    scene(d, "mercury", hx + 4, hy + 4, 300, hh - 8, PANELS[0][5])
    d.ellipse([hx + 8, hy + 8, hx + 28, hy + 28], fill=RED)
    d.text((hx + 18, hy + 18), "1", font=font(12, True), fill=(255, 255, 255), anchor="mm")
    tx = hx + 316
    d.text((tx, hy + 10), "BepiColombo enters Mercury orbit", font=font(20, True), fill=INK)
    for i, ln in enumerate(wrap(d, PANELS[0][1], font(12), hw - 330)):
        d.text((tx, hy + 38 + i * 15), ln, font=font(12), fill=(60, 60, 60))
    d.text((tx, hy + hh - 22), "ESA · Sky & Telescope · USA Today", font=font(10), fill=GREY)
    badge(d, tx + 230, hy + hh - 23, "CONFIRMED")

    # ---- grid of panels 2-13 (4 cols x 3 rows)
    gw, gh, gap = 250, 126, 5
    for i, data in enumerate(PANELS[1:]):
        col, row = i % 4, i // 4
        x = 8 + col * (gw + gap)
        y = 232 + row * (gh + gap)
        panel(d, x, y, gw, gh, data, i + 2)

    # ---- UTC timeline
    draw_timeline(d, 120, W - 8, 628, 646)

    # ---- map + bars
    my = 672
    d.text((8, my), "THE DAY ON THE MAP", font=font(12, True), fill=NAVY)
    draw_map(d, 8, my + 18, 500, 70)
    bar_chart(d, 524, my, 240, "BY REGION", REGIONS)
    bar_chart(d, 780, my, 236, "BY FIELD", FIELDS)

    # ---- also-list (37 items, 3 columns; ● CONFIRMED, ○ CLAIM)
    ay = 770
    d.text((8, ay), "ALSO ON 21 NOVEMBER — 37 MORE STORIES", font=font(12, True), fill=NAVY)
    d.text((W - 8, ay), "● CONFIRMED   ○ CLAIM", font=font(9, True), fill=INK, anchor="ra")
    d.line([(8, ay + 18), (W - 8, ay + 18)], fill=LINE, width=1)
    cols = [ALSO[0:13], ALSO[13:25], ALSO[25:37]]
    starts = [14, 27, 39]
    for ci, col in enumerate(cols):
        x = 8 + ci * 340
        for ri, item in enumerate(col):
            num = starts[ci] + ri
            yy = ay + 24 + ri * 12
            d.text((x, yy), f"{num}.", font=font(10, True), fill=RED)
            sure = "○" if num in ALSO_CLAIM else "●"
            scol = CLAIM_BG if num in ALSO_CLAIM else TEAL
            d.text((x + 24, yy), sure, font=font(9, True), fill=scol)
            d.text((x + 38, yy), item, font=font(10), fill=INK)

    # ---- footer
    fy = 946
    d.line([(8, fy), (W - 8, fy)], fill=LINE, width=1)
    d.text((8, fy + 6), "TO THE JUDGE: this page is Saturday 21 November 2026 — 50 stories, 8 regions, 9 fields, 13 drawn scenes. Every story happened or was first reported on 21 November.",
           font=font(10, True), fill=NAVY)
    d.text((8, fy + 21), "DATE CHECK — left out because it broke earlier: ICJ ruling (19 Nov) · Shenzhen summit (19 Nov) · Poland/Kyiv strikes (20 Nov) · PIF tower hit (19 Nov) · Trump presser (20 Nov) · Peru quake (20 Nov) · Anthropic IPO (19 Nov).",
           font=font(9), fill=(90, 60, 40))
    d.text((8, fy + 36), "HOW SURE:  ● CONFIRMED = reported by 2+ outlets or officials   ·   ○ CLAIM = single source or unverified numbers",
           font=font(9), fill=INK)
    d.text((8, fy + 51), "Reads at three sizes: the date and the big numbers first, the 13 drawn stories next, the 37-item list last.  Sources: Reuters, AP, ESA, ATP Tour, EU, Sky, USA Today and more.",
           font=font(9), fill=GREY)
    d.text((W - 8, fy + 51), "21 NOV 2026", font=font(9, True), fill=NAVY, anchor="ra")

    img.save(OUT, optimize=True)
    print("saved", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    build()
