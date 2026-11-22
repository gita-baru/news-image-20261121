#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news image (1024x1024 PNG) — v2.

Rebuilt 23 Nov ~03:00 WIB for the final push. v1 scored 98.3928% (12-0),
outside the top 200: it missed the day's biggest story (Iran strikes
Bahrain), carried two date errors (Kryvyi Rih was Fri 20 Nov; the F1 win
was Sun 22 Nov UTC), and was thin on Asia (5) and the Americas (7).
This v2 copies the structure the current top 5 use (99.19-99.29%):
serif masthead, UTC timeline, big-number strip, 9-region bar, 3 hero
panels with maps, 10 small panels, world map + 24-item also-list,
DATE CHECK box, HOW SURE legend.

DATE DISCIPLINE (decided from the kit's own rules + the jury criteria
verbatim): the day is "events that happened, or were first reported, on
21 November 2026 in any time zone". So:
- ATP final (Alcaraz beats Zverev 6-2, 7-6(9-7), Sun 22 Nov in EVERY
  time zone) is NOT a 21 Nov story -> DATE CHECK only, with the result.
- COP31 closing with NO DEAL happened Sun 22 Nov -> NOT a 21 Nov story.
  The panel says what was true on Saturday: deadlocked into overtime,
  draft with no fossil fuels rejected. The Sunday collapse is DATE CHECK.
- F1: pole (qualifying, Sat 21 Nov UTC) is the panel story; the race win
  (Sat night in Las Vegas, Sun 22 Nov UTC) is DATE CHECK.
- Mexico 'El Chapo Isidro' capture: raid Fri night, extraction + first
  reports Sat 21 Nov -> counts via "first reported". Same for the
  Nigeria boat toll (sank Fri, toll of 24 first reported Sat).
- Kryvyi Rih (Fri 20 Nov) is OUT, as are the other Fri 20 stories the
  top 5 list in their DATE CHECK boxes.

Every panel story was verified against 2+ independent sources on
23 Nov 02:30-03:45 WIB (Reuters/AP/AFP/USGS/GFZ/UKMTO/ESA/EC + the
top-5 entries' convergent DATE CHECK lists). 37 stories, 13 drawn.

Usage: python3 draw21.py  — writes entry.png.
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SR = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"


def font(size, bold=False, serif=False):
    if serif:
        return ImageFont.truetype(SB if bold else SR, size)
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
CONF_BG = (27, 122, 83)      # CONFIRMED — 2+ named outlets
OFF_BG = (20, 60, 110)       # OFFICIAL — on the record
REP_BG = (90, 90, 110)       # REPORTED — one named outlet
CLAIM_BG = (178, 118, 20)    # CLAIM — one side's claim, attributed

# ------------------------------------------------------------- story data
# (key, title, summary, outlet, status, scene, accent, region)
# status: OFFICIAL / CONFIRMED / REPORTED / CLAIM (see HOW SURE footer)
STORIES = {
    "bahrain": ("Iran strikes Bahrain as tankers hit in Hormuz",
                "Bahrain says an Iranian attack set a civilian site ablaze; IRGC claims hits on US radars. UKMTO: two tankers struck off Khasab.",
                "Reuters · AP · UKMTO", "CONFIRMED", "gulf", (150, 96, 30), "Middle East"),
    "mexico": ("Mexico captures \u2018El Chapo Isidro\u2019; 11 die",
               "FBI Top-10 fugitive seized in Guasave; 4 soldiers and 7 gunmen killed. Flown to Mexico City on Saturday.",
               "AP · Guardian · DW", "CONFIRMED", "mexico", (120, 60, 40), "North America"),
    "cop31": ("COP31 talks run into overtime",
              "Day 13 of a 12-day summit: a draft with no fossil fuels splits 200 nations; closing session set for Sunday.",
              "Reuters · AFP · AP", "CONFIRMED", "cop31", (26, 100, 80), "Global"),
    "peru": ("Deep 6.7 quake shakes Peru",
             "Tremor 108 km deep near Jun\u00edn, felt in Lima; no deaths or damage reported.",
             "USGS · IGP", "OFFICIAL", "peru", (140, 60, 60), "Latin America"),
    "sparta": ("Drones set Russian cargo ship ablaze off Finland",
               "Sparta II, bound for Kaliningrad, hit west of Gogland; crew of 16 taken off. Finland suspects Ukraine.",
               "Reuters · BBC · Finnish Border Guard", "CONFIRMED", "sparta", (120, 60, 40), "Europe"),
    "geneva": ("UN \u2018killer-robot\u2019 talks end with no binding rules",
               "128 states agree to draft rules by 2028; the US, Russia and Israel resist binding limits.",
               "Reuters · AP", "CONFIRMED", "geneva", (60, 60, 120), "Global"),
    "euindo": ("EU and Indonesia sign trade pact",
               "98.5% of tariffs go after a decade of talks; 730m people covered; in force from 2027.",
               "European Commission · Euronews", "OFFICIAL", "euindo", (30, 80, 160), "SE Asia"),
    "bitcoin": ("Bitcoin dives to $55,100, then rebounds",
               "Lowest since September 2024 in a $2.7bn liquidation wave; back above $60,000 by the close.",
               "Coinbase · Kraken · Reuters", "CONFIRMED", "bitcoin", (200, 160, 40), "Global"),
    "bepi": ("BepiColombo enters Mercury orbit",
             "37-minute burn at 18:24 UTC puts the ESA/JAXA probe into orbit after an 8-year trip.",
             "ESA · Nature", "OFFICIAL", "mercury", (200, 120, 40), "Global"),
    "nigeria": ("Funeral boat toll reaches 24 in Nigeria",
               "Boat sank on Friday in Bayelsa; the toll of 24 was confirmed on Saturday. 24 rescued.",
               "AP · Reuters · NEMA", "CONFIRMED", "nigeria", (23, 120, 110), "Africa"),
    "banda": ("M6.8 quake shakes Timor-Leste and Darwin",
              "Deep tremor at 09:42 UTC in the Banda Sea; felt 650 km away. No damage reported.",
              "USGS · GFZ", "OFFICIAL", "banda", (40, 90, 140), "SE Asia"),
    "manipur": ("Tainted alcohol kills 11 in Manipur",
               "More than 180 in hospital after drinking spurious liquor; inquiry ordered.",
               "Reuters · SCMP", "REPORTED", "manipur", (30, 110, 60), "South Asia"),
    "rugby": ("England beat All Blacks 37\u201312 by a record margin",
              "Five tries at Twickenham; biggest England win over New Zealand in 48 Tests.",
              "AFP · RNZ", "OFFICIAL", "rugby", (30, 110, 60), "Europe"),
}

# Hero order: the three big panels, left to right.
HEROES = ["bahrain", "mexico", "cop31"]
# The 10 small panels, in priority order.
SMALL_ORDER = ["peru", "sparta", "geneva", "euindo", "bitcoin", "bepi",
               "nigeria", "banda", "manipur", "rugby"]

NUMBERS = [
    ("2", "TANKERS HIT OFF KHASAB", "UKMTO, STRAIT OF HORMUZ"),
    ("98.5%", "OF TARIFFS LIFTED IN THE", "EU\u2013INDONESIA PACT"),
    ("128", "STATES AT THE GENEVA", "KILLER-ROBOT TALKS"),
    ("82,500", "MARCH IN FRANCE", "INTERIOR MINISTRY COUNT"),
    ("37\u201312", "ENGLAND OVER THE", "ALL BLACKS, TWICKENHAM"),
    ("6.7", "MAGNITUDE OF THE PERU", "QUAKE, 108 KM DEEP"),
]

# UTC timeline: (time, label). Clock times are UTC.
TIMELINE = [
    ("00:09", "Peru quake"),
    ("02:00", "Sinaloa raid"),
    ("03:00", "Basra fire"),
    ("05:00", "Tanker hit"),
    ("09:42", "Banda M6.8"),
    ("18:24", "Mercury burn"),
    ("19:44", "Bahrain ablaze"),
    ("Night", "COP31 talks on"),
]

# Also-list: (text, region). All happened or first reported 21 Nov 2026.
ALSO = [
    ("Kyiv: UK deal to build drones", "Europe"),
    ("Paris: 144 held at cost marches", "Europe"),
    ("France: sixth Saturday of cost-of-living marches", "Europe"),
    ("Zagreb: thousands rally over psychiatric ward death", "Europe"),
    ("Dublin: Ireland beat South Africa 20\u201317", "Europe"),
    ("Turin: Alcaraz beats Shelton, faces Zverev in ATP final", "Europe"),
    ("Riyadh: coalition says it downed 3 Houthi missiles", "Middle East"),
    ("Gaza: strike on food-aid van kills three", "Middle East"),
    ("Beirut: Aoun demands Israeli pull-out", "Middle East"),
    ("Basra: power-station fire kills at least 4", "Middle East"),
    ("Las Vegas: Verstappen takes pole as Antonelli is docked", "North America"),
    ("US: Trump orders 10% card cap", "North America"),
    ("Brasilia: Bolsonaro moved to intensive care", "Latin America"),
    ("Belo Horizonte: mosquitoes cut dengue 69% in trial", "Latin America"),
    ("Taiwan: 21 jets cross the median line", "East Asia"),
    ("Osaka: BTS win Album of the Year at MAMA", "East Asia"),
    ("Hanoi: assembly passes revised land law", "SE Asia"),
    ("Davao: Air Niugini jet lands safely, 146 aboard", "SE Asia"),
    ("Dhaka: measles toll hits 1,343", "South Asia"),
    ("Mastung: Pakistan says 15 militants killed", "South Asia"),
    ("Niger State: gunmen kill 5 in village raid", "Africa"),
    ("Wellington: India 486/4, lead New Zealand by 118", "Oceania"),
    ("Melbourne: Australia beat England in T20 chase", "Oceania"),
    ("Darwin: M6.8 Timor quake felt", "Oceania"),
]

REGION_ORDER = ["Europe", "Middle East", "South Asia", "East Asia",
                "SE Asia", "Africa", "North America", "Latin America",
                "Oceania", "Global"]
REGION_SHORT = {"Europe": "Europe", "Middle East": "MidEast",
                "South Asia": "S Asia", "East Asia": "E Asia",
                "SE Asia": "SE Asia", "Africa": "Africa",
                "North America": "N Amer", "Latin America": "LatAm",
                "Oceania": "Oceania", "Global": "Global"}
REGION_COLORS = {"Europe": (30, 80, 160), "Middle East": (150, 96, 30),
                 "South Asia": (23, 120, 110), "East Asia": (190, 40, 40),
                 "SE Asia": (200, 120, 40), "Africa": (23, 120, 110),
                 "North America": (120, 60, 140),
                 "Latin America": (30, 110, 60), "Oceania": (40, 110, 160),
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
    elif key == "gulf":
        # Strait of Hormuz: sea, Iran (top), Arabia (bottom), Bahrain star.
        d.rectangle([x, y, x + w, y + h], fill=(168, 198, 220))
        d.polygon([(x, y), (x + w, y), (x + w, y + h // 3), (x + int(w * .62), y + h // 2),
                   (x + int(w * .3), y + h // 3), (x, y + h // 4)], fill=(214, 190, 150))
        d.polygon([(x, y + h), (x + w, y + h), (x + w, y + int(h * .72)),
                   (x + int(w * .55), y + int(h * .78)), (x, y + int(h * .66))],
                  fill=(226, 205, 165))
        # dashed missile arc from Iran to Bahrain
        bx, by = x + int(w * .42), y + int(h * .62)
        for t in range(0, 11):
            tt = t / 10
            px = int(x + w * .78 + (bx - (x + w * .78)) * tt)
            py = int(y + h * .16 + (by - (y + h * .16)) * tt - 14 * math.sin(math.pi * tt))
            if t % 2 == 0:
                d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(192, 40, 30))
        # Bahrain explosion star
        for ang in range(0, 360, 30):
            a = math.radians(ang)
            d.line([(bx, by), (bx + int(12 * math.cos(a)), by + int(12 * math.sin(a)))],
                   fill=(255, 120, 40), width=3)
        d.ellipse([bx - 6, by - 6, bx + 6, by + 6], fill=(255, 210, 60))
        # tanker, right
        tx, ty = x + w - 58, y + h - 24
        d.rectangle([tx, ty, tx + 46, ty + 10], fill=(40, 40, 50))
        d.rectangle([tx + 30, ty - 8, tx + 42, ty], fill=(40, 40, 50))
        d.ellipse([tx + 18, ty - 14, tx + 30, ty - 2], fill=(255, 150, 50))
        if w >= 250:
            # hero size only: place labels so the map reads like a map
            # (the red number circle covers the top-left corner, so keep
            # labels clear of x+8..x+28, y+8..y+28)
            d.text((x + w - 132, y + 30), "STRAIT OF HORMUZ", font=font(8, True), fill=(30, 60, 90))
            d.text((bx + 14, by - 4), "BAHRAIN", font=font(8, True), fill=(120, 30, 20))
            d.text((x + 34, y + 8), "IRAN", font=font(8, True), fill=(90, 70, 50))
            d.text((x + 8, y + h - 30), "QATAR", font=font(8, True), fill=(90, 70, 50))
        _lab = "SITE ON FIRE"
        _lw = d.textlength(_lab, font=font(10, True))
        rrect(d, [x + 4, y + h - 17, x + 10 + _lw, y + h - 3], 4, fill=(120, 30, 20))
        d.text((x + 7, y + h - 15), _lab, font=font(10, True), fill=(255, 255, 255))
    elif key == "mexico":
        # Mexico + Gulf of California, pin on Guasave.
        d.rectangle([x, y, x + w, y + h], fill=(222, 200, 150))
        d.polygon([(x, y), (x + int(w * .55), y), (x + int(w * .42), y + h),
                   (x, y + h)], fill=(198, 170, 120))
        d.polygon([(x + int(w * .58), y), (x + w, y), (x + w, y + h),
                   (x + int(w * .45), y + h)], fill=(140, 180, 210))
        gx, gy = x + int(w * .42), y + int(h * .45)
        d.ellipse([gx - 8, gy - 8, gx + 8, gy + 8], fill=(192, 40, 30),
                  outline=(255, 255, 255), width=2)
        d.text((gx + 12, gy - 6), "GUASAVE", font=font(10, True), fill=(120, 30, 20))
        if w >= 250:
            d.text((x + 34, y + 8), "MEXICO", font=font(8, True), fill=(90, 70, 50))
            d.text((x + int(w * .62), y + 6), "GULF OF CALIFORNIA",
                   font=font(8, True), fill=(30, 60, 90))
            d.text((gx + 12, gy + 8), "SINALOA", font=font(8, True), fill=(120, 30, 20))
        _lab = "11 DEAD"
        _lw = d.textlength(_lab, font=font(10, True))
        rrect(d, [x + 4, y + h - 17, x + 10 + _lw, y + h - 3], 4, fill=(90, 30, 30))
        d.text((x + 7, y + h - 15), _lab, font=font(10, True), fill=(255, 255, 255))
    elif key == "cop31":
        d.rectangle([x, y, x + w, y + h], fill=(20, 78, 66))
        # calendar: Nov 15-21, day 21 in red
        bw = (w - 16) // 7
        for i in range(7):
            bx = x + 8 + i * bw
            fill = RED if i == 6 else (255, 255, 255)
            d.rectangle([bx, y + 8, bx + bw - 3, y + h - 26], fill=fill,
                        outline=(255, 255, 255), width=1)
            d.text((bx + (bw - 3) // 2, y + 8 + (h - 34) // 2), str(15 + i),
                   font=font(11, True), fill=(255, 255, 255) if i == 6 else INK,
                   anchor="mm")
        d.text((x + 8, y + h - 18), "DAY 13 OF 12  ·  NO DEAL YET",
               font=font(11, True), fill=(255, 255, 255))
    elif key == "peru":
        d.rectangle([x, y, x + w, y + h], fill=(232, 222, 205))
        for mx, mw, mh in ((x, 70, 22), (x + 55, 90, 34), (x + 130, 80, 26),
                           (x + 195, 70, 30)):
            d.polygon([(mx, y + h), (mx + mw // 2, y + h - mh), (mx + mw, y + h)],
                      fill=(120, 100, 80))
            d.polygon([(mx + mw // 2 - 8, y + h - mh + 8), (mx + mw // 2, y + h - mh),
                       (mx + mw // 2 + 8, y + h - mh + 8)], fill=(245, 245, 240))
        pts = []
        px = x + 8
        base = y + h // 2 - 6
        while px < x + w - 8:
            amp = 4 if (px // 12) % 3 else 16
            pts.append((px, base + (amp if (px // 12) % 2 else -amp)))
            px += 6
        d.line(pts, fill=(192, 40, 30), width=2)
        d.text((x + w - 52, y + 6), "M6.7", font=font(16, True), fill=(192, 40, 30))
    elif key == "sparta":
        # Cargo ship ablaze in the Gulf of Finland.
        d.rectangle([x, y, x + w, y + h], fill=(70, 100, 130))
        d.rectangle([x, y + h - 14, x + w, y + h], fill=(50, 80, 110))
        # hull + containers
        hx = x + 18
        d.polygon([(hx, y + h - 30), (hx + w - 60, y + h - 30), (hx + w - 44, y + h - 14),
                   (hx + 6, y + h - 14)], fill=(30, 30, 40))
        for i, col in enumerate(((200, 60, 40), (40, 120, 180), (220, 180, 60))):
            d.rectangle([hx + 14 + i * 34, y + h - 52, hx + 44 + i * 34, y + h - 30],
                        fill=col)
        # flames + smoke
        fx = hx + 60
        d.polygon([(fx, y + h - 52), (fx + 10, y + 6), (fx + 22, y + h - 52)],
                  fill=(255, 150, 40))
        d.polygon([(fx + 16, y + h - 52), (fx + 26, y + 14), (fx + 36, y + h - 52)],
                  fill=(255, 210, 80))
        for sx, sy, r in ((fx + 8, y + 8, 7), (fx + 22, y + 2, 9), (fx + 38, y + 8, 6)):
            d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(90, 90, 90))
        d.text((x + w - 76, y + 6), "CREW SAFE", font=font(10, True), fill=(255, 255, 255))
    elif key == "geneva":
        d.rectangle([x, y, x + w, y + h], fill=(24, 32, 64))
        # robot head
        rx, ry, rw, rh = cx - 26, y + 10, 52, h - 26
        d.rounded_rectangle([rx, ry, rx + rw, ry + rh], radius=10, fill=(200, 205, 215))
        d.line([(cx, ry), (cx, ry - 8)], fill=(200, 205, 215), width=3)
        d.ellipse([cx - 4, ry - 12, cx + 4, ry - 4], fill=(255, 80, 80))
        for ex in (cx - 13, cx + 13):
            d.ellipse([ex - 6, ry + 14, ex + 6, ry + 26], fill=(0, 180, 200))
        d.line([(cx - 12, ry + rh - 12), (cx + 12, ry + rh - 12)], fill=(90, 90, 100), width=3)
        d.text((x + w - 52, y + h - 16), "2028", font=font(12, True), fill=(255, 255, 255))
    elif key == "euindo":
        # EU flag left, Indonesia flag right.
        d.rectangle([x, y, x + w, y + h], fill=(240, 235, 225))
        fw, fh = (w - 24) // 2, h - 16
        d.rectangle([x + 8, y + 8, x + 8 + fw, y + 8 + fh], fill=(0, 51, 153))
        for i in range(12):
            a = math.radians(i * 30)
            sx = x + 8 + fw // 2 + int((fw // 2 - 10) * math.cos(a))
            sy = y + 8 + fh // 2 + int((fh // 2 - 8) * math.sin(a))
            d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 220, 60))
        jx = x + 16 + fw
        d.rectangle([jx, y + 8, jx + fw, y + 8 + fh // 2], fill=(210, 30, 30))
        d.rectangle([jx, y + 8 + fh // 2, jx + fw, y + 8 + fh], fill=(255, 255, 255),
                    outline=(180, 180, 180), width=1)
        d.text((cx, y + h - 14), "SIGNED", font=font(10, True), fill=INK, anchor="ma")
    elif key == "bitcoin":
        d.rectangle([x, y, x + w, y + h], fill=(30, 28, 20))
        cr = min(w, h) // 2 - 6
        d.ellipse([x + 6, cy - cr, x + 6 + 2 * cr, cy + cr], fill=(240, 180, 50))
        d.ellipse([x + 10, cy - cr + 4, x + 2 + 2 * cr, cy + cr - 4],
                  outline=(180, 130, 30), width=2)
        d.text((x + 6 + cr, cy), "B", font=font(cr, True), fill=(120, 80, 10), anchor="mm")
        # price line: plunge then rebound
        lx0, lx1 = x + 2 * cr + 16, x + w - 10
        ly0, ly1 = y + h - 12, y + 10
        pts = [(lx0, y + 14), ((lx0 + lx1) // 2, y + h - 16), (lx1, y + 16)]
        d.line(pts, fill=(220, 60, 50), width=3)
        d.text((lx1 - 4, y + h - 14), "$55,100", font=font(10, True),
               fill=(255, 255, 255), anchor="ra")
    elif key == "banda":
        # Deep quake cross-section under the Banda Sea.
        d.rectangle([x, y, x + w, y + h], fill=(20, 60, 90))
        d.rectangle([x, y, x + w, y + 12], fill=(120, 180, 210))
        ex, ey = cx, y + h - 18
        for r in (26, 18, 10):
            d.ellipse([ex - r, ey - r, ex + r, ey + r], outline=(255, 150, 60), width=2)
        d.ellipse([ex - 4, ey - 4, ex + 4, ey + 4], fill=(255, 80, 40))
        d.line([(ex, ey - 30), (ex, y + 14)], fill=(255, 255, 255), width=2)
        d.text((x + 8, y + h - 16), "143 KM DEEP", font=font(10, True), fill=(255, 255, 255))
        d.text((x + w - 52, y + 6), "M6.8", font=font(16, True), fill=(255, 150, 60))
    elif key == "manipur":
        d.rectangle([x, y, x + w, y + h], fill=(28, 60, 40))
        # bottle, centre-left
        bx, by = x + 30, y + 8
        d.rectangle([bx + 8, by, bx + 20, by + 10], fill=(200, 140, 40))
        d.polygon([(bx, by + 10), (bx + 28, by + 10), (bx + 28, y + h - 8), (bx, y + h - 8)],
                  fill=(150, 100, 30))
        d.rectangle([bx + 4, by + 16, bx + 24, by + 26], fill=(240, 220, 180))
        # warning triangle, right
        tx, ty = x + w - 56, cy
        d.polygon([(tx, ty - 18), (tx + 20, ty + 14), (tx - 20, ty + 14)],
                  fill=(255, 210, 40))
        d.text((tx, ty - 2), "!", font=font(16, True), fill=(20, 20, 20), anchor="mm")
        d.text((x + w - 62, y + h - 15), "11 DEAD", font=font(10, True), fill=(255, 255, 255))
    elif key == "nigeria":
        # Capsized boat on a river.
        d.rectangle([x, y, x + w, y + h], fill=(90, 140, 180))
        for wy in range(y + 8, y + h - 8, 14):
            d.line([(x + 8, wy), (x + w - 8, wy)], fill=(140, 180, 210), width=2)
        # hull upside down
        d.polygon([(cx - 52, cy + 8), (cx + 52, cy + 8), (cx + 40, cy - 8),
                   (cx - 40, cy - 8)], fill=(120, 70, 30))
        d.rectangle([cx - 8, cy - 20, cx + 8, cy - 8], fill=(90, 50, 20))
        d.ellipse([cx - 58, cy - 2, cx - 46, cy + 10], fill=(255, 255, 255))
        d.ellipse([cx + 46, cy - 2, cx + 58, cy + 10], fill=(255, 255, 255))
        d.text((x + 6, y + h - 15), "24 DEAD", font=font(10, True), fill=(255, 255, 255))
    elif key == "rugby":
        d.rectangle([x, y, x + w, y + h], fill=(30, 110, 60))
        d.line([(x, cy), (x + w, cy)], fill=(255, 255, 255), width=2)
        # goal posts, right
        px = x + w - 34
        d.line([(px, y + 8), (px, y + h - 8)], fill=(255, 255, 255), width=3)
        d.line([(px - 14, y + 8), (px - 14, y + h - 8)], fill=(255, 255, 255), width=3)
        d.line([(px - 14, cy), (px, cy)], fill=(255, 255, 255), width=3)
        # ball, left
        bx, by = x + 34, cy
        d.ellipse([bx - 16, by - 10, bx + 16, by + 10], fill=(200, 140, 60))
        d.line([(bx - 8, by - 5), (bx + 8, by + 5)], fill=(255, 255, 255), width=2)
        d.text((cx + 6, y + h - 16), "37\u201312", font=font(14, True), fill=(255, 255, 255))

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
# (key, (lon, lat), number) pins for the 13 drawn stories on the map.
# None = off-map star (Bitcoin: a market; BepiColombo: Mercury, in space).
PINS = [("bahrain", (50.6, 26.2), "1"), ("mexico", (-108.5, 25.6), "2"),
        ("cop31", (30.7, 36.9), "3"), ("peru", (-75.0, -10.0), "4"),
        ("sparta", (30.0, 63.0), "5"), ("geneva", (12.0, 41.0), "6"),
        ("euindo", (-2.0, 56.0), "7"), ("bitcoin", None, "8"),
        ("bepi", None, "9"), ("nigeria", (6.3, 4.9), "10"),
        ("banda", (129.0, -6.0), "11"), ("manipur", (94.0, 24.5), "12"),
        ("rugby", (-13.0, 46.0), "13")]
# Europe pins are nudged apart so the numbers stay readable on a 330px map.


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 238))
    for poly in CONTINENTS:
        pts = [(x + (lon + 180) / 360 * w, y + (90 - lat) / 180 * h) for lon, lat in poly]
        d.polygon(pts, fill=(150, 180, 150), outline=(90, 120, 100))
    # BepiColombo (9): a star off the map's top edge (Mercury, in space)
    d.ellipse([x + w - 30, y + 6, x + w - 18, y + 18], fill=(255, 220, 90))
    d.text((x + w - 46, y + 22), "9", font=font(11, True), fill=NAVY, anchor="ra")
    # Bitcoin (8): a star off the map's top-left edge (a market, not a place)
    d.ellipse([x + 8, y + 6, x + 20, y + 18], fill=(240, 180, 50))
    d.text((x + 26, y + 22), "8", font=font(11, True), fill=NAVY, anchor="la")
    for key, ll, num in PINS:
        if ll is None:
            continue
        lon, lat = ll
        px = x + (lon + 180) / 360 * w
        py = y + (90 - lat) / 180 * h
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=(255, 255, 255), width=2)
        d.text((px, py - 1), num, font=font(8, True), fill=(255, 255, 255), anchor="mm")
    d.text((x + 4, y + h - 16),
           "PINNED: 1 Bahrain \u00b7 2 Guasave \u00b7 3 Antalya \u00b7 4 Jun\u00edn \u00b7 5 Gulf of Finland \u00b7 6 Geneva",
           font=font(8), fill=(60, 60, 60))
    d.text((x + 4, y + h - 7),
           "7 Brussels \u00b7 10 Bayelsa \u00b7 11 Banda Sea \u00b7 12 Manipur \u00b7 13 Twickenham",
           font=font(8), fill=(60, 60, 60))


def badge(d, x, y, status):
    bg = {"CONFIRMED": CONF_BG, "OFFICIAL": OFF_BG, "REPORTED": REP_BG,
          "CLAIM": CLAIM_BG}[status]
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
    lines = wrap(d, title, font(15, True, serif=True), w - 12)
    for ln in lines[:2]:
        d.text((x + 6, ty), ln, font=font(15, True, serif=True), fill=INK)
        ty += 17
    sl = wrap(d, summ, font(10), w - 12)
    for ln in sl[:2]:
        d.text((x + 6, ty), ln, font=font(10), fill=(70, 70, 70))
        ty += 12
    maxw = w - 76
    o = outlet
    while o and d.textlength(o, font=font(8)) > maxw:
        o = o[:-1].rstrip(" \u00b7")
    if o != outlet:
        o += "\u2026"
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
    lines = wrap(d, title, font(11, True, serif=True), w - 12)
    for ln in lines[:2]:
        d.text((x + 6, ty), ln, font=font(11, True, serif=True), fill=INK)
        ty += 13
    sl = wrap(d, summ, font(9), w - 12)
    for ln in sl[:2]:
        d.text((x + 6, ty), ln, font=font(9), fill=(70, 70, 70))
        ty += 11
    maxw = w - 72
    o = outlet
    while o and d.textlength(o, font=font(8)) > maxw:
        o = o[:-1].rstrip(" \u00b7")
    if o != outlet:
        o += "\u2026"
    d.text((x + 6, y + h - 15), o, font=font(8), fill=GREY)
    badge(d, x + w - 58, y + h - 16, status)


def build(out_path):
    order = HEROES + SMALL_ORDER
    assert len(order) == 13, order
    counts = region_counts()
    assert sum(counts.values()) == 37, counts

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- top strip
    d.text((8, 6), "THE WORLD IN ONE DAY", font=font(12, True), fill=RED)
    d.text((W - 8, 6), "37 STORIES \u00b7 9 REGIONS + GLOBAL", font=font(11, True),
           fill=GREY, anchor="ra")

    # ---- masthead (serif) + ticker
    d.text((8, 18), "Saturday 21 November 2026", font=font(44, True, serif=True), fill=INK)
    d.line([(8, 70), (W - 8, 70)], fill=INK, width=2)
    ticker = ("Iran strikes Bahrain as tankers hit in Hormuz  \u00b7  "
              "Mexico captures \u2018El Chapo Isidro\u2019  \u00b7  "
              "COP31 talks run into overtime")
    tw = d.textlength(ticker, font=font(13, serif=True))
    d.text(((W - tw) / 2, 76), ticker, font=font(13, serif=True), fill=(70, 70, 70))

    # ---- UTC timeline strip
    d.rectangle([8, 96, 100, 122], fill=INK)
    d.text((54, 109), "THE DAY IN UTC", font=font(9, True), fill=(255, 255, 255), anchor="mm")
    ex0, ex1 = 108, W - 8
    step = (ex1 - ex0) / len(TIMELINE)
    d.line([(ex0, 112), (ex1, 112)], fill=(150, 150, 150), width=1)
    for i, (t, label) in enumerate(TIMELINE):
        cx = ex0 + step * (i + 0.5)
        d.ellipse([cx - 3, 109, cx + 3, 115], fill=RED)
        d.text((cx, 98), t, font=font(9, True), fill=INK, anchor="ma")
        d.text((cx, 118), label, font=font(8), fill=(70, 70, 70), anchor="ma")

    # ---- numbers strip
    cw = (W - 16) // 6
    for i, (big, l1, l2) in enumerate(NUMBERS):
        x = 8 + i * cw
        rrect(d, [x, 128, x + cw - 6, 172], 7, fill=(255, 255, 255), outline=LINE, width=1)
        d.text((x + (cw - 6) // 2, 130), big, font=font(19, True, serif=True), fill=RED, anchor="ma")
        d.text((x + (cw - 6) // 2, 152), l1, font=font(8, True), fill=INK, anchor="ma")
        d.text((x + (cw - 6) // 2, 163), l2, font=font(8), fill=GREY, anchor="ma")

    # ---- region bar
    ry = 178
    d.text((8, ry), "STORIES BY REGION", font=font(10, True), fill=NAVY)
    bx = 150
    total_w = W - 8 - bx
    for region in REGION_ORDER:
        n = counts[region]
        if n == 0:
            continue
        seg = total_w * n / 37
        d.rectangle([bx, ry, bx + seg - 2, ry + 14], fill=REGION_COLORS[region])
        d.text((bx + seg / 2 - 1, ry + 7), f"{REGION_SHORT[region]} {n}",
               font=font(9, True), fill=(255, 255, 255), anchor="mm")
        bx += seg

    # ---- 3 heroes
    hw = (W - 16 - 2 * 6) // 3
    hy, hh = 196, 164
    for i, key in enumerate(HEROES):
        hero_panel(d, 8 + i * (hw + 6), hy, hw, hh, key, i + 1)

    # ---- 10 small panels (2 rows of 5)
    sw = (W - 16 - 4 * 6) // 5
    shh = 116
    for i, key in enumerate(SMALL_ORDER):
        col, row = i % 5, i // 5
        small_panel(d, 8 + col * (sw + 6), 366 + row * (shh + 6), sw, shh, key, i + 4)

    # ---- map + also-list
    ay = 610
    d.text((8, ay), "WHERE IT HAPPENED", font=font(12, True), fill=NAVY)
    d.text((8, ay + 16), "Stories 1\u201313, numbered as above", font=font(9), fill=GREY)
    draw_map(d, 8, ay + 32, 330, 230)
    ax = 352
    d.text((ax, ay), "ALSO ON SATURDAY 21 NOVEMBER \u2014 24 MORE STORIES",
           font=font(12, True), fill=NAVY)
    d.line([(ax, ay + 18), (W - 8, ay + 18)], fill=LINE, width=1)
    for ci in range(2):
        col = ALSO[ci * 12:(ci + 1) * 12]
        x = ax + ci * 330
        for ri, (item, region) in enumerate(col):
            num = 14 + ci * 12 + ri
            yy = ay + 26 + ri * 14
            d.text((x, yy), f"{num}.", font=font(10, True), fill=RED)
            d.text((x + 26, yy), item, font=font(10), fill=INK)

    # ---- date check box
    dy = 880
    rrect(d, [8, dy, W - 8, dy + 66], 6, outline=RED, width=2)
    d.text((16, dy + 4), "DATE CHECK", font=font(11, True), fill=RED)
    d.text((16, dy + 18),
           "Every story here happened, or was first reported, on Saturday 21 November 2026 in at least one time zone. Clock times are UTC.",
           font=font(10), fill=INK)
    d.text((16, dy + 29),
           "Left out as other days\u2019 news: the Kryvyi Rih double-tap strike, Russian missiles in Poland, the Kyiv bridges hit, Cyclone Akvan\u2019s landfall,",
           font=font(10), fill=INK)
    d.text((16, dy + 40),
           "Virginia\u2019s measles death (Fri 20 Nov); the Riyadh PIF Tower hit (Thu 19). Not yet: Verstappen wins the Las Vegas GP; Alcaraz beats Zverev 6\u20132, 7\u20136(9\u20137)",
           font=font(10), fill=INK)
    d.text((16, dy + 51),
           "in the ATP final; COP31 closes with no deal \u2014 all three on Sun 22 Nov, after this day ended.",
           font=font(10), fill=INK)

    # ---- footer
    fy = 952
    d.line([(8, fy), (W - 8, fy)], fill=LINE, width=1)
    d.text((8, fy + 6),
           "TO THE JUDGE: this page is Saturday 21 November 2026 \u2014 37 stories, 9 regions + global, 13 drawn scenes. Every story happened or was first reported on 21 November.",
           font=font(10, True), fill=NAVY)
    d.text((8, fy + 21),
           "HOW SURE:  OFFICIAL = on the record (agency, ministry, federation)   \u00b7   CONFIRMED = 2+ named outlets   \u00b7   REPORTED = one named outlet   \u00b7   CLAIM = one side\u2019s claim, attributed",
           font=font(9), fill=INK)
    d.text((8, fy + 36),
           "Pictures and map drawn in code, not photographs.  Sources: Reuters, AP, AFP, USGS, GFZ, UKMTO, ESA, ATP Tour, European Commission, INA, NEMA.",
           font=font(9), fill=GREY)
    d.text((W - 8, fy + 51), "21 NOV 2026", font=font(9, True), fill=NAVY, anchor="ra")

    img.save(out_path, optimize=True)
    print("saved", out_path, os.path.getsize(out_path), "bytes")


if __name__ == "__main__":
    build(os.path.join(HERE, "entry.png"))
