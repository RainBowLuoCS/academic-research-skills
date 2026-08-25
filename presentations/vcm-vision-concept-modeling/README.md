# VCM 论文汇报

基于 `arXiv:2504.19627v2` 制作的 22 页、16:9 学术汇报，视觉风格参考用户提供的
`Multimodal Alignment: From Learning Principles to Foundation Models`。

## 交付物

- `out/VCM_talk.pptx`：PowerPoint 演示文稿
- `out/VCM_talk.pdf`：快速预览版本
- `out/slides/*.svg`：每一页的完整 SVG
- `out/figures/*.svg`：每一页中心科研图的独立 SVG
- `out-condensed/VCM_talk_condensed.pptx`：视觉元素更丰富的 8 页精简版
- `out-condensed/VCM_talk_condensed.pdf`：8 页精简版预览
- `out-condensed/{slides,figures}/*.svg`：精简版完整页面及独立科研图
- `content.py`：叙事结构、论文数据和引用来源
- `figures.py`：科研图定义
- `build.py`：SVG、PDF 和 PPTX 生成器

PPT 中的标题、结论框和引用是 PowerPoint 原生对象，可直接编辑。中心科研图以 SVG
嵌入；在桌面版 PowerPoint 中选择图形并使用“转换为形状”，即可进一步编辑其中的
文本、线条、颜色和几何元素。原始 SVG 也可以在 Figma、Illustrator 或 Inkscape 中编辑。

## 叙事结构

1. 应用背景与 token-level 冗余
2. 现有压缩方法的缺口
3. Vision Concept Model 的定义与挑战
4. 无标注监督信号与 VCM 五步方法
5. VQA、效率、密集感知、泛化和消融证据
6. 核心结论与局限

## 重新生成

```bash
cd presentations/vcm-vision-concept-modeling
python3 build.py
python3 check_layout.py

# 生成并检查 8 页精简版
python3 build.py --deck condensed
python3 check_layout.py --deck condensed
```

`check_layout.py` 会检查所有科研图是否越出其版面区域。
