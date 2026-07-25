Based on the provided research paper, here is the extracted research methodology:

### **TechnicalMethod**
*   **Answer:** The **Transformer**.
*   **Evidence:** "In this work we propose the **Transformer**, a model architecture eschewing recurrence and instead relying entirely on an **attention mechanism** to draw global dependencies between input and output."

### **Task**
*   **Answer:** **Sequence transduction**, specifically machine translation and English constituency parsing.
*   **Evidence:** "The dominant **sequence transduction** models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder." "Experiments on two **machine translation** tasks show these models to be superior in quality..." "To evaluate if the Transformer can generalize to other tasks we performed experiments on **English constituency parsing**."

### **Dataset**
*   **Answer:** **WMT 2014 English-German** dataset, **WMT 2014 English-French** dataset, and the **Wall Street Journal (WSJ)** portion of the **Penn Treebank**.
*   **Evidence:** "We trained on the standard **WMT 2014 English-German** dataset consisting of about 4.5 million sentence pairs." "For English-French, we used the significantly larger **WMT 2014 English-French** dataset consisting of 36M sentences..." "We trained a 4-layer transformer with dmodel = 1024 on the **Wall Street Journal (WSJ) portion of the Penn Treebank**, about 40K training sentences."

### **EvaluationMetric**
*   **Answer:** **BLEU** score (for translation) and **F1** (for parsing).
*   **Evidence:** "Our model achieves 28.4 **BLEU** on the WMT 2014 English-to-German translation task..." "On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art **BLEU** score of 41.8..." "Table 4: The Transformer generalizes well to English constituency parsing (Results are on Section 23 of WSJ) ... **WSJ 23 F1**"
