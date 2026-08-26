"""Editable SVG figures for the seven-slide NExT-OMNI talk."""

from content import DATA
from svgkit import (
    AMBER, FILL_AMBER, FILL_BLUE, FILL_BLUE_D, FILL_GREEN, FILL_GREY,
    FILL_RED, GREEN, GREY, INK, MUTED, NAVY, RED, WHITE, Canvas, bar_chart,
)

BORDER = "#C9D6E4"
PURPLE = "#7651A8"
FILL_PURPLE = "#EEE8F6"
CYAN = "#1889A6"
FILL_CYAN = "#DDF2F6"


def panel(cv, x, y, w, h, title=None, fill=WHITE, stroke=BORDER, tcolor=NAVY):
    cv.rect(x, y, w, h, fill=fill, stroke=stroke, sw=1.4, rx=8)
    if title:
        cv.text(x + 16, y + 26, title, size=17, weight="bold", fill=tcolor)
        return y + 42
    return y + 14


def pill(cv, x, y, w, text, color=NAVY, fill=FILL_BLUE, size=14):
    cv.rect(x, y, w, 34, fill=fill, stroke=color, sw=1.4, rx=17)
    cv.text(x + w / 2, y + 22, text, size=size, weight="bold", fill=color,
            anchor="middle")


def card(cv, x, y, w, h, head, body, color=NAVY, fill=FILL_BLUE):
    cv.rect(x, y, w, h, fill=fill, stroke=color, sw=1.5, rx=8)
    cv.text(x + 16, y + 28, head, size=16, weight="bold", fill=color)
    rows = body if isinstance(body, (list, tuple)) else [body]
    for i, row in enumerate(rows):
        cv.text(x + 16, y + 54 + i * 20, row, size=13.5, fill=INK)


def modality_icon(cv, x, y, label, color, fill):
    cv.circle(x, y, 30, fill=fill, stroke=color, sw=1.8)
    symbol = {"TEXT": "T", "IMAGE": "V", "VIDEO": "▶", "AUDIO": "∿"}[label]
    cv.text(x, y + 8, symbol, size=24, weight="bold", fill=color,
            anchor="middle")
    cv.text(x, y + 52, label, size=13, weight="bold", fill=color,
            anchor="middle")


def token_row(cv, x, y, colors, cell=24, gap=5):
    for i, color in enumerate(colors):
        cv.rect(x + i * (cell + gap), y, cell, cell, fill=color,
                stroke=WHITE, sw=1, rx=3)


def style(row):
    if row.get("role") == "ours":
        return dict(color=FILL_BLUE_D, edge=NAVY, bold=True)
    if row.get("role") == "baseline":
        return dict(color=FILL_AMBER, edge=AMBER, vcolor=AMBER)
    return dict(color=FILL_GREY, edge=GREY, vcolor=GREY, lcolor=GREY)


def fig_title_motif(cv: Canvas):
    """Four modality streams converge into a corrected token field."""
    cols = [(NAVY, 710), (PURPLE, 752), (CYAN, 794), (AMBER, 836)]
    for color, y in cols:
        for i in range(13):
            cv.rect(728 + i * 34, y - 676, 22, 22, fill=color, stroke=None,
                    rx=4, opacity=0.26 + i * 0.045)
    for r in range(6):
        for c in range(12):
            active = (r * 7 + c * 5) % 8 < 5
            cv.rect(846 + c * 31, 188 + r * 31, 21, 21,
                    fill=WHITE if active else "#7FA8D2", stroke=None, rx=3,
                    opacity=0.62 if active else 0.22)
    cv.text(1216, 402, "discrete flow  ·  any-to-any", size=15, weight="bold",
            fill="#8DB1D2", anchor="end")


def fig_problem(cv: Canvas):
    """AR conflict, hybrid fragmentation, and the desired capability cube."""
    top = panel(cv, 0, 0, 350, 286, "Autoregressive")
    token_row(cv, 28, top + 34, [FILL_BLUE_D] * 8)
    for i in range(7):
        cv.arrow(51 + i * 29, top + 46, 73 + i * 29, top + 46,
                 color="navy", sw=1.6)
    cv.text(175, top + 90, "left → right, one token at a time",
            size=14, weight="bold", fill=NAVY, anchor="middle")
    card(cv, 24, top + 112, 302, 58, "Understanding",
         "needs bidirectional evidence", RED, FILL_RED)
    card(cv, 24, top + 180, 302, 58, "Generation",
         "needs flexible refinement", AMBER, FILL_AMBER)

    top = panel(cv, 374, 0, 350, 286, "Hybrid / decoupled")
    for i, (head, col, fill) in enumerate((
            ("understand", NAVY, FILL_BLUE), ("generate", AMBER, FILL_AMBER),
            ("retrieve", PURPLE, FILL_PURPLE))):
        y = top + 18 + i * 66
        cv.rect(402, y, 112, 44, fill=fill, stroke=col, sw=1.4, rx=6)
        cv.text(458, y + 28, head, size=13.5, weight="bold", fill=col,
                anchor="middle")
        cv.arrow(522, y + 22, 566, y + 22, color="grey", sw=1.8)
        cv.rect(578, y, 118, 44, fill=FILL_GREY, stroke=GREY, sw=1.3, rx=6)
        cv.text(637, y + 28, "own module", size=13, weight="bold", fill=GREY,
                anchor="middle")
    cv.text(549, top + 232, "more parameters · slower · separated features",
            size=13.5, weight="bold", fill=RED, anchor="middle")

    top = panel(cv, 748, 0, 404, 286, "What an omni model must unify")
    modalities = [
        ("TEXT", NAVY, FILL_BLUE), ("IMAGE", PURPLE, FILL_PURPLE),
        ("VIDEO", CYAN, FILL_CYAN), ("AUDIO", AMBER, FILL_AMBER),
    ]
    for i, args in enumerate(modalities):
        modality_icon(cv, 804 + i * 94, top + 62, *args)
    tasks = [
        ("UNDERSTAND", NAVY, FILL_BLUE), ("GENERATE", AMBER, FILL_AMBER),
        ("RETRIEVE", PURPLE, FILL_PURPLE),
    ]
    for i, (lab, col, fill) in enumerate(tasks):
        pill(cv, 776 + i * 122, top + 146, 108, lab, col, fill, 12.5)
    cv.rect(782, top + 204, 336, 42, fill=FILL_GREEN, stroke=GREEN, sw=1.5, rx=7)
    cv.text(950, top + 231, "one representation · any input → any output",
            size=14, weight="bold", fill=GREEN, anchor="middle")

    cv.rect(0, 306, 1152, 76, fill=NAVY, stroke=NAVY, sw=1.5, rx=8)
    cv.text(576, 338, "Design target", size=14, weight="bold",
            fill="#9FC0DE", anchor="middle")
    cv.text(576, 365,
            "Fuse the modalities deeply without splitting understanding from generation",
            size=19, weight="bold", fill=WHITE, anchor="middle")


def fig_flow(cv: Canvas):
    """Discrete corruption path, global prediction, and iterative correction."""
    cv.text(46, 26, "corrupted sequence", size=14, weight="bold", fill=GREY)
    cv.text(1106, 26, "data sequence", size=14, weight="bold", fill=NAVY,
            anchor="end")
    stages = [
        (0.0, [GREY] * 12, "t = 0"),
        (0.35, [GREY, NAVY, GREY, PURPLE, GREY, GREY, CYAN, GREY, GREY, AMBER, GREY, GREY],
         "t = .35"),
        (0.70, [NAVY, NAVY, PURPLE, PURPLE, CYAN, CYAN, CYAN, AMBER, AMBER, NAVY, GREY, PURPLE],
         "t = .70"),
        (1.0, [NAVY, NAVY, PURPLE, PURPLE, CYAN, CYAN, CYAN, AMBER, AMBER, NAVY, NAVY, PURPLE],
         "t = 1"),
    ]
    xs = [28, 310, 592, 874]
    for i, ((_, colors, lab), x) in enumerate(zip(stages, xs)):
        cv.rect(x, 48, 250, 106, fill=FILL_GREY if i == 0 else WHITE,
                stroke=GREY if i == 0 else NAVY, sw=1.5, rx=8)
        token_row(cv, x + 20, 76, colors, cell=14, gap=4)
        token_row(cv, x + 20, 98, colors[::-1], cell=14, gap=4)
        cv.text(x + 125, 139, lab, size=15, weight="bold",
                fill=GREY if i == 0 else NAVY, anchor="middle")
        if i < 3:
            cv.arrow(x + 254, 101, x + 278, 101, color="red", sw=2.3)

    cv.rect(72, 182, 1008, 58, fill=FILL_BLUE, stroke=NAVY, sw=1.7, rx=9)
    cv.text(576, 208,
            "One bidirectional backbone predicts every clean token from the whole noisy sequence",
            size=17, weight="bold", fill=NAVY, anchor="middle")
    cv.math(576, 229, "x_t ~ p_t(·|x_1)       model: p_{1|t}(x_1|x_t)",
            size=15, fill=INK, anchor="middle")

    cards = [
        ("GLOBAL CORRUPTION", "noise all positions", RED, FILL_RED),
        ("GLOBAL VELOCITY", "move along the path", PURPLE, FILL_PURPLE),
        ("GLOBAL CORRECTION", "refine in parallel", GREEN, FILL_GREEN),
    ]
    for i, (head, body, col, fill) in enumerate(cards):
        x = 84 + i * 354
        card(cv, x, 270, 306, 86, head, body, col, fill)
        if i < 2:
            cv.arrow(x + 310, 313, x + 344, 313, color="navy", sw=2.2)
    cv.text(576, 380,
            "Unlike causal masking, every position can integrate context from both directions",
            size=14.5, weight="bold", fill=GREY, anchor="middle")


def fig_architecture(cv: Canvas):
    """Encoders, codebooks, unified transformer, heads, and objectives."""
    modalities = [
        ("TEXT", NAVY, FILL_BLUE), ("IMAGE", PURPLE, FILL_PURPLE),
        ("VIDEO", CYAN, FILL_CYAN), ("AUDIO", AMBER, FILL_AMBER),
    ]
    for i, (lab, col, fill) in enumerate(modalities):
        y = 6 + i * 90
        modality_icon(cv, 42, y + 30, lab, col, fill)
        cv.arrow(78, y + 30, 118, y + 30, color="navy", sw=2)
        cv.rect(130, y + 7, 150, 48, fill=fill, stroke=col, sw=1.4, rx=6)
        cv.text(205, y + 37,
                "tokenizer" if lab == "TEXT" else f"{lab.lower()} encoder",
                size=14, weight="bold", fill=col, anchor="middle")
        cv.arrow(286, y + 30, 326, y + 30, color="navy", sw=2)
        cv.rect(338, y + 7, 112, 48, fill=WHITE, stroke=col, sw=1.4, rx=6)
        cv.text(394, y + 29, "word embedding" if lab == "TEXT" else "codebook",
                size=12.5, weight="bold", fill=col, anchor="middle")
        cv.text(394, y + 45, "discrete tokens", size=11.5, fill=GREY,
                anchor="middle")

    cv.arrow(460, 184, 508, 184, color="navy", sw=2.6)
    cv.rect(520, 28, 274, 310, fill=FILL_BLUE, stroke=NAVY, sw=2, rx=10)
    cv.text(657, 66, "UNIFIED DISCRETE FLOW", size=21, weight="bold", fill=NAVY,
            anchor="middle")
    for i in range(5):
        y = 92 + i * 42
        cv.rect(550, y, 214, 30, fill=WHITE, stroke=NAVY, sw=1.1, rx=5)
        cv.text(657, y + 20,
                "multimodal self-attention" if i % 2 == 0 else "feed-forward network",
                size=12.5, weight="bold", fill=NAVY, anchor="middle")
    cv.rect(550, 306, 214, 22, fill=NAVY, stroke=None, rx=4)
    cv.text(657, 321, "deep fusion at every layer", size=12, weight="bold",
            fill=WHITE, anchor="middle")

    heads = [
        ("LM head", NAVY, FILL_BLUE), ("vision head", PURPLE, FILL_PURPLE),
        ("audio head", AMBER, FILL_AMBER), ("<EOS> feature", GREEN, FILL_GREEN),
    ]
    for i, (lab, col, fill) in enumerate(heads):
        y = 42 + i * 74
        cv.arrow(804, y + 22, 842, y + 22, color="navy", sw=2)
        cv.rect(854, y, 138, 44, fill=fill, stroke=col, sw=1.4, rx=6)
        cv.text(923, y + 28, lab, size=14, weight="bold", fill=col,
                anchor="middle")
        dest = ["text", "image / video", "speech / audio", "retrieval"][i]
        cv.text(1016, y + 27, dest, size=13.5, weight="bold", fill=INK)

    cv.rect(842, 342, 310, 40, fill=FILL_GREY, stroke=GREY, sw=1.3, rx=6)
    cv.math(997, 368, "L = λ₁L_CE + λ₂L^V_rec + λ₃L^A_rec",
            size=17, fill=INK, anchor="middle")


def fig_efficiency(cv: Canvas):
    """Interleaved batches, dynamic block growth, and adaptive caching."""
    top = panel(cv, 0, 0, 350, 300, "1 · Interleave modality batches")
    colors = [PURPLE, AMBER, NAVY, CYAN, PURPLE, NAVY, AMBER]
    labels = ["V", "A", "T", "Vd", "V", "T", "A"]
    for i, (col, lab) in enumerate(zip(colors, labels)):
        y = top + 8 + i * 30
        cv.rect(28, y, 68, 22, fill=col, stroke=None, rx=4)
        cv.text(62, y + 15, lab, size=12, weight="bold", fill=WHITE,
                anchor="middle")
        cv.rect(108, y, 204, 22, fill=FILL_GREY, stroke=GREY, sw=0.8, rx=4)
        cv.rect(108, y, 204 * (0.42 + (i % 3) * 0.18), 22,
                fill=FILL_BLUE_D, stroke=None, rx=4)
    cv.rect(28, top + 230, 284, 38, fill=FILL_GREEN, stroke=GREEN, sw=1.4, rx=6)
    cv.text(170, top + 255, "1.4× training efficiency",
            size=16, weight="bold", fill=GREEN, anchor="middle")

    top = panel(cv, 374, 0, 390, 300, "2 · Grow response length by blocks")
    cv.text(398, top + 18, "training", size=13, weight="bold", fill=GREY)
    for i in range(5):
        cv.rect(398 + i * 52, top + 34, 42, 34,
                fill=FILL_BLUE_D if i < 3 else FILL_GREY,
                stroke=NAVY if i < 3 else GREY, sw=1.2, rx=4)
        cv.text(419 + i * 52, top + 56, "tok" if i < 3 else "PAD",
                size=11.5, weight="bold", fill=NAVY if i < 3 else GREY,
                anchor="middle")
    cv.text(398, top + 104, "inference", size=13, weight="bold", fill=GREY)
    for row in range(3):
        y = top + 120 + row * 42
        blocks = row + 1
        for i in range(blocks):
            cv.rect(452 + i * 72, y, 62, 28, fill=FILL_BLUE,
                    stroke=NAVY, sw=1.2, rx=4)
        cv.text(420, y + 19, f"step {row + 1}", size=12.5, weight="bold",
                fill=NAVY, anchor="middle")
        if row < 2:
            cv.arrow(646, y + 14, 694, y + 14, color="red", sw=1.8)
            cv.text(738, y + 19, "expand", size=12.5, weight="bold", fill=RED,
                    anchor="end")
    cv.text(569, top + 264, "EOS confidence decides when to stop",
            size=13.5, weight="bold", fill=NAVY, anchor="middle")

    top = panel(cv, 788, 0, 364, 300, "3 · Cache what barely changes")
    grid_x, grid_y = 816, top + 30
    for r in range(6):
        for c in range(9):
            stable = c < 4 or (r + c) % 4 != 0
            cv.rect(grid_x + c * 30, grid_y + r * 30, 23, 23,
                    fill=FILL_GREEN if stable else FILL_RED,
                    stroke=GREEN if stable else RED, sw=1, rx=3)
    cv.text(838, top + 236, "cached", size=13, weight="bold", fill=GREEN)
    cv.text(974, top + 236, "updated", size=13, weight="bold", fill=RED)
    cv.rect(816, top + 250, 308, 30, fill=FILL_GREEN, stroke=GREEN, sw=1.3, rx=6)
    cv.text(970, top + 271, "1.2× vs AR response speed",
            size=14.5, weight="bold", fill=GREEN, anchor="middle")

    cv.rect(0, 320, 1152, 62, fill=NAVY, stroke=NAVY, sw=1.4, rx=8)
    cv.text(576, 358,
            "Parallel decoding supplies the opportunity; scheduling and caching realize the gain",
            size=18, weight="bold", fill=WHITE, anchor="middle")


def fig_results(cv: Canvas):
    """Three source-checked benchmark panels plus headline deltas."""
    groups = [
        ("Omnimodal understanding", DATA["understanding"], 25, 42, "Table 1"),
        ("Multi-turn vision", DATA["vision_interaction"], 45, 57, "Table 2"),
        ("Cross-modal retrieval", DATA["retrieval"], 26, 34, "Table 4"),
    ]
    for i, (head, rows, vmin, vmax, source) in enumerate(groups):
        x = i * 392
        top = panel(cv, x, 0, 368, 292, head)
        items = [dict(label=r["name"].replace("-", "-\n"), value=r["avg"],
                      **style(r)) for r in rows]
        bar_chart(cv, x + 32, top + 10, 304, 184, items, vmin=vmin, vmax=vmax,
                  label_size=11.5, value_size=15, sub_size=10)
        cv.text(x + 32, top + 242, f"Avg. (%) · axis starts at {vmin}",
                size=11.5, fill=MUTED)
        cv.text(x + 336, top + 242, source, size=11.5, weight="bold",
                fill=GREY, anchor="end")

    kpis = [
        ("+3.2", "vs OpenOmni", "understanding", NAVY, FILL_BLUE),
        ("+4.6", "vs next best", "multi-turn vision", PURPLE, FILL_PURPLE),
        ("+1.1", "vs MMaDA", "retrieval", GREEN, FILL_GREEN),
    ]
    for i, (value, comp, task, col, fill) in enumerate(kpis):
        x = i * 392
        cv.rect(x, 314, 368, 68, fill=fill, stroke=col, sw=1.5, rx=8)
        cv.text(x + 78, 357, value, size=28, weight="bold", fill=col,
                anchor="middle")
        cv.text(x + 220, 341, comp, size=14, weight="bold", fill=INK,
                anchor="middle")
        cv.text(x + 220, 364, task, size=13, fill=GREY, anchor="middle")


def fig_takeaway(cv: Canvas):
    """Ablation trajectory, contribution stack, and honest scope."""
    top = panel(cv, 0, 0, 660, 292, "Cumulative ablation average · Table 5")
    items = [dict(label=r["name"].replace(" · ", "\n"), value=r["avg"],
                  **style(r)) for r in DATA["ablation"]]
    bar_chart(cv, 44, top + 14, 574, 184, items, vmin=40, vmax=47,
              label_size=12, value_size=16)
    cv.text(44, top + 244, "Average over understanding, generation, and retrieval",
            size=12, fill=MUTED)
    cv.arrow(96, top + 6, 594, top + 6, color="green", sw=2.1)
    cv.text(345, top, "+4.2 points end to end", size=14, weight="bold",
            fill=GREEN, anchor="middle")

    top = panel(cv, 684, 0, 468, 292, "The recipe")
    steps = [
        ("DFM", "bidirectional correction", NAVY, FILL_BLUE),
        ("Unified rep.", "one feature space", PURPLE, FILL_PURPLE),
        ("Dynamic length", "restore understanding", AMBER, FILL_AMBER),
        ("Reconstruction", "retain fine detail", GREEN, FILL_GREEN),
    ]
    for i, (head, body, col, fill) in enumerate(steps):
        y = top + 2 + i * 58
        cv.circle(718, y + 20, 16, fill=col, stroke=None)
        cv.text(718, y + 26, str(i + 1), size=14, weight="bold", fill=WHITE,
                anchor="middle")
        cv.rect(746, y, 378, 42, fill=fill, stroke=col, sw=1.2, rx=6)
        cv.text(760, y + 18, head, size=14.5, weight="bold", fill=col)
        cv.text(908, y + 18, body, size=13.5, fill=INK)

    cards = [
        ("CONTRIBUTION", "First open-source omni model fully built on DFM",
         NAVY, FILL_BLUE),
        ("CAPABILITY", "Text · image · video · audio, any-to-any",
         PURPLE, FILL_PURPLE),
        ("NEXT STEP", "Action trajectories and world-model video",
         AMBER, FILL_AMBER),
    ]
    for i, (head, body, col, fill) in enumerate(cards):
        x = i * 392
        cv.rect(x, 314, 368, 68, fill=fill, stroke=col, sw=1.5, rx=8)
        cv.text(x + 18, 339, head, size=13.5, weight="bold", fill=col)
        cv.text(x + 18, 363, body, size=13.5, weight="bold", fill=INK)


# ---------------------------------------------------------- visual refinement
# These final definitions intentionally override the first-pass versions above.
# The refined deck uses fewer boxes, larger focal graphics, and a continuous
# visual story from fragmentation to flow to fusion.

def fig_title_motif(cv: Canvas):
    streams = [
        (NAVY, 48, "T"), (PURPLE, 86, "V"), (CYAN, 124, "▶"), (AMBER, 162, "∿"),
    ]
    for color, y, symbol in streams:
        cv.circle(760, y, 13, fill=color, stroke=WHITE, sw=1.2, opacity=0.82)
        cv.text(760, y + 5, symbol, size=12, weight="bold", fill=WHITE,
                anchor="middle")
        cv.path(
            f"M 780 {y} C 900 {y}, 910 {202 + (y - 48) * .2}, 1008 202",
            stroke=color, sw=4, opacity=0.58,
        )
    cv.circle(1030, 202, 50, fill=WHITE, stroke="#7FA8D2", sw=2, opacity=0.18)
    cv.circle(1030, 202, 34, fill=WHITE, stroke=None, opacity=0.22)
    cv.text(1030, 199, "DFM", size=20, weight="bold", fill=WHITE,
            anchor="middle")
    cv.text(1030, 220, "unified flow", size=12, weight="bold", fill="#A9C6E2",
            anchor="middle")
    for i in range(7):
        angle_y = 120 + i * 28
        cv.path(f"M 1076 202 C 1130 202, 1140 {angle_y}, 1210 {angle_y}",
                stroke=WHITE, sw=2.2, opacity=0.18 + i * 0.06)
        cv.circle(1224, angle_y, 8, fill=WHITE, stroke=None,
                  opacity=0.22 + i * 0.05)
    cv.text(1248, 344, "any input  →  any output", size=15, weight="bold",
            fill="#8DB1D2", anchor="end")


def fig_problem(cv: Canvas):
    # Left: causal AR corridor.
    cv.text(0, 24, "01  CAUSAL BOTTLENECK", size=15, weight="bold", fill=RED)
    cv.text(0, 54, "Autoregression forces every modality through one direction",
            size=19, weight="bold", fill=INK)
    x0, y0 = 18, 92
    for i in range(10):
        col = [NAVY, NAVY, PURPLE, PURPLE, CYAN, CYAN, AMBER, AMBER, NAVY, PURPLE][i]
        cv.rect(x0 + i * 43, y0, 31, 31, fill=col, stroke=WHITE, sw=1, rx=4)
        if i < 9:
            cv.arrow(x0 + i * 43 + 32, y0 + 15, x0 + (i + 1) * 43 - 3,
                     y0 + 15, color="grey", sw=1.6)
    cv.text(214, 148, "token 1 must wait for token 0", size=14,
            weight="bold", fill=RED, anchor="middle")
    cv.path("M 18 174 C 120 200, 320 150, 438 180", stroke=RED, sw=2.5,
            dash="7 5")
    cv.text(220, 211, "understanding wants both directions", size=14,
            weight="bold", fill=NAVY, anchor="middle")

    # Right: separated hybrid branches.
    cv.text(588, 24, "02  DECOUPLING TAX", size=15, weight="bold", fill=AMBER)
    cv.text(588, 54, "Hybrid systems solve the conflict by duplicating pathways",
            size=19, weight="bold", fill=INK)
    cv.rect(590, 86, 126, 114, fill=FILL_GREY, stroke=GREY, sw=1.5, rx=8)
    cv.text(653, 116, "shared", size=15, weight="bold", fill=GREY,
            anchor="middle")
    cv.text(653, 142, "input", size=15, weight="bold", fill=GREY,
            anchor="middle")
    cv.text(653, 178, "T · V · A", size=17, weight="bold", fill=INK,
            anchor="middle")
    branches = [
        ("understand", NAVY, FILL_BLUE, 82),
        ("generate", AMBER, FILL_AMBER, 140),
        ("retrieve", PURPLE, FILL_PURPLE, 198),
    ]
    for label, col, fill, y in branches:
        cv.path(f"M 716 143 C 760 143, 760 {y + 18}, 808 {y + 18}",
                stroke=col, sw=2.2)
        cv.rect(820, y, 288, 38, fill=fill, stroke=col, sw=1.4, rx=6)
        cv.text(842, y + 25, label, size=14.5, weight="bold", fill=col)
        cv.text(1088, y + 25, "separate module", size=13, fill=GREY,
                anchor="end")
    cv.text(964, 257, "features stay separated", size=14, weight="bold",
            fill=RED, anchor="middle")

    # Bottom: one bold target statement with modality/task matrix.
    cv.rect(0, 282, 1152, 100, fill=NAVY, stroke=NAVY, sw=1.5, rx=9)
    cv.text(28, 316, "THE TARGET", size=14, weight="bold", fill="#9FC0DE")
    cv.text(28, 350, "one representation", size=24, weight="bold", fill=WHITE)
    cv.text(228, 350, "for", size=18, fill="#9FC0DE")
    modalities = [("TEXT", NAVY), ("IMAGE", PURPLE), ("VIDEO", CYAN), ("AUDIO", AMBER)]
    for i, (lab, col) in enumerate(modalities):
        x = 282 + i * 112
        cv.rect(x, 309, 96, 44, fill=WHITE, stroke=col, sw=2, rx=22)
        cv.text(x + 48, 337, lab, size=13.5, weight="bold", fill=col,
                anchor="middle")
    cv.text(744, 338, "×", size=25, weight="bold", fill="#9FC0DE",
            anchor="middle")
    for i, lab in enumerate(("UNDERSTAND", "GENERATE", "RETRIEVE")):
        x = 780 + i * 118
        cv.text(x, 335, lab, size=12.5, weight="bold",
                fill=WHITE if i != 2 else "#D2C1E8", anchor="middle")


def fig_flow(cv: Canvas):
    cv.text(0, 25, "A probability path replaces a causal chain",
            size=19, weight="bold", fill=INK)
    cv.text(1152, 25, "all positions move together", size=14,
            weight="bold", fill=RED, anchor="end")

    # A broad flow ribbon with three representative token states.
    cv.path("M 40 166 C 280 36, 520 282, 760 136 C 900 50, 1010 86, 1110 80",
            stroke="#D8E5F2", sw=60, opacity=0.9)
    cv.path("M 40 166 C 280 36, 520 282, 760 136 C 900 50, 1010 86, 1110 80",
            stroke=NAVY, sw=3.5, arrow="navy")
    anchors = [(64, 156, "t = 0", "noise"), (544, 207, "t = .5", "mixed"),
               (1062, 82, "t = 1", "data")]
    state_colors = [
        [GREY] * 8,
        [GREY, NAVY, GREY, PURPLE, CYAN, GREY, AMBER, NAVY],
        [NAVY, NAVY, PURPLE, PURPLE, CYAN, CYAN, AMBER, NAVY],
    ]
    for (x, y, tlabel, desc), colors in zip(anchors, state_colors):
        cv.circle(x, y, 42, fill=WHITE, stroke=NAVY, sw=2.2)
        for r in range(2):
            for c in range(4):
                cv.rect(x - 25 + c * 15, y - 17 + r * 18, 11, 11,
                        fill=colors[r * 4 + c], stroke=None, rx=2)
        cv.text(x, y + 62, tlabel, size=15, weight="bold", fill=NAVY,
                anchor="middle")
        cv.text(x, y + 82, desc, size=12.5, fill=GREY, anchor="middle")

    cv.rect(214, 102, 248, 72, fill=WHITE, stroke=RED, sw=1.7, rx=8)
    cv.text(338, 130, "predict kinetic velocity", size=15,
            weight="bold", fill=RED, anchor="middle")
    cv.math(338, 158, "v_t  →  p_{1|t}(x_1|x_t)", size=17, fill=INK,
            anchor="middle")
    cv.rect(712, 192, 242, 58, fill=WHITE, stroke=PURPLE, sw=1.7, rx=8)
    cv.text(833, 219, "correct every position", size=15,
            weight="bold", fill=PURPLE, anchor="middle")
    cv.text(833, 239, "with bidirectional context", size=13, fill=INK,
            anchor="middle")

    # Three large principles, visually connected to the ribbon.
    principles = [
        ("CORRUPT", "sample xₜ on a metric-induced path", RED, FILL_RED),
        ("PREDICT", "recover clean tokens at every position", PURPLE, FILL_PURPLE),
        ("REFINE", "iterate in parallel until t = 1", GREEN, FILL_GREEN),
    ]
    for i, (head, body, col, fill) in enumerate(principles):
        x = i * 392
        cv.rect(x, 286, 368, 96, fill=fill, stroke=col, sw=1.5, rx=8)
        cv.text(x + 22, 319, f"0{i + 1}  {head}", size=16,
                weight="bold", fill=col)
        cv.text(x + 22, 351, body, size=14.5, weight="bold", fill=INK)
        if i < 2:
            cv.arrow(x + 370, 334, x + 388, 334, color="navy", sw=2.1)


def fig_architecture(cv: Canvas):
    # Four modality ribbons feed one prominent backbone.
    cv.text(0, 23, "ENCODE ONCE", size=14, weight="bold", fill=GREY)
    modalities = [
        ("TEXT", NAVY, FILL_BLUE, "tokenizer"),
        ("IMAGE", PURPLE, FILL_PURPLE, "VQ codebook"),
        ("VIDEO", CYAN, FILL_CYAN, "VQ codebook"),
        ("AUDIO", AMBER, FILL_AMBER, "VQ codebook"),
    ]
    for i, (lab, col, fill, enc) in enumerate(modalities):
        y = 48 + i * 68
        cv.rect(0, y, 114, 46, fill=fill, stroke=col, sw=1.5, rx=23)
        cv.text(57, y + 29, lab, size=14, weight="bold", fill=col,
                anchor="middle")
        cv.arrow(120, y + 23, 162, y + 23, color="navy", sw=2)
        cv.text(176, y + 28, enc, size=13.5, weight="bold", fill=col)
        cv.path(f"M 286 {y + 23} C 338 {y + 23}, 350 184, 398 184",
                stroke=col, sw=3, opacity=0.7)

    cv.rect(410, 20, 348, 324, fill=FILL_BLUE, stroke=NAVY, sw=2.2, rx=12)
    cv.text(584, 56, "ONE DISCRETE-FLOW BACKBONE", size=21,
            weight="bold", fill=NAVY, anchor="middle")
    cv.text(584, 80, "Qwen2.5-7B initialization", size=13.5, fill=GREY,
            anchor="middle")
    for i in range(4):
        y = 104 + i * 50
        cv.rect(446, y, 276, 36, fill=WHITE, stroke=NAVY, sw=1.2, rx=6)
        cv.text(584, y + 23,
                "bidirectional multimodal self-attention" if i % 2 == 0
                else "shared feed-forward transformation",
                size=13.5, weight="bold", fill=NAVY, anchor="middle")
    cv.rect(446, 306, 276, 24, fill=NAVY, stroke=None, rx=5)
    cv.text(584, 322, "deep fusion at every layer", size=12.5,
            weight="bold", fill=WHITE, anchor="middle")

    cv.text(810, 23, "DECODE OR EMBED", size=14, weight="bold", fill=GREY)
    outputs = [
        ("LM HEAD", "text", NAVY, FILL_BLUE),
        ("VISION HEAD", "image · video", PURPLE, FILL_PURPLE),
        ("AUDIO HEAD", "speech · music", AMBER, FILL_AMBER),
        ("<EOS> FEATURE", "retrieval", GREEN, FILL_GREEN),
    ]
    for i, (head, body, col, fill) in enumerate(outputs):
        y = 48 + i * 68
        cv.path(f"M 758 184 C 800 184, 794 {y + 23}, 826 {y + 23}",
                stroke=col, sw=2.5, opacity=0.75)
        cv.rect(838, y, 192, 46, fill=fill, stroke=col, sw=1.5, rx=7)
        cv.text(854, y + 20, head, size=13.5, weight="bold", fill=col)
        cv.text(1014, y + 35, body, size=12.5, fill=INK, anchor="end")

    cv.rect(0, 358, 1152, 24, fill=FILL_GREY, stroke=GREY, sw=1.1, rx=6)
    cv.text(18, 375, "warmup", size=12.5, weight="bold", fill=GREY)
    cv.math(100, 375, "L_rec + L_sem", size=14, fill=INK)
    cv.text(410, 375, "joint flow training", size=12.5,
            weight="bold", fill=GREY)
    cv.math(560, 375, "λ₁L_CE + λ₂L^V_rec + λ₃L^A_rec",
            size=14, fill=INK)
    cv.text(1128, 375, "GradNorm balances the objectives", size=12.5,
            weight="bold", fill=NAVY, anchor="end")


def fig_efficiency(cv: Canvas):
    # Dominant center: dynamic block generation.
    cv.text(0, 25, "DYNAMIC RESPONSE", size=14, weight="bold", fill=RED)
    cv.text(0, 54, "Generate only as many blocks as the answer needs",
            size=19, weight="bold", fill=INK)
    cv.rect(0, 82, 684, 190, fill=WHITE, stroke=BORDER, sw=1.4, rx=9)
    rows = [
        ("step 1", 1, ".23", False),
        ("step 2", 2, ".45", False),
        ("step 3", 3, ".89", True),
    ]
    for r, (lab, blocks, conf, stop) in enumerate(rows):
        y = 106 + r * 52
        cv.text(24, y + 24, lab, size=13.5, weight="bold", fill=NAVY)
        for i in range(4):
            active = i < blocks
            cv.rect(102 + i * 92, y, 78, 34,
                    fill=FILL_BLUE_D if active else FILL_GREY,
                    stroke=NAVY if active else "#D9E0E7", sw=1.2, rx=5)
            if active:
                cv.text(141 + i * 92, y + 22, "block", size=12.5,
                        weight="bold", fill=NAVY, anchor="middle")
        cv.text(510, y + 22, f"EOS {conf}", size=13.5, weight="bold",
                fill=GREEN if stop else RED)
        cv.text(632, y + 22, "STOP" if stop else "EXPAND", size=13.5,
                weight="bold", fill=GREEN if stop else RED, anchor="end")
    cv.text(342, 254, "responses are padded only during training",
            size=13, fill=GREY, anchor="middle")

    # Right: cache matrix with clear updated diagonal.
    cv.text(730, 25, "ADAPTIVE CACHE", size=14, weight="bold", fill=GREEN)
    cv.text(730, 54, "Reuse features that barely move",
            size=19, weight="bold", fill=INK)
    cv.rect(730, 82, 422, 190, fill=WHITE, stroke=BORDER, sw=1.4, rx=9)
    for r in range(6):
        for c in range(11):
            changed = c >= 5 and (r * 2 + c) % 5 == 0
            fill = FILL_RED if changed else FILL_GREEN
            stroke = RED if changed else GREEN
            cv.rect(756 + c * 32, 104 + r * 24, 25, 18, fill=fill,
                    stroke=stroke, sw=.8, rx=3)
    cv.text(756, 262, "instruction: cached throughout", size=12.5,
            weight="bold", fill=GREEN)
    cv.text(1126, 262, "response: update only when needed", size=12.5,
            weight="bold", fill=RED, anchor="end")

    # Bottom KPI band: larger and cleaner.
    metrics = [
        ("1.4×", "training efficiency", "single-modality batches",
         NAVY, FILL_BLUE),
        ("1.2×", "response speed vs AR", "parallel decode + cache",
         GREEN, FILL_GREEN),
        ("64", "token block size", "dynamic expansion",
         AMBER, FILL_AMBER),
    ]
    for i, (value, head, body, col, fill) in enumerate(metrics):
        x = i * 392
        cv.rect(x, 296, 368, 86, fill=fill, stroke=col, sw=1.5, rx=8)
        cv.text(x + 74, 350, value, size=31, weight="bold", fill=col,
                anchor="middle")
        cv.text(x + 148, 329, head, size=14.5, weight="bold", fill=INK)
        cv.text(x + 148, 356, body, size=13, fill=GREY)


def fig_results(cv: Canvas):
    # Each result is a strong baseline-to-ours slope rather than a dense chart.
    results = [
        ("OMNIMODAL\nUNDERSTANDING", "OpenOmni", 36.5, 39.7, "+3.2",
         NAVY, FILL_BLUE, "Table 1"),
        ("MULTI-TURN\nVISION", "Anole", 50.4, 55.0, "+4.6",
         PURPLE, FILL_PURPLE, "Table 2"),
        ("CROSS-MODAL\nRETRIEVAL", "MMaDA", 31.8, 32.9, "+1.1",
         GREEN, FILL_GREEN, "Table 4"),
    ]
    for i, (head, baseline, before, after, delta, col, fill, source) in enumerate(results):
        x = i * 392
        cv.text(x + 8, 24, head, size=16, weight="bold", fill=col)
        cv.text(x + 350, 24, source, size=12, weight="bold", fill=GREY,
                anchor="end")
        cv.rect(x, 52, 368, 244, fill=WHITE, stroke=BORDER, sw=1.4, rx=9)
        # Baseline and ours towers, joined by an upward slope.
        base_h = 90
        ours_h = 90 + (after - before) * 13
        cv.rect(x + 54, 236 - base_h, 82, base_h, fill=FILL_GREY,
                stroke=GREY, sw=1.3, rx=5)
        cv.rect(x + 226, 236 - ours_h, 82, ours_h, fill=fill,
                stroke=col, sw=2, rx=5)
        cv.path(f"M {x + 136} {236 - base_h} L {x + 226} {236 - ours_h}",
                stroke=col, sw=3, arrow="navy" if col == NAVY else None)
        cv.text(x + 95, 132, f"{before:.1f}", size=20, weight="bold",
                fill=GREY, anchor="middle")
        cv.text(x + 267, 236 - ours_h - 14, f"{after:.1f}", size=23,
                weight="bold", fill=col, anchor="middle")
        cv.text(x + 95, 262, baseline, size=13.5, weight="bold",
                fill=GREY, anchor="middle")
        cv.text(x + 267, 262, "NExT-OMNI", size=13.5, weight="bold",
                fill=col, anchor="middle")
        cv.circle(x + 184, 101, 34, fill=fill, stroke=col, sw=1.6)
        cv.text(x + 184, 109, delta, size=20, weight="bold", fill=col,
                anchor="middle")

    cv.rect(0, 318, 1152, 64, fill=NAVY, stroke=NAVY, sw=1.5, rx=8)
    cv.text(576, 347, "One representation transfers beyond generation",
            size=14, weight="bold", fill="#9FC0DE", anchor="middle")
    cv.text(576, 371,
            "bidirectional correction + deep fusion benefit every evaluated task family",
            size=17, weight="bold", fill=WHITE, anchor="middle")


def fig_takeaway(cv: Canvas):
    # Left: ablation as a staircase.
    cv.text(0, 24, "THE ABLATION BUILDS A CAUSAL STORY",
            size=15, weight="bold", fill=NAVY)
    values = [41.4, 42.6, 43.0, 43.9, 45.6]
    labels = ["AR\nsplit", "DFM\nsplit", "DFM\nunified", "+ dynamic\nlength",
              "+ recon." ]
    cols = [GREY, NAVY, PURPLE, AMBER, GREEN]
    fills = [FILL_GREY, FILL_BLUE, FILL_PURPLE, FILL_AMBER, FILL_GREEN]
    x0, base = 18, 286
    pts = []
    for i, (val, lab, col, fill) in enumerate(zip(values, labels, cols, fills)):
        x = x0 + i * 118
        y = base - (val - 40) * 24
        cv.rect(x, y, 92, base - y, fill=fill, stroke=col, sw=1.5, rx=5)
        cv.text(x + 46, y - 12, f"{val:.1f}", size=16, weight="bold",
                fill=col, anchor="middle")
        rows = lab.split("\n")
        for j, row in enumerate(rows):
            cv.text(x + 46, base + 22 + j * 17, row, size=12.5,
                    weight="bold", fill=col, anchor="middle")
        pts.append((x + 46, y))
    cv.path("M " + " L ".join(f"{x} {y}" for x, y in pts),
            stroke=GREEN, sw=2.8, arrow="green")
    cv.text(302, 365, "+4.2 average points", size=15, weight="bold",
            fill=GREEN, anchor="middle")

    # Right: four principles, visually stacked as the final recipe.
    cv.text(650, 24, "THE FINAL RECIPE", size=15, weight="bold", fill=NAVY)
    recipe = [
        ("1", "Discrete flow", "correct globally", NAVY, FILL_BLUE),
        ("2", "Unified representation", "fuse deeply", PURPLE, FILL_PURPLE),
        ("3", "Dynamic length", "answer naturally", AMBER, FILL_AMBER),
        ("4", "Reconstruction", "keep fine detail", GREEN, FILL_GREEN),
    ]
    for i, (num, head, body, col, fill) in enumerate(recipe):
        y = 48 + i * 66
        cv.circle(676, y + 22, 20, fill=col, stroke=None)
        cv.text(676, y + 29, num, size=17, weight="bold", fill=WHITE,
                anchor="middle")
        cv.rect(710, y, 420, 44, fill=fill, stroke=col, sw=1.4, rx=7)
        cv.text(728, y + 19, head, size=15, weight="bold", fill=col)
        cv.text(1108, y + 28, body, size=13.5, weight="bold", fill=INK,
                anchor="end")

    cv.rect(650, 324, 480, 58, fill=FILL_GREY, stroke=GREY, sw=1.3, rx=8)
    cv.text(670, 347, "NEXT", size=13, weight="bold", fill=AMBER)
    cv.text(730, 347, "action trajectories · physical-AI video",
            size=14.5, weight="bold", fill=INK)
    cv.text(670, 370, "SCOPE", size=13, weight="bold", fill=RED)
    cv.text(730, 370, "paper reports benchmark breadth, not deployed safety",
            size=13.5, fill=INK)
