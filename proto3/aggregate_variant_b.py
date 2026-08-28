#!/usr/bin/env python3
"""Compare Variant A (joint extraction) against Variant B (decomposed
extraction) per role, one run each.

Reads proto3/results/run1/*.json (Variant A) and proto3/results_b/*.json
(Variant B) -- both one run per paper, so the comparison is apples-to-apples
(no repeated-run variance study for Variant B, per proto3/memo.md
"Architecture reconsideration"). Prints a side-by-side per-role table and
writes proto3/results_b/aggregate.json.

Run:
    python proto3/aggregate_variant_b.py
"""

import json
from pathlib import Path

from uol_fp.scoring import ROLES, precision_recall_f1, score_profile

# Duplicated from 3pipeline.ipynb cell 20 -- GOLD_LABELS has no separate
# source file (see proto3/memo.md). Keep in sync with that cell by hand.
GOLD_LABELS: dict[str, dict[str, str | None]] = {
    "transformer": {
        "TechnicalMethod": "Transformer",
        "Task": "machine translation",
        "Dataset": "WMT",
        "EvaluationMetric": "BLEU",
    },
    "bert": {
        "TechnicalMethod": "BERT",
        "Task": "GLUE",
        "Dataset": "BooksCorpus",
        "EvaluationMetric": "F1",
    },
    "alexnet": {
        "TechnicalMethod": "convolutional",
        "Task": "object recognition",
        "Dataset": "ImageNet",
        "EvaluationMetric": "top-5",
    },
    "resnet": {
        "TechnicalMethod": "residual",
        "Task": "image recognition",
        "Dataset": "ImageNet",
        "EvaluationMetric": "top-1",
    },
    "mapreduce": {
        "TechnicalMethod": "MapReduce",
        "Task": "distributed",
        "Dataset": "TeraSort",
        "EvaluationMetric": "seconds",
    },
    "pagerank": {
        "TechnicalMethod": "PageRank",
        "Task": "web search",
        "Dataset": "million pages",
        "EvaluationMetric": "quality",
    },
}

REPO_ROOT = Path(__file__).resolve().parent
VARIANT_A_DIR = REPO_ROOT / "results" / "run1"
VARIANT_B_DIR = REPO_ROOT / "results_b"

Totals = dict[str, tuple[int, int, int, int]]


def load_variant(variant_dir: Path) -> dict[str, dict[str, str | None]]:
    results: dict[str, dict[str, str | None]] = {}
    for slug in GOLD_LABELS:
        data = json.loads((variant_dir / f"{slug}.json").read_text())
        results[slug] = {role: data[role]["answer"] for role in ROLES}
    return results


def aggregate_scores(
    results: dict[str, dict[str, str | None]],
    gold: dict[str, dict[str, str | None]],
) -> Totals:
    totals: Totals = {role: (0, 0, 0, 0) for role in ROLES}
    for slug, sys_answers in results.items():
        per_role = score_profile(gold[slug], sys_answers)
        for role, (tp, fp, fn, tn) in per_role.items():
            t_tp, t_fp, t_fn, t_tn = totals[role]
            totals[role] = (t_tp + tp, t_fp + fp, t_fn + fn, t_tn + tn)
    return totals


def print_comparison_table(a_totals: Totals, b_totals: Totals) -> None:
    print("Variant A (joint, results/run1) vs Variant B (decomposed, results_b):")
    print(
        f"{'Role':<18} {'A: P':>5} {'A: R':>5} {'A: F1':>6}"
        f"  {'B: P':>5} {'B: R':>5} {'B: F1':>6}  {'ΔF1':>6}"
    )
    for role in ROLES:
        a_p, a_r, a_f1 = precision_recall_f1(*a_totals[role][:3])
        b_p, b_r, b_f1 = precision_recall_f1(*b_totals[role][:3])
        print(
            f"{role:<18} {a_p:>5.2f} {a_r:>5.2f} {a_f1:>6.2f}"
            f"  {b_p:>5.2f} {b_r:>5.2f} {b_f1:>6.2f}  {b_f1 - a_f1:>+6.2f}"
        )
    print()


def variant_summary(totals: Totals) -> dict[str, dict[str, float | int]]:
    return {
        role: {
            "tp": totals[role][0],
            "fp": totals[role][1],
            "fn": totals[role][2],
            "tn": totals[role][3],
            **dict(
                zip(
                    ("precision", "recall", "f1"),
                    precision_recall_f1(*totals[role][:3]),
                )
            ),
        }
        for role in ROLES
    }


def main() -> None:
    variant_a = load_variant(VARIANT_A_DIR)
    variant_b = load_variant(VARIANT_B_DIR)

    a_totals = aggregate_scores(variant_a, GOLD_LABELS)
    b_totals = aggregate_scores(variant_b, GOLD_LABELS)

    print_comparison_table(a_totals, b_totals)

    summary = {
        "variant_a_source": str(VARIANT_A_DIR.relative_to(REPO_ROOT)),
        "variant_b_source": str(VARIANT_B_DIR.relative_to(REPO_ROOT)),
        "variant_a": variant_summary(a_totals),
        "variant_b": variant_summary(b_totals),
    }
    out_path = VARIANT_B_DIR / "aggregate.json"
    out_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
