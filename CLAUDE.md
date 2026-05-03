# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a UoL (University of London) final project for CM3060 Natural Language Programming.

**Goal:** Automatically extract research methodology from computing research papers using LLMs.

**Methodology structure (4 parts):**
- **Design** — type of research (experiment, theoretical)
- **Method** — model or algorithm (e.g. BERT, CNN)
- **Data** — dataset or source (e.g. MNIST)
- **Evaluation** — metrics (e.g. accuracy, F1)

## Repository Layout

- `pitch.md` — project pitch slides (presentation source)
- `week*.md` — weekly course notes
- `proto1/` — Python prototype (pipeline implementation)
  - `pipeline.ipynb` — **main notebook, runs on Google Colab**
  - `src/uol_fp/` — shared library (models, design detector, consistency checker)
  - `tests/` — unit tests for the shared library
  - `pyproject.toml` — Pyright + Ruff config
  - `.tool-versions` — Python 3.14.1 (managed by asdf)

## Development Setup (proto1/)

```bash
cd proto1
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Commands (proto1/)

```bash
# Type check
pyright

# Lint
ruff check src/

# Format
ruff format src/

# Run a single test (once tests exist)
python -m pytest tests/test_<name>.py
```

## Pipeline Architecture (proto1/)

All pipeline steps run in `pipeline.ipynb` on Google Colab.

1. **Candidate extraction** — SciBERT (`allenai/scibert_scivocab_uncased`) + regex
2. **Role classification** — rule-based (Method / Data / Evaluation / Other)
3. **Design detection** — rule pattern matching (experiment, survey, case study, etc.)
4. **Structured output** — JSON with Design, Method, Data, Evaluation fields
5. **Consistency checking** — validation rules (e.g. experiment → needs Data + Evaluation)

The `src/uol_fp/` library contains the shared Python models and rule logic.
Local commands (pyright, ruff, pytest) are for the library only — not for running the pipeline.

Focus is on a **working prototype**, not perfect accuracy. Avoid complex model training.

## Tool Management

`aqua.yaml` manages CLI tools (uses [aqua](https://aquaproj.github.io/)). Run `aqua install` to install declared tools.
