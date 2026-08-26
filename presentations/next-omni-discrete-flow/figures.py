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
