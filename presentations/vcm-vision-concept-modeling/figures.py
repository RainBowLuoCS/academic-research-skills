"""Figure bodies for the VCM talk.

Each ``fig_*`` function draws into a :class:`svgkit.Canvas` whose local origin is
the top-left of the slide's figure region. Only vector primitives and real text
are used, so every figure stays editable after export.
"""

from __future__ import annotations

from content import DATA
from svgkit import (
    AMBER, FILL_AMBER, FILL_BLUE, FILL_BLUE_D, FILL_GREEN, FILL_GREY, FILL_RED,
    GREEN, GREY, INK, MATH, MONO, MUTED, NAVY, RED, SANS, SYM_BLANK,
    SYM_KEEP, WHITE, Canvas,
    bar_chart, paired_bars, table,
)

BORDER = "#C9D6E4"


# ------------------------------------------------------------------- utilities

def panel(cv, x, y, w, h, title=None, fill=WHITE, stroke=BORDER, sw=1.4, rx=8,
          tcolor=NAVY, tsize=17):
    """Draw a bordered panel; return the y where its content can start."""
    cv.rect(x, y, w, h, fill=fill, stroke=stroke, sw=sw, rx=rx)
    if title:
        cv.text(x + 16, y + 25, title, size=tsize, weight="bold", fill=tcolor)
        return y + 42
    return y + 14


def note(cv, x, y, s, size=12, fill=MUTED, anchor="start", weight=None):
    cv.text(x, y, s, size=size, fill=fill, anchor=anchor, weight=weight)


def axis_note(cv, x, y, start, anchor="start"):
    note(cv, x, y, f"Avg. (%) — vertical axis starts at {start}", size=11.5,
         anchor=anchor)


def chevron(cv, x, y, w, h, rows, fill=FILL_BLUE, stroke=NAVY, size=14,
            notch=16, color=INK):
    """A right-pointing chevron used for pipeline steps."""
    cv.poly([(x, y), (x + w - notch, y), (x + w, y + h / 2),
             (x + w - notch, y + h), (x, y + h), (x + notch, y + h / 2)],
            fill=fill, stroke=stroke, sw=1.5)
    rows = [rows] if isinstance(rows, str) else list(rows)
    lh = size * 1.22
    top = y + h / 2 - (len(rows) - 1) * lh / 2 + size * 0.34
    for i, row in enumerate(rows):
        cv.text(x + w / 2 + notch / 2, top + i * lh, row, size=size,
                weight="bold", fill=color, anchor="middle")


def flow_text(cv, x, y, words, size=14, gap=5, default=INK, weights=None):
    """Lay out a sentence word by word, advancing by measured glyph widths.

    *words* is a list of ``(text, colour)`` pairs. Returns the end x.
    """
    from svgkit import text_width
    cursor = x
    for i, item in enumerate(words):
        word, colour = item if isinstance(item, tuple) else (item, default)
        weight = weights[i] if weights else ("bold" if colour != default else None)
        cv.text(cursor, y, word, size=size, weight=weight, fill=colour)
        cursor += text_width(word, size, weight) + gap
    return cursor - gap


def image_glyph(cv, x, y, w, h, fill="#EDF2F8", stroke="#B9C8D8"):
    """A neutral 'photo' placeholder: frame, horizon, sun, hill."""
    cv.rect(x, y, w, h, fill=fill, stroke=stroke, sw=1.4, rx=4)
    cv.circle(x + w * 0.26, y + h * 0.3, min(w, h) * 0.1, fill="#F6D68A",
              stroke="#D9AE4E", sw=1.1)
    cv.path(f"M {x + 4} {y + h - 6} L {x + w * 0.36} {y + h * 0.46} "
            f"L {x + w * 0.56} {y + h - 6} Z", fill="#BFD3E6", stroke="#93AFC9", sw=1.1)
    cv.path(f"M {x + w * 0.42} {y + h - 6} L {x + w * 0.68} {y + h * 0.36} "
            f"L {x + w - 4} {y + h - 6} Z", fill="#A8C1DA", stroke="#8AA7C2", sw=1.1)


def bubble(cv, x, y, w, h, s, size=14, fill=WHITE, stroke=NAVY, color=INK,
           tail="left", weight="bold"):
    cv.rect(x, y, w, h, fill=fill, stroke=stroke, sw=1.5, rx=8)
    if tail == "left":
        cv.poly([(x, y + h * 0.55), (x - 9, y + h * 0.72), (x, y + h * 0.86)],
                fill=fill, stroke=stroke, sw=1.5)
    cv.text(x + w / 2, y + h / 2 + size * 0.35, s, size=size, weight=weight,
            fill=color, anchor="middle")


def llm_box(cv, x, y, w, h, label="Large Language Model", size=15):
    cv.rect(x, y, w, h, fill=NAVY, stroke=NAVY, sw=1.5, rx=7)
    rows = label.split("\n")
    lh = size * 1.2
    top = y + h / 2 - (len(rows) - 1) * lh / 2 + size * 0.34
    for i, row in enumerate(rows):
        cv.text(x + w / 2, top + i * lh, row, size=size, weight="bold",
                fill=WHITE, anchor="middle")


def token_row(cv, x, y, n, cell=30, gap=6, labels=None, fills=None,
              strokes=None, size=13, lcolor=None, sub=None, sub_size=12,
              sub_color=None, rx=4):
    """A horizontal row of labelled token boxes; returns the row width."""
    for i in range(n):
        bx = x + i * (cell + gap)
        cv.rect(bx, y, cell, cell,
                fill=(fills[i] if fills else FILL_GREY),
                stroke=(strokes[i] if strokes else "#C3CFDC"), sw=1.3, rx=rx)
        if labels and labels[i] is not None:
            col = lcolor[i] if isinstance(lcolor, list) else (lcolor or INK)
            cv.text(bx + cell / 2, y + cell / 2 + size * 0.35, str(labels[i]),
                    size=size, weight="bold", fill=col, anchor="middle")
        if sub and sub[i] is not None:
            col = sub_color[i] if isinstance(sub_color, list) else (sub_color or GREY)
            cv.text(bx + cell / 2, y + cell + sub_size + 4, str(sub[i]),
                    size=sub_size, weight="bold", fill=col, anchor="middle")
    return n * (cell + gap) - gap


# ------------------------------------------------------------------ 1 · title

def fig_title_motif(cv: Canvas):
    """Title-slide decoration only: a dense token grid thinning into concepts.

    The navy background and all title text are native slide chrome, so this
    function deliberately draws no words.
    """
    cell, step = 15, 21
    for r in range(8):
        for c in range(26):
            dense = c <= 14
            if not dense and (r * 26 + c * 5) % 7 >= 2:
                continue
            cv.rect(742 + c * step, 24 + r * step, cell, cell, fill=WHITE,
                    stroke=None, rx=2, opacity=0.20 if dense else 0.55)
    cv.text(1264, 214, "tokens  \u2192  concepts", size=15, weight="bold",
            fill="#7FA8D2", anchor="end")


# ------------------------------------------------------- 2 · motivation

def fig_motivation(cv: Canvas):
    cards = [
        ("Embodied intelligence", "act in a physical scene"),
        ("Autonomous driving", "read a road in real time"),
        ("Everyday assistants", "answer about any screen"),
    ]
    cw, gap = 352, 48
    for i, (name, sub) in enumerate(cards):
        x = i * (cw + gap)
        cv.rect(x, 0, cw, 136, fill=FILL_GREY, stroke=BORDER, sw=1.4, rx=8)
        gx, gy = x + 26, 26
        if i == 0:  # robot
            cv.rect(gx + 16, gy + 6, 44, 34, fill=FILL_BLUE, stroke=NAVY, sw=1.6, rx=6)
            cv.circle(gx + 28, gy + 22, 4.5, fill=NAVY, stroke=None)
            cv.circle(gx + 48, gy + 22, 4.5, fill=NAVY, stroke=None)
            cv.line(gx + 38, gy, gx + 38, gy + 6, stroke=NAVY, sw=1.8)
            cv.circle(gx + 38, gy - 3, 3.5, fill=RED, stroke=None)
            cv.rect(gx + 22, gy + 46, 32, 30, fill=WHITE, stroke=NAVY, sw=1.6, rx=4)
            cv.line(gx + 22, gy + 54, gx + 8, gy + 66, stroke=NAVY, sw=1.8)
            cv.line(gx + 54, gy + 54, gx + 68, gy + 66, stroke=NAVY, sw=1.8)
        elif i == 1:  # car on a road
            cv.path(f"M {gx + 6} {gy + 52} L {gx + 70} {gy + 52}", stroke=GREY, sw=2)
            cv.path(f"M {gx + 10} {gy + 44} L {gx + 20} {gy + 26} L {gx + 54} {gy + 26} "
                    f"L {gx + 66} {gy + 44} Z", fill=FILL_BLUE, stroke=NAVY, sw=1.6)
            cv.rect(gx + 6, gy + 40, 64, 12, fill=WHITE, stroke=NAVY, sw=1.6, rx=4)
            cv.circle(gx + 20, gy + 54, 6, fill=WHITE, stroke=NAVY, sw=1.8)
            cv.circle(gx + 56, gy + 54, 6, fill=WHITE, stroke=NAVY, sw=1.8)
            cv.line(gx + 6, gy + 68, gx + 26, gy + 68, stroke=RED, sw=2.4)
            cv.line(gx + 38, gy + 68, gx + 58, gy + 68, stroke=RED, sw=2.4)
        else:  # screen with chat
            cv.rect(gx + 12, gy, 52, 76, fill=WHITE, stroke=NAVY, sw=1.6, rx=7)
            cv.rect(gx + 18, gy + 10, 26, 12, fill=FILL_BLUE, stroke=None, rx=3)
            cv.rect(gx + 32, gy + 28, 26, 12, fill=FILL_BLUE_D, stroke=None, rx=3)
            cv.rect(gx + 18, gy + 46, 30, 12, fill=FILL_BLUE, stroke=None, rx=3)
            cv.circle(gx + 38, gy + 68, 4, fill=NAVY, stroke=None)
        cv.text(x + 122, 56, name, size=20, weight="bold", fill=INK)
        cv.text(x + 122, 82, sub, size=15, fill=GREY)

    # The shared pipeline underneath.
    y = 214
    image_glyph(cv, 8, y, 96, 74)
    cv.text(56, y + 92, "Image", size=15, weight="bold", fill=INK, anchor="middle")
    bubble(cv, 140, y + 14, 214, 46,
           "\u201cWhat color is the collar?\u201d", size=15)
    cv.text(247, y + 92, "Instruction", size=15, weight="bold", fill=INK,
            anchor="middle")

    cv.arrow(374, y + 37, 424, y + 37, color="navy", sw=2.4)
    cv.rect(436, y - 8, 356, 106, fill=FILL_BLUE, stroke=NAVY, sw=1.8, rx=8)
    cv.text(614, y + 14, "Large vision-language model", size=17, weight="bold",
            fill=NAVY, anchor="middle")
    for i, name in enumerate(["Vision\nencoder", "Projector", "LLM"]):
        bx = 452 + i * 112
        cv.mbox(bx, y + 26, 100, 54, name.split("\n"), size=13, fill=WHITE,
                stroke=NAVY, sw=1.4, rx=6, color=NAVY)
        if i < 2:
            cv.arrow(bx + 100, y + 53, bx + 112, y + 53, color="navy", sw=2)

    cv.arrow(806, y + 37, 856, y + 37, color="navy", sw=2.4)
    bubble(cv, 868, y + 14, 150, 46, "\u201cBlack\u201d", size=17,
           fill=FILL_GREEN, stroke=GREEN, color=GREEN, tail=None)

    cv.rect(1042, y - 8, 110, 106, fill=FILL_RED, stroke=RED, sw=1.6, rx=8)
    cv.text(1097, y + 24, "576", size=34, weight="bold", fill=RED, anchor="middle")
    cv.text(1097, y + 50, "vision tokens", size=13, weight="bold", fill=RED,
            anchor="middle")
    cv.text(1097, y + 74, "for one image", size=12, fill=RED, anchor="middle")


# ------------------------------------------- 3 · token level vs concept level

def fig_token_vs_concept(cv: Canvas):
    bubble(cv, 396, 0, 380, 40, "Q:  What color is the dog's collar?", size=17,
           fill=FILL_GREY, stroke=GREY, tail=None)
    cv.line(576, 62, 576, 400, stroke="#D6DEE7", sw=1.6, dash="7 6")

    # A compact 16-patch region, standing for the collar the question asks about.
    kept = {r * 24 + c
            for r, cols in ((11, (9, 10, 11)), (12, (8, 9, 10, 11, 12)),
                            (13, (8, 9, 10, 11, 12)), (14, (9, 10, 11)))
            for c in cols}

    for side in (0, 1):
        x0 = 20 if side == 0 else 600
        head, hcol = ("w/o VCM", GREY) if side == 0 else ("w/ VCM", NAVY)
        cv.text(x0 + 86, 82, head, size=20, weight="bold", fill=hcol,
                anchor="middle")

        gx, gy, cell, gap, cols = x0, 96, 6.6, 0.9, 24
        if side == 0:
            cv.grid_tokens(gx, gy, cols, cols, cell, gap=gap,
                           off=FILL_BLUE, off_stroke="#B8CEE4")
        else:
            cv.grid_tokens(gx, gy, cols, cols, cell, gap=gap, keep=kept,
                           on=FILL_BLUE_D, on_stroke=NAVY,
                           off=WHITE, off_stroke="#E7ECF2")
        gsize = cols * (cell + gap) - gap
        cv.rect(gx - 4, gy - 4, gsize + 8, gsize + 8, fill=None,
                stroke="#9FB4C9", sw=1.4, rx=3)

        cnt, ccol, cfill = ("576", RED, FILL_RED) if side == 0 else ("16", NAVY, FILL_BLUE)
        cv.rect(gx + gsize / 2 - 82, gy + gsize + 14, 164, 36, fill=cfill,
                stroke=ccol, sw=1.5, rx=6)
        cv.text(gx + gsize / 2, gy + gsize + 38, f"{cnt} vision tokens",
                size=17, weight="bold", fill=ccol, anchor="middle")

        ax = gx + gsize + 22
        cv.arrow(ax, gy + gsize / 2, ax + 40, gy + gsize / 2, color="navy", sw=2.4)
        llm_box(cv, ax + 52, gy + gsize / 2 - 34, 104, 68, "Large\nLanguage\nModel", size=14)
        cv.arrow(ax + 168, gy + gsize / 2, ax + 206, gy + gsize / 2, color="navy", sw=2.4)
        bubble(cv, ax + 218, gy + gsize / 2 - 22, 124, 44, "A:  Black", size=17,
               fill=FILL_GREEN, stroke=GREEN, color=GREEN, tail=None)

    cv.text(576, 396, "identical answer  ·  the instruction only ever needed the collar",
            size=15, weight="bold", fill=GREY, anchor="middle")


# ------------------------------------------------------------------- 4 · cost

def fig_cost(cv: Canvas):
    # Sequence composition.
    y = 6
    cv.text(0, y + 14, "One LVLM forward pass, sequence length n", size=17,
            weight="bold", fill=NAVY)
    bx, bw, bh = 0, 700, 42
    by = y + 30
    img_w = bw * 20 / 21
    cv.rect(bx, by, img_w, bh, fill=FILL_BLUE_D, stroke=NAVY, sw=1.5, rx=4)
    cv.rect(bx + img_w, by, bw - img_w, bh, fill=FILL_GREY, stroke=GREY, sw=1.5, rx=4)
    cv.math(bx + img_w / 2, by + 27, "n_{img}", size=20, fill=NAVY, anchor="middle",
            weight="bold")
    cv.math(bx + bw + 14, by + 27, "n_{sys} + n_{ins} + n_{res}", size=17,
            fill=GREY, weight="bold")
    cv.brace(bx, by + bh + 6, bx + img_w, depth=9, stroke=RED, sw=1.6)
    cv.text(bx + img_w / 2, by + bh + 40,
            "vision tokens \u2248 20\u00d7 everything else", size=15,
            weight="bold", fill=RED, anchor="middle")

    # The cost model. The highlight box is placed from the measured width of the
    # formula prefix, so it always lands on the quadratic term.
    top = panel(cv, 0, 156, 556, 200, "Attention cost is quadratic in n")
    formula, fsize, fx = "FLOPs = T \u00b7 ( 4nd\u00b2 + 2n\u00b2d + 2ndm )", 25, 24
    cv.math(fx, top + 32, formula, size=fsize, fill=INK, italic=False)
    pre = cv.math_width("FLOPs = T \u00b7 ( 4nd\u00b2 + ", fsize, italic=False)
    term = cv.math_width("2n\u00b2d", fsize, italic=False)
    cv.rect(fx + pre - 5, top + 8, term + 8, 34, fill=None, stroke=RED, sw=2.2,
            rx=5)
    cv.text(fx + pre + term / 2, top + 62, "grows with n\u00b2", size=14,
            weight="bold", fill=RED, anchor="middle")
    cv.text(24, top + 92,
            "Cutting the vision tokens is the only lever that", size=15, fill=INK)
    cv.text(24, top + 112,
            "touches the dominant term of the sequence.", size=15, fill=INK)
    cv.rect(24, top + 124, 508, 30, fill=FILL_GREEN, stroke=GREEN, sw=1.5, rx=6)
    cv.text(278, top + 144,
            "n scaled by 1/8  \u2192  R \u2248 3/25  \u2192  85% fewer FLOPs",
            size=15, weight="bold", fill=GREEN, anchor="middle")

    # And it only gets worse with resolution / video.
    top = panel(cv, 596, 156, 556, 200, "\u2026 and the input keeps growing")
    bar_chart(cv, 636, top + 8, 470, 100, [
        {"label": "LLaVA-1.5", "value": 576, "sub": "336\u00d7336",
         "color": FILL_BLUE, "edge": NAVY},
        {"label": "Video-LLaVA", "value": 2048, "sub": "8 frames",
         "color": FILL_BLUE_D, "edge": NAVY},
        {"label": "LLaVA-NeXT", "value": 2880, "sub": "high-res tiles",
         "color": FILL_AMBER, "edge": AMBER, "vcolor": AMBER},
    ], vmin=0, vmax=3200, value_fmt="{:.0f}", label_size=15, value_size=17)
    note(cv, 636, top + 154, "vision tokens fed to the LLM backbone", size=12.5)


# --------------------------------------------------------------- 5 · prior art

def fig_prior_art(cv: Canvas):
    for side in (0, 1):
        x0 = 0 if side == 0 else 596
        title = ("(a)  Prune  \u2014  threshold the attention matrix"
                 if side == 0 else
                 "(b)  Merge  \u2014  fixed-length trainable queries")
        top = panel(cv, x0, 0, 556, 306, title)

        if side == 0:
            # An attention matrix, thresholded into a keep/drop mask.
            cv.text(x0 + 24, top + 16, "attention matrix", size=13,
                    weight="bold", fill=GREY)
            vals = [0.9, 0.15, 0.7, 0.1, 0.2, 0.85, 0.12, 0.6]
            for r in range(8):
                for c in range(8):
                    v = (vals[(r + c) % 8] * 0.6 + vals[c] * 0.4)
                    cv.rect(x0 + 24 + c * 17, top + 26 + r * 17, 15, 15,
                            fill=NAVY, stroke=None, rx=1.5, opacity=round(v, 2))
            cv.arrow(x0 + 176, top + 94, x0 + 218, top + 94, color="red", sw=2.4)
            cv.text(x0 + 197, top + 84, "top-k", size=13, weight="bold",
                    fill=RED, anchor="middle")
            token_row(cv, x0 + 234, top + 78, 8, cell=26, gap=6,
                      fills=[FILL_BLUE_D if v > 0.5 else WHITE for v in vals],
                      strokes=[NAVY if v > 0.5 else "#DCE3EA" for v in vals])
            cv.text(x0 + 234, top + 138, "kept tokens keep their index,",
                    size=14, fill=INK)
            cv.text(x0 + 234, top + 158, "but carry no concept boundary",
                    size=14, fill=INK)
            lims = ["no semantic concept, only surviving patches",
                    "the number kept is set by a fixed ratio"]
        else:
            token_row(cv, x0 + 24, top + 10, 8, cell=26, gap=6,
                      fills=[FILL_GREY] * 8, strokes=["#C3CFDC"] * 8)
            cv.text(x0 + 24, top + 62, "vision tokens", size=13, weight="bold",
                    fill=GREY)
            cv.mbox(x0 + 24, top + 78, 232, 46, "cross-attention", size=15,
                    fill=FILL_BLUE, stroke=NAVY, rx=6, color=NAVY)
            for i in range(4):
                cv.rect(x0 + 46 + i * 52, top + 138, 34, 26, fill=FILL_AMBER,
                        stroke=AMBER, sw=1.4, rx=4)
                cv.text(x0 + 63 + i * 52, top + 156, "q", size=14, weight="bold",
                        fill=AMBER, anchor="middle")
            cv.text(x0 + 24, top + 186, "fixed-length learnable queries",
                    size=13, weight="bold", fill=AMBER)
            cv.arrow(x0 + 268, top + 100, x0 + 306, top + 100, color="navy", sw=2.4)
            token_row(cv, x0 + 320, top + 86, 4, cell=30, gap=8,
                      fills=[FILL_BLUE_D] * 4, strokes=[NAVY] * 4)
            cv.text(x0 + 320, top + 146, "always the same length,", size=14, fill=INK)
            cv.text(x0 + 320, top + 166, "original order discarded", size=14, fill=INK)
            lims = ["relative order and position are lost",
                    "length cannot follow the instruction"]

        for i, s in enumerate(lims):
            cv.circle(x0 + 30, top + 214 + i * 26, 4, fill=RED, stroke=None)
            cv.text(x0 + 42, top + 219 + i * 26, s, size=14.5, weight="bold",
                    fill=RED)

    cv.rect(0, 330, 1152, 52, fill=FILL_GREY, stroke=GREY, sw=1.5, rx=8)
    cv.text(576, 362,
            "Both operate on tokens. Neither returns a concept that a downstream "
            "task can point at in the image.",
            size=18, weight="bold", fill=INK, anchor="middle")


# ----------------------------------------------------------------- 6 · missing

def fig_missing(cv: Canvas):
    cards = [
        ("No spatial grounding",
         ["compressed vectors do not say", "where in the image they came from"]),
        ("Order and position lost",
         ["merged queries drop the relative", "layout the answer may depend on"]),
        ("Length not controllable",
         ["a fixed ratio cannot follow what", "the instruction actually asks for"]),
    ]
    cw, gap = 352, 48
    for i, (name, body) in enumerate(cards):
        x = i * (cw + gap)
        cv.rect(x, 0, cw, 236, fill=WHITE, stroke=RED, sw=1.8, rx=8)
        cv.rect(x, 0, cw, 46, fill=FILL_RED, stroke=None, rx=8)
        cv.rect(x, 36, cw, 10, fill=FILL_RED, stroke=None)
        cv.text(x + cw / 2, 30, name, size=19, weight="bold", fill=RED,
                anchor="middle")

        gy = 66
        if i == 0:
            image_glyph(cv, x + 30, gy, 118, 90)
            cv.text(x + 89, gy + 106, "image", size=13, weight="bold",
                    fill=GREY, anchor="middle")
            cv.arrow(x + 158, gy + 45, x + 196, gy + 45, color="grey", sw=2.2)
            for k in range(3):
                cv.rect(x + 208, gy + 8 + k * 30, 96, 22, fill=FILL_GREY,
                        stroke="#C3CFDC", sw=1.3, rx=4)
                cv.text(x + 256, gy + 24 + k * 30, "vector", size=12,
                        fill=GREY, anchor="middle")
            cv.text(x + 256, gy + 106, "?  where", size=15, weight="bold",
                    fill=RED, anchor="middle")
        elif i == 1:
            for k, lab in enumerate("1234"):
                cv.rect(x + 34 + k * 40, gy + 6, 32, 32, fill=FILL_BLUE,
                        stroke=NAVY, sw=1.3, rx=4)
                cv.text(x + 50 + k * 40, gy + 28, lab, size=15, weight="bold",
                        fill=NAVY, anchor="middle")
            cv.arrow(x + 208, gy + 22, x + 246, gy + 22, color="grey", sw=2.2)
            for k, lab in enumerate("3142"):
                cv.rect(x + 258 + k * 22, gy + 6, 18, 32, fill=FILL_GREY,
                        stroke="#C3CFDC", sw=1.3, rx=3)
            cv.text(x + 176, gy + 76, "order no longer recoverable", size=14.5,
                    weight="bold", fill=RED, anchor="middle")
            cv.text(x + 176, gy + 100, "\u2192 region-level tasks break", size=14,
                    fill=INK, anchor="middle")
        else:
            cv.path(f"M {x + 92} {gy + 74} A 62 62 0 1 1 {x + 260} {gy + 74}",
                    stroke="#C3CFDC", sw=9, cap="round")
            cv.path(f"M {x + 92} {gy + 74} A 62 62 0 0 1 {x + 132} {gy + 18}",
                    stroke=RED, sw=9, cap="round")
            cv.circle(x + 176, gy + 74, 8, fill=NAVY, stroke=None)
            cv.line(x + 176, gy + 74, x + 132, gy + 30, stroke=NAVY, sw=3)
            cv.text(x + 176, gy + 104, "fixed ratio", size=15, weight="bold",
                    fill=RED, anchor="middle")

        for j, row in enumerate(body):
            cv.text(x + cw / 2, 198 + j * 21, row, size=14, fill=INK,
                    anchor="middle")

    cv.rect(0, 264, 1152, 62, fill=NAVY, stroke=None, rx=8)
    cv.text(576, 292, "Consequence:  applicable to visual question answering, and "
            "little else.", size=20, weight="bold", fill=WHITE, anchor="middle")
    cv.text(576, 316, "Detection, segmentation and region-level tasks all need "
            "concepts that stay attached to the image.",
            size=15, fill="#BBD3EA", anchor="middle")


# -------------------------------------------------------------- 7 · definition

def fig_definition(cv: Canvas):
    image_glyph(cv, 0, 78, 108, 82)
    cv.text(54, 176, "image", size=14, weight="bold", fill=INK, anchor="middle")
    bubble(cv, 0, 206, 176, 44, "instruction", size=15, tail=None)

    cv.arrow(120, 118, 176, 132, color="navy", sw=2.4)
    cv.arrow(186, 224, 236, 176, color="navy", sw=2.4)

    cv.rect(196, 84, 232, 122, fill=NAVY, stroke=NAVY, sw=1.6, rx=8)
    cv.text(312, 128, "Vision", size=25, weight="bold", fill=WHITE, anchor="middle")
    cv.text(312, 158, "concept model", size=25, weight="bold", fill=WHITE,
            anchor="middle")
    cv.text(312, 188, "(this paper)", size=14, fill="#A9C6E2", anchor="middle")

    outs = [
        ("How many", "a target length L, derived from the instruction"),
        ("Which", "only the concepts the instruction asks about"),
        ("Where", "the original spatial positions are preserved"),
    ]
    for i, (head, body) in enumerate(outs):
        y = 22 + i * 96
        cv.arrow(440, 145, 486, y + 34, color="navy", sw=2.2,
                 curve=(-10, (y + 34 - 145) * 0.12))
        cv.rect(496, y, 500, 78, fill=FILL_BLUE, stroke=NAVY, sw=1.6, rx=8)
        cv.text(516, y + 32, head, size=21, weight="bold", fill=NAVY)
        cv.text(516, y + 60, body, size=15, fill=INK)

    cv.rect(1016, 22, 136, 248, fill=FILL_GREEN, stroke=GREEN, sw=1.6, rx=8)
    cv.text(1084, 62, "output", size=15, weight="bold", fill=GREEN, anchor="middle")
    cv.grid_tokens(1036, 78, 6, 6, 14, gap=2.2,
                   keep={7, 8, 13, 20, 26, 27, 33}, on=FILL_BLUE_D,
                   on_stroke=NAVY, off=WHITE, off_stroke="#DDE6EE")
    cv.text(1084, 214, "sparse,", size=14, weight="bold", fill=GREEN, anchor="middle")
    cv.text(1084, 236, "still located", size=14, weight="bold", fill=GREEN,
            anchor="middle")

    cv.rect(0, 300, 996, 62, fill=FILL_GREY, stroke=GREY, sw=1.5, rx=8)
    cv.math(24, 340, "H^{V}_{C}", size=26, fill=NAVY, weight="bold")
    cv.text(94, 336, "is a sparse subset of", size=17, fill=INK)
    cv.math(268, 340, "H^{V}", size=26, fill=NAVY, weight="bold")
    cv.text(330, 336,
            "\u2014  far fewer entries, and every one keeps its coordinates",
            size=17, weight="bold", fill=INK)


# -------------------------------------------------------------- 8 · challenges

def fig_challenges(cv: Canvas):
    # Challenge 1 — annotation.
    top = panel(cv, 0, 0, 556, 336, "Challenge 1 \u00b7 no concept-level labels",
                tcolor=RED, tsize=20)
    cv.rect(24, top + 8, 214, 128, fill=FILL_BLUE, stroke=NAVY, sw=1.5, rx=6)
    cv.text(131, top + 34, "abundant", size=17, weight="bold", fill=NAVY,
            anchor="middle")
    cv.text(131, top + 56, "VQA instruction data", size=15, fill=INK, anchor="middle")
    cv.grid_tokens(44, top + 70, 12, 4, 13, gap=2.4, off=WHITE,
                   off_stroke="#9EC0E0")
    cv.text(131, top + 154, "no concept annotation", size=14, weight="bold",
            fill=GREY, anchor="middle")

    cv.rect(300, top + 8, 214, 128, fill=FILL_RED, stroke=RED, sw=1.5, rx=6)
    cv.text(407, top + 34, "concept-level labels", size=17, weight="bold",
            fill=RED, anchor="middle")
    cv.text(407, top + 56, "would be exact \u2014 but", size=15, fill=INK,
            anchor="middle")
    for i, s in enumerate(["labor-intensive", "time-consuming", "does not scale"]):
        cv.text(407, top + 82 + i * 20, s, size=14, weight="bold", fill=RED,
                anchor="middle")
    cv.text(407, top + 154, "so nobody has them", size=14, weight="bold",
            fill=GREY, anchor="middle")

    cv.rect(24, top + 182, 490, 52, fill=WHITE, stroke=NAVY, sw=1.8, rx=6)
    cv.text(269, top + 213,
            "Needed: a signal already inside the data.", size=18,
            weight="bold", fill=NAVY, anchor="middle")

    # Challenge 2 — variable length.
    top = panel(cv, 596, 0, 556, 336, "Challenge 2 \u00b7 the length is not fixed",
                tcolor=RED, tsize=20)
    examples = [
        ("\u201cWhere is the person in yellow?\u201d", 3),
        ("\u201cWhat is the orange number of the bus?\u201d", 5),
        ("\u201cCan you describe this image in detail?\u201d", 10),
    ]
    for i, (q, k) in enumerate(examples):
        y = top + 8 + i * 52
        cv.text(620, y + 18, q, size=14.5, fill=INK)
        for j in range(12):
            cv.rect(950 + j * 15, y + 4, 12, 18,
                    fill=FILL_BLUE_D if j < k else WHITE,
                    stroke=NAVY if j < k else "#DDE6EE", sw=1.1, rx=2)
        cv.text(1136, y + 18, str(k), size=14, weight="bold", fill=NAVY,
                anchor="middle")
    cv.text(1042, top + 178, "concepts actually needed", size=13, weight="bold",
            fill=GREY, anchor="middle")

    cv.rect(620, top + 196, 508, 56, fill=FILL_RED, stroke=RED, sw=1.6, rx=6)
    cv.math(644, top + 232,
            "searching every cut point:   O(2^{M})",
            size=22, fill=RED, weight="bold")
    cv.text(1000, top + 230, "M = 576", size=16, weight="bold", fill=RED)


# ------------------------------------------------------------- 9 · observation

def fig_observation(cv: Canvas):
    steps = [
        ["5K instances", "LLaVA instruction data"],
        ["GPT-4o", "mark image-related keywords"],
        ["VisionZip", "24 different token lengths"],
        ["GPT-4o judge", "minimum sufficient length"],
    ]
    sw_, gap = 268, 20
    for i, rows in enumerate(steps):
        x = i * (sw_ + gap)
        chevron(cv, x, 0, sw_, 62, rows[:1], fill=FILL_BLUE, size=17)
        cv.text(x + sw_ / 2 + 8, 84, rows[1], size=13.5, fill=GREY, anchor="middle")

    panels = [
        ("(a)  keywords in the response",
         "more keywords \u2192 longer minimum", 1, NAVY),
        ("(b)  keywords in the instruction",
         "more keywords \u2192 shorter minimum", -1, NAVY),
        ("(c)  response \u2212 instruction gap",
         "the most stable of the three", -1, RED),
    ]
    pw = 368
    for i, (head, sub, slope, col) in enumerate(panels):
        x = i * (pw + 24)
        top = panel(cv, x, 108, pw, 248, head, tcolor=col, tsize=15.5)
        note(cv, x + 16, top + 2,
             "schematic \u2014 direction as reported in Fig. 2", size=11)
        ax, ay, aw, ah = x + 66, top + 14, pw - 106, 118
        cv.line(ax, ay, ax, ay + ah, stroke=GREY, sw=1.5)
        cv.line(ax, ay + ah, ax + aw, ay + ah, stroke=GREY, sw=1.5)
        y1, y2 = (ay + ah - 14, ay + 14) if slope > 0 else (ay + 14, ay + ah - 14)
        cv.line(ax + 10, y1, ax + aw - 12, y2, stroke=col, sw=3)
        for k in range(9):
            t = k / 8
            jitter = (-1) ** k * (6 - 2 * (k % 3))
            cv.circle(ax + 14 + t * (aw - 30), y1 + (y2 - y1) * t + jitter, 3.4,
                      fill=col, stroke=None, opacity=0.5)
        for j, lab in enumerate(("min", "vision", "length")):
            cv.text(ax - 8, ay + ah / 2 - 12 + j * 16, lab, size=12,
                    weight="bold", fill=GREY, anchor="end")
        cv.text(ax + aw / 2, ay + ah + 20, "# keywords", size=12.5,
                weight="bold", fill=GREY, anchor="middle")
        sign = "positive correlation" if slope > 0 else "negative correlation"
        cv.text(x + pw / 2, top + 170, sign, size=16, weight="bold", fill=col,
                anchor="middle")
        cv.text(x + pw / 2, top + 192, sub, size=13.5, fill=INK, anchor="middle")


# ---------------------------------------------------------------- 10 · overview

def fig_overview(cv: Canvas):
    # Instruction branch.
    bubble(cv, 0, 12, 246, 42, "\u201cWhere is the person in yellow?\u201d",
           size=14, fill=FILL_GREY, stroke=GREY, tail=None)
    cv.arrow(123, 54, 123, 84, color="navy", sw=2.2)
    cv.mbox(0, 84, 246, 52, "Keyword selector", size=16, fill=FILL_AMBER,
            stroke=AMBER, color=AMBER)
    cv.text(123, 156, "text prior", size=15, weight="bold", fill=AMBER,
            anchor="middle")
    cv.arrow(123, 166, 123, 196, color="navy", sw=2.2)

    # Vision branch.
    image_glyph(cv, 24, 220, 88, 68)
    cv.text(68, 306, "image", size=14, weight="bold", fill=INK, anchor="middle")
    cv.arrow(120, 254, 158, 254, color="navy", sw=2.2)

    cv.mbox(0, 196, 246, 40, "Vision encoder  f_V", size=15, fill=FILL_BLUE,
            stroke=NAVY, color=NAVY)

    stages = [
        (280, "Projector", ["cross-attention", "+ text prior"], FILL_BLUE, NAVY),
        (528, "VCM", ["target length +", "forward\u2013backward"], FILL_AMBER, AMBER),
    ]
    for x, head, body, fill, col in stages:
        cv.rect(x, 84, 210, 204, fill=fill, stroke=col, sw=1.8, rx=8)
        cv.text(x + 105, 118, head, size=22, weight="bold", fill=col,
                anchor="middle")
        for j, row in enumerate(body):
            cv.text(x + 105, 148 + j * 22, row, size=14, fill=INK, anchor="middle")

    cv.grid_tokens(316, 194, 9, 5, 15, gap=2.4, off=WHITE, off_stroke="#9EC0E0")
    cv.grid_tokens(564, 194, 9, 5, 15, gap=2.4,
                   keep={11, 12, 20, 29, 30, 38}, on=FILL_BLUE_D, on_stroke=NAVY,
                   off=WHITE, off_stroke="#EAEFF4")
    cv.text(385, 282, "vision tokens", size=13, weight="bold", fill=NAVY,
            anchor="middle")
    cv.text(633, 282, "vision concepts", size=13, weight="bold", fill=AMBER,
            anchor="middle")

    cv.arrow(250, 186, 276, 186, color="navy", sw=2.4)
    cv.arrow(494, 186, 522, 186, color="navy", sw=2.4)
    cv.arrow(742, 186, 786, 186, color="navy", sw=2.4)

    llm_box(cv, 798, 130, 200, 112, "Large\nLanguage\nModel", size=17)
    cv.arrow(1002, 186, 1040, 186, color="navy", sw=2.4)
    bubble(cv, 1050, 162, 102, 48, "answer", size=15, fill=FILL_GREEN,
           stroke=GREEN, color=GREEN, tail=None)

    # Two-stage training schedule.
    cv.rect(0, 320, 566, 62, fill=WHITE, stroke=NAVY, sw=1.6, rx=8)
    cv.text(16, 342, "Stage I \u00b7 pre-training", size=15, weight="bold", fill=NAVY)
    cv.math(16, 370, "L_{NTP} + \u03b1 \u00b7 L_{SA}", size=19, fill=INK)
    cv.text(210, 368, "\u03b1 = 0.05  \u00b7  learns the keyword selector",
            size=13.5, fill=GREY)
    cv.rect(586, 320, 566, 62, fill=WHITE, stroke=AMBER, sw=1.6, rx=8)
    cv.text(602, 342, "Stage II \u00b7 instruction fine-tuning", size=15,
            weight="bold", fill=AMBER)
    cv.math(602, 370, "L_{NTP} + \u03b5(r) \u00b7 L_{VCM}", size=19, fill=INK)
    cv.text(818, 368, "selector frozen  \u00b7  learns the concepts",
            size=13.5, fill=GREY)


# ----------------------------------------------------------------- 11 · keyword

def fig_keyword(cv: Canvas):
    words = ["Where", "is", "the", "person", "in", "yellow", "?"]
    scores = [0.03, 0.01, 0.03, 0.51, 0.02, 0.39, 0.01]
    mean = sum(scores) / len(scores)
    keep = [s > mean for s in scores]

    # Left: the image gives the global vision token.
    image_glyph(cv, 0, 30, 104, 80)
    cv.arrow(112, 70, 148, 70, color="navy", sw=2.2)
    cv.mbox(156, 44, 150, 52, ["vision encoder", "+ avg pooling"], size=13,
            fill=FILL_BLUE, stroke=NAVY, color=NAVY, lh=17)
    cv.arrow(314, 70, 350, 70, color="navy", sw=2.2)
    cv.rect(358, 46, 104, 48, fill=NAVY, stroke=NAVY, sw=1.5, rx=6)
    cv.math(410, 78, "G^{V}", size=24, fill=WHITE, anchor="middle", weight="bold")
    cv.text(410, 116, "global vision token", size=13, weight="bold", fill=NAVY,
            anchor="middle")

    # Right: instruction + response through the selector.
    cv.text(516, 24, "instruction  +  response tokens", size=14, weight="bold",
            fill=GREY)
    cell, gap, x0 = 78, 8, 516
    for i, wd in enumerate(words):
        bx = x0 + i * (cell + gap)
        cv.rect(bx, 34, cell, 34, fill=FILL_GREY, stroke="#C3CFDC", sw=1.3, rx=4)
        cv.text(bx + cell / 2, 57, wd, size=14, weight="bold", fill=INK,
                anchor="middle")
    cv.arrow(x0 + 3 * (cell + gap) + cell / 2, 76,
             x0 + 3 * (cell + gap) + cell / 2, 100, color="navy", sw=2.2)
    cv.mbox(x0, 100, 7 * (cell + gap) - gap, 40,
            "multi-head self-attention, scored against the global vision token", size=15,
            fill=FILL_AMBER, stroke=AMBER, color=AMBER)

    # Scores and the mean threshold.
    for i, (wd, sc) in enumerate(zip(words, scores)):
        bx = x0 + i * (cell + gap)
        lit = keep[i]
        cv.rect(bx, 156, cell, 40, fill=FILL_RED if lit else WHITE,
                stroke=RED if lit else "#DDE6EE", sw=1.8 if lit else 1.2, rx=4)
        cv.text(bx + cell / 2, 182, f"{sc:.2f}", size=16, weight="bold",
                fill=RED if lit else GREY, anchor="middle")
        cv.text(bx + cell / 2, 218, wd, size=14, weight="bold",
                fill=RED if lit else MUTED, anchor="middle")
    cv.line(x0 - 10, 232, x0 + 7 * (cell + gap) - gap + 10, 232, stroke=NAVY,
            sw=1.6, dash="6 4")
    cv.text(x0 - 16, 236, f"E(K) = {mean:.2f}", size=14, weight="bold",
            fill=NAVY, anchor="end")
    cv.text(x0 + (7 * (cell + gap) - gap) / 2, 258,
            "keep every token scoring above the mean", size=15, weight="bold",
            fill=RED, anchor="middle")

    # The two objectives.
    cv.rect(0, 152, 462, 106, fill=WHITE, stroke=NAVY, sw=1.6, rx=8)
    cv.text(20, 178, "Semantic alignment loss", size=16, weight="bold", fill=NAVY)
    cv.math(20, 212,
            "L_{SA} = \u2212 p(G^{T}_{LLM}) log p(G^{V}) \u2212 p(G^{T}_{LLM}) log p(G^{T})",
            size=15, fill=INK)
    cv.text(20, 240, "pulls text, vision and LLM features into one space",
            size=13.5, fill=GREY)

    cv.rect(0, 286, 1152, 62, fill=FILL_GREY, stroke=GREY, sw=1.5, rx=8)
    cv.math(24, 326,
            "K = Softmax( MHSA([H^{I}; H^{R}]) \u00b7 G^{V} ),      keep k > E(K)",
            size=23, fill=INK)
    cv.text(700, 322,
            "\u2192  \u201cperson\u201d and \u201cyellow\u201d survive; the rest is "
            "function words", size=16, weight="bold", fill=RED)


# ----------------------------------------------------------------- 12 · masking

def fig_masking(cv: Canvas):
    variants = [
        ("Where is the person in yellow ?", ["person", "yellow"], 6),
        ("Where is the person in <mask> ?", ["person"], 11),
        ("Where is the <mask> in yellow ?", ["yellow"], 11),
        ("Where is the <mask> in <mask> ?", [], 25),
    ]
    keeps = [
        {8, 9, 14, 15, 20, 21},
        {2, 3, 8, 9, 10, 14, 15, 16, 20, 21, 27},
        {7, 8, 9, 13, 14, 15, 19, 20, 21, 26, 27},
        {1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
         21, 22, 23, 25, 26, 27},
    ]
    pw, gap = 264, 32
    for i, (text_, kws, _n) in enumerate(variants):
        x = i * (pw + gap)
        cv.rect(x, 0, pw, 244, fill=WHITE, stroke=BORDER, sw=1.4, rx=8)
        cv.text(x + pw / 2, 26, f"mask {i} keyword{'' if i == 1 else 's'}",
                size=14, weight="bold", fill=GREY, anchor="middle")
        parts = text_.split()
        tx = x + 14
        for wd in parts:
            is_kw = wd in kws
            is_mask = wd == "<mask>"
            col = RED if is_kw else (MUTED if is_mask else INK)
            cv.text(tx, 54, wd, size=13.5, weight="bold" if is_kw or is_mask else None,
                    fill=col)
            tx += len(wd) * 6.6 + 5
        cv.grid_tokens(x + 58, 74, 6, 5, 22, gap=3, keep=keeps[i],
                       on=FILL_BLUE_D, on_stroke=NAVY, off=WHITE,
                       off_stroke="#E7ECF2")
        cv.rect(x + 44, 200, pw - 88, 30, fill=FILL_BLUE, stroke=NAVY, sw=1.4, rx=6)
        cv.text(x + pw / 2, 221, f"{len(keeps[i])} concepts kept", size=14,
                weight="bold", fill=NAVY, anchor="middle")

    cv.arrow(20, 266, 1132, 266, color="red", sw=2.6)
    cv.text(576, 258, "more masking  \u2192  more vision information required",
            size=17, weight="bold", fill=RED, anchor="middle")

    # The coefficient schedule.
    top = panel(cv, 0, 288, 556, 94, None)
    cv.text(20, top + 12, "Why this is safe", size=16, weight="bold", fill=NAVY)
    cv.text(20, top + 38,
            "Masking never shortens the requirement, so the objective cannot",
            size=14, fill=INK)
    cv.text(20, top + 58,
            "learn to discard information the answer depends on.", size=14, fill=INK)

    top = panel(cv, 596, 288, 556, 94, None)
    cv.math(616, top + 24, "r ~ Uniform(0, 1)", size=17, fill=INK)
    cv.math(616, top + 56,
            "\u03b5(r) = a + (b\u2212a) \u00b7 [1 + tanh(k(2r\u22121))] / 2", size=17,
            fill=INK)
    cv.text(940, top + 20, "a = 0.2,  b = 1.2,  k = 5", size=14, weight="bold",
            fill=NAVY)
    # A small tanh schedule sketch.
    ax, ay, aw, ah = 940, top + 32, 190, 42
    cv.line(ax, ay + ah, ax + aw, ay + ah, stroke=GREY, sw=1.2)
    pts = []
    for k in range(25):
        t = k / 24
        import math
        s = (1 + math.tanh(5 * (2 * t - 1))) / 2
        pts.append((ax + t * aw, ay + ah - s * ah))
    cv.path("M " + " L ".join(f"{p[0]:.1f} {p[1]:.1f}" for p in pts),
            stroke=AMBER, sw=2.4)
    cv.text(ax + aw + 6, ay + ah, "r", size=13, weight="bold", fill=GREY)


# ------------------------------------------------------------------ 13 · length

def fig_length(cv: Canvas):
    cv.rect(0, 0, 1152, 96, fill=FILL_GREY, stroke=GREY, sw=1.5, rx=8)
    cv.math(40, 62,
            "L = floor( M \u00b7 S \u00b7 [ 1 \u2212 Norm(N_{key}) ] )",
            size=38, fill=INK)
    marks = [
        (86, "M", "input vision tokens", NAVY),
        (206, "S", "information domain", AMBER),
        (400, "N_key", "keyword gap", RED),
    ]
    for x, sym, desc, col in marks:
        cv.line(x, 74, x, 92, stroke=col, sw=1.6)
        cv.text(x, 112, sym, size=15, weight="bold", fill=col, anchor="middle")
        cv.text(x, 132, desc, size=13, fill=GREY, anchor="middle")

    # The scalar S and its resulting budget.
    top = panel(cv, 0, 152, 470, 230, "The information domain sets the budget")
    table(cv, 24, top + 6, [("S", 110), ("max tokens", 150), ("Avg. (%)", 140)],
          [["1/2", "288", "58.9"], ["1/4", "144", "59.3"],
           ["1/6", "72", "56.4"], ["1/8", "36", "57.2"]],
          highlight={1}, row_h=30, head_h=30)
    note(cv, 24, top + 190, "Avg. over 4 VQA benchmarks (Table 4).")

    # The instruction-conditioned length curve.
    top = panel(cv, 500, 152, 652, 230,
                "The keyword gap moves the target length")
    ax, ay, aw, ah = 566, top + 16, 470, 132
    cv.line(ax, ay, ax, ay + ah, stroke=GREY, sw=1.5)
    cv.line(ax, ay + ah, ax + aw, ay + ah, stroke=GREY, sw=1.5)
    # L(N_key) is exactly the formula above, at M = 576 and S = 1/4.
    import math as _m
    pts = []
    for k in range(46):
        nk = -35 + k
        L = _m.floor(576 * 0.25 * (1 - (nk + 35) / 45))
        pts.append((ax + (nk + 35) / 45 * aw, ay + ah - L / 144 * ah))
    cv.path("M " + " L ".join(f"{p[0]:.1f} {p[1]:.1f}" for p in pts),
            stroke=NAVY, sw=3)
    for nk, lab in ((-35, "144"), (-13, "70"), (10, "0")):
        L = _m.floor(576 * 0.25 * (1 - (nk + 35) / 45))
        px, py = ax + (nk + 35) / 45 * aw, ay + ah - L / 144 * ah
        cv.circle(px, py, 4.6, fill=WHITE, stroke=NAVY, sw=2)
        cv.text(px, py - 12, lab, size=13, weight="bold", fill=NAVY, anchor="middle")
    cv.text(ax - 10, ay + 6, "L", size=15, weight="bold", fill=NAVY, anchor="end")
    cv.text(ax - 10, ay + ah, "0", size=13, fill=GREY, anchor="end")
    cv.text(ax, ay + ah + 20, "\u221235", size=13, fill=GREY, anchor="middle")
    cv.text(ax + aw, ay + ah + 20, "+10", size=13, fill=GREY, anchor="middle")
    cv.text(ax + aw / 2, ay + ah + 20,
            "keyword gap N_key  (instruction \u2212 response)", size=13.5,
            weight="bold", fill=GREY, anchor="middle")
    note(cv, 566, top + 194,
         "Exact evaluation of the formula at M = 576, S = 1/4; "
         "N_key is clipped to [\u221235, +10].")


# ---------------------------------------------------------------------- 14 · dp

def fig_dp(cv: Canvas):
    ex = DATA["dp_example"]
    p_star = ex["p_star"]
    rows = [SYM_BLANK, SYM_KEEP, SYM_BLANK, SYM_KEEP, SYM_BLANK]
    # The argmax path implied by Table 6: keep t where p(star) > p(blank).
    keep = [p > 0.5 for p in p_star]
    path, level = [], 0
    for t, k in enumerate(keep):
        if k and level % 2 == 0:
            level += 1
        elif not k and level % 2 == 1:
            level += 1
        path.append(level)

    x0, y0, dx, dy = 176, 16, 86, 58
    cv.text(x0 - 132, y0 - 2, "extended target", size=14, weight="bold", fill=GREY)
    for l, sym in enumerate(rows):
        cv.text(x0 - 34, y0 + l * dy + 7, sym, size=24, weight="bold",
                fill=NAVY if sym == SYM_KEEP else GREY, anchor="middle")
        cv.line(x0 - 14, y0 + l * dy, x0 + 7 * dx + 24, y0 + l * dy,
                stroke="#EDF1F6", sw=1.2)

    # Feasible / infeasible transitions.
    for t in range(7):
        for l in range(5):
            for nl in (l, l + 1):
                if nl > 4:
                    continue
                on = (path[t] == l and path[t + 1] == nl)
                near = abs(nl - path[t + 1]) <= 1 and abs(l - path[t]) <= 1
                col, sw_, op = ("#E9B75E", 1.2, 0.55)
                if near:
                    col, sw_, op = (FILL_BLUE_D, 2.0, 0.95)
                if on:
                    continue
                cv.line(x0 + t * dx, y0 + l * dy, x0 + (t + 1) * dx,
                        y0 + nl * dy, stroke=col, sw=sw_, opacity=op)
    for t in range(7):
        cv.line(x0 + t * dx, y0 + path[t] * dy, x0 + (t + 1) * dx,
                y0 + path[t + 1] * dy, stroke=RED, sw=3.6)

    for t in range(8):
        for l in range(5):
            hit = path[t] == l
            cv.circle(x0 + t * dx, y0 + l * dy, 9 if hit else 6,
                      fill=RED if hit else WHITE, stroke=RED if hit else "#B9C8D8",
                      sw=2 if hit else 1.4)
        cv.text(x0 + t * dx, y0 + 4 * dy + 32, f"t{t + 1}", size=14,
                weight="bold", fill=INK, anchor="middle")
        cv.text(x0 + t * dx, y0 + 4 * dy + 54, f"{p_star[t]:.1f}", size=13,
                weight="bold", fill=RED if keep[t] else MUTED, anchor="middle")
    cv.text(x0 - 34, y0 + 4 * dy + 54, f"p({SYM_KEEP})", size=13, weight="bold",
            fill=GREY, anchor="middle")

    legend = [("possible path", FILL_BLUE_D), ("most probable path", RED),
              ("impossible path", "#E9B75E")]
    cv.text(x0 + 7 * dx + 66, y0 - 6,
            f"{SYM_KEEP} = kept concept    {SYM_BLANK} = blank", size=13,
            weight="bold", fill=GREY)
    for i, (name, col) in enumerate(legend):
        lx = x0 + 7 * dx + 66
        cv.line(lx, y0 + 14 + i * 26, lx + 30, y0 + 14 + i * 26, stroke=col, sw=3.4)
        cv.text(lx + 40, y0 + 19 + i * 26, name, size=14, weight="bold", fill=col)

    cv.rect(x0 + 7 * dx + 60, y0 + 104, 260, 96, fill=FILL_GREEN, stroke=GREEN,
            sw=1.6, rx=8)
    cv.text(x0 + 7 * dx + 190, y0 + 132, "exhaustive search", size=14,
            weight="bold", fill=GREY, anchor="middle")
    cv.math(x0 + 7 * dx + 190, y0 + 162,
            "O(2^{M})   \u2192   O(M\u00b2)", size=24, fill=GREEN, anchor="middle",
            weight="bold")
    cv.text(x0 + 7 * dx + 190, y0 + 188, "by dynamic programming", size=13,
            fill=GREEN, anchor="middle")

    cv.text(0, 40, "target length", size=14, weight="bold", fill=NAVY)
    cv.math(0, 70, "L = 2", size=26, fill=NAVY, weight="bold")
    cv.text(0, 100, "so the extended", size=13, fill=GREY)
    cv.text(0, 118, "sequence holds", size=13, fill=GREY)
    cv.math(0, 146, "2L + 1 = 5", size=19, fill=INK)
    cv.text(0, 172, "positions, with a", size=13, fill=GREY)
    cv.text(0, 190, "blank around every", size=13, fill=GREY)
    cv.text(0, 208, "kept concept.", size=13, fill=GREY)
    note(cv, 0, 240, "Worked example from")
    note(cv, 0, 256, "Table 6:  M = 8,  L = 2.")

    # The two recursions, with real sub/superscripts.
    cv.rect(0, 274, 1152, 62, fill=FILL_GREY, stroke=GREY, sw=1.4, rx=8)
    cv.math(28, 312,
            "\u03b1(t,l) = p(z_{l}|y_{t}) \u00b7 [ \u03b1(t\u22121,l) + \u03b1(t\u22121,l\u22121) ]",
            size=21, fill=INK)
    cv.line(576, 284, 576, 326, stroke="#C9D6E4", sw=1.4)
    cv.math(604, 312,
            "\u03b2(t,l) = [ \u03b2(t+1,l) + \u03b2(t+1,l+1) ] \u00b7 p(z_{l}|y_{t})",
            size=21, fill=INK)


# ---------------------------------------------------------------- 15 · gradient

def fig_gradient(cv: Canvas):
    ex = DATA["dp_example"]
    gamma, total = ex["gamma"], ex["row_total"]
    hi = max(max(r) for r in gamma)

    top = panel(cv, 0, 0, 596, 356, "\u03b3 = \u03b1\u03b2 / p(Z|Y)   \u2014  the posterior over alignments")
    cw, ch, gx, gy = 74, 30, 130, top + 28
    for l in range(5):
        cv.text(gx + l * cw + cw / 2, gy - 8, f"l={l + 1}", size=13,
                weight="bold", fill=GREY, anchor="middle")
    cv.text(gx + 5 * cw + 52, gy - 8, "row sum", size=13, weight="bold",
            fill=NAVY, anchor="middle")
    for t, row in enumerate(gamma):
        cv.text(gx - 14, gy + t * ch + 20, f"t{t + 1}", size=13, weight="bold",
                fill=INK, anchor="end")
        for l, v in enumerate(row):
            cv.rect(gx + l * cw, gy + t * ch, cw - 2, ch - 2, fill=NAVY,
                    stroke=None, rx=2, opacity=round(0.06 + 0.82 * v / hi, 3))
            cv.text(gx + l * cw + (cw - 2) / 2, gy + t * ch + 20,
                    f"{v:.3f}", size=12.5,
                    weight="bold" if v > hi * 0.5 else None,
                    fill=WHITE if v > hi * 0.5 else INK, anchor="middle")
        cv.text(gx + 5 * cw + 52, gy + t * ch + 20, f"{total:.3f}", size=12.5,
                weight="bold", fill=NAVY, anchor="middle")
    note(cv, gx, gy + 8 * ch + 22,
         "The row sum is constant in t \u2014 every column redistributes the same "
         "total probability mass.")

    top = panel(cv, 624, 0, 528, 356, "From posterior to gradient")
    y = top + 12
    cv.rect(648, y, 480, 56, fill=FILL_GREY, stroke=GREY, sw=1.4, rx=6)
    cv.math(668, y + 36,
            "p(Z^{V}|Y^{V}) = \u03b1(M,2L) + \u03b1(M,2L+1) = \u03b2(1,1) + \u03b2(1,2)",
            size=16, fill=INK)
    cv.arrow(888, y + 62, 888, y + 80, color="navy", sw=2.2)

    y += 82
    cv.rect(648, y, 480, 52, fill=FILL_GREY, stroke=GREY, sw=1.4, rx=6)
    cv.math(668, y + 34, "L_{VCM} = \u2212 log p(Z^{V}|Y^{V})", size=20, fill=INK)
    cv.arrow(888, y + 58, 888, y + 76, color="navy", sw=2.2)

    y += 78
    cv.rect(648, y, 480, 62, fill=FILL_BLUE, stroke=NAVY, sw=2, rx=6)
    cv.math(668, y + 40,
            "\u2202L_{VCM} / \u2202y_{t}(z_{l}) = p(z_{l}|y_{t}) \u2212 \u03b3(t,l)",
            size=19, fill=NAVY, weight="bold")

    y += 76
    cv.text(648, y + 16, "prediction minus posterior \u2014 the same shape as CTC.",
            size=15, weight="bold", fill=INK)
    cv.text(648, y + 44,
            f"keep token t   when   p({SYM_KEEP} | y) > p({SYM_BLANK} | y)",
            size=17, weight="bold", fill=RED)


# ------------------------------------------------------------------- 16 · merge

def fig_merge(cv: Canvas):
    ex = DATA["dp_example"]
    p_star = ex["p_star"]
    keep = [p > 0.5 for p in p_star]

    cell, gap, x0, y0 = 68, 12, 88, 12
    cv.text(0, y0 + 30, "token", size=14, weight="bold", fill=GREY)
    cv.text(0, y0 + 48, "level", size=14, weight="bold", fill=GREY)
    for t in range(8):
        bx = x0 + t * (cell + gap)
        lit = keep[t]
        cv.rect(bx, y0, cell, 46, fill=FILL_BLUE_D if lit else WHITE,
                stroke=NAVY if lit else "#DDE6EE", sw=1.8 if lit else 1.2, rx=5)
        cv.math(bx + cell / 2, y0 + 30, f"h_{{{t + 1}}}", size=20,
                fill=NAVY if lit else MUTED, anchor="middle")
        cv.text(bx + cell / 2, y0 + 66, f"{p_star[t]:.1f}", size=13,
                weight="bold", fill=RED if lit else MUTED, anchor="middle")
        if not lit:
            cv.line(bx + 12, y0 + 88, bx + cell - 12, y0 + 100, stroke=MUTED, sw=2)
            cv.line(bx + 12, y0 + 100, bx + cell - 12, y0 + 88, stroke=MUTED, sw=2)
    cv.text(0, y0 + 70, f"p({SYM_KEEP})", size=13, weight="bold", fill=GREY)
    cv.text(0, y0 + 98, "dropped", size=13, weight="bold", fill=MUTED)

    # The two surviving runs.
    runs = [(2, 3), (6, 7)]
    for ri, (a, b) in enumerate(runs):
        ax = x0 + a * (cell + gap) - 6
        bx = x0 + b * (cell + gap) + cell + 6
        cv.rect(ax, y0 - 8, bx - ax, 62, fill=None, stroke=RED, sw=2.2, rx=8,
                dash="7 5")
        mid = (ax + bx) / 2
        cv.arrow(mid, y0 + 116, mid, y0 + 152, color="red", sw=2.4)
        cv.text(mid, y0 + 140, "score-weighted average", size=13, weight="bold",
                fill=RED, anchor="middle")
        cx = 300 + ri * 300
        cv.rect(cx, y0 + 162, 168, 54, fill=FILL_AMBER, stroke=AMBER, sw=1.8, rx=6)
        cv.math(cx + 84, y0 + 196, f"h^{{C}}_{{{ri + 1}}}", size=24, fill=AMBER,
                anchor="middle", weight="bold")
        cv.arrow(mid, y0 + 152, cx + 84, y0 + 160, color="red", sw=2.2)

    cv.text(576, y0 + 240, "2 vision concepts  \u2014  exactly the target length L",
            size=17, weight="bold", fill=AMBER, anchor="middle")

    cv.arrow(770, y0 + 190, 826, y0 + 190, color="navy", sw=2.4)
    llm_box(cv, 838, y0 + 156, 160, 66, "Large Language\nModel", size=14)
    cv.arrow(1002, y0 + 190, 1040, y0 + 190, color="navy", sw=2.4)
    bubble(cv, 1050, y0 + 168, 102, 44, "answer", size=14, fill=FILL_GREEN,
           stroke=GREEN, color=GREEN, tail=None)

    top = panel(cv, 0, 288, 556, 94, None)
    cv.text(20, top + 14, "Implementation", size=16, weight="bold", fill=NAVY)
    cv.text(20, top + 42,
            "Variable-length segments are merged with cumulative sums,", size=14,
            fill=INK)
    cv.text(20, top + 62,
            "not a double loop over batch and sequence.", size=14, fill=INK)
    cv.rect(392, top + 18, 146, 52, fill=FILL_GREEN, stroke=GREEN, sw=1.6, rx=6)
    cv.text(465, top + 44, "100\u00d7", size=26, weight="bold", fill=GREEN,
            anchor="middle")
    cv.text(465, top + 64, "faster", size=13, weight="bold", fill=GREEN,
            anchor="middle")

    top = panel(cv, 596, 288, 556, 94, None)
    cv.text(616, top + 14, "The objective actually optimized", size=16,
            weight="bold", fill=NAVY)
    cv.math(616, top + 44,
            "L^{I} = L_{NTP} + \u03b1 \u00b7 L_{SA}", size=18, fill=INK)
    cv.math(616, top + 70,
            "L^{II} = L_{NTP} + \u03b5(r) \u00b7 L_{VCM}", size=18, fill=INK)
    cv.text(892, top + 44, "pre-training", size=13.5, fill=GREY)
    cv.text(892, top + 70, "instruction fine-tuning", size=13.5, fill=GREY)


# --------------------------------------------------------------------- 17 · vqa

def _style(row):
    role = row.get("role")
    if role == "ours":
        return {"color": FILL_BLUE_D, "edge": NAVY, "bold": True}
    if role == "baseline":
        return {"color": FILL_AMBER, "edge": AMBER, "vcolor": AMBER}
    return {"color": FILL_GREY, "edge": GREY, "vcolor": GREY, "lcolor": GREY}


def fig_vqa(cv: Canvas):
    rows = DATA["vqa11"]
    items = [dict(label=r["name"], value=r["avg"], sub=f"{r['tokens']} tok",
                  **_style(r)) for r in rows]
    top = panel(cv, 0, 0, 690, 340, None)
    bar_chart(cv, 46, top + 22, 606, 216, items, vmin=50, vmax=62,
              baseline=59.5, baseline_label="LLaVA-1.5 baseline",
              label_size=14, value_size=17)
    axis_note(cv, 46, top + 314, "50.0")

    top = panel(cv, 714, 0, 438, 340,
                "Per-benchmark change, VCM 144 vs LLaVA-1.5 576")
    zero = 900
    for i, (name, d) in enumerate(DATA["vqa11_delta"]):
        y = top + 12 + i * 25
        cv.text(756, y + 12, name, size=13.5, weight="bold", fill=INK)
        w = abs(d) * 22
        pos = d >= 0
        cv.rect(zero if pos else zero - w, y + 2, max(w, 1.5), 16,
                fill=FILL_GREEN if pos else FILL_RED,
                stroke=GREEN if pos else RED, sw=1.2, rx=2)
        cv.text(zero + (w + 8 if pos else -w - 8), y + 15,
                f"{d:+.1f}", size=13, weight="bold",
                fill=GREEN if pos else RED, anchor="start" if pos else "end")
    cv.line(zero, top + 8, zero, top + 262, stroke=GREY, sw=1.4)
    cv.text(zero, top + 280, "0", size=12, fill=GREY, anchor="middle")
    note(cv, 756, top + 288,
         "MME reported separately: 1862.1 \u2192 1842.7 (\u221219.4);")
    note(cv, 756, top + 304, "it uses a 0\u20132800 scale, not percent.")


# -------------------------------------------------------------- 18 · efficiency

def fig_efficiency(cv: Canvas):
    rows = DATA["cost"]
    top = panel(cv, 0, 0, 740, 340,
                "Accuracy against measured latency \u2014 upper left is better")
    ax, ay, aw, ah = 82, top + 16, 610, 240
    xlo, xhi, ylo, yhi = 24, 62, 42, 65

    for gy in range(45, 66, 5):
        py = ay + ah - (gy - ylo) / (yhi - ylo) * ah
        cv.line(ax, py, ax + aw, py, stroke="#EDF1F6", sw=1.2)
        cv.text(ax - 10, py + 5, str(gy), size=12.5, fill=GREY, anchor="end")
    for gx in range(25, 61, 5):
        px = ax + (gx - xlo) / (xhi - xlo) * aw
        cv.text(px, ay + ah + 22, str(gx), size=12.5, fill=GREY, anchor="middle")
    cv.line(ax, ay + ah, ax + aw, ay + ah, stroke=GREY, sw=1.5)
    cv.line(ax, ay, ax, ay + ah, stroke=GREY, sw=1.5)
    cv.text(ax + aw / 2, ay + ah + 46, "latency (ms)", size=14, weight="bold",
            fill=GREY, anchor="middle")
    cv.text(ax - 46, ay + ah / 2, "Avg. (%)", size=14, weight="bold", fill=GREY,
            anchor="middle")

    def px_py(r):
        return (ax + (r["lat"] - xlo) / (xhi - xlo) * aw,
                ay + ah - (r["avg"] - ylo) / (yhi - ylo) * ah)

    ours = [r for r in rows if r.get("role") == "ours"]
    cv.path("M " + " L ".join(f"{px_py(r)[0]:.1f} {px_py(r)[1]:.1f}"
                              for r in sorted(ours, key=lambda r: r["lat"])),
            stroke=NAVY, sw=2.2, dash="7 5")

    offsets = {"LLaVA-1.5": (0, -18), "FastV": (0, 20), "PDrop": (0, 20),
               "SparseVLM": (-2, 20), "VCM": (0, -18)}
    for r in rows:
        x, y = px_py(r)
        role = r.get("role")
        if role == "ours":
            cv.circle(x, y, 9.5, fill=NAVY, stroke=WHITE, sw=2)
        elif role == "baseline":
            cv.circle(x, y, 8.5, fill=FILL_AMBER, stroke=AMBER, sw=2.4)
        else:
            cv.circle(x, y, 6.5, fill=WHITE, stroke=GREY, sw=2)
        dxy = offsets.get(r["name"], (0, -16))
        col = NAVY if role == "ours" else (AMBER if role == "baseline" else GREY)
        cv.text(x + dxy[0], y + dxy[1], f"{r['name']} {r['tokens']}", size=13,
                weight="bold", fill=col, anchor="middle")

    top = panel(cv, 764, 0, 388, 340, "Where the saving comes from")
    bar_chart(cv, 806, top + 20, 300, 150, [
        {"label": "LLaVA-1.5", "value": 4.62, "sub": "576 tok",
         "color": FILL_AMBER, "edge": AMBER, "vcolor": AMBER},
        {"label": "VCM", "value": 1.71, "sub": "128 tok",
         "color": FILL_BLUE_D, "edge": NAVY, "bold": True},
        {"label": "VCM", "value": 1.24, "sub": "64 tok",
         "color": FILL_BLUE_D, "edge": NAVY, "bold": True},
    ], vmin=0, vmax=5.2, value_fmt="{:.2f}", label_size=14, value_size=16)
    note(cv, 806, top + 208, "FLOPs (T), measured \u2014 Table 10")
    cv.rect(806, top + 226, 300, 76, fill=FILL_GREEN, stroke=GREEN, sw=1.8, rx=8)
    cv.text(956, top + 258, "85%", size=34, weight="bold", fill=GREEN,
            anchor="middle")
    cv.text(956, top + 284, "fewer FLOPs, analytically at S = 1/4", size=13,
            weight="bold", fill=GREEN, anchor="middle")


# ------------------------------------------------------------------- 19 · dense

def fig_dense(cv: Canvas):
    top = panel(cv, 0, 0, 828, 340, None)
    paired_bars(cv, 44, top + 40, 748, 202, DATA["dense"], vmin=0, vmax=50,
                legend=["CLIP ViT-L/14", "+ VCM fine-tuning"],
                colors=(FILL_GREY, FILL_BLUE_D), edges=(GREY, NAVY),
                label_size=13.5, value_size=13)
    note(cv, 44, top + 306,
         "Zero axis. Classification and CIDEr from Table 2; detection and "
         "segmentation from Table 3.")

    top = panel(cv, 852, 0, 300, 340, "Why it transfers")
    steps = [
        ("VCM fine-tunes", "the CLIP ViT itself"),
        ("dense features", "cluster by object"),
        ("drop-in encoder", "for F-VLM / Cat-Seg"),
    ]
    for i, (head, body) in enumerate(steps):
        y = top + 12 + i * 84
        cv.rect(876, y, 252, 62, fill=FILL_BLUE, stroke=NAVY, sw=1.5, rx=6)
        cv.text(1002, y + 26, head, size=15.5, weight="bold", fill=NAVY,
                anchor="middle")
        cv.text(1002, y + 48, body, size=13.5, fill=INK, anchor="middle")
        if i < 2:
            cv.arrow(1002, y + 62, 1002, y + 82, color="navy", sw=2.2)
    cv.rect(876, top + 264, 252, 40, fill=FILL_GREEN, stroke=GREEN, sw=1.6, rx=6)
    cv.text(1002, top + 290, "no task-specific retraining", size=14,
            weight="bold", fill=GREEN, anchor="middle")


# ----------------------------------------------------------------- 20 · general

def fig_general(cv: Canvas):
    blocks = [
        ("High resolution", "LLaVA-NeXT", DATA["highres"], 60, 76, "tok"),
        ("Video", "Video-LLaVA", DATA["video"], 24, 58, "tok"),
    ]
    pw = 368
    for i, (head, base, rows, vmin, vmax, unit) in enumerate(blocks):
        x = i * (pw + 24)
        top = panel(cv, x, 0, pw, 340, f"{head}  \u00b7  {base}")
        items = [dict(label=r["name"].replace("-", "-\n") if len(r["name"]) > 10
                      else r["name"], value=r["avg"], sub=f"{r['tokens']} {unit}",
                      **_style(r)) for r in rows]
        bar_chart(cv, x + 34, top + 18, pw - 68, 196, items, vmin=vmin, vmax=vmax,
                  label_size=12.5, value_size=14.5, sub_size=11)
        axis_note(cv, x + 34, top + 288, f"{vmin}.0")

    x = 2 * (pw + 24)
    top = panel(cv, x, 0, pw, 340, "Architecture and scale")
    items = [dict(label=r["name"].replace(" ", "\n"), value=r["avg"],
                  sub=r["detail"], **_style(r)) for r in DATA["scale"]]
    bar_chart(cv, x + 34, top + 18, pw - 68, 196, items, vmin=58, vmax=73,
              label_size=12.5, value_size=14.5, sub_size=10.5)
    axis_note(cv, x + 34, top + 288, "58.0")
    note(cv, x + 34, top + 306,
         "Left pair: Qwen2-VL. Right three: LLaVA-1.5 + VCM.")


# ---------------------------------------------------------------- 21 · ablation

def fig_ablation(cv: Canvas):
    top = panel(cv, 0, 0, 690, 340, "Components, added one at a time")
    items = [dict(label=r["label"], value=r["avg"], **_style(r))
             for r in DATA["ablation_components"]]
    bar_chart(cv, 46, top + 22, 606, 210, items, vmin=54, vmax=60.5,
              label_size=13.5, value_size=17)
    axis_note(cv, 46, top + 306, "54.0")
    cv.arrow(96, top + 20, 620, top + 20, color="green", sw=2.2)
    cv.text(358, top + 12, "+3.2 points", size=15, weight="bold", fill=GREEN,
            anchor="middle")

    top = panel(cv, 714, 0, 438, 340, "Information domain scalar S")
    items = [dict(label=r["label"], value=r["avg"], sub=f"{r['tokens']} tok",
                  **_style(r)) for r in DATA["ablation_domain"]]
    bar_chart(cv, 756, top + 22, 354, 210, items, vmin=54, vmax=60.5,
              label_size=13.5, value_size=16)
    axis_note(cv, 756, top + 306, "54.0")
    cv.text(933, top + 262,
            "more budget is not monotonically better", size=13.5, weight="bold",
            fill=RED, anchor="middle")


# -------------------------------------------------------------- 22 · conclusion

def fig_conclusion(cv: Canvas):
    top = panel(cv, 0, 0, 690, 300, "Contributions")
    items = [
        ("Define the vision concept model",
         "quantity, identity and location, all conditioned on the instruction"),
        ("A self-supervised framework",
         "keyword selection plus a forward\u2013backward algorithm; no concept labels"),
        ("Efficiency and capability together",
         "85% fewer FLOPs, and a stronger dense-perception encoder"),
    ]
    for i, (head, body) in enumerate(items):
        y = top + 10 + i * 82
        cv.circle(46, y + 26, 20, fill=NAVY, stroke=None)
        cv.text(46, y + 33, str(i + 1), size=21, weight="bold", fill=WHITE,
                anchor="middle")
        cv.text(82, y + 22, head, size=19, weight="bold", fill=NAVY)
        cv.text(82, y + 48, body, size=14.5, fill=INK)

    top = panel(cv, 714, 0, 438, 300, "Limitations the paper states",
                tcolor=RED)
    lims = [
        ("Keyword selection is adaptive",
         ["selected keywords may not be the", "true ones \u2014 a source of bias"]),
        ("Length estimate is coarse",
         ["min-max normalization is a", "simplification of the mapping"]),
    ]
    for i, (head, body) in enumerate(lims):
        y = top + 12 + i * 104
        cv.rect(742, y, 384, 88, fill=FILL_RED, stroke=RED, sw=1.5, rx=6)
        cv.text(762, y + 28, head, size=16, weight="bold", fill=RED)
        for j, row in enumerate(body):
            cv.text(762, y + 52 + j * 20, row, size=13.5, fill=INK)
    cv.text(742, top + 236, "Next: finer keyword selection with open-source LLMs.",
            size=14, weight="bold", fill=GREY)

    cv.rect(0, 324, 1152, 58, fill=NAVY, stroke=None, rx=8)
    cv.text(576, 360,
            "Model the concepts the instruction needs \u2014 not every token the "
            "image has.", size=23, weight="bold", fill=WHITE, anchor="middle")
