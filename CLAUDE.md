# CLAUDE.md

## Project Overview

UoL (University of London) final project for CM3060 Natural Language Programming.

**Goal:** Automatically extract research methodology from computing research papers using LLMs.

**Methodology structure (4 parts):**
- **Design** — type of research (experiment, theoretical)
- **Method** — model or algorithm (e.g. BERT, CNN)
- **Data** — dataset or source (e.g. MNIST)
- **Evaluation** — metrics (e.g. accuracy, F1)

## Repository Layout

- `pitch.md` — project pitch slides
- `week*.md` — weekly course notes
- `proto1/` — Python prototype
  - `pipeline.ipynb` — **main notebook, runs on Google Colab**
  - `pdf_to_xml.py` — CLI: converts PDF → TEI XML via local GROBID (`python pdf_to_xml.py paper.pdf`)
  - `dataset/` — input PDFs and generated TEI XML files (gitignored)
  - `Makefile` — GROBID Docker commands (`make grobid-start`, `make grobid-stop`)
  - `src/uol_fp/` — shared library (models, design detector, consistency checker)
  - `tests/` — unit tests for the shared library
  - `pyproject.toml` — Pyright + Ruff config
  - `.tool-versions` — Python 3.14.1 (managed by asdf)

## Colab Sync Workflow

Notebook syncs via GitHub — no manual upload needed.

1. **Open in Colab:** click the badge inside `pipeline.ipynb`, or use the Colab URL in the file.
2. **Save back from Colab:** File → Save a copy in GitHub → commit to `main`
3. **Pull locally:** `git pull origin main`

Cell outputs are stripped automatically on commit (`nbstripout` git filter).

**Colab branch name restriction:** Colab cannot open notebooks from branches with `/` in the name (e.g. `feat/t11` fails). Use `-` instead (e.g. `t11-e2e-test`).

## Development Setup (proto1/)

```bash
cd proto1
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Commands (proto1/)

```bash
pyright                                    # type check
ruff check src/ pipeline.ipynb            # lint
ruff format src/ pipeline.ipynb           # format
python -m pytest tests/test_<name>.py     # run a single test

make grobid-start                          # start GROBID Docker on port 8070
make grobid-stop                           # stop GROBID
python pdf_to_xml.py dataset/paper.pdf    # convert PDF → TEI XML (saves paper.xml)
```

`pyright` / `ruff` / `pytest` apply to `src/uol_fp/` only — not for running the Colab pipeline.

## Coding Conventions (proto1/)

- Line length: 88 (Ruff default)
- Type annotations required in `src/uol_fp/`
- Notebook cell IDs must be stable — do not remove or rename existing IDs
- `dataset/` is gitignored — never commit PDFs or XML files

## Pipeline Architecture (proto1/)

PDF parsing runs locally; NLP pipeline runs on Colab.

```
Local:  PDF → GROBID (Docker) → TEI XML
Colab:  upload TEI XML → parse sections → extract candidates → classify → output JSON
```

Colab pipeline steps (`pipeline.ipynb`):

1. **Load TEI XML** — ElementTree parse; produces `sections: list[dict]` with `heading` + `text`
2. **Candidate extraction** — regex per section; `CandidateWithContext(candidate, sentence, section)`
3. **Role classification** — rule-based (Method / Task / Data / Evaluation / Other)
4. **Design detection** — regex on full text of all sections
5. **Structured output** — JSON with Design, Method, Task, Data, Evaluation
6. **Consistency checking** — e.g. experiment without Method/Task → warning

## Constraints

- Focus on a **working prototype**, not perfect accuracy.
- Do not introduce complex model training or fine-tuning.
- Do not modify cell outputs in the notebook — `nbstripout` handles this on commit.

## Tool Management

`aqua.yaml` manages CLI tools (uses [aqua](https://aquaproj.github.io/)). Run `aqua install` to install declared tools.
