# CLAUDE.md

## Project Overview

UoL (University of London) final project for CM3060 Natural Language Programming.

**Goal:** Automatically extract research methodology from computing research papers using LLMs.

## Course Constraint

AI assistance is **not allowed** for CM3060 submissions.

- `proto1/` files marked as AI drafts are **reference only** — do not copy into submissions
- `proto2/` is the workspace for work written from scratch by the user
- Code in `proto1/` may be used as a base, but must be understood and rewritten by the user

## Navigation

- Repo layout: run `ls` or `find . -maxdepth 2`
- Commands: see `proto1/Makefile` and `proto1/pyproject.toml`
- Pipeline: read `proto1/pipeline.ipynb` or `proto2/2pipeline.ipynb`
- CLI tools: run `aqua install` to install declared tools (`aqua.yaml`)

## Colab Sync Workflow

Notebook syncs via GitHub — no manual upload needed.

1. **Open in Colab:** click the badge inside `pipeline.ipynb`, or use the Colab URL in the file.
2. **Save back from Colab:** File → Save a copy in GitHub → commit to `main`
3. **Pull locally:** `git pull origin main`

Cell outputs are stripped automatically on commit (`nbwipers` git filter).

**Colab branch name restriction:** Colab cannot open notebooks from branches with `/` in the name (e.g. `feat/t11` fails). Use `-` instead (e.g. `t11-e2e-test`).

## Constraints

- Do not modify cell outputs in the notebook — `nbwipers` handles this on commit.
- Notebook cell IDs must be stable — do not remove or rename existing IDs.
- `dataset/` is gitignored — never commit PDFs or XML files.

## Writing (report1/)

Avoid absolute claims in report text:
- Do not write "X does not exist" → write "X is difficult to find" or "I could not find X"
- Do not write "X will always work" → write "X may work" or "X is expected to work"
- Do not write "all X are Y" → write "many X tend to be Y" or "X often appears to be Y"
- Use hedged language: "tends to", "appears to", "may", "suggests", "is likely"
- Expand non-general abbreviations on first use, e.g. "human-computer interaction (HCI)". Skip common terms like ML, GPU, JSON, PDF, API.
