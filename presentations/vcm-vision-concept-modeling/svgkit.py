"""Minimal SVG authoring kit for slide figures.

Everything it emits is plain SVG markup with real <text> nodes and real vector
primitives, so the result stays editable in Inkscape/Illustrator and survives
PowerPoint's "Convert to Shape" round trip.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from xml.sax.saxutils import escape

# ---------------------------------------------------------------- design tokens

SLIDE_W = 1280
SLIDE_H = 720

NAVY = "#004282"
RED = "#C00000"
INK = "#101010"
GREY = "#6E7B8B"
MUTED = "#8A97A6"
FILL_BLUE = "#DCE8F5"
FILL_BLUE_D = "#9EC0E0"
FILL_GREY = "#F0F3F7"
FILL_RED = "#FBE4E4"
FILL_GREEN = "#DFF0E4"
GREEN = "#1E7A46"
AMBER = "#E8A33D"
FILL_AMBER = "#FBEFD9"
WHITE = "#FFFFFF"

# "Calibri" matches the reference deck on Windows/macOS PowerPoint; the build
# host aliases it to metric-compatible Carlito so previews match the real thing.
# Math is set in italic Calibri rather than a dedicated math font so that the
# glyph widths measured at build time are the widths PowerPoint will use.
SANS = "Calibri"
MATH = SANS
MONO = "Consolas"

# Symbols chosen for coverage in both Carlito and Calibri. The CTC-style blank
# (U+2205) and star (U+2605) are absent from both, so the deck uses these.
SYM_BLANK = "\u00f8"   # stands in for the blank symbol
SYM_KEEP = "\u2022"    # stands in for a retained vision concept

_ARROW_COLORS = {
    "navy": NAVY,
    "red": RED,
    "ink": INK,
    "grey": GREY,
    "muted": MUTED,
    "green": GREEN,
    "white": WHITE,
}


def _fmt(v: float) -> str:
    """Compact number formatting so the emitted markup stays readable."""
    if isinstance(v, int) or float(v).is_integer():
        return str(int(v))
    return f"{float(v):.2f}".rstrip("0").rstrip(".")


class _Metrics:
    """Glyph-accurate text widths, measured from the real font outlines.

    Carlito is metric-compatible with Calibri, so a width measured here is the
    width PowerPoint produces when it renders the deck with Calibri. Every
    multi-run text in this deck is positioned from these measurements instead of
    relying on ``text-anchor`` plus inline ``tspan`` flow, which renderers
    disagree about.
    """

    _FILES = {
        (False, False): "Carlito-Regular.ttf",
        (True, False): "Carlito-Bold.ttf",
        (False, True): "Carlito-Italic.ttf",
        (True, True): "Carlito-BoldItalic.ttf",
    }
    _DIRS = ("/usr/share/fonts/truetype/crosextra/",)
    _REF = 200  # measure once at a large size, then scale linearly

    def __init__(self):
        self._fonts = {}
        try:
            from PIL import ImageFont  # noqa: F401
            self._pil = True
        except ImportError:
            self._pil = False

    def _font(self, bold, italic):
        key = (bool(bold), bool(italic))
        if key not in self._fonts:
            from PIL import ImageFont
            for d in self._DIRS:
                path = d + self._FILES[key]
                if os.path.exists(path):
                    self._fonts[key] = ImageFont.truetype(path, self._REF)
                    break
            else:
                self._fonts[key] = None
        return self._fonts[key]

    def width(self, text, size, bold=False, italic=False):
        if not text:
            return 0.0
        if self._pil:
            font = self._font(bold, italic)
            if font is not None:
                return font.getlength(text) * size / self._REF
        return len(text) * size * (0.52 if bold else 0.48)


METRICS = _Metrics()


def text_width(text, size, weight=None, italic=False):
    return METRICS.width(text, size, bold=(weight == "bold"), italic=italic)


def _attrs(pairs: dict) -> str:
    out = []
    for key, value in pairs.items():
        if value is None:
            continue
        name = key.replace("__", ":").replace("_", "-")
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            value = _fmt(value)
        out.append(f'{name}="{value}"')
    return " ".join(out)


# ------------------------------------------------------------------- math markup

def _split_math(s: str):
    """Parse a tiny sub/superscript markup into (text, level) runs.

    ``H^{V}_{C}`` -> [("H", 0), ("V", 1), ("C", -1)] where level 1 is
    superscript and -1 is subscript.
    """
    runs, buf, i = [], "", 0
    while i < len(s):
        ch = s[i]
        if ch in "^_" and i + 1 < len(s) and s[i + 1] == "{":
            end = s.index("}", i + 2)
            if buf:
                runs.append((buf, 0))
                buf = ""
            runs.append((s[i + 2:end], 1 if ch == "^" else -1))
            i = end + 1
            continue
        buf += ch
        i += 1
    if buf:
        runs.append((buf, 0))
    return runs


@dataclass
class Canvas:
    """A drawing surface that also records which arrow markers it needs."""

    w: float
    h: float
    parts: list = field(default_factory=list)
    markers: set = field(default_factory=set)

    # -- primitives ---------------------------------------------------------

    def raw(self, markup: str) -> "Canvas":
        self.parts.append(markup)
        return self

    def rect(self, x, y, w, h, fill=WHITE, stroke=None, sw=1.6, rx=None,
             dash=None, opacity=None) -> "Canvas":
        return self.raw("<rect " + _attrs({
            "x": x, "y": y, "width": w, "height": h, "rx": rx, "ry": rx,
            "fill": fill or "none", "stroke": stroke, "stroke_width": sw if stroke else None,
            "stroke_dasharray": dash, "opacity": opacity,
        }) + "/>")

    def circle(self, cx, cy, r, fill=WHITE, stroke=None, sw=1.6, opacity=None) -> "Canvas":
        return self.raw("<circle " + _attrs({
            "cx": cx, "cy": cy, "r": r, "fill": fill or "none",
            "stroke": stroke, "stroke_width": sw if stroke else None, "opacity": opacity,
        }) + "/>")

    def ellipse(self, cx, cy, rx, ry, fill=WHITE, stroke=None, sw=1.6, dash=None) -> "Canvas":
        return self.raw("<ellipse " + _attrs({
            "cx": cx, "cy": cy, "rx": rx, "ry": ry, "fill": fill or "none",
            "stroke": stroke, "stroke_width": sw if stroke else None, "stroke_dasharray": dash,
        }) + "/>")

    def line(self, x1, y1, x2, y2, stroke=INK, sw=1.6, dash=None, cap="round",
             opacity=None) -> "Canvas":
        return self.raw("<line " + _attrs({
            "x1": x1, "y1": y1, "x2": x2, "y2": y2, "stroke": stroke,
            "stroke_width": sw, "stroke_dasharray": dash, "stroke_linecap": cap,
            "opacity": opacity,
        }) + "/>")

    def path(self, d, stroke=INK, sw=1.6, fill="none", dash=None, arrow=None,
             cap="round", opacity=None) -> "Canvas":
        marker = None
        if arrow:
            self.markers.add(arrow)
            marker = f"url(#arw-{arrow})"
        return self.raw("<path " + _attrs({
            "d": d, "stroke": stroke, "stroke_width": sw, "fill": fill,
            "stroke_dasharray": dash, "stroke_linecap": cap,
            "marker_end": marker, "opacity": opacity,
        }) + "/>")

    def poly(self, points, fill=WHITE, stroke=None, sw=1.6, opacity=None) -> "Canvas":
        pts = " ".join(f"{_fmt(x)},{_fmt(y)}" for x, y in points)
        return self.raw("<polygon " + _attrs({
            "points": pts, "fill": fill or "none", "stroke": stroke,
            "stroke_width": sw if stroke else None, "opacity": opacity,
        }) + "/>")

    def arrow(self, x1, y1, x2, y2, color="ink", sw=2.0, dash=None,
              curve=None) -> "Canvas":
        """Straight (or quadratic, when *curve* is a control offset) arrow."""
        stroke = _ARROW_COLORS.get(color, color)
        key = color if color in _ARROW_COLORS else "ink"
        if curve is None:
            d = f"M {_fmt(x1)} {_fmt(y1)} L {_fmt(x2)} {_fmt(y2)}"
        else:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            d = (f"M {_fmt(x1)} {_fmt(y1)} Q {_fmt(mx + curve[0])} "
                 f"{_fmt(my + curve[1])} {_fmt(x2)} {_fmt(y2)}")
        return self.path(d, stroke=stroke, sw=sw, dash=dash, arrow=key)

    # -- text ---------------------------------------------------------------

    def text(self, x, y, s, size=16, weight=None, fill=INK, anchor="start",
             family=SANS, italic=False, opacity=None, spacing=None) -> "Canvas":
        return self.raw("<text " + _attrs({
            "x": x, "y": y, "font_family": family, "font_size": size,
            "font_weight": weight, "font_style": "italic" if italic else None,
            "fill": fill, "text_anchor": anchor, "opacity": opacity,
            "letter_spacing": spacing, "xml__space": "preserve",
        }) + f">{escape(s)}</text>")

    def math_width(self, s, size, weight=None, italic=True) -> float:
        total = 0.0
        for run, level in _split_math(s):
            rs = size * 0.68 if level else size
            total += METRICS.width(run, rs, bold=(weight == "bold"), italic=italic)
        return total

    def math(self, x, y, s, size=16, fill=INK, anchor="start", weight=None,
             family=MATH, italic=True) -> "Canvas":
        """Text with ``^{}`` / ``_{}`` sub- and superscripts.

        Each run is emitted as its own ``<text>`` at a measured offset, so the
        layout is identical in every renderer.
        """
        runs = _split_math(s)
        if anchor == "middle":
            cursor = x - self.math_width(s, size, weight, italic) / 2
        elif anchor == "end":
            cursor = x - self.math_width(s, size, weight, italic)
        else:
            cursor = x
        for run, level in runs:
            rs = size * 0.68 if level else size
            dy = -size * 0.34 if level == 1 else (size * 0.20 if level == -1 else 0)
            self.raw("<text " + _attrs({
                "x": cursor, "y": y + dy, "font_family": family,
                "font_size": rs, "font_weight": weight,
                "font_style": "italic" if italic else None,
                "fill": fill, "text_anchor": "start",
                "xml__space": "preserve",
            }) + f">{escape(run)}</text>")
            cursor += METRICS.width(run, rs, bold=(weight == "bold"), italic=italic)
        return self

    def lines(self, x, y, rows, size=16, lh=None, **kw) -> "Canvas":
        lh = lh if lh is not None else size * 1.32
        for i, row in enumerate(rows):
            self.text(x, y + i * lh, row, size=size, **kw)
        return self

    # -- composites ---------------------------------------------------------

    def mbox(self, x, y, w, h, rows, size=16, fill=FILL_BLUE, stroke=NAVY,
             sw=1.6, rx=6, weight="bold", color=INK, lh=None, dash=None,
             anchor="middle") -> "Canvas":
        """A labelled module box with vertically centred lines of text."""
        self.rect(x, y, w, h, fill=fill, stroke=stroke, sw=sw, rx=rx, dash=dash)
        rows = [rows] if isinstance(rows, str) else list(rows)
        lh = lh if lh is not None else size * 1.24
        top = y + h / 2 - (len(rows) - 1) * lh / 2 + size * 0.35
        tx = x + w / 2 if anchor == "middle" else x + 10
        for i, row in enumerate(rows):
            self.text(tx, top + i * lh, row, size=size, weight=weight,
                      fill=color, anchor=anchor)
        return self

    def tag(self, x, y, s, size=13, fill=NAVY, color=WHITE, pad=8, h=22,
            weight="bold") -> "Canvas":
        """A small pill label centred on (x, y)."""
        w = len(s) * size * 0.52 + pad * 2
        self.rect(x - w / 2, y - h / 2, w, h, fill=fill, rx=h / 2, stroke=None)
        self.text(x, y + size * 0.36, s, size=size, weight=weight, fill=color,
                  anchor="middle")
        return self

    def brace(self, x1, y, x2, depth=10, stroke=GREY, sw=1.5, down=True) -> "Canvas":
        """A horizontal curly-ish brace spanning x1..x2."""
        d = depth if down else -depth
        mid = (x1 + x2) / 2
        return self.path(
            f"M {_fmt(x1)} {_fmt(y)} q 0 {_fmt(d)} {_fmt(min(12, (x2 - x1) / 4))} {_fmt(d)} "
            f"L {_fmt(mid - 6)} {_fmt(y + d)} q 6 0 6 {_fmt(d * 0.6)} "
            f"q 0 {_fmt(-d * 0.6)} 6 {_fmt(-d * 0.6)} "
            f"L {_fmt(x2 - min(12, (x2 - x1) / 4))} {_fmt(y + d)} "
            f"q {_fmt(min(12, (x2 - x1) / 4))} 0 {_fmt(min(12, (x2 - x1) / 4))} {_fmt(-d)}",
            stroke=stroke, sw=sw)

    def grid_tokens(self, x, y, cols, rows, cell, keep=None, gap=1.5,
                    on=FILL_BLUE_D, off=FILL_GREY, on_stroke=NAVY,
                    off_stroke="#D2DAE4", drop=()) -> "Canvas":
        """A patch grid; indices in *keep* are highlighted, in *drop* omitted."""
        keep = set() if keep is None else set(keep)
        for r in range(rows):
            for c in range(cols):
                idx = r * cols + c
                if idx in drop:
                    continue
                lit = idx in keep
                self.rect(x + c * (cell + gap), y + r * (cell + gap), cell, cell,
                          fill=on if lit else off,
                          stroke=on_stroke if lit else off_stroke,
                          sw=1.0, rx=1.5)
        return self

    # -- assembly -----------------------------------------------------------

    def defs(self) -> str:
        if not self.markers:
            return ""
        out = []
        for key in sorted(self.markers):
            color = _ARROW_COLORS.get(key, INK)
            out.append(
                f'<marker id="arw-{key}" viewBox="0 0 10 10" refX="8.5" refY="5" '
                f'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
                f'<path d="M 0 1 L 9 5 L 0 9 z" fill="{color}"/></marker>')
        return "<defs>" + "".join(out) + "</defs>"

    def body(self) -> str:
        return "".join(self.parts)

    def standalone(self) -> str:
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{_fmt(self.w)}" height="{_fmt(self.h)}" '
            f'viewBox="0 0 {_fmt(self.w)} {_fmt(self.h)}">'
            + self.defs() + self.body() + "</svg>")


# --------------------------------------------------------------- chart helpers

def bar_chart(cv: Canvas, x, y, w, h, items, *, vmin=None, vmax=None,
              value_fmt="{:.1f}", label_size=14, value_size=15, axis_label=None,
              baseline=None, baseline_label=None, bar_gap=0.34, sub_size=12):
    """Vertical bar chart.

    *items* is a list of dicts: ``{label, value, color, sub, edge, bold}``.
    Bars are drawn from a true zero-or-*vmin* baseline; ``vmin`` is only ever
    set explicitly by the caller so the axis choice stays visible in the source.
    """
    lo = min(i["value"] for i in items) if vmin is None else vmin
    hi = max(i["value"] for i in items) if vmax is None else vmax
    span = (hi - lo) or 1.0
    n = len(items)
    slot = w / n
    bw = slot * (1 - bar_gap)

    cv.line(x, y + h, x + w, y + h, stroke=GREY, sw=1.4)
    if axis_label:
        cv.text(x - 12, y - 8, axis_label, size=12, weight="bold", fill=GREY,
                anchor="start")

    if baseline is not None:
        by = y + h - (baseline - lo) / span * h
        cv.line(x, by, x + w, by, stroke=RED, sw=1.4, dash="6 4")
        if baseline_label:
            cv.text(x + w, by - 7, baseline_label, size=12, weight="bold",
                    fill=RED, anchor="end")

    for i, it in enumerate(items):
        cx = x + slot * (i + 0.5)
        bh = max(2.0, (it["value"] - lo) / span * h)
        cv.rect(cx - bw / 2, y + h - bh, bw, bh,
                fill=it.get("color", FILL_BLUE_D),
                stroke=it.get("edge", NAVY), sw=1.2, rx=2)
        cv.text(cx, y + h - bh - 9, value_fmt.format(it["value"]),
                size=value_size, weight="bold",
                fill=it.get("vcolor", it.get("edge", NAVY)), anchor="middle")
        for j, part in enumerate(str(it["label"]).split("\n")):
            cv.text(cx, y + h + 19 + j * (label_size + 2), part, size=label_size,
                    weight="bold" if it.get("bold") else None,
                    fill=it.get("lcolor", INK), anchor="middle")
        if it.get("sub"):
            nlines = len(str(it["label"]).split("\n"))
            cv.text(cx, y + h + 19 + nlines * (label_size + 2), it["sub"],
                    size=sub_size, fill=GREY, anchor="middle")
    return cv


def paired_bars(cv: Canvas, x, y, w, h, groups, *, vmin=0, vmax=None,
                value_fmt="{:.1f}", legend=None, label_size=14, value_size=13,
                colors=(FILL_GREY, FILL_BLUE_D), edges=(GREY, NAVY)):
    """Grouped before/after bars. *groups* = [{label, values:[a, b], sub}]."""
    hi = vmax if vmax is not None else max(max(g["values"]) for g in groups)
    span = (hi - vmin) or 1.0
    slot = w / len(groups)
    k = len(colors)
    bw = slot * 0.62 / k

    cv.line(x, y + h, x + w, y + h, stroke=GREY, sw=1.4)
    for gi, g in enumerate(groups):
        base = x + slot * (gi + 0.5)
        for vi, val in enumerate(g["values"]):
            bx = base + (vi - (k - 1) / 2) * bw - bw / 2
            bh = max(2.0, (val - vmin) / span * h)
            cv.rect(bx, y + h - bh, bw, bh, fill=colors[vi], stroke=edges[vi],
                    sw=1.2, rx=2)
            cv.text(bx + bw / 2, y + h - bh - 8, value_fmt.format(val),
                    size=value_size, weight="bold", fill=edges[vi],
                    anchor="middle")
        for j, part in enumerate(str(g["label"]).split("\n")):
            cv.text(base, y + h + 19 + j * (label_size + 1), part,
                    size=label_size, weight="bold", fill=INK, anchor="middle")
        if g.get("sub"):
            nl = len(str(g["label"]).split("\n"))
            cv.text(base, y + h + 19 + nl * (label_size + 1), g["sub"],
                    size=12, fill=GREY, anchor="middle")

    if legend:
        lx = x
        for li, name in enumerate(legend):
            cv.rect(lx, y - 20, 16, 12, fill=colors[li], stroke=edges[li], sw=1.2, rx=2)
            cv.text(lx + 22, y - 10, name, size=13, weight="bold", fill=edges[li])
            lx += 26 + len(name) * 7.4
    return cv


def table(cv: Canvas, x, y, cols, rows, *, size=14, row_h=26, head_h=28,
          head_fill=NAVY, head_color=WHITE, zebra=FILL_GREY,
          highlight=None, highlight_fill=FILL_BLUE, align=None):
    """A light data table. *cols* = [(title, width)]; *rows* = list of lists."""
    highlight = set() if highlight is None else set(highlight)
    align = align or ["left"] + ["middle"] * (len(cols) - 1)
    total = sum(c[1] for c in cols)

    cv.rect(x, y, total, head_h, fill=head_fill, rx=3, stroke=None)
    cx = x
    for (title, cw), al in zip(cols, align):
        tx = cx + 10 if al == "left" else cx + cw / 2
        cv.text(tx, y + head_h / 2 + size * 0.36, title, size=size,
                weight="bold", fill=head_color,
                anchor="start" if al == "left" else "middle")
        cx += cw

    for ri, row in enumerate(rows):
        ry = y + head_h + ri * row_h
        hit = ri in highlight
        if hit:
            cv.rect(x, ry, total, row_h, fill=highlight_fill, stroke=NAVY, sw=1.3)
        elif ri % 2 == 1:
            cv.rect(x, ry, total, row_h, fill=zebra, stroke=None)
        cx = x
        for (title, cw), cell, al in zip(cols, row, align):
            tx = cx + 10 if al == "left" else cx + cw / 2
            cv.text(tx, ry + row_h / 2 + size * 0.34, str(cell), size=size,
                    weight="bold" if hit else None,
                    fill=NAVY if hit else INK,
                    anchor="start" if al == "left" else "middle")
            cx += cw
    return cv
