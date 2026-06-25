<style>
@page {
  size: A4;
  margin: 2.5cm;
}

html, body {
  font-size: 12pt;
  line-height: 1.45;
}

p, li, td, th, figcaption, blockquote {
  font-size: 12pt;
}

pre, code {
  font-size: 11pt;
  line-height: 1.35;
  white-space: pre-wrap;
}

h1 {
  font-size: 18pt;
}

h2 {
  font-size: 15pt;
}

h3 {
  font-size: 13pt;
}

table, figure, img {
  max-width: 100%;
}

* {
  box-sizing: border-box;
}
</style>

# Literature Review (1067 words)

## Introduction (117 words)

"Attention Is All You Need" is a very famous AI paper. But the title does not tell us how it works.

<pre>
Methodology:
    Design or strategy: design and creation + experiment
    Data generation method: documents
    Technical method: Transformer
    Task: machine translation
    Dataset: WMT machine translation datasets
    EvaluationMetric: BLEU score
</pre>

Figure 1: Research Methodology from "Attention Is All You Need".

Extracting research methodology from computing papers automatically is useful, but it remains challenging. When people read papers, they often identify the technical method, task, dataset, and evaluation metric by themselves. This process is slow and manual, especially when they must review many papers.
This review covers three areas: how methodology is defined, how information is extracted from papers, and how classification can work without training data. At the end, this review will identify a gap: existing methods can extract some information from papers, but reliably extracting full research methodology from computing papers is still difficult.

## Defining Research Methodology (271 words)

Research methodology in computing papers can be described using a structured vocabulary, but defining it is not the same as extracting it.

Oates [8] provides six research strategies (experiment, design and creation, survey, case study, action research, and ethnography) and four data generation methods (interviews, observations, questionnaires, and documents). His book defines the vocabulary that researchers use to describe their methodology in papers, so my project needs these concept names to identify what to extract. His book was published in 2006, but it still provides useful categories for describing how computing researchers conduct their work.

Pilkington & Pretorius [9] go further: they formalize the structure using UML and ontology engineering, with the goal of "providing clear and unambiguous semantics" [9] — a formal structure, not a textbook description. Key concepts are ResearchScheme, PhilosophicalWorldview, ResearchDesign, and ResearchMethod. ResearchScheme belongs to one PhilosophicalWorldview, has one or more ResearchDesigns, and has one or more ResearchMethods. The paper tries to solve the problem that students and supervisors had no shared, consistent vocabulary for methodology, so they often used the same terms with different meanings.

A philosophical worldview is one of the important parts of Pilkington & Pretorius [9], but it may not appear directly in paper text, so my project skips it.

Oates [8] gives concept names. Pilkington & Pretorius [9] give formal relationships between those concepts. My project uses vocabulary from Oates and formal structure from Pilkington & Pretorius.

Both works are designed for human use. Neither provides a system to extract methodology components automatically from text. These works suggest that methodology can be defined and formalized. The question is whether any system can extract it.


## Closest Prior Work (183 words)

Systems that extract methodology-like entities from papers exist, but the closest supervised approaches require labeled training data that this project does not have.

Jain et al. [4] extract four entity types: Dataset, Metric, Task, and Method.

Dataset: WMT machine translation datasets
Metric: BLEU score
Task: machine translation
Method: Transformer

Figure 2: Entity types from "Attention Is All You Need".

These four types closely match the four roles in this project. This suggests that the problem is real and may be solvable in principle.

Jain et al. [4] operate at the document level. The authors argue that "a significant amount of information can only be gleaned from analyzing the full document" [4] — relations may span sections, not just sentences.

But Jain et al. [4] required 438 annotated papers and 4 expert PhD-level annotators (Cohen-κ 95%). The corpus comes from Papers with Code, which covers only ML benchmarks. My project targets general computing papers (systems, algorithms, HCI, etc.) and has no annotated corpus. The Jain et al. [4] approach is difficult to adopt directly.

The right entity types are identified, but building a supervised system requires annotation effort that does not exist for this scope. A zero-shot method is therefore a reasonable direction.

## Zero-shot Classification (267 words)

Zero-shot NLI can assign roles to text without task-specific training data, but applying it to scientific papers introduces a domain mismatch risk.

Yin et al. [10] define zero-shot text classification as assigning a label to text without any task-specific training examples.

Yin et al. [10] show that NLI can classify text into many possible labels by turning the label into a natural language hypothesis — "this text is about [label]" [10] — and asking a model whether the text entails it. No labeled examples for the target labels are needed.

| aspect | labels | interpretation | example hypothesis (word) | example hypothesis (wordnet definition) |
|---|---|---|---|---|
| topic | sports etc. | this text is about ? | "?"= sports | "?" = an active diversion requiring physical exertion and competition |
| emotion | anger etc. | this text expresses ? | "?"= anger | "?" = a strong emotion; a feeling that is oriented toward some real or supposed grievance |
| situation | shelter etc. | The people there need ? | "?"= shelter | "?" = a structure that provides privacy and protection from danger |

*Table 1 (reproduced from Yin et al. [10]): example hypotheses for three task types.*

This provides a possible way to support the core step in this project: classifying sentences into TechnicalMethod, Task, Dataset, or EvaluationMetric without a methodology-annotated corpus. This project applies the same entailment approach with four methodology roles:

| role | hypothesis (this project, short label) |
|---|---|
| TechnicalMethod | technical_method |
| Task | task |
| Dataset | dataset |
| EvaluationMetric | evaluation_metric |

*Table 2: hypothesis set used in this project (short label format, selected by hypothesis set).*

For TechnicalMethod, a longer hypothesis was also tested: "This text describes a technique, algorithm, system, or architecture used or proposed in the research." The hypothesis set comparison investigates whether this verbose form can extract TechnicalMethod more accurately than the short label on scientific text.

However, a domain mismatch risk exists. Yin et al. test on Yahoo News articles, emotion tweets, and crisis situation reports. Their NLI model is trained on MNLI (news, fiction, telephone speech). None of these are scientific papers, which use dense technical vocabulary, passive constructions, and section-based structure.

This project accepts the risk and tests it: the hypothesis set comparison (short vs verbose hypotheses) directly investigates how label wording affects classification on scientific text.

Zero-shot NLI reduces the labeled data requirement. The question is whether any prior work combines this approach with a methodology schema on scientific papers.

## Synthesis (229 words)

It is difficult to find existing work that applies zero-shot NLI with a structured methodology schema to general computing papers. This is the gap this project addresses.

Section 2 established the schema. Oates [8] and Pilkington & Pretorius [9] together justify a four-component structure — TechnicalMethod, Task, Dataset, and EvaluationMetric — grounded in formal ontology. But both works are designed for human use. Neither provides a system to extract those components from text automatically.

Section 3 showed that extraction of the same four types is possible. Jain et al. [4] built a working system, but it required 438 annotated papers, 4 PhD-level annotators, and a corpus limited to ML benchmarks. This approach cannot generalize to general computing papers without similar annotation effort that this project does not have.

Section 4 showed that zero-shot NLI removes the labeled data requirement. Yin et al. [10] demonstrate that NLI can classify text into any label without task-specific training. But their approach was tested only on news articles, tweets, and crisis reports — not scientific papers. Domain mismatch remains an open risk.

Combining these elements appears to remain underexplored: the 4-role methodology schema from Oates and Pilkington, the zero-shot NLI method from Yin et al., and application to general computing papers. This project addresses that gap. It applies Yin et al.'s entailment approach with the 4-role schema on GROBID-parsed computing papers, without requiring annotated data.

## References

[4] Jain, S., van Zuylen, M., Hajishirzi, H., and Beltagy, I. 2020. SciREX: A Challenge Dataset for Document-Level Information Extraction. In *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, Online, July 2020. Association for Computational Linguistics, 7506–7516. DOI: https://doi.org/10.18653/v1/2020.acl-main.670

[8] B. J. Oates. 2006. *Researching Information Systems and Computing*. SAGE Publications, London.

[9] C. Pilkington and L. Pretorius. 2015. A conceptual model of the research methodology domain. In *Proceedings of the 7th International Joint Conference on Knowledge Discovery, Knowledge Engineering and Knowledge Management (IC3K 2015), Volume 2: KEOD*. SCITEPRESS – Science and Technology Publications, Setúbal, Portugal, 96–107. https://doi.org/10.5220/0005613100960107

[10] Yin, W., Hay, J., and Roth, D. 2019. Benchmarking Zero-shot Text Classification: Datasets, Evaluation and Entailment Approach. In *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)*, Hong Kong, China, November 2019. Association for Computational Linguistics, 3914–3923. DOI: https://doi.org/10.18653/v1/D19-1404
