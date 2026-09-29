#!/usr/bin/env python3
"""Build AiryJP.ttf, the icon font of the Airy kanji add-on.

Icons are drawn as strokes on a 24x24 grid, outlined and unioned by Inkscape, then packed
into a TTF at U+10F000+index (index = order in ICONS; append new icons, never reorder).
`build.py preview` renders a sheet of every icon instead. Needs inkscape, fontTools, cairosvg, Pillow.
"""
import math, os, subprocess, sys, tempfile, xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.environ.get("ICON_WORK") or tempfile.mkdtemp(prefix="airyjp-")
FONT_OUT = os.path.join(HERE, "..", "kanji", ".local", "share", "fonts", "AiryJP", "AiryJP.ttf")
BASE = 0x10F000
F = 'fill="#000" stroke="none"'  # filled shape inside the stroked group


def spiral(turns=1.5, r0=1.0, r1=6.4, n=90):
    pts = []
    for i in range(n + 1):
        t = i / n
        a = t * turns * 2 * math.pi - math.pi / 2
        r = r0 + (r1 - r0) * t
        pts.append(f"{12 + r * math.cos(a):.2f} {12 + r * math.sin(a):.2f}")
    return "M" + " L".join(pts)


def rays(r_in, r_out, n=8, cx=12, cy=12):
    out = []
    for i in range(n):
        a = i * 2 * math.pi / n
        out.append(f"M{cx + r_in * math.cos(a):.2f} {cy + r_in * math.sin(a):.2f}"
                   f"L{cx + r_out * math.cos(a):.2f} {cy + r_out * math.sin(a):.2f}")
    return " ".join(out)


PETAL = "M12 12 C8.4 9.8 8.4 4.6 10.5 3.2 L12 4.6 L13.5 3.2 C15.6 4.6 15.6 9.8 12 12 Z"
SAKURA = "".join(f'<path d="{PETAL}" transform="rotate({a} 12 12)"/>' for a in range(0, 360, 72))
CLOUD = "M7 18.5 H17.4 A3.9 3.9 0 0 0 17 10.7 A5.5 5.5 0 0 0 6.7 12.3 A3.1 3.1 0 0 0 7 18.5 Z"
MOON = "M19.5 14.6 A8 8 0 1 1 9.4 4.5 A6.4 6.4 0 0 0 19.5 14.6 Z"
SUN = f'<circle cx="12" cy="12" r="4"/><path d="{rays(6.8, 9.6)}"/>'
SUSHI = ('<path d="M3 12.6 C3 9.6 6.6 8 12 8 S21 9.6 21 12.6 C21 13.7 20 14.2 19 14.2 H5 C4 14.2 3 13.7 3 12.6 Z"/>'
         '<path d="M5.6 14.2 V17 C5.6 18.2 6.5 19 7.7 19 H16.3 C17.5 19 18.4 18.2 18.4 17 V14.2"/>'
         '<path d="M9.2 9.2 L8.4 13 M13.4 8.7 L12.6 13.2"/>')
FURIN = ('<path d="M12 2.4 V5"/><path d="M4.4 13.4 C4.4 8.2 8 5 12 5 S19.6 8.2 19.6 13.4 Z"/>'
         '<path d="M12 13.4 V16"/><path d="M9 16 H15 V22 H9 Z"/>')
KOI = ('<path d="M2.5 12 C5 7.2 11 6.5 15.5 9.5 L21.5 6 L19.5 12 L21.5 18 L15.5 14.5 C11 17.5 5 16.8 2.5 12 Z"/>'
       f'<circle cx="7.2" cy="11" r="1.2" {F}/>')
SLASH = '<path d="M3.5 20.5 L20.5 3.5" stroke-width="2.4"/>'
CASTLE = ('<path d="M2 16.2 Q6 16.2 7 13.6 H17 Q18 16.2 22 16.2"/><path d="M5 16.2 V21.5 H19 V16.2"/>'
          '<path d="M8.4 13.6 V10.8 H15.6 V13.6"/><path d="M5.6 11 Q9.2 11 9.8 8.4 H14.2 Q14.8 11 18.4 11"/>'
          '<path d="M9.8 8.4 V6.2 H14.2 V8.4"/><path d="M8 6.4 Q11 6.2 12 3 Q13 6.2 16 6.4"/>'
          '<path d="M10.5 21.5 V18.8 H13.5 V21.5"/>')

ICONS = {
    "narutomaki": f'<circle cx="12" cy="12" r="9.2"/><path d="{spiral()}"/>',
    "sakura": SAKURA,
    "moon": f'<path d="{MOON}"/><path d="M17.6 2.8 V6.6 M15.7 4.7 H19.5" stroke-width="1.5"/>',
    "bento": ('<rect x="2.8" y="5" width="18.4" height="14" rx="2.6"/><path d="M12 5 V19 M12 12 H21"/>'
              f'<circle cx="7.4" cy="12" r="2.4"/><circle cx="16.6" cy="8.6" r="1.1" {F}/>'
              f'<circle cx="16.6" cy="15.6" r="1.1" {F}/>'),
    "dango": ('<g transform="rotate(35 12 12)"><path d="M12 1 V3 M12 21 V23"/>'
              '<circle cx="12" cy="6.1" r="3.1"/><circle cx="12" cy="12" r="3.1"/><circle cx="12" cy="17.9" r="3.1"/></g>'),
    "onigiri": ('<path d="M12 3.4 C13.2 3.4 14 4 14.8 5.3 L20.3 15.4 C21.4 17.4 20.4 20 17.8 20 H6.2 '
                'C3.6 20 2.6 17.4 3.7 15.4 L9.2 5.3 C10 4 10.8 3.4 12 3.4 Z"/>'
                f'<path d="M8.6 20 V14.6 H15.4 V20 Z" {F}/>'),
    "shuriken": ('<path d="M12 2 L14.3 9.7 L22 12 L14.3 14.3 L12 22 L9.7 14.3 L2 12 L9.7 9.7 Z"/>'
                 '<circle cx="12" cy="12" r="1.9"/>'),
    "bamboo": ('<path d="M9.5 2.5 H14.5 V10 H9.5 Z M9.5 12.6 H14.5 V21.5 H9.5 Z"/>'
               '<path d="M14.5 7 C17 4.4 20 4.4 21.6 5.4 C20.6 8.4 17.4 9 14.5 7 Z"/>'
               '<path d="M9.5 17 C7 14.8 4 14.8 2.4 15.8 C3.4 18.8 6.6 19.4 9.5 17 Z"/>'),
    "sushi": SUSHI,
    "sushi_dnd": SUSHI + SLASH,
    "dot": f'<circle cx="12" cy="12" r="6" {F}/>',
    "chochin": ('<path d="M8 2.5 H16 V5 H8 Z"/><path d="M8 19 V21.5 H16 V19"/>'
                '<path d="M8 5 C3.5 6 2.8 9 2.8 12 S3.5 18 8 19 H16 C20.5 18 21.2 15 21.2 12 S20.5 6 16 5"/>'
                '<path d="M3.4 9 Q12 11.6 20.6 9 M3.4 15 Q12 17.6 20.6 15"/>'),
    "sun": SUN,
    "sunset": ('<path d="M7.4 16.5 A4.6 4.6 0 0 1 16.6 16.5"/><path d="M3 16.5 H21 M6 20.5 H18"/>'
               '<path d="M12 6.4 V8.4 M5.4 9.4 L6.9 10.9 M18.6 9.4 L17.1 10.9"/>'),
    "cloud": f'<path d="{CLOUD}" transform="translate(0 -1)"/>',
    "cloud_off": f'<path d="{CLOUD}" transform="translate(0 -1)"/>' + SLASH,
    "rain": (f'<path d="{CLOUD}" transform="translate(0 -3.5)"/>'
             '<path d="M8.2 17.2 L7.2 20.2 M12.2 17.2 L11.2 20.2 M16.2 17.2 L15.2 20.2"/>'),
    "snow": (f'<path d="{CLOUD}" transform="translate(0 -3.5)"/>'
             f'<circle cx="8" cy="18.6" r="1" {F}/><circle cx="12" cy="20.8" r="1" {F}/><circle cx="16" cy="18.6" r="1" {F}/>'),
    "storm": (f'<path d="{CLOUD}" transform="translate(0 -3.5)"/>'
              '<path d="M12.8 14.6 L10 18.6 H14 L11.2 22.6"/>'),
    "tokkuri": ('<path d="M10 2.6 H14 V5.2 C14 7 16.6 8 16.6 11 V19.4 C16.6 20.4 15.8 21.2 14.8 21.2 H9.2 '
                'C8.2 21.2 7.4 20.4 7.4 19.4 V11 C7.4 8 10 7 10 5.2 Z"/><path d="M7.6 13.4 H16.4"/>'),
    "senbei": ('<circle cx="12" cy="12" r="9.2"/>'
               f'<ellipse cx="8.6" cy="9" rx="1.3" ry="0.8" transform="rotate(-25 8.6 9)" {F}/>'
               f'<ellipse cx="15" cy="8" rx="1.3" ry="0.8" transform="rotate(20 15 8)" {F}/>'
               f'<ellipse cx="15.6" cy="14" rx="1.3" ry="0.8" transform="rotate(-20 15.6 14)" {F}/>'
               f'<ellipse cx="9.4" cy="15.6" rx="1.3" ry="0.8" transform="rotate(30 9.4 15.6)" {F}/>'
               f'<ellipse cx="12" cy="11.8" rx="1.3" ry="0.8" {F}/>'),
    "yunomi": ('<path d="M5.4 8.4 H18.6 L17.6 15 C17.2 18.2 15 20.6 12 20.6 S6.8 18.2 6.4 15 Z"/>'
               '<path d="M9.6 2.8 C8.6 4.4 10.6 5.4 9.6 7 M14.4 2.8 C13.4 4.4 15.4 5.4 14.4 7"/>'),
    "flame": ('<path d="M12 2.5 C13 6 18 8.5 18 14 A6 6 0 0 1 6 14 C6 11.5 7.5 10 8.8 8.8 '
              'C9 10.4 9.8 11 10.6 11 C10.2 8 10.6 5 12 2.5 Z"/>'),
    "tomoe": ('<circle cx="12" cy="12" r="9.2"/><path d="M12 2.8 A4.6 4.6 0 0 1 12 12 A4.6 4.6 0 0 0 12 21.2"/>'
              f'<circle cx="12" cy="7.4" r="1.1" {F}/>'),
    "leaf": '<path d="M4.6 19.4 C3.6 10 10 4 20 4 C20 14 14 20.4 4.6 19.4 Z"/><path d="M4.6 19.4 C9 15 12 12 16 9"/>',
    "koi": KOI,
    "koi_off": KOI + SLASH,
    "furin": FURIN,
    "furin_off": FURIN + SLASH,
    "castle": CASTLE,
    "torii": ('<path d="M1.8 4 Q12 7.4 22.2 4"/><path d="M4 9.2 H20 M5.6 13.6 H18.4 M12 6.4 V9.2"/>'
              '<path d="M7 9.2 V21.6 M17 9.2 V21.6"/>'),
}
NAMES = list(ICONS)


def wrap(inner):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">'
            '<g fill="none" stroke="#000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            f'{inner}</g></svg>')


ACTIONS = ("select-all:all;selection-ungroup;select-all:all;object-to-path;object-stroke-to-path;"
           "selection-ungroup;select-all:all;path-union;export-filename:{out};export-plain-svg;export-do")


def outline(name):
    src, out = f"{WORK}/{name}.src.svg", f"{WORK}/{name}.svg"
    open(src, "w").write(wrap(ICONS[name]))
    subprocess.run(["inkscape", "--batch-process", f"--actions={ACTIONS.format(out=out)}", src],
                   check=True, capture_output=True)
    return out


def path_d(svg):
    ns = {"s": "http://www.w3.org/2000/svg"}
    paths = ET.parse(svg).getroot().findall(".//s:path", ns)
    assert len(paths) == 1, (svg, len(paths))
    return paths[0].get("d")


def build_font(ds):
    from fontTools.fontBuilder import FontBuilder
    from fontTools.pens.cu2quPen import Cu2QuPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.pens.ttGlyphPen import TTGlyphPen
    from fontTools.svgLib.path import parse_path

    scale, cy, adv = 54.0, 370, 1300  # 24 units -> 1296 font units, centred just above the x-height middle
    glyphs = {".notdef": TTGlyphPen(None).glyph()}
    for n, d in ds.items():
        pen = TTGlyphPen(None)
        parse_path(d, TransformPen(Cu2QuPen(pen, 1.0, reverse_direction=True),
                                   (scale, 0, 0, -scale, (adv - 24 * scale) / 2, cy + 12 * scale)))
        glyphs[n] = pen.glyph()
    order = [".notdef"] + list(ds)
    fb = FontBuilder(1000, isTTF=True)
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap({BASE + i: n for i, n in enumerate(ds)})
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics({n: (adv, 0) for n in order})
    fb.setupHorizontalHeader(ascent=950, descent=-250)
    fb.setupNameTable({"familyName": "AiryJP", "styleName": "Regular"})
    fb.setupOS2(sTypoAscender=950, sTypoDescender=-250, usWinAscent=950, usWinDescent=250)
    fb.setupPost()
    os.makedirs(os.path.dirname(FONT_OUT), exist_ok=True)
    fb.font.save(FONT_OUT)


def preview(files):
    import cairosvg
    from PIL import Image
    cell, cols = 120, 8
    rows = -(-len(files) // cols)
    sheet = Image.new("RGB", (cell * cols, cell * rows), "#1B1E26")
    for i, n in enumerate(NAMES):
        cairosvg.svg2png(url=files[n], write_to=f"{WORK}/{n}.png", output_width=96, output_height=96,
                         background_color="white")
        # outlines are black; recolour to ice-blue on the dark cell
        im = Image.open(f"{WORK}/{n}.png").convert("L")
        col = Image.new("RGB", im.size, "#AACCDD")
        sheet.paste(col, (i % cols * cell + 12, i // cols * cell + 12), Image.eval(im, lambda v: 255 - v))
    sheet.save(f"{WORK}/sheet.png")


if __name__ == "__main__":
    os.makedirs(WORK, exist_ok=True)
    files = {n: outline(n) for n in NAMES}
    if sys.argv[1:] == ["preview"]:
        preview(files)
        print(f"{WORK}/sheet.png")
    else:
        build_font({n: path_d(files[n]) for n in NAMES})
        print("\n".join(f"U+{BASE + i:X} {n}" for i, n in enumerate(NAMES)))
