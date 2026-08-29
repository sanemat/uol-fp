#!/usr/bin/env python3
"""Compare Task's F1 under three variants: A (joint), B (decomposed,
single-valued), and the multi-valued Task pilot -- one run each.

Reads proto3/results/run1/*.json (A), proto3/results_b/*.json (B), and
proto3/results_multi_task/*.json (multi-valued pilot). See proto3/memo.md
"Multi-valued roles" Update (2026-08-29) for the pilot's design and
hypothesis.

Run:
    python proto3/aggregate_multi_task.py
"""

import json
from pathlib import Path

from uol_fp.scoring import matches, precision_recall_f1, score_role, score_role_multi

# Duplicated from 3pipeline.ipynb cell 20 -- GOLD_LABELS has no separate
# source file (see proto3/memo.md). Keep in sync with that cell by hand.
GOLD_LABELS: dict[str, str | None] = {
    "transformer": "machine translation",
    "bert": "GLUE",
    "alexnet": "object recognition",
    "resnet": "image recognition",
    "mapreduce": "distributed",
    "pagerank": "web search",
}

REPO_ROOT = Path(__file__).resolve().parent
VARIANT_A_DIR = REPO_ROOT / "results" / "run1"
VARIANT_B_DIR = REPO_ROOT / "results_b"
MULTI_TASK_DIR = REPO_ROOT / "results_multi_task"

Totals = tuple[int, int, int, int]


def main() -> None:
    a_totals: Totals = (0, 0, 0, 0)
    b_totals: Totals = (0, 0, 0, 0)
    multi_totals: Totals = (0, 0, 0, 0)
    primary_totals: Totals = (0, 0, 0, 0)

    print(
        f"{'Paper':<12} {'Gold':<22} {'A':<22} {'B':<22} {'Multi-valued answers'}"
    )
    for slug, gold in GOLD_LABELS.items():
        a_answer = json.loads((VARIANT_A_DIR / f"{slug}.json").read_text())["Task"][
            "answer"
        ]
        b_answer = json.loads((VARIANT_B_DIR / f"{slug}.json").read_text())["Task"][
            "answer"
        ]
        multi_answers = [
            item["answer"]
            for item in json.loads((MULTI_TASK_DIR / f"{slug}.json").read_text())[
                "answers"
            ]
        ]
        primary_answer = multi_answers[0] if multi_answers else None

        print(
            f"{slug:<12} {gold:<22} {(a_answer or '(none)'):<22}"
            f" {(b_answer or '(none)'):<22} {', '.join(multi_answers)}"
        )

        a_totals = tuple(
            x + y for x, y in zip(a_totals, score_role(gold, a_answer))
        )
        b_totals = tuple(
            x + y for x, y in zip(b_totals, score_role(gold, b_answer))
        )
        multi_totals = tuple(
            x + y for x, y in zip(multi_totals, score_role_multi(gold, multi_answers))
        )
        primary_totals = tuple(
            x + y for x, y in zip(primary_totals, score_role(gold, primary_answer))
        )
    print()

    # Diagnostic: is any-match F1 just an artifact of wide candidate lists?
    # Report list length and the position of the first (if any) matching
    # candidate, so a reader can see how much of "any-match" credit came from
    # the model's own top pick vs. a long net.
    print(f"{'Paper':<12} {'n answers':>9}  {'primary hit?':<13} {'hit position(s)'}")
    for slug, gold in GOLD_LABELS.items():
        multi_answers = [
            item["answer"]
            for item in json.loads((MULTI_TASK_DIR / f"{slug}.json").read_text())[
                "answers"
            ]
        ]
        hit_positions = [i for i, a in enumerate(multi_answers) if matches(gold, a)]
        primary_hit = bool(multi_answers) and matches(gold, multi_answers[0])
        print(
            f"{slug:<12} {len(multi_answers):>9}  {str(primary_hit):<13}"
            f" {hit_positions or '(none)'}"
        )
    print()

    print(f"{'Variant':<28} {'P':>5} {'R':>5} {'F1':>6}  {'TP':>3} {'FP':>3} {'FN':>3}")
    for label, totals in [
        ("A (joint)", a_totals),
        ("B (decomposed, single)", b_totals),
        ("Multi-valued pilot, any-match", multi_totals),
        ("Multi-valued pilot, primary-only", primary_totals),
    ]:
        p, r, f1 = precision_recall_f1(*totals[:3])
        print(
            f"{label:<28} {p:>5.2f} {r:>5.2f} {f1:>6.2f}"
            f"  {totals[0]:>3} {totals[1]:>3} {totals[2]:>3}"
        )
    print()
    print(
        "Caveat: any-match F1 is upper-bounded by list length -- it credits a hit"
        " anywhere in the candidate list, with no cap and no penalty for extra"
        " items. Primary-only F1 (scoring just answers[0], what a single-valued"
        " schema would have forced the model to commit to) is the harder, more"
        " honest number; see the position table above for where each any-match"
        " hit actually came from."
    )


if __name__ == "__main__":
    main()
