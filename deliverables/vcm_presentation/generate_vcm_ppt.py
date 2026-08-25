"""Generate an editable, style-matched presentation for the VCM paper.

All diagrams and data charts are composed from native PowerPoint objects.
Only the small paper thumbnail on the title slide is rasterized from the
source PDF. Run from this directory with:

    python3 generate_vcm_ppt.py
"""

from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE, MSO_CONNECTOR
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.xmlchemy import OxmlElement
from pptx.util import Inches, Pt


OUT_DIR = Path(__file__).resolve().parent
OUT_FILE = OUT_DIR / "VCM_论文汇报_可编辑版.pptx"

W = Inches(13.333)
H = Inches(7.5)

NAVY = RGBColor(7, 70, 124)
BLUE = RGBColor(39, 112, 177)
LIGHT_BLUE = RGBColor(230, 241, 250)
PALE_BLUE = RGBColor(244, 249, 253)
CYAN = RGBColor(60, 180, 196)
RED = RGBColor(206, 38, 54)
ORANGE = RGBColor(238, 119, 51)
GREEN = RGBColor(0, 153, 136)
YELLOW = RGBColor(246, 197, 68)
INK = RGBColor(30, 35, 40)
MID = RGBColor(93, 103, 112)
LIGHT = RGBColor(224, 229, 234)
WHITE = RGBColor(255, 255, 255)
BLACK = RGBColor(0, 0, 0)

FONT_CN = "Microsoft YaHei"
FONT_EN = "Arial"


def add_text(
    slide,
    text,
    x,
    y,
    w,
    h,
    *,
    size=18,
    bold=False,
    color=INK,
    align=PP_ALIGN.LEFT,
    valign=MSO_ANCHOR.MIDDLE,
    font=FONT_CN,
    margin=0.03,
    rotation=0,
):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    box.rotation = rotation
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.margin_left = Inches(margin)
    tf.margin_right = Inches(margin)
    tf.margin_top = Inches(margin)
    tf.margin_bottom = Inches(margin)
    tf.vertical_anchor = valign
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = text
    r.font.name = font
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.color.rgb = color
    return box


def add_rich_text(slide, runs, x, y, w, h, *, size=18, align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.03)
    tf.margin_top = tf.margin_bottom = Inches(0.03)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = align
    for text, color, bold in runs:
        r = p.add_run()
        r.text = text
        r.font.name = FONT_CN
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = color
    return box


def add_box(
    slide,
    x,
    y,
    w,
    h,
    *,
    fill=WHITE,
    line=BLUE,
    radius=True,
    line_width=1.2,
    shadow=False,
):
    shape_type = (
        MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE
        if radius
        else MSO_AUTO_SHAPE_TYPE.RECTANGLE
    )
    shp = slide.shapes.add_shape(
        shape_type, Inches(x), Inches(y), Inches(w), Inches(h)
    )
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    shp.line.color.rgb = line
    shp.line.width = Pt(line_width)
    if shadow:
        shp.shadow.inherit = False
    return shp


def add_circle(slide, x, y, d, *, fill=WHITE, line=BLUE, width=1.2):
    shp = slide.shapes.add_shape(
        MSO_AUTO_SHAPE_TYPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d)
    )
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    shp.line.color.rgb = line
    shp.line.width = Pt(width)
    return shp


def add_line(
    slide,
    x1,
    y1,
    x2,
    y2,
    *,
    color=BLUE,
    width=1.6,
    arrow=False,
    dash=False,
):
    line = slide.shapes.add_connector(
        MSO_CONNECTOR.STRAIGHT,
        Inches(x1),
        Inches(y1),
        Inches(x2),
        Inches(y2),
    )
    line.line.color.rgb = color
    line.line.width = Pt(width)
    if arrow:
        line_xml = line.line._get_or_add_ln()
        arrow_xml = OxmlElement("a:tailEnd")
        arrow_xml.set("type", "triangle")
        line_xml.append(arrow_xml)
    if dash:
        line.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    return line


def add_title(slide, title, subtitle=None):
    add_text(slide, title, 0.65, 0.28, 11.9, 0.55, size=25, bold=True)
    add_line(slide, 0.65, 0.92, 12.65, 0.92, color=LIGHT, width=0.8)
    if subtitle:
        add_text(slide, subtitle, 9.6, 0.32, 3.0, 0.35, size=9, color=MID, align=PP_ALIGN.RIGHT)


def add_footer(slide, index, source="Luo et al., VCM, arXiv:2504.19627v2 (2025)"):
    add_text(slide, source, 0.65, 7.08, 10.8, 0.2, size=7, color=MID)
    add_text(slide, str(index), 12.1, 7.04, 0.5, 0.22, size=8, color=MID, align=PP_ALIGN.RIGHT)


def add_callout(slide, text, *, y=6.18, color=BLUE):
    add_box(slide, 1.25, y, 10.83, 0.55, fill=WHITE, line=color, radius=False, line_width=1.1)
    add_text(slide, text, 1.45, y + 0.06, 10.43, 0.42, size=15, bold=True, color=color, align=PP_ALIGN.CENTER)


def add_bullet_list(slide, items, x, y, w, h, *, size=16, color=INK, spacing=8):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.margin_left = Inches(0.08)
    tf.margin_right = Inches(0.03)
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = item
        p.level = 0
        p.font.name = FONT_CN
        p.font.size = Pt(size)
        p.font.color.rgb = color
        p.space_after = Pt(spacing)
        p.text = "• " + item
    return box


def add_token_grid(slide, x, y, cols, rows, *, active=None, cell=0.25, gap=0.04):
    active = set(active or [])
    for r in range(rows):
        for c in range(cols):
            idx = r * cols + c
            fill = BLUE if idx in active else RGBColor(218, 225, 232)
            line = NAVY if idx in active else WHITE
            add_box(
                slide,
                x + c * (cell + gap),
                y + r * (cell + gap),
                cell,
                cell,
                fill=fill,
                line=line,
                radius=False,
                line_width=0.4,
            )


def add_native_chart(
    slide,
    categories,
    series,
    x,
    y,
    w,
    h,
    *,
    chart_type=XL_CHART_TYPE.COLUMN_CLUSTERED,
    colors=None,
    ymin=0,
    ymax=None,
    legend=True,
    value_format="0.0",
):
    data = CategoryChartData()
    data.categories = categories
    for name, values in series:
        data.add_series(name, values)
    chart = slide.shapes.add_chart(
        chart_type, Inches(x), Inches(y), Inches(w), Inches(h), data
    ).chart
    chart.has_title = False
    chart.has_legend = legend
    if legend:
        chart.legend.position = XL_LEGEND_POSITION.BOTTOM
        chart.legend.include_in_layout = False
        chart.legend.font.size = Pt(9)
    chart.value_axis.minimum_scale = ymin
    if ymax is not None:
        chart.value_axis.maximum_scale = ymax
    chart.value_axis.has_major_gridlines = True
    chart.value_axis.major_gridlines.format.line.color.rgb = LIGHT
    chart.value_axis.tick_labels.font.size = Pt(9)
    chart.value_axis.tick_labels.number_format = value_format
    chart.category_axis.tick_labels.font.size = Pt(9)
    chart.category_axis.format.line.color.rgb = MID
    chart.value_axis.format.line.color.rgb = MID
    palette = colors or [BLUE, ORANGE, GREEN, RED]
    for i, ser in enumerate(chart.series):
        ser.format.fill.solid()
        ser.format.fill.fore_color.rgb = palette[i % len(palette)]
        ser.format.line.color.rgb = palette[i % len(palette)]
    return chart


def new_slide(prs, *, bg=WHITE):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = bg
    return slide


def build_deck():
    prs = Presentation()
    prs.slide_width = W
    prs.slide_height = H
    prs.core_properties.title = "VCM：基于指令的自适应视觉概念建模"
    prs.core_properties.subject = "Editable research presentation"
    prs.core_properties.author = "Generated from Luo et al. (2025)"
    prs.core_properties.comments = (
        "Diagrams and charts are native editable PowerPoint objects."
    )

    # 1 — Title
    s = new_slide(prs, bg=NAVY)
    add_text(s, "VCM", 0.75, 1.10, 2.2, 0.75, size=38, bold=True, color=WHITE, font=FONT_EN)
    add_text(
        s,
        "Vision Concept Modeling with Adaptive Vision Token\nCompression via Instruction Fine-Tuning",
        0.78,
        1.88,
        8.8,
        1.40,
        size=25,
        bold=True,
        color=WHITE,
        valign=MSO_ANCHOR.TOP,
        font=FONT_EN,
    )
    add_text(s, "从 token-level 冗余到 instruction-aware vision concepts", 0.80, 3.53, 8.7, 0.55, size=18, color=RGBColor(181, 219, 245))
    for i, col in enumerate([CYAN, BLUE, ORANGE, GREEN]):
        add_circle(s, 10.0 + (i % 2) * 1.1, 1.35 + (i // 2) * 1.1, 0.72, fill=col, line=WHITE, width=0.6)
        add_text(s, ["图像", "指令", "概念", "回答"][i], 9.99 + (i % 2) * 1.1, 1.46 + (i // 2) * 1.1, 0.74, 0.3, size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_line(s, 10.72, 1.72, 11.1, 1.72, color=WHITE, arrow=True)
    add_line(s, 11.45, 2.08, 11.45, 2.43, color=WHITE, arrow=True)
    add_text(s, "论文逻辑凝练 · 可编辑科研汇报", 0.80, 6.52, 5.0, 0.35, size=12, color=WHITE)
    add_text(s, "Luo et al. · arXiv:2504.19627v2 · 2025", 8.35, 6.52, 4.2, 0.35, size=10, color=WHITE, align=PP_ALIGN.RIGHT)

    # 2 — Problem
    s = new_slide(prs)
    add_title(s, "LVLM 的现实瓶颈：看得越多，算得越重")
    add_text(s, "高分辨率图像 / 长视频", 0.8, 1.22, 3.0, 0.4, size=17, bold=True, align=PP_ALIGN.CENTER)
    add_token_grid(s, 1.12, 1.85, 10, 7, cell=0.22, gap=0.05)
    add_text(s, "576+ vision tokens", 1.2, 4.06, 2.9, 0.35, size=14, bold=True, color=RED, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_line(s, 4.35, 2.8, 5.15, 2.8, color=RED, width=2.2, arrow=True)
    add_box(s, 5.25, 1.62, 2.2, 2.35, fill=PALE_BLUE, line=BLUE)
    add_text(s, "LLM", 5.73, 2.05, 1.25, 0.45, size=26, bold=True, color=NAVY, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_text(s, "Self-Attention\n计算随序列长度快速增长", 5.52, 2.65, 1.7, 0.82, size=13, color=MID, align=PP_ALIGN.CENTER)
    add_line(s, 7.65, 2.8, 8.45, 2.8, color=RED, width=2.2, arrow=True)
    for i, (t, c) in enumerate([("FLOPs ↑", RED), ("Latency ↑", ORANGE), ("Memory ↑", NAVY)]):
        add_box(s, 8.60, 1.45 + i * 1.0, 2.4, 0.64, fill=WHITE, line=c)
        add_text(s, t, 8.72, 1.54 + i * 1.0, 2.15, 0.42, size=18, bold=True, color=c, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_callout(s, "核心矛盾：当前 LVLM 处理所有视觉 token，而人类按任务选择少量高层概念")
    add_footer(s, 2)

    # 3 — Cognitive contrast
    s = new_slide(prs)
    add_title(s, "从“处理整幅图”转向“提取任务相关概念”")
    add_text(s, "Token-level processing", 0.9, 1.25, 4.9, 0.4, size=19, bold=True, color=MID, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_token_grid(s, 1.78, 1.92, 12, 7, cell=0.23, gap=0.05)
    add_text(s, "每个 patch 都进入 LLM", 1.35, 4.28, 4.0, 0.4, size=15, color=MID, align=PP_ALIGN.CENTER)
    add_line(s, 5.82, 3.0, 7.25, 3.0, color=BLUE, width=3, arrow=True)
    add_text(s, "instruction", 6.0, 2.48, 1.1, 0.35, size=12, bold=True, color=BLUE, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_text(s, "Concept-level processing", 7.35, 1.25, 4.9, 0.4, size=19, bold=True, color=NAVY, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_token_grid(s, 8.18, 1.92, 12, 7, active={18, 19, 20, 30, 31, 32, 42, 43}, cell=0.23, gap=0.05)
    add_text(s, "只保留与问题相关的区域 / 概念", 7.75, 4.28, 4.0, 0.4, size=15, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
    add_callout(s, "Compression ≠ 丢弃信息；VCM 的目标是压缩冗余，同时保留可解释的空间语义")
    add_footer(s, 3)

    # 4 — Definition
    s = new_slide(prs)
    add_title(s, "Vision Concept Model：由指令决定“看多少、看哪里”")
    add_box(s, 0.9, 1.35, 2.6, 1.10, fill=PALE_BLUE, line=BLUE)
    add_text(s, "图像 Xᴠ", 1.25, 1.55, 1.9, 0.45, size=23, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
    add_box(s, 0.9, 3.35, 2.6, 1.10, fill=WHITE, line=ORANGE)
    add_text(s, "任务指令 Xɪ", 1.18, 3.55, 2.0, 0.45, size=23, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)
    add_line(s, 3.55, 1.90, 4.50, 2.70, color=BLUE, width=2, arrow=True)
    add_line(s, 3.55, 3.90, 4.50, 3.10, color=ORANGE, width=2, arrow=True)
    add_box(s, 4.60, 1.72, 3.05, 2.52, fill=LIGHT_BLUE, line=NAVY, line_width=1.8)
    add_text(s, "VCM", 5.32, 2.05, 1.6, 0.5, size=30, bold=True, color=NAVY, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_text(s, "Adaptive quantity\n+\nSpatial alignment", 5.05, 2.66, 2.15, 1.10, size=16, color=INK, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_line(s, 7.75, 2.96, 8.70, 2.96, color=GREEN, width=2.4, arrow=True)
    for i, (label, color) in enumerate([("概念 1", BLUE), ("概念 2", GREEN), ("概念 K", ORANGE)]):
        add_circle(s, 8.88 + i * 1.05, 2.45, 0.85, fill=color, line=WHITE)
        add_text(s, label, 8.91 + i * 1.05, 2.67, 0.79, 0.28, size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_rich_text(s, [("输出长度 ", INK, False), ("K", RED, True), (" 随样本与指令动态变化", INK, False)], 8.65, 3.55, 3.6, 0.55, size=16, align=PP_ALIGN.CENTER)
    add_callout(s, "形式化定义：从固定数量的 vision tokens，升级为 instruction-conditioned vision concepts")
    add_footer(s, 4)

    # 5 — Prior methods
    s = new_slide(prs)
    add_title(s, "为什么已有 token reduction 还不是 Vision Concept Model？")
    headers = ["Prune", "Merge / Query", "VCM"]
    subtitles = ["按 attention 阈值删除", "压为固定长度", "自适应局部合并 + 过滤"]
    colors = [MID, ORANGE, BLUE]
    for j in range(3):
        x = 0.75 + j * 4.15
        add_box(s, x, 1.25, 3.65, 4.65, fill=WHITE if j < 2 else PALE_BLUE, line=colors[j], line_width=1.5)
        add_text(s, headers[j], x + 0.2, 1.48, 3.25, 0.42, size=22, bold=True, color=colors[j], align=PP_ALIGN.CENTER, font=FONT_EN)
        add_text(s, subtitles[j], x + 0.25, 1.95, 3.15, 0.55, size=14, color=INK, align=PP_ALIGN.CENTER)
        if j == 0:
            add_token_grid(s, x + 0.68, 2.78, 8, 4, active={1, 9, 10, 18, 26}, cell=0.20, gap=0.05)
            detail = "长度难控制\n可能破坏语义连续性"
        elif j == 1:
            for i in range(5):
                add_circle(s, x + 0.55 + i * 0.55, 3.00, 0.38, fill=ORANGE, line=WHITE)
            detail = "固定 query 数量\n空间关系容易丢失"
        else:
            add_token_grid(s, x + 0.68, 2.78, 8, 4, active={9, 10, 11, 18, 19}, cell=0.20, gap=0.05)
            detail = "长度可控\n保留相对顺序与位置"
        add_text(s, detail, x + 0.45, 4.35, 2.75, 0.85, size=15, bold=j == 2, color=colors[j], align=PP_ALIGN.CENTER)
    add_callout(s, "VCM 不只追求“更少的 token”，而是学习具有语义与空间对应关系的概念")
    add_footer(s, 5)

    # 6 — Empirical clue
    s = new_slide(prs)
    add_title(s, "关键观察：最小视觉长度与文本先验存在稳定相关性")
    add_box(s, 0.8, 1.30, 3.65, 3.95, fill=WHITE, line=BLUE)
    add_text(s, "Response keywords ↑", 1.18, 1.58, 2.9, 0.35, size=17, bold=True, color=BLUE, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_line(s, 1.25, 4.55, 3.90, 4.55, color=MID)
    add_line(s, 1.25, 4.55, 1.25, 2.20, color=MID)
    add_line(s, 1.55, 4.15, 3.58, 2.45, color=BLUE, width=3)
    add_text(s, "需要的 vision length ↑", 1.30, 4.72, 3.0, 0.25, size=11, color=MID, align=PP_ALIGN.CENTER)
    add_box(s, 4.85, 1.30, 3.65, 3.95, fill=WHITE, line=ORANGE)
    add_text(s, "Instruction keywords ↑", 5.18, 1.58, 3.0, 0.35, size=17, bold=True, color=ORANGE, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_line(s, 5.30, 4.55, 7.95, 4.55, color=MID)
    add_line(s, 5.30, 4.55, 5.30, 2.20, color=MID)
    add_line(s, 5.62, 2.45, 7.65, 4.15, color=ORANGE, width=3)
    add_text(s, "问题越具体，所需视觉信息越少", 5.38, 4.72, 3.0, 0.25, size=11, color=MID, align=PP_ALIGN.CENTER)
    add_box(s, 8.90, 1.30, 3.65, 3.95, fill=PALE_BLUE, line=NAVY)
    add_text(s, "Δ keywords", 9.55, 1.58, 2.35, 0.35, size=17, bold=True, color=NAVY, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_line(s, 9.35, 4.55, 12.00, 4.55, color=MID)
    add_line(s, 9.35, 4.55, 9.35, 2.20, color=MID)
    add_line(s, 9.68, 2.55, 11.72, 4.10, color=NAVY, width=3)
    add_text(s, "response − instruction\n更稳定的估计信号", 9.55, 4.67, 2.3, 0.48, size=11, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
    add_callout(s, "利用粗粒度 instruction–response 数据，即可自监督估计每个样本需要多少 vision concepts")
    add_footer(s, 6, source="Paper Fig. 2; correlations estimated on 5K LLaVA instruction-tuning instances")

    # 7 — Challenges and solution map
    s = new_slide(prs)
    add_title(s, "两个挑战，对应两条技术路线")
    add_circle(s, 1.15, 1.72, 0.75, fill=RED, line=WHITE)
    add_text(s, "1", 1.31, 1.87, 0.42, 0.3, size=18, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text(s, "缺少 fine-grained concept annotations", 2.05, 1.72, 4.25, 0.48, size=21, bold=True)
    add_line(s, 6.30, 2.10, 7.10, 2.10, color=BLUE, width=2.5, arrow=True)
    add_box(s, 7.22, 1.42, 4.85, 1.38, fill=PALE_BLUE, line=BLUE)
    add_text(s, "Semantic alignment + implicit contrastive sampling", 7.53, 1.62, 4.22, 0.50, size=17, bold=True, color=NAVY, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_text(s, "从指令与回答中自动寻找 image-relevant keywords", 7.62, 2.17, 4.05, 0.35, size=13, color=MID, align=PP_ALIGN.CENTER)
    add_circle(s, 1.15, 3.82, 0.75, fill=ORANGE, line=WHITE)
    add_text(s, "2", 1.31, 3.97, 0.42, 0.3, size=18, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text(s, "不同样本需要不同 concept length", 2.05, 3.82, 4.25, 0.48, size=21, bold=True)
    add_line(s, 6.30, 4.20, 7.10, 4.20, color=ORANGE, width=2.5, arrow=True)
    add_box(s, 7.22, 3.52, 4.85, 1.38, fill=WHITE, line=ORANGE)
    add_text(s, "Forward–backward dynamic programming", 7.53, 3.72, 4.22, 0.50, size=17, bold=True, color=ORANGE, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_text(s, "O(2ᴹ) 搜索 → O(M²) 可优化目标", 7.62, 4.27, 4.05, 0.35, size=13, color=MID, align=PP_ALIGN.CENTER)
    add_callout(s, "VCM = 文本先验提供“目标长度” + 动态规划学习“具体位置”")
    add_footer(s, 7)

    # 8 — Overall architecture
    s = new_slide(prs)
    add_title(s, "VCM 总体框架：先学习语义，再学习动态概念")
    stages = [
        ("① Pre-training", "Semantic alignment", BLUE),
        ("② Instruction FT", "Keyword selection", ORANGE),
        ("③ VCM optimization", "Forward–backward", GREEN),
        ("④ Inference", "Concept → LLM", NAVY),
    ]
    for i, (head, body, col) in enumerate(stages):
        x = 0.65 + i * 3.16
        add_box(s, x, 1.55, 2.65, 3.38, fill=PALE_BLUE if i in (0, 2) else WHITE, line=col, line_width=1.5)
        add_text(s, head, x + 0.18, 1.80, 2.29, 0.4, size=16, bold=True, color=col, align=PP_ALIGN.CENTER, font=FONT_EN)
        add_text(s, body, x + 0.18, 2.32, 2.29, 0.55, size=18, bold=True, color=INK, align=PP_ALIGN.CENTER, font=FONT_EN)
        if i == 0:
            add_circle(s, x + 0.48, 3.33, 0.55, fill=BLUE, line=WHITE)
            add_circle(s, x + 1.08, 3.33, 0.55, fill=CYAN, line=WHITE)
            add_circle(s, x + 1.68, 3.33, 0.55, fill=NAVY, line=WHITE)
            add_text(s, "Gᵀ   Gⱽ   Gᴸᴸᴹ", x + 0.35, 4.08, 1.95, 0.28, size=12, color=MID, align=PP_ALIGN.CENTER, font=FONT_EN)
        elif i == 1:
            for k, t in enumerate(["person", "yellow", "?"]):
                add_box(s, x + 0.35 + k * 0.65, 3.28, 0.58, 0.55, fill=ORANGE if k < 2 else LIGHT, line=WHITE, radius=False)
                add_text(s, t, x + 0.36 + k * 0.65, 3.38, 0.56, 0.3, size=8, color=WHITE if k < 2 else MID, align=PP_ALIGN.CENTER, font=FONT_EN)
            add_text(s, "K > E(K)", x + 0.72, 4.08, 1.25, 0.28, size=12, bold=True, color=ORANGE, align=PP_ALIGN.CENTER, font=FONT_EN)
        elif i == 2:
            add_text(s, "∅  ★  ∅  ★  ∅", x + 0.35, 3.22, 1.95, 0.4, size=20, bold=True, color=GREEN, align=PP_ALIGN.CENTER, font=FONT_EN)
            add_text(s, "α(t,l)  ↔  β(t,l)", x + 0.35, 3.87, 1.95, 0.35, size=13, color=MID, align=PP_ALIGN.CENTER, font=FONT_EN)
        else:
            add_token_grid(s, x + 0.45, 3.22, 7, 3, active={2, 3, 9, 10}, cell=0.20, gap=0.04)
            add_text(s, "Hᵥ → Hᵥᶜ", x + 0.55, 4.12, 1.55, 0.3, size=13, bold=True, color=NAVY, align=PP_ALIGN.CENTER, font=FONT_EN)
        if i < 3:
            add_line(s, x + 2.67, 3.25, x + 3.10, 3.25, color=MID, width=1.7, arrow=True)
    add_callout(s, "训练时：用粗监督学习可变长度概念；推理时：把少量 Hᵥᶜ 与指令一起送入 LLM")
    add_footer(s, 8, source="Editable reconstruction of the paper's Figure 3 workflow")

    # 9 — Semantic alignment
    s = new_slide(prs)
    add_title(s, "阶段一：Semantic Alignment 让关键词选择器理解“图文相关”")
    nodes = [
        (1.0, 1.55, "Instruction\n+ Response", ORANGE),
        (1.0, 3.45, "Image", BLUE),
        (4.05, 1.55, "Keyword\nSelector", ORANGE),
        (4.05, 3.45, "Vision\nEncoder", BLUE),
        (7.10, 1.55, "Global Text\nGᵀ", ORANGE),
        (7.10, 3.45, "Global Vision\nGⱽ", BLUE),
        (10.15, 2.52, "LM Head\nsemantic space", NAVY),
    ]
    for x, y, label, col in nodes:
        add_box(s, x, y, 2.15, 0.95, fill=PALE_BLUE if col in (BLUE, NAVY) else WHITE, line=col)
        add_text(s, label, x + 0.15, y + 0.15, 1.85, 0.65, size=15, bold=True, color=col, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_line(s, 3.16, 2.02, 4.02, 2.02, color=ORANGE, arrow=True)
    add_line(s, 3.16, 3.92, 4.02, 3.92, color=BLUE, arrow=True)
    add_line(s, 6.21, 2.02, 7.07, 2.02, color=ORANGE, arrow=True)
    add_line(s, 6.21, 3.92, 7.07, 3.92, color=BLUE, arrow=True)
    add_line(s, 9.28, 2.02, 10.10, 2.72, color=ORANGE, arrow=True)
    add_line(s, 9.28, 3.92, 10.10, 3.22, color=BLUE, arrow=True)
    add_box(s, 4.88, 5.00, 3.55, 0.75, fill=LIGHT_BLUE, line=NAVY)
    add_text(s, "Lₛₐ：对齐 Gᵀ、Gⱽ 与 Gᴸᴸᴹ 的语义分布", 5.05, 5.15, 3.22, 0.42, size=15, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
    add_callout(s, "目的不是直接标注概念，而是让 selector 学会哪些词与当前图像真正相关", y=6.20)
    add_footer(s, 9)

    # 10 — Keyword selection
    s = new_slide(prs)
    add_title(s, "阶段二：从 instruction–response 中自适应选择 image-relevant keywords")
    sentence = ["Where", "is", "the", "person", "in", "yellow", "?"]
    scores = [0.03, 0.01, 0.03, 0.51, 0.02, 0.39, 0.01]
    start = 0.78
    for i, (word, score) in enumerate(zip(sentence, scores)):
        active = score > sum(scores) / len(scores)
        col = RED if active else LIGHT
        txt = WHITE if active else MID
        add_box(s, start + i * 1.72, 1.55, 1.43, 0.70, fill=col, line=WHITE, radius=False)
        add_text(s, word, start + i * 1.72, 1.67, 1.43, 0.33, size=15, bold=active, color=txt, align=PP_ALIGN.CENTER, font=FONT_EN)
        add_text(s, f"{score:.2f}", start + i * 1.72, 2.33, 1.43, 0.30, size=11, color=RED if active else MID, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_text(s, "Softmax similarity score K", 4.58, 2.82, 4.1, 0.38, size=14, color=MID, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_line(s, 6.62, 3.25, 6.62, 3.78, color=BLUE, width=2, arrow=True)
    add_box(s, 4.28, 3.88, 4.70, 0.82, fill=PALE_BLUE, line=BLUE)
    add_rich_text(s, [("阈值：", INK, False), (" K > E(K) ", RED, True), ("→ {person, yellow}", INK, False)], 4.55, 4.05, 4.16, 0.42, size=17, align=PP_ALIGN.CENTER)
    add_box(s, 1.28, 5.08, 4.40, 0.72, fill=WHITE, line=ORANGE)
    add_text(s, "随机 mask keywords → 构造隐式对比样本", 1.53, 5.23, 3.9, 0.4, size=15, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)
    add_box(s, 7.55, 5.08, 4.40, 0.72, fill=WHITE, line=GREEN)
    add_text(s, "mask 越多 → 目标 concept length 越长", 7.80, 5.23, 3.9, 0.4, size=15, bold=True, color=GREEN, align=PP_ALIGN.CENTER)
    add_footer(s, 10)

    # 11 — Length estimation
    s = new_slide(prs)
    add_title(s, "目标长度估计：把文本先验映射为每个样本的 concept budget")
    add_box(s, 0.9, 1.52, 3.0, 1.28, fill=WHITE, line=ORANGE)
    add_text(s, "Nₖₑᵧ", 1.75, 1.72, 1.3, 0.45, size=29, bold=True, color=ORANGE, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_text(s, "instruction 与 response\n关键词数量差", 1.40, 2.18, 2.0, 0.45, size=12, color=MID, align=PP_ALIGN.CENTER)
    add_line(s, 3.95, 2.17, 4.87, 2.17, color=BLUE, width=2.3, arrow=True)
    add_box(s, 4.97, 1.52, 3.38, 1.28, fill=PALE_BLUE, line=BLUE)
    add_text(s, "Min–max normalization", 5.25, 1.78, 2.82, 0.35, size=17, bold=True, color=BLUE, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_text(s, "控制信息需求比例", 5.55, 2.22, 2.2, 0.32, size=12, color=MID, align=PP_ALIGN.CENTER)
    add_line(s, 8.42, 2.17, 9.32, 2.17, color=GREEN, width=2.3, arrow=True)
    add_box(s, 9.42, 1.52, 2.95, 1.28, fill=WHITE, line=GREEN)
    add_text(s, "Target length L", 9.75, 1.78, 2.3, 0.35, size=19, bold=True, color=GREEN, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_text(s, "动态、样本级", 9.92, 2.22, 2.0, 0.32, size=12, color=MID, align=PP_ALIGN.CENTER)
    add_box(s, 2.05, 3.35, 9.25, 1.02, fill=LIGHT_BLUE, line=NAVY, radius=False)
    add_text(s, "L = ⌊ M · S · (1 − Norm(Nₖₑᵧ)) ⌋", 2.45, 3.57, 8.45, 0.52, size=27, bold=True, color=NAVY, align=PP_ALIGN.CENTER, font=FONT_EN)
    labels = [("M", "原始 token 数"), ("S", "information domain"), ("r", "mask ratio 控制柄")]
    for i, (symbol, label) in enumerate(labels):
        x = 2.10 + i * 3.20
        add_circle(s, x, 4.82, 0.58, fill=[BLUE, ORANGE, GREEN][i], line=WHITE)
        add_text(s, symbol, x + 0.12, 4.95, 0.34, 0.24, size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER, font=FONT_EN)
        add_text(s, label, x + 0.72, 4.85, 2.15, 0.45, size=13, color=INK)
    add_callout(s, "文本先验只告诉模型“保留多少”，下一步仍需解决“保留哪些位置”")
    add_footer(s, 11)

    # 12 — Forward-backward
    s = new_slide(prs)
    add_title(s, "Forward–Backward：在所有合法对齐路径上学习 token 位置")
    add_text(s, "Input vision sequence Yᵥ", 0.78, 1.20, 2.55, 0.35, size=15, bold=True, color=BLUE, font=FONT_EN)
    for i in range(8):
        add_box(s, 0.82 + i * 0.63, 1.70, 0.46, 0.46, fill=BLUE, line=WHITE, radius=False)
        add_text(s, f"y{i+1}", 0.84 + i * 0.63, 1.79, 0.42, 0.23, size=9, color=WHITE, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_text(s, "Extended target Zᵥ", 7.22, 1.20, 2.55, 0.35, size=15, bold=True, color=GREEN, font=FONT_EN)
    target = ["∅", "★", "∅", "★", "∅"]
    for i, t in enumerate(target):
        fill = GREEN if t == "★" else WHITE
        add_circle(s, 7.35 + i * 0.84, 1.63, 0.54, fill=fill, line=GREEN)
        add_text(s, t, 7.45 + i * 0.84, 1.75, 0.34, 0.24, size=14, bold=True, color=WHITE if t == "★" else GREEN, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_text(s, "α(t,l)", 1.15, 2.80, 1.45, 0.52, size=25, bold=True, color=BLUE, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_text(s, "Forward\nprefix alignment", 1.10, 3.32, 1.55, 0.72, size=13, color=MID, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_line(s, 2.75, 3.25, 4.50, 3.25, color=BLUE, width=2.5, arrow=True)
    add_box(s, 4.62, 2.55, 4.10, 1.38, fill=PALE_BLUE, line=NAVY)
    add_text(s, "p(Zᵥ|Yᵥ) = Σₗ α(t,l) · β(t,l)", 4.90, 2.83, 3.55, 0.38, size=20, bold=True, color=NAVY, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_text(s, "Lᵥ꜀ₘ = −log p(Zᵥ|Yᵥ)", 5.13, 3.32, 3.10, 0.33, size=16, color=RED, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_line(s, 8.84, 3.25, 10.55, 3.25, color=GREEN, width=2.5, arrow=True)
    add_text(s, "β(t,l)", 10.65, 2.80, 1.45, 0.52, size=25, bold=True, color=GREEN, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_text(s, "Backward\nsuffix alignment", 10.60, 3.32, 1.55, 0.72, size=13, color=MID, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_box(s, 1.38, 4.72, 3.05, 0.70, fill=WHITE, line=RED)
    add_text(s, "暴力枚举：O(2ᴹ)", 1.65, 4.86, 2.52, 0.38, size=17, bold=True, color=RED, align=PP_ALIGN.CENTER)
    add_line(s, 4.55, 5.06, 5.18, 5.06, color=MID, arrow=True)
    add_box(s, 5.32, 4.72, 3.05, 0.70, fill=PALE_BLUE, line=BLUE)
    add_text(s, "动态规划：O(M²)", 5.58, 4.86, 2.52, 0.38, size=17, bold=True, color=BLUE, align=PP_ALIGN.CENTER)
    add_line(s, 8.50, 5.06, 9.12, 5.06, color=MID, arrow=True)
    add_box(s, 9.25, 4.72, 2.72, 0.70, fill=WHITE, line=GREEN)
    add_text(s, "可端到端优化", 9.53, 4.86, 2.18, 0.38, size=17, bold=True, color=GREEN, align=PP_ALIGN.CENTER)
    add_callout(s, "训练最大化所有可行路径；推理选择最可能路径，再进行 Segment Merging")
    add_footer(s, 12)

    # 13 — Segment merging
    s = new_slide(prs)
    add_title(s, "从 token 到 concept：选择路径后进行连续片段加权合并")
    add_text(s, "Vision tokens", 0.85, 1.30, 2.0, 0.35, size=16, bold=True, color=BLUE, font=FONT_EN)
    probs = [0.10, 0.82, 0.75, 0.12, 0.88, 0.79, 0.15, 0.08]
    for i, p in enumerate(probs):
        active = p > 0.5
        add_box(s, 0.88 + i * 0.72, 1.86, 0.55, 0.72, fill=BLUE if active else LIGHT, line=WHITE, radius=False)
        add_text(s, f"{p:.2f}", 0.90 + i * 0.72, 2.08, 0.51, 0.25, size=8, color=WHITE if active else MID, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_text(s, "★   ★        ★   ★", 1.52, 2.73, 4.1, 0.35, size=18, bold=True, color=GREEN, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_line(s, 6.75, 2.25, 7.45, 2.25, color=GREEN, width=2.5, arrow=True)
    add_box(s, 7.62, 1.55, 1.65, 1.35, fill=LIGHT_BLUE, line=BLUE)
    add_text(s, "Concept 1", 7.85, 2.00, 1.18, 0.35, size=14, bold=True, color=NAVY, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_box(s, 9.72, 1.55, 1.65, 1.35, fill=RGBColor(232, 247, 240), line=GREEN)
    add_text(s, "Concept 2", 9.95, 2.00, 1.18, 0.35, size=14, bold=True, color=GREEN, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_text(s, "score-weighted average", 7.65, 3.02, 3.68, 0.35, size=12, color=MID, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_line(s, 8.45, 3.55, 8.45, 4.05, color=NAVY, arrow=True)
    add_line(s, 10.55, 3.55, 10.55, 4.05, color=NAVY, arrow=True)
    add_box(s, 7.42, 4.15, 4.20, 1.10, fill=PALE_BLUE, line=NAVY)
    add_text(s, "[Global token; Hᵥᶜ; Instruction]", 7.70, 4.36, 3.65, 0.35, size=16, bold=True, color=NAVY, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_text(s, "→ Large Language Model", 7.93, 4.75, 3.18, 0.28, size=13, color=MID, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_box(s, 0.98, 3.70, 4.85, 1.34, fill=WHITE, line=ORANGE)
    add_text(s, "物理含义", 1.23, 3.92, 1.05, 0.35, size=15, bold=True, color=ORANGE)
    add_text(s, "连续保留区域形成一个 concept；\n相邻关系与空间顺序不被打乱", 2.25, 3.80, 3.30, 0.80, size=15)
    add_callout(s, "Segment Merging 的并行实现比双重循环快约 100×（论文 Appendix E）")
    add_footer(s, 13)

    # 14 — Efficiency
    s = new_slide(prs)
    add_title(s, "结果一：显著减少计算量，同时保持强性能")
    chart = add_native_chart(
        s,
        ["Baseline\n576", "VCM\n128", "VCM\n64"],
        [("FLOPs (T)", [4.62, 1.71, 1.24])],
        0.80,
        1.35,
        5.60,
        4.35,
        colors=[BLUE],
        ymax=5.0,
        legend=False,
    )
    chart.value_axis.has_title = True
    chart.value_axis.axis_title.text_frame.text = "FLOPs (T)"
    chart.value_axis.axis_title.text_frame.paragraphs[0].font.size = Pt(10)
    add_box(s, 6.85, 1.48, 2.15, 1.58, fill=PALE_BLUE, line=BLUE, line_width=1.8)
    add_text(s, "85%", 7.10, 1.70, 1.65, 0.62, size=39, bold=True, color=BLUE, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_text(s, "理论 FLOPs reduction", 7.06, 2.38, 1.75, 0.35, size=11, color=MID, align=PP_ALIGN.CENTER)
    add_box(s, 9.45, 1.48, 2.15, 1.58, fill=WHITE, line=ORANGE, line_width=1.8)
    add_text(s, "31.42 ms", 9.63, 1.80, 1.78, 0.48, size=25, bold=True, color=ORANGE, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_text(s, "VCM-128 latency", 9.72, 2.38, 1.60, 0.35, size=11, color=MID, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_box(s, 6.85, 3.56, 4.75, 1.42, fill=WHITE, line=GREEN)
    add_text(s, "62.0% Avg.", 7.15, 3.80, 1.55, 0.45, size=24, bold=True, color=GREEN, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_text(s, "VCM-128", 7.34, 4.30, 1.18, 0.28, size=10, color=MID, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_text(s, "vs.", 8.80, 3.98, 0.50, 0.3, size=12, color=MID, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_text(s, "61.6% Avg.", 9.45, 3.80, 1.55, 0.45, size=24, bold=True, color=MID, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_text(s, "LLaVA-1.5", 9.58, 4.30, 1.30, 0.28, size=10, color=MID, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_callout(s, "压缩带来的不是单纯速度收益：VCM-128 的平均表现还略高于 576-token baseline")
    add_footer(s, 14, source="Paper Appendix D and Table 10")

    # 15 — VQA comparison
    s = new_slide(prs)
    add_title(s, "结果二：仅用 144 tokens，11 个 VQA benchmark 平均性能更高")
    methods = ["FastV\n192", "PDrop\n192", "SparseVLM\n192", "VisionZip\n192", "LLaVA\n576", "VCM\n144"]
    scores = [53.1, 57.8, 57.9, 59.1, 59.5, 60.8]
    chart = add_native_chart(
        s,
        methods,
        [("Average (%)", scores)],
        0.78,
        1.35,
        7.15,
        4.45,
        colors=[BLUE],
        ymin=50,
        ymax=62,
        legend=False,
    )
    # highlight VCM point/bar
    chart.series[0].points[5].format.fill.solid()
    chart.series[0].points[5].format.fill.fore_color.rgb = RED
    chart.series[0].points[5].format.line.color.rgb = RED
    add_box(s, 8.40, 1.52, 3.82, 1.15, fill=PALE_BLUE, line=NAVY)
    add_text(s, "144 / 576", 8.75, 1.72, 3.12, 0.46, size=28, bold=True, color=NAVY, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_text(s, "仅保留 25% vision tokens", 8.90, 2.20, 2.82, 0.28, size=11, color=MID, align=PP_ALIGN.CENTER)
    for i, (metric, value, col) in enumerate([
        ("VizWiz", "+4.9", BLUE),
        ("SEED", "+5.7", GREEN),
        ("MMStar", "+2.5", ORANGE),
    ]):
        y = 3.10 + i * 0.78
        add_text(s, metric, 8.70, y, 1.30, 0.38, size=14, bold=True, color=MID, font=FONT_EN)
        add_text(s, value, 10.35, y, 1.20, 0.38, size=18, bold=True, color=col, align=PP_ALIGN.RIGHT, font=FONT_EN)
    add_text(s, "Δ vs. LLaVA-v1.5", 9.02, 5.52, 2.55, 0.28, size=10, color=MID, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_callout(s, "VCM 以更少的 token 获得最高平均分，说明学习到的 concepts 比简单剪枝更具表示力")
    add_footer(s, 15, source="Paper Table 1; averages reported by the authors")

    # 16 — Dense perception
    s = new_slide(prs)
    add_title(s, "结果三：压缩之外，VCM 还增强 dense perception")
    add_native_chart(
        s,
        ["BBox testA", "BBox testB", "Mask val", "Top-1\nThing", "Top-1\nStuff"],
        [
            ("w/o VCM", [14.9, 40.1, 29.6, 28.3, 11.8]),
            ("w/ VCM", [16.5, 41.3, 31.9, 43.8, 25.4]),
        ],
        0.72,
        1.38,
        7.20,
        4.25,
        colors=[RGBColor(175, 183, 191), BLUE],
        ymax=50,
        legend=True,
    )
    add_text(s, "Region-level VQA & zero-shot classification", 1.45, 1.15, 5.8, 0.3, size=13, bold=True, color=MID, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_box(s, 8.35, 1.50, 3.95, 1.20, fill=PALE_BLUE, line=BLUE)
    add_text(s, "空间语义更清晰", 8.82, 1.73, 3.02, 0.40, size=22, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
    add_text(s, "dense features 更易聚类为对象", 8.80, 2.18, 3.05, 0.26, size=11, color=MID, align=PP_ALIGN.CENTER)
    add_box(s, 8.35, 3.10, 3.95, 1.20, fill=WHITE, line=GREEN)
    add_text(s, "任务适用范围扩大", 8.82, 3.33, 3.02, 0.40, size=22, bold=True, color=GREEN, align=PP_ALIGN.CENTER)
    add_text(s, "Detection · Segmentation · Classification", 8.63, 3.78, 3.40, 0.26, size=11, color=MID, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_rich_text(s, [("不是“少看”，而是", INK, False), ("“看得更聚焦”", RED, True)], 8.45, 4.78, 3.72, 0.48, size=17, align=PP_ALIGN.CENTER)
    add_callout(s, "概念级训练改善了视觉编码器：效率提升与细粒度感知增强可以同时发生")
    add_footer(s, 16, source="Paper Table 2 (ViT-L/14 rows)")

    # 17 — Ablation
    s = new_slide(prs)
    add_title(s, "消融实验：性能提升来自逐步叠加的完整设计")
    categories = ["Base", "+ ε(r)", "+ weighted\naverage", "+ semantic\nalignment", "+ mask\nstrategy"]
    values = [56.1, 57.0, 58.4, 58.7, 59.3]
    chart = add_native_chart(
        s,
        categories,
        [("Average", values)],
        0.82,
        1.40,
        7.25,
        4.20,
        chart_type=XL_CHART_TYPE.LINE_MARKERS,
        colors=[BLUE],
        ymin=55,
        ymax=60,
        legend=False,
    )
    add_box(s, 8.48, 1.52, 3.62, 3.75, fill=PALE_BLUE, line=NAVY)
    add_text(s, "最佳 information domain", 8.88, 1.82, 2.82, 0.38, size=17, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
    add_text(s, "S = 1/4", 9.22, 2.42, 2.15, 0.55, size=30, bold=True, color=RED, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_line(s, 9.22, 3.22, 11.37, 3.22, color=LIGHT)
    add_bullet_list(
        s,
        [
            "144 max tokens",
            "平均性能 59.3",
            "成本–性能折中最佳",
        ],
        8.92,
        3.48,
        2.75,
        1.30,
        size=14,
        spacing=5,
    )
    add_callout(s, "ε(r)、加权合并、语义对齐与 mask strategy 均有独立贡献")
    add_footer(s, 17, source="Paper Table 4; four-benchmark average")

    # 18 — Generalization
    s = new_slide(prs)
    add_title(s, "泛化：高分辨率、视频与不同架构都能受益")
    cards = [
        ("High-resolution", "2880 → 160", "70.1 Avg.", BLUE),
        ("Video", "2048 → 136", "52.5 Avg.", ORANGE),
        ("Qwen2-VL", "1326 → 576", "69.6 Avg.", GREEN),
    ]
    for i, (head, tok, score, col) in enumerate(cards):
        x = 0.78 + i * 4.18
        add_box(s, x, 1.42, 3.66, 3.90, fill=PALE_BLUE if i != 1 else WHITE, line=col, line_width=1.5)
        add_text(s, head, x + 0.25, 1.77, 3.16, 0.45, size=20, bold=True, color=col, align=PP_ALIGN.CENTER, font=FONT_EN)
        add_text(s, tok, x + 0.35, 2.58, 2.96, 0.58, size=27, bold=True, color=INK, align=PP_ALIGN.CENTER, font=FONT_EN)
        add_text(s, "vision tokens", x + 0.70, 3.18, 2.25, 0.28, size=11, color=MID, align=PP_ALIGN.CENTER, font=FONT_EN)
        add_line(s, x + 0.52, 3.73, x + 3.14, 3.73, color=LIGHT)
        add_text(s, score, x + 0.70, 4.08, 2.25, 0.52, size=24, bold=True, color=col, align=PP_ALIGN.CENTER, font=FONT_EN)
        add_text(s, "benchmark average", x + 0.70, 4.62, 2.25, 0.25, size=10, color=MID, align=PP_ALIGN.CENTER, font=FONT_EN)
    add_callout(s, "VCM 是可移植的 vision concept modeling 机制，而不是只针对单一 LLaVA 设置的技巧")
    add_footer(s, 18, source="Paper Tables 7–9")

    # 19 — Limitations
    s = new_slide(prs)
    add_title(s, "边界与仍待解决的问题")
    limitations = [
        ("Keyword bias", "自适应关键词不一定等于真实视觉概念", RED),
        ("Coarse length prior", "Min–max length estimation 较粗粒度", ORANGE),
        ("External supervision", "相关性分析使用 GPT-4o 识别与评判", BLUE),
        ("Evaluation scope", "概念可解释性仍主要依赖定性证据", GREEN),
    ]
    for i, (head, body, col) in enumerate(limitations):
        x = 0.80 + (i % 2) * 6.20
        y = 1.40 + (i // 2) * 2.05
        add_box(s, x, y, 5.70, 1.55, fill=PALE_BLUE if i in (1, 2) else WHITE, line=col)
        add_circle(s, x + 0.28, y + 0.37, 0.62, fill=col, line=WHITE)
        add_text(s, str(i + 1), x + 0.42, y + 0.50, 0.34, 0.24, size=15, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        add_text(s, head, x + 1.15, y + 0.26, 4.05, 0.40, size=18, bold=True, color=col, font=FONT_EN)
        add_text(s, body, x + 1.15, y + 0.73, 4.10, 0.48, size=14, color=INK)
    add_callout(s, "结论成立于论文实验范围内；“concept”质量、偏差与可解释性仍需要更直接的测量")
    add_footer(s, 19, source="Paper Section I (Limitations) plus presentation-level critical reading")

    # 20 — Takeaways
    s = new_slide(prs)
    add_title(s, "Take-home message")
    takeaways = [
        ("01", "问题", "token-level 冗余限制 LVLM 扩展", RED),
        ("02", "原则", "由 instruction 决定看多少、看哪里", BLUE),
        ("03", "方法", "语义对齐 + 动态长度 + forward–backward", ORANGE),
        ("04", "证据", "最高 85% FLOPs reduction，性能保持或提升", GREEN),
    ]
    for i, (num, head, body, col) in enumerate(takeaways):
        y = 1.26 + i * 1.22
        add_text(s, num, 0.95, y, 0.75, 0.55, size=24, bold=True, color=col, align=PP_ALIGN.CENTER, font=FONT_EN)
        add_line(s, 1.85, y + 0.28, 2.45, y + 0.28, color=col, width=2.0)
        add_text(s, head, 2.68, y, 1.12, 0.55, size=20, bold=True, color=col, align=PP_ALIGN.CENTER)
        add_text(s, body, 4.05, y, 7.65, 0.55, size=20, bold=i == 3, color=INK)
    add_box(s, 1.25, 6.24, 10.80, 0.58, fill=NAVY, line=NAVY, radius=False)
    add_text(s, "VCM 的核心价值：把“视觉压缩”重新定义为“任务条件化的概念建模”", 1.52, 6.32, 10.26, 0.40, size=17, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_footer(s, 20)

    prs.save(OUT_FILE)
    return OUT_FILE


if __name__ == "__main__":
    output = build_deck()
    print(output)
