# Demo Script — Auto-Extracting Research Methodology from Papers

Total: ~3 minutes

---

## [0:00–0:35] Introduction & Motivation

*[Camera only — no slides]*

"In this video I'll demonstrate a prototype that automatically extracts
research methodology from computing papers.

When you read a research paper, it can be hundreds of sentences long.
But you usually want to know just four things:
what method did they use, what task did they solve,
what data did they train on, and how did they measure results.

Finding this manually takes time, and it doesn't scale well
when you have many papers to read.
This prototype is designed to automate that process."

---

## [0:35–0:45] Show the input — BERT PDF

*[Open BERT PDF on screen]*

"The input is a standard research paper PDF.
This is the BERT paper by Devlin et al., published in 2019.
The pipeline starts here."

---

## [0:45–1:00] Show the XML

*[Open BERT XML in editor or browser]*

"First I convert the PDF to TEI XML using a tool called GROBID,
which runs locally.
The XML preserves the document structure — sections, headings, paragraphs —
in a format the pipeline can read."

---

## [1:00–2:45] Colab Demo

*[Switch to Google Colab — 2pipeline.ipynb]*

---

### [1:00–1:10] Setup

*[Show Setup cell — already run]*

"The notebook installs the dependencies: transformers, spaCy, and torch.
I've already run this to save time."

---

### [1:10–1:25] Load XML — section list

*[Run Step 0 — upload XML, show section list]*

"I upload the BERT XML here.
The notebook loads all body sections and skips References,
Acknowledgements, and Related Work.

The design decision here is to include all other sections —
Abstract, Introduction, Architecture, Training, Experiments —
rather than filtering by keyword.
An earlier version that filtered by keyword missed the Training Data section entirely."

---

### [1:25–1:40] Sentence splitting

*[Run Step 0c — show sentence count]*

"The text is cleaned — citation markers like [13] are removed —
then split into sentences using spaCy.
That gives us 258 valid sentences ready for classification."

---

### [1:40–2:10] Classification

*[Run Step 2 — show first few lines printing]*

"Now the model classifies each sentence.
The technique is called zero-shot NLI.
Instead of training on labeled examples,
the model answers a question for each sentence:
does this sentence describe a technical method? A dataset? And so on.
This avoids the need for task-specific labeled training data.

Classification takes a few minutes on 258 sentences,
so I have a pre-run cell below."

*[Scroll to pre-run output cell]*

"You can see each sentence with its predicted label and score.
A checkmark means the score is at or above 0.5 and the sentence is accepted.

The hypothesis wording has a large effect on results.
I tested four versions. Short labels like 'technical method' gave the best
and most balanced output across all roles.
Longer, more detailed descriptions introduced strong label bias —
one label absorbed nearly all sentences."

---

### [2:10–2:25] JSON output

*[Scroll to final JSON output]*

"Here is the final output.
TechnicalMethod contains sentences about BERT itself.
Task contains sentences about the GLUE benchmark.
Dataset contains sentences about BooksCorpus.
EvaluationMetric contains sentences mentioning F1 score.
All four gold labels appear in the output."

---

## [2:25–2:45] Results

*[Stay in Colab or show results cell]*

"I ran this on six papers.
Using a gold label check — one expected answer per role per paper —
BERT and AlexNet each found all four roles.

The Transformer paper found two out of four.
This appears to be related to the hypothesis wording used in that run
rather than the pipeline missing the information."

---

## [2:45–3:00] Summary

*[Camera or stay in Colab]*

"The prototype shows that zero-shot NLI can extract research methodology
from structured ML papers without any labeled training data.
The main limitations are noise from the Introduction section
and large output volume in systems papers.
The next steps are a usage filter and top-three selection by score.
Thank you."

---

## Notes for recording

- Pre-run Setup, Model Setup, and Step 2 (classification) before recording
- Keep the pre-run Step 2 output visible below the live cell
- Upload BERT XML before starting — avoids the file dialog on camera
- Keep browser zoom at 100% so output is readable
