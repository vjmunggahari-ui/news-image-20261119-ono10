#!/usr/bin/env python3
"""Draw the v3 front page for 19 November 2026 and write entry.png.

A newspaper front page for THE WORLD TODAY, Thursday 19 November 2026:
one lead story with a drawn Shenzhen dusk scene, three illustrated
secondaries, an eight-story grid, and an eight-item "Also today" strip --
twenty verified stories from the full day, morning to late evening.

Everything is drawn in code with Pillow: vector text plus simple flat
illustrations (skyline and flags, scales of justice, a rising market
chart, a capitol dome). No network, no clock, no randomness: the same
script always writes the same bytes.

Run:  python3 draw.py            (writes entry.png beside this file)
Fonts: Liberation Serif / Sans from /usr/share/fonts/truetype.
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
M = 28                      # outer margin
CW = W - 2 * M              # content width: 968

PAPER = (247, 242, 231)     # warm newsprint cream
INK = (20, 20, 20)          # near-black text
RED = (163, 22, 33)         # masthead red / kickers
NAVY = (27, 42, 74)         # navy bands and night sky
NAVY_DK = (18, 30, 56)
GOLD = (198, 158, 62)       # gold accents
GREY = (90, 86, 78)         # captions and footer
RULE = (60, 56, 50)         # thin rule colour
SKY_TOP = (44, 62, 110)     # dusk gradient top
SKY_BOT = (214, 164, 96)    # dusk gradient bottom
SUN = (232, 190, 90)

FONT_DIR = "/usr/share/fonts/truetype"
SERIF_B = os.path.join(FONT_DIR, "liberation/LiberationSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "liberation/LiberationSerif-Regular.ttf")
SERIF_I = os.path.join(FONT_DIR, "liberation/LiberationSerif-Italic.ttf")
SANS_B = os.path.join(FONT_DIR, "liberation/LiberationSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "liberation/LiberationSans-Regular.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap of text to fit `width` pixels with font `fnt`."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=None, max_lines=None):
    """Draw wrapped text; return the y just below the last line."""
    lines = wrap(draw, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    step = leading or int(fnt.size * 1.18)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += step
    return y


def kicker(draw, x, y, text, size=14):
    draw.text((x, y), text.upper(), font=font(SANS_B, size), fill=RED)
    return y + size + 6


def hrule(draw, y, x0=M, x1=W - M, width=2):
    draw.line([(x0, y), (x1, y)], fill=RULE, width=width)


def vrule(draw, x, y0, y1, width=1):
    draw.line([(x, y0), (x, y1)], fill=(200, 192, 176), width=width)


def draw_flag_us(d, x, y, w, h):
    """Small US flag: red/white stripes, blue canton, dot stars."""
    stripe = h / 13.0
    for i in range(13):
        c = (178, 34, 52) if i % 2 == 0 else (240, 240, 240)
        d.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe], fill=c)
    cw, ch = w * 0.4, stripe * 7
    d.rectangle([x, y, x + cw, y + ch], fill=(40, 60, 120))
    for r in range(5):
        for c in range(6):
            sx = x + 4 + c * (cw - 8) / 5.0
            sy = y + 3 + r * (ch - 6) / 4.0
            d.ellipse([sx - 1.5, sy - 1.5, sx + 1.5, sy + 1.5], fill=(255, 255, 255))


def draw_flag_cn(d, x, y, w, h):
    """Small Chinese flag: red field, one large + four small gold stars."""
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    cx, cy = x + w * 0.22, y + h * 0.28
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 222, 0))
    for dx, dy in [(0.42, 0.12), (0.52, 0.30), (0.46, 0.52), (0.30, 0.55)]:
        sx, sy = x + w * dx, y + h * dy
        d.ellipse([sx - 2.5, sy - 2.5, sx + 2.5, sy + 2.5], fill=(255, 222, 0))


def draw_flag_ru(d, x, y, w, h):
    """Small Russian flag: white / blue / red horizontal tricolour."""
    d.rectangle([x, y, x + w, y + h / 3], fill=(245, 245, 245))
    d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 57, 166))
    d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 0, 50))


def draw_lead_art(d, x, y, w, h):
    """Shenzhen at dusk: gradient sky, low sun, skyline, three flags."""
    for i in range(h):
        t = i / max(h - 1, 1)
        r = int(SKY_TOP[0] + (SKY_BOT[0] - SKY_TOP[0]) * t)
        g = int(SKY_TOP[1] + (SKY_BOT[1] - SKY_TOP[1]) * t)
        b = int(SKY_TOP[2] + (SKY_BOT[2] - SKY_TOP[2]) * t)
        d.line([(x, y + i), (x + w, y + i)], fill=(r, g, b))
    # low sun over the bay
    sx, sy, sr = x + int(w * 0.62), y + int(h * 0.52), 34
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=SUN)
    # skyline silhouettes, back row then front row
    back = [(0, 150, 46, 92), (58, 128, 40, 114), (112, 158, 52, 84),
            (176, 118, 38, 124), (226, 146, 46, 96), (286, 132, 40, 110),
            (338, 156, 48, 86), (398, 138, 26, 104)]
    for bx, by, bw, bh in back:
        d.rectangle([x + bx, y + by, x + bx + bw, y + h], fill=(52, 66, 104))
    front = [(0, 178, 60, 64), (72, 164, 34, 78), (118, 186, 58, 56),
             (188, 158, 30, 84), (228, 182, 52, 60), (292, 170, 36, 72),
             (340, 188, 44, 54), (396, 176, 28, 66)]
    for fx, fy, fw, fh in front:
        d.rectangle([x + fx, y + fy, x + fx + fw, y + h], fill=NAVY_DK)
    # lit windows in the front row (kept inside the art bounds)
    for wx in range(x + 8, x + w - 8, 18):
        for wy in (y + 168, y + 184, y + 200):
            if wy + 5 <= y + h - 8 and (wx * 7 + wy * 3) % 5 < 2:
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(232, 190, 90))
    # bay reflection lines
    for i, ry in enumerate((h - 22, h - 14, h - 6)):
        d.line([(x + 14, y + ry), (x + w - 14 - i * 30, y + ry)],
               fill=(232, 190, 90), width=2)
    # three flags on poles above the skyline
    flags = [(draw_flag_us, 0.10), (draw_flag_cn, 0.44), (draw_flag_ru, 0.76)]
    for fn, fx in flags:
        px = x + int(w * fx)
        d.line([(px, y + 18), (px, y + 96)], fill=(20, 20, 20), width=3)
        fn(d, px + 3, y + 20, 74, 46)
    d.rectangle([x, y, x + w - 1, y + h - 1], outline=(20, 20, 20), width=2)


def draw_scales(d, x, y, w, h):
    """Scales of justice in gold on navy."""
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    cx = x + w // 2
    d.rectangle([cx - 3, y + 14, cx + 3, y + h - 16], fill=GOLD)
    d.rectangle([x + 28, y + 22, x + w - 28, y + 27], fill=GOLD)
    d.ellipse([cx - 6, y + 8, cx + 6, y + 20], fill=GOLD)
    for side in (-1, 1):
        px = cx + side * (w // 2 - 34)
        d.line([(cx, y + 24), (px, y + 44)], fill=GOLD, width=2)
        d.line([(px - 22, y + 44), (px, y + 30)], fill=GOLD, width=2)
        d.line([(px + 22, y + 44), (px, y + 30)], fill=GOLD, width=2)
        d.pieslice([px - 24, y + 42, px + 24, y + 66], 0, 180, fill=GOLD)
    d.rectangle([cx - 26, y + h - 16, cx + 26, y + h - 10], fill=GOLD)


def draw_chart(d, x, y, w, h):
    """Rising market chart: bars and an arrowed trend line on navy."""
    d.rectangle([x, y, x + w, y + h], fill=(16, 52, 38))
    bars = [22, 30, 26, 40, 48, 44, 58, 70]
    bw = w // len(bars)
    for i, bh in enumerate(bars):
        bx = x + i * bw + 6
        d.rectangle([bx, y + h - 10 - bh, bx + bw - 12, y + h - 10],
                    fill=(88, 168, 120))
    pts = [(x + 12, y + h - 26), (x + 60, y + h - 44), (x + 110, y + h - 34),
           (x + 160, y + h - 52), (x + 210, y + h - 62), (x + w - 16, y + 22)]
    d.line(pts, fill=GOLD, width=4, joint="curve")
    hx, hy = pts[-1]
    d.polygon([(hx, hy), (hx - 16, hy + 2), (hx - 4, hy + 14)], fill=GOLD)
    d.text((x + 10, y + 6), "+17%", font=font(SANS_B, 20), fill=(255, 255, 255))


def draw_capitol(d, x, y, w, h):
    """Capitol dome: columns, dome and flag on navy."""
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    cx = x + w // 2
    d.rectangle([x + 34, y + h - 18, x + w - 34, y + h - 12], fill=(220, 220, 220))
    for i in range(6):
        colx = x + 44 + i * ((w - 88) // 5)
        d.rectangle([colx, y + h - 52, colx + 10, y + h - 18],
                    fill=(220, 220, 220))
    d.rectangle([x + 34, y + h - 58, x + w - 34, y + h - 52],
                fill=(220, 220, 220))
    d.pieslice([cx - 52, y + 10, cx + 52, y + h - 40], 180, 360,
               fill=(235, 235, 235))
    d.rectangle([cx - 52, y + h - 62, cx + 52, y + h - 58],
                fill=(235, 235, 235))
    d.line([(cx, y + 8), (cx, y + 26)], fill=GOLD, width=3)
    d.polygon([(cx, y + 8), (cx + 18, y + 13), (cx, y + 18)], fill=RED)


def secondary(d, x, y, w, art_fn, kick, head, deck):
    """One illustrated secondary column; returns y below the deck."""
    art_fn(d, x, y, w, 88)
    y += 88 + 8
    y = kicker(d, x, y, kick, size=13)
    y = para(d, x, y, head, font(SERIF_B, 23), w, leading=27, max_lines=3)
    y = para(d, x, y + 3, deck, font(SERIF, 14), w, leading=17, max_lines=2)
    return y


def grid_cell(d, x, y, w, kick, head, deck):
    """One grid cell; returns y below the deck."""
    y = kicker(d, x, y, kick, size=12)
    y = para(d, x, y, head, font(SERIF_B, 19), w, leading=22, max_lines=2)
    y = para(d, x, y + 2, deck, font(SERIF, 13), w, leading=16, max_lines=2)
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ------------------------------------------------------
    title = "THE WORLD TODAY"
    tf = font(SERIF_B, 62)
    d.text(((W - d.textlength(title, font=tf)) / 2, 14), title,
           font=tf, fill=INK)
    hrule(d, 92)
    d.rectangle([M, 100, W - M, 130], fill=RED)
    date = "THURSDAY  ·  19 NOVEMBER 2026"
    df = font(SANS_B, 21)
    d.text(((W - d.textlength(date, font=df)) / 2, 104), date,
           font=df, fill=(255, 255, 255))
    sub = "Twenty stories from a full day around the world — morning to late evening"
    sf = font(SERIF_I, 16)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 138), sub,
           font=sf, fill=GREY)
    hrule(d, 164, width=3)

    # ---- lead: Shenzhen summit -----------------------------------------
    lx, lw = M, 528
    ax, aw = 572, W - M - 572
    y = 176
    y = kicker(d, lx, y, "Diplomacy  ·  The lead", size=15)
    y = para(d, lx, y, "Trump, Xi and Putin issue a 'peace declaration' in Shenzhen",
             font(SERIF_B, 45), lw, leading=50, max_lines=3)
    y = para(d, lx, y + 6,
             "The first-ever three-way summit closes at the APEC meeting "
             "with a joint declaration — silent on Ukraine and Iran — and "
             "Trump then dials into European allies to talk Ukraine.",
             font(SERIF, 19), lw, leading=23, max_lines=4)
    draw_lead_art(d, ax, 176, aw, 216)
    cap = "The three leaders met on Thursday at the APEC summit in Shenzhen, China."
    para(d, ax, 398, cap, font(SERIF_I, 13), aw, leading=16, max_lines=2)
    hrule(d, 442, width=3)

    # ---- three illustrated secondaries ---------------------------------
    col_w = 304
    gap = (CW - 3 * col_w) // 2
    xs = [M, M + col_w + gap, M + 2 * (col_w + gap)]
    secondary(d, xs[0], 454, col_w, draw_scales,
              "Justice",
              "UN court: Myanmar committed genocide",
              "The Hague rules 9–6 that the Rohingya crackdown was "
              "genocide; about 10,000 were killed.")
    secondary(d, xs[1], 454, col_w, draw_chart,
              "Markets",
              "Anthropic debut tops $2 trillion",
              "Shares close up 17% after the record $81.3bn IPO, the "
              "biggest ever, passing SpaceX's listing.")
    secondary(d, xs[2], 454, col_w, draw_capitol,
              "Washington",
              "Senate rejects curb on Trump's Iran war powers",
              "The 51–48 vote kills the resolution after a week of "
              "strikes across the Gulf.")
    hrule(d, 678)

    # ---- eight-story grid ----------------------------------------------
    gcol = 228
    ggap = (CW - 4 * gcol) // 3
    gx = [M + i * (gcol + ggap) for i in range(4)]
    grid = [
        ("Europe", "Crimean Bridge hit a third time",
         "Rail traffic halts after Ukraine's latest strike on the crossing."),
        ("Middle East", "Israeli tanks cross Gaza ceasefire line",
         "A rare ground push near Nuseirat; four allies urge aid access."),
        ("Culture", "Van Gogh sells for a record $190.4m",
         "The 1890 canvas sets an artist record despite its Nazi-era past."),
        ("Culture", "GTA VI arrives at last, 13 years on",
         "Vice City returns at midnight on PlayStation 5 and Xbox."),
        ("Space", "Voyager 1 sails one light-day from Earth",
         "NASA confirms the 48-year-old probe's record distance."),
        ("Americas", "Trump pardons baseball legend Pete Rose",
         "The late slugger, banned for betting, is pardoned posthumously."),
        ("Europe", "Denmark approves Greenland deal, 109–0",
         "Parliament backs the Arctic defence pact with the US."),
        ("Asia", "Four killed as unrest flares in Bangladesh",
         "Nobel laureate Yunus's ancestral home is set ablaze."),
    ]
    for i, (kick, head, deck) in enumerate(grid):
        row, col = divmod(i, 4)
        gy = 690 + row * 100
        grid_cell(d, gx[col], gy, gcol, kick, head, deck)
        if col < 3:
            vrule(d, gx[col] + gcol + ggap // 2, gy, gy + 92)
    hrule(d, 894)

    # ---- also today: eight briefs ---------------------------------------
    d.rectangle([M, 902, W - M, 984], fill=NAVY)
    d.text((M + 14, 908), "ALSO TODAY", font=font(SANS_B, 15), fill=GOLD)
    briefs = [
        "US and Venezuela sign a military deal",
        "Dozens missing as migrant boat sinks off Senegal",
        "Fiona the hippo dies at Cincinnati Zoo",
        "IAEA: North Korea expanding enrichment",
        "Houthis launch attacks on Saudi Arabia",
        "Jeffries nominated for House Speaker",
        "US auctions Pacific acres for deep-sea mining",
        "Fed minutes point to further rate hikes",
    ]
    bx = [M + 150, M + 150 + 420]
    bf = font(SANS, 14)
    for i, text in enumerate(briefs):
        col, row = divmod(i, 4)
        x = bx[col]
        y = 908 + row * 19
        d.text((x, y), "•", font=bf, fill=GOLD)
        d.text((x + 14, y), text, font=bf, fill=(240, 240, 240))

    # ---- footer ---------------------------------------------------------
    foot = ("Sources: BBC · The New York Times · Al Jazeera · Associated Press · "
            "Reuters · Breitbart — All stories reported 19 November 2026.")
    ff = font(SERIF, 12)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 994), foot,
           font=ff, fill=GREY)

    img.save(OUT, "PNG", optimize=True)
    print("wrote %s (%d bytes, %dx%d)" % (OUT, os.path.getsize(OUT), W, H))


if __name__ == "__main__":
    main()
