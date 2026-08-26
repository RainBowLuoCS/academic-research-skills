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
