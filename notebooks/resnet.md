Based on the provided research paper, here is the extracted methodology:

### **TechnicalMethod**
*   **Answer:** The authors propose a **deep residual learning framework**, realized through **residual networks (ResNets)** that utilize identity shortcut connections to learn residual functions.
*   **Evidence:** "We present a residual learning framework to ease the training of networks that are substantially deeper than those used previously. We explicitly reformulate the layers as learning residual functions with reference to the layer inputs, instead of learning unreferenced functions."

### **Task**
*   **Answer:** The primary task is addressing the **degradation problem** in **deep neural network training**, where increasing depth leads to higher training error and saturated accuracy. The framework is applied to various **image recognition** tasks including image classification, object detection, localization, and segmentation.
*   **Evidence:** "When deeper networks are able to start converging, a degradation problem has been exposed: with the network depth increasing, accuracy gets saturated (which might be unsurprising) and then degrades rapidly."

### **Dataset**
*   **Answer:** The authors evaluate their method using the **ImageNet 2012** classification dataset, the **CIFAR-10** dataset, **PASCAL VOC 2007/2012**, and **MS COCO**.
*   **Evidence:** "On the ImageNet dataset we evaluate residual nets with a depth of up to 152 layers... We also present analysis on CIFAR-10 with 100 and 1000 layers."
*   **Evidence:** "Table 7 and 8 show the object detection baseline results on PASCAL VOC 2007 and 2012 and COCO."

### **EvaluationMetric**
*   **Answer:** The results are reported using **top-1 error rate**, **top-5 error rate**, and **mean Average Precision (mAP)**.
*   **Evidence:** "We evaluate both top-1 and top-5 error rates."
*   **Evidence:** "Most remarkably, on the challenging COCO dataset we obtain a 6.0% increase in COCO’s standard metric (mAP@[.5, .95]), which is a 28% relative improvement."
