# VCM 论文汇报（可编辑版）

## 文件

- `VCM_7页精简汇报_可编辑版.pptx`：推荐使用的 7 页版本。
- `generate_vcm_deck.py`：当前版本的生成脚本，包含统一的排版栅格、
  配色与图表样式定义。
- `generate_vcm_ppt_refined.py`、`generate_vcm_ppt_7slides.py`：早期版本脚本。
- `VCM_论文汇报_可编辑版.pptx`：20 页、16:9 中文科研汇报。
- `generate_vcm_ppt.py`：可重复生成 PPT 的源脚本。

## 设计系统

`generate_vcm_deck.py` 顶部集中定义了整套视觉规则，便于统一调整：

- 栅格：左右边距 0.85"，内容宽度 11.63"，标题、正文、页脚使用固定纵向节奏。
- 配色：深蓝 `#123A5F` 为主，蓝 `#1F6FB2` 为强调，珊瑚红 `#C8443C` 仅用于重点，
  其余为中性灰与浅蓝底色。
- 字体：拉丁文 Segoe UI，中文 Microsoft YaHei（同时写入 `latin` 与 `ea`）。
- 图表：去除网格线与数值轴，直接标注数据标签，仅高亮关键柱。

## 内容说明

七页对应论文主线，每页只表达一个判断：

1. 标题与一句话贡献
2. 问题：整幅图都进入 LLM，576 vs 16 tokens
3. 洞察：文本先验透露所需视觉长度
4. 方法：语义对齐 → 关键词选择 → 概念建模
5. 算法：Forward–Backward 与 segment merging
6. 结果：FLOPs 与 VQA 平均分
7. 结论：贡献、证据、局限与 take-home

版式参考 `mm_alignment_v1_23c2.pdf`：白底、顶部大标题、中心示意图、
底部结论条、少文字、逐页推进。

## 可编辑性

- 示意图、栅格、箭头、公式、标题与结论条均为 PowerPoint 原生对象。
- 两个数据图为原生图表，双击即可修改内嵌数据。
- 仅两张论文图作为图片使用：指令驱动稀疏化与 K-Means 聚类，
  它们是照片类证据，无法用矢量形状还原。
- 若系统缺少 Segoe UI 或 Microsoft YaHei，PowerPoint 会自动替换，
  可通过“替换字体”统一调整。

## 重新生成

```bash
python3 generate_vcm_deck.py
```

依赖：`python-pptx>=1.0.2`、`pymupdf`（用于裁剪论文图）。
