# Todo

## Setup

- [x] Set up Python environment (`proto1/`) — for local type check / tests only
- [x] Install dependencies (local: pyright, ruff, pytest)
- [ ] Set up Google Colab notebook — open `proto1/pipeline.ipynb` in Colab
- [ ] Collect sample papers for testing

## Pipeline (all steps run on Google Colab — `pipeline.ipynb`)

- [x] Step 1: Candidate extraction (SciBERT)
- [x] Step 2: Role classification (rule-based — Method / Data / Evaluation / Other)
- [x] Step 3: Design detection (rules)
- [x] Step 4: Build JSON output
- [x] Step 5: Consistency checking rules

## Evaluation

- [ ] Annotate gold dataset (10–20 papers, Design / Method / Data / Evaluation labels)
- [ ] Evaluate candidate extraction quality
- [ ] Evaluate role classification accuracy
- [ ] Evaluate full structure quality
