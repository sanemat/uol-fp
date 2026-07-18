# Prototype: Document-Level Methodology Extraction (884 words, exclude: References, Appendix)

<style>
@page {
  margin: 2cm;
}
body {
  font-size: 12pt;
}
code, pre, pre code {
  font-size: 12pt !important;
  white-space: pre-wrap !important;
  word-break: break-word !important;
  overflow-wrap: anywhere !important;
}
</style>

## 1. Template Statement

I use Template 12.1 from the Natural Language Processing (NLP) module: identifying research methodologies used in computing research papers.

## 2. Project Overview and Fit

proto3 is a document-level methodology extraction pipeline, built after an earlier sentence-level zero-shot Natural Language Inference (NLI) prototype (proto2) produced too much noise and ignored document-level context. Given a computing paper, it extracts one answer per role — TechnicalMethod, Task, Dataset, EvaluationMetric — each with a section heading and a verbatim quote as evidence, using a schema-guided prompt to a long-context large language model (LLM). On "Attention Is All You Need": TechnicalMethod = "Transformer", Task = "machine translation", Dataset = "WMT 2014 English-German", EvaluationMetric = "BLEU".

proto1 is an AI-drafted reference only; proto2 was my sentence-level NLI attempt; proto3 reframes the task as document-level extraction. proto2 classified every sentence rather than extracting an answer, produced 151 TechnicalMethod sentences for MapReduce alone, and had no way to separate the authors' own method from cited prior work — BERT's Introduction cites ELMo, which NLI scored 0.87 as TechnicalMethod. Its recall-only evaluation (18/24 across six papers) only checked whether a gold term appeared somewhere among 100+ sentences, not whether the output was correct.

## 3. Features Implemented

The prototype takes GROBID TEI XML and produces one JSON object containing an answer and evidence for each of the four roles (full example in Section 6).

Parsing the XML and extracting section text reuses proto2's GROBID-based approach — not the core feature here. The core feature is extracting one structured answer and its evidence for each role. Structured extraction with LLMs is not itself new (see [Dagdelen et al. 2024], [Polak and Morgan 2024]); I apply it to this project's four-role schema.

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

Stage 1 joins the remaining section texts in order, with no sentence splitting and no per-sentence threshold.

Dataset and EvaluationMetric often occur in experimental sections rather than the Abstract or Method [Jain et al. 2020], so I retain the full document rather than an excerpt. The papers I use fit within the model's context window, so I send the full structured paper directly rather than introducing chunking or retrieval. I use Gemini (`gemini-3.5-flash`, via the `google-genai` software development kit).

The prompt names all four roles and specifies the required JSON structure. Quotes must be verbatim, and absent roles are returned as `null`. One rule, "use the authors' own method, not methods cited from prior work," is explained further in Section 5.

## 5. Code Explanation

The prompt template (`proto3/3pipeline.ipynb`, "Stage 2b — Prompt Template"):

```
Rules:
- Use the authors' own method, not methods cited from prior work.
- If a field is not present in the paper, return null for both "answer" and "evidence".
- The "quote" must be copied verbatim from the paper text, not paraphrased.
```

`evidence` is a nested object rather than a single string so `section` and `quote` stay separate fields for the checks in Section 7.

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

The Markdown-fence strip exists because Gemini does not always return pure JSON. `json.loads` has no fallback if parsing fails — that path is untested. I am not yet using Gemini's structured-output/JSON-schema API. `temperature=0` and `seed=0` reduce variation, but exact reproducibility is not guaranteed.

An earlier prompt described `evidence` inconsistently, so Gemini returned the heading and quote as one string. Specifying the nested object explicitly fixed this.

Code quality: `pyright` runs in `strict` mode and `ruff` lints and formats, the same setup as proto2. The notebook is organised into named stages (Setup through Stage 2c) as markdown headers. It still mixes exploratory output with pipeline logic, and there are no automated tests for the JSON-parsing or evidence-validation logic yet.

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

This output is from `proto3/baseline/transformer.json` (compared with proto2's output for the same paper in Section 2).

Figures 1–2 contrast proto2's sentence-count output with proto3's answer-and-evidence output:

![proto3 output](<./Screenshot 2026-07-18 195120.png>)
![proto2 output](<./Screenshot 2026-07-18 195636.png>)

## 7. Evaluation and Improvement

I evaluate on the same six papers and gold labels as proto2, on three axes. Gold label match: does `answer` contain the gold label as a substring. Human precision: is `answer` plausibly correct by human judgment. Evidence check: does `evidence.quote` support `answer`, is it about the paper's own work rather than prior work, does the quote appear verbatim in the paper, and is `evidence.section` correct.

Testing on "Attention Is All You Need" surfaced the evidence-shape bug from Section 5. Since fixing it, I have run Stage 0–2 on all six proto2 papers (Transformer, BERT, AlexNet, ResNet, MapReduce, Google Search); raw output is saved in `proto3/baseline/*.json`. The formal three-axis evaluation and Related Work ablation have not yet been implemented.

As an informal, hand-checked gold-label match only:

| Paper | TechnicalMethod | Task | Dataset | EvaluationMetric | Score |
|---|---|---|---|---|---|
| Transformer | match | match | match | match | 4/4 |
| BERT | match | no | no | match | 2/4 |
| AlexNet | match | match | match | match | 4/4 |
| ResNet | match | no | match | match | 3/4 |
| MapReduce | match | no | no (null) | no | 1/4 |
| Google Search | no | no | match | no (null) | 1/4 |

Total: 15/24 (62.5%). Substring matching penalises near misses (ResNet's "image classification" vs. gold "image recognition") and null fields (MapReduce, Google Search) always score as a miss. Some misses reflect gold-label ambiguity rather than extraction failure: BERT's Task miss is scored against benchmark names ("GLUE"/"SQuAD"), while proto3 answered with the paper's own framing ("Language model pre-training") — the schema does not distinguish a research task from a downstream benchmark from a pre-training objective. These six baseline files also predate the `temperature=0`/`seed=0` change, so scores may shift on a fresh run.

The next step is to implement the three-axis evaluation for the six saved outputs. After that, I will test whether including Related Work changes attribution errors.

## References

[Dagdelen et al. 2024] John Dagdelen, Alexander Dunn, Sanghoon Lee, Nicholas Walker, Andrew S. Rosen, Gerbrand Ceder, Kristin A. Persson, and Anubhav Jain. 2024. Structured information extraction from scientific text with large language models. *Nature Communications* 15 (2024), 1418. DOI: https://doi.org/10.1038/s41467-024-45563-x

[Jain et al. 2020] Sarthak Jain, Madeleine Van Zuylen, Hannaneh Hajishirzi, and Iz Beltagy. 2020. SciREX: A Challenge Dataset for Document-Level Information Extraction. In *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, Online, July 2020. Association for Computational Linguistics, 7506–7516. DOI: https://doi.org/10.18653/v1/2020.acl-main.670

[Polak and Morgan 2024] Maciej P. Polak and Dane Morgan. 2024. Extracting accurate materials data from research papers with conversational language models and prompt engineering. *Nature Communications* 15 (2024), 1569. DOI: https://doi.org/10.1038/s41467-024-45914-8

## Appendix: Full Extraction Output for the Remaining Five Papers

Outputs from `proto3/baseline/*.json`.

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
