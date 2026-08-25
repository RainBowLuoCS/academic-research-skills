#!/usr/bin/env python3
"""Geometry check for the generated deck.

Parses every figure SVG and reports elements that fall outside their region, so
overflow is caught mechanically instead of by eye. Text extents are computed
from the same font metrics the build uses.

    python3 check_layout.py
"""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import build
from content import CONDENSED_SLIDES, SLIDES
from svgkit import text_width

SVG_NS = "{http://www.w3.org/2000/svg}"
TOL = 1.0  # px of slack, to ignore stroke-width rounding


def _f(el, name, default=0.0):
    try:
        return float(el.get(name, default))
    except (TypeError, ValueError):
        return default


def _path_extent(d):
    """Extent of an absolute-only path.

    Relative commands and arcs carry operands that are not coordinate pairs, so
    those paths are skipped rather than measured wrongly.
    """
    if re.search(r"[a-zA]", d.replace("e-", "").replace("e+", "")):
        return None   # relative commands and arcs are not plain coordinate pairs
    nums = [float(n) for n in re.findall(r"-?\d+\.?\d*", d)]
    xs, ys = nums[0::2], nums[1::2]
    return (min(xs), min(ys), max(xs), max(ys)) if xs and ys else None


def element_boxes(root):
    """Yield (tag, x0, y0, x1, y1, label) for every drawable leaf."""
    for el in root.iter():
        tag = el.tag.replace(SVG_NS, "")
        if tag == "rect":
            x, y = _f(el, "x"), _f(el, "y")
            yield tag, x, y, x + _f(el, "width"), y + _f(el, "height"), ""
        elif tag == "circle":
            cx, cy, r = _f(el, "cx"), _f(el, "cy"), _f(el, "r")
            yield tag, cx - r, cy - r, cx + r, cy + r, ""
        elif tag == "ellipse":
            cx, cy = _f(el, "cx"), _f(el, "cy")
            rx, ry = _f(el, "rx"), _f(el, "ry")
            yield tag, cx - rx, cy - ry, cx + rx, cy + ry, ""
        elif tag == "line":
            x1, y1, x2, y2 = (_f(el, k) for k in ("x1", "y1", "x2", "y2"))
            yield tag, min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2), ""
        elif tag in ("path", "polygon"):
            geom = el.get("d") or el.get("points")
            ext = _path_extent(geom) if geom else None
            if ext:
                yield tag, *ext, ""
        elif tag == "text":
            size = _f(el, "font-size", 12)
            weight = el.get("font-weight")
            italic = el.get("font-style") == "italic"
            content = "".join(el.itertext())
            w = text_width(content, size, weight, italic)
            x, y = _f(el, "x"), _f(el, "y")
            anchor = el.get("text-anchor", "start")
            if anchor == "middle":
                x -= w / 2
            elif anchor == "end":
                x -= w
            # Rough vertical ink box around the baseline.
            yield tag, x, y - size * 0.78, x + w, y + size * 0.26, content[:44]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--deck", choices=["full", "condensed"], default="full")
    args = ap.parse_args()
    slides = CONDENSED_SLIDES if args.deck == "condensed" else SLIDES
    build.SLIDES = slides

    problems = 0
    for idx, slide in enumerate(slides, start=1):
        box = build.figure_box(slide)
        if box is None:
            continue
        _, _, w, h = box
        cv = build.build_figure(slide)
        root = ET.fromstring(cv.standalone())
        hits = []
        for tag, x0, y0, x1, y1, label in element_boxes(root):
            over = []
            if y1 > h + TOL:
                over.append(f"bottom by {y1 - h:.0f}")
            if y0 < -TOL:
                over.append(f"top by {-y0:.0f}")
            if x1 > w + TOL:
                over.append(f"right by {x1 - w:.0f}")
            if x0 < -TOL:
                over.append(f"left by {-x0:.0f}")
            if over:
                hits.append((tag, ", ".join(over), label))
        if hits:
            problems += len(hits)
            print(f"\nslide {idx:02d} {slide['key']}  (region {w:.0f}x{h:.0f})")
            for tag, over, label in sorted(hits, key=lambda t: t[1]):
                suffix = f'  "{label}"' if label else ""
                print(f"    {tag:8s} overflows {over}{suffix}")

    print(f"\n{'no overflow' if not problems else f'{problems} overflowing elements'}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
