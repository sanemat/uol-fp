# Demo Script — Auto-Extracting Research Methodology from Papers

Total: ~3 minutes

---

## [0:00–0:10] Introduction

*[Show title slide or notebook top]*

"In this video I'll demonstrate a prototype that automatically extracts
research methodology from computing papers."

---

## [0:10–0:40] Motivation

*[Stay on slide or scroll to motivation cell]*

"When you read a research paper, it can be hundreds of sentences long.
But you usually want to know just four things:
what method did they use, what task did they solve,
what data did they train on, and how did they measure results.

Finding this manually takes time, and it doesn't scale
when you have many papers to read.
This prototype does it automatically."

---

## [0:40–1:05] Approach

*[Show pipeline overview]*

"The pipeline works in two stages.
First, I convert a PDF to structured XML using a tool called GROBID,
which runs locally on my machine.

Then, inside Google Colab, the notebook loads that XML,
splits the text into sentences,
and classifies each sentence into one of four roles
using a technique called zero-shot NLI.

Zero-shot means the model was never trained on research papers specifically.
Instead, it answers a simple question for each sentence:
does this sentence describe a technical method?
Does it describe a dataset? And so on.
No labeled training data is needed."

---

## [1:05–1:10] Demo Transition

*[Switch to Colab — open 2pipeline.ipynb]*

"Let me run it now on the BERT paper."

---

## [1:10–2:10] Live Demo

*[Run Setup cell]*

"First I install the dependencies — transformers, spaCy, and torch.
This takes about thirty seconds on a fresh Colab runtime."

*[Run Model Setup cell — classifier loads]*

"Now the NLI model is loaded. It's about 568 megabytes
and fits within the free Colab memory limit."

*[Run Step 0 — upload XML, show section list]*

"I upload the BERT paper XML produced by GROBID.
The notebook finds twelve sections — Abstract, Introduction,
Related Work is skipped automatically, then Model Architecture,
Training, Experiments, and so on."

*[Run Step 0c — sentence splitting, show count]*

"After cleaning and splitting, we have 258 valid sentences
ready for classification."

*[Run Step 2 — classification, scroll through output]*

"Now the model classifies each sentence.
You can see the top label and score for each one.
A checkmark means the score is at or above 0.5 and the sentence is accepted."

*[Scroll to final JSON output]*

"Here is the final output.
TechnicalMethod contains sentences about BERT itself.
Task contains sentences about the GLUE benchmark.
Dataset contains sentences about BooksCorpus.
EvaluationMetric contains sentences mentioning F1 score.
All four roles are found correctly."

---

## [2:10–2:35] Results

*[Show results slide or results cell]*

"I tested the pipeline on six papers in total.
Using a gold label check — one known answer per role per paper —
BERT scored four out of four, and AlexNet also scored four out of four.

The Transformer paper scored two out of four,
but this was caused by the hypothesis wording I used,
not by the pipeline failing to find the information."

---

## [2:35–2:55] Limitations and Next Steps

*[Show limitations slide or next steps cell]*

"The main limitation is noise from the Introduction section,
where the paper describes other researchers' methods,
and the model incorrectly assigns those to the target paper.

The next step is a second NLI pass that filters sentences
to keep only those used by the authors themselves,
and a top-three selection to reduce the large output volume."

---

## [2:55–3:00] Wrap-up

"Thank you for watching."

---

## Notes for recording

- Upload the BERT XML before starting to record — avoids waiting for the file dialog
- Pre-run Setup and Model Setup cells if runtime allows — saves ~40 seconds on camera
- Keep the browser zoom at 100% so output text is readable
