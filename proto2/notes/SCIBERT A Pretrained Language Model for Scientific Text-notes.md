> ScispaCy を使用して文を分割しました

1. What is it about?
2. What part of my project does it support?
3. What does it not solve?
4. How will I use it?
5. Useful terms / concepts:
6. One or two key quotes or page references:

a pretrained language model based on BERT.

Beltagy, Lo and Cohan (2019) construct SCIVOCAB from a scientific corpus and report that "the resulting token overlap between BASEVOCAB and SCIVOCAB is 42%", showing a substantial vocabulary difference between scientific and general-domain text.

Scientific text is different from general text.
SciBERT improves scientific NLP compared with BERT.
But SciBERT does not solve my methodology-role classification.
So it is a useful comparison point, not the central method.

## Points

1. **What problem does SciBERT solve?**
   Scientific text is different from general text.

2. **Why is scientific text different?**
   "the resulting token overlap between BASEVOCAB and SCIVOCAB is 42%"

3. **What is SciBERT trained on?**
   "This corpus consists of 18% papers
from the computer science domain and 82% from
the broad biomedical domain.""

4. **What does “pretraining” mean here?**
   SciBERT learns scientific language patterns before it is used for a specific task.

5. **What downstream tasks are used?**
   Pay attention to:

   * sequence tagging
   * sentence classification
   * dependency parsing

6. **Which task is closest to my project?**
   Sentence classification is the closest, because my prototype also classifies whole sentences.

7. **Does SciBERT directly extract methodology?**
   No. Check this carefully. SciBERT is a language model, not a methodology extraction system.

8. **What would I need to use SciBERT for my project?**
   I would need labelled sentences, for example:

   * Method
   * Task
   * Dataset
   * Evaluation
   * Used
   * Mentioned

9. **Why is labelled data a problem?**
   Creating many correct labels takes time and human judgement.

10. **How is my project different?**
    My project uses zero-shot NLI because I do not have a labelled methodology dataset.

11. **What is SciBERT useful for in my literature review?**
    It shows that scientific papers need domain-aware NLP models.

12. **What should I not claim?**
    Do not say SciBERT extracts methodology.
    Say SciBERT could support a supervised version of this project.

sentence split に ScispaCy
