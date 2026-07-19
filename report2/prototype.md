# Prototype: Document-Level Methodology Extraction (870 words, exclude: References, Appendix, figures, tables)

<style>
@page {
  margin: 2cm;
}
body {
  font-size: 12pt;
}
code, pre, pre code,
pre[class*="language-"], pre[class*="language-"] code,
code[class*="language-"] {
  font-size: 12pt !important;
  white-space: pre-wrap !important;
  word-break: break-word !important;
  overflow-wrap: anywhere !important;
  overflow-x: visible !important;
  max-width: 100% !important;
  box-sizing: border-box !important;
}
</style>

## 1. Template Statement

I use Template 12.1 from the Natural Language Processing (NLP) module: identifying research methodologies used in computing research papers.

## 2. Project Overview and Fit

proto3 is a document-level methodology extraction pipeline, built after an earlier sentence-level zero-shot Natural Language Inference (NLI) prototype (proto2) produced too much noise and ignored document-level context. Given a computing paper, it extracts one answer per role — TechnicalMethod, Task, Dataset, EvaluationMetric — each with a section heading and a verbatim quote as evidence, using a schema-guided prompt to a long-context large language model (LLM). On "Attention Is All You Need" [D6]: TechnicalMethod = "Transformer", Task = "machine translation", Dataset = "WMT 2014 English-German", EvaluationMetric = "BLEU".

proto2 was my sentence-level NLI attempt; proto3 reframes the task as document-level extraction. proto2 classified every sentence rather than extracting an answer, produced 151 TechnicalMethod sentences for MapReduce alone, and had no way to separate the authors' own method from cited prior work. Its recall-only evaluation (18/24 across six papers) only checked whether a gold term appeared somewhere in the output, not whether the output itself was correct.

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
*Figure 1: Extraction pipeline, five stages from PDF to structured JSON.*

References and Acknowledgements are removed by heading match; Stage 1 then joins the remaining section texts in order, with no sentence splitting and no per-sentence threshold.

Dataset and EvaluationMetric often occur in experimental sections rather than the Abstract or Method [Jain et al. 2020], so I retain the full document rather than an excerpt. The papers I use fit within the model's context window, so I send the full structured paper directly rather than introducing chunking or retrieval. I use Gemini (`gemini-3.5-flash`, via the `google-genai` software development kit).

The prompt names all four roles and states rules the JSON schema itself cannot express: use the authors' own method, not methods cited from prior work; return null for an absent role; quotes must be verbatim. The four-role JSON structure itself is enforced separately, by passing a JSON schema generated from the Pydantic models to Gemini's structured-output config — not by describing the shape in the prompt text. This is explained further in Section 5.

## 5. Code Explanation

The prompt template (`proto3/3pipeline.ipynb`, "Stage 2b — Prompt Template"):

```
Rules:
- Use the authors' own method, not methods cited from prior work.
- Return null when a role is not present in the paper.
- Evidence quotes must be copied verbatim from the paper, not paraphrased.
```
*Figure 2: Prompt rules excerpt from `proto3/3pipeline.ipynb` Stage 2b.*

The prompt no longer describes the output shape at all — `evidence` being a nested object with separate `section` and `quote` fields (needed for the checks in Section 7) is defined once, on the `Evidence` Pydantic model, and enforced through the schema below rather than repeated in prompt text.

The call and response parsing (`proto3/3pipeline.ipynb`, "Stage 2c — Call Gemini and Parse Response"):

```python
response = client.models.generate_content(
    model=MODEL_NAME,
    contents=prompt,
    config=types.GenerateContentConfig(
        temperature=0,
        seed=0,
        response_mime_type="application/json",
        response_json_schema=MethodologyProfile.model_json_schema(),
    ),
)

profile = MethodologyProfile.model_validate_json(response.text)
```
*Figure 3: Gemini call and response parsing from `proto3/3pipeline.ipynb` Stage 2c.*

`response_json_schema`, generated from the `MethodologyProfile` Pydantic model, constrains Gemini to return the required four-role shape; `MethodologyProfile.model_validate_json` then parses it directly, with no manual JSON extraction step. `temperature=0` and `seed=0` reduce (but do not guarantee) run-to-run variation.

An earlier prompt described `evidence` inconsistently, so Gemini returned the heading and quote as one string. At the time this was patched by making the prompt's nested shape explicit; today the nested shape is guaranteed by `response_json_schema` regardless of prompt wording, so this specific output-shape bug is now prevented by schema validation.

Code quality: `pyright` runs in `strict` mode and `ruff` lints and formats, but there are no automated tests yet for the JSON-parsing or evidence-validation logic.

## 6. Visual Representation / Demonstration

For "Attention Is All You Need" [D6], the full output is:

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
*Figure 4: Full extraction output for "Attention Is All You Need" [D6] (`proto3/baseline/transformer.json`).*

This output is from `proto3/baseline/transformer.json` (compared with proto2's output for the same paper in Section 2).

Figures 5–6 contrast proto2's sentence-count output with proto3's answer-and-evidence output:

![proto3 output](<./Screenshot 2026-07-19 180851.png>)
*Figure 5: proto3 Stage 2c cell and output (screenshot).*

![proto2 output](<./Screenshot 2026-07-18 195636.png>)
*Figure 6: proto2 output (screenshot).*

## 7. Evaluation and Improvement

Same six papers and gold labels as proto2, three axes:

*Table 1: Evaluation axes and implementation status.*

| Axis | Method | Status |
|---|---|---|
| 1. Gold label match | Each paper-role pair is classified as TP, FP, FN, or TN. A wrong non-null answer counts as both FP and FN. | Implemented |
| 2. Human precision | Is `answer` plausibly correct by human judgment | Not yet implemented |
| 3. Evidence check | Does `evidence.quote` support `answer`, is it about the paper's own work, does it appear verbatim, is `evidence.section` correct | Not yet implemented |

Initial testing identified and corrected a schema inconsistency (Section 5). I scored the frozen baseline (`proto3/baseline/*.json`) against gold across all six papers:

*Table 2: Baseline (frozen `proto3/baseline/*.json`) Precision/Recall/F1 vs. gold, all six papers.*

| Role | P | R | F1 |
|---|---|---|---|
| TechnicalMethod | 0.83 | 0.83 | 0.83 |
| Task | 0.33 | 0.33 | 0.33 |
| Dataset | 0.80 | 0.67 | 0.73 |
| EvaluationMetric | 0.80 | 0.67 | 0.73 |
| Overall | 0.68 | 0.62 | 0.65 |

I then ran the current pipeline twice across a kernel restart and compared these runs with the earlier frozen baseline, although the baseline was generated before the `temperature=0` and `seed=0` settings were added:

*Table 3: Baseline vs. two pipeline runs, F1 per role.*

| Role | Baseline F1 | Pipeline run 1 F1 | Pipeline run 2 F1 |
|---|---|---|---|
| TechnicalMethod | 0.83 | 0.83 | 0.83 |
| Task | 0.33 | 0.33 | 0.33 |
| Dataset | 0.73 | 0.80 | 0.91 |
| EvaluationMetric | 0.73 | 0.67 | 0.50 |
| Overall | 0.65 | 0.65 | 0.64 |

Findings:
- TechnicalMethod and Task have identical scores in the frozen baseline and both current pipeline runs. Task is the weakest role (F1=0.33), and its unchanged score in both current runs suggests a systematic weakness rather than run-to-run noise.
- Dataset and EvaluationMetric change between pipeline runs despite unchanged code, `temperature=0`, and `seed=0` — Gemini does not guarantee bit-for-bit reproducibility, so a single run's F1 for these two roles is one observation, not a stable score.

Next steps:
- Target Task with a prompt change, since it is the most stable weak point.
- Implement the human precision and evidence checks (axes 2-3).
- Run the pipeline several times to quantify the Dataset/EvaluationMetric variance rather than treat one run as final.
- Test whether including Related Work changes attribution errors.

## References

[Dagdelen et al. 2024] John Dagdelen, Alexander Dunn, Sanghoon Lee, Nicholas Walker, Andrew S. Rosen, Gerbrand Ceder, Kristin A. Persson, and Anubhav Jain. 2024. Structured information extraction from scientific text with large language models. *Nature Communications* 15 (2024), 1418. DOI: https://doi.org/10.1038/s41467-024-45563-x

[Jain et al. 2020] Sarthak Jain, Madeleine Van Zuylen, Hannaneh Hajishirzi, and Iz Beltagy. 2020. SciREX: A Challenge Dataset for Document-Level Information Extraction. In *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, Online, July 2020. Association for Computational Linguistics, 7506–7516. DOI: https://doi.org/10.18653/v1/2020.acl-main.670

[Polak and Morgan 2024] Maciej P. Polak and Dane Morgan. 2024. Extracting accurate materials data from research papers with conversational language models and prompt engineering. *Nature Communications* 15 (2024), 1569. DOI: https://doi.org/10.1038/s41467-024-45914-8

## Dataset Papers

The six papers used as the evaluation set (Figures 4, 7-11; Tables 4-5):

[D1] Sergey Brin and Lawrence Page. 1998. The anatomy of a large-scale hypertextual web search engine. *Computer Networks and ISDN Systems*, 30(1–7), 107–117. https://doi.org/10.1016/S0169-7552(98)00110-X

[D2] Jeffrey Dean and Sanjay Ghemawat. 2004. MapReduce: Simplified data processing on large clusters. In *Proceedings of the 6th Symposium on Operating Systems Design and Implementation (OSDI '04)*. USENIX Association, 137–150. https://www.usenix.org/conference/osdi-04/mapreduce-simplified-data-processing-large-clusters

[D3] Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. 2019. BERT: Pre-training of deep bidirectional transformers for language understanding. In *Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (NAACL-HLT 2019)*, Volume 1. Minneapolis, Minnesota: Association for Computational Linguistics, 4171–4186. https://doi.org/10.18653/v1/N19-1423

[D4] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. 2016. Deep residual learning for image recognition. In *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR 2016)*, 770–778. https://doi.org/10.1109/CVPR.2016.90

[D5] Alex Krizhevsky, Ilya Sutskever, and Geoffrey E. Hinton. 2012. ImageNet classification with deep convolutional neural networks. In *Advances in Neural Information Processing Systems*, 25, 1097–1105. https://proceedings.neurips.cc/paper_files/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html

[D6] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, and Illia Polosukhin. 2017. Attention is all you need. In *Advances in Neural Information Processing Systems*, 30, 5998–6008. https://proceedings.neurips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html

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
*Figure 7: Full extraction output for AlexNet [D5].*

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
*Figure 8: Full extraction output for BERT [D3].*

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
*Figure 9: Full extraction output for MapReduce [D2].*

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
*Figure 10: Full extraction output for Google Search (PageRank) [D1].*

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
*Figure 11: Full extraction output for ResNet [D4].*

### Gold labels (six papers)

*Table 4: Gold labels used for evaluation (six papers).*

| Paper | Gold TechnicalMethod | Gold Task | Gold Dataset | Gold EvaluationMetric |
|---|---|---|---|---|
| Transformer [D6] | "Transformer" | "machine translation" | "WMT" | "BLEU" |
| BERT [D3] | "BERT" | "GLUE" or "SQuAD" | "BooksCorpus" or "Wikipedia" | "F1" or "accuracy" |
| AlexNet [D5] | "convolutional" (paper predates the name "AlexNet") | "object recognition" | "ImageNet" | "top-1" or "top-5" |
| ResNet [D4] | "residual" | "image recognition" | "ImageNet" | "top-1" |
| MapReduce [D2] | "MapReduce" | "distributed" | "TeraSort" | "seconds" |
| Google Search [D1] | "PageRank" | "web search" | "million pages" | "quality" |

### proto2 background data

*Table 5: proto2 sentence-count output per role (six papers).*

| Paper | TM | Task | Dataset | EM | Hypothesis set |
|---|---|---|---|---|---|
| Transformer [D6] | 14 | 0 | 0 | 160 | verbose_v1 |
| BERT [D3] | 62 | 23 | 15 | 13 | short |
| AlexNet [D5] | 51 | 6 | 11 | 4 | short |
| ResNet [D4] | 51 | 6 | 14 | 12 | short |
| MapReduce [D2] | 151 | 24 | 3 | 5 | short |
| Google Search [D1] | 69 | 21 | 8 | 29 | short |

proto2 extended evaluation result (`report1/report.md` Appendix B): total 18/24 (75%) — ML papers 13/16 (81%), systems papers 5/8 (63%). Failures: ResNet ✗ Task, MapReduce ✗ Task + Dataset, Google Search ✗ TechnicalMethod ("PageRank" never appears in the TechnicalMethod output).
