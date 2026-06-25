# Demo Script — Auto-Extracting Research Methodology from Papers

Total: ~3 minutes

Stage directions: `▶ run` = click Run on that cell now. `(pre-run)` = already executed before recording.

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
This is the BERT paper by Devlin et al., published in 2019."

---

## [0:45–1:00] Show the XML

*[Open BERT XML in editor or file viewer]*

"First I convert the PDF to TEI XML using a tool called GROBID,
which runs locally.
The XML preserves the document structure — sections, headings, paragraphs —
in a format the pipeline can read."

---

## [1:00–2:45] Colab Demo

*[Switch to Google Colab — 2pipeline.ipynb]*

---

### [1:00–1:10] Setup

*[Scroll to Setup section — cells already executed (pre-run)]*

`(pre-run)` Python version check → pip install transformers torch spacy → imports → Data Models

"The notebook starts with setup — installing libraries and defining data models.
I've already run these to save time.
You can see 'Setup complete' and 'Models ready' in the output."

---

### [1:10–1:20] Model load

*[Scroll to Model Setup cell — already executed (pre-run)]*

`(pre-run)` spacy load + classifier pipeline load → "Models ready."

"The NLI model is also pre-loaded.
It's about 568 megabytes and runs on the free Colab GPU."

---

### [1:20–1:40] Load XML

*[Scroll to Step 0 cell]*

`▶ run` Step 0 — upload dialog appears → select BERT XML → output shows section list

"Now I upload the BERT XML.
The notebook parses all body sections and skips References,
Acknowledgements, and Related Work automatically.

The design decision here is to include all other sections —
rather than filtering by keyword.
An earlier version that filtered by keyword missed the Training Data section."

*[Wait for output — section list printed]*

"You can see twelve sections loaded —
Abstract, Introduction, Conclusion, and so on."

---

### [1:40–1:50] Select sections

*[Step 0b cell]*

`▶ run` Step 0b — target_sections = sections → prints section list again

"This cell confirms which sections go into the pipeline.
All loaded sections are used."

---

### [1:50–2:05] Sentence splitting

*[Step 0c cell]*

`▶ run` Step 0c — sentence splitting → "Total sentences: 258" + first 5 lines

"The text is cleaned first — inline citation markers like [13] are removed —
then split into sentences using spaCy.
That gives us 258 valid sentences ready for classification."

---

### [2:05–2:20] Classification

*[Step 2 cell]*

`▶ run` Step 2 — classification starts, first few lines print

"Now the model classifies each sentence using zero-shot NLI.
Instead of training on labeled examples,
the model answers a question for each sentence:
does this sentence describe a technical method? A dataset? And so on.
This avoids the need for task-specific labeled training data."

*[After ~5 lines print, scroll down to pre-run output cell below]*

"Classification takes a few minutes on 258 sentences,
so I have the completed output here from a previous run."

*[Show pre-run output — scroll through a few lines]*

"Each line shows the section, the sentence, the predicted label, and the score.
A checkmark means the score is at or above 0.5 and the sentence is accepted.
The labels are short strings — 'technical method', 'task', 'dataset', 'evaluation metric' —
and the model scores each sentence against all four."

---

### [2:20–2:30] JSON output

*[Scroll to final JSON in pre-run output]*

"Here is the final output.
TechnicalMethod contains sentences about BERT itself.
Task contains sentences about the GLUE benchmark.
Dataset contains sentences about BooksCorpus.
EvaluationMetric contains sentences mentioning F1 score.
All four gold labels appear in the output."

---

## [2:30–2:45] Results

*[Stay in Colab or show results summary cell]*

"I ran the pipeline on six papers in total.
For three of them — BERT, AlexNet, and ResNet —
I checked one gold label per role and the pipeline found all four in the output.

For systems papers like MapReduce and Google Search,
the output looked different.
TechnicalMethod had over 150 sentences in some cases,
while Dataset and EvaluationMetric had almost none.
This is likely because systems papers describe the system throughout,
and they don't follow the standard ML benchmark structure with a clear dataset and metric.

So the approach appears to work better for ML papers than for systems papers at this stage."

---

## [2:45–3:00] Summary

*[Camera]*

"The prototype shows that zero-shot NLI can find relevant methodology sentences
in ML papers without any labeled training data,
though output volume and systems papers remain challenges.
Thank you."

---

## Notes for recording

- Pre-run before recording: Python check, pip install, imports, Data Models, Model Setup
- Pre-run Step 2 (classification) and keep output visible below the live cell
- Upload BERT XML before starting — avoids the file dialog on camera
- Keep browser zoom at 100% so output is readable
