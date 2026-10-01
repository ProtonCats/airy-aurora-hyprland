#!/usr/bin/env python3
"""Build AiryBars.ttf: 16 rounded-capsule visualizer bars at U+10F100+level (0 = dot, 15 = full height)."""
import os
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen

LEVELS, ADV, W, BOTTOM, TOP, K = 16, 600, 340, -150, 760, 0.5523
OUT = os.path.expanduser("~/.local/share/fonts/AiryBars/AiryBars.ttf")


def capsule(pen, h):
    r, x0 = W / 2, (ADV - W) / 2
    x1, y0, y1 = x0 + W, BOTTOM, BOTTOM + h
    k = r * K
    pen.moveTo((x0, y0 + r))
    pen.lineTo((x0, y1 - r))
    pen.curveTo((x0, y1 - r + k), (x0 + r - k, y1), (x0 + r, y1))
    pen.curveTo((x0 + r + k, y1), (x1, y1 - r + k), (x1, y1 - r))
    pen.lineTo((x1, y0 + r))
    pen.curveTo((x1, y0 + r - k), (x0 + r + k, y0), (x0 + r, y0))
    pen.curveTo((x0 + r - k, y0), (x0, y0 + r - k), (x0, y0 + r))
    pen.closePath()


glyphs, cmap, names = {".notdef": TTGlyphPen(None).glyph()}, {}, [".notdef"]
for n in range(LEVELS):
    name = f"bar{n}"
    pen = TTGlyphPen(None)
    capsule(Cu2QuPen(pen, 1.0, reverse_direction=False), W + (TOP - BOTTOM - W) * n / (LEVELS - 1))
    glyphs[name] = pen.glyph()
    cmap[0x10F100 + n] = name
    names.append(name)

fb = FontBuilder(1000, isTTF=True)
fb.setupGlyphOrder(names)
fb.setupCharacterMap(cmap)
fb.setupGlyf(glyphs)
fb.setupHorizontalMetrics({n: (ADV, 0) for n in names})
fb.setupHorizontalHeader(ascent=800, descent=-200)
fb.setupNameTable({"familyName": "AiryBars", "styleName": "Regular"})
fb.setupOS2(sTypoAscender=800, sTypoDescender=-200, usWinAscent=800, usWinDescent=200)
fb.setupPost()
os.makedirs(os.path.dirname(OUT), exist_ok=True)
fb.save(OUT)
print(OUT)
