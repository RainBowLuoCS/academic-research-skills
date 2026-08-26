"""Seven-slide narrative and source-checked data for NExT-OMNI."""

PAPER = {
    "title_main": "NExT-OMNI",
    "title_sub": "Any-to-Any Omnimodal Foundation Models with Discrete Flow Matching",
    "authors": "Run Luo · Xiaobo Xia · Lu Wang · Longze Chen · Renke Shan · Jing Luo · Min Yang · Tat-Seng Chua",
    "affil": "SIAT, Chinese Academy of Sciences · UCAS · NExT++ Research Center · NUS",
    "venue": "arXiv:2510.13721v2 [cs.CL]",
}

DATA = {
    # Main-paper Table 1, average over OmniBench, WorldSense, and AV-Odyssey.
    "understanding": [
        {"name": "UnifiedIO2-XL", "avg": 28.4},
        {"name": "VITA-1.5", "avg": 33.9},
        {"name": "OpenOmni", "avg": 36.5, "role": "baseline"},
        {"name": "NExT-OMNI", "avg": 39.7, "role": "ours"},
    ],
    # Main-paper Table 2, OpenING multi-turn vision interaction average.
    "vision_interaction": [
        {"name": "VILA-U", "avg": 48.4},
        {"name": "SEED-X", "avg": 50.2},
        {"name": "Anole", "avg": 50.4, "role": "baseline"},
        {"name": "NExT-OMNI", "avg": 55.0, "role": "ours"},
    ],
    # Main-paper Table 4, multimodal retrieval average.
    "retrieval": [
        {"name": "Bagel", "avg": 28.5},
        {"name": "Show-o", "avg": 30.6},
        {"name": "MMaDA", "avg": 31.8, "role": "baseline"},
        {"name": "NExT-OMNI", "avg": 32.9, "role": "ours"},
    ],
    # Main-paper Table 5, cumulative architecture/training ablation.
    "ablation": [
        {"name": "AR · decoupled", "avg": 41.4},
        {"name": "DFM · decoupled", "avg": 42.6},
        {"name": "DFM · unified", "avg": 43.0},
        {"name": "+ DGS", "avg": 43.9},
        {"name": "+ reconstruction", "avg": 45.6, "role": "ours"},
    ],
}

CITATION = (
    "Run Luo, Xiaobo Xia, Lu Wang, Longze Chen, Renke Shan, Jing Luo, "
    "Min Yang, and Tat-Seng Chua. NExT-OMNI: Towards Any-to-Any "
    "Omnimodal Foundation Models with Discrete Flow Matching. "
    "arXiv:2510.13721v2, 2025."
)

SLIDES = [
    dict(key="title", fig="fig_title_motif", kind="title"),
    dict(
        key="problem", fig="fig_problem",
        title="The conflict — one model, three jobs, four modalities",
        takeaway="Autoregression is sequential; hybrid systems unify tasks by *splitting the model*.",
        cite="Introduction and Figure 1 of the paper.",
    ),
    dict(
        key="flow", fig="fig_flow",
        title="The alternative — discrete flow learns to correct in parallel",
        takeaway="Corrupt globally, predict globally, refine iteratively — with *bidirectional context*.",
        cite="Sections 2.3–2.4 and Appendix A of the paper.",
    ),
    dict(
        key="architecture", fig="fig_architecture",
        title="NExT-OMNI — a single deeply fused representation",
        takeaway="One backbone serves understanding, generation, and retrieval — *no task router required*.",
        cite="Sections 2.1–2.3 and Figure 2 of the paper.",
    ),
    dict(
        key="efficiency", fig="fig_efficiency",
        title="Training and inference — make iterative decoding practical",
        takeaway="Interleave modalities, grow responses by blocks, and cache features that barely change.",
        cite="Section 2.4 and Figure 3 of the paper.",
    ),
    dict(
        key="results", fig="fig_results",
        title="Evidence — the unified flow transfers across task families",
        takeaway="NExT-OMNI leads on understanding, multi-turn vision, and cross-modal retrieval.",
        cite="Main-paper Tables 1, 2, and 4.",
    ),
    dict(
        key="takeaway", fig="fig_takeaway",
        title="What the ablation says — unification needs the full recipe",
        takeaway="DFM opens the door; dynamic length and reconstruction make the unified model *work*.",
        cite=CITATION,
    ),
]

# Compatibility with the shared deck renderer.
CONDENSED_SLIDES = SLIDES
