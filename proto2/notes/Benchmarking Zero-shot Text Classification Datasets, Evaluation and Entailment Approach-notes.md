1. What problem does this paper solve, and what is the entailment approach in simple terms?
   (how does it turn a label like "sports" into something a model can reason about?)

2. My project classifies extracted terms into roles (Method, Task, Dataset, Metric). How is that similar to zero-shot classification?
   (does my system see labeled training examples for each role, or not?)

3. What does this paper use instead of training data for unseen labels?
   (what existing NLP task does it reuse, and why does that transfer work?)

4. What does this paper not address that my project still needs to handle?
   (think about the type of text — general news/emotions vs. scientific papers)

  ---
## Q1: Problems

  The paper says existing 0SHOT-TC research has 3 problems. What are they?

- modeled in a too restrictive vision

a single task, mainly topic categorization

- denotes labels as indices

without understanding neigher the aspect's specific interpretation nor the meaning of the labels.

- evaluated on different datasets and adoptsed different evaluation setups

which makes it hard to compare them fairly.

  ---
## Q2: Two definitions

  The paper gives two definitions of 0SHOT-TC.

  - Definition-Restrictive — what is it?

often a precondition that a part of classes are seen and their labeled instances are available to train a model

  - Definition-Wild — what is it?

f(.): X -> Y, where classifer f(.) never sees Y=specific labeled data in its model development

  What is the difference?

The same text may have different background. Based on topic, emotion, situation, ... aspect affect it's categorization.

Thinking:
So complete zero-shot is not easy. The easier way is training.
we don't need to have correct labels, but we need the label space, in my case, using computer area papers, then we will make latent space, then categorize papers...

  ---
## Q3: Datasets

  The paper prepares datasets for 3 aspects. What are they? Give one label example for each.

- topic categorization
- emotion detection
- situation frame detection

  ---
## Q4: Two evaluations

  - Label-partially-unseen — what does this mean?

corresponds to the Definition-Restrictive.
for the set of labels of a specific aspect, given traning data for a part of labels, predicting in the full label set.

  - Label-fully-unseen — what does this mean?

corresponds to the Definition-Wild.
the system is unaware of the upcoming aspects and can not access any labeled data for task-specific training.

  What does each one test?

  ---
## Q5: The main idea

  Why does the paper use textual entailment for text classification?

to imitate how humans decide the truth value of labels from any aspects.

  Example: for the label "sports", what is the hypothesis the model uses?

int the aspect-defined problem "the text is about ?" "?" = sports
"?" = an active diversion requiring physical exertion and competion

Thinking:
The main idea is making the hypothesis by themselves.

  ---
## Q6: Results — step by step

  Step 1: Look at the table in Section 6.1 (label-partially-unseen).

  For the topic task, compare Binary-BERT and MNLI (our entailment model):

  - Seen labels (s): which score is higher?
Binary-BERT

  - Unseen labels (u): which score is higher?
MNLI

  Step 2: Why does Binary-BERT perform well on seen labels but badly on unseen labels?

  Hint: Binary-BERT is trained on the seen labels. What happens when it sees a label it never trained on?

  Step 3: Why does the entailment model handle unseen labels better?

  Hint: The entailment model never learns label-specific parameters. It only asks "does this text entail this
  hypothesis?" — so it works the same way for any label, seen or unseen.

  Step 4: What is the trade-off?

  Complete this sentence:

"Binary-BERT is better at ___, but the entailment model is better at ___."

---
