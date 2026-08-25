# VCM 论文汇报（可编辑版）

## 文件

- `VCM_7页精简汇报_可编辑版.pptx`：推荐使用的 7 页精简版。
- `generate_vcm_ppt_7slides.py`：7 页精简版生成脚本。
- `VCM_论文汇报_可编辑版.pptx`：20 页、16:9 中文科研汇报。
- `generate_vcm_ppt.py`：可重复生成 PPT 的源脚本。

## 设计说明

叙事顺序为：

1. LVLM 的 token-level 计算瓶颈
2. 从 token processing 转向 instruction-conditioned vision concepts
3. 论文定义与已有 token reduction 的差异
4. 文本先验与最小视觉长度的相关性
5. Semantic alignment、keyword selection 与动态长度估计
6. Forward–backward optimization 与 segment merging
7. 效率、VQA、dense perception、消融与泛化证据
8. 局限性与 take-home message

版式参考 `mm_alignment_v1_23c2.pdf`：白底、顶部大标题、中心示意图、
底部结论框、少文字和逐页推进。

## 可编辑性

- 流程图、token 网格、箭头、公式、标题和结论框均为 PowerPoint 原生对象。
- 数据图为 PowerPoint 原生图表，双击图表后可编辑内嵌数据。
- 未把论文整页或统计图截图贴入幻灯片。
- 字体指定为 Microsoft YaHei / Arial；若系统缺少对应字体，PowerPoint
  会自动替换，可在“替换字体”中统一调整。

## 重新生成

```bash
python3 generate_vcm_ppt.py
```

依赖：`python-pptx>=1.0.2`。
