# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a UoL (University of London) final project for CM3060 Natural Language Programming.

**Goal:** Automatically extract research methodology from academic paper abstracts using LLMs.

**Methodology structure (4 parts):**
- **Design** — type of research (experiment, theoretical)
- **Method** — model or algorithm (e.g. BERT, CNN)
- **Data** — dataset or source (e.g. MNIST)
- **Evaluation** — metrics (e.g. accuracy, F1)

## Repository Layout

- `pitch.md` — project pitch slides (presentation source)
- `week*.md` — weekly course notes
- `proto1/` — Python prototype (pipeline implementation)
  - `src/` — source code (currently empty, to be built)
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

The planned pipeline (from `memo.md`):

1. **Sentence splitting** — split abstract text into sentences
2. **Sentence embedding** — SciBERT vectors (run on Google Colab, not local)
3. **Clustering** — k-means to group similar sentences
4. **Entity extraction** — rule-based keyword matching for Method/Data/Evaluation
5. **Design detection** — simple rules (e.g. "experiment" → Experiment)
6. **Structured output** — JSON with Design, Method, Data, Evaluation fields

Focus is on a **working prototype**, not perfect accuracy. Avoid complex model training.

## Tool Management

`aqua.yaml` manages CLI tools (uses [aqua](https://aquaproj.github.io/)). Run `aqua install` to install declared tools.
