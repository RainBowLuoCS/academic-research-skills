#!/usr/bin/env python3
"""Build the NExT-OMNI deck as editable SVG, PDF, and PPTX."""

from __future__ import annotations

import argparse
import importlib.util
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COMMON = ROOT.parent / "vcm-vision-concept-modeling"
sys.path.insert(0, str(COMMON))
sys.path.insert(0, str(ROOT))

# Load the shared, tested slide renderer without colliding with this file name.
spec = importlib.util.spec_from_file_location("shared_deck_build", COMMON / "build.py")
deck = importlib.util.module_from_spec(spec)
spec.loader.exec_module(deck)

from content import SLIDES  # noqa: E402
from svgkit import Canvas  # noqa: E402
import figures  # noqa: E402

OUT = ROOT / "out"
SLIDE_DIR = OUT / "slides"
FIG_DIR = OUT / "figures"
PNG_DIR = OUT / "png"
STEM = "NExT_OMNI_talk"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--only", choices=["svg", "pdf", "pptx", "all"],
                    default="all")
    args = ap.parse_args()

    deck.SLIDES = SLIDES
    deck.OUT = OUT
    deck.SLIDE_DIR = SLIDE_DIR
    deck.FIG_DIR = FIG_DIR
    deck.PNG_DIR = PNG_DIR

    for directory in (SLIDE_DIR, FIG_DIR, PNG_DIR):
        if directory.exists():
            shutil.rmtree(directory)
        directory.mkdir(parents=True, exist_ok=True)

    slide_svgs, fig_assets = [], {}
    for idx, slide_def in enumerate(SLIDES, start=1):
        name = f"{idx:02d}_{slide_def['key']}"
        svg = deck.build_slide_svg(slide_def)
        slide_svgs.append(svg)
        (SLIDE_DIR / f"slide_{name}.svg").write_text(svg, encoding="utf-8")

        if slide_def.get("kind") == "title":
            cv = Canvas(deck.W, deck.H)
            figures.fig_title_motif(cv)
            box = (0, 0, deck.W, deck.H)
        else:
            cv = deck.build_figure(slide_def)
            box = deck.figure_box(slide_def)
        fig_svg = cv.standalone()
        (FIG_DIR / f"fig_{name}.svg").write_text(fig_svg, encoding="utf-8")
        fig_assets[idx] = (fig_svg.encode("utf-8"), box)

    print(f"  {len(slide_svgs)} slide SVGs -> out/slides")
    print(f"  {len(fig_assets)} figure SVGs -> out/figures")
    if args.only == "svg":
        return 0

    pngs = {}
    for idx, svg in enumerate(slide_svgs, start=1):
        name = f"{idx:02d}_{SLIDES[idx - 1]['key']}"
        png = deck.to_png(svg)
        (PNG_DIR / f"slide_{name}.png").write_bytes(png)
        pngs[idx] = png

    if args.only in ("pdf", "all"):
        deck.write_pdf(slide_svgs, OUT / f"{STEM}.pdf")
        print(f"  PDF  -> out/{STEM}.pdf")

    if args.only in ("pptx", "all"):
        import cairosvg
        figs = {}
        for idx, (svg_bytes, box) in fig_assets.items():
            png = cairosvg.svg2png(
                bytestring=svg_bytes,
                output_width=int(box[2] * 2),
                output_height=int(box[3] * 2),
            )
            figs[idx] = (svg_bytes, png, box)
        deck.write_pptx(OUT / f"{STEM}.pptx", figs)
        print(f"  PPTX -> out/{STEM}.pptx")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
