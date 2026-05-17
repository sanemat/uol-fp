CSO Classfier v3.0

input
タイトル、要約、キーワード
output
CSOから抽出した研究トピックの選択肢

入力テキストに明示的に記載されているオントロジー内のすべてのトピックを検索
品詞タグ付けとワールド埋め込みを利用して、意味的に関連するトピックをさらに特定
外れ値を除去し、CSO分類法を活用して上位領域を含めることで、このトピックセットを充実させる

pip install cso-classifier

https://github.com/angelosalatino/cso-classifier
http://w3id.org/cso/cso-classifier

トピックモデリング
教師あり機械学習アプローチ
引用ネットワークに基づくアプローチ
自然言語処理に基づくアプローチ

トピックモデリング
潜在ディリクレ分析

各文書をトピックの混合としてモデル化

教師あり機械学習アプローチ

引用ネットワークに基づくアプローチ
共引用分析によって科学文書をクラスタリングする原理

自然言語処理に基づくアプローチ

generate the topics from scratch
vs
exploit a domain vocabulary or ontology

generate methodology labels from scratch
vs
extract components using a predefined MethodologyProfile schema

A fixed ontology or controlled vocabulary improves interpretability, but it may fail to cover new terms and emerging methods.

For my project, I should not use a fully closed vocabulary. Instead, I can use a controlled schema with open values. The component types are predefined, such as ResearchDesign, TechnicalMethod, Dataset, Task, and EvaluationMetric. However, the actual extracted values can include new models, datasets, tasks, or metrics.

This gives a hybrid approach: ontology-guided structure with open candidate discovery.

1. What is it about?
2. What part of my project does it support?
3. What does it not solve?
4. How will I use it?
5. Useful terms / concepts:
6. One or two key quotes or page references:

- What does CSO represent?
- What is the input of the CSO Classifier?
- What is the output of the CSO Classifier?
- How can CSO help with field or topic mapping?
- Can CSO represent methodology components?
- Can I use CSO as a mapping target, not as the whole classification system?
- What does CSO not solve for my project?
