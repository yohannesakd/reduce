# More Code, Less Reuse: Investigating Code Quality and Reviewer Sentiment towards AI-generated Pull Requests

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: Haoming Huang, Pongchai Jaisri, Shota Shimizu, Lingfeng Chen, Sota Nakashima, Gema Rodríguez-Pérez
- Date: 2026-01-29
- Original location: https://arxiv.org/abs/2601.21276v1
- Copied: 2026-11-20, from the arXiv HTML full text, converted to Markdown with trafilatura

## Text
# More Code, Less Reuse: Investigating Code Quality and Reviewer Sentiment towards AI-generated Pull Requests

###### Abstract.

Large Language Model (LLM) Agents are advancing quickly, with the increasing leveraging of LLM Agents to assist in development tasks such as code generation. While LLM Agents accelerate code generation, studies indicate they may introduce adverse effects on development. However, existing metrics solely measure pass rates, failing to reflect impacts on long-term maintainability and readability, and failing to capture human intuitive evaluations of PR. To increase the comprehensiveness of this problem, we investigate and evaluate the characteristics of LLM to know the pull requests’ characteristics beyond the pass rate. We observe the code quality and maintainability within PRs based on code metrics to evaluate objective characteristics and developers’ reactions to the pull requests from both humans and LLM’s generation. Evaluation results indicate that LLM Agents frequently disregard code reuse opportunities, resulting in higher levels of redundancy compared to human developers. In contrast to the quality issues, our emotions analysis reveals that reviewers tend to express more neutral or positive emotions towards AI-generated contributions than human ones. This disconnect suggests that the surface-level plausibility of AI code masks redundancy, leading to the silent accumulation of technical debt in real-world development environments. Our research provides insights for improving human-AI collaboration.

###### Keywords:

Large Language Models, Agents, Code Quality, Code Clone, Code Generation, Reviewer Sentiment
<sup>†</sup>

<sup>†</sup>cc-license: by

## 1. Introduction

The software engineering (SE) landscape is undergoing a paradigm shift towards SE 3.0, where Large Language Model (LLM) agents are evolving from passive assistants to autonomous teammates ([Li et al., 2025](#bib.bib6)).
The AIDev dataset ([Li et al., 2025](#bib.bib6)) captures the emergence of pull requests (PRs) submitted autonomously by AI Agents (Agentic-PRs).
While LLM Agents accelerate code generation, researches ([Becker et al., 2025](#bib.bib1); [Perry et al., 2023](#bib.bib21)) indicate they may introduce adverse effects on development. Existing benchmark (like SWE-Bench ([Jimenez et al., 2023](#bib.bib3))) solely measure pass rates, failing to reflect impacts on long-term maintainability and readability. While code redundancy or code clone is a well-known issue in SE ([Roy and Cordy, 2007](#bib.bib8)), evaluating it in the context of AI agents remains unexplored.

A concern with AI-generated code is code clone ([Fowler, 2018](#bib.bib2)), a.k.a code redundancy. In SE, code redundancy is a known bad smell that increases maintenance effort ([Fowler, 2018](#bib.bib2)).
Due to LLM’s probabilistic model-based nature ([Bengio et al., 2003](#bib.bib15); [Shumailov et al., 2024a](#bib.bib16)), we believe generative AI models tend to produce Type-4 semantic clones ([Roy and Cordy, 2007](#bib.bib8); [Shumailov et al., 2024b](#bib.bib24)), unlike human developers who often copy and paste code (creating Type-1 or Type-2 clones ([Juergens et al., 2009](#bib.bib4))).
These clones implement the same logic as existing functions but use different syntax or variable names. This behavior violates the SE principle of reuse.
However, existing tools are not effective at detecting these Type-4 semantic clones (see [section 5](#S5)).

To address this problem, we propose a comprehensive evaluation framework. We assess Agentic-PRs from two perspectives: internal code quality and external reviewer perception. For internal code quality, we measure traditional metrics including Lines of Code (LOC) and Cyclomatic Complexity ([McCabe, 1976](#bib.bib7)). Furthermore, we propose a new metric called the Max Redundancy Score (MRS) to measure semantic redundancy. We use code emebdding model to build an approach, to detect Type-4 semantic clones. For external reviewer perception, we investigate how human reviewers react to Agentic-PRs. We conduct a sentiment analysis on review comments to see if reviewers identify the quality issues in AI-generated code.

We analyze the AIDev dataset ([Li et al., 2025](#bib.bib6)) to answer the following:

- • 
RQ1: How do AI-generated code differ from human-generated code in terms of code quality?
- • 
RQ2: How does reviewer sentiment differ between AI-generated and human-written PRs

This study provides the first empirical evidence of the disconnect between AI-generated code redundancy and human reviewer sentiment. By highlighting the risk of silent technical debt, we offer insights for improving human-AI collaboration.

## 2. Methodology

### 2.1. Dataset

We utilize the AIDev dataset ([Li et al., 2025](#bib.bib6)) for our empirical study. To ensure the analysis focuses on mature projects, we filter the dataset to include only Python repositories with more than 500 stars, following the popularity standard mentioned in AIDev ([Li et al., 2025](#bib.bib6)).
We separate the data into human-generated PRs (Human-PRs) and agent-generated PRs (Agentic-PRs).
To balance the depth of semantic analysis with computational feasibility, we employ a two-level data strategy:

- • 
Dataset A (Full Python Dataset): This dataset comprises 3,858 PRs across all filtered Python repositories. We use this broad dataset to analyze traditional code metrics (RQ1) and reviewer sentiment (RQ2).
- • 
Dataset B (Core Case Study): This dataset consists of 617 PRs from the crewAI repository, the repository with the most PRs in AIDev. As the most active repository in AIDev with high agent activity, it serves as a representative case for our computationally intensive redundancy analysis (RQ1).

### 2.2. RQ1: How do AI-generated code differ from human-generated code in terms of code quality?

This question compares the code quality between handcraft changes and AI-generated changes. We employ a multi-dimensional evaluation strategy including both traditional static metrics and a novel code redundancy analysis.

As shown in [Figure 1](#S2.F1), We extracted pairs of source files representing the pre- and post-update states by identifying the modified files in each PR relative to their parent commits.

#### 2.2.1. Traditional Metrics

We calculated Cyclomatic Complexity (CC) and raw metrics (LOC, multi-lines-string, blank lines) using Radon<sup>1</sup><sup>1</sup>
                1
                
                
                
              [https://pypi.org/project/radon/](https://pypi.org/project/radon/) for each file pair to compare human and AI contributions.

#### 2.2.2. Redundancy Score

Due to the probabilistic nature of LLM models ([Shumailov et al., 2024a](#bib.bib16); [Bengio et al., 2003](#bib.bib15)), they are more prone to generating Type-4 Clones, which reduce software maintainability. While LLMs can also produce Type-1 and Type-2 clones, existing tools that rely on literal keyword matching remain ineffective at identifying the more prevalent Type-4 Clones.

To bridge this gap, we introduce a Snapshot-based Semantic Differential Analysis pipeline.
We extract all existing functions from the snapshot ($F_{base}$) and generate semantic embeddings using CodeSage-Large ([Zhang et al., 2024](#bib.bib10)), a model optimized for code representation.
This allows us to capture functional equivalence beyond syntactic similarity.
A naive comparison of added code yields false positives, as moving or renaming a function appears as an addition in Git diffs.
To isolate true redundancy, we integrate PyRef ([Atwi et al., 2021](#bib.bib12)), a refactoring detection tool, to identify and exclude Move Method and Rename Method instances from the set of new functions ($F_{new}$).
We define the redundancy of a PR not by its average similarity, but by its worst offender.
In maintenance, a single instance of severe duplication (e.g., rewriting a complex core utility) creates a single point of failure for future updates ([Juergens et al., 2009](#bib.bib4)).
Thus, we calculate the Max Redundancy Score (MRS) by [Equation 1](#S2.E1);

| (1) |  | $$ \text{MRS}(P_{i})=\max_{f\in F_{new}^{(i)}}\left(\max_{g\in F_{base}^{(i)}}\cos(\mathbf{v}(f),\mathbf{v}(g))\right) $$ |  | 

where $\mathbf{v}(\cdot)$ denotes the embedding vector. We finally report the Average Max Redundancy (AMR) to compare human and AI groups.

### 2.3. RQ 2: How does reviewer sentiment differ between AI-generated and human-written PRs

To understand how human developers perceive code generated by AI agents, we analyze the sentiments expressed in code review comments. Specifically, we compare the emotional reactions in Agentic-PRs versus Human-PRs using Dataset A (the full Python dataset) for this analysis.

To obtain the sentiments, we use state-of-the-art sentiment analysis model, Emotion English DistilRoBERTa-base ([Hartmann, 2022](#bib.bib11)). This model classifies emotions to Ekman’s six basic emotions (anger, disgust, fear, joy, sadness, surprise) and neutral. Since the model has a maximum token length of 512, we exclude the data which was more than maximum token lengths.

To compare the emotional reactions in Agentic-PRs versus Human-PRs, we analyze in the following process. First, we used code review comments from $pr\_comments$, $pr\_review\_comments\_v2$, $pr\_reviews$ from AIdev ([Li et al., 2025](#bib.bib6)).
To focus on developer sentiments, we exclude comments made by bots.
Second, we filter Dataset A to identify the PRs made by Agents and Humans.
Next, we classify the sentiments of comments made by each PR using Emotion English DistilRoBERTa-base.
We calculate the average sentiment scores per PR to obtain how developers perceived within each PR.
This process was applied separately to Agentic-PRs and Human-PRs.

Additionally, we identify the PRs with the highest sentiment scores for each emotion in both Agentic-PRs and Human-PRs. Analyzing these PRs provides further insights into how the two groups differ in terms of sentiments expressed during code reviews.

## 3. Results

### 3.1. Results of RQ1

##### Raw Code Metrics:

As shown in [Table 1](#S3.T1), while code additions vary slightly between groups, human developers remove significantly ($p<0.001$) more multi-lines-string (26.26) than AI agents (8.47), alongside a higher average LOC removal (25.51 vs. 16.60).

| Change Types | PRs’ types | LOC | Multi- Lines | Blank Lines | 
| Addition | Human | 23.01 | 15.79 | 6.16 | 
|  | Agent | 23.78 | 16.48 | 6.02 | 
|  | $\Delta$ Diff | -0.77 <sup>\*\*\*</sup> | -0.69 | 0.14 <sup>\*</sup> | 
| Removal | Human | 25.51 | 26.26 | 6.99 | 
|  | Agent | 16.60 | 8.47 | 5.05 | 
|  | $\Delta$ Diff | 8.91 | 17.79 <sup>\*\*\*</sup> | 1.94 | 
| \* Significant ($p<0.05$) \*\*\* Highly Significant ($p<0.001$) |  |  |  |  | 

##### Cyclomatic Complexity (CC):

As shown in [Table 2](#S3.T2), the computation of the CC through all pairs, most of code changes or 18,968 pairs (85.02%) have zero complexity score. The result shows that only 3,333 from 22,311 pairs (14.94%) have scored more than 0 which include 1,343 pairs (6.02%) are low risk code removal pairs, 1,979 pairs (8.87%) are low risk code addition pairs and 11 pairs (0.05%) are high risk code addition pairs.

| PRs’ types | Complexity Score (CC) |  |  | 
|  | 0 | 0 \< \|CC\| \< 10 | 10+ | 
|  | No Risk | Low Risk | High Risk | 
| Human | 8,643 | 1,463 | 6 | 
| Agent | 10,325 | 1,859 | 5 | 
| All (PRs) | 18,968 | 3,322 | 11 | 

##### Redundancy:

As shown in [Figure 2](#S3.F2), Agentic-PRs demonstrate a significantly higher level of redundancy.
For low Max Redundancy Score (MRS, see [subsubsection 2.2.2](#S2.SS2.SSS2)) sections, the distributions of AI agents and humans are largely similar.
However, for medium MRS sections (0.3–0.8), AI agents exhibit higher AMR.
We infer that both humans and AI agents produce some similar code (e.g., API calls or common patterns).
However, LLM-generated code significantly exceeds human-written code in higher AMR ranges.
Quantitatively, the Average Max Redundancy (AMR) for AI agents is 0.2867, compared to only 0.1532 for humans, representing a nearly 1.87x increase. Mann-Whitney test confirms that this difference is statistically significant ($p<0.001$).

Answer to RQ1: While traditional metrics show minimal differences between agentic-PRs and human-PRs, redundancy metric analysis shows code in agentic-PRs contain significantly more redundancy ($p<0.001$).

### 3.2. Results of RQ2

The result of RQ2 is shown in [Figure 3](#S3.F3).
The most frequent sentiment is neutral, meaning that reviewers mostly review PRs respectfully for both Human-PRs and Agentic-PRs.
However, comparing the differences between each sentiment, Agentic-PRs had a higher proportion of neutral, joy, and sadness, while Human-PRs had a higher proportion of disgust, anger, fear, and surprise.

Answer to RQ2: Our analysis shows that reviewers tend to express more neutral or positive emotions towards AI-generated contributions than human ones.

## 4. Discussion

### 4.1. Disconnect between Quality and Sentiment

Despite the similarity in traditional metrics, we found a more critical issue on AI-generated PR. Our redundancy analysis (RQ1) shows that AI agents introduce significantly more redundancy than humans. AMR for Agentic-PRs is nearly double that of Human-PRs. This confirms that AI agents tend to generate redundant code instead of reusing existing code.

However, RQ2 shows that reviewers do not react negatively to this issue. In fact, reviewers express fewer negative emotions (such as anger or disgust) towards Agentic-PRs compared to Human-PRs. This counter-intuitive disconnect may stem from the training objectives of current LLMs. Models aligned using Reinforcement Learning from Human Feedback([Ouyang et al., 2022](#bib.bib17)) are optimized to maximize human preference and perceived helpfulness  ([Casper et al., 2023](#bib.bib18)). Existing studies observed that LLMs tend to prioritize sycophancy over maximizing the accuracy of truthful statements or code quality when responding([Ouyang et al., 2022](#bib.bib17); [Sharma et al., 2023](#bib.bib23); [Li et al., 2024](#bib.bib22); [Perry et al., 2023](#bib.bib21); [Wei et al., 2024](#bib.bib20); [Fanous et al., 2025](#bib.bib19)).
Consequently, AI agents tend to produce code that appears superficially correct and helpful.

This disconnect suggests a reviewer’s blind spot. AI-generated code is syntactically correct and often passes tests. Because LLM agents generate code based on probability, the output looks plausible on the surface. As a result, reviewers may lower their vigilance. They focus on whether the code works (pass rate), but they fail to check if the code duplicates existing logic in the repository.

### 4.2. The Risk of Silent Technical Debt

This situation leads to the accumulation of silent technical debt. When an AI agent introduces a Type-4 clone, it creates a duplicate maintenance point. Previous studies have demonstrated that inconsistent updates to duplicated code are a primary source of software defects ([Juergens et al., 2009](#bib.bib4)). If a bug exists in the logic, a developer might fix the original utility function but miss the redundant copy created by the AI.
Because reviewers are reacting positively (or neutrally) to these PRs, this debt accumulates unnoticed. Consequently, the codebase becomes bloated with redundant logic, which decreases long-term readability and increases future maintenance effort ([Roy and Cordy, 2007](#bib.bib8)).

### 4.3. Implications

For Agent Builders: Researchers and tool developers need to address the issue of code redundancy. Our results show that current agents often ignore existing code. Therefore, builders should evaluate agents not just on pass rates, but also on code reuse metrics. For Software Developers: Although AI agents increase coding speed in the short term, developers must be aware of the impact on long-term maintainability. The plausible code from AI may contain hidden redundancy. Reviewers should actively check for duplicated logic during code reviews. Ignoring this now may lead to higher review costs and maintenance efforts in the future.

## 5. Related Work

There are some existing approach for detect redundancy in the code (i.e., code clone), such as ([Baxter et al., 1998](#bib.bib13); [Kamiya et al., 2002](#bib.bib14)). Due to LLM’s probabilistic model-based nature ([Bengio et al., 2003](#bib.bib15); [Shumailov et al., 2024a](#bib.bib16)), LLM models typically do not generate textually identical code clones. Instead, they tend to produce more Type-4 clones ([Roy and Cordy, 2007](#bib.bib8)), redundant code that exhibits textual inconsistencies but shares similar semantic meaning. However, existing tools are not effective at detecting these Type-4 semantic clones in Agentic-PRs. Early approaches, such as ([Sasaki et al., 2010](#bib.bib9)), detect clones by comparing file hashes. This approach is too coarse because agents often add specific functions rather than duplicating entire files. Later approaches, such as ([Kim et al., 2018](#bib.bib5)), use information retrieval techniques to find similar code, but they rely on keyword matching and often miss semantic similarities when the syntax is different.

## 6. Threats to Validity

Internal Validity We relied on PyRef to filter out refactorings (Move Method/Rename Method). If PyRef fails to detect a refactoring, we might incorrectly label valid code movement as redundancy. To mitigate this, we manually verified 10 sample of the results. Additionally, we only analyzed the crewAI repository for RQ1 due to computational costs. While this repository is highly active, it may not represent all coding styles and results might not generalize.

External Validity We focused only on Python repositories. The behavior of AI agents may differ in other languages like Java or C++. Furthermore, our sentiment analysis model is trained on general English text. It may misinterpret technical discussions in code reviews as neutral or negative emotions.

## 7. Conclusion

This study investigates the impact of AI coding agents in SE beyond simple pass rates. We combined a semantic redundancy analysis with a reviewer sentiment analysis. We found that AI agents produce more redundant code (Type-4 clones) than human developers. However, human reviewers do not punish this behavior; instead, they show less negative sentiment towards AI-generated PRs. We conclude that the surface-level plausibility of AI code can mask poor design choices. This leads to hidden technical debt, where redundancy accumulates without being noticed. As the use of AI agents increases, developers need to maintain high review standards to ensure long-term code maintainability.

###### Acknowledgements.

This work was partly developed through discussions held during the AI-Driven SE Summit 2025.
## References

- 
PYREF: 21st IEEE International Working Conference on Source Code Analysis and Manipulation, SCAM 2021.
pp. 136–141.
External Links: [Document](https://dx.doi.org/10.1109/SCAM52516.2021.00025), [Link](https://www.scopus.com/pages/publications/85123293057) Cited by: [§2.2.2](#S2.SS2.SSS2.p2.1).
- 
Clone detection using abstract syntax trees.
In Proceedings. International Conference on Software Maintenance (Cat. No. 98CB36272),
pp. 368–377.
External Links: ISSN 1063-6773,
[Document](https://dx.doi.org/10.1109/ICSM.1998.738528) Cited by: [§5](#S5.p1.1).
- 
Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity.
 arXiv.
External Links: 2507.09089,
[Document](https://dx.doi.org/10.48550/arXiv.2507.09089) Cited by: [§1](#S1.p1.1).
- 
A neural probabilistic language model.
Journal of machine learning research 3 (Feb), pp. 1137–1155.
Cited by: [§1](#S1.p2.1), [§2.2.2](#S2.SS2.SSS2.p1.1), [§5](#S5.p1.1).
- 
Open Problems and Fundamental Limitations of Reinforcement Learning from Human Feedback.
Transactions on Machine Learning Research.
External Links: ISSN 2835-8856
Cited by: [§4.1](#S4.SS1.p2.1).
- 
SycEval: Evaluating LLM Sycophancy.
 arXiv.
External Links: 2502.08177,
[Document](https://dx.doi.org/10.48550/arXiv.2502.08177) Cited by: [§4.1](#S4.SS1.p2.1).
- 
Refactoring: improving the design of existing code.
 Addison-Wesley Professional.
Cited by: [§1](#S1.p2.1).
- 
Emotion english distilroberta-base.
Note: [https://huggingface.co/j-hartmann/emotion-english-distilroberta-base/](https://huggingface.co/j-hartmann/emotion-english-distilroberta-base/) Cited by: [§2.3](#S2.SS3.p2.1).
- 
SWE-bench: Can Language Models Resolve Real-world Github Issues?.
In The Twelfth International Conference on Learning Representations,
Cited by: [§1](#S1.p1.1).
- 
Do code clones matter?.
In Proceedings of the 31st International Conference on Software Engineering,
ICSE ’09, USA, pp. 485–495.
External Links: [Document](https://dx.doi.org/10.1109/ICSE.2009.5070547),
ISBN 978-1-4244-3453-4
Cited by: [§1](#S1.p2.1), [§2.2.2](#S2.SS2.SSS2.p2.1), [§4.2](#S4.SS2.p1.1).
- 
CCFinder: a multilinguistic token-based code clone detection system for large scale source code.
IEEE Transactions on Software Engineering 28 (7), pp. 654–670.
External Links: ISSN 1939-3520,
[Document](https://dx.doi.org/10.1109/TSE.2002.1019480) Cited by: [§5](#S5.p1.1).
- 
FaCoY: a code-to-code search engine.
In Proceedings of the 40th International Conference on Software Engineering,
ICSE ’18, New York, NY, USA, pp. 946–957.
External Links: [Document](https://dx.doi.org/10.1145/3180155.3180187),
ISBN 978-1-4503-5638-1
Cited by: [§5](#S5.p1.1).
- 
The Rise of AI Teammates in Software Engineering (SE) 3.0: How Autonomous Coding Agents Are Reshaping Software Engineering.
 arXiv.
External Links: 2507.15003,
[Document](https://dx.doi.org/10.48550/arXiv.2507.15003) Cited by: [§1](#S1.p1.1), [§1](#S1.p4.1), [§2.1](#S2.SS1.p1.1), [§2.3](#S2.SS3.p3.1).
- 
Dissecting Human and LLM Preferences.
In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers),  L. Ku, A. Martins, and V. Srikumar (Eds.),
Bangkok, Thailand, pp. 1790–1811.
External Links: [Document](https://dx.doi.org/10.18653/v1/2024.acl-long.99) Cited by: [§4.1](#S4.SS1.p2.1).
- 
A Complexity Measure.
IEEE Transactions on Software Engineering SE-2 (4), pp. 308–320.
External Links: ISSN 1939-3520,
[Document](https://dx.doi.org/10.1109/TSE.1976.233837) Cited by: [§1](#S1.p3.1).
- 
Training language models to follow instructions with human feedback.
In Proceedings of the 36th International Conference on Neural Information Processing Systems,
NIPS ’22, Red Hook, NY, USA, pp. 27730–27744.
External Links: ISBN 978-1-7138-7108-8
Cited by: [§4.1](#S4.SS1.p2.1).
- 
Do Users Write More Insecure Code with AI Assistants?.
In Proceedings of the 2023 ACM SIGSAC Conference on Computer and Communications Security,
CCS ’23, New York, NY, USA, pp. 2785–2799.
External Links: [Document](https://dx.doi.org/10.1145/3576915.3623157),
ISBN 979-8-4007-0050-7
Cited by: [§1](#S1.p1.1), [§4.1](#S4.SS1.p2.1).
- 
A survey on software clone detection research.
Queen’s School of computing TR 541 (115), pp. 64–68.
Cited by: [§1](#S1.p1.1), [§1](#S1.p2.1), [§4.2](#S4.SS2.p1.1), [§5](#S5.p1.1).
- 
Finding file clones in FreeBSD Ports Collection.
In 2010 7th IEEE Working Conference on Mining Software Repositories (MSR 2010),
pp. 102–105.
External Links: ISSN 2160-1860,
[Document](https://dx.doi.org/10.1109/MSR.2010.5463293) Cited by: [§5](#S5.p1.1).
- 
Towards Understanding Sycophancy in Language Models.
In The Twelfth International Conference on Learning Representations,
Cited by: [§4.1](#S4.SS1.p2.1).
- 
The Curse of Recursion: Training on Generated Data Makes Models Forget.
 arXiv.
External Links: 2305.17493,
[Document](https://dx.doi.org/10.48550/arXiv.2305.17493) Cited by: [§1](#S1.p2.1), [§2.2.2](#S2.SS2.SSS2.p1.1), [§5](#S5.p1.1).
- 
AI models collapse when trained on recursively generated data.
Nature 631 (8022), pp. 755–759.
External Links: ISSN 1476-4687,
[Document](https://dx.doi.org/10.1038/s41586-024-07566-y) Cited by: [§1](#S1.p2.1).
- 
Simple synthetic data reduces sycophancy in large language models.
Cited by: [§4.1](#S4.SS1.p2.1).
- 
Code Representation Learning At Scale.
 arXiv.
External Links: 2402.01935,
[Document](https://dx.doi.org/10.48550/arXiv.2402.01935) Cited by: [§2.2.2](#S2.SS2.SSS2.p2.1).
