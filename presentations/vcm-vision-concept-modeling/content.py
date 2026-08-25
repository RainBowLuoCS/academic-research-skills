"""Deck script and paper data for the VCM talk.

Every number in ``DATA`` carries the table or appendix it was copied from, so a
reviewer can check the deck against arXiv:2504.19627v2 without re-deriving
anything. Nothing here is estimated or interpolated.

Takeaway strings use ``*...*`` to mark the words rendered in the accent red.
"""

PAPER = {
    "title_main": "VCM: Vision Concept Modeling",
    "title_sub": "Adaptive Vision Token Compression via Instruction Fine-Tuning",
    "authors": "Run Luo · Renke Shan · Longze Chen · Ziqiang Liu · Lu Wang · Min Yang · Xiaobo Xia",
    "affil": "SIAT, Chinese Academy of Sciences · UCAS · National University of Singapore · USTC",
    "venue": "arXiv:2504.19627v2 [cs.CL]",
}

# --------------------------------------------------------------------- the data

DATA = {
    # Table 1 — average over 11 image-based VQA benchmarks.
    "vqa11": [
        {"name": "FastV",        "tokens": 192, "avg": 53.1},
        {"name": "PDrop",        "tokens": 192, "avg": 57.8},
        {"name": "SparseVLM",    "tokens": 192, "avg": 57.9},
        {"name": "MQT-LLaVA",    "tokens": 144, "avg": 58.6},
        {"name": "VisionZip",    "tokens": 192, "avg": 59.1},
        {"name": "LLaVA-1.5",    "tokens": 576, "avg": 59.5, "role": "baseline"},
        {"name": "VCM",          "tokens": 144, "avg": 60.8, "role": "ours"},
    ],
    # Table 1 — per-benchmark deltas of VCM (144 tokens) vs LLaVA-1.5 (576).
    "vqa11_delta": [
        ("VisWiz", 4.9), ("SEED", 5.7), ("MMStar", 2.5), ("SciQA", 2.3),
        ("MM-Vet", 1.9), ("MMB", 0.2), ("POPE", 0.2), ("GQA", -0.1),
        ("VQAT", -0.8), ("VQAv2", -1.3),
    ],
    # Table 10 — FLOPs / latency / average over the 8 benchmarks listed there.
    "cost": [
        {"name": "LLaVA-1.5", "tokens": 576, "flops": 4.62, "lat": 57.82, "avg": 61.6,
         "role": "baseline"},
        {"name": "FastV",     "tokens": 128, "flops": 1.70, "lat": 30.70, "avg": 50.7},
        {"name": "PDrop",     "tokens": 128, "flops": 1.62, "lat": 37.77, "avg": 58.5},
        {"name": "SparseVLM", "tokens": 128, "flops": 1.72, "lat": 33.28, "avg": 60.3},
        {"name": "VCM",       "tokens": 128, "flops": 1.71, "lat": 31.42, "avg": 62.0,
         "role": "ours"},
        {"name": "FastV",     "tokens": 64,  "flops": 1.29, "lat": 27.30, "avg": 44.5},
        {"name": "PDrop",     "tokens": 64,  "flops": 1.18, "lat": 43.41, "avg": 44.5},
        {"name": "SparseVLM", "tokens": 64,  "flops": 1.30, "lat": 29.89, "avg": 56.1},
        {"name": "VCM",       "tokens": 64,  "flops": 1.24, "lat": 28.46, "avg": 60.9,
         "role": "ours"},
    ],
    # Tables 2 and 3 — CLIP ViT-L/14 encoder, with and without VCM fine-tuning.
    "dense": [
        {"label": "COCO cls.\nthing Top-1", "values": [28.3, 43.8], "sub": "Table 2"},
        {"label": "COCO cls.\nstuff Top-1", "values": [11.8, 25.4], "sub": "Table 2"},
        {"label": "RefCOCO\nval CIDEr",     "values": [29.5, 31.8], "sub": "Table 2"},
        {"label": "OV-COCO\nAP50",          "values": [35.2, 39.2], "sub": "Table 3"},
        {"label": "ADE-150\nmIoU",          "values": [31.5, 34.8], "sub": "Table 3"},
        {"label": "ADE-847\nmIoU",          "values": [10.8, 11.9], "sub": "Table 3"},
    ],
    # Table 7 — high resolution, LLaVA-NeXT.
    "highres": [
        {"name": "LLaVA-NeXT", "tokens": 2880, "avg": 72.4, "role": "baseline"},
        {"name": "SparseVLM",  "tokens": 160,  "avg": 63.0},
        {"name": "PDrop",      "tokens": 160,  "avg": 65.9},
        {"name": "VisionZip",  "tokens": 160,  "avg": 66.2},
        {"name": "VCM",        "tokens": 160,  "avg": 70.1, "role": "ours"},
    ],
    # Table 8 — video understanding, Video-LLaVA.
    "video": [
        {"name": "Video-LLaVA", "tokens": 2048, "avg": 54.2, "role": "baseline"},
        {"name": "FastV",       "tokens": 198,  "avg": 27.8},
        {"name": "SparseVLM",   "tokens": 198,  "avg": 46.6},
        {"name": "VisionZip",   "tokens": 136,  "avg": 50.3},
        {"name": "VCM",         "tokens": 136,  "avg": 52.5, "role": "ours"},
    ],
    # Table 9 — architecture transfer and scaling.
    "scale": [
        {"name": "Qwen2-VL",       "detail": "1326 tok",         "avg": 70.3, "role": "baseline"},
        {"name": "+ VCM",          "detail": "576 tok",          "avg": 69.6, "role": "ours"},
        {"name": "VCM 7B",         "detail": "144 tok · 500 st", "avg": 60.3, "role": "ours"},
        {"name": "VCM 7B",         "detail": "144 tok · 1k st",  "avg": 62.4, "role": "ours"},
        {"name": "VCM 13B",        "detail": "144 tok · 1k st",  "avg": 64.9, "role": "ours"},
    ],
    # Table 4 — cumulative component ablation (average over 4 VQA benchmarks).
    "ablation_components": [
        {"label": "none",                 "avg": 56.1},
        {"label": "+ \u03b5(r)",          "avg": 57.0},
        {"label": "+ weighted\naverage",  "avg": 58.4},
        {"label": "+ semantic\nalignment", "avg": 58.7},
        {"label": "+ mask\nstrategy",     "avg": 59.3, "role": "ours"},
    ],
    # Table 4 — information-domain scalar S.
    "ablation_domain": [
        {"label": "S = 1/2", "tokens": 288, "avg": 58.9},
        {"label": "S = 1/4", "tokens": 144, "avg": 59.3, "role": "ours"},
        {"label": "S = 1/6", "tokens": 72,  "avg": 56.4},
        {"label": "S = 1/8", "tokens": 36,  "avg": 57.2},
    ],
    # Table 6 — worked dynamic-programming example, M = 8 input tokens, L = 2.
    "dp_example": {
        "p_blank": [0.800, 0.600, 0.200, 0.300, 0.700, 0.900, 0.100, 0.300],
        "p_star":  [0.200, 0.400, 0.800, 0.700, 0.300, 0.100, 0.900, 0.700],
        "gamma": [
            [1.818, 0.196, 0.000, 0.000, 0.000],
            [1.163, 0.819, 0.032, 0.000, 0.000],
            [0.248, 1.677, 0.074, 0.015, 0.000],
            [0.075, 1.447, 0.464, 0.027, 0.002],
            [0.052, 0.458, 1.449, 0.042, 0.014],
            [0.047, 0.051, 1.723, 0.167, 0.027],
            [0.005, 0.088, 0.177, 1.708, 0.036],
            [0.002, 0.046, 0.133, 0.943, 0.890],
        ],
        "row_total": 2.014,
    },
}

# ------------------------------------------------------------------- the script

CITE_VCM = "Run Luo, Renke Shan, Longze Chen, Ziqiang Liu, Lu Wang, Min Yang, Xiaobo Xia. VCM: Vision Concept Modeling with Adaptive Vision Token Compression via Instruction Fine-Tuning. arXiv:2504.19627v2, 2025."

SLIDES = [
    dict(
        key="title", fig="fig_title_motif", kind="title",
    ),
    dict(
        key="motivation", fig="fig_motivation",
        title="LVLMs are the interface to the real world",
        takeaway="Powerful, general, deployed — and still reading every image *token by token*.",
        cite="Liu et al. Visual Instruction Tuning. NeurIPS 2024. · Bai et al. Qwen-VL. arXiv:2308.12966, 2023.",
    ),
    dict(
        key="gap", fig="fig_token_vs_concept",
        title="Humans answer with concepts, LVLMs pay for tokens",
        takeaway="The question needs *a few concepts*; the model still pays for *all 576 tokens*.",
        cite="Figure 1 of the paper.",
    ),
    dict(
        key="cost", fig="fig_cost",
        title="Why that redundancy is expensive",
        subline="Vision tokens dominate the sequence, and attention is quadratic in its length.",
        takeaway="Higher resolution and longer video make the *dominant* term grow *fastest*.",
        cite="Appendix D of the paper. FLOPs = T\u00b7(4nd\u00b2 + 2n\u00b2d + 2ndm).",
    ),
    dict(
        key="prior", fig="fig_prior_art",
        title="The existing recipe: prune, or merge",
        takeaway="Both make the sequence *shorter*; neither makes it *conceptual*.",
        cite="FastV (ECCV 2025) · SparseVLM · PyramidDrop · VisionZip · MQT-LLaVA · ToMe.",
    ),
    dict(
        key="missing", fig="fig_missing",
        title="What is still missing",
        takeaway="Shorter is not the same as conceptual — so *none of them is a vision concept model*.",
        cite="Section 1 and Section 5.1 of the paper.",
    ),
    dict(
        key="define", fig="fig_definition",
        title="Definition: the vision concept model",
        takeaway="A model that decides *how many* concepts, *which* ones, and *where* — from the instruction.",
        cite="Contribution (1) of the paper.",
    ),
    dict(
        key="challenges", fig="fig_challenges",
        title="Two challenges stand in the way",
        takeaway="We need supervision *without labels*, and optimization *without a fixed length*.",
        cite="Section 2, Goal and challenges.",
    ),
    dict(
        key="observation", fig="fig_observation",
        title="The text prior already knows the answer",
        subline="Probe: 5K LLaVA instances · GPT-4o extracts image-related keywords · VisionZip at 24 lengths · GPT-4o judges the minimum sufficient length.",
        takeaway="The instruction\u2013response *keyword gap* is a supervision signal that costs nothing.",
        cite="Section 3.1 and Figure 2 of the paper.",
    ),
    dict(
        key="overview", fig="fig_overview",
        title="VCM at a glance",
        takeaway="Select keywords, estimate a length, then *align by dynamic programming*.",
        cite="Figure 3(a) of the paper.",
    ),
    dict(
        key="keyword", fig="fig_keyword",
        title="Step 1 — keywords from semantic alignment",
        takeaway="Keywords fall out of *vision\u2013language alignment*, not out of human annotation.",
        cite="Section 3.2 and Figure 3(b) of the paper.",
    ),
    dict(
        key="masking", fig="fig_masking",
        title="Step 2 — implicit contrastive sampling",
        takeaway="Masking keywords *lengthens* what is needed — a free contrast, and a *knob* at inference.",
        cite="Section 3.3 and Figure 4 (top) of the paper.",
    ),
    dict(
        key="length", fig="fig_length",
        title="Step 3 — turn the prior into a target length",
        takeaway="The text prior becomes an explicit *target length* — still no concept labels.",
        cite="Section 3.3 of the paper.",
    ),
    dict(
        key="dp", fig="fig_dp",
        title="Step 4 — forward\u2013backward over all alignments",
        subline="Every monotone path through the lattice is one way to cut the sequence into L concepts; the forward and backward recursions score all of them at once.",
        takeaway="Where to cut is unknown, so we sum over *every* alignment: 2\u1d39 \u2192 *M\u00b2*.",
        cite="Section 3.3 of the paper. Dynamic programming: Bellman, Science 1966.",
    ),
    dict(
        key="grad", fig="fig_gradient",
        title="The gradient is a posterior residual",
        subline="Worked example from Table 6: M = 8 input tokens, target length L = 2. Row sums of \u03b3 stay constant across t.",
        takeaway="One clean rule — *prediction minus posterior*, exactly CTC's gradient shape.",
        cite="Section 3.4, Appendix C, and Table 6 of the paper.",
    ),
    dict(
        key="merge", fig="fig_merge",
        title="Step 5 — merge the kept runs into concepts",
        takeaway="Adjacent kept tokens merge by *score-weighted average* — and the op is *100\u00d7 faster* than a double loop.",
        cite="Section 3.4 and Algorithm 2 of the paper.",
    ),
    dict(
        key="vqa", fig="fig_vqa",
        title="Evidence — better than the model it compresses",
        subline="Average over 11 image-based VQA benchmarks (Table 1).",
        takeaway="*144* tokens instead of 576, and a *higher* average than LLaVA-1.5 itself.",
        cite="Table 1 of the paper. #Vision Tokens = tokens fed to the LLM backbone.",
    ),
    dict(
        key="efficiency", fig="fig_efficiency",
        title="Evidence — the cost actually drops",
        subline="Average over the 8 benchmarks reported in Table 10; FLOPs and latency measured in the same setting.",
        takeaway="*85%* fewer FLOPs in theory, *1.8\u00d7* lower latency in practice, *no* average loss.",
        cite="Table 10 and Appendix D of the paper. Analytic ratio R \u2248 3/25 at S = 1/4.",
    ),
    dict(
        key="dense", fig="fig_dense",
        title="Evidence — the vision encoder itself improves",
        subline="CLIP ViT-L/14 with and without VCM fine-tuning, dropped into F-VLM (detection) and Cat-Seg (segmentation).",
        takeaway="Not only compression — concept modeling *improves dense perception*.",
        cite="Tables 2 and 3 of the paper.",
    ),
    dict(
        key="general", fig="fig_general",
        title="Evidence — the recipe transfers",
        subline="High resolution (Table 7) · video (Table 8) · other architectures and larger LLMs (Table 9).",
        takeaway="Resolution, modality, architecture, scale — *the same recipe holds*.",
        cite="Tables 7, 8, and 9 of the paper.",
    ),
    dict(
        key="ablation", fig="fig_ablation",
        title="Ablation — what each piece buys",
        subline="Average over 4 image-based VQA benchmarks, batch size 128, 500 training steps (Table 4).",
        takeaway="Every component contributes, and *S = 1/4* is the accuracy\u2013cost sweet spot.",
        cite="Table 4 of the paper.",
    ),
    dict(
        key="conclusion", fig="fig_conclusion",
        title="Conclusion",
        takeaway="Model the concepts the instruction *needs* — not every token the image *has*.",
        cite=CITE_VCM,
    ),
]


# Eight-slide version for a shorter talk.  It is a separate narrative rather
# than a slice of ``SLIDES``: each page combines several adjacent claims into
# one richer visual argument.
CONDENSED_SLIDES = [
    dict(
        key="c_title", fig="fig_title_motif", kind="title",
    ),
    dict(
        key="c_problem", fig="fig_c_problem",
        title="The bottleneck — LVLMs still read every image token",
        takeaway="The answer needs *a concept*; the model pays for *the whole image*.",
        cite="Figure 1 and Appendix D of the paper.",
    ),
    dict(
        key="c_gap", fig="fig_c_gap",
        title="Compression is not yet concept modeling",
        takeaway="A vision concept model must decide *how many*, *which*, and *where* — from the instruction.",
        cite="Sections 1, 2, and 5.1 of the paper.",
    ),
    dict(
        key="c_overview", fig="fig_overview",
        title="VCM — one model, two training stages",
        takeaway="Use the text prior to set a budget, then *align tokens into concepts*.",
        cite="Section 3 and Figure 3(a) of the paper.",
    ),
    dict(
        key="c_supervision", fig="fig_c_supervision",
        title="Self-supervision — the instruction tells us what vision is needed",
        takeaway="Keywords provide the signal; masking creates the contrast; *no concept labels are required*.",
        cite="Sections 3.1–3.3 and Figures 2–4 of the paper.",
    ),
    dict(
        key="c_optimization", fig="fig_c_optimization",
        title="Optimization — learn variable-length concepts without choosing a cut",
        takeaway="Forward–backward sums every alignment, then adjacent kept tokens *merge into concepts*.",
        cite="Sections 3.3–3.4, Appendix C, Table 6, and Algorithm 2.",
    ),
    dict(
        key="c_evidence", fig="fig_c_evidence",
        title="Core evidence — less computation, no performance trade-off",
        takeaway="At 144 tokens VCM beats the 576-token baseline; at S = 1/4 it uses *85% fewer FLOPs*.",
        cite="Tables 1 and 10; Appendix D.",
    ),
    dict(
        key="c_takeaway", fig="fig_c_takeaway",
        title="What VCM changes — efficiency, representation, and scope",
        takeaway="Model the concepts the instruction *needs* — not every token the image *has*.",
        cite=CITE_VCM,
    ),
]
