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

## Defining Research Methodology

Research methodology in computer paper has a well-defined structure, but defining it is not the same as extracting it.

Oates [1] provides six research strategies (experiment, design and creation, survey, case study, action research, and ethnograpy) and four data generation methods (interviews, ovservations, questionnaires, and documents). His book defines the vocabulary that researchers use to describe their methodology in papers, so my project need these concept names to identify what to extract. His book was publshed in 2006, but still describe how researchers conduct their work now, it includes computing researchers.

Pilkington & Pretorius [2] formalizes structure using UML. Key concept are ResearchScheme, PhilosophicalWorldview, ResearchDesign, and ResearchMethod. ResearchScheme belongs to a one PhilosophicalWorldview and has one ore more ResearchDesigns, and has one ore more ResearchMethod. The paper tries to solve the problem that students and supoervisors had no shared, consistent vocabulary for methodology, so they often used the same terms with different meanings.

Oates [1] gives concept names. Pilkington & Pretorius [2] gives formal relationships between those concepts. My project use vocabulary from Oates, formal structure from Pilkington & Pretorius.

Both works are designed for human use. Neither provides a system to extract methodology components automatically from text. The next step is whether any system can extract it.

## Closest Prior Work

## Zero-shot Classification

| aspect | labels | interpretation | example hypothesis (word) | example hypothesis (wordnet definition) |
|---|---|---|---|---|
| topic | sports etc. | this text is about ? | "?"= sports | "?" = an active diversion requiring physical exertion and competition |
| emotion | anger etc. | this text expresses ? | "?"= anger | "?" = a strong emotion; a feeling that is oriented toward some real or supposed grievance |
| situation | shelter etc. | The people there need ? | "?"= shelter | "?" = a structure that provides privacy and protection from danger |

*Table 1 (reproduced from Yin et al. [4]): example hypotheses for three task types.*

- This directly enables the core step in this project: classifying sentences into TechnicalMethod, Task, Dataset, or EvaluationMetric without a methodology-annotated corpus. This project applies the same entailment approach with four methodology roles:

| role | hypothesis (this project, short label) |
|---|---|
| TechnicalMethod | technical_method |
| Task | task |
| Dataset | dataset |
| EvaluationMetric | evaluation_metric |

*Table 2: hypothesis set used in this project (short label format, selected by hypothesis set).*

## Synthesis

## References

[1] B. J. Oates. 2006. *Researching Information Systems and Computing*. SAGE Publications, London.

[2] C. Pilkington and L. Pretorius. 2015. A conceptual model of the research methodology domain. In *Proceedings of the 7th International Joint Conference on Knowledge Discovery, Knowledge Engineering and Knowledge Management (IC3K 2015), Volume 2: KEOD*. SCITEPRESS – Science and Technology Publications, Setúbal, Portugal, 96–107. https://doi.org/10.5220/0005613100960107

[3] Jain, S., van Zuylen, M., Hajishirzi, H., and Beltagy, I. 2020. SciREX: A Challenge Dataset for Document-Level Information Extraction. In *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, Online, July 2020. Association for Computational Linguistics, 7506–7516. DOI: https://doi.org/10.18653/v1/2020.acl-main.670

[4] Yin, W., Hay, J., and Roth, D. 2019. Benchmarking Zero-shot Text Classification: Datasets, Evaluation and Entailment Approach. In *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)*, Hong Kong, China, November 2019. Association for Computational Linguistics, 3914–3923. DOI: https://doi.org/10.18653/v1/D19-1404
