# NExT-OMNI 论文汇报

基于 `arXiv:2510.13721v2` 制作的 7 页、16:9 学术汇报。核心逻辑为：

1. AR 与任务解耦架构的矛盾
2. Any-to-any omnimodal 统一目标
3. Discrete Flow Matching 的并行修正机制
4. 重建增强的统一表示与单一骨干网络
5. 动态长度生成和 adaptive cache
6. 理解、多轮视觉交互与跨模态检索结果
7. 消融证据、贡献与后续方向

## 交付物

- `out/NExT_OMNI_talk.pptx`
- `out/NExT_OMNI_talk.pdf`
- `out/slides/*.svg`：完整页面 SVG
- `out/figures/*.svg`：独立科研图 SVG

PPT 的标题、结论框和引用均为原生对象。中心科研图以 SVG 嵌入，可在桌面版
PowerPoint 中使用“转换为形状”进一步编辑。

## 重新生成

```bash
cd presentations/next-omni-discrete-flow
python3 build.py
python3 check_layout.py
```
