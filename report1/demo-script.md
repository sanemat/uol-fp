# Demo Script — Auto-Extracting Research Methodology from Papers

Total: about 2 minutes 40 seconds

## [0:00–0:20] Introduction and motivation

Today, I will demonstrate my prototype.

This prototype automatically extracts research methodology from computing papers.

By research methodology, I mean four things:
the technical method, the task, the dataset, and the evaluation metric.

Normally, a researcher has to read the paper and find these manually.
This can take time, especially when reviewing many papers.
My prototype aims to support this process automatically.

## [0:20–0:30] Input: BERT paper

Here is the input.

This is the BERT paper by Devlin and colleagues, published in 2019.

## [0:30–0:40] XML output from GROBID

Before using the prototype, the PDF is converted into TEI XML using GROBID.

GROBID keeps useful document structure, such as section headings.
This is important because the pipeline uses section information later.

## [0:40–0:50] Colab setup

Now I will switch to Google Colab.

The package installation and model download have already been run before recording, because they take some time.

The remaining cells will be run live.

## [0:50–1:05] Load XML

First, I upload the XML file.

The pipeline loads the paper sections and skips sections that are not useful for methodology extraction, such as References, Acknowledgements, and Related Work.

For the BERT paper, it loads twenty-three body sections.

## [1:05–1:15] Sentence splitting

Next, the text is cleaned and split into sentences.

Citation markers are removed, and very short or invalid fragments are filtered out.

After this step, the BERT paper has 258 valid sentences.

## [1:15–1:40] Zero-shot classification

Now the prototype classifies the sentences.

It uses zero-shot Natural Language Inference, or NLI.

Each sentence is classified into one of four roles:
TechnicalMethod, Task, Dataset, or EvaluationMetric.

The important point is that this does not require labeled training data for this project.

With a GPU, all 258 sentences are classified in a few seconds.

## [1:40–1:50] Results summary

Here is the results summary.

For each role, the output shows the number of accepted sentences and an example sentence.

For the BERT paper, all four methodology roles appear in the output.

## [1:50–2:20] Results across papers

I also tested the prototype on six computing papers.

For machine learning papers such as BERT, AlexNet, and ResNet, the prototype found all four expected gold labels in the output.

However, the results were weaker for systems papers such as MapReduce and Google Search.

In those papers, TechnicalMethod dominated the output, sometimes with more than 150 sentences.

At the same time, Dataset and EvaluationMetric were much less clear, because these papers do not always follow the standard machine learning benchmark structure.

## [2:20–2:40] Summary

To summarise, the prototype shows that zero-shot NLI can find relevant methodology sentences in machine learning papers without labeled training data.

However, there are still two main challenges.

First, the output can be too large.

Second, systems papers are harder to handle than standard machine learning papers.

Thank you.
