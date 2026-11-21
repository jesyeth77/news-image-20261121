#!/usr/bin/env python3
"""Paint the 21 Nov 2026 world-news front page (1024x1024 PNG).

Input is data/news.json; output is assets/entry.png, drawn with Pillow
and the bundled DejaVu typefaces. The drawing is fully deterministic —
no clock, network or randomness — so identical inputs give identical
pixels on every run. Run: python3 render.py
"""

from __future__ import annotations

import json
import os

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
CANVAS = 1024
MARGIN = 46

# Palette: deep navy masthead, paper white, signal red, brass gold.
PAPER = (250, 248, 243)
NAVY = (13, 33, 55)
NAVY_SOFT = (222, 231, 238)
RED = (178, 34, 34)
BRASS = (176, 138, 58)
INK = (24, 24, 22)
GREY = (96, 98, 94)
RULE = (203, 197, 184)
CARD = (238, 234, 226)
WHITE = (255, 255, 255)


def load(path: str) -> dict:
    """Read the day's stories from data/news.json."""
    with open(os.path.join(BASE, "data", path), encoding="utf-8") as fh:
        return json.load(fh)


class Page:
    """A 1024x1024 front page with text helpers."""

    def __init__(self) -> None:
        self.img = Image.new("RGB", (CANVAS, CANVAS), PAPER)
        self.pen = ImageDraw.Draw(self.img)

    def font(self, name: str, size: int) -> ImageFont.FreeTypeFont:
        return ImageFont.truetype(os.path.join(BASE, "fonts", name), size)

    def wrap(self, text: str, font: ImageFont.FreeTypeFont, width: int) -> list[str]:
        """Greedy word wrap of `text` to fit `width` pixels."""
        lines: list[str] = []
        line = ""
        for word in text.split():
            trial = (line + " " + word).strip()
            if self.pen.textlength(trial, font=font) <= width:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
        return lines

    def para(self, x: int, y: int, text: str, font: ImageFont.FreeTypeFont,
             colour: tuple[int, int, int], width: int, leading: int) -> int:
        """Set a wrapped paragraph; return the y below its last line."""
        for row in self.wrap(text, font, width):
            self.pen.text((x, y), row, font=font, fill=colour)
            y += leading
        return y

    def rule(self, y: int, weight: int = 2) -> int:
        self.pen.line([(MARGIN, y), (CANVAS - MARGIN, y)], fill=RULE, width=weight)
        return y + weight


def draw() -> None:
    """Compose the whole front page from data/news.json."""
    news = load("news.json")
    page = Page()
    pen = page.pen

    bold = lambda s: page.font("DejaVuSans-Bold.ttf", s)
    plain = lambda s: page.font("DejaVuSans.ttf", s)

    # --- Masthead: navy band, paper title, brass rule. ---
    pen.rectangle([0, 0, CANVAS, 118], fill=NAVY)
    pen.text((MARGIN, 18), news["masthead"], font=bold(52), fill=WHITE)
    pen.text((MARGIN, 84), news["date"].upper(), font=bold(17), fill=(197, 210, 222))
    pen.text((CANVAS - MARGIN - 210, 84), news["tagline"], font=plain(17),
             fill=(197, 210, 222))
    pen.line([(0, 118), (CANVAS, 118)], fill=BRASS, width=5)

    y = 140

    # --- Lead story: red kicker, big headline, summary, sources. ---
    lead = news["lead"]
    pen.text((MARGIN, y), "LEAD  ·  " + lead["kicker"], font=bold(16), fill=RED)
    y += 26
    y = page.para(MARGIN, y, lead["headline"], bold(40), INK,
                  CANVAS - 2 * MARGIN, 48)
    y += 8
    y = page.para(MARGIN, y, lead["summary"], plain(18), INK,
                  CANVAS - 2 * MARGIN, 25)
    y += 6
    pen.text((MARGIN, y), "Sources: " + " · ".join(lead["sources"]),
             font=plain(15), fill=GREY)
    y += 24
    y = page.rule(y)

    # --- Four numbered stories in a 2x2 grid. ---
    y += 16
    col_w = (CANVAS - 2 * MARGIN - 30) // 2
    row_top = y
    for idx, story in enumerate(news["stories"]):
        col = idx % 2
        row = idx // 2
        x = MARGIN + col * (col_w + 30)
        top = row_top + row * 186
        pen.rectangle([x, top, x + col_w, top + 184], fill=CARD)
        pen.text((x + 16, top + 12), f"{idx + 1:02d}", font=bold(26), fill=RED)
        pen.text((x + 62, top + 18), story["kicker"], font=bold(13), fill=NAVY)
        top = page.para(x + 16, top + 52, story["headline"], bold(21), INK,
                        col_w - 32, 27)
        page.para(x + 16, top + 6, story["summary"], plain(15), INK,
                  col_w - 32, 21)

    y = row_top + 2 * 186 + 8
    y = page.rule(y)

    # --- Also today: boxed strip of short items. ---
    y += 12
    pen.text((MARGIN, y), "ALSO TODAY", font=bold(16), fill=RED)
    y += 24
    for item in news["also"]:
        pen.text((MARGIN + 14, y), "•", font=bold(16), fill=BRASS)
        y = page.para(MARGIN + 34, y, item, plain(16), INK,
                      CANVAS - 2 * MARGIN - 34, 20)
        y += 1
    y += 6
    y = page.rule(y)

    # --- Footer: sources. ---
    y += 8
    pen.text((MARGIN, y), "Sources: " + news["footer_sources"],
             font=plain(14), fill=GREY)
    pen.text((CANVAS - MARGIN - 260, y), "make.fun · news-image-20261121",
             font=plain(14), fill=GREY)

    out = os.path.join(BASE, "assets", "entry.png")
    page.img.save(out, optimize=True)
    print(f"wrote {out} — {page.img.size[0]}x{page.img.size[1]}")


if __name__ == "__main__":
    draw()
