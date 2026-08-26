#!/usr/bin/env python3
"""Check every NExT-OMNI SVG figure for geometric overflow."""

from __future__ import annotations

import importlib.util
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COMMON = ROOT.parent / "vcm-vision-concept-modeling"
sys.path.insert(0, str(COMMON))
sys.path.insert(0, str(ROOT))

import build  # noqa: E402
from content import SLIDES  # noqa: E402

spec = importlib.util.spec_from_file_location(
    "shared_layout_check", COMMON / "check_layout.py"
)
shared = importlib.util.module_from_spec(spec)
spec.loader.exec_module(shared)


def main():
    build.deck.SLIDES = SLIDES
    problems = 0
    for idx, slide in enumerate(SLIDES, start=1):
        box = build.deck.figure_box(slide)
        if box is None:
            continue
        _, _, width, height = box
        root = ET.fromstring(build.deck.build_figure(slide).standalone())
        hits = []
        for tag, x0, y0, x1, y1, label in shared.element_boxes(root):
            over = []
            if y1 > height + shared.TOL:
                over.append(f"bottom by {y1 - height:.0f}")
            if y0 < -shared.TOL:
                over.append(f"top by {-y0:.0f}")
            if x1 > width + shared.TOL:
                over.append(f"right by {x1 - width:.0f}")
            if x0 < -shared.TOL:
                over.append(f"left by {-x0:.0f}")
            if over:
                hits.append((tag, ", ".join(over), label))
        if hits:
            problems += len(hits)
            print(f"\nslide {idx:02d} {slide['key']}")
            for tag, over, label in hits:
                print(f"  {tag} overflows {over} {label}")
    print(f"\n{'no overflow' if not problems else f'{problems} overflowing elements'}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
