Based on the provided research paper, here is the extraction of the research methodology:

**TechnicalMethod**
*   **Answer:** **MapReduce**, a programming model and implementation for processing large-scale data on clusters.
*   **Supporting Evidence:** "MapReduce is a programming model and an associated implementation for processing and generating large data sets." "The major contributions of this work are a simple and powerful interface that enables automatic parallelization and distribution of large-scale computations, combined with an implementation of this interface that achieves high performance on large clusters of commodity PCs."

**Task**
*   **Answer:** Simplifying the **processing of large amounts of raw data** by hiding the complexities of **parallelization, fault-tolerance, and data distribution**.
*   **Supporting Evidence:** "The issues of how to parallelize the computation, distribute the data, and handle failures conspire to obscure the original simple computation with large amounts of complex code to deal with these issues." "As a reaction to this complexity, we designed a new abstraction that allows us to express the simple computations we were trying to perform but hides the messy details of parallelization, fault-tolerance, data distribution and load balancing in a library."

**Dataset**
*   **Answer:** Two datasets each consisting of approximately **one terabyte of data** ($10^{10}$ 100-byte records).
*   **Supporting Evidence:** "One computation searches through approximately one terabyte of data looking for a particular pattern. The other computation sorts approximately one terabyte of data." "The grep program scans through $10^{10}$ 100-byte records, searching for a relatively rare three-character pattern..." "The sort program sorts $10^{10}$ 100-byte records (approximately 1 terabyte of data)."

**EvaluationMetric**
*   **Answer:** **Data transfer rate** (throughput) and **total elapsed time** for computation.
*   **Supporting Evidence:** "The Y-axis shows the rate at which the input data is scanned." "The entire computation takes approximately 150 seconds from start to finish." "Including startup overhead, the entire computation takes 891 seconds."
