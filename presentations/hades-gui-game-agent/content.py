"""Seven-slide narrative and source-bound facts for the Hades paper."""

PAPER = {
    "title_main": "Hades",
    "title_sub": "A Generalist Vision-Language-Action Model for Long-Horizon Real-Time GUI Game Agents",
    "authors": "miHoYo Lumi · full author list in the paper's Contributions section",
    "affil": "Industrial-scale generalist agent research",
    "venue": "Manuscript dated 26 August 2026",
}

FACTS = {
    "decision_ms": 200,
    "action_chunks": 6,
    "control_hz": 30,
    "repeat_share": 85,
    "loss_decay": 0.9,
    "inference_speedup": 20,
    "parallel_workers": 100,
}

CITATION = (
    "miHoYo Lumi. Hades: A Generalist Vision-Language Action Foundation "
    "Model for Long-Horizon Real-Time GUI Game Agent. Manuscript, 2026."
)

SLIDES = [
    dict(key="title", fig="fig_title_motif", kind="title"),
    dict(
        key="problem", fig="fig_problem",
        title="Commercial games expose the full agent problem",
        takeaway="Pixels in, keyboard and mouse out — with *hours of state* in between.",
        cite="Introduction of the paper.",
    ),
    dict(
        key="pretraining", fig="fig_pretraining",
        title="Stage 1 — learn a universal device-level action language",
        takeaway="Compress 30 Hz control into tokens, then debias what the model learns from repetition.",
        cite="Sections 2.1–2.5 and Figure 1.",
    ),
    dict(
        key="thinking", fig="fig_thinking",
        title="Stage 2 — think sparsely and remember across context windows",
        takeaway="Routine control stays fast; decisions and memory appear only at *critical moments*.",
        cite="Sections 3.1–3.6 and Figure 1.",
    ),
    dict(
        key="rl", fig="fig_rl",
        title="Stage 3 — TA-GRPO turns an hour-long rollout into learnable segments",
        takeaway="Compact memory across segments and assign credit near the state changes that matter.",
        cite="Sections 4.1–4.5 and Figure 2.",
    ),
    dict(
        key="inference", fig="fig_inference",
        title="Deployment — stream actions while the model is still decoding",
        takeaway="Streaming-vLLM overlaps generation with execution and reuses the moving context.",
        cite="Sections 5.1–5.7 and Figure 3.",
    ),
    dict(
        key="flywheel", fig="fig_flywheel",
        title="System view — data, policy, verifier, and infrastructure form one loop",
        takeaway="The contribution is an industrial agent stack, not only a policy model.",
        cite=CITATION,
    ),
]

CONDENSED_SLIDES = SLIDES
