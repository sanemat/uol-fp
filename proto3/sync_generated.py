#!/usr/bin/env python3
"""Regenerate auto-generated notebook cells in 3pipeline.ipynb from their
corresponding proto3/src/uol_fp/*.py modules.

Run after proto3/src/uol_fp/models.py or proto3/src/uol_fp/scoring.py changes:
    python proto3/sync_generated.py
"""

import json
from pathlib import Path
from typing import Any

SCRIPT_NAME = "sync_generated.py"
BEGIN_MARKER = f"# BEGIN AUTO-GENERATED ({SCRIPT_NAME})"
END_MARKER = "# END AUTO-GENERATED"

REPO_ROOT = Path(__file__).resolve().parent
NOTEBOOK_PATH = REPO_ROOT / "3pipeline.ipynb"

TARGETS = [
    (REPO_ROOT / "src" / "uol_fp" / "models.py", "6"),
    (REPO_ROOT / "src" / "uol_fp" / "scoring.py", "7964702d"),
]


def render_literal(module_path: Path) -> str:
    return module_path.read_text().rstrip("\n")


def update_cell(nb: dict[str, Any], cell_id: str, new_literal: str) -> None:
    for cell in nb["cells"]:
        if cell.get("id") == cell_id:
            source: list[str] | str = cell["source"]
            text = "".join(source) if isinstance(source, list) else source
            if BEGIN_MARKER not in text or END_MARKER not in text:
                raise RuntimeError(
                    f"Markers not found in cell {cell_id!r}; "
                    "has the cell been edited by hand?"
                )
            before, _, rest = text.partition(BEGIN_MARKER)
            _, _, after = rest.partition(END_MARKER)
            cell["source"] = (
                f"{before}{BEGIN_MARKER}\n{new_literal}\n\n\n{END_MARKER}{after}"
            )
            return
    raise RuntimeError(f"Cell {cell_id!r} not found in {NOTEBOOK_PATH}")


def main() -> None:
    nb: dict[str, Any] = json.loads(NOTEBOOK_PATH.read_text())
    for module_path, cell_id in TARGETS:
        update_cell(nb, cell_id, render_literal(module_path))
        print(f"Updated cell {cell_id} from {module_path}")
    NOTEBOOK_PATH.write_text(json.dumps(nb, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
