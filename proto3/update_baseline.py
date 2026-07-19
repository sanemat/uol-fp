#!/usr/bin/env python3
"""Regenerate BASELINE_ANSWERS in 3pipeline.ipynb from proto3/baseline/*.json.

Run after proto3/baseline/*.json changes:
    python proto3/update_baseline.py
"""

import json
from pathlib import Path

ROLES = ["TechnicalMethod", "Task", "Dataset", "EvaluationMetric"]
BEGIN_MARKER = "# BEGIN AUTO-GENERATED (update_baseline.py)"
END_MARKER = "# END AUTO-GENERATED"
TARGET_CELL_ID = "2b432d50"

REPO_ROOT = Path(__file__).resolve().parent
BASELINE_DIR = REPO_ROOT / "baseline"
NOTEBOOK_PATH = REPO_ROOT / "3pipeline.ipynb"


def load_baseline_answers() -> dict[str, dict[str, str | None]]:
    answers = {}
    for path in sorted(BASELINE_DIR.glob("*.json")):
        data = json.loads(path.read_text())
        answers[path.stem] = {role: data[role]["answer"] for role in ROLES}
    return answers


MAX_LINE_LENGTH = 88


def render_literal(answers: dict[str, dict[str, str | None]]) -> str:
    lines = ["BASELINE_ANSWERS = {"]
    for slug, roles in answers.items():
        lines.append(f'    "{slug}": {{')
        for role in ROLES:
            value = roles[role]
            value_repr = (
                "None" if value is None else json.dumps(value, ensure_ascii=False)
            )
            one_line = f'        "{role}": {value_repr},'
            if len(one_line) <= MAX_LINE_LENGTH:
                lines.append(one_line)
            else:
                lines.append(f'        "{role}": (')
                lines.append(f"            {value_repr}")
                lines.append("        ),")
        lines.append("    },")
    lines.append("}")
    return "\n".join(lines)


def update_notebook(new_literal: str) -> None:
    nb = json.loads(NOTEBOOK_PATH.read_text())
    for cell in nb["cells"]:
        if cell.get("id") == TARGET_CELL_ID:
            source: list[str] | str = cell["source"]
            text = "".join(source) if isinstance(source, list) else source
            if BEGIN_MARKER not in text or END_MARKER not in text:
                raise RuntimeError(
                    f"Markers not found in cell {TARGET_CELL_ID!r}; "
                    "has the cell been edited by hand?"
                )
            before, _, rest = text.partition(BEGIN_MARKER)
            _, _, after = rest.partition(END_MARKER)
            cell["source"] = (
                f"{before}{BEGIN_MARKER}\n{new_literal}\n{END_MARKER}{after}"
            )
            break
    else:
        raise RuntimeError(f"Cell {TARGET_CELL_ID!r} not found in {NOTEBOOK_PATH}")

    NOTEBOOK_PATH.write_text(json.dumps(nb, indent=1, ensure_ascii=False))


def main() -> None:
    answers = load_baseline_answers()
    literal = render_literal(answers)
    update_notebook(literal)
    print(
        f"Updated cell {TARGET_CELL_ID} from {len(answers)} baseline file(s): "
        f"{sorted(answers)}"
    )


if __name__ == "__main__":
    main()
