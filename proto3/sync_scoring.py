#!/usr/bin/env python3
"""Regenerate the scoring-functions cell in 3pipeline.ipynb from
proto3/src/uol_fp/scoring.py.

Run after proto3/src/uol_fp/scoring.py changes:
    python proto3/sync_scoring.py
"""

import json
from pathlib import Path

BEGIN_MARKER = "# BEGIN AUTO-GENERATED (sync_scoring.py)"
END_MARKER = "# END AUTO-GENERATED"
TARGET_CELL_ID = "7964702d"

REPO_ROOT = Path(__file__).resolve().parent
SCORING_MODULE = REPO_ROOT / "src" / "uol_fp" / "scoring.py"
NOTEBOOK_PATH = REPO_ROOT / "3pipeline.ipynb"


def render_literal() -> str:
    return SCORING_MODULE.read_text().rstrip("\n")


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
                f"{before}{BEGIN_MARKER}\n{new_literal}\n\n\n{END_MARKER}{after}"
            )
            break
    else:
        raise RuntimeError(f"Cell {TARGET_CELL_ID!r} not found in {NOTEBOOK_PATH}")

    NOTEBOOK_PATH.write_text(json.dumps(nb, indent=1, ensure_ascii=False))


def main() -> None:
    literal = render_literal()
    update_notebook(literal)
    print(f"Updated cell {TARGET_CELL_ID} from {SCORING_MODULE}")


if __name__ == "__main__":
    main()
