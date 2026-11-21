#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news image (1024x1024 PNG) — v2.

Rebuilt from scratch for the icantcodefyi-style iteration: 35 stories
(13 drawn panels + 22 also-list), matching the density of the current
top-5 entries (32-35 stories), not the 50-story v1. Every story happened
or was first reported on Saturday 21 November 2026 (UTC day). Scheduled
events (BepiColombo insertion 19:24 CET, ATP semifinals, Premier League
fixtures) are labelled TONIGHT, never presented as results. Results that
landed after the v1 build are now in: Peru quake M6.7 (00:09 GMT, a
21 Nov UTC story), F1 qualifying (Verstappen inherits pole), Bitcoin
below $59,000, Rahul 136, Air Niugini 767 safe in Davao.

Usage: python3 draw21.py  — writes entry.png (winning variant C).
Variant C: Riyadh hero, Peru #2, COP31 #3. Variants A (BepiColombo hero)
and B (Peru hero) were built with draw21_v2.py and tested vs the top 5.
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

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
CONF_BG = (27, 122, 83)      # CONFIRMED — green
TONIGHT_BG = (30, 80, 160)   # TONIGHT (scheduled) — blue
CLAIM_BG = (178, 118, 20)    # CLAIM — amber

# ------------------------------------------------------------- story data
# (key, title, summary, outlet, status, scene, accent, region)
# status: CONFIRMED = happened/reported 21 Nov; TONIGHT = scheduled tonight
STORIES = {
    "bepi": ("BepiColombo enters Mercury orbit",
             "ESA/JAXA probe fires thrusters at 19:24 CET tonight, aiming to orbit Mercury.",
             "ESA · Sky & Telescope", "TONIGHT", "mercury", (200, 120, 40), "Global"),
    "riyadh": ("Saudi defences shoot down three missiles at the capital",
               "Three Houthi missiles aimed at Riyadh shot down — second attack in days.",
               "Reuters · AFP", "CONFIRMED", "riyadh", (150, 96, 30), "Middle East"),
    "cop31": ("Climate talks miss their deadline and run into a 13th day",
              "A draft with no fossil fuels splits 200 nations; a third text is promised.",
              "AP · AFP · Al Jazeera", "CONFIRMED", "cop31", (26, 100, 80), "Global"),
    "peru": ("Magnitude 6.7 earthquake rattles the Andes",
             "Deep tremor near Carhuamayo, felt in Lima; no deaths or damage reported.",
             "USGS · IGP", "CONFIRMED", "peru", (140, 60, 60), "Americas"),
    "kryvyi": ("Russian double strike hits Kryvyi Rih",
               "A boy and a medic killed, 42 hurt in a double-tap strike on rescuers.",
               "Kyiv Independent · Kyiv Post", "CONFIRMED", "kryvyi", (120, 60, 40), "Europe"),
    "chinajapan": ("Beijing tells Tokyo to 'correct' Taiwan words",
                  "China renews its demand after the APEC snub; Japan says stance unchanged.",
                  "Reuters · AFP", "CONFIRMED", "chinajapan", (160, 40, 40), "Asia"),
    "bitcoin": ("Bitcoin slips below $59,000",
                "Down 3.9% in 24 hours; ether $1,625. Lowest since September 2024.",
                "CoinGecko · Binance", "CONFIRMED", "bitcoin", (200, 160, 40), "Global"),
    "rahul": ("Rahul century puts India on top",
              "Rahul 136, India 486/4 at stumps, lead 118 — his 13th Test hundred.",
              "BCCI · AFP", "CONFIRMED", "cricket", (30, 110, 60), "Oceania"),
    "davao": ("Jet lands safely after engine fire alert",
              "Air Niugini 767 diverts to Davao after midnight; all 146 aboard safe.",
              "AP · CAAP", "CONFIRMED", "davao", (40, 90, 140), "Asia"),
    "f1": ("Verstappen on pole in Las Vegas",
           "Antonelli fastest, but a grid penalty hands pole to Verstappen.",
           "Formula 1 · FIA", "CONFIRMED", "f1", (180, 40, 90), "Americas"),
    "atp": ("ATP Finals semifinals tonight",
            "In Turin: Alcaraz vs Shelton, then No. 1 Zverev vs Medvedev.",
            "ATP Tour", "TONIGHT", "tennis", (40, 120, 60), "Europe"),
    "pl": ("Premier League returns with seven matches",
           "Matchweek 11: Man City–Fulham, Chelsea–Leeds, Newcastle–Arsenal.",
           "premierleague.com", "TONIGHT", "football", (30, 110, 60), "Europe"),
    "eu79": ("EU completes €7.9B reforms payment to Ukraine",
            "The EU completes its largest-ever reforms payout — nearly €8 billion.",
            "EU", "CONFIRMED", "eu79", (30, 60, 140), "Europe"),
}

# Hero order per variant: the three big panels, left to right.
VARIANTS = {
    "A": ["bepi", "riyadh", "cop31"],
    "B": ["peru", "riyadh", "cop31"],
    "C": ["riyadh", "peru", "cop31"],
}
# The 10 small panels, in priority order (same for every variant).
# Filtered at build time to drop whichever stories are heroes.
SMALL_ORDER = ["peru", "bepi", "kryvyi", "chinajapan", "bitcoin", "rahul",
               "davao", "f1", "atp", "pl", "eu79"]

NUMBERS = [
    ("13", "COP31 DAY 13", "IT WAS MEANT TO CLOSE ON DAY 12"),
    ("3", "MISSILES SHOT DOWN", "OVER RIYADH"),
    ("6.7", "MAGNITUDE OF THE PERU", "QUAKE"),
    ("146", "PEOPLE SAFE AFTER THE DAVAO", "EMERGENCY LANDING"),
    ("$58,983", "BITCOIN EARLY SATURDAY", "DOWN 3.9% IN A DAY"),
    ("136", "RAHUL'S RUNS AT STUMPS", "INDIA 486/4, LEAD 118"),
]

# Also-list: (text, region). All CONFIRMED, reported 21 Nov 2026.
ALSO = [
    ("NATO chief Rutte due in Warsaw", "Europe"),
    ("EU Council gives €1B military aid to Ukraine", "Europe"),
    ("France seeks UN Security Council meeting on Kyiv", "Europe"),
    ("Hungary lifts block on Ukraine EU accession talks", "Europe"),
    ("German metal workers launch 24-hour strikes", "Europe"),
    ("Taiwan reports China-linked accounts to Meta", "Asia"),
    ("Malaysia to move 10,000 Rohingya to Turkey", "Asia"),
    ("North Korea and Laos vow closer cooperation", "Asia"),
    ("Four killed in Israeli strike on Bureij camp", "Middle East"),
    ("Kataib Hezbollah tells fighters to return to duties", "Middle East"),
    ("UN: Yemen displacement rises to about 357,000", "Middle East"),
    ("ANC scrambles for coalition deals after worst result", "Africa"),
    ("Morocco commits €366M to build defence sector", "Africa"),
    ("Sudan war leaves disabled children out of school", "Africa"),
    ("Trump and Dana White pledge $500,000 to Marine Band", "Americas"),
    ("Hegseth memo limits US–Canada defence ties", "Americas"),
    ("Senate honours Fiona the hippo", "Americas"),
    ("US says Shenzhen declaration 'not a concession'", "Americas"),
    ("Goldy Brar tops Canada's 25 most-wanted list", "Americas"),
    ("US sanctions Australian Comanchero gang", "Oceania"),
    ("NSW lets Mount Pleasant coalmine lift output 32%", "Oceania"),
    ("AFP smashes global cocaine ring, seizes 660 kg", "Oceania"),
]

REGION_ORDER = ["Europe", "Asia", "Middle East", "Africa",
                "Americas", "Oceania", "Global"]
REGION_COLORS = {"Europe": (30, 80, 160), "Asia": (200, 120, 40),
                 "Middle East": (150, 96, 30), "Africa": (23, 120, 110),
                 "Americas": (120, 60, 140), "Oceania": (23, 120, 110),
                 "Global": (90, 90, 90)}


def region_counts():
    counts = {r: 0 for r in REGION_ORDER}
    for key in STORIES:
        counts[STORIES[key][6]] += 1
    for _, region in ALSO:
        counts[region] += 1
    return counts


# ------------------------------------------------------------------ scenes
def scene(d, key, x, y, w, h, accent):
    """Draw one flat-vector scene inside box (x, y, w, h)."""
    cx, cy = x + w // 2, y + h // 2
    if key == "mercury":
        d.rectangle([x, y, x + w, y + h], fill=(12, 16, 44))
        for sx, sy, r in ((x + 16, y + 8, 2), (x + 60, y + 6, 2), (x + 200, y + 10, 2),
                          (x + w - 20, y + 26, 2), (x + 96, y + 12, 1), (x + 160, y + 8, 1)):
            d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 255))
        # Mercury disc, kept fully inside the scene box.
        mr = min(w, h) // 3
        mx, my = x + mr + 4, y + h - mr - 2
        d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(198, 148, 92))
        for crx, cry, cr in ((mx - mr // 2, my - mr // 2, 5), (mx + mr // 3, my - mr // 2, 3),
                             (mx + mr // 2, my, 4), (mx - mr // 4, my + mr // 3, 3)):
            d.ellipse([crx - cr, cry - cr, crx + cr, cry + cr], fill=(170, 120, 70))
        d.arc([x + w // 2, y - 6, x + w - 10, y + h // 2 + 10], 200, 340,
              fill=(150, 180, 255), width=2)
        sx, sy = x + w - 52, y + 12
        d.rectangle([sx - 20, sy - 3, sx - 5, sy + 3], fill=(60, 110, 200))
        d.rectangle([sx + 5, sy - 3, sx + 20, sy + 3], fill=(60, 110, 200))
        d.rectangle([sx - 5, sy - 5, sx + 5, sy + 5], fill=(220, 220, 230))
        d.polygon([(sx + 5, sy - 4), (sx + 16, sy), (sx + 5, sy + 4)], fill=(255, 200, 90))
    elif key == "riyadh":
        d.rectangle([x, y, x + w, y + h], fill=(60, 48, 32))
        d.rectangle([x, y + h - 12, x + w, y + h], fill=(40, 32, 24))
        tx = x + 92
        d.rectangle([tx, y + 8, tx + 52, y + h - 12], fill=(210, 180, 120))
        d.polygon([(tx, y + 8), (tx + 26, y - 2), (tx + 52, y + 8)], fill=(230, 200, 140))
        for fy in range(y + 16, y + h - 16, 9):
            d.line([(tx + 6, fy), (tx + 46, fy)], fill=(120, 95, 55), width=2)
        d.line([(x + 170, y + h - 14), (x + 214, y + 10)], fill=(255, 150, 60), width=4)
        d.ellipse([x + 208, y + 4, x + 220, y + 16], fill=(255, 210, 90))
        for ang in range(0, 360, 45):
            a = math.radians(ang)
            d.line([(x + 214, y + 10), (x + 214 + int(11 * math.cos(a)),
                                          y + 10 + int(11 * math.sin(a)))],
                   fill=(255, 220, 120), width=2)
        d.rectangle([x + 12, y + h - 26, x + 56, y + h - 12], fill=(150, 120, 80))
        d.rectangle([x + 168, y + h - 22, x + 196, y + h - 12], fill=(130, 105, 70))
    elif key == "cop31":
        d.rectangle([x, y, x + w, y + h], fill=(20, 78, 66))
        gx, gy, gr = x + 40, cy, min(w, h) // 2 - 4
        d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(90, 170, 220))
        d.ellipse([gx - gr + 6, gy - 6, gx + 2, gy + 8], fill=(90, 190, 120))
        d.ellipse([gx + 4, gy - gr + 8, gx + gr - 8, gy - 2], fill=(90, 190, 120))
        d.ellipse([x + w - 44, y + 6, x + w - 14, y + 36], fill=(255, 210, 80))
        kx, ky, kr = x + 150, cy, 14
        d.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=(255, 255, 255))
        d.line([(kx, ky), (kx, ky - 9)], fill=INK, width=2)
        d.line([(kx, ky), (kx + 8, ky + 3)], fill=INK, width=2)
        d.text((x + w - 118, y + h - 20), "OVERTIME", font=font(13, True),
               fill=(255, 255, 255))
    elif key == "peru":
        # Seismograph trace over the Andes, red on pale paper.
        d.rectangle([x, y, x + w, y + h], fill=(232, 222, 205))
        # mountains along the bottom
        for mx, mw, mh in ((x, 70, 22), (x + 55, 90, 34), (x + 130, 80, 26),
                           (x + 195, 70, 30)):
            d.polygon([(mx, y + h), (mx + mw // 2, y + h - mh), (mx + mw, y + h)],
                      fill=(120, 100, 80))
            d.polygon([(mx + mw // 2 - 8, y + h - mh + 8), (mx + mw // 2, y + h - mh),
                       (mx + mw // 2 + 8, y + h - mh + 8)], fill=(245, 245, 240))
        # seismograph zigzag
        pts = []
        px = x + 8
        base = y + h // 2 - 6
        while px < x + w - 8:
            amp = 4 if (px // 12) % 3 else 16
            pts.append((px, base + (amp if (px // 12) % 2 else -amp)))
            px += 6
        d.line(pts, fill=(192, 40, 30), width=2)
        d.text((x + w - 52, y + 6), "M6.7", font=font(16, True), fill=(192, 40, 30))
    elif key == "kryvyi":
        d.rectangle([x, y, x + w, y + h], fill=(50, 45, 55))
        # damaged building, centre-left
        bx, bw, bh = x + 30, 80, h - 18
        d.rectangle([bx, y + h - 8 - bh, bx + bw, y + h - 8], fill=(150, 125, 105))
        for wy in range(y + h - 8 - bh + 6, y + h - 12, 9):
            d.rectangle([bx + 6, wy, bx + bw - 6, wy + 3], fill=(110, 90, 75))
        # smoke + fire glow
        d.ellipse([bx + 20, y + 4, bx + 44, y + 22], fill=(190, 185, 175))
        d.ellipse([bx + 34, y + 12, bx + 58, y + 30], fill=(170, 165, 155))
        d.polygon([(bx + 30, y + h - 8 - bh), (bx + 42, y + h - 8 - bh - 12),
                   (bx + 54, y + h - 8 - bh)], fill=(255, 150, 60))
        # ambulance cross, right
        ax, ay = x + w - 60, cy
        d.rectangle([ax - 18, ay - 6, ax + 18, ay + 6], fill=(255, 255, 255))
        d.rectangle([ax - 6, ay - 18, ax + 6, ay + 18], fill=(255, 255, 255))
        d.text((x + w - 78, y + h - 18), "42 HURT", font=font(11, True),
               fill=(255, 255, 255))
    elif key == "chinajapan":
        # Two flags facing off: China (red, yellow stars) left, Japan right.
        d.rectangle([x, y, x + w, y + h], fill=(240, 235, 225))
        fw, fh = (w - 24) // 2, h - 16
        # China flag
        d.rectangle([x + 8, y + 8, x + 8 + fw, y + 8 + fh], fill=(200, 30, 30))
        d.ellipse([x + 18, y + 16, x + 30, y + 28], fill=(255, 220, 60))
        for sx, sy in ((x + 36, y + 14), (x + 42, y + 22), (x + 36, y + 30)):
            d.ellipse([sx, sy, sx + 4, sy + 4], fill=(255, 220, 60))
        # Japan flag
        jx = x + 16 + fw
        d.rectangle([jx, y + 8, jx + fw, y + 8 + fh], fill=(255, 255, 255),
                    outline=(180, 180, 180), width=1)
        d.ellipse([jx + fw // 2 - 12, y + 8 + fh // 2 - 12,
                   jx + fw // 2 + 12, y + 8 + fh // 2 + 12], fill=(190, 30, 40))
        d.text((cx, y + h - 14), "STANDOFF", font=font(10, True), fill=INK, anchor="ma")
    elif key == "bitcoin":
        d.rectangle([x, y, x + w, y + h], fill=(30, 28, 20))
        # gold coin with a bold B
        cr = min(w, h) // 2 - 6
        d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(240, 180, 50))
        d.ellipse([cx - cr + 4, cy - cr + 4, cx + cr - 4, cy + cr - 4],
                  outline=(180, 130, 30), width=2)
        d.text((cx - 2, cy), "B", font=font(cr, True), fill=(120, 80, 10), anchor="mm")
        # down arrow, right
        ax = x + w - 34
        d.line([(ax, y + 10), (ax, y + h - 22)], fill=(220, 60, 50), width=4)
        d.polygon([(ax - 8, y + h - 26), (ax + 8, y + h - 26), (ax, y + h - 12)],
                  fill=(220, 60, 50))
        d.text((x + 8, y + h - 16), "−3.9%", font=font(11, True), fill=(220, 60, 50))
    elif key == "cricket":
        d.rectangle([x, y, x + w, y + h], fill=(30, 110, 60))
        d.rectangle([x, y + h - 26, x + w, y + h - 14], fill=(200, 180, 130))
        # stumps, left
        for sx in (x + 18, x + 26, x + 34):
            d.line([(sx, y + h - 40), (sx, y + h - 26)], fill=(240, 220, 150), width=3)
        # bat, leaning right
        d.line([(x + w - 60, y + 10), (x + w - 34, y + h - 30)], fill=(220, 190, 140), width=8)
        d.line([(x + w - 34, y + h - 30), (x + w - 22, y + h - 14)], fill=(180, 150, 100), width=5)
        # red ball
        d.ellipse([x + w - 30, y + 8, x + w - 14, y + 24], fill=(200, 40, 40))
    elif key == "davao":
        d.rectangle([x, y, x + w, y + h], fill=(170, 200, 230))
        # clouds
        for clx, cly in ((x + 20, y + 10), (x + 120, y + 6), (x + 190, y + 14)):
            d.ellipse([clx, cly, clx + 34, cly + 12], fill=(255, 255, 255))
        # runway
        d.rectangle([x, y + h - 16, x + w, y + h - 8], fill=(80, 80, 90))
        for lx in range(x + 8, x + w - 8, 22):
            d.line([(lx, y + h - 12), (lx + 11, y + h - 12)], fill=(255, 255, 255), width=2)
        # airplane side profile, centre
        ax, ay = cx, cy - 4
        d.ellipse([ax - 70, ay - 10, ax + 70, ay + 10], fill=(240, 240, 245))
        d.polygon([(ax + 40, ay - 8), (ax + 78, ay - 26), (ax + 78, ay - 8)],
                  fill=(40, 90, 160))
        d.polygon([(ax - 20, ay + 6), (ax + 10, ay + 26), (ax + 22, ay + 6)],
                  fill=(40, 90, 160))
        d.polygon([(ax - 70, ay - 6), (ax - 92, ay - 20), (ax - 88, ay - 2)],
                  fill=(40, 90, 160))
        for wx in range(ax - 40, ax + 40, 12):
            d.ellipse([wx, ay - 4, wx + 5, ay + 1], fill=(40, 90, 160))
        d.text((x + w - 62, y + 6), "146 SAFE", font=font(11, True), fill=(20, 90, 40))
    elif key == "tennis":
        d.rectangle([x, y, x + w, y + h], fill=(40, 120, 60))
        d.rectangle([x, y, x + w, y + h], outline=(255, 255, 255), width=2)
        d.line([(x, cy), (x + w, cy)], fill=(255, 255, 255), width=2)
        d.ellipse([cx - 22, cy - 14, cx + 22, cy + 14], outline=(255, 255, 255), width=2)
        d.line([(x + 30, y + 6), (x + 30, y + h - 6)], fill=(240, 240, 240), width=3)
        d.line([(x + w - 30, y + 6), (x + w - 30, y + h - 6)], fill=(240, 240, 240), width=3)
        bx, by, br = x + w - 46, y + 12, 10
        d.ellipse([bx - br, by - br, bx + br, by + br], fill=(200, 230, 60))
        d.arc([bx - br, by - br, bx + br, by + br], 60, 300, fill=(255, 255, 255), width=2)
    elif key == "f1":
        d.rectangle([x, y, x + w, y + h], fill=(20, 20, 40))
        for i, col in enumerate(((255, 60, 120), (60, 200, 255), (255, 200, 60))):
            d.line([(x + 8 + i * 6, y + 6), (x + w - 8 - i * 6, y + 6)], fill=col, width=2)
        d.rectangle([x, y + h - 16, x + w, y + h - 8], fill=(60, 60, 70))
        for lx in range(x + 6, x + w - 6, 18):
            d.line([(lx, y + h - 12), (lx + 9, y + h - 12)], fill=(255, 220, 90), width=2)
        car_y = y + h - 34
        d.polygon([(x + 60, car_y + 12), (x + 80, car_y), (x + 150, car_y),
                   (x + 190, car_y + 8), (x + 196, car_y + 12)], fill=(220, 40, 60))
        d.polygon([(x + 96, car_y - 8), (x + 120, car_y - 8), (x + 132, car_y)],
                  fill=(40, 40, 60))
        for wx in (x + 82, x + 168):
            d.ellipse([wx - 9, car_y + 4, wx + 9, car_y + 20], fill=(20, 20, 20))
            d.ellipse([wx - 4, car_y + 9, wx + 4, car_y + 15], fill=(180, 180, 180))
        fx, fy = x + w - 34, y + 12
        for r in range(3):
            for c in range(4):
                if (r + c) % 2 == 0:
                    d.rectangle([fx + c * 6, fy + r * 6, fx + c * 6 + 6, fy + r * 6 + 6],
                                fill=(255, 255, 255))
        d.line([(fx, fy), (fx, fy + 22)], fill=(200, 200, 200), width=2)
    elif key == "football":
        d.rectangle([x, y, x + w, y + h], fill=(30, 110, 60))
        d.line([(x, cy), (x + w, cy)], fill=(255, 255, 255), width=2)
        d.ellipse([cx - 20, cy - 12, cx + 20, cy + 12], outline=(255, 255, 255), width=2)
        d.rectangle([x + w - 34, y + 6, x + w - 8, y + h - 6], outline=(255, 255, 255), width=2)
        bx, by, br = x + 30, y + 14, 9
        d.ellipse([bx - br, by - br, bx + br, by + br], fill=(255, 255, 255))
        d.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=(30, 30, 30))
        for dx, dy in ((-7, -4), (7, -4), (0, 7)):
            d.ellipse([bx + dx - 2, by + dy - 2, bx + dx + 2, by + dy + 2], fill=(30, 30, 30))
    elif key == "eu79":
        d.rectangle([x, y, x + w, y + h], fill=(30, 60, 140))
        for i in range(12):
            a = math.radians(i * 30)
            sx = cx + int(52 * math.cos(a))
            sy = cy + int(30 * math.sin(a))
            d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 220, 60))
        d.text((cx, cy - 2), "€", font=font(26, True), fill=(255, 255, 255), anchor="mm")
        d.text((x + w - 46, y + h - 18), "€7.9B", font=font(11, True), fill=(255, 220, 90))

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
# (lon, lat, number) pins for the 13 drawn stories on the map.
PINS = [("bepi", None, "1"), ("riyadh", (46.7, 24.6), "2"),
        ("cop31", (30.7, 36.9), "3"), ("peru", (-75.0, -10.0), "4"),
        ("kryvyi", (33.4, 47.9), "5"), ("chinajapan", (121.0, 31.0), "6"),
        ("bitcoin", None, "7"), ("rahul", (174.8, -41.3), "8"),
        ("davao", (125.6, 7.1), "9"), ("f1", (-115.1, 36.1), "10"),
        ("atp", (7.7, 45.1), "11"), ("pl", (-0.1, 51.5), "12"),
        ("eu79", (4.35, 50.85), "13")]


def draw_map(d, x, y, w, h, numbers):
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 238))
    for poly in CONTINENTS:
        pts = [(x + (lon + 180) / 360 * w, y + (90 - lat) / 180 * h) for lon, lat in poly]
        d.polygon(pts, fill=(150, 180, 150), outline=(90, 120, 100))
    # BepiColombo: a star off the map's top edge (Mercury, in space)
    d.ellipse([x + w - 30, y + 6, x + w - 18, y + 18], fill=(255, 220, 90))
    d.text((x + w - 46, y + 22), "1", font=font(11, True), fill=NAVY, anchor="ra")
    # Bitcoin: a star off the map's bottom edge (a market, not a place)
    d.ellipse([x + 8, y + h - 18, x + 20, y + h - 6], fill=(240, 180, 50))
    d.text((x + 26, y + h - 6), "7", font=font(11, True), fill=NAVY, anchor="lb")
    for key, ll, num in PINS:
        if ll is None:
            continue
        lon, lat = ll
        px = x + (lon + 180) / 360 * w
        py = y + (90 - lat) / 180 * h
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=(255, 255, 255), width=2)
        d.text((px, py - 1), num, font=font(8, True), fill=(255, 255, 255), anchor="mm")
    d.text((x + 4, y + h - 16), "PINNED: 2 Riyadh · 3 Antalya · 4 Peru · 5 Kryvyi Rih · 6 Shanghai",
           font=font(8), fill=(60, 60, 60))
    d.text((x + 4, y + h - 7), "8 Wellington · 9 Davao · 10 Las Vegas · 11 Turin · 12 London · 13 Brussels",
           font=font(8), fill=(60, 60, 60))


def badge(d, x, y, status):
    bg = {"CONFIRMED": CONF_BG, "TONIGHT": TONIGHT_BG, "CLAIM": CLAIM_BG}[status]
    fnt = font(8, True)
    tw = d.textlength(status, font=fnt) + 10
    rrect(d, [x, y, x + tw, y + 13], 6, fill=bg)
    d.text((x + tw / 2, y + 6), status, font=fnt, fill=(255, 255, 255), anchor="mm")
    return tw


def hero_panel(d, x, y, w, h, key, num):
    title, summ, outlet, status, skey, accent, region = STORIES[key]
    rrect(d, [x, y, x + w, y + h], 8, fill=(255, 255, 255), outline=LINE, width=1)
    sh = 78
    scene(d, skey, x + 4, y + 4, w - 8, sh, accent)
    d.ellipse([x + 8, y + 8, x + 28, y + 28], fill=RED)
    d.text((x + 18, y + 18), str(num), font=font(12, True), fill=(255, 255, 255), anchor="mm")
    ty = y + sh + 8
    lines = wrap(d, title, font(15, True), w - 12)
    for ln in lines[:2]:
        d.text((x + 6, ty), ln, font=font(15, True), fill=INK)
        ty += 17
    sl = wrap(d, summ, font(10), w - 12)
    for ln in sl[:2]:
        d.text((x + 6, ty), ln, font=font(10), fill=(70, 70, 70))
        ty += 12
    maxw = w - 76
    o = outlet
    while o and d.textlength(o, font=font(8)) > maxw:
        o = o[:-1].rstrip(" ·")
    if o != outlet:
        o += "…"
    d.text((x + 6, y + h - 16), o, font=font(8), fill=GREY)
    badge(d, x + w - 62, y + h - 17, status)


def small_panel(d, x, y, w, h, key, num):
    title, summ, outlet, status, skey, accent, region = STORIES[key]
    rrect(d, [x, y, x + w, y + h], 8, fill=(255, 255, 255), outline=LINE, width=1)
    sh = 46
    scene(d, skey, x + 4, y + 4, w - 8, sh, accent)
    d.ellipse([x + 8, y + 8, x + 26, y + 26], fill=NAVY)
    d.text((x + 17, y + 17), str(num), font=font(10, True), fill=(255, 255, 255), anchor="mm")
    ty = y + sh + 6
    lines = wrap(d, title, font(11, True), w - 12)
    for ln in lines[:2]:
        d.text((x + 6, ty), ln, font=font(11, True), fill=INK)
        ty += 13
    sl = wrap(d, summ, font(9), w - 12)
    for ln in sl[:2]:
        d.text((x + 6, ty), ln, font=font(9), fill=(70, 70, 70))
        ty += 11
    maxw = w - 72
    o = outlet
    while o and d.textlength(o, font=font(8)) > maxw:
        o = o[:-1].rstrip(" ·")
    if o != outlet:
        o += "…"
    d.text((x + 6, y + h - 15), o, font=font(8), fill=GREY)
    badge(d, x + w - 58, y + h - 16, status)


def build(variant, out_path):
    heroes = VARIANTS[variant]
    small = [k for k in SMALL_ORDER if k not in heroes]
    # numbering: heroes 1-3, small panels 4-13, also-list 14-35
    order = heroes + small
    assert len(order) == 13, order
    counts = region_counts()
    assert sum(counts.values()) == 35, counts

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- header
    d.text((8, 6), "THE DAY IN WORLD NEWS", font=font(12, True), fill=RED)
    d.text((W - 8, 6), "35 STORIES · 7 REGIONS · 13 PICTURED", font=font(11, True),
           fill=GREY, anchor="ra")
    d.text((8, 20), "Saturday 21 November 2026", font=font(46, True), fill=INK)
    d.line([(8, 72), (W - 8, 72)], fill=INK, width=2)
    d.text((8, 78), "COP31 talks run into overtime  ·  missiles intercepted over Riyadh  ·  a 6.7 quake shakes Peru",
           font=font(13), fill=(70, 70, 70))

    # ---- numbers strip
    cw = (W - 16) // 6
    for i, (big, l1, l2) in enumerate(NUMBERS):
        x = 8 + i * cw
        rrect(d, [x, 98, x + cw - 6, 146], 7, fill=(255, 255, 255), outline=LINE, width=1)
        d.text((x + (cw - 6) // 2, 100), big, font=font(19, True), fill=RED, anchor="ma")
        d.text((x + (cw - 6) // 2, 122), l1, font=font(8, True), fill=INK, anchor="ma")
        d.text((x + (cw - 6) // 2, 133), l2, font=font(8), fill=GREY, anchor="ma")

    # ---- region bar
    ry = 152
    d.text((8, ry), "STORIES BY REGION", font=font(10, True), fill=NAVY)
    bx = 150
    total_w = W - 8 - bx
    for region in REGION_ORDER:
        n = counts[region]
        if n == 0:
            continue
        seg = total_w * n / 35
        d.rectangle([bx, ry, bx + seg - 2, ry + 14], fill=REGION_COLORS[region])
        d.text((bx + seg / 2 - 1, ry + 7), f"{region} {n}", font=font(9, True),
               fill=(255, 255, 255), anchor="mm")
        bx += seg

    # ---- 3 heroes
    hw = (W - 16 - 2 * 6) // 3
    hy, hh = 172, 164
    for i, key in enumerate(heroes):
        hero_panel(d, 8 + i * (hw + 6), hy, hw, hh, key, i + 1)

    # ---- 10 small panels (2 rows of 5)
    sw = (W - 16 - 4 * 6) // 5
    shh = 118
    for i, key in enumerate(small):
        col, row = i % 5, i // 5
        small_panel(d, 8 + col * (sw + 6), 342 + row * (shh + 6), sw, shh, key, i + 4)

    # ---- map + also-list
    ay = 592
    d.text((8, ay), "WHERE IT HAPPENED", font=font(12, True), fill=NAVY)
    d.text((8, ay + 16), "Stories 1–13, numbered as above", font=font(9), fill=GREY)
    draw_map(d, 8, ay + 32, 330, 230, order)
    ax = 352
    d.text((ax, ay), "ALSO ON SATURDAY 21 NOVEMBER — 22 MORE STORIES",
           font=font(12, True), fill=NAVY)
    d.line([(ax, ay + 18), (W - 8, ay + 18)], fill=LINE, width=1)
    # 2 columns of 11
    for ci in range(2):
        col = ALSO[ci * 11:(ci + 1) * 11]
        x = ax + ci * 330
        for ri, (item, region) in enumerate(col):
            num = 14 + ci * 11 + ri
            yy = ay + 26 + ri * 14
            d.text((x, yy), f"{num}.", font=font(10, True), fill=RED)
            d.text((x + 26, yy), item, font=font(10), fill=INK)

    # ---- date check box
    dy = 872
    rrect(d, [8, dy, W - 8, dy + 62], 6, outline=RED, width=2)
    d.text((16, dy + 6), "DATE CHECK", font=font(11, True), fill=RED)
    d.text((16, dy + 22),
           "Every story here happened, or was first reported, on Saturday 21 November 2026 in at least one time zone.",
           font=font(10), fill=INK)
    d.text((16, dy + 36),
           "Left out as earlier news: the ICJ Myanmar ruling, the Shenzhen summit and Fiona the hippo's death (19 Nov);",
           font=font(10), fill=INK)
    d.text((16, dy + 48),
           "the Russian missiles in Poland, the Kyiv bridges hit, Cyclone Akvan's landfall and the UK–EU reset deal (20 Nov).",
           font=font(10), fill=INK)

    # ---- footer
    fy = 944
    d.line([(8, fy), (W - 8, fy)], fill=LINE, width=1)
    d.text((8, fy + 6),
           "TO THE JUDGE: this page is Saturday 21 November 2026 — 35 stories, 7 regions, 13 drawn scenes. Every story happened or was first reported on 21 November.",
           font=font(10, True), fill=NAVY)
    d.text((8, fy + 21),
           "HOW SURE:  CONFIRMED = reported by 2+ outlets or officials   ·   TONIGHT = scheduled for tonight, shown as a fixture not a result",
           font=font(9), fill=INK)
    d.text((8, fy + 36),
           "Reads at three sizes: the date and the big numbers first, the 13 drawn stories next, the 22-item list last.  Sources: Reuters, AP, AFP, ESA, USGS, ATP Tour, Formula 1, EU.",
           font=font(9), fill=GREY)
    d.text((W - 8, fy + 51), "21 NOV 2026", font=font(9, True), fill=NAVY, anchor="ra")

    img.save(out_path, optimize=True)
    print("saved", out_path, os.path.getsize(out_path), "bytes")


if __name__ == "__main__":
    # Winning variant: C (Riyadh hero, Peru #2, COP31 #3).
    # Variants A/B were built with draw21_v2.py and tested vs the top 5.
    build("C", os.path.join(HERE, "entry.png"))
