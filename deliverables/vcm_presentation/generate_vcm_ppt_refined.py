"""Generate a refined seven-slide VCM deck matching the supplied reference style."""

from pathlib import Path

import pymupdf
from pptx import Presentation
from pptx.enum.chart import XL_CHART_TYPE
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

from generate_vcm_ppt import (
    BLUE,
    CYAN,
    GREEN,
    INK,
    LIGHT,
    MID,
    NAVY,
    ORANGE,
    PALE_BLUE,
    RED,
    WHITE,
    W,
    H,
    add_box,
    add_callout,
    add_circle,
    add_footer,
    add_line,
    add_native_chart,
    add_rich_text,
    add_text,
    add_title,
    new_slide,
)


ROOT = Path(__file__).resolve().parent
OUT_FILE = ROOT / "VCM_7页精简汇报_可编辑版.pptx"
ASSET_DIR = ROOT / "assets"
PAPER = Path(
    "/home/ubuntu/.cursor/projects/workspace/uploads/"
    "2504.19627v2_compressed_d67d.pdf"
)

# Reference-deck palette: restrained blue, coral emphasis, pale scientific panels.
DEEP = NAVY
ACCENT = BLUE
CORAL = RED
TEAL = GREEN
SKY = CYAN
PAPER_BLUE = PALE_BLUE
PAPER_GREY = LIGHT


def extract_asset(page_index, rect, name, zoom=2.4):
    """Extract a paper figure crop for visual evidence panels."""
    ASSET_DIR.mkdir(exist_ok=True)
    target = ASSET_DIR / name
    if target.exists():
        return target
    doc = pymupdf.open(PAPER)
    page = doc[page_index]
    pix = page.get_pixmap(
        matrix=pymupdf.Matrix(zoom, zoom),
        clip=pymupdf.Rect(*rect),
        alpha=False,
    )
    pix.save(target)
    return target


def thin_panel(slide, x, y, w, h, fill=WHITE, line=PAPER_GREY):
    return add_box(
        slide,
        x,
        y,
        w,
        h,
        fill=fill,
        line=line,
        radius=True,
        line_width=0.7,
    )


def small_token(slide, x, y, color, label="", w=0.35, h=0.24):
    add_box(slide, x, y, w, h, fill=color, line=WHITE, radius=False, line_width=0.3)
    if label:
        add_text(
            slide,
            label,
            x,
            y,
            w,
            h,
            size=6.5,
            bold=True,
            color=WHITE,
            align=PP_ALIGN.CENTER,
        )


def icon_image(slide, x, y, d, color=ACCENT):
    add_circle(slide, x, y, d, fill=WHITE, line=color, width=1.2)
    add_box(
        slide,
        x + d * 0.19,
        y + d * 0.24,
        d * 0.62,
        d * 0.48,
        fill=color,
        line=color,
        radius=False,
    )
    add_circle(slide, x + d * 0.57, y + d * 0.31, d * 0.10, fill=WHITE, line=WHITE)
    tri = slide.shapes.add_shape(
        MSO_AUTO_SHAPE_TYPE.ISOSCELES_TRIANGLE,
        Inches(x + d * 0.29),
        Inches(y + d * 0.43),
        Inches(d * 0.36),
        Inches(d * 0.25),
    )
    tri.fill.solid()
    tri.fill.fore_color.rgb = WHITE
    tri.line.fill.background()


def add_lattice(slide, x, y):
    """Editable forward-backward lattice with possible and selected paths."""
    rows, cols = 5, 8
    dx, dy = 0.55, 0.47
    for c in range(cols - 1):
        for r in range(rows):
            add_line(
                slide,
                x + c * dx,
                y + r * dy,
                x + (c + 1) * dx,
                y + r * dy,
                color=ACCENT,
                width=0.55,
            )
            if r < rows - 1:
                add_line(
                    slide,
                    x + c * dx,
                    y + r * dy,
                    x + (c + 1) * dx,
                    y + (r + 1) * dy,
                    color=RGB_LIGHT_BLUE,
                    width=0.45,
                )
    path = [0, 0, 1, 1, 2, 3, 3, 4]
    for c in range(cols - 1):
        add_line(
            slide,
            x + c * dx,
            y + path[c] * dy,
            x + (c + 1) * dx,
            y + path[c + 1] * dy,
            color=CORAL,
            width=2.7,
        )
    for c in range(cols):
        for r in range(rows):
            active = r == path[c]
            add_circle(
                slide,
                x + c * dx - 0.07,
                y + r * dy - 0.07,
                0.14,
                fill=CORAL if active else WHITE,
                line=CORAL if active else ACCENT,
                width=0.7,
            )


RGB_LIGHT_BLUE = SKY


def build_deck():
    fig1 = extract_asset(1, (70, 54, 540, 225), "paper_figure1.png")
    fig4 = extract_asset(5, (70, 55, 540, 265), "paper_figure4.png")

    prs = Presentation()
    prs.slide_width = W
    prs.slide_height = H
    prs.core_properties.title = "VCM：7页精修论文汇报"
    prs.core_properties.author = "Generated from Luo et al. (2025)"
    prs.core_properties.comments = (
        "Scientific diagrams and charts are native editable PowerPoint objects. "
        "Two qualitative evidence panels are cropped from the source paper."
    )

    # 1 — Reference-like title page
    s = new_slide(prs, bg=DEEP)
    add_text(
        s,
        "VCM:",
        1.05,
        1.20,
        2.0,
        0.60,
        size=37,
        bold=True,
        color=WHITE,
    )
    add_text(
        s,
        "Vision Concept Modeling with\nAdaptive Vision Token Compression",
        1.05,
        1.88,
        10.60,
        1.48,
        size=29,
        bold=True,
        color=WHITE,
        align=PP_ALIGN.CENTER,
    )
    add_line(s, 2.10, 3.72, 11.18, 3.72, color=SKY, width=1.4)
    add_text(
        s,
        "From token-level redundancy to instruction-conditioned concepts",
        1.55,
        4.12,
        10.25,
        0.48,
        size=18,
        color=WHITE,
        align=PP_ALIGN.CENTER,
    )
    add_text(
        s,
        "Luo et al. · arXiv:2504.19627v2 · 2025",
        4.20,
        5.32,
        4.95,
        0.30,
        size=11,
        color=SKY,
        align=PP_ALIGN.CENTER,
    )

    # 2 — Rich problem framing with paper visual
    s = new_slide(prs)
    add_title(s, "Vision tokens are not vision concepts")
    s.shapes.add_picture(str(fig1), Inches(0.72), Inches(1.25), width=Inches(5.30))
    add_text(
        s,
        "Current LVLM",
        0.92,
        4.05,
        1.55,
        0.30,
        size=13,
        bold=True,
        color=MID,
        align=PP_ALIGN.CENTER,
    )
    # Dense token stack
    for row in range(5):
        for col in range(8):
            small_token(
                s,
                6.55 + col * 0.31,
                1.55 + row * 0.30,
                ACCENT if (row + col) % 3 else SKY,
                w=0.27,
                h=0.25,
            )
    add_text(
        s,
        "all image patches",
        6.72,
        3.13,
        2.10,
        0.30,
        size=11,
        color=MID,
        align=PP_ALIGN.CENTER,
    )
    add_line(s, 9.05, 2.28, 9.72, 2.28, color=CORAL, width=2.2, arrow=True)
    thin_panel(s, 9.86, 1.38, 2.65, 1.80, fill=PAPER_BLUE, line=ACCENT)
    add_text(
        s,
        "LLM",
        10.55,
        1.70,
        1.25,
        0.40,
        size=25,
        bold=True,
        color=DEEP,
        align=PP_ALIGN.CENTER,
    )
    add_text(
        s,
        "attention cost\n∝ sequence length",
        10.34,
        2.30,
        1.65,
        0.52,
        size=11,
        color=MID,
        align=PP_ALIGN.CENTER,
    )
    add_line(s, 7.95, 3.63, 7.95, 4.15, color=TEAL, width=2.0, arrow=True)
    add_text(
        s,
        "instruction",
        8.10,
        3.72,
        1.18,
        0.25,
        size=10,
        bold=True,
        color=TEAL,
    )
    # Sparse concepts
    for i, (label, color) in enumerate(
        [("object", ACCENT), ("attribute", TEAL), ("location", ORANGE)]
    ):
        add_circle(s, 6.60 + i * 1.35, 4.45, 0.83, fill=color, line=WHITE)
        add_text(
            s,
            label,
            6.64 + i * 1.35,
            4.70,
            0.75,
            0.24,
            size=8,
            bold=True,
            color=WHITE,
            align=PP_ALIGN.CENTER,
        )
    add_line(s, 10.55, 4.85, 11.30, 4.85, color=TEAL, width=2.2, arrow=True)
    add_text(
        s,
        "16 tokens",
        11.35,
        4.64,
        1.00,
        0.38,
        size=15,
        bold=True,
        color=TEAL,
        align=PP_ALIGN.CENTER,
    )
    add_callout(
        s,
        "Vision Concept Model = 根据任务动态决定概念数量，并保留对应空间位置"
    )
    add_footer(s, 2, source="Paper Figure 1; right-side schematic is editable")

    # 3 — Empirical clue: chart-like scientific composite
    s = new_slide(prs)
    add_title(s, "Text prior reveals the required visual budget")
    labels = [
        ("Response keywords", "positive correlation", ACCENT, False),
        ("Instruction keywords", "negative correlation", ORANGE, True),
        ("Response − Instruction", "stable negative prior", TEAL, True),
    ]
    for i, (head, note, color, down) in enumerate(labels):
        x = 0.72 + i * 4.12
        add_text(
            s,
            head,
            x,
            1.28,
            3.55,
            0.32,
            size=14,
            bold=True,
            color=INK,
            align=PP_ALIGN.CENTER,
        )
        add_line(s, x + 0.48, 3.62, x + 3.20, 3.62, color=MID, width=0.8)
        add_line(s, x + 0.48, 3.62, x + 0.48, 1.82, color=MID, width=0.8)
        for j in range(10):
            px = x + 0.75 + j * 0.23
            base = (j / 9) * 1.10
            py = (
                2.00 + base + (0.10 if j % 2 else -0.08)
                if down
                else 3.28 - base + (0.10 if j % 2 else -0.08)
            )
            add_circle(s, px, py, 0.10, fill=color, line=color, width=0.3)
        if down:
            add_line(s, x + 0.72, 1.95, x + 2.98, 3.30, color=color, width=2.0)
        else:
            add_line(s, x + 0.72, 3.28, x + 2.98, 1.95, color=color, width=2.0)
        add_text(
            s,
            note,
            x + 0.52,
            3.82,
            2.62,
            0.28,
            size=10,
            bold=i == 2,
            color=color,
            align=PP_ALIGN.CENTER,
        )
    # Compact causal explanation
    add_text(s, "coarse supervision", 1.05, 4.54, 2.05, 0.30, size=13, bold=True, color=ACCENT, align=PP_ALIGN.CENTER)
    add_line(s, 3.15, 4.70, 4.25, 4.70, color=ACCENT, width=1.8, arrow=True)
    add_text(s, "keyword difference Nₖₑᵧ", 4.42, 4.54, 2.45, 0.30, size=13, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)
    add_line(s, 6.98, 4.70, 8.08, 4.70, color=ORANGE, width=1.8, arrow=True)
    add_text(s, "target concept length L", 8.25, 4.54, 2.45, 0.30, size=13, bold=True, color=TEAL, align=PP_ALIGN.CENTER)
    add_line(s, 10.83, 4.70, 11.45, 4.70, color=TEAL, width=1.8, arrow=True)
    add_text(s, "self-supervision", 11.48, 4.54, 1.15, 0.30, size=11, bold=True, color=DEEP, align=PP_ALIGN.CENTER)
    add_box(s, 1.82, 5.24, 9.68, 0.62, fill=WHITE, line=ACCENT, radius=False, line_width=1.1)
    add_rich_text(
        s,
        [
            ("无需 concept annotations：", INK, False),
            ("文本先验估计“保留多少”", CORAL, True),
            ("，动态规划再学习“保留哪里”", DEEP, True),
        ],
        2.05,
        5.34,
        9.20,
        0.40,
        size=15,
        align=PP_ALIGN.CENTER,
    )
    add_callout(s, "The key signal is not a fixed pruning ratio, but a sample-specific visual budget")
    add_footer(s, 3, source="Paper Figure 2 and Section 3.1")

    # 4 — Dense architecture, matching reference's scientific schematic density
    s = new_slide(prs)
    add_title(s, "VCM: learn semantics first, then learn variable-length concepts")
    # Left inputs
    icon_image(s, 0.72, 1.43, 0.78, ACCENT)
    add_text(s, "Visual input Xⱽ", 0.62, 2.28, 1.00, 0.30, size=10, bold=True, color=ACCENT, align=PP_ALIGN.CENTER)
    thin_panel(s, 0.52, 2.78, 1.42, 1.72, fill=WHITE, line=ORANGE)
    words = ["Where", "is", "the", "person", "in", "yellow", "?"]
    for i, word in enumerate(words):
        active = word in {"person", "yellow"}
        add_box(
            s,
            0.68,
            2.94 + i * 0.19,
            1.10,
            0.16,
            fill=CORAL if active else PAPER_GREY,
            line=WHITE,
            radius=False,
            line_width=0.2,
        )
        add_text(
            s,
            word,
            0.70,
            2.94 + i * 0.19,
            1.06,
            0.16,
            size=6,
            bold=active,
            color=WHITE if active else MID,
            align=PP_ALIGN.CENTER,
        )
    add_text(s, "Instruction Xᴵ", 0.62, 4.65, 1.22, 0.30, size=10, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)
    # Stage A
    thin_panel(s, 2.25, 1.32, 3.05, 3.84, fill=PAPER_BLUE, line=PAPER_GREY)
    add_text(s, "A  Semantic alignment", 2.52, 1.53, 2.50, 0.34, size=15, bold=True, color=DEEP, align=PP_ALIGN.CENTER)
    blocks = [
        (2.55, 2.16, "Vision\nEncoder", ACCENT),
        (3.82, 2.16, "Keyword\nSelector", ORANGE),
        (2.55, 3.42, "Global\nVision Gⱽ", ACCENT),
        (3.82, 3.42, "Global\nText Gᵀ", ORANGE),
    ]
    for x, y, label, color in blocks:
        add_box(s, x, y, 1.02, 0.62, fill=WHITE, line=color, radius=True, line_width=0.9)
        add_text(s, label, x + 0.08, y + 0.10, 0.86, 0.42, size=9, bold=True, color=color, align=PP_ALIGN.CENTER)
    add_line(s, 3.06, 2.80, 3.06, 3.36, color=ACCENT, arrow=True)
    add_line(s, 4.33, 2.80, 4.33, 3.36, color=ORANGE, arrow=True)
    add_line(s, 3.58, 3.74, 3.77, 3.74, color=CORAL, width=1.5, arrow=True)
    add_text(s, "Lₛₐ", 3.42, 4.34, 0.72, 0.30, size=16, bold=True, color=CORAL, align=PP_ALIGN.CENTER)
    # Stage B
    thin_panel(s, 5.58, 1.32, 2.62, 3.84, fill=WHITE, line=PAPER_GREY)
    add_text(s, "B  Keyword selection", 5.80, 1.53, 2.18, 0.34, size=15, bold=True, color=DEEP, align=PP_ALIGN.CENTER)
    for i, word in enumerate(words):
        active = word in {"person", "yellow"}
        small_token(
            s,
            5.82 + (i % 4) * 0.51,
            2.25 + (i // 4) * 0.42,
            CORAL if active else PAPER_GREY,
            word[:3],
            w=0.44,
            h=0.28,
        )
    add_text(s, "K = Softmax(·)", 5.95, 3.24, 1.88, 0.30, size=13, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)
    add_text(s, "K > E(K)", 6.10, 3.69, 1.58, 0.30, size=14, bold=True, color=CORAL, align=PP_ALIGN.CENTER)
    add_text(s, "person · yellow", 5.93, 4.28, 1.93, 0.30, size=12, bold=True, color=CORAL, align=PP_ALIGN.CENTER)
    # Stage C
    thin_panel(s, 8.48, 1.32, 3.98, 3.84, fill=PAPER_BLUE, line=PAPER_GREY)
    add_text(s, "C  Vision concept modeling", 8.77, 1.53, 3.40, 0.34, size=15, bold=True, color=DEEP, align=PP_ALIGN.CENTER)
    for r in range(5):
        for c in range(7):
            keep = (r, c) in {(1, 2), (1, 3), (2, 2), (2, 3), (3, 4)}
            small_token(
                s,
                8.83 + c * 0.35,
                2.16 + r * 0.31,
                ACCENT if keep else PAPER_GREY,
                w=0.29,
                h=0.25,
            )
    add_line(s, 11.42, 2.88, 11.95, 2.88, color=TEAL, width=2.0, arrow=True)
    add_circle(s, 11.73, 3.52, 0.55, fill=TEAL, line=WHITE)
    add_text(s, "Hᵥᶜ", 11.83, 3.67, 0.35, 0.20, size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text(s, "Lᵥ꜀ₘ", 10.01, 4.36, 0.90, 0.30, size=16, bold=True, color=TEAL, align=PP_ALIGN.CENTER)
    # Cross-stage arrows and objective
    add_line(s, 1.96, 2.05, 2.20, 2.45, color=ACCENT, width=1.4, arrow=True)
    add_line(s, 1.96, 3.65, 2.20, 3.20, color=ORANGE, width=1.4, arrow=True)
    add_line(s, 5.32, 3.16, 5.53, 3.16, color=MID, width=1.4, arrow=True)
    add_line(s, 8.23, 3.16, 8.43, 3.16, color=MID, width=1.4, arrow=True)
    add_box(s, 2.42, 5.43, 8.50, 0.55, fill=WHITE, line=ACCENT, radius=False, line_width=1.0)
    add_text(
        s,
        "L = ⌊M·S·(1−Norm(Nₖₑᵧ))⌋     |     L = Lₙₜₚ + ε(r)·Lᵥ꜀ₘ",
        2.62,
        5.52,
        8.10,
        0.34,
        size=15,
        bold=True,
        color=DEEP,
        align=PP_ALIGN.CENTER,
    )
    add_callout(s, "Coarse text supervision → adaptive visual concepts → efficient LLM inference")
    add_footer(s, 4, source="Editable reconstruction of Paper Figure 3")

    # 5 — DP lattice and segment merging
    s = new_slide(prs)
    add_title(s, "Forward–Backward turns unknown positions into a learnable alignment problem")
    add_text(s, "Target length", 0.78, 1.24, 1.65, 0.30, size=14, bold=True, color=ACCENT)
    add_text(
        s,
        "L = ⌊M·S·(1−Norm(Nₖₑᵧ))⌋",
        0.78,
        1.62,
        4.10,
        0.45,
        size=20,
        bold=True,
        color=DEEP,
    )
    add_text(s, "Extended target", 0.78, 2.38, 1.65, 0.30, size=14, bold=True, color=TEAL)
    add_text(s, "∅  ★  ∅  ★  ∅", 0.88, 2.76, 3.10, 0.45, size=25, bold=True, color=TEAL, align=PP_ALIGN.CENTER)
    add_box(s, 0.78, 3.58, 3.95, 1.05, fill=PAPER_BLUE, line=PAPER_GREY, radius=True, line_width=0.7)
    add_text(s, "p(Zᵥ|Yᵥ) = Σₗ α(t,l)β(t,l)", 1.02, 3.78, 3.48, 0.34, size=17, bold=True, color=DEEP, align=PP_ALIGN.CENTER)
    add_text(s, "Lᵥ꜀ₘ = −log p(Zᵥ|Yᵥ)", 1.25, 4.18, 3.02, 0.28, size=14, color=CORAL, align=PP_ALIGN.CENTER)
    add_text(s, "All possible alignments", 5.45, 1.22, 2.30, 0.30, size=14, bold=True, color=ACCENT)
    add_lattice(s, 5.48, 1.82)
    add_text(s, "possible paths", 9.92, 1.55, 1.28, 0.25, size=9, color=ACCENT)
    add_line(s, 9.92, 1.95, 10.62, 1.95, color=ACCENT, width=1.2)
    add_text(s, "most probable", 9.92, 2.26, 1.28, 0.25, size=9, color=CORAL)
    add_line(s, 9.92, 2.66, 10.62, 2.66, color=CORAL, width=2.7)
    add_box(s, 9.67, 3.26, 2.35, 0.80, fill=WHITE, line=CORAL, radius=True, line_width=1.0)
    add_text(s, "O(2ᴹ)  →  O(M²)", 9.88, 3.48, 1.94, 0.30, size=17, bold=True, color=CORAL, align=PP_ALIGN.CENTER)
    # Segment merging illustration
    add_line(s, 6.78, 4.32, 6.78, 4.78, color=TEAL, width=2.0, arrow=True)
    add_text(s, "Segment Merging", 5.92, 4.84, 1.72, 0.28, size=12, bold=True, color=TEAL, align=PP_ALIGN.CENTER)
    probs = [0.12, 0.82, 0.76, 0.18, 0.87, 0.72, 0.10, 0.08]
    for i, p in enumerate(probs):
        active = p > 0.5
        add_box(
            s,
            4.98 + i * 0.47,
            5.24,
            0.38,
            0.42,
            fill=ACCENT if active else PAPER_GREY,
            line=WHITE,
            radius=False,
            line_width=0.3,
        )
    add_line(s, 8.85, 5.44, 9.42, 5.44, color=TEAL, width=1.8, arrow=True)
    for i, color in enumerate([ACCENT, TEAL]):
        add_circle(s, 9.58 + i * 0.90, 5.06, 0.72, fill=color, line=WHITE)
        add_text(s, f"C{i+1}", 9.75 + i * 0.90, 5.28, 0.38, 0.22, size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_callout(s, "Train on all feasible paths; infer the best path; merge adjacent retained features")
    add_footer(s, 5, source="Paper Sections 3.3–3.4 and Figure 6")

    # 6 — Mixed quantitative and qualitative evidence
    s = new_slide(prs)
    add_title(s, "Less computation, stronger visual concepts")
    chart1 = add_native_chart(
        s,
        ["LLaVA\n576", "VCM\n128", "VCM\n64"],
        [("FLOPs (T)", [4.62, 1.71, 1.24])],
        0.62,
        1.28,
        3.70,
        3.25,
        colors=[ACCENT],
        ymax=5.0,
        legend=False,
    )
    chart1.value_axis.has_title = True
    chart1.value_axis.axis_title.text_frame.text = "FLOPs (T)"
    chart1.value_axis.axis_title.text_frame.paragraphs[0].font.size = Pt(8)
    add_text(s, "Efficiency", 1.55, 1.04, 1.80, 0.28, size=13, bold=True, color=INK, align=PP_ALIGN.CENTER)
    chart2 = add_native_chart(
        s,
        ["FastV", "PDrop", "Sparse", "VisionZip", "LLaVA", "VCM"],
        [("VQA Avg.", [53.1, 57.8, 57.9, 59.1, 59.5, 60.8])],
        4.55,
        1.28,
        4.05,
        3.25,
        colors=[ORANGE],
        ymin=50,
        ymax=62,
        legend=False,
    )
    chart2.series[0].points[5].format.fill.solid()
    chart2.series[0].points[5].format.fill.fore_color.rgb = CORAL
    chart2.series[0].points[5].format.line.color.rgb = CORAL
    add_text(s, "11-benchmark VQA average", 5.25, 1.04, 2.62, 0.28, size=13, bold=True, color=INK, align=PP_ALIGN.CENTER)
    # Qualitative paper evidence
    thin_panel(s, 8.84, 1.15, 3.85, 3.58, fill=WHITE, line=PAPER_GREY)
    s.shapes.add_picture(str(fig4), Inches(9.02), Inches(1.48), width=Inches(3.50))
    add_text(s, "Instruction-conditioned sparsity", 9.12, 4.28, 3.25, 0.28, size=11, bold=True, color=INK, align=PP_ALIGN.CENTER)
    # Three takeaways
    metrics = [
        ("≈85%", "fewer FLOPs", ACCENT),
        ("60.8", "best VQA Avg.", CORAL),
        ("↑", "dense perception", TEAL),
    ]
    for i, (value, label, color) in enumerate(metrics):
        x = 1.05 + i * 4.10
        add_text(s, value, x, 4.86, 1.30, 0.55, size=30, bold=True, color=color, align=PP_ALIGN.CENTER)
        add_text(s, label, x + 1.38, 5.04, 1.95, 0.30, size=13, bold=True, color=INK)
    add_callout(s, "VCM compresses redundancy without collapsing the visual concepts needed by the task")
    add_footer(s, 6, source="Paper Figure 4, Table 1, Table 10 and Appendix D")

    # 7 — Reference-like conclusion: one diagram plus a strong callout
    s = new_slide(prs)
    add_title(s, "From token compression to vision concept modeling")
    add_text(s, "Token-level LVLM", 0.82, 1.22, 2.40, 0.36, size=17, bold=True, color=MID, align=PP_ALIGN.CENTER)
    for row in range(5):
        for col in range(8):
            small_token(
                s,
                0.92 + col * 0.30,
                1.86 + row * 0.29,
                ACCENT if (row + col) % 2 else SKY,
                w=0.26,
                h=0.24,
            )
    add_text(s, "fixed, dense, redundant", 1.05, 3.48, 2.15, 0.30, size=11, color=MID, align=PP_ALIGN.CENTER)
    add_line(s, 3.62, 2.57, 5.05, 2.57, color=CORAL, width=2.7, arrow=True)
    add_text(s, "instruction prior", 3.72, 2.02, 1.20, 0.28, size=11, bold=True, color=CORAL, align=PP_ALIGN.CENTER)
    # Center VCM mechanism
    add_circle(s, 5.23, 1.62, 1.92, fill=PAPER_BLUE, line=ACCENT, width=1.5)
    add_text(s, "VCM", 5.56, 2.04, 1.25, 0.43, size=27, bold=True, color=DEEP, align=PP_ALIGN.CENTER)
    add_text(s, "semantic alignment\n+ dynamic paths", 5.46, 2.56, 1.45, 0.53, size=10, color=MID, align=PP_ALIGN.CENTER)
    add_line(s, 7.28, 2.57, 8.65, 2.57, color=TEAL, width=2.7, arrow=True)
    # Concepts
    for i, (label, color) in enumerate(
        [("what", ACCENT), ("where", TEAL), ("how much", ORANGE)]
    ):
        add_circle(s, 8.90 + i * 1.10, 1.96, 0.84, fill=color, line=WHITE)
        add_text(s, label, 8.94 + i * 1.10, 2.21, 0.76, 0.24, size=8, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text(s, "adaptive, sparse, spatially grounded", 9.02, 3.48, 3.00, 0.30, size=11, color=TEAL, align=PP_ALIGN.CENTER)
    # Contributions + limitations
    add_line(s, 0.90, 4.18, 12.32, 4.18, color=PAPER_GREY, width=0.8)
    rows = [
        ("Contribution", "Instruction-conditioned concept quantity + location", ACCENT),
        ("Evidence", "≈85% fewer FLOPs; competitive VQA; stronger dense perception", TEAL),
        ("Limitation", "keyword bias · coarse length prior · concept interpretability", CORAL),
    ]
    for i, (head, body, color) in enumerate(rows):
        y = 4.46 + i * 0.55
        add_text(s, head, 1.12, y, 1.35, 0.34, size=13, bold=True, color=color, align=PP_ALIGN.RIGHT)
        add_line(s, 2.66, y + 0.17, 3.20, y + 0.17, color=color, width=1.6)
        add_text(s, body, 3.45, y, 8.35, 0.34, size=13, bold=i == 0, color=INK)
    add_box(s, 1.18, 6.16, 10.95, 0.60, fill=WHITE, line=ACCENT, radius=False, line_width=1.2)
    add_rich_text(
        s,
        [
            ("Take-home: ", DEEP, True),
            ("do not process everything; ", CORAL, True),
            ("select the concepts required by the instruction.", DEEP, True),
        ],
        1.42,
        6.25,
        10.48,
        0.40,
        size=16,
        align=PP_ALIGN.CENTER,
    )
    add_footer(s, 7, source="Paper conclusion and limitations")

    prs.save(OUT_FILE)
    return OUT_FILE


if __name__ == "__main__":
    print(build_deck())
