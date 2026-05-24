> ScispaCy を使用して文を分割しました

1. What is it about?
2. What part of my project does it support?
3. What does it not solve?
4. How will I use it?
5. Useful terms / concepts:
6. One or two key quotes or page references:

## Points

1. **What problem does SciBERT solve?**
   Check why normal BERT may not be enough for scientific papers.

2. **Why is scientific text different?**
   Look for examples such as special terms, technical phrases, dataset names, model names, and metric names.

3. **What is SciBERT trained on?**
   Check that it uses a large corpus of scientific papers, including computer science and biomedical papers.

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
