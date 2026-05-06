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

## Development Setup (proto1/)

```bash
cd proto1
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Commands (proto1/)

```bash
pyright                          # type check
ruff check src/                  # lint
ruff format src/                 # format
python -m pytest tests/test_<name>.py  # run a single test
```

These commands apply to `src/uol_fp/` only — not for running the Colab pipeline.

## Pipeline Architecture (proto1/)

All pipeline steps run in `pipeline.ipynb` on Google Colab.

1. **Candidate extraction** — SciBERT (`allenai/scibert_scivocab_uncased`) + regex
2. **Role classification** — rule-based (Method / Data / Evaluation / Other)
3. **Design detection** — rule pattern matching (experiment, survey, case study, etc.)
4. **Structured output** — JSON with Design, Method, Data, Evaluation fields
5. **Consistency checking** — validation rules (e.g. experiment → needs Data + Evaluation)

## Constraints

- Focus on a **working prototype**, not perfect accuracy.
- Do not introduce complex model training or fine-tuning.
- Do not modify cell outputs in the notebook — `nbstripout` handles this on commit.

## Tool Management

`aqua.yaml` manages CLI tools (uses [aqua](https://aquaproj.github.io/)). Run `aqua install` to install declared tools.
