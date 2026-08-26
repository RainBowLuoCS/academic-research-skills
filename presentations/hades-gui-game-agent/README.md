# Hades GUI Agent 论文汇报

基于用户提供的 Hades 稿件制作的 7 页、16:9 学术汇报，版式与
`mm_alignment_v1.pdf` 保持一致：白底科研图、单页单结论、底部蓝框 takeaway。

## 交付物

- `out/Hades_GUI_Agent_talk.pptx`
- `out/Hades_GUI_Agent_talk.pdf`
- `out/slides/*.svg`：完整页面 SVG
- `out/figures/*.svg`：独立科研图 SVG

## 材料边界

提供的 PDF 在摘要中声称达到 near-human expert level 和多项 SOTA，但正文的
Evaluation 部分没有具体 benchmark 表格。因此汇报不生成或推断实验数值，只使用正文
明确给出的系统指标，例如 Streaming-vLLM 超过 `20×` 的解码加速和超过 `30 Hz`
的动作预测频率。

## 重新生成

```bash
cd presentations/hades-gui-game-agent
python3 build.py
python3 check_layout.py
```
