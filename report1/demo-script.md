# Demo Script — Auto-Extracting Research Methodology from Papers

Total: ~2:40

Stage directions: `▶ run` = click Run on that cell now. `(pre-run)` = already executed before recording.

With GPU runtime, all cells except pip install and model download complete instantly.

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

## [0:40–2:00] Colab Demo

*[Switch to Google Colab — 2pipeline.ipynb]*

---

### [0:40–0:50] Setup

*[Scroll to Setup and Model Setup sections — all pre-run]*

`(pre-run)` pip install → spacy download → classifier model download

`▶ run` Python check → imports → Data Models

"pip install and model download are pre-run. Everything else runs now."

---

### [0:50–1:05] Load XML

*[Scroll to Step 0 cell]*

`▶ run` Step 0 — upload XML → section list prints instantly

"The XML is uploaded here. The pipeline skips References, Acknowledgements, and Related Work,
and loads all other body sections — twenty three sections for the BERT paper."

---

### [1:05–1:15] Sentence splitting

*[Step 0c cell]*

`▶ run` Step 0c — "Total sentences: 258" — instant

"After cleaning citation markers and splitting with spaCy, we have 258 valid sentences."

---

### [1:15–1:40] Classification

*[## Step 2 — Classify Sentences cell]*

`▶ run` Step 2 — all 258 sentences classified instantly on GPU

"Zero-shot NLI classifies each sentence by role — no labeled training data needed.
With GPU, all 258 sentences finish in seconds."

---

### [1:40–1:50] Results summary

*[## Step 2 — Results Summary cell]*

`▶ run` Results Summary — instant

"Here is the summary. Each role, the count of accepted sentences,
and one example containing the expected term.
All four roles appear in the output for the BERT paper."

---

## [1:50–2:20] Results

*[Stay in Colab]*

"I ran this on six papers. For BERT, AlexNet, and ResNet, all four gold labels appeared in the output.
For systems papers like MapReduce and Google Search, TechnicalMethod dominated —
over 150 sentences in some cases — while Dataset and EvaluationMetric had almost none."

---

## [2:20–2:40] Summary

*[Camera]*

"The prototype shows that zero-shot NLI can find relevant methodology sentences
in ML papers without any labeled training data,
though output volume and systems papers remain challenges.
Thank you."

---

## Notes for recording

- Pre-run before recording: pip install (5851e3a0), Model Setup / classifier download (e3e215db)
- All other cells run live during recording
- Keep browser zoom at 100% so output is readable
