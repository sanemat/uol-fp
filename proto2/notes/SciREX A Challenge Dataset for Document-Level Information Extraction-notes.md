1. What are the four entity types in SciREX? How do they match the four roles in my project?

Dataset
Metric
Task
Method

2. Why does SciREX say sentence-level IE is not enough? Can I show this with a number from the paper?
3. What ground truth did SciREX use for annotation?

a comprehensive list of imfirmation extraction tasks "from scratch", where the input is the raw document.

4. What is the technical stack of the SciREX model? How is my approach different?
5. Does SciREX connect to a methodology framework like Pilkington or Oates? If not, what is missing?
6. If I add SciREX to my previous work table, what do I write for "What it does" and "What is still missing"?

> SciRex, a document level IE dataset that encompasses multiple IE tasks, including salient entity identification and document level N-ary relation identification from scientific articles.

SciERC (Luan et al., 2018)


  ---
  Q1: The problem

  Most previous IE (information extraction) research worked on sentences or short paragraphs. Why is that not
  enough for scientific papers?

  Give one example from the paper.

  ---
  Q2: The 4 entity types

  SCIREX annotates 4 types of entities. What are they?

  Write an example for each type using this sentence:

  ▎ "We evaluate BiDAF on SQuAD using Exact Match."

  ---
  Q3: What is "saliency"?

  Not all entities in a paper are equally important. What does salient mean in this paper?

  Example: Is a dataset mentioned only in the Related Work section salient? Why or why not?

  ---
  Q4: Dataset construction — 3 steps

  The authors built SCIREX using 3 steps. What are they?

  Hint: automatic → noisy labels → human fixes

  ---
  Q5: The model pipeline

  The model does 5 things in order. Can you put these in the right order?

  - Relation extraction
  - Mention identification
  - Salient entity cluster identification
  - Coreference resolution
  - Salient mention classification

  ---
  Q6: The biggest problem

  The paper says one subtask is the hardest bottleneck in the model. Which one? Why does the model struggle
  with it?

  ---
  Q7: Connection to your project

  Your project extracts Design, Method, Data, Evaluation from research papers. How is SCIREX similar to your
  goal? What is different?

  ---
