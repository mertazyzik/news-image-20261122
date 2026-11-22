#!/usr/bin/env python3
"""Render the front page of 'The World in One Day' for 22 November 2026.

A single 1024x1024 PNG newspaper page, drawn with Pillow. All text is
baked into this file, so the render is deterministic: the same input
always produces the same bytes. Run: python3 draw.py  (writes entry.png
next to this file).
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (24, 22, 18)
RED = (158, 28, 32)
GREY = (96, 90, 80)
RULE = (24, 22, 18)
LIGHT_RULE = (180, 172, 156)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning lines that fit `width` px."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for word in words:
            trial = (cur + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, leading, color=INK):
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def story(draw, x, y, width, kicker, title, body, title_size=23,
          title_lead=28, body_size=15, body_lead=20):
    draw.text((x, y), kicker, font=font(SANS_B, 13), fill=RED)
    y += 20
    y = para(draw, x, y, title, font(SERIF_B, title_size), width,
             title_lead)
    y += 3
    y = para(draw, x, y, body, font(SERIF, body_size), width, body_lead)
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Outer frame.
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=3)
    d.rectangle([22, 22, W - 23, H - 23], outline=INK, width=1)

    # Top dateline strip.
    d.text((34, 32), "SUNDAY, 22 NOVEMBER 2026", font=font(SANS_B, 15),
           fill=INK)
    right = "THE WORLD  •  ONE PAGE  •  No. 326"
    d.text((W - 34 - d.textlength(right, font=font(SANS_B, 15)), 32),
           right, font=font(SANS_B, 15), fill=INK)
    d.line([(34, 58), (W - 34, 58)], fill=RULE, width=2)

    # Masthead.
    mast = "THE WORLD IN ONE DAY"
    mw = d.textlength(mast, font=font(SERIF_B, 58))
    d.text(((W - mw) / 2, 66), mast, font=font(SERIF_B, 58), fill=INK)
    d.line([(34, 138), (W - 34, 138)], fill=RULE, width=3)
    d.line([(34, 144), (W - 34, 144)], fill=RULE, width=1)

    # ---- Lead story: COP31, full width ----
    y = story(
        d, 34, 156, W - 68,
        "CLIMATE  •  ANTALYA, TURKEY",
        "COP31 draft drops fossil fuels as talks run into a second day of overtime",
        "A new deal draft released in the early hours of Sunday makes no mention of "
        "fossil fuels at all: the words \u201cfossil\u201d, \u201coil\u201d, \u201ccoal\u201d and "
        "\u201cphase out\u201d appear nowhere in its ten pages. Instead it recalls the 2023 "
        "Dubai pledge, sets electricity at 35% of energy use by 2035, and backs "
        "capturing one billion tonnes of carbon a year.",
        title_size=28, title_lead=34, body_size=16, body_lead=22)
    d.line([(34, y + 10), (W - 34, y + 10)], fill=RULE, width=2)
    y += 24

    # ---- Middle: two columns ----
    col_w = (W - 68 - 28) // 2
    left_x, right_x = 34, 34 + col_w + 28
    top_y = y

    ly = story(
        d, left_x, top_y, col_w,
        "MIDDLE EAST  •  BAHRAIN",
        "Iran strikes US bases in Bahrain; industrial site hit, no one hurt",
        "Iran\u2019s Revolutionary Guards said they fired missiles and drones at US "
        "positions at the Al-Riffa and Awali bases overnight, claiming two Patriot "
        "radars were hit. Bahrain said its air defences intercepted several attacks "
        "and a civilian industrial site caught fire.")
    ly += 12
    d.line([(left_x, ly), (left_x + col_w, ly)], fill=LIGHT_RULE, width=1)
    ly += 12
    ly = story(
        d, left_x, ly, col_w,
        "MEXICO  •  SINALOA",
        "FBI most-wanted cartel boss seized in raid; 11 killed",
        "Fausto Isidro Meza Flores, \u201cEl Chapo Isidro\u201d, was captured in Guasave "
        "on Friday night with US intelligence help. Four soldiers and seven gunmen "
        "died; eight people were arrested. He was flown to Mexico City on Saturday.")

    ry = story(
        d, right_x, top_y, col_w,
        "BALTIC SEA  •  GULF OF FINLAND",
        "Russian cargo ship still burning after drone strike",
        "The Sparta II, bound for Kaliningrad, was hit by two drones on Saturday and "
        "drifted into Finnish waters, still on fire on Sunday. All 16 crew were "
        "evacuated. Finland\u2019s military said the strike was likely by Ukraine.")
    ry += 12
    d.line([(right_x, ry), (right_x + col_w, ry)], fill=LIGHT_RULE, width=1)
    ry += 12
    ry = story(
        d, right_x, ry, col_w,
        "INDONESIA  •  WEST JAVA",
        "Three dead, 36 missing after fire at Java candy factory",
        "The blaze broke out on Saturday evening at the Fonusa Agung Mulia factory "
        "in Cikande, Serang. Rescuers searched on Sunday for 36 workers; 15 people "
        "survived, four of them taken to hospital.")

    y = max(ly, ry) + 12
    d.line([(34, y), (W - 34, y)], fill=RULE, width=2)
    y += 14

    # ---- Sport strip ----
    y = story(
        d, 34, y, W - 68,
        "SPORT  •  LAS VEGAS",
        "Verstappen wins wild Las Vegas Grand Prix",
        "Max Verstappen held off Lando Norris by 0.639 seconds for his third Las Vegas "
        "win in four years, with Oscar Piastri third. The 50-lap race featured 35 lead "
        "changes; George Russell hit the wall three laps from the end.",
        title_size=24, title_lead=29, body_size=15, body_lead=20)
    d.line([(34, y + 8), (W - 34, y + 8)], fill=RULE, width=2)
    y += 22

    # ---- Also in the news: one line per item, two columns ----
    d.text((34, y), "ALSO IN THE NEWS", font=font(SANS_B, 13), fill=RED)
    y += 22
    also = [
        ("NIGERIA", "24 dead as a boat of funeral mourners capsizes in Bayelsa."),
        ("UNITED STATES", "FBI probes hack of its NCIC database."),
        ("SOUTH KOREA", "Education minister quits over exam cheating chaos."),
        ("ITALY", "Jeweller Paolo Bulgari dies aged 89."),
    ]
    half = (W - 68 - 28) // 2
    for i, (tag, text) in enumerate(also):
        x = 34 if i % 2 == 0 else 34 + half + 28
        yy = y + (i // 2) * 24
        d.text((x, yy), tag + " — ", font=font(SANS_B, 13), fill=INK)
        tw = d.textlength(tag + " — ", font=font(SANS_B, 13))
        d.text((x + tw, yy), text, font=font(SERIF, 13), fill=INK)
    y += 48

    # ---- Footer ----
    fy = H - 56
    d.line([(34, fy), (W - 34, fy)], fill=RULE, width=1)
    foot = ("Sources: Reuters, Associated Press, BBC, Formula 1, AFP  •  "
            "All stories reported on 22 November 2026")
    fw = d.textlength(foot, font=font(SANS, 13))
    d.text(((W - fw) / 2, fy + 9), foot, font=font(SANS, 13), fill=GREY)

    img.save("entry.png", format="PNG")
    print("wrote entry.png", img.size, "content ends at y =", y,
          "footer at", fy)


if __name__ == "__main__":
    main()
