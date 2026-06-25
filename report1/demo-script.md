# Demo Script — Auto-Extracting Research Methodology from Papers

Total: ~3 minutes

Stage directions: `▶ run` = click Run on that cell now. `(pre-run)` = already executed before recording.

---

## [0:00–0:20] Introduction & Motivation

*[Camera only — no slides]*

"This prototype automatically extracts research methodology from computing papers —
what method, what task, what data, and how results were measured.
Finding this manually takes time, so this prototype is designed to automate it."

---

## [0:20–0:30] Show the input — BERT PDF

*[Open BERT PDF on screen]*

"The input is the BERT paper by Devlin et al., 2019."

---

## [0:30–0:40] Show the XML

*[Open BERT XML in editor or file viewer]*

"GROBID converts the PDF to TEI XML locally, preserving section structure."

---

## [0:40–2:30] Colab Demo

*[Switch to Google Colab — 2pipeline.ipynb]*

---

### [0:40–0:50] Setup

*[Scroll to Setup and Model Setup sections — all pre-run]*

`(pre-run)` Python check → pip install → imports → Data Models → spacy + classifier load

"Setup and model loading are pre-run."

---

### [0:50–1:10] Load XML

*[Scroll to Step 0 cell]*

`(pre-run)` Step 0 — XML uploaded → section list printed

"The XML is uploaded here. The pipeline skips References, Acknowledgements, and Related Work,
and loads all other body sections — twenty three sections for the BERT paper."

---

### [1:10–1:20] Sentence splitting

*[Step 0c cell]*

`▶ run` Step 0c — "Total sentences: 258"

"After cleaning citation markers and splitting with spaCy, we have 258 valid sentences."

---

### [1:20–2:10] Classification

*[## Step 2 — Classify Sentences cell]*

`▶ run` Step 2 — first few lines print

"Zero-shot NLI classifies each sentence by role — no labeled training data needed.
Classification takes a few minutes, so here is the pre-run output."

*[Scroll down to ## Step 2 — Classify Sentences (Pre-run output) cell — do not scroll through it]*

*[Scroll past it to ## Step 2 — Results Summary cell]*

`▶ run` Results Summary

"Here is the summary. Each role, the count of accepted sentences,
and one example containing the expected term.
All four roles appear in the output for the BERT paper."

---

## [2:10–2:40] Results

*[Stay in Colab]*

"I ran this on six papers. For BERT, AlexNet, and ResNet, all four gold labels appeared in the output.
For systems papers like MapReduce and Google Search, TechnicalMethod dominated —
over 150 sentences in some cases — while Dataset and EvaluationMetric had almost none."

---

## [2:40–3:00] Summary

*[Camera]*

"The prototype shows that zero-shot NLI can find relevant methodology sentences
in ML papers without any labeled training data,
though output volume and systems papers remain challenges.
Thank you."

---

## Notes for recording

- Pre-run before recording: Python check, pip install, imports, Data Models, Model Setup, Step 0 (XML upload)
- Pre-run Step 2 (Pre-run output cell) — do not need to scroll through it on camera
- Pre-run Results Summary cell so output is ready
- Keep browser zoom at 100% so output is readable
