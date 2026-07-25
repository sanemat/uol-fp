# Manual review (P0 item 3)

24-slot consolidated pass: 6 papers x 4 roles, one read per paper. Reviews the
frozen baseline sample (`proto3/baseline/*.json`) — the same sample Q19's
gold-label-match table is computed from.

Source PDFs (gitignored, present locally): `proto1/dataset/`.

## How to judge each slot

Four checks per slot, all from the same read of the source PDF — don't build
separate tooling for any of these (see `proto3/memo.md` "Evaluation plan").

1. **Plausible?** Does the answer look like a real, sensible value for this role,
   independent of the evidence quote — i.e. if you only saw the answer string,
   would it make sense as this paper's TechnicalMethod/Task/Dataset/EvaluationMetric?
2. **Evidence supports answer?** Does the quoted sentence(s) actually establish the
   answer, not just mention a related term? A quote can be real and still not
   support the specific answer given.
3. **Authors' own work, not prior work?** Is the answer something *this paper*
   contributes, not a method/dataset/metric it only cites from someone else's
   prior work? (This is the check proto2's ELMo/BERT mix-up failed — see
   `proto2/memo.md`.)
4. **Quote appears verbatim in source?** Search the PDF text for the exact quote.
   Necessary but **not sufficient** — a real quote can still be the *wrong*
   evidence (e.g. a genuine Related Work sentence cited as if it were the paper's
   own method). Flag that case separately from "quote fabricated."

**Null slots (Pagerank/EvaluationMetric, MapReduce/Dataset):** there's no answer
to plausibility-check, so instead judge: is the role genuinely absent from the
paper, or is this a missed extraction? Both of these two nulls already have a
cross-check pointing at "missed extraction" — see the note under each below.
Record your own independent read; don't just defer to the cross-check.

**Bias note to carry into Q21's write-up:** this pass has the same
single-annotator bias as the gold labels themselves (same person, one read) —
say so once in the report, don't present this review as more objective than the
gold labels it's checking against.

**Optional aid, not a substitute for reading the source:** `notebooks/<paper>.md`
has an independent NotebookLM extraction for the same paper. Useful as a second
opinion on plausibility while you read, but the quote-in-source check must be done
against the actual PDF — NotebookLM's citations are not verified here.

---

## Pagerank (`proto1/dataset/pagerank_The anatomy of a large-scale hypertextual Web search engine.pdf`)

Gold: TechnicalMethod=`PageRank`, Task=`web search`, Dataset=`million pages`, EvaluationMetric=`quality`

| Role | Answer | Section | Quote | Plausible? | Evidence supports? | Authors' own? | Quote in source? | Notes |
|---|---|---|---|---|---|---|---|---|
| TechnicalMethod | Google | Abstract | "In this paper, we present Google, a prototype of a large-scale search engine which makes heavy use of the structure present in hypertext." | | | | | |
| Task | information retrieval | Introduction | "The Web creates new challenges for information retrieval." | | | | | |
| Dataset | 24 million pages | Anchor-test | "In our current crawl of 24 million pages. we had over 259 million anchors which we indexed." | | | | | |
| EvaluationMetric | *(null)* | — | — | | | | | See "Null slots" above — real runs answer `"precision"` every time (5/5), and NotebookLM independently names Precision too. Judge whether this is a real miss. |

## AlexNet (`proto1/dataset/alexnet_NIPS-2012-imagenet-classification-with-deep-convolutional-neural-networks-Paper.pdf`)

Gold: TechnicalMethod=`convolutional`, Task=`object recognition`, Dataset=`ImageNet`, EvaluationMetric=`top-5`

| Role | Answer | Section | Quote | Plausible? | Evidence supports? | Authors' own? | Quote in source? | Notes |
|---|---|---|---|---|---|---|---|---|
| TechnicalMethod | deep convolutional neural network | Abstract | "We trained a large, deep convolutional neural network to classify the 1.2 million high-resolution images in the ImageNet LSVRC-2010 contest into the 1000 different classes." | | | | | |
| Task | object recognition | Introduction | "Current approaches to object recognition make essential use of machine learning methods." | | | | | |
| Dataset | ImageNet | The Dataset | "ImageNet is a dataset of over 15 million labeled high-resolution images belonging to roughly 22,000 categories." | | | | | |
| EvaluationMetric | top-1 and top-5 error rates | The Dataset | "On ImageNet, it is customary to report two error rates: top-1 and top-5, where the top-5 error rate is the fraction of test images for which the correct label is not among the five labels considered most probable by the model." | | | | | |

## BERT (`proto1/dataset/BERT Pre-training of Deep Bidirectional Transformers for Language Understanding.pdf`)

Gold: TechnicalMethod=`BERT`, Task=`GLUE`, Dataset=`BooksCorpus`, EvaluationMetric=`F1`

| Role | Answer | Section | Quote | Plausible? | Evidence supports? | Authors' own? | Quote in source? | Notes |
|---|---|---|---|---|---|---|---|---|
| TechnicalMethod | BERT | Abstract | "We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers." | | | | | |
| Task | Language model pre-training | Introduction | "Language model pre-training has been shown to be effective for improving many natural language processing tasks (Dai and Le, 2015; Peters et al., 2018a; Radford et al., 2018; Howard and Ruder, 2018)." | | | | | Watch this one for "authors' own work" — the quote cites prior work by name. Is pre-training itself BERT's contribution, or just motivation? |
| Dataset | SQuAD v1.1 | SQuAD v1.1 | "The Stanford Question Answering Dataset (SQuAD v1.1) is a collection of 100k crowdsourced question/answer pairs (Rajpurkar et al., 2016)." | | | | | Answer is one of several valid datasets (see Q9 multi-valued discussion) — judge plausibility as "a correct dataset," not "the only one." |
| EvaluationMetric | F1 score | SQuAD v1.1 | "Our single BERT model outperforms the top ensemble system in terms of F1 score." | | | | | Same multi-valued caveat as Dataset above. |

## MapReduce (`proto1/dataset/MapReduce Simplified Data Processing on Large Clusters.pdf`)

Gold: TechnicalMethod=`MapReduce`, Task=`distributed`, Dataset=`TeraSort`, EvaluationMetric=`seconds`

| Role | Answer | Section | Quote | Plausible? | Evidence supports? | Authors' own? | Quote in source? | Notes |
|---|---|---|---|---|---|---|---|---|
| TechnicalMethod | MapReduce | Abstract | "MapReduce is a programming model and an associated implementation for processing and generating large data sets." | | | | | |
| Task | automatic parallelization and distribution of large-scale computations | Introduction | "The major contributions of this work are a simple and powerful interface that enables automatic parallelization and distribution of large-scale computations, combined with an implementation of this interface that achieves high performance on large clusters of commodity PCs." | | | | | Already known: fails substring match against gold `"distributed"` despite being arguably correct — the "metric is blunt" example already slated for Q20. |
| Dataset | *(null)* | — | — | | | | | See "Null slots" above — null in the baseline **and all 5 real runs**, but NotebookLM independently found "two ~1TB datasets (grep, sort benchmarks)" in the text. Judge whether this is a real miss. |
| EvaluationMetric | elapsed time | Effect of Backup Tasks | "The entire computation takes 1283 seconds, an increase of 44% in elapsed time." | | | | | |

## ResNet (`proto1/dataset/resnet_Deep_Residual_Learning_for_Image_Recognition.pdf`)

Gold: TechnicalMethod=`residual`, Task=`image recognition`, Dataset=`ImageNet`, EvaluationMetric=`top-1`

| Role | Answer | Section | Quote | Plausible? | Evidence supports? | Authors' own? | Quote in source? | Notes |
|---|---|---|---|---|---|---|---|---|
| TechnicalMethod | deep residual learning framework | Introduction | "In this paper, we address the degradation problem by introducing a deep residual learning framework." | | | | | |
| Task | image classification | Introduction | "Deep convolutional neural networks [22, 21] have led to a series of breakthroughs for image classification [21, 49, 39]." | | | | | Quote cites bracketed prior work `[21, 49, 39]` for the breakthroughs — check whether the sentence is establishing the paper's own task or crediting others'. |
| Dataset | ImageNet 2012 classification dataset | ImageNet Classification | "We evaluate our method on the ImageNet 2012 classification dataset [35] that consists of 1000 classes." | | | | | Multi-valued caveat, as BERT above (CIFAR-10/PASCAL VOC/COCO also used). |
| EvaluationMetric | top-1 and top-5 error rates | ImageNet Classification | "We evaluate both top-1 and top-5 error rates." | | | | | |

## Transformer (`proto1/dataset/Attention Is All You Need.pdf`)

Gold: TechnicalMethod=`Transformer`, Task=`machine translation`, Dataset=`WMT`, EvaluationMetric=`BLEU`

| Role | Answer | Section | Quote | Plausible? | Evidence supports? | Authors' own? | Quote in source? | Notes |
|---|---|---|---|---|---|---|---|---|
| TechnicalMethod | Transformer | Abstract | "We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely." | | | | | |
| Task | machine translation | Abstract | "Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train." | | | | | |
| Dataset | WMT 2014 English-German | Training Data and Batching | "We trained on the standard WMT 2014 English-German dataset consisting of about 4.5 million sentence pairs." | | | | | Multi-valued caveat, as BERT/ResNet above (also WMT En-Fr, WSJ Penn Treebank). |
| EvaluationMetric | BLEU | Machine Translation | "On the WMT 2014 English-to-German translation task, the big transformer model (Transformer (big) in Table 2) outperforms the best previously reported models (including ensembles) by more than 2.0 BLEU, establishing a new state-of-the-art BLEU score of 28.4." | | | | | |

---

## After finishing all 24 slots

Roll the results up for Q21 in `report3/report-memo.md`:
- Count of failures per check type (plausibility / support / authorship / quote-in-source), not just a pass/fail total — the requirement doc rewards *which* checks fail, not just how many.
- Any case where quote-in-source passed but evidence-supports or authors'-own-work failed — call these out explicitly (Q21's hint already asks for this).
- Resolution on the two null slots: real miss or genuine absence.
- One line on the single-annotator bias, per the note above.
