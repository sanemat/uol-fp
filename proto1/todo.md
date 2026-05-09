# Todo

## Setup

- [x] Set up Python environment (`proto1/`) — for local type check / tests only
- [x] Install dependencies (local: pyright, ruff, pytest)
- [ ] Set up Google Colab notebook — open `proto1/pipeline.ipynb` in Colab
- [ ] Collect sample papers for testing

## Pipeline (all steps run on Google Colab — `pipeline.ipynb`)

- [x] Step 1: Candidate extraction (SciBERT)
- [x] Step 2: Role classification (rule-based — Method / Task / Data / Evaluation / Other)
- [x] Step 3: Design detection (rules)
- [x] Step 4: Build JSON output
- [x] Step 5: Consistency checking rules

## Candidate Context (next small change)

- [ ] Add `CandidateWithContext` dataclass to `src/uol_fp/models.py`
  - fields: `candidate`, `sentence`, `section`, `source_paper`
- [ ] Add `src/uol_fp/candidate_extractor.py` — `extract_candidates_with_context()`
  - section detection: best-effort heuristic (short line, no trailing punctuation)
  - falls back to `section="unknown"`
- [ ] Add `tests/test_candidate_extractor.py`
- [ ] Update `pipeline.ipynb` Step 1 to use `extract_candidates_with_context()`
- [ ] Add logging cell after Step 2: print `{candidate, sentence, section, role}` as JSON

## Evaluation

- [ ] Annotate gold dataset (10–20 papers, Design / Method / Task labels; Data / Evaluation optional)
- [ ] Run error analysis — classify failures: missing / noisy / wrong role
- [ ] Evaluate candidate extraction quality
- [ ] Evaluate role classification accuracy
- [ ] Evaluate full structure quality
