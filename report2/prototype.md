# Prototype: Document-Level Methodology Extraction

## 1. Template Statement

I use Template 12.1 from the Natural Language Processing (NLP) module: identifying research methodologies used in computing research papers.

## 2. Project Overview and Fit

My prototype (proto3) is a document-level methodology extraction pipeline, built after an earlier sentence-level zero-shot Natural Language Inference (NLI) prototype (proto2) showed too much output noise and no use of document-level context. Given a computing research paper, proto3 extracts one answer per role — TechnicalMethod, Task, Dataset, and EvaluationMetric — each backed by evidence: a section heading and a verbatim quote. On "Attention Is All You Need," for example, it extracts TechnicalMethod = "Transformer", Task = "machine translation", Dataset = "WMT 2014 English-German", and EvaluationMetric = "BLEU". The approach is schema-guided document-level extraction with a long-context large language model (LLM): rather than sending the paper to an LLM and trusting the answer, every answer carries evidence I can check against the source text.

This fits my overall project goal of automatically extracting research methodology from computing research papers using LLMs: proto1 is an AI-drafted reference only, proto2 was my sentence-level NLI attempt, and proto3 reframes the task as document-level extraction. This reframing is motivated directly by proto2's failures: it classified every sentence with NLI rather than performing information extraction, produced output volumes too large to use as an answer (151 TechnicalMethod sentences for MapReduce), had no way to separate the authors' own method from cited prior work (BERT's Introduction cites ELMo, which scored 0.87 as TechnicalMethod), and its recall-only evaluation (18/24 across six papers) only showed a gold term appeared somewhere among 100+ candidate sentences, not that the output itself was usable. The real question is closer to information extraction than sentence classification: what is the primary TechnicalMethod?

## 3. Features Implemented

The prototype takes TEI XML of one computing research paper (produced by GROBID) and reads the full paper as a single document, extracting one answer per role with a schema-guided prompt to a long-context LLM, to produce one JSON object per paper. Each role's entry has an `answer` plus an `evidence` object with `section` and `quote` (full example in Section 6).

Parsing the XML and extracting section text uses the same GROBID-based approach as proto2 and is already solved — it is not the core feature. The feature I am prototyping is turning a full paper into one structured, evidence-backed answer per role. This is what makes the output usable: a single named answer instead of a list of 14 to 160 candidate sentences. Structured extraction with LLMs is not itself new (see [Dagdelen et al. 2024], [Polak and Morgan 2024]); I apply it to this project's specific four-role methodology schema. The evidence field is not decorative — it is what makes the answer checkable and what makes the evaluation in Section 7 possible.

## 4. Algorithms, Techniques and Methods

The pipeline has five stages:

```
PDF
  → GROBID (Stage 0: parse sections, same as proto2)
  → structured TEI document (Abstract + body sections, References/Acknowledgements skipped)
  → Stage 1: concatenate section texts in reading order, no sentence-level filtering
  → Stage 2: LLM extraction with a schema-guided prompt
  → MethodologyProfile JSON (answer + evidence per role)
```

Stage 0 skips References and Acknowledgements by heading:

```python
SKIP_HEADINGS = {"references", "acknowledgements", "acknowledgments"}
...
for div in root.findall(".//tei:body//tei:div", NS):
    heading = div.findtext("tei:head", namespaces=NS) or ""
    if heading.lower().strip() in SKIP_HEADINGS:
        continue
```

Stage 1 joins the remaining section texts in order, with no sentence splitting and no per-sentence threshold — the key difference from proto2, where the LLM now sees the (mostly) whole document and returns one decision per role rather than a list of candidates.

I use document-level extraction, and feed the LLM the full paper rather than a filtered excerpt, because a significant amount of information can only be found by analysing the full document [Jain et al. 2020]. Dataset and EvaluationMetric typically appear only in the Experiment section, not the Abstract or Method, so a filtered excerpt would recreate the same recall gap document-level extraction is meant to avoid. The papers I use fit within the model's context window, so I send the full structured paper directly rather than introducing chunking or retrieval. I use Gemini (`gemini-3.5-flash`, via the `google-genai` software development kit).

The four-role schema is enforced by naming all four roles explicitly and giving the exact output shape in the prompt — one JSON object per role with an `answer` and a nested `evidence` object — with the quote required verbatim rather than paraphrased, and `null` returned for a role that is absent rather than guessed. One explicit rule, "use the authors' own method, not methods cited from prior work," targets proto2's biggest known failure directly; Section 5 quotes and explains this rule set.

## 5. Code Explanation

The prompt template (`proto3/3pipeline.ipynb`, "Stage 2b — Prompt Template"):

```
Rules:
- Use the authors' own method, not methods cited from prior work.
- If a field is not present in the paper, return null for both "answer" and "evidence".
- The "quote" must be copied verbatim from the paper text, not paraphrased.
```

`answer` is constrained elsewhere in the prompt to the shortest identifying term, so the model returns a usable label such as "Transformer" instead of a full sentence — proto2's core problem, where the "answer" was really 151 candidate sentences. `evidence` is a nested object rather than a single string so `section` and `quote` stay separate fields; this was not my first design. An earlier version asked for a single string, and Gemini merged the heading and quote together, which is not checkable. The verbatim-quote rule matters because my Section 7 evidence check needs to confirm the quote appears in the paper text word-for-word.

The call and response parsing (`proto3/3pipeline.ipynb`, "Stage 2c — Call Gemini and Parse Response"):

```python
response = client.models.generate_content(
    model=MODEL_NAME,
    contents=prompt,
    config=types.GenerateContentConfig(temperature=0, seed=0),
)

raw_text = response.text.strip()
if raw_text.startswith("```"):
    raw_text = raw_text.strip("`")
    raw_text = raw_text.removeprefix("json").strip()

profile = json.loads(raw_text)
```

sends the prompt to `client.models.generate_content` and parses the response with `json.loads` after stripping any Markdown code fence Gemini adds around the JSON. I added `config=types.GenerateContentConfig(temperature=0, seed=0)` after testing: this is schema-guided extraction, not creative generation, so I do not want sampling diversity, and a fixed seed is a second determinism lever alongside temperature zero. Even with both set, some LLM serving backends, including Gemini's, may still vary slightly at temperature zero (for example through batching effects), so exact reproducibility across runs is not fully guaranteed.

During testing on "Attention Is All You Need," I found a concrete bug: an earlier prompt version asked for "evidence" as a single quoted sentence but also said to return the section heading and the quote together — an internally inconsistent instruction. Gemini resolved the ambiguity by returning `evidence` as one flat string with the heading prepended, not the nested object the design intended. I fixed this by rewriting the prompt to make the nested shape explicit, after which `evidence.section` and `evidence.quote` came back as reliably separate fields.

On code quality: I use `pyright` in `strict` type-checking mode and `ruff` for linting and formatting, the same strict setup as proto2, now applied to this new pipeline. The notebook is organised into named, ordered stages (Setup, Data Models, Stage 0, Stage 1, Stage 2, Stage 2b, Stage 2c) as markdown headers, so the pipeline structure is visible directly in the table of contents. Two honest limitations remain: this is still notebook code that mixes exploratory output with pipeline logic, with no automated tests yet for the JSON-parsing or evidence-validation logic even though `pytest` is a listed development dependency; and `proto3/baseline.ipynb`, a byte-identical duplicate of `proto3/3pipeline.ipynb` used to produce the six baseline outputs, still has a Colab-badge cell linking to `3pipeline.ipynb` rather than its own filename.

## 6. Visual Representation / Demonstration

For "Attention Is All You Need," the full output is:

```json
{
  "TechnicalMethod": {
    "answer": "Transformer",
    "evidence": {
      "section": "Abstract",
      "quote": "We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely."
    }
  },
  "Task": {
    "answer": "machine translation",
    "evidence": {
      "section": "Abstract",
      "quote": "Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train."
    }
  },
  "Dataset": {
    "answer": "WMT 2014 English-German",
    "evidence": {
      "section": "Training Data and Batching",
      "quote": "We trained on the standard WMT 2014 English-German dataset consisting of about 4.5 million sentence pairs."
    }
  },
  "EvaluationMetric": {
    "answer": "BLEU",
    "evidence": {
      "section": "Machine Translation",
      "quote": "On the WMT 2014 English-to-German translation task, the big transformer model (Transformer (big) in Table 2) outperforms the best previously reported models (including ensembles) by more than 2.0 BLEU, establishing a new state-of-the-art BLEU score of 28.4."
    }
  }
}
```

This is real pipeline output, not a mockup. Compared with proto2's output for the same paper (14 TechnicalMethod, 0 Task, 0 Dataset, 160 EvaluationMetric sentences), proto3 returns one checkable answer per role, each with a specific place in the paper to verify it against.

Figures 1–2 contrast proto2's sentence-count output with proto3's answer-and-evidence output:

![proto3 output](<./Screenshot 2026-07-18 195120.png>)
![proto2 output](<./Screenshot 2026-07-18 195636.png>)

## 7. Evaluation and Improvement

I evaluate on the same six papers and gold labels as proto2, on three axes: (1) gold label match — does `answer` contain the gold label as a substring, now applied to one answer per role instead of over 100 candidate sentences, much harder to pass; (2) human precision — is `answer` plausibly correct by human judgment, catching valid answers that miss the gold string and wrong answers that happen to match it; and (3) an evidence check — does `evidence.quote` support `answer`; is it about the paper's own work, not prior work; does the quote appear verbatim in the paper; and is `evidence.section` correct. This checks precision, not just recall, which proto2's recall-only score could not do.

Testing on "Attention Is All You Need" surfaced the evidence-shape bug from Section 5. Since fixing it, I have run Stage 0–2 on all six proto2 papers (Transformer, BERT, AlexNet, ResNet, MapReduce, PageRank); raw output is saved in `proto3/baseline/*.json`. The formal three-axis evaluation has not been run yet — no scoring script, no pass/fail count — and a Related Work ablation and wider batch processing are also not yet implemented.

As an informal, hand-checked gold-label match only:

| Paper | TechnicalMethod | Task | Dataset | EvaluationMetric | Score |
|---|---|---|---|---|---|
| Transformer | match | match | match | match | 4/4 |
| BERT | match | no | no | match | 2/4 |
| AlexNet | match | match | match | match | 4/4 |
| ResNet | match | no | match | match | 3/4 |
| MapReduce | match | no | no (null) | no | 1/4 |
| PageRank | no | no | match | no (null) | 1/4 |

Total: 15/24 (62.5%). Strict substring matching penalises near misses — ResNet's "image classification" versus the gold "image recognition" is arguably close but scored a miss — and MapReduce and PageRank each have one `null` field, always a miss under this method. This is a rough indicator, not a final result: the baseline files were generated before I added `temperature=0`/`seed=0` to the Gemini call, so scores may shift once I run the formal evaluation against fresh output.

Next, I will score the six existing outputs against the gold labels with the three-axis method above — extraction is done; scoring it is what remains. I can then compare against proto2's 18/24 (75%) recall-only result, though not directly comparable: my check is against one answer per role, not acceptance anywhere among 100+ sentences, so a lower raw score could still be a stronger result. I also plan a Related Work ablation to test whether extra context helps or introduces attribution noise (visible through `evidence.section`), and to automate the evidence verbatim check instead of checking it by hand.

## References

[Dagdelen et al. 2024] John Dagdelen, Alexander Dunn, Sanghoon Lee, Nicholas Walker, Andrew S. Rosen, Gerbrand Ceder, Kristin A. Persson, and Anubhav Jain. 2024. Structured information extraction from scientific text with large language models. *Nature Communications* 15 (2024), 1418. DOI: https://doi.org/10.1038/s41467-024-45563-x

[Jain et al. 2020] Sarthak Jain, Madeleine Van Zuylen, Hannaneh Hajishirzi, and Iz Beltagy. 2020. SciREX: A Challenge Dataset for Document-Level Information Extraction. In *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, Online, July 2020. Association for Computational Linguistics, 7506–7516. DOI: https://doi.org/10.18653/v1/2020.acl-main.670

[Polak and Morgan 2024] Maciej P. Polak and Dane Morgan. 2024. Extracting accurate materials data from research papers with conversational language models and prompt engineering. *Nature Communications* 15 (2024), 1569. DOI: https://doi.org/10.1038/s41467-024-45914-8

## Appendix: Full Extraction Output for the Remaining Five Papers

Real pipeline output, matching `proto3/baseline/*.json` exactly.

```json
{
  "TechnicalMethod": {
    "answer": "deep convolutional neural network",
    "evidence": {
      "section": "Abstract",
      "quote": "We trained a large, deep convolutional neural network to classify the 1.2 million high-resolution images in the ImageNet LSVRC-2010 contest into the 1000 different classes."
    }
  },
  "Task": {
    "answer": "object recognition",
    "evidence": {
      "section": "Introduction",
      "quote": "Current approaches to object recognition make essential use of machine learning methods."
    }
  },
  "Dataset": {
    "answer": "ImageNet",
    "evidence": {
      "section": "The Dataset",
      "quote": "ImageNet is a dataset of over 15 million labeled high-resolution images belonging to roughly 22,000 categories."
    }
  },
  "EvaluationMetric": {
    "answer": "top-1 and top-5 error rates",
    "evidence": {
      "section": "The Dataset",
      "quote": "On ImageNet, it is customary to report two error rates: top-1 and top-5, where the top-5 error rate is the fraction of test images for which the correct label is not among the five labels considered most probable by the model."
    }
  }
}
```

```json
{
  "TechnicalMethod": {
    "answer": "BERT",
    "evidence": {
      "section": "Abstract",
      "quote": "We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers."
    }
  },
  "Task": {
    "answer": "Language model pre-training",
    "evidence": {
      "section": "Introduction",
      "quote": "Language model pre-training has been shown to be effective for improving many natural language processing tasks (Dai and  Le, 2015; Peters et al., 2018a; Radford et al., 2018; Howard and Ruder, 2018) ."
    }
  },
  "Dataset": {
    "answer": "SQuAD v1.1",
    "evidence": {
      "section": "SQuAD v1.1",
      "quote": "The Stanford Question Answering Dataset (SQuAD v1.1) is a collection of 100k crowdsourced question/answer pairs  (Rajpurkar et al., 2016) ."
    }
  },
  "EvaluationMetric": {
    "answer": "F1 score",
    "evidence": {
      "section": "SQuAD v1.1",
      "quote": "Our single BERT model outperforms the top ensemble system in terms of F1 score."
    }
  }
}
```

```json
{
  "TechnicalMethod": {
    "answer": "MapReduce",
    "evidence": {
      "section": "Abstract",
      "quote": "MapReduce is a programming model and an associated implementation for processing and generating large data sets."
    }
  },
  "Task": {
    "answer": "automatic parallelization and distribution of large-scale computations",
    "evidence": {
      "section": "Introduction",
      "quote": "The major contributions of this work are a simple and powerful interface that enables automatic parallelization and distribution of large-scale computations, combined with an implementation of this interface that achieves high performance on large clusters of commodity PCs."
    }
  },
  "Dataset": {
    "answer": null,
    "evidence": null
  },
  "EvaluationMetric": {
    "answer": "elapsed time",
    "evidence": {
      "section": "Effect of Backup Tasks",
      "quote": "The entire computation takes 1283 seconds, an increase of 44% in elapsed time."
    }
  }
}
```

```json
{
  "TechnicalMethod": {
    "answer": "Google",
    "evidence": {
      "section": "Abstract",
      "quote": "In this paper, we present Google, a prototype of a large-scale search engine which makes heavy use of the structure present in hypertext."
    }
  },
  "Task": {
    "answer": "information retrieval",
    "evidence": {
      "section": "Introduction",
      "quote": "The Web creates new challenges for information retrieval."
    }
  },
  "Dataset": {
    "answer": "24 million pages",
    "evidence": {
      "section": "Anchor-test",
      "quote": "In our current crawl of 24 million pages. we had over 259 million anchors which we indexed."
    }
  },
  "EvaluationMetric": {
    "answer": null,
    "evidence": null
  }
}
```

```json
{
  "TechnicalMethod": {
    "answer": "deep residual learning framework",
    "evidence": {
      "section": "Introduction",
      "quote": "In this paper, we address the degradation problem by introducing a deep residual learning framework."
    }
  },
  "Task": {
    "answer": "image classification",
    "evidence": {
      "section": "Introduction",
      "quote": "Deep convolutional neural networks [22, 21] have led to a series of breakthroughs for image classification [21, 49, 39]."
    }
  },
  "Dataset": {
    "answer": "ImageNet 2012 classification dataset",
    "evidence": {
      "section": "ImageNet Classification",
      "quote": "We evaluate our method on the ImageNet 2012 classification dataset [35] that consists of 1000 classes."
    }
  },
  "EvaluationMetric": {
    "answer": "top-1 and top-5 error rates",
    "evidence": {
      "section": "ImageNet Classification",
      "quote": "We evaluate both top-1 and top-5 error rates."
    }
  }
}
```

### Gold labels (six papers)

| Paper | Gold TechnicalMethod | Gold Task | Gold Dataset | Gold EvaluationMetric |
|---|---|---|---|---|
| Transformer | "Transformer" | "machine translation" | "WMT" | "BLEU" |
| BERT | "BERT" | "GLUE" or "SQuAD" | "BooksCorpus" or "Wikipedia" | "F1" or "accuracy" |
| AlexNet | "convolutional" (paper predates the name "AlexNet") | "object recognition" | "ImageNet" | "top-1" or "top-5" |
| ResNet | "residual" | "image recognition" | "ImageNet" | "top-1" |
| MapReduce | "MapReduce" | "distributed" | "TeraSort" | "seconds" |
| Google Search | "PageRank" | "web search" | "million pages" | "quality" |

### proto2 background data

| Paper | TM | Task | Dataset | EM | Hypothesis set |
|---|---|---|---|---|---|
| Transformer | 14 | 0 | 0 | 160 | verbose_v1 |
| BERT | 62 | 23 | 15 | 13 | short |
| AlexNet | 51 | 6 | 11 | 4 | short |
| ResNet | 51 | 6 | 14 | 12 | short |
| MapReduce | 151 | 24 | 3 | 5 | short |
| Google Search | 69 | 21 | 8 | 29 | short |

proto2 extended evaluation result (`report1/report.md` Appendix B): total 18/24 (75%) — ML papers 13/16 (81%), systems papers 5/8 (63%). Failures: ResNet ✗ Task, MapReduce ✗ Task + Dataset, Google Search ✗ TechnicalMethod ("PageRank" never appears in the TechnicalMethod output).
