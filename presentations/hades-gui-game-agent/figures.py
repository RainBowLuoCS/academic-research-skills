"""Editable reference-style SVG figures for the Hades GUI-agent talk."""

from content import FACTS
from svgkit import (
    AMBER, FILL_AMBER, FILL_BLUE, FILL_BLUE_D, FILL_GREEN, FILL_GREY,
    FILL_RED, GREEN, GREY, INK, MUTED, NAVY, RED, WHITE, Canvas,
)

BORDER = "#C9D6E4"
PURPLE = "#7651A8"
FILL_PURPLE = "#EEE8F6"
CYAN = "#1889A6"
FILL_CYAN = "#DDF2F6"


def screen(cv, x, y, w, h, accent=NAVY):
    cv.rect(x, y, w, h, fill="#EAF0F5", stroke=GREY, sw=1.2, rx=4)
    cv.circle(x + w * .25, y + h * .28, min(w, h) * .09,
              fill=FILL_AMBER, stroke=AMBER, sw=.9)
    cv.poly([(x + 5, y + h - 6), (x + w * .36, y + h * .46),
             (x + w * .56, y + h - 6)], fill=FILL_BLUE_D,
            stroke=NAVY, sw=.9)
    cv.poly([(x + w * .42, y + h - 6), (x + w * .72, y + h * .30),
             (x + w - 5, y + h - 6)], fill=FILL_PURPLE,
            stroke=PURPLE, sw=.9)
    cv.rect(x, y + h - 6, w, 6, fill=accent, stroke=None)


def key(cv, x, y, label, color=NAVY, fill=WHITE, size=13):
    cv.rect(x, y, 38, 32, fill=fill, stroke=color, sw=1.2, rx=5)
    cv.text(x + 19, y + 21, label, size=size, weight="bold", fill=color,
            anchor="middle")


def block(cv, x, y, w, text, color=NAVY, fill=FILL_BLUE, size=13):
    cv.rect(x, y, w, 38, fill=fill, stroke=color, sw=1.3, rx=5)
    cv.text(x + w / 2, y + 24, text, size=size, weight="bold", fill=color,
            anchor="middle")


def fig_title_motif(cv: Canvas):
    # A screen stream becomes keyboard/mouse actions and a long memory trace.
    for i in range(5):
        x = 760 + i * 78
        screen(cv, x, 48 + i * 24, 64, 46,
               [NAVY, PURPLE, CYAN, AMBER, GREEN][i])
        if i < 4:
            cv.path(f"M {x + 64} {71 + i * 24} C {x + 72} {71 + i * 24}, "
                    f"{x + 74} {95 + i * 24}, {x + 80} {95 + i * 24}",
                    stroke=WHITE, sw=1.5, opacity=.45)
    cv.path("M 770 224 C 880 188, 1000 282, 1180 232",
            stroke="#8DB1D2", sw=3, opacity=.55)
    for i, lab in enumerate(("W", "A", "S", "D", "F", "↖")):
        x = 840 + i * 56
        cv.rect(x, 260 + (i % 2) * 18, 34, 28, fill=WHITE,
                stroke="#8DB1D2", sw=1, rx=4, opacity=.28 + i * .07)
        cv.text(x + 17, 279 + (i % 2) * 18, lab, size=12,
                weight="bold", fill=WHITE, anchor="middle")
    cv.text(1238, 334, "screen  →  reason  →  act  →  remember",
            size=14.5, weight="bold", fill="#8DB1D2", anchor="end")


def fig_problem(cv: Canvas):
    # Three visual examples of what commercial-game agents must coordinate.
    cards = [
        ("3D perception", "partial observation", NAVY),
        ("GUI operation", "menus · inventory · maps", PURPLE),
        ("long-horizon control", "quests · combat · recovery", AMBER),
    ]
    for i, (head, sub, col) in enumerate(cards):
        x = i * 392
        cv.text(x + 184, 18, head, size=15.5, weight="bold",
                fill=INK, anchor="middle")
        cv.rect(x + 24, 38, 320, 126, fill=WHITE, stroke=BORDER,
                sw=1.2, rx=5)
        if i == 0:
            screen(cv, x + 52, 58, 132, 82, col)
            cv.path(f"M {x + 196} 118 C {x + 230} 90, {x + 268} 82, {x + 310} 70",
                    stroke=RED, sw=2, dash="5 4")
            cv.circle(x + 306, 70, 7, fill=RED, stroke=WHITE, sw=1)
        elif i == 1:
            cv.rect(x + 54, 56, 250, 90, fill=FILL_GREY,
                    stroke=GREY, sw=1, rx=4)
            for r in range(2):
                for c in range(4):
                    cv.rect(x + 70 + c * 54, 70 + r * 34, 42, 25,
                            fill=FILL_PURPLE if (r + c) % 3 == 0 else WHITE,
                            stroke=PURPLE if (r + c) % 3 == 0 else GREY,
                            sw=.8, rx=3)
            cv.path(f"M {x + 286} 124 L {x + 298} 146 L {x + 278} 140 Z",
                    fill=INK, stroke=WHITE, sw=1)
        else:
            pts = [(x + 50 + j * 42, 118 - (j % 3) * 22) for j in range(7)]
            cv.path("M " + " L ".join(f"{a} {b}" for a, b in pts),
                    stroke=col, sw=2.5)
            for j, (a, b) in enumerate(pts):
                cv.circle(a, b, 8, fill=FILL_AMBER, stroke=col, sw=1.3)
                cv.text(a, b + 4, str(j + 1), size=9.5, weight="bold",
                        fill=col, anchor="middle")
        cv.text(x + 184, 188, sub, size=13.5, weight="bold",
                fill=col, anchor="middle")

    # Unified non-invasive interaction loop.
    cv.text(0, 230, "No privileged game API", size=15,
            weight="bold", fill=RED)
    screen(cv, 40, 252, 142, 92, NAVY)
    cv.text(111, 368, "screen pixels", size=13.5,
            weight="bold", fill=NAVY, anchor="middle")
    cv.arrow(196, 298, 282, 298, color="navy", sw=2.3)
    cv.rect(300, 244, 300, 108, fill=FILL_BLUE, stroke=NAVY,
            sw=1.7, rx=8)
    cv.text(450, 280, "HADES", size=22, weight="bold",
            fill=NAVY, anchor="middle")
    cv.text(450, 307, "perception · memory · reasoning", size=14,
            weight="bold", fill=INK, anchor="middle")
    cv.text(450, 331, "one VLA policy", size=13.5, fill=GREY,
            anchor="middle")
    cv.arrow(614, 298, 700, 298, color="navy", sw=2.3)
    for i, lab in enumerate(("W", "A", "S", "D")):
        key(cv, 724 + (i % 3) * 46, 270 + (i // 3) * 38, lab)
    cv.path("M 894 270 C 932 264, 948 286, 934 330 C 916 364, 874 348, "
            "878 310 C 880 286, 884 274, 894 270 Z",
            fill=WHITE, stroke=PURPLE, sw=1.8)
    cv.line(906, 274, 906, 307, stroke=PURPLE, sw=1.4)
    cv.text(1032, 304, "device-level\naction space", size=16,
            weight="bold", fill=PURPLE, anchor="middle")


def fig_pretraining(cv: Canvas):
    # Main trajectory reconstruction: 5 Hz visual decisions, 30 Hz actions.
    cv.text(0, 18, "Decouple visual and action time scales",
            size=16, weight="bold", fill=INK)
    cv.text(1152, 18, "one decision window = 200 ms",
            size=13.5, weight="bold", fill=NAVY, anchor="end")
    screen(cv, 18, 46, 112, 72, NAVY)
    cv.arrow(140, 82, 202, 82, color="navy", sw=2)
    cv.rect(216, 40, 918, 84, fill="#F6F8FA", stroke=BORDER,
            sw=1.2, rx=6)
    for i in range(6):
        x = 238 + i * 142
        cv.rect(x, 58, 118, 40, fill=FILL_BLUE if i % 2 == 0 else WHITE,
                stroke=NAVY, sw=1.1, rx=4)
        cv.text(x + 59, 82, f"K{i + 1} · 33 ms", size=13,
                weight="bold", fill=NAVY, anchor="middle")
        if i < 5:
            cv.arrow(x + 120, 78, x + 138, 78, color="grey", sw=1.3)
    cv.text(676, 115, "≈ 30 Hz low-level keyboard–mouse control",
            size=13.5, weight="bold", fill=GREY, anchor="middle")

    cv.rect(0, 146, 1152, 54, fill=WHITE, stroke=NAVY, sw=1.3, rx=5)
    cv.text(18, 169, "Unified action token", size=13.5,
            weight="bold", fill=NAVY)
    cv.text(186, 181,
            "<action_start> ΔX ΔY ΔZ ; K1 ; K2 ; K3 ; K4 ; K5 ; K6 <action_end>",
            size=17, weight="bold", fill=INK)

    # Three debiasing/decoding mechanisms, reference-style.
    cv.text(0, 238, "Key Shuffle", size=15, weight="bold", fill=INK)
    for i, lab in enumerate(("W", "A", "S", "D")):
        key(cv, 10 + i * 48, 260, lab, NAVY, FILL_BLUE)
    cv.arrow(210, 276, 258, 276, color="red", sw=1.8)
    for i, lab in enumerate(("D", "S", "W", "A")):
        key(cv, 274 + i * 48, 260, lab, RED, FILL_RED)
    cv.text(224, 330, "same function · shuffled physical key",
            size=12.5, weight="bold", fill=RED, anchor="middle")

    cv.line(480, 220, 480, 360, stroke="#D6DEE7", sw=1.2, dash="5 5")
    cv.text(514, 238, "Time-aware loss decay", size=15,
            weight="bold", fill=INK)
    ax, ay, aw, ah = 524, 258, 220, 70
    cv.line(ax, ay + ah, ax + aw, ay + ah, stroke=GREY, sw=1)
    cv.line(ax, ay, ax, ay + ah, stroke=GREY, sw=1)
    pts = []
    for i in range(9):
        val = FACTS["loss_decay"] ** i
        pts.append((ax + i * aw / 8, ay + ah - val * ah))
    cv.path("M " + " L ".join(f"{a:.1f} {b:.1f}" for a, b in pts),
            stroke=RED, sw=2.3)
    cv.text(634, 350, "ωₜ = 0.9ᵏ⁻¹", size=14,
            weight="bold", fill=RED, anchor="middle")

    cv.line(790, 220, 790, 360, stroke="#D6DEE7", sw=1.2, dash="5 5")
    cv.text(824, 238, "Mouse inversion", size=15,
            weight="bold", fill=INK)
    jagged = [(824, 308), (862, 270), (900, 322), (938, 258), (976, 304)]
    smooth = [(824, 318), (862, 300), (900, 286), (938, 276), (976, 270),
              (1014, 266), (1052, 264), (1090, 262)]
    cv.path("M " + " L ".join(f"{a} {b}" for a, b in jagged),
            stroke=GREY, sw=1.5, dash="5 4")
    cv.path("M " + " C ".join(
        [f"{smooth[0][0]} {smooth[0][1]}"] +
        [f"{a-16} {b+5}, {a-4} {b}, {a} {b}" for a, b in smooth[1:]]
    ), stroke=GREEN, sw=2.3)
    cv.text(960, 350, "Kalman smoothing · 5 Hz → 30 Hz",
            size=12.5, weight="bold", fill=GREEN, anchor="middle")


def fig_thinking(cv: Canvas):
    # Sparse decision timeline.
    cv.text(0, 18, "Most steps execute; a few steps decide",
            size=16, weight="bold", fill=INK)
    events = [
        ("move", "∅", NAVY), ("move", "∅", NAVY),
        ("path blocked", "current decision", RED),
        ("combat", "∅", NAVY), ("subgoal done", "memory summary", PURPLE),
        ("move", "∅", NAVY), ("new UI", "current decision", RED),
    ]
    for i, (state, think, col) in enumerate(events):
        x = 8 + i * 162
        screen(cv, x, 48, 116, 70, col)
        cv.text(x + 58, 138, state, size=12.5, weight="bold",
                fill=col, anchor="middle")
        cv.rect(x, 154, 116, 36,
                fill=FILL_GREY if think == "∅" else
                (FILL_RED if think == "current decision" else FILL_PURPLE),
                stroke=GREY if think == "∅" else col, sw=1.1, rx=4)
        cv.text(x + 58, 177, think, size=11.5, weight="bold",
                fill=GREY if think == "∅" else col, anchor="middle")
        if i < 6:
            cv.arrow(x + 118, 82, x + 156, 82, color="grey", sw=1.2)
    cv.text(576, 216,
            "rₜ ∈ { ∅, current decision, memory summary }",
            size=18, weight="bold", fill=NAVY, anchor="middle")

    # Dual memory queues.
    cv.text(0, 254, "Two timescales of memory", size=16,
            weight="bold", fill=INK)
    cv.rect(8, 278, 520, 72, fill=WHITE, stroke=NAVY, sw=1.3, rx=6)
    cv.text(24, 302, "SHORT-TERM HISTORY", size=13.5,
            weight="bold", fill=NAVY)
    for i in range(6):
        cv.rect(190 + i * 50, 292, 40, 30, fill=FILL_BLUE,
                stroke=NAVY, sw=.9, rx=3)
        cv.text(210 + i * 50, 312, ["V", "A", "V", "A", "r", "A"][i],
                size=12, weight="bold", fill=NAVY, anchor="middle")
    cv.text(24, 335, "recent pixels · actions · local decisions",
            size=12.5, fill=GREY)

    cv.arrow(538, 314, 610, 314, color="red", sw=2)
    cv.text(574, 304, "compact", size=12, weight="bold",
            fill=RED, anchor="middle")
    cv.rect(624, 278, 528, 72, fill=WHITE, stroke=PURPLE,
            sw=1.3, rx=6)
    cv.text(640, 302, "LONG-TERM MEMORY", size=13.5,
            weight="bold", fill=PURPLE)
    cv.text(816, 303,
            "stage · completed goals · failures · locations · future plan",
            size=13, weight="bold", fill=INK)
    cv.text(640, 335, "text summaries carry state across context windows",
            size=12.5, fill=GREY)
    cv.math(576, 380,
            "πθ(rₜ, aₜ | instruction, memoryₜ, historyₜ)",
            size=17, fill=INK, anchor="middle")


def fig_rl(cv: Canvas):
    # Failure case: one enormous rollout.
    cv.text(0, 18, "Naïve rollout-level RL", size=16,
            weight="bold", fill=INK)
    cv.text(1152, 18, "context overflow · sparse terminal reward",
            size=13.5, weight="bold", fill=RED, anchor="end")
    for i in range(18):
        x = 12 + i * 61
        cv.rect(x, 48, 48, 26, fill=FILL_GREY, stroke=GREY, sw=.8, rx=3)
        if i < 17:
            cv.line(x + 48, 61, x + 61, 61, stroke=GREY, sw=1)
    cv.path("M 12 86 L 1110 86", stroke=RED, sw=2, dash="7 5")
    cv.text(576, 106, "one minute already exceeds typical language-task scale",
            size=13.5, weight="bold", fill=RED, anchor="middle")

    cv.text(0, 144, "TA-GRPO: segment, remember, reward locally",
            size=16, weight="bold", fill=INK)
    seg_cols = [NAVY, PURPLE, AMBER]
    for g, col in enumerate(seg_cols):
        x = 16 + g * 376
        cv.rect(x, 174, 326, 112, fill=WHITE, stroke=col,
                sw=1.5, rx=7)
        cv.text(x + 16, 198, f"SEGMENT {g + 1}", size=13.5,
                weight="bold", fill=col)
        for i in range(5):
            cv.rect(x + 18 + i * 56, 216, 44, 28,
                    fill=[FILL_BLUE, FILL_PURPLE, FILL_AMBER][g],
                    stroke=col, sw=.8, rx=3)
        cv.text(x + 20, 272, "verify  +  α · PRM", size=13,
                weight="bold", fill=INK)
        cv.circle(x + 278, 263, 18, fill=FILL_GREEN, stroke=GREEN, sw=1.1)
        cv.text(x + 278, 269, f"R{g + 1}", size=12.5,
                weight="bold", fill=GREEN, anchor="middle")
        if g < 2:
            cv.arrow(x + 330, 230, x + 366, 230, color="navy", sw=1.8)
            cv.text(x + 348, 218, "memory", size=11,
                    weight="bold", fill=NAVY, anchor="middle")

    cv.text(0, 326, "Time-aware credit inside each segment",
            size=15, weight="bold", fill=INK)
    for i in range(9):
        alpha = .18 + i * .09
        cv.rect(18 + i * 72, 344, 56, 28, fill=GREEN, stroke=None,
                rx=3, opacity=min(alpha, .95))
        cv.text(46 + i * 72, 363, f"t{i}", size=11,
                weight="bold", fill=WHITE if alpha > .55 else GREEN,
                anchor="middle")
    cv.arrow(670, 358, 790, 358, color="green", sw=2)
    cv.math(968, 365, "A_{g,t} = β^{T_g−1−t} A_g",
            size=20, fill=INK, anchor="middle")


def fig_inference(cv: Canvas):
    # Environment and streaming action overlap.
    cv.text(0, 18, "Streaming action generation", size=16,
            weight="bold", fill=INK)
    screen(cv, 18, 48, 122, 82, NAVY)
    cv.text(79, 154, "game client", size=13,
            weight="bold", fill=NAVY, anchor="middle")
    cv.arrow(150, 90, 218, 90, color="navy", sw=2)
    cv.rect(232, 46, 302, 88, fill=FILL_BLUE, stroke=NAVY,
            sw=1.5, rx=7)
    cv.text(383, 77, "Streaming-vLLM", size=18,
            weight="bold", fill=NAVY, anchor="middle")
    cv.text(383, 105, "decode K1 → execute K1 → decode K2 …",
            size=13.5, weight="bold", fill=INK, anchor="middle")
    for i in range(6):
        x = 572 + i * 86
        cv.rect(x, 54, 68, 32, fill=FILL_BLUE if i < 3 else WHITE,
                stroke=NAVY, sw=1, rx=4)
        cv.text(x + 34, 75, f"K{i + 1}", size=12.5,
                weight="bold", fill=NAVY, anchor="middle")
        cv.rect(x, 102, 68, 24, fill=FILL_GREEN if i < 2 else FILL_GREY,
                stroke=GREEN if i < 2 else GREY, sw=.8, rx=3)
        cv.text(x + 34, 119, "run" if i < 2 else "wait", size=10.5,
                weight="bold", fill=GREEN if i < 2 else GREY,
                anchor="middle")
    cv.text(826, 154, "generation overlaps environment execution",
            size=13, weight="bold", fill=RED, anchor="middle")

    # Logical and physical cache views.
    cv.text(0, 202, "Long context without recomputation", size=16,
            weight="bold", fill=INK)
    cv.text(26, 238, "logical window", size=13.5,
            weight="bold", fill=GREY)
    logical = [1, 2, 3, 4, 5, 6, 7, 8]
    for i, n in enumerate(logical):
        x = 154 + i * 58
        cv.rect(x, 220, 46, 36, fill=FILL_BLUE if n > 2 else FILL_GREY,
                stroke=NAVY if n > 2 else GREY, sw=1, rx=4)
        cv.text(x + 23, 244, str(n), size=12.5,
                weight="bold", fill=NAVY if n > 2 else GREY,
                anchor="middle")
    cv.arrow(628, 238, 704, 238, color="navy", sw=2)
    cv.text(666, 226, "slide", size=11.5,
            weight="bold", fill=NAVY, anchor="middle")
    for i, n in enumerate((3, 4, 5, 6, 7, 8, 9, 10)):
        x = 720 + i * 50
        cv.rect(x, 220, 40, 36, fill=FILL_BLUE,
                stroke=NAVY, sw=1, rx=4)
        cv.text(x + 20, 244, str(n), size=12.5,
                weight="bold", fill=NAVY, anchor="middle")

    cv.text(26, 292, "physical KV", size=13.5,
            weight="bold", fill=GREY)
    for i in range(12):
        x = 154 + i * 74
        kept = i in (2, 3, 4, 5, 6, 7)
        cv.rect(x, 274, 58, 34,
                fill=FILL_GREEN if kept else FILL_GREY,
                stroke=GREEN if kept else GREY, sw=1, rx=4)
        cv.text(x + 29, 297, "reuse" if kept else "free",
                size=11.5, weight="bold",
                fill=GREEN if kept else GREY, anchor="middle")
    cv.text(576, 330,
            "block lookup · RoPE refresh · CUDA Graph · action-aware speculation",
            size=13.5, weight="bold", fill=GREY, anchor="middle")

    cv.rect(160, 344, 330, 38, fill=WHITE, stroke=NAVY, sw=1.4, rx=5)
    cv.text(325, 369, ">20× vs standard vLLM",
            size=16, weight="bold", fill=NAVY, anchor="middle")
    cv.rect(662, 344, 330, 38, fill=WHITE, stroke=GREEN, sw=1.4, rx=5)
    cv.text(827, 369, ">30 Hz action prediction",
            size=16, weight="bold", fill=GREEN, anchor="middle")


def fig_flywheel(cv: Canvas):
    # Multi-source data enters four training stores.
    cv.text(0, 18, "Unified raw format", size=16,
            weight="bold", fill=INK)
    cv.math(0, 48, "τ = (o₁, a₁, o₂, a₂, …, o_T, a_T)",
            size=20, fill=NAVY)
    sources = [
        ("public video", NAVY, FILL_BLUE),
        ("expert recording", PURPLE, FILL_PURPLE),
        ("agent rollout", AMBER, FILL_AMBER),
    ]
    for i, (lab, col, fill) in enumerate(sources):
        y = 78 + i * 64
        cv.rect(0, y, 190, 40, fill=fill, stroke=col, sw=1.2, rx=5)
        cv.text(95, y + 25, lab, size=13.5,
                weight="bold", fill=col, anchor="middle")
        cv.arrow(198, y + 20, 256, 174, color="grey", sw=1.4)

    # Central flywheel.
    cv.circle(454, 174, 92, fill=WHITE, stroke=NAVY, sw=1.8)
    cv.circle(454, 174, 58, fill=FILL_BLUE, stroke=NAVY, sw=1.5)
    cv.text(454, 166, "HADES", size=19, weight="bold",
            fill=NAVY, anchor="middle")
    cv.text(454, 190, "policy", size=14, weight="bold",
            fill=INK, anchor="middle")
    stores = [
        (454, 46, "CPT", NAVY, FILL_BLUE),
        (598, 174, "SFT / RL", PURPLE, FILL_PURPLE),
        (454, 302, "PRM", RED, FILL_RED),
        (310, 174, "verify", GREEN, FILL_GREEN),
    ]
    for x, y, lab, col, fill in stores:
        cv.rect(x - 50, y - 19, 100, 38, fill=fill, stroke=col,
                sw=1.2, rx=5)
        cv.text(x, y + 5, lab, size=13.5, weight="bold",
                fill=col, anchor="middle")
    cv.path("M 454 66 C 548 72, 588 100, 598 155", stroke=NAVY,
            sw=2, arrow="navy")
    cv.path("M 598 193 C 590 258, 530 298, 504 302", stroke=PURPLE,
            sw=2)
    cv.path("M 404 302 C 340 286, 310 238, 310 193", stroke=RED, sw=2)
    cv.path("M 310 155 C 320 96, 382 72, 454 66", stroke=GREEN, sw=2)

    # Scalable environment and honest evidence boundary.
    cv.line(718, 8, 718, 330, stroke="#D6DEE7",
            sw=1.2, dash="5 5")
    cv.text(752, 18, "Industrial execution loop", size=16,
            weight="bold", fill=INK)
    for r in range(4):
        for c in range(5):
            x, y = 760 + c * 70, 56 + r * 54
            cv.rect(x, y, 54, 38, fill=FILL_GREY,
                    stroke=GREY, sw=.9, rx=4)
            cv.text(x + 27, y + 23, "game", size=11.5,
                    weight="bold", fill=GREY, anchor="middle")
    cv.text(928, 286, "100+ parallel workers",
            size=15, weight="bold", fill=NAVY, anchor="middle")
    cv.text(928, 312, "checker + model judger",
            size=13.5, weight="bold", fill=GREEN, anchor="middle")

    cv.rect(0, 344, 1152, 38, fill=WHITE, stroke=RED,
            sw=1.2, rx=5)
    cv.text(18, 369, "MATERIAL BOUNDARY", size=12.5,
            weight="bold", fill=RED)
    cv.text(170, 369,
            "the supplied PDF states near-human / SOTA results but includes no benchmark tables to verify them",
            size=13.5, weight="bold", fill=INK)


# ------------------------------------------------------ paper-specific detail
# Final overrides: redraw Figures 1–4 at presentation scale with the paper's
# exact mechanisms rather than generic architecture cards.

def fig_problem(cv: Canvas):
    # Richer commercial-game task strip.
    tasks = [
        ("WORLD", "navigate 3D space", NAVY),
        ("COMBAT", "react and strategize", RED),
        ("GUI", "operate nested menus", PURPLE),
        ("QUEST", "preserve state for hours", AMBER),
    ]
    for i, (head, sub, col) in enumerate(tasks):
        x = i * 288
        cv.text(x + 132, 16, head, size=14, weight="bold", fill=col,
                anchor="middle")
        cv.rect(x + 10, 32, 244, 116, fill=WHITE, stroke=BORDER, sw=1.2, rx=5)
        if i == 0:
            screen(cv, x + 26, 48, 118, 78, col)
            cv.path(f"M {x+154} 118 C {x+178} 96, {x+196} 72, {x+234} 62",
                    stroke=col, sw=2, dash="5 4")
            cv.circle(x + 230, 64, 6, fill=col, stroke=WHITE, sw=1)
        elif i == 1:
            cv.circle(x + 72, 88, 24, fill=FILL_RED, stroke=RED, sw=1.3)
            cv.circle(x + 192, 88, 24, fill=FILL_BLUE, stroke=NAVY, sw=1.3)
            cv.path(f"M {x+96} 88 L {x+168} 88", stroke=RED, sw=3)
            cv.text(x + 132, 64, "HP", size=12, weight="bold", fill=RED,
                    anchor="middle")
            cv.rect(x + 76, 122, 112, 7, fill=FILL_RED, stroke=RED, sw=.8)
            cv.rect(x + 76, 122, 74, 7, fill=GREEN, stroke=None)
        elif i == 2:
            for r in range(2):
                for c in range(4):
                    active = (r, c) in ((0, 1), (1, 3))
                    cv.rect(x + 30 + c * 51, 54 + r * 40, 40, 29,
                            fill=FILL_PURPLE if active else FILL_GREY,
                            stroke=PURPLE if active else GREY, sw=.9, rx=3)
            cv.path(f"M {x+218} 116 L {x+230} 140 L {x+210} 132 Z",
                    fill=INK, stroke=WHITE, sw=1)
        else:
            pts = [(x + 30 + j * 34, 116 - (j % 3) * 25) for j in range(7)]
            cv.path("M " + " L ".join(f"{a} {b}" for a, b in pts),
                    stroke=col, sw=2.2)
            for j, (a, b) in enumerate(pts):
                cv.circle(a, b, 7, fill=FILL_AMBER, stroke=col, sw=1)
                cv.text(a, b + 3, str(j + 1), size=8.5, weight="bold",
                        fill=col, anchor="middle")
        cv.text(x + 132, 174, sub, size=13, weight="bold", fill=INK,
                anchor="middle")

    # Capability coupling diagram.
    cv.text(0, 216, "One task couples four systems", size=16,
            weight="bold", fill=INK)
    centers = [
        (174, 286, "PERCEIVE", "screen only", NAVY, FILL_BLUE),
        (442, 286, "REASON", "sparse decisions", RED, FILL_RED),
        (710, 286, "REMEMBER", "cross-context state", PURPLE, FILL_PURPLE),
        (978, 286, "CONTROL", "keyboard + mouse", AMBER, FILL_AMBER),
    ]
    for i, (x, y, head, body, col, fill) in enumerate(centers):
        cv.circle(x, y, 48, fill=fill, stroke=col, sw=1.6)
        cv.text(x, y - 2, head, size=14, weight="bold", fill=col,
                anchor="middle")
        cv.text(x, y + 20, body, size=11.5, fill=INK, anchor="middle")
        if i < 3:
            cv.arrow(x + 50, y, centers[i + 1][0] - 50, y,
                     color="navy", sw=2)
    cv.path("M 978 340 C 852 384, 292 384, 174 340",
            stroke=GREEN, sw=2, dash="7 5", arrow="green")
    cv.text(576, 370, "environment feedback closes the loop",
            size=13.5, weight="bold", fill=GREEN, anchor="middle")


def fig_pretraining(cv: Canvas):
    # Figure 1 left: raw video/action reconstruction at two temporal scales.
    cv.text(0, 18, "Raw interaction trajectory", size=15.5,
            weight="bold", fill=INK)
    cv.text(1152, 18, "visual 5 Hz · action 30 Hz",
            size=13.5, weight="bold", fill=NAVY, anchor="end")
    for t in range(4):
        x = 14 + t * 278
        screen(cv, x, 42, 96, 62, [NAVY, PURPLE, CYAN, AMBER][t])
        cv.text(x + 48, 122, f"o{t + 1}", size=13,
                weight="bold", fill=NAVY, anchor="middle")
        cv.arrow(x + 106, 73, x + 144, 73, color="navy", sw=1.5)
        for k in range(6):
            bx = x + 150 + (k % 3) * 38
            by = 42 + (k // 3) * 34
            cv.rect(bx, by, 30, 27,
                    fill=FILL_BLUE if (t + k) % 3 else FILL_RED,
                    stroke=NAVY if (t + k) % 3 else RED, sw=.8, rx=3)
            cv.text(bx + 15, by + 18,
                    ["W", "A", "∅", "D", "F", "↖"][(t + k) % 6],
                    size=10.5, weight="bold",
                    fill=NAVY if (t + k) % 3 else RED, anchor="middle")
        cv.text(x + 190, 122, f"a{t + 1}: 6 chunks",
                size=12, weight="bold", fill=GREY, anchor="middle")
        if t < 3:
            cv.arrow(x + 264, 80, x + 276, 80, color="grey", sw=1.2)

    cv.rect(0, 144, 1152, 44, fill=WHITE, stroke=NAVY, sw=1.2, rx=5)
    cv.text(14, 171, "serialize", size=12.5, weight="bold", fill=NAVY)
    cv.text(98, 173,
            "<action_start>  ΔX  ΔY  ΔZ  ;  K1 ; K2 ; K3 ; K4 ; K5 ; K6  <action_end>",
            size=16, weight="bold", fill=INK)

    # Three method details, each with a more explicit mechanism.
    cv.text(0, 226, "A  Key Shuffle", size=14.5, weight="bold", fill=INK)
    cv.text(388, 226, "B  Repeated-action loss", size=14.5,
            weight="bold", fill=INK)
    cv.text(780, 226, "C  Mouse inversion", size=14.5,
            weight="bold", fill=INK)
    cv.line(366, 208, 366, 372, stroke="#D8E0E7", sw=1.1, dash="5 5")
    cv.line(758, 208, 758, 372, stroke="#D8E0E7", sw=1.1, dash="5 5")

    # A: conditional key bindings and synchronous label permutation.
    cv.text(8, 254, "prompt", size=11.5, weight="bold", fill=GREY)
    for i, lab in enumerate(("W↑", "A←", "S↓", "D→")):
        key(cv, 62 + i * 54, 238, lab, NAVY, FILL_BLUE, 11)
    cv.arrow(286, 254, 330, 254, color="red", sw=1.6)
    cv.text(8, 308, "label", size=11.5, weight="bold", fill=GREY)
    for i, lab in enumerate(("D↑", "S←", "W↓", "A→")):
        key(cv, 62 + i * 54, 292, lab, RED, FILL_RED, 11)
    cv.text(182, 354, "σ(prompt) = σ(action label)",
            size=12.5, weight="bold", fill=RED, anchor="middle")

    # B: 85% repeated actions and exponential weighting.
    cv.text(576, 254, ">85% of steps repeat the previous action",
            size=12.5, weight="bold", fill=RED, anchor="middle")
    for i in range(9):
        x = 400 + i * 38
        opacity = .22 + .78 * FACTS["loss_decay"] ** i
        cv.rect(x, 278, 30, 34, fill=RED, stroke=None, rx=3,
                opacity=opacity)
        cv.text(x + 15, 300, "W", size=11, weight="bold", fill=WHITE,
                anchor="middle")
        cv.text(x + 15, 330, f"{FACTS['loss_decay'] ** i:.2f}",
                size=9.5, fill=GREY, anchor="middle")
    cv.math(576, 358, "ω_t = γ^{k_t−1},   γ = 0.9",
            size=14.5, fill=INK, anchor="middle")

    # C: macro prediction to smooth high-frequency path.
    cv.text(792, 254, "model: Δp every 200 ms", size=12.5,
            weight="bold", fill=GREY)
    cv.text(792, 278, "executor: six 33 ms increments", size=12.5,
            weight="bold", fill=GREY)
    jag = [(800, 342), (860, 294), (920, 350), (980, 282), (1042, 326)]
    cv.path("M " + " L ".join(f"{a} {b}" for a, b in jag),
            stroke=GREY, sw=1.4, dash="5 4")
    cv.path("M 800 348 C 860 330, 900 316, 936 306 C 980 294, 1032 292, 1120 288",
            stroke=GREEN, sw=2.4)
    cv.text(1054, 354, "Kalman-filtered 30 Hz path", size=12.5,
            weight="bold", fill=GREEN, anchor="middle")


def fig_thinking(cv: Canvas):
    # Figure 1 right: the exact input/output contract.
    cv.text(0, 18, "Task-conditioned interaction contract",
            size=15.5, weight="bold", fill=INK)
    inputs = [
        ("I", "task instruction", NAVY, FILL_BLUE),
        ("mₜ", "long-term memory", PURPLE, FILL_PURPLE),
        ("Hₜ", "recent vision + action", AMBER, FILL_AMBER),
    ]
    for i, (sym, body, col, fill) in enumerate(inputs):
        x = 8 + i * 210
        cv.rect(x, 44, 184, 48, fill=fill, stroke=col, sw=1.2, rx=5)
        cv.text(x + 30, 74, sym, size=18, weight="bold", fill=col,
                anchor="middle")
        cv.text(x + 104, 72, body, size=12.5, weight="bold", fill=INK,
                anchor="middle")
        cv.path(f"M {x+92} 94 C {x+92} 116, 660 106, 660 132",
                stroke=col, sw=1.6)
    cv.rect(628, 128, 198, 54, fill=FILL_BLUE,
            stroke=NAVY, sw=1.5, rx=7)
    cv.text(727, 151, "HADES", size=17, weight="bold",
            fill=NAVY, anchor="middle")
    cv.text(727, 171, "adaptive think", size=12.5, fill=INK,
            anchor="middle")
    outputs = [
        ("∅", "routine control", GREY, FILL_GREY),
        ("rᶜᵘʳ", "local decision", RED, FILL_RED),
        ("rᵐᵉᵐ", "memory summary", PURPLE, FILL_PURPLE),
        ("aₜ", "device action", GREEN, FILL_GREEN),
    ]
    for i, (sym, body, col, fill) in enumerate(outputs):
        y = 18 + i * 48
        cv.path(f"M 826 155 C 854 155, 852 {y+19}, 878 {y+19}",
                stroke=col, sw=1.4)
        cv.rect(888, y, 250, 38, fill=fill, stroke=col, sw=1.1, rx=4)
        cv.text(916, y + 24, sym, size=15, weight="bold", fill=col)
        cv.text(1122, y + 24, body, size=12.5, weight="bold",
                fill=INK, anchor="end")
    cv.math(520, 210,
            "πθ(rₜ, aₜ | I, mₜ, Hₜ) = πθ(rₜ | ·) πθ(aₜ | ·, rₜ)",
            size=16.5, fill=INK, anchor="middle")

    # Decision timeline with explicit triggers.
    cv.text(0, 246, "Sparse annotation over a continuous trajectory",
            size=15, weight="bold", fill=INK)
    events = [
        ("move", "∅", NAVY), ("move", "∅", NAVY),
        ("route fails", "rᶜᵘʳ", RED), ("combat", "∅", NAVY),
        ("subgoal", "rᵐᵉᵐ", PURPLE), ("UI change", "rᶜᵘʳ", RED),
        ("move", "∅", NAVY),
    ]
    for i, (state, think, col) in enumerate(events):
        x = 4 + i * 164
        screen(cv, x, 266, 106, 56, col)
        cv.text(x + 53, 338, state, size=11.5, weight="bold",
                fill=col, anchor="middle")
        cv.rect(x + 112, 275, 40, 38,
                fill=FILL_GREY if think == "∅" else
                (FILL_RED if col == RED else FILL_PURPLE),
                stroke=col if think != "∅" else GREY, sw=1, rx=4)
        cv.text(x + 132, 299, think, size=11.5, weight="bold",
                fill=col if think != "∅" else GREY, anchor="middle")
        if i < 6:
            cv.arrow(x + 154, 294, x + 162, 294, color="grey", sw=1)
    cv.text(576, 374,
            "short-term queue keeps local detail  ·  rᵐᵉᵐ compacts completed stages into long-term memory",
            size=13.5, weight="bold", fill=PURPLE, anchor="middle")


def fig_rl(cv: Canvas):
    # Figure 2 upper failure mode.
    cv.text(0, 18, "Without compaction", size=15,
            weight="bold", fill=RED)
    cv.text(1146, 18, "hour-long trajectory → context OOM",
            size=13, weight="bold", fill=RED, anchor="end")
    for i in range(22):
        x = 8 + i * 50
        col = [FILL_BLUE, FILL_PURPLE, FILL_AMBER][(i // 7) % 3]
        edge = [NAVY, PURPLE, AMBER][(i // 7) % 3]
        cv.rect(x, 42, 40, 24, fill=col, stroke=edge, sw=.7, rx=3)
    cv.line(8, 78, 1100, 78, stroke=RED, sw=1.8, dash="7 5")
    cv.text(554, 98, "one terminal reward cannot explain which local action failed",
            size=12.5, weight="bold", fill=RED, anchor="middle")

    # Figure 2 lower TA-GRPO segmentation and memory transfer.
    cv.text(0, 132, "TA-GRPO with memory-compacted segments",
            size=15, weight="bold", fill=INK)
    segs = [
        (NAVY, FILL_BLUE, "τ₁", "m₁→m₂"),
        (PURPLE, FILL_PURPLE, "τ₂", "m₂→m₃"),
        (AMBER, FILL_AMBER, "τ₃", "m₃→m₄"),
    ]
    for g, (col, fill, lab, mem) in enumerate(segs):
        x = 12 + g * 382
        cv.rect(x, 156, 326, 112, fill=WHITE, stroke=col, sw=1.4, rx=6)
        cv.text(x + 14, 178, f"SEGMENT {lab}", size=13.5,
                weight="bold", fill=col)
        for i in range(5):
            cv.rect(x + 14 + i * 56, 192, 44, 26, fill=fill,
                    stroke=col, sw=.8, rx=3)
            cv.text(x + 36 + i * 56, 210, ["V", "r", "A", "V", "A"][i],
                    size=10.5, weight="bold", fill=col, anchor="middle")
        cv.rect(x + 14, 230, 132, 26, fill=FILL_GREEN,
                stroke=GREEN, sw=.9, rx=4)
        cv.text(x + 80, 248, "Rᵍ ∈ {0,1}", size=11.5,
                weight="bold", fill=GREEN, anchor="middle")
        cv.rect(x + 158, 230, 150, 26, fill=FILL_RED,
                stroke=RED, sw=.9, rx=4)
        cv.text(x + 233, 248, "+ α · PRMᵍ,ₜ", size=11.5,
                weight="bold", fill=RED, anchor="middle")
        if g < 2:
            cv.arrow(x + 330, 208, x + 368, 208, color="navy", sw=1.7)
            cv.text(x + 349, 198, mem, size=10.5, weight="bold",
                    fill=NAVY, anchor="middle")

    # Exact credit computation pipeline.
    cv.text(0, 306, "Trajectory-aware credit assignment",
            size=14.5, weight="bold", fill=INK)
    stages = [
        ("local reward", "rᵍ,ₜ = Rᵍ + α·PRMᵍ,ₜ", NAVY, FILL_BLUE, 210),
        ("time discount", "r̃ᵍ,ₜ = βᵀ⁻¹⁻ᵗ rᵍ,ₜ", PURPLE, FILL_PURPLE, 226),
        ("group normalize", "Aᵍ = (r̄ᵍ−μ)/σ", AMBER, FILL_AMBER, 196),
        ("token credit", "Aᵍ,ₜ = βᵀ⁻¹⁻ᵗ Aᵍ", GREEN, FILL_GREEN, 210),
    ]
    x = 8
    for i, (head, eq, col, fill, w) in enumerate(stages):
        cv.rect(x, 326, w, 52, fill=fill, stroke=col, sw=1.1, rx=5)
        cv.text(x + 10, 344, head, size=11.5, weight="bold", fill=col)
        cv.text(x + w / 2, 366, eq, size=12.5, weight="bold",
                fill=INK, anchor="middle")
        if i < 3:
            cv.arrow(x + w + 2, 352, x + w + 26, 352,
                     color="navy", sw=1.4)
        x += w + 28


def fig_inference(cv: Canvas):
    # Figure 3: client/server streaming at the top.
    cv.text(0, 18, "A  Streaming client–server loop",
            size=14.5, weight="bold", fill=INK)
    screen(cv, 8, 42, 98, 64, NAVY)
    cv.text(57, 125, "environment", size=11.5,
            weight="bold", fill=NAVY, anchor="middle")
    cv.arrow(114, 72, 168, 72, color="navy", sw=1.8)
    cv.rect(182, 38, 280, 72, fill=FILL_BLUE,
            stroke=NAVY, sw=1.4, rx=6)
    cv.text(322, 64, "Streaming-vLLM", size=17,
            weight="bold", fill=NAVY, anchor="middle")
    cv.text(322, 89, "prefill once · decode action chunks",
            size=12.5, weight="bold", fill=INK, anchor="middle")
    cv.arrow(470, 72, 514, 72, color="navy", sw=1.8)
    for i in range(6):
        x = 528 + i * 82
        cv.rect(x, 44, 66, 28, fill=FILL_BLUE,
                stroke=NAVY, sw=.9, rx=3)
        cv.text(x + 33, 63, f"K{i+1}", size=11,
                weight="bold", fill=NAVY, anchor="middle")
        cv.rect(x, 84, 66, 22,
                fill=FILL_GREEN if i < 2 else FILL_GREY,
                stroke=GREEN if i < 2 else GREY, sw=.8, rx=3)
        cv.text(x + 33, 100, "execute" if i < 2 else "queued",
                size=9.5, weight="bold",
                fill=GREEN if i < 2 else GREY, anchor="middle")
    cv.text(818, 126, "decode and execute overlap",
            size=12.5, weight="bold", fill=RED, anchor="middle")

    # Logical -> physical cache map.
    cv.text(0, 166, "B  Sliding logical context",
            size=14.5, weight="bold", fill=INK)
    logical = [
        ("Sys", NAVY, FILL_BLUE), ("Mem", PURPLE, FILL_PURPLE),
        ("Vₜ₋₁", CYAN, FILL_CYAN), ("Aₜ₋₁", AMBER, FILL_AMBER),
        ("Vₜ", CYAN, FILL_CYAN), ("Aₜ", AMBER, FILL_AMBER),
        ("Vₜ₊₁", CYAN, FILL_CYAN), ("Aₜ₊₁", AMBER, FILL_AMBER),
    ]
    for i, (lab, col, fill) in enumerate(logical):
        x = 14 + i * 91
        cv.rect(x, 190, 76, 36, fill=fill, stroke=col, sw=1, rx=4)
        cv.text(x + 38, 214, lab, size=11.5,
                weight="bold", fill=col, anchor="middle")
        cv.text(x + 38, 242, f"L{i+1}", size=10.5,
                weight="bold", fill=GREY, anchor="middle")
    cv.arrow(748, 208, 804, 208, color="red", sw=1.8)
    cv.text(776, 197, "slide", size=10.5, weight="bold",
            fill=RED, anchor="middle")
    for i, (lab, col, fill) in enumerate(logical[2:] + [("Vₜ₊₂", CYAN, FILL_CYAN),
                                                        ("Aₜ₊₂", AMBER, FILL_AMBER)]):
        x = 816 + (i % 4) * 82
        y = 174 + (i // 4) * 54
        cv.rect(x, y, 68, 32, fill=fill, stroke=col, sw=.9, rx=4)
        cv.text(x + 34, y + 21, lab, size=10.5,
                weight="bold", fill=col, anchor="middle")

    cv.text(0, 278, "C  Logical-to-physical KV lookup",
            size=14.5, weight="bold", fill=INK)
    mappings = [(1, 3), (2, 7), (3, 1), (4, 8), (5, 4), (6, 2)]
    for i, (logical_id, physical_id) in enumerate(mappings):
        x = 18 + i * 102
        cv.rect(x, 300, 78, 28, fill=FILL_BLUE,
                stroke=NAVY, sw=.9, rx=3)
        cv.text(x + 39, 319, f"L{logical_id}", size=11,
                weight="bold", fill=NAVY, anchor="middle")
        cv.arrow(x + 39, 330, x + 39, 346, color="grey", sw=1)
        cv.rect(x, 348, 78, 28, fill=FILL_GREEN,
                stroke=GREEN, sw=.9, rx=3)
        cv.text(x + 39, 367, f"P{physical_id}", size=11,
                weight="bold", fill=GREEN, anchor="middle")
    opts = [
        ("RoPE refresh", PURPLE), ("CUDA Graph", NAVY),
        ("action FSM", AMBER), ("C++ scheduler", GREEN),
    ]
    for i, (lab, col) in enumerate(opts):
        x = 676 + (i % 2) * 228
        y = 294 + (i // 2) * 46
        cv.rect(x, y, 206, 34, fill=WHITE, stroke=col, sw=1.1, rx=4)
        cv.text(x + 103, y + 22, lab, size=12.5,
                weight="bold", fill=col, anchor="middle")
    cv.text(1100, 377, ">20× vLLM  ·  >30 Hz",
            size=15.5, weight="bold", fill=RED, anchor="end")


def fig_flywheel(cv: Canvas):
    # Figure 4 left: source-specific data construction.
    cv.text(0, 18, "A  Multi-source data construction",
            size=14.5, weight="bold", fill=INK)
    sources = [
        ("WEB", "rule filtering", "CPT data", NAVY, FILL_BLUE),
        ("HUMAN", "segment + annotate", "SFT data", PURPLE, FILL_PURPLE),
        ("AGENT", "verify + judge", "RL / PRM data", AMBER, FILL_AMBER),
    ]
    for i, (src, process, dest, col, fill) in enumerate(sources):
        y = 46 + i * 74
        cv.rect(0, y, 112, 42, fill=fill, stroke=col, sw=1.1, rx=5)
        cv.text(56, y + 26, src, size=13.5,
                weight="bold", fill=col, anchor="middle")
        cv.arrow(118, y + 21, 174, y + 21, color="navy", sw=1.5)
        cv.rect(184, y, 174, 42, fill=WHITE, stroke=GREY, sw=1, rx=5)
        cv.text(271, y + 26, process, size=12.5,
                weight="bold", fill=INK, anchor="middle")
        cv.arrow(364, y + 21, 416, y + 21, color="navy", sw=1.5)
        cv.rect(426, y, 140, 42, fill=fill, stroke=col, sw=1.1, rx=5)
        cv.text(496, y + 26, dest, size=12.5,
                weight="bold", fill=col, anchor="middle")
    cv.math(282, 284, "τ = (o₁,a₁,o₂,a₂,…,o_T,a_T)",
            size=17, fill=NAVY, anchor="middle")
    cv.text(282, 310, "same API-free format across every source",
            size=12.5, weight="bold", fill=GREY, anchor="middle")

    cv.line(596, 8, 596, 326, stroke="#D8E0E7",
            sw=1.1, dash="5 5")
    cv.text(628, 18, "B  Online data flywheel",
            size=14.5, weight="bold", fill=INK)

    # Exact pass/fail routing around the policy.
    cx, cy = 842, 174
    cv.circle(cx, cy, 62, fill=FILL_BLUE, stroke=NAVY, sw=1.5)
    cv.text(cx, cy - 4, "HADES", size=17, weight="bold",
            fill=NAVY, anchor="middle")
    cv.text(cx, cy + 20, "policy πᵏ", size=13, fill=INK,
            anchor="middle")
    nodes = [
        (842, 48, "100+ workers", PURPLE, FILL_PURPLE),
        (1040, 174, "checker + judger", GREEN, FILL_GREEN),
        (842, 300, "PRM labels", RED, FILL_RED),
        (650, 174, "SFT / RL pool", AMBER, FILL_AMBER),
    ]
    for x, y, lab, col, fill in nodes:
        cv.rect(x - 72, y - 20, 144, 40, fill=fill,
                stroke=col, sw=1.1, rx=5)
        cv.text(x, y + 5, lab, size=12.5,
                weight="bold", fill=col, anchor="middle")
    cv.path("M 842 112 C 922 108, 1000 126, 1012 156",
            stroke=PURPLE, sw=1.8, arrow="navy")
    cv.path("M 1012 194 C 990 252, 924 292, 914 296",
            stroke=RED, sw=1.8)
    cv.text(998, 236, "FAIL", size=10.5, weight="bold",
            fill=RED, anchor="middle")
    cv.path("M 770 300 C 704 278, 656 232, 650 194",
            stroke=RED, sw=1.8)
    cv.path("M 650 154 C 672 92, 770 60, 812 68",
            stroke=GREEN, sw=1.8)
    cv.text(670, 112, "PASS", size=10.5, weight="bold",
            fill=GREEN, anchor="middle")

    # Compact evidence boundary and paper-level contribution.
    cv.rect(0, 340, 1152, 42, fill=WHITE, stroke=RED,
            sw=1.1, rx=5)
    cv.text(14, 366, "EVIDENCE BOUNDARY", size=12.5,
            weight="bold", fill=RED)
    cv.text(170, 366,
            "system metrics are reported; claimed benchmark leadership is not tabulated in the supplied manuscript",
            size=13.2, weight="bold", fill=INK)
