#!/usr/bin/env python3
"""Aggregate proto3/results/run{1..5}/*.json into a variance study and
pooled Wilson 95% confidence intervals on Precision/Recall.

Reads the raw per-paper pipeline output JSON files directly (not the
run.txt console captures, which are just a human-readable copy of one
run's printout). Prints a report and writes proto3/results/aggregate.json.

Run:
    python proto3/aggregate_runs.py
"""

import json
import math
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
RESULTS_DIR = REPO_ROOT / "results"
RUN_DIRS = [RESULTS_DIR / f"run{n}" for n in range(1, 6)]

Totals = dict[str, tuple[int, int, int, int]]


def load_run(run_dir: Path) -> dict[str, dict[str, str | None]]:
    results: dict[str, dict[str, str | None]] = {}
    for slug in GOLD_LABELS:
        data = json.loads((run_dir / f"{slug}.json").read_text())
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


def wilson_interval(
    successes: int, trials: int, z: float = 1.96
) -> tuple[float, float]:
    """Wilson score interval for a binomial proportion successes/trials."""
    if trials == 0:
        return (0.0, 0.0)
    p_hat = successes / trials
    denom = 1 + z * z / trials
    center = (p_hat + z * z / (2 * trials)) / denom
    margin = (
        z
        * math.sqrt(p_hat * (1 - p_hat) / trials + z * z / (4 * trials * trials))
        / denom
    )
    return (max(0.0, center - margin), min(1.0, center + margin))


def print_score_table(totals: Totals, title: str) -> None:
    print(title)
    print(
        f"{'Role':<18} {'TP':>3} {'FP':>3} {'FN':>3} {'TN':>3}"
        f"  {'P':>5} {'R':>5} {'F1':>5}"
    )
    overall = (0, 0, 0, 0)
    for role in ROLES:
        tp, fp, fn, tn = totals[role]
        p, r, f1 = precision_recall_f1(tp, fp, fn)
        print(
            f"{role:<18} {tp:>3} {fp:>3} {fn:>3} {tn:>3}"
            f"  {p:>5.2f} {r:>5.2f} {f1:>5.2f}"
        )
        overall = tuple(a + b for a, b in zip(overall, (tp, fp, fn, tn)))
    p, r, f1 = precision_recall_f1(overall[0], overall[1], overall[2])
    print(
        f"{'Overall':<18} {overall[0]:>3} {overall[1]:>3} {overall[2]:>3}"
        f" {overall[3]:>3}"
        f"  {p:>5.2f} {r:>5.2f} {f1:>5.2f}"
    )
    print()


def main() -> None:
    per_run_totals: list[Totals] = []
    for run_dir in RUN_DIRS:
        results = load_run(run_dir)
        totals = aggregate_scores(results, GOLD_LABELS)
        per_run_totals.append(totals)
        print_score_table(totals, f"Pipeline vs gold ({run_dir.name}):")

    # Variance summary: per-role F1 (and P, R) across the 5 runs.
    variance: dict[str, dict[str, float]] = {}
    print("Variance across 5 runs:")
    print(f"{'Role':<18} {'F1 mean':>8} {'F1 min':>8} {'F1 max':>8} {'F1 range':>9}")
    for role in ROLES:
        f1s: list[float] = []
        ps: list[float] = []
        rs: list[float] = []
        for totals in per_run_totals:
            tp, fp, fn, _tn = totals[role]
            p, r, f1 = precision_recall_f1(tp, fp, fn)
            f1s.append(f1)
            ps.append(p)
            rs.append(r)
        f1_mean = sum(f1s) / len(f1s)
        f1_min, f1_max = min(f1s), max(f1s)
        variance[role] = {
            "f1_mean": f1_mean,
            "f1_min": f1_min,
            "f1_max": f1_max,
            "f1_range": f1_max - f1_min,
            "p_mean": sum(ps) / len(ps),
            "r_mean": sum(rs) / len(rs),
        }
        print(
            f"{role:<18} {f1_mean:>8.2f} {f1_min:>8.2f} {f1_max:>8.2f}"
            f" {f1_max - f1_min:>9.2f}"
        )
    print()

    # Pooled Wilson 95% CI per role: sum tp/fp/fn across the 5 runs.
    pooled_ci: dict[str, dict[str, object]] = {}
    print("Pooled Wilson 95% CI across 5 runs (n=30 trials/role):")
    print(
        f"{'Role':<18} {'TP':>4} {'FP':>4} {'FN':>4}"
        f"  {'P':>5} {'P CI':>15}  {'R':>5} {'R CI':>15}"
    )
    for role in ROLES:
        tp = sum(totals[role][0] for totals in per_run_totals)
        fp = sum(totals[role][1] for totals in per_run_totals)
        fn = sum(totals[role][2] for totals in per_run_totals)
        p, r, _f1 = precision_recall_f1(tp, fp, fn)
        p_lo, p_hi = wilson_interval(tp, tp + fp)
        r_lo, r_hi = wilson_interval(tp, tp + fn)
        pooled_ci[role] = {
            "tp": tp,
            "fp": fp,
            "fn": fn,
            "precision": p,
            "precision_ci": [p_lo, p_hi],
            "recall": r,
            "recall_ci": [r_lo, r_hi],
        }
        p_ci_str = f"[{p_lo:.2f}, {p_hi:.2f}]"
        r_ci_str = f"[{r_lo:.2f}, {r_hi:.2f}]"
        print(
            f"{role:<18} {tp:>4} {fp:>4} {fn:>4}"
            f"  {p:>5.2f} {p_ci_str:>15}  {r:>5.2f} {r_ci_str:>15}"
        )
    print()
    print(
        "Caveat: the 5 runs repeat the same 6 papers, so the 30 trials/role "
        "pooled above are not fully independent -- these intervals are "
        "narrower than a true 30-independent-paper sample would give."
    )

    summary = {
        "runs": [run_dir.name for run_dir in RUN_DIRS],
        "per_run": {
            run_dir.name: {
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
            for run_dir, totals in zip(RUN_DIRS, per_run_totals)
        },
        "variance": variance,
        "pooled_ci": pooled_ci,
    }
    out_path = RESULTS_DIR / "aggregate.json"
    out_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
