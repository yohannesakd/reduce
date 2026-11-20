# Agentic Refactoring: An Empirical Study of AI Coding Agents

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: Kosei Horikawa, Hao Li, Yutaro Kashiwa, Bram Adams, Hajimu Iida, Ahmed E. Hassan
- Date: 2025-11-06
- Original location: https://arxiv.org/pdf/2511.04824
- Copied: 2026-11-20, from the arXiv HTML full text, converted to Markdown with trafilatura

## Text
# Agentic Refactoring: An Empirical Study of AI Coding Agents

###### Abstract.

Agentic coding tools, such as OpenAI Codex, Claude Code, and Cursor, are changing how software is developed. These AI-powered systems function as autonomous teammates capable of planning and executing complex development tasks. Agents have become active participants in refactoring, a key practice for improving internal code quality without altering observable behavior. Despite their increasing adoption, there is little empirical understanding of how agentic refactoring is used in practice, how it compares to human-driven refactoring, and what impact it has on code quality.

To address this empirical gap, we present a large-scale study of AI agent-generated refactorings in real-world open-source Java projects, analyzing $51\,412$ refactoring instances across $12\,256$ pull requests and $14\,998$ commits based on the AIDev dataset. Our empirical analysis shows that refactoring is a common and intentional activity in this development paradigm, with agents explicitly targeting refactoring in 26.1% of commits. The subsequent analyses of refactoring types, purposes, and code quality focus on the $3907$ commits ($32\,611$ instances) with explicit refactoring intent. Analysis of refactoring types reveals that high-level refactorings form the largest category overall. However, agentic refactoring contains a slightly larger share of low-level, consistency-oriented edits than human refactoring (27.6% vs. 24.4%), and its two most frequent operations are Rename Variable (7.6%) and Change Variable Type (6.8%). Additionally, the stated motivations behind agentic refactoring focus overwhelmingly on internal quality concerns (with 52.5% in maintainability and 28.1% in readability), although the measured metric improvements from these frequently occurring low-level refactorings remain limited. Furthermore, quantitative evaluation of code quality metrics shows that agentic refactoring yields small but statistically significant improvements in structural metrics, particularly for medium-level changes, reducing class size and complexity.

###### Keywords:

Agentic Coding, Coding Agent, Refactoring, Pull Requests, Large Language Models
<sup>†</sup>

<sup>†</sup>cc-license: by

## 1. Introduction

Refactoring is a cornerstone of sustainable software development that improves a software system’s internal quality without changing its observable behavior ([Opdyke, 1992](#bib.bib53)). Since Martin Fowler’s catalog ([Fowler, 1999](#bib.bib21)) established the field’s conceptual foundation, subsequent studies have emphasized refactoring as a core maintenance activity that supports long-term software evolvability. Prior work links refactoring to improved readability ([Kim et al., 2014](#bib.bib11); [Sellitto et al., 2022](#bib.bib41)), higher developer productivity ([Moser et al., 2007](#bib.bib26)), and the removal of code smells ([Silva et al., 2016](#bib.bib38)), as well as to preparing a codebase for future modifications ([Pantiuchina et al., 2020](#bib.bib33)).

Despite its importance, refactoring demands deep domain knowledge and specialized skills. When executed improperly, refactoring can introduce bugs ([Pantiuchina et al., 2022](#bib.bib19)), break existing tests ([Rachatasumrit and Kim, 2012](#bib.bib31); [Kashiwa et al., 2021](#bib.bib22)), or destabilize the system ([Bavota et al., 2012](#bib.bib49)). To mitigate these inherent risks, researchers have proposed many sophisticated approaches over the decades. These techniques include methods to identify appropriate refactoring locations ([Tsantalis and Chatzigeorgiou, 2009](#bib.bib58)), refactoring recommendation systems ([Mkaouer et al., 2014](#bib.bib56)), and automatic refactoring approaches ([Shahidi et al., 2022](#bib.bib57)). While several studies reported that practitioners did not use refactoring tools ([Murphy-Hill et al., 2012](#bib.bib50)), the advent of large language models (LLMs) has recently accelerated these techniques and spurred practical adoption of automatic refactoring ([Shirafuji et al., 2023](#bib.bib59); [Depalma et al., 2024](#bib.bib35); [Bellur et al., 2025](#bib.bib62)). Many studies report that practitioners now actively leverage LLMs to generate and apply refactoring operations ([Tufano et al., 2024](#bib.bib18); [Watanabe et al., 2024](#bib.bib2); [AlOmar et al., 2024](#bib.bib60); [Deo et al., 2024](#bib.bib61)).

Software engineering is now undergoing another shift with the rise of agentic coding tools ([Hassan et al., 2025](#bib.bib51)). Unlike traditional prompt-based LLM workflows, where developers manually guide the AI step-by-step, agentic coding tools such as OpenAI Codex,<sup>1</sup><sup>1</sup>
            1
            
            
            
          [https://chatgpt.com/features/codex](https://chatgpt.com/features/codex) Claude Code,<sup>2</sup><sup>2</sup>
            2
            
            
            
          [https://www.claude.com/product/claude-code](https://www.claude.com/product/claude-code) and Cursor <sup>3</sup><sup>3</sup>
            3
            
            
            
          [https://cursor.com/](https://cursor.com/) operate as AI teammates ([Li et al., 2025](#bib.bib12)). These agents can autonomously plan, execute, test, and iterate on complex development tasks with minimal human intervention ([Sapkota et al., 2025](#bib.bib54)). In this new paradigm, agents act as collaborative refactoring teammates, actively participating in the refactoring process, ranging from simple cleanups to substantial design modifications. However, while these tools are being rapidly adopted, there is currently no empirical understanding of how this new class of agentic refactoring is used in practice, how it compares to human-driven refactoring, and what impact it has on code quality.

To address these critical gaps, we conduct a large-scale empirical study of refactorings produced in agentic coding workflows in real-world open-source projects based on the AIDev dataset ([Li et al., 2025](#bib.bib12)). We identify $51\,412$ refactoring instances across $12\,256$ pull requests and $14\,998$ commits in Java generated by agentic coding tools. We examine these agentic refactorings along four core dimensions (i.e., prevalence, types, purposes, and impacts) to answer the following research questions (RQs):

- • 
$RQ_{1}$: How prevalent is refactoring in agentic commits? To determine whether refactoring is a significant and intentional activity in agentic software development, we first quantify how often it occurs. We find that refactoring is common, with agents explicitly targeting it in 26.1% of agentic Java commits, which contain a total of $32\,611$ refactoring instances.
- • 
$RQ_{2}$: What are the common types of agentic refactoring? To assess the current sophistication of AI agents, it is crucial to determine whether they perform simple cosmetic cleanups or engage in more complex structural transformations. Our analysis reveals that, although high-level refactorings remain the largest abstraction-level category (52.4%), agentic refactoring has a slightly larger share of low-level, consistency-oriented edits than human refactoring (27.6% vs. 24.4%).
- • 
$RQ_{3}$: What is the purpose of agentic refactoring? Understanding the why behind these operations is essential to see if developers use agents for proactive quality improvement or for other tactical reasons. We find that agentic refactoring is overwhelmingly driven by the desire to improve internal code quality, specifically maintainability (52.5%) and readability (28.1%).
- • 
$RQ_{4}$: To what extent does agentic refactoring affect code quality? To justify agentic refactoring adoption, it is essential to quantitatively measure whether agentic refactoring provides tangible benefits to the codebase’s structural health. The results show that agentic refactoring yields small but significant improvements in structural metrics like code size and complexity, yet it currently fails to consistently reduce the overall count of known design and implementation smells.

Our findings provide the first large-scale empirical baseline of agentic refactoring. These results have direct implications for developers, helping them set expectations for what current agents can (and cannot) reliably refactor. For researchers, our work enables new studies of human-agent collaboration in software maintenance. Finally, for coding agent builders, our findings highlight current limitations (e.g., limited impact on design smells) and opportunities for creating agents that can perform more sophisticated, structurally-aware refactorings.

Replication Package. To facilitate replication and further studies, we provide the data used in our replication package.<sup>4</sup><sup>4</sup>
            4
            
            
            
          [https://github.com/Mont9165/Agent\_Refactoring\_Analysis](https://github.com/Mont9165/Agent_Refactoring_Analysis)

Paper Structure. The remainder of this paper is organized as follows. Section [2](#S2) reviews related work. Section [3](#S3) presents the motivating examples. Section [4](#S4) describes how we collected and filtered the data. Section [5](#S5) presents the findings of our research questions. Section [6](#S6) summarizes the key insights and discusses the implications of our study. Section [7](#S7) outlines threats to validity, and Section [8](#S8) concludes the paper.

## 2. Related Work

In this section, we discuss related work about the foundations of refactoring, large-scale empirical analyses, automated refactoring techniques, and AI-assisted software development.

### 2.1. Refactoring and Its Empirical Foundations

Research on refactoring has built a substantial empirical foundation since Fowler cataloged its patterns ([Fowler, 1999](#bib.bib21)). Beyond establishing refactoring as a core maintenance practice ([Wilking et al., 2007](#bib.bib25); [Moser et al., 2007](#bib.bib26); [Kim et al., 2011](#bib.bib29); [Chávez et al., 2017](#bib.bib28); [Dallal and Abdin, 2018](#bib.bib27)), this line of work has examined why developers refactor: to improve readability, reduce duplication, and facilitate the maintainability of software systems ([Silva et al., 2016](#bib.bib38); [Kim et al., 2012](#bib.bib37)), but also to improve comprehension, reduce cognitive load, and prepare code for future changes ([Dallal and Abdin, 2018](#bib.bib27)). For instance, Kim et al. ([Kim et al., 2014](#bib.bib11)) surveyed Microsoft developers and found that refactoring is widely regarded as beneficial for improving code quality and productivity. Specifically, developers cited the benefits of refactoring as improved readability, improved maintainability, and fewer bugs. Their quantitative analysis of Windows 7 modules also showed that a dedicated refactoring effort led to measurable benefits, including a significant reduction in inter-module dependencies and post-release defects. Their findings provide the conceptual basis for our analysis of refactoring purpose in agentic commits (RQ3).
Building on these foundational insights, subsequent research has investigated refactoring practices at scale to understand their prevalence and impact on software quality.

### 2.2. Large-Scale Refactoring Studies and Quality Impact

The large-scale mining of refactorings has revealed that refactoring is pervasive in both industrial and open-source development ([Xing and Stroulia, 2006](#bib.bib48); [Murphy-Hill et al., 2012](#bib.bib50); [Vassallo et al., 2019](#bib.bib39)).
More recently, large-scale refactoring detectors such as RefactoringMiner ([Tsantalis et al., 2022](#bib.bib9); [Alikhanifard and Tsantalis, 2025](#bib.bib6)) and RefDiff ([Silva et al., 2021](#bib.bib30)) have enabled mining-based studies at scale.

Although refactoring is generally expected to improve quality, empirical evidence on its actual impact remains mixed.
Some studies report positive effects on code stability, readability, and productivity, particularly in agile settings ([Horikawa et al., 2025](#bib.bib32); [Kim et al., 2012](#bib.bib37); [Moser et al., 2007](#bib.bib26)),
whereas others show that refactoring does not consistently remove design problems or prevent defects ([Bavota et al., 2015](#bib.bib24)).
For example, Cedrim et al. ([Cedrim et al., 2017](#bib.bib42)) found that less than 10% of refactorings effectively remove code smells, while over 30% introduce new ones.
Similarly, Szoke et al. ([Szoke et al., 2014](#bib.bib34)) observed that only large-scale, systematic bulk refactorings lead to measurable quality improvement, suggesting that scope matters as much as type. Bavota et al. ([Bavota et al., 2012](#bib.bib49)) further noted that inheritance-related refactorings are especially error-prone, emphasizing the need to consider technical context.

Beyond the technical dimension, developer intent matters.
Palomba et al. ([Palomba et al., 2017](#bib.bib40)) showed that refactorings frequently co-occur with bug fixes, implying opportunistic rather than proactive behavior.
This aligns with Silva et al. ([Silva et al., 2016](#bib.bib38)) and Pantiuchina et al. ([Pantiuchina et al., 2020](#bib.bib33)), who found that evolving requirements, readability, and maintainability, rather than smell removal, drive most refactoring decisions.
Taken together, these findings highlight that refactoring impact depends on its type, scope, and motivation. We extend this perspective to agentic refactoring in RQ2 and RQ4.

### 2.3. Automated Refactoring Support

Automated and semi-automated refactoring has been explored in software engineering for over two decades. Rule-based tools such as JDeodorant ([Tsantalis et al., 2018](#bib.bib47); [Mazinanian et al., 2016](#bib.bib46)) and search-based refactoring engines ([O’Keeffe and Cinnéide, 2008](#bib.bib44)) attempted to reduce manual effort; however, they suffered from low adoption due to lack of trust and limited semantic reasoning ([Murphy-Hill et al., 2012](#bib.bib50); [Vassallo et al., 2019](#bib.bib39)).
Recently, the refactoring capability of large language models (LLMs) has also been explored ([Depalma et al., 2024](#bib.bib35); [Cordeiro et al., 2026](#bib.bib36)). Cordeiro et al. ([Cordeiro et al., 2026](#bib.bib36)) evaluated the refactoring quality of StarCoder2 under various prompt-engineering strategies (e.g., zero-shot, one-shot) and found that LLMs can outperform developers in removing code smells under specific prompting configurations. However, these studies focus on prompt-based refactoring, where models perform one-shot transformations given explicit instructions.

In contrast, our study explores agentic refactoring, where autonomous coding agents (e.g., OpenAI Codex, Devin, Cursor) plan, execute, and validate changes through iterative reasoning and feedback. This paradigm differs from prompt-based generation in that agents can decompose complex objectives, perform refactoring alongside other maintenance activities, and generate verifiable pull requests with minimal human intervention. Thus, our work provides the first large-scale empirical view of intentional, agentic refactoring practices carried out through agentic coding workflows.

### 2.4. AI-Assisted Software Development

AI-based coding assistance has evolved rapidly from autocomplete-style tools ([Svyatkovskiy et al., 2020](#bib.bib14)) to modern LLM-based copilots capable of nontrivial synthesis and transformation ([Dakhel et al., 2023](#bib.bib13)). Empirical studies report that AI-generated code accelerates development but often introduces maintainability, redundancy, and security concerns ([Sandoval et al., 2023](#bib.bib15); [Asare et al., 2023](#bib.bib16)).
Trust and validation remain key challenges when adopting AI-generated code.
Sergeyuk et al. ([Sergeyuk et al., 2025](#bib.bib45)) reported that developers frequently verify AI suggestions manually due to concerns over correctness and control.
In particular, 21.9% of respondents avoided using AI for refactoring tasks, highlighting that trust is critical where functional behavior must remain unchanged. LLMs further exhibit inconsistency and limited contextual understanding ([Sandoval et al., 2023](#bib.bib15); [Asare et al., 2023](#bib.bib16)). Even with identical prompts, tools like ChatGPT may produce divergent or unnecessary edits, increasing review effort and cognitive overhead ([Depalma et al., 2024](#bib.bib35)).
Evidence from agentic coding platforms further supports these findings.
A recent study of autonomously generated pull requests (Agentic-PRs) ([Watanabe et al., 2026](#bib.bib55)) found that 45.1% required post-review fixes (most often for bugs, refactoring, or documentation), despite agents performing refactoring more frequently than humans (24.9% vs. 14.9%).
Overall, while AI-assisted tools can restructure code effectively, human oversight remains essential to ensure correctness and maintainability. This issue becomes even more significant in agentic refactoring, where AI autonomously plans and applies code changes.

### 2.5. Agentic Software Development and Research Gap

Recent work has introduced the notion of agentic software engineering ([Hassan et al., 2025](#bib.bib51)), where AI systems act as autonomous collaborators capable of proposing, modifying, and integrating pull requests ([Li et al., 2025](#bib.bib12)). The AIDev dataset enables empirical research on such activities at scale. However, while early work analyzes AI contributions in issue resolution ([Chouchen et al., 2024](#bib.bib1)) and documentation ([Rahman et al., 2024](#bib.bib17)), and reports refactoring only as one broad category of agent activity, no study has mined the concrete refactoring operations that agents perform or examined how AI-generated refactorings differ in type, intent, and impact from human refactoring. Our work addresses this gap by providing the first large-scale, operation-level empirical analysis of refactoring in agentic commits, introducing Agentic Refactoring as a novel concept and dataset.

In summary, prior research has matured along multiple refactoring dimensions (motivation, automation, empirical evolution, and human factors), but agentic refactoring remains unexplored. Our study is the first to provide a large-scale empirical view of agentic refactoring by (i) quantifying its operation-level prevalence, (ii) contrasting AI and human refactoring styles, (iii) classifying refactoring intent in AI settings, and (iv) evaluating its quality impact.

## 3. Motivating Example

AI agents are increasingly integrated into software development workflows. Coding agents such as Claude Code, Devin, and Cursor can not only generate code but also collaboratively refactor existing codebases with developers ([Watanabe et al., 2026](#bib.bib55)). Rather than acting as fully autonomous systems, these agents increasingly function as collaborative refactoring teammates, assisting humans in restructuring large or complex code to enhance maintainability and readability.

Figure [1](#S3.F1) illustrates two representative examples of such agentic refactoring. Figure [1(a)](#S3.F1.sf1) demonstrates an agent automatically replacing raw types with parameterized generic types to improve type safety.<sup>5</sup><sup>5</sup>
            5
            
            
            
          [https://github.com/jdereg/java-util/commit/15b8e6d932ead9860f854bd0e0e84e16f2bbf230](https://github.com/jdereg/java-util/commit/15b8e6d932ead9860f854bd0e0e84e16f2bbf230) By systematically converting raw Map declarations to their fully parameterized equivalents, the agent eliminates unsafe casts and improves code clarity.
In contrast, Figure [1(b)](#S3.F1.sf2) shows another type of agentic refactoring, where an agent systematically renames methods to improve consistency.<sup>6</sup><sup>6</sup>
            6
            
            
            
          [https://github.com/Ddemon26/2006Scape/pull/4/files](https://github.com/Ddemon26/2006Scape/pull/4/files) Such operations improve naming clarity and stylistic uniformity but have little direct effect on structural quality metrics.

These contrasting examples show that AI agents are active participants in the refactoring process. However, this observation raises a critical question: Do these operations consistently improve software quality metrics (e.g., lines of code, cyclomatic complexity, coupling), or do they merely restructure code superficially? Despite the rapid adoption of these agents, there remains limited empirical understanding of how such agentic refactorings are used in practice.

To address this gap, we conduct a large-scale empirical study of agentic refactorings in real-world open-source projects. We systematically examine four dimensions of agentic refactoring: the frequency of AI participation (RQ1), the types of refactoring operations performed (RQ2), the purpose expressed by developers and AI agents (RQ3), and the resulting impacts on internal quality metrics (RQ4). Together, these research questions aim to clarify whether agentic refactorings merely automate surface-level cleanup tasks or contribute to structural and maintainability improvements in software systems.

## 4. Data Collection

In this section, we describe the data mining and data filtering as outlined in Figure [2](#S3.F2).

### 4.1. Data Mining

To study agentic refactoring in real-world projects, we start with the AIDev dataset ([Li et al., 2025](#bib.bib12)). This dataset is an ideal source as it contains 932,791 pull requests (PRs) created by five coding agents from over 61,000 repositories.
However, the commit data included in the AIDev dataset<sup>7</sup><sup>7</sup>
              7
              
              
              
            [https://huggingface.co/datasets/hao-li/AIDev](https://huggingface.co/datasets/hao-li/AIDev) (the pr\_commits table) only covers repositories with more than 100 GitHub stars.
To ensure broader coverage, we leverage the GitHub REST API<sup>8</sup><sup>8</sup>
              8
              
              
              
            [https://docs.github.com/en/rest](https://docs.github.com/en/rest) to mine all commits using the all\_pull\_request table, which provides pull request metadata for all repositories regardless of star count. In total, we collect 1,311,057 agentic commits and share this expanded dataset publicly as AIDev-full.<sup>9</sup><sup>9</sup>
              9
              
              
              
            [https://huggingface.co/datasets/hao-li/AIDev-full](https://huggingface.co/datasets/hao-li/AIDev-full)

### 4.2. Data Filtering

To construct a focused dataset tailored for refactoring analysis, we perform a multi-stage filtering process based on the collected data curated from the AIDev dataset.

#### 4.2.1. Identify Java Modifying Commits

In this study, we focus on commits that modify at least one .java file for three reasons.
First, focusing on Java is consistent with the majority of large-scale empirical refactoring studies ([Murphy-Hill et al., 2012](#bib.bib50); [Vassallo et al., 2019](#bib.bib39); [Cedrim et al., 2017](#bib.bib42)), enabling direct comparison with prior work.
Second, RefactoringMiner ([Tsantalis et al., 2022](#bib.bib9); [Alikhanifard and Tsantalis, 2025](#bib.bib6)) is the only refactoring detection tool that supports 103 types with an F-score of 99.5%; multi-language alternatives such as RefDiff ([Silva et al., 2021](#bib.bib30)) support substantially fewer types.
Third, DesigniteJava ([Sharma, 2024](#bib.bib10)) provides comprehensive code quality metrics, code smell detection, and design smell detection specifically for Java, enabling the multi-perspective analysis in RQ4.

We further exclude all merge commits to avoid duplicated changes and ambiguous parent relationships.

#### 4.2.2. Project Filtering

To ensure that our analysis targets substantive software systems rather than educational or trivial repositories, we apply several steps to filter the projects.

##### Step 1 – Automated Classification.

We leverage GPT-4.1-mini to classify each repository based on the content of its README.md file. We selected GPT-4.1-mini for its cost efficiency given the scale of the dataset ($3232$ repositories); the total API cost was approximately $4 for 5.58 million tokens, whereas using a higher-end model (e.g., Claude Opus) would cost approximately $120 for the same task. The classification prompt was designed to operationalize the three category definitions described below and was verified on examples before application to the full dataset. The full prompt and its development process are documented in the replication package.<sup>10</sup><sup>10</sup>
                  10
                  
                  
                  
                [https://github.com/Mont9165/Agent\_Refactoring\_Analysis/blob/main/PROMPTS.md](https://github.com/Mont9165/Agent_Refactoring_Analysis/blob/main/PROMPTS.md)
The classification reliability is ensured through human validation (see Step 2).
Each project is assigned to one of the following three categories:

- • 
non\_toy: Software repositories with meaningful functionality intended for real-world use or research purposes (e.g., web frameworks, database client libraries, build plugins, academic research tools, domain-specific utilities), identified by the presence of usage instructions, installation guides, CI pipelines, versioned releases, documented APIs, or active issue management.
- • 
toy: Tutorial repositories, coursework material, evaluation harnesses, or minimal demonstrative examples, identified by explicit indicators such as assignment instructions, tutorial structure, absence of CI/CD, no versioned releases, or no evidence of external usage.
- • 
uncertain: Repositories whose purpose cannot be reliably determined due to minimal or missing README.md, ambiguous descriptions, or insufficient information to classify as either non\_toy or toy.

##### Step 2 – Manual Verification.

To validate the reliability of the automated classification in Step 1, we conducted a systematic manual verification. We drew a stratified proportional sample of 344 repositories from the full set of $3232$ GPT-classified repositories (95% confidence level, 5% margin of error, using the Cochran formula). Of the 344 sampled repositories, 25 were excluded because the repositories had been deleted or made private since the time of data collection, leaving 319 for analysis. Two annotators (with 8 and 9 years of programming experience), blind to the GPT-4.1-mini labels, independently classified each of the 319 repositories based on its README, source code, and GitHub activity. Disagreements were resolved through discussion with a third annotator (18 years of experience). As shown in Table [1](#S4.T1), inter-rater agreement between annotators was Cohen’s $\kappa$ = 0.83 (almost perfect agreement), and agreement between GPT-4.1-mini and the adjudicated human labels was Cohen’s $\kappa$ = 0.80 (substantial agreement). These results confirm that the automated classification is consistent with human judgment.

To characterize the disagreements behind these kappa scores, we inspected all 32 of the 319 cases in which the GPT-4.1-mini label differed from the adjudicated human label. All 32 disagreements involved the boundary between non\_toy and toy, and most of them followed the same direction. In 24 of the 32 cases, GPT-4.1-mini labeled a repository as non\_toy, while the annotators labeled it as toy. A typical case was a personal or experimental project with a README that described substantive functionality, such as a microservice-based terminal-operations system or an AI question-answering service. However, the repository had no releases, no CI, and no evidence of external use. The annotators also inspected the source code and GitHub activity. They gave these signals more weight than the README. The reverse error occurred in only 8 of the 32 cases. These cases usually involved niche but functional software, such as a game-specific mod with installation and troubleshooting instructions. The same boundary accounts for all 26 disagreements between the two annotators. This result suggests that distinguishing non\_toy from toy is the most difficult judgment in this task. For our study, this error pattern has a limited effect. About 7.5% of the repositories (24 of 319 cases) may be toy-like projects that pass the filter and add noise. By contrast, substantive projects are rarely excluded.

| Comparison | Cohen’s $\kappa$ | Accuracy | Macro F1 | 
|---|---|---|---|
| Human vs Human | 0.83 | 0.92 | 0.92 | 
| GPT-4.1-mini vs Human | 0.80 | 0.90 | 0.90 | 

##### Step 3 – Final Project Selection.

After classification and verification, we retain $1635$ projects labeled as non\_toy. We exclude $1235$ repositories categorized as toy and $362$ as uncertain. Finally, to avoid redundancy, we remove forked repositories. This results in a final corpus of $1613$ unique software projects for analysis. The Java subset includes $14\,998$ non-merge commits suitable for automated refactoring detection and metric extraction. This filtering step reduces noise from trivial repositories and ensures that our analysis focuses on substantive software systems.

#### 4.2.3. Collect Refactoring Operations by RefactoringMiner

To identify specific refactoring operations within our set of Java commits, we use RefactoringMiner 3.0<sup>11</sup><sup>11</sup>
                11
                
                
                
              [https://github.com/tsantalis/RefactoringMiner/releases/tag/3.0.11](https://github.com/tsantalis/RefactoringMiner/releases/tag/3.0.11) for each commit. RefactoringMiner detects 103 distinct refactoring types and identifies their precise locations, achieving an overall F-score of 99.5% ([Tsantalis et al., 2022](#bib.bib9); [Alikhanifard and Tsantalis, 2025](#bib.bib6)).
Specifically, RefactoringMiner analyzes the abstract syntax trees (ASTs) of the modified Java files between consecutive revisions to identify the types and locations of applied refactorings.

We adopt the commit as the unit of analysis in this study. RefactoringMiner operates on pairs of consecutive revisions, making the commit the natural and necessary unit for refactoring detection. This is consistent with prior large-scale empirical refactoring studies ([Murphy-Hill et al., 2012](#bib.bib50); [Vassallo et al., 2019](#bib.bib39); [Cedrim et al., 2017](#bib.bib42)), which also adopt the commit as their unit of analysis. Furthermore, the scale of our dataset ($14\,998$ commits across $1613$ repositories) requires automated and reproducible methods.
This process generates a dataset linking specific commits to the refactoring operations they contain.
From the initial set of $14\,998$ commits, RefactoringMiner identifies $5789$ commits as containing at least one refactoring operation.

[AlOmar et al., 2019](#bib.bib3))

| (1) Refactor\* |  | (30) Removed poor coding practice |  | (59) Change design |  | 
| (2) Mov\* |  | (31) Improve naming consistency |  | (60) Modularize the code |  | 
| (3) Split\* |  | (32) Removing unused classes |  | (61) Code cosmetics |  | 
| (4) Fix\* |  | (33) Pull some code up |  | (62) Moved more code out of |  | 
| (5) Introduce\* |  | (34) Use better name |  | (63) Remove dependency |  | 
| (6) Decompos\* |  | (35) Replace it with |  | (64) Enhanced code beauty |  | 
| (7) Reorganiz\* |  | (36) Make maintenance easier |  | (65) Simplify internal design |  | 
| (8) Extract\* |  | (37) Code cleanup |  | (66) Change package structure |  | 
| (9) Merg\* |  | (38) Minor Simplification |  | (67) Use a safer method |  | 
| (10) Renam\* |  | (39) Reorganize project structures |  | (68) Code improvements |  | 
| (11) Chang\* |  | (40) Code maintenance for refactoring |  | (69) Minor enhancement |  | 
| (12) Restructur\* |  | (41) Remove redundant code |  | (70) Get rid of unused code |  | 
| (13) Reformat\* |  | (42) Moved and gave clearer names to |  | (71) Fixing naming convention |  | 
| (14) Extend\* |  | (43) Refactor bad designed code |  | (72) Fix module structure |  | 
| (15) Remov\* |  | (44) Getting code out of |  | (73) Code optimization |  | 
| (16) Replac\* |  | (45) Deleting a lot of old stuff |  | (74) Fix a design flaw |  | 
| (17) Rewrit\* |  | (46) Code revision |  | (75) Nonfunctional code cleanup |  | 
| (18) Simplifi\* |  | (47) Fix technical debt |  | (76) Improve code quality |  | 
| (19) Creat\* |  | (48) Fix quality issue |  | (77) Fix code smell |  | 
| (20) Improv\* |  | (49) Antipattern bad for performances |  | (78) Use less code |  | 
| (21) Add\* |  | (50) Major/Minor structural changes |  | (79) Avoid future confusion |  | 
| (22) Modif\* |  | (51) Clean up unnecessary code |  | (80) More easily extended |  | 
| (23) Enhanc\* |  | (52) Code reformatting & reordering |  | (81) Polishing code |  | 
| (24) Rework\* |  | (53) Nicer code / formatted / structure |  | (82) Move unused file away |  | 
| (25) Inlin\* |  | (54) Simplify code redundancies |  | (83) Many cosmetic changes |  | 
| (26) Redesign\* |  | (55) Added more checks for quality factors |  | (84) Inlined unnecessary classes |  | 
| (27) Cleanup |  | (56) Naming improvements |  | (85) Code cleansing |  | 
| (28) Reduc\* |  | (57) Renamed for consistency |  | (86) Fix quality flaws |  | 
| (29) Encapsulat\* |  | (58) Refactoring towards nicer name analysis |  | (87) Simplify the code |  | 

#### 4.2.4. Identify Agentic Refactoring Commits

To understand how often agentic refactoring is an intentional act, we must identify commits that explicitly state refactoring intent. We define a commit as having *explicit refactoring intent* if (i) its commit message matches at least one of the Self-Affirmed Refactoring (SAR) keyword patterns from AlOmar et al. \[2\], and (ii) RefactoringMiner detects at least one refactoring operation in the commit. We refer to such commits as *Agentic Refactoring* commits. The keyword patterns (listed in Table [2](#S4.T2)) were developed and validated by AlOmar  et al. and have been widely adopted in self-affirmed refactoring research; our study applies these established patterns without modification.

We distinguish *intent* from *purpose* in this study. Intent is a binary classification of whether a commit explicitly targets refactoring (this section, based on SAR keyword matching). Purpose is a multi-class classification of why the refactoring was performed (e.g., maintainability, readability), analyzed in Section 5.3.2 using GPT-4.1-mini.

The complete list of patterns is presented in Table [2](#S4.T2).
Applying this procedure to the $14\,998$ commits yields $3907$ Agentic Refactoring Commits.

| AI Agent | # PRs (%) | # Commits (%) | 
|---|---|---|
| OpenAI Codex | $11\,557$ (94.3%) | $13\,389$ (89.3%) | 
| Devin | $335$ (2.7%) | $860$ (5.7%) | 
| Cursor | $337$ (2.7%) | $663$ (4.4%) | 
| Claude Code | $27$ (0.2%) | $86$ (0.6%) | 
| Total | $12\,256$ (100%) | $14\,998$ (100%) | 
| \*GitHub Copilot is part of the AIDev dataset but produced no commits after filtering, so it is excluded here. |  |  | 

#### 4.2.5. Dataset Overview

After filtering, our curated dataset contains $14\,998$ unique, non-merge commits that modify at least one Java file. Of these, $3907$ are labeled as agentic refactoring commits (those with explicit refactoring intent in their messages) and the remaining $11\,091$ commits are categorized as Other Agentic Commits.

These $14\,998$ commits originate from $12\,256$ PRs across $1613$ repositories. Among these PRs, $11\,504$ (93.9%) are closed and $10\,645$ (86.9%) are merged. This high merge rate indicates that most agentic contributions were integrated into their respective projects, demonstrating substantial acceptance of agent-generated code. Regarding agent participation, the distribution across the agents is shown in Table [3](#S4.T3). Although the AIDev dataset includes five coding agents, GitHub Copilot produced no Java-modifying, non-merge commits after our filtering and is therefore absent from our final dataset.
The data reveal that OpenAI Codex dominates the dataset, accounting for 89.3% of all commits and 94.3% of PRs. Devin and Cursor contribute 5.7% and 4.4% respectively, while Claude Code accounts for only 0.6% of the commits analyzed.

## 5. Results

In this section, we provide the motivation, approach, and findings for each of our research questions. Figure [2](#S3.F2) provides an overview of our study design.

### 5.1. $RQ_{1}$: How prevalent is refactoring in agentic commits?

#### 5.1.1. Motivation

Agentic coding is transitioning from a novelty to an everyday practice, yet little is known about the extent of refactoring performed by these agents in real-world projects. Although agentic coding tools promise to act as autonomous collaborators rather than mere code generators ([Hassan et al., 2025](#bib.bib51)), most research has focused on their ability to create new features or fix bugs. Their role in software maintenance, particularly refactoring, remains largely unexplored. Before assessing the quality or types of refactorings agents perform, we must first establish a baseline: Is agentic refactoring a significant real-world activity or merely an incidental byproduct of other development tasks? Quantifying its frequency is the first step toward understanding whether these agents contribute to refactoring.

#### 5.1.2. Approach

We record the distribution of refactoring instances for the collected $14\,998$ commits. Both groups in this comparison consist exclusively of agentic commits: *Agentic Refactoring* denotes commits with both detected refactoring and explicit refactoring intent in the commit message, while *Other Agentic Commits* denotes all remaining agentic commits. No human commits are included. To determine whether the distributions of refactoring instances differ between these two groups, we perform the Mann–Whitney U test ([Mann and Whitney, 1947](#bib.bib63)), a non-parametric rank-based test that does not assume normality, at a significance level of $\alpha=0.05$.
We also compute Cliff’s delta $d$ ([Long et al., 2003](#bib.bib64)) effect size to quantify the difference based on the following thresholds ([Romano et al., 2006](#bib.bib65)):

| (1) |  | $$ \mathrm{Effect\ size}=\left\{\begin{array}[]{ll}negligible,&\mathrm{if}\ \|d\|\leq 0.147\\ small,&\mathrm{if}\ 0.147<\|d\|\leq 0.33\\ medium,&\mathrm{if}\ 0.33<\|d\|\leq 0.474\\ large,&\mathrm{if}\ 0.474<\|d\|\leq 1\\ \end{array}\right. $$ |  | 

We examine refactoring activity from two complementary perspectives: (i) aggregate prevalence, based on the total number of detected refactoring instances in each group, and (ii) per-commit prevalence, based on the distribution of refactoring instances per commit.

|  | # Commits (%) | # Instances (%) | 
|---|---|---|
| Agentic Refactoring | $3907$ (26.1%) | $32\,611$ (63.4%) | 
| Other Agentic Commits | $11\,091$ (73.9%) | $18\,801$ (36.6%) | 
| Total | $14\,998$ (100%) | $51\,412$(100%) | 

#### 5.1.3. Findings

Finding #1: Refactoring is common in agentic software development and often appears even without explicit intent.
As shown in Table [4](#S5.T4), commits with explicit refactoring intent account for 26.1% ($3907$ out of $14\,998$) of all commits and contain $32\,611$ detected refactoring instances. However, the remaining $11\,091$ other agentic commits (whose messages do not explicitly indicate refactoring) contain $18\,801$ detected refactoring instances (36.6% of all instances). This pattern suggests tangled commits: while implementing a feature or fixing a bug, agents also refactor nearby code (e.g., rename variables, extract small helpers) within the same commit.

Finding #2: When agents state refactoring intent, they perform significantly more refactoring instances than other agentic commits.
Figure [3](#S5.F3) shows the distribution of refactoring instances per commit in agentic refactoring and other agentic commits. Although other agentic commits contribute many refactoring instances in aggregate, those instances are spread across a much larger number of commits. The result of the Mann–Whitney $U$ test shows that the difference is statistically significant ($p\leq 0.001$). In addition, the result of Cliff’s delta ($d=0.838$) indicates a large effect size. The results suggest that when AI agents explicitly signal refactoring intent, they perform more concentrated and substantial restructuring activities. In contrast, when refactoring is unacknowledged, it tends to appear sporadically or incidentally as part of broader code modifications, such as feature implementation or bug fixing.

### 5.2. $RQ_{2}$: What are the common types of agentic refactoring?

#### 5.2.1. Motivation

Refactoring encompasses a wide range of activities, from simple, localized cleanups such as variable renaming to complex, structural transformations like splitting a class or extracting a superclass, which require a comprehensive understanding of the software system. Analyzing the types of refactorings performed by agents serves as a direct indicator of their sophistication and capability. Are these agents merely acting as “code janitors,” automating low-level syntactic cleanup, or are they beginning to function as “software architects,” executing deep structural design improvements essential for long-term maintainability? By comparing the distribution of agentic refactoring types with known human refactoring patterns ([Horikawa et al., 2025](#bib.bib32)), this RQ establishes the first empirical profile of agentic refactoring and evaluates its current level of maturity.

#### 5.2.2. Approach

For each detected refactoring instance, RefactoringMiner provides its specific type from a set of 103 distinct operations. We record these types for all Agentic Refactoring instances in our dataset. To understand the structural impact of these operations, we classify them using the three abstraction levels proposed by Murphy-Hill et al. ([Murphy-Hill et al., 2012](#bib.bib50)). Since Murphy-Hill et al. ([Murphy-Hill et al., 2012](#bib.bib50)) did not classify all 103 refactoring types detected by RefactoringMiner, we extended their classification framework by applying the same criteria to categorize the remaining refactoring types. RefactoringMiner’s official benchmark evaluation<sup>12</sup><sup>12</sup>
                12
                
                
                
              [https://github.com/tsantalis/RefactoringMiner/blob/master/documentation/accuracy.md](https://github.com/tsantalis/RefactoringMiner/blob/master/documentation/accuracy.md) demonstrates uniformly high precision and recall across all abstraction levels, ensuring that our results are not skewed by detection bias. Specifically, we classified each refactoring based on whether it modifies (i) only signatures or interfaces, (ii) both signatures and code blocks, or (iii) only internal code blocks. The details of the three abstraction levels of refactoring instances are as below:

- • 
High-level (58 types): Refactorings that only change the signatures of classes, methods, or fields without modifying internal code blocks. These alter the public interface and often require changes to calling code (e.g., Rename Method, Add Parameter, Move Class, Change Method Access Modifier).
- • 
Medium-level (21 types): Refactorings that change both signatures and code blocks, bridging internal logic and external structure (e.g., Extract Method, Inline Method, Move and Inline Method, Change Attribute Type).
- • 
Low-level (24 types): Refactorings confined exclusively to code blocks (typically within method bodies) that are not visible externally (e.g., Rename Variable, Change Variable Type, Extract Variable, Replace Anonymous with Lambda).

The complete mapping of all 103 refactoring types to abstraction levels is available in our replication package.<sup>13</sup><sup>13</sup>
                13
                
                
                
              [https://github.com/Mont9165/Agent\_Refactoring\_Analysis/blob/main/Refactoring\_Level\_Classification.md](https://github.com/Mont9165/Agent_Refactoring_Analysis/blob/main/Refactoring_Level_Classification.md) We then calculate the distribution of refactoring instances across these three levels. To identify differences between agent and human behavior, we compare our results with human refactoring patterns reported in prior work ([Horikawa et al., 2025](#bib.bib32)), mapping the human-driven instances to the same three-level framework for a direct comparison.

| Abstraction Level | % Agentic Refactoring | % Human Refactoring ( [Horikawa et al., 2025](#bib.bib32)) | 
|---|---|---|
| High-level | 52.4% | 54.9% | 
| Medium-level | 20.0% | 20.7% | 
| Low-level | 27.6% | 24.4% | 

#### 5.2.3. Findings

Finding #3: Agents and humans refactor at similar abstraction levels, with agents leaning slightly toward low-level edits.
As shown in Table [5](#S5.T5), the ranking of abstraction levels is the same for both agents and humans: high-level refactorings are the most frequent, followed by low-level and then medium-level.
The proportions are also close. High-level refactorings account for 52.4% of agentic and 54.9% of human refactorings, and medium-level refactorings for 20.0% and 20.7%. The largest gap is in low-level refactorings (27.6% vs. 24.4%).
This small difference may arise because low-level refactorings (e.g., Rename Variable, Change Variable Type) need less system context than high-level ones, or because developers delegate routine cleanup to agents.

| Abstraction Level | Actor | Refactoring Type | % Instances | 
|---|---|---|---|
| High-level | Agent | Move Class | 5.3% | 
|  |  | Rename Attribute | 5.3% | 
|  |  | Rename Method | 4.3% | 
|  | Human | Add Method Annotation | 5.8% | 
|  |  | Rename Method | 4.4% | 
|  |  | Add Parameter | 4.3% | 
| Medium-level | Agent | Change Attribute Type | 4.6% | 
|  |  | Change Parameter Type | 3.6% | 
|  |  | Extract Method | 3.0% | 
|  | Human | Change Parameter Type | 6.2% | 
|  |  | Change Return Type | 4.7% | 
|  |  | Change Attribute Type | 3.5% | 
| Low-level | Agent | Rename Variable | 7.6% | 
|  |  | Change Variable Type | 6.8% | 
|  |  | Rename Parameter | 4.9% | 
|  | Human | Change Variable Type | 7.7% | 
|  |  | Rename Variable | 3.3% | 
|  |  | Rename Parameter | 3.0% | 

Finding #4: Agents and humans share a common focus on low-level refactoring operations but diverge in high-level refactoring. Table [6](#S5.T6) highlights distinct agentic priorities in the most common refactoring operations.
At the low level, Rename Variable, Change Variable Type, and Rename Parameter are the top three operations for both agents and humans. Together they account for 19.3% of agentic and 14.0% of human refactoring instances. The gap comes from Rename Variable (7.6% vs. 3.3%) and Rename Parameter (4.9% vs. 3.0%), while Change Variable Type is slightly less frequent for agents (6.8% vs. 7.7%).
At the high level, however, their focus diverges.
Rename Method appears in both top-three lists (4.3% vs. 4.4%), but the two most frequent agentic high-level types are Move Class (5.3%) and Rename Attribute (5.3%), whereas Add Method Annotation (5.8%) and Add Parameter (4.3%) appear only in the human top three. Move Class is concentrated in a few commits: it appears in 136 agentic refactoring commits, and five of them contain 32% of its instances.
At the medium level, both agents and humans frequently perform Change Attribute Type and Change Parameter Type. Beyond these two, agents most often apply Extract Method (3.0%) and humans Change Return Type (4.7%).

### 5.3. $RQ_{3}$: What is the purpose of agentic refactoring?

#### 5.3.1. Motivation

In human-driven development, intent is central. Developers refactor code to improve readability, reduce coupling in preparation for new features, or make the code easier to test ([Kim et al., 2014](#bib.bib11)). But what about agents? This research question explores the motivations behind agentic refactoring. Do developers use agents as proactive “quality partners” to enhance maintainability and reduce technical debt, or as tactical assistants for short-term objectives such as improving the readability of a specific method? Understanding these motivations is essential for aligning agent behavior with developer expectations.

#### 5.3.2. Approach

To analyze why agentic refactoring is performed, we classify the primary motivation of each Agentic Refactoring commit using the ten motivation categories defined by Kim et al. ([Kim et al., 2014](#bib.bib11)) (e.g., maintainability, readability, testability, legacy code etc.), which include logical mismatch. Because logical mismatch corresponds to bug fixing rather than a refactoring motivation, we exclude commits assigned to it and report the motivation distribution over the remaining nine refactoring-motivation categories; for consistency we also rerank the human refactoring data reported by Kim et al. ([Kim et al., 2014](#bib.bib11)) accordingly. In our data, GPT-4.1-mini labeled 446 of the $3907$ agentic refactoring commits (11.4%) as logical mismatch; the distribution in Figure [4](#S5.F4) is therefore reported over the remaining $3461$ commits.
The classification uses the Pull Request title, commit message, and detected refactoring types as input.
Due to the large sample size of the collected Agentic Refactoring commits, we leverage GPT-4.1-mini to automatically categorize each commit. We selected GPT-4.1-mini for its cost efficiency (see Section 4.2.2), while its classification reliability is confirmed by the human validation reported below (Cohen’s $\kappa$ = 0.77).

To validate the reliability of the automatic classification, two inspectors (each with eight years of programming experience) independently label a stratified sample of 100 Agentic Refactoring commits, comprising ten commits from each of the ten categories the classifier can output, including logical mismatch. For the reliability analysis we retain the commits whose labels in the respective comparison both fall within the nine refactoring-motivation categories, excluding those where at least one label is logical mismatch (i.e., bug fixing rather than a refactoring motivation) or could not be assigned to a refactoring-motivation category; this yields 79 valid label pairs per comparison. We assess inter-rater reliability using Cohen’s $\kappa$ coefficient ([Emam, 1999](#bib.bib52)), which measures the degree of agreement between annotators.
As shown in Table [7](#S5.T7), inter-rater agreement between the two human annotators is almost perfect (Cohen’s $\kappa$ = 0.83). Disagreements are resolved through discussion with another inspector (eighteen years of programming experience), producing the final reference labels. We then compare the GPT-4.1-mini annotations with these adjudicated human labels. Agreement between GPT-4.1-mini and the adjudicated human labels is substantial (Cohen’s $\kappa$ = 0.77), indicating that GPT-4.1-mini provides reliable motivation classification for large-scale empirical analysis.

We inspected all 16 disagreements among the 79 valid label pairs in the GPT–human comparison, and found three recurring patterns. First, the most common confusion was between maintainability and readability (3 cases). These categories overlap conceptually. For example, removing unused parameters can reduce future maintenance effort and improve code clarity. GPT-4.1-mini selected maintainability, while the annotators judged readability to be the primary motivation. Second, legacy code accounted for the largest number of missed labels (5 cases). These cases often involved modernization commits, such as “Update Spring Boot to 3.4.5 and fix deprecation warnings” or “Refactor callbacks to avoid lambdas” for Java 7 compatibility. GPT-4.1-mini labeled the mechanism of the change, such as dependency or repurpose/reuse. The annotators instead labeled the underlying motivation: addressing outdated code. Third, maintainability often served as a broad catch-all category. It appeared in 6 of the 16 GPT–human disagreements, and in 8 of the 12 disagreements between the two human annotators. These confusions occurred between closely related categories. Therefore, they do not affect the main RQ3 finding. Internal quality concerns, especially maintainability and readability, motivate most agentic refactorings.

| Comparison | Cohen’s $\kappa$ | Accuracy | Macro F1 | 
|---|---|---|---|
| Human vs Human | 0.83 | 0.85 | 0.85 | 
| GPT-4.1-mini vs Human | 0.77 | 0.80 | 0.80 | 

[Kim et al., 2014](#bib.bib11))

#### 5.3.3. Findings

Finding #5: Agentic refactoring is primarily driven by maintainability, a purpose that is far more dominant for agents than for humans.
As shown in Figure [4](#S5.F4), maintainability is the primary driver for more than half (52.5%) of the agentic refactoring commits with an identified refactoring motivation. This differs sharply from human refactoring patterns, where maintainability is a much less frequent purpose (11.7%) ([Kim et al., 2014](#bib.bib11)). The second most common agent purpose is readability (28.1%), which aligns closely with the most common human purpose (25.7%), establishing it as a shared, core priority for both. Together, these two categories account for over 80% of all agentic refactoring purposes.
This suggests that developers primarily dispatch agents to perform day-to-day codebase care (e.g., cleanups and consistency edits) rather than to pursue broader design goals.

Finding #6: Agentic refactoring rarely targets design-level improvements, such as duplication or reuse. In sharp contrast to the focus on maintainability, motivations related to design-level refactoring are much less frequent in agentic commits than in human ones. For example, duplication (1.1%) and repurpose/reuse (4.6%) are far less common motivations for agents than for humans. This is the inverse of human-driven refactoring, where these two categories are prominent (13.7% and 12.9%, respectively), indicating that humans frequently refactor to improve modularity and reduce redundancy. This pattern suggests that current agents focus on localized quality cleanup rather than complex, system-wide restructuring.

Finding #7: Corrective refactoring occasionally appears but remains a secondary purpose.
A small fraction of agentic refactoring is motivated by corrective concerns. This includes addressing code that is hard to debug (1.9%) or dealing with legacy code (2.0%). These instances often involve tactical improvements rather than deep bug fixing, such as adding logging (e.g., log.debug()) where it was missing,<sup>14</sup><sup>14</sup>
                14
                
                
                
              [https://github.com/Braindeiko01/CRduels/commit/4ea01106f0cf74663cf1dccecd94b4475e11794a](https://github.com/Braindeiko01/CRduels/commit/4ea01106f0cf74663cf1dccecd94b4475e11794a) or modernizing code by upgrading Java versions (e.g., from Java 7 to Java 17).<sup>15</sup><sup>15</sup>
                15
                
                
                
              [https://github.com/BrettMiller99/ReallyOldJavaProject/commit/daea563191184899891e1a1c66e2e8d60fa94bfc](https://github.com/BrettMiller99/ReallyOldJavaProject/commit/daea563191184899891e1a1c66e2e8d60fa94bfc) These cases are present but clearly not the primary use case for agents.

### 5.4. $RQ_{4}$: To what extent does agentic refactoring affect code quality?

#### 5.4.1. Motivation

The core premise of refactoring is to improve a software system’s internal code quality. However, decades of research on human refactoring indicate that this outcome is not guaranteed. Refactorings may fail to remove existing smells or even introduce new ones ([Cedrim et al., 2017](#bib.bib42); [Bavota et al., 2012](#bib.bib49)), and similar uncertainty applies to agents. To justify delegating maintenance tasks to AI agents, we need quantitative evidence of their impact. This RQ shifts the focus from intent to outcomes. By analyzing established software metrics and comparing smell counts before and after agentic commits, we provide the first empirical assessment of whether agentic refactoring improves code quality.

#### 5.4.2. Approach

To quantify the impact of refactoring on internal code quality, we extract object-oriented metrics and design smells before and after each Agentic Refactoring commit using DesigniteJava ([Sharma, 2024](#bib.bib10)). We select DesigniteJava because it is widely used in empirical software engineering research (e.g., ([Shah et al., 2023](#bib.bib5); [Lambaria and Cerný, 2022](#bib.bib4))). As it performs static analysis directly on source code, it ensures consistent metric extraction across heterogeneous projects without requiring build configuration. The tool computes class- and method-level metrics commonly used in software quality assessment ([Chidamber and Kemerer, 1994](#bib.bib7)), including size (Lines of Code), complexity (Cyclomatic Complexity, Weighted Methods per Class), coupling (Fan-in, Fan-out), cohesion (Lack of Cohesion in Methods), and inheritance depth (Depth of Inheritance Tree). DesigniteJava also detects 27 design and implementation smells (e.g., Long Method, Complex Method, Cyclic Dependency), enabling a multi-perspective analysis of code maintainability.

In addition, we evaluate before-and-after changes ($\Delta=\textit{after}-\textit{before}$) in internal code quality metrics detected by DesigniteJava for agentic refactoring commits. Before-and-after changes (i.e., values of $\Delta$) are aggregated along two dimensions: (1) the abstraction level (high, medium, low) of the refactoring instances, and (2) the type of the refactoring instances. To study the differences in these code-quality metrics changes, we perform the Wilcoxon signed-rank test ([Wilcoxon, 1945](#bib.bib23)), a non-parametric paired test that does not assume normality, with $p$-values adjusted via the Benjamini-Hochberg FDR ([Glueck et al., 2008](#bib.bib8)).
We also compute the rank-biserial effect size to quantify the difference. For cross-group comparisons (e.g., levels or refactoring types), we use Kruskal–Wallis tests ([Daniel, 1990](#bib.bib43)) with FDR adjustment, and when relevant, we summarize post-hoc contrasts descriptively. Given the skewed distributions of deltas, we also report the median values of these before-and-after changes.

#### 5.4.3. Findings

Finding #8: Changes in design and implementation smell counts are statistically significant but practically negligible.
Figure [5](#S5.F5) shows that the before-and-after distributions for both design and implementation smells almost completely overlap, indicating no visible shift in typical smell levels.
Consistently, the median values remain virtually identical for both smell categories (Design: before 77.50, after 77.50; Implementation: before 355.50, after 356.00), resulting in a median $\Delta$ of 0.00 in both cases.
Note that the median of pairwise differences can be zero even when the group-level medians differ slightly (e.g., Implementation Smell before: 355.50, after: 356.00), because the median $\Delta$ is computed per commit rather than as the difference of aggregate medians.
Although the Wilcoxon signed-rank test detects a statistically significant difference (FDR-adjusted $p\leq 0.001$), the effect sizes are negligible (rank-biserial $r=-0.027$ and $-0.026$). The mean $\Delta$ values ($-6.63$ and $-32.85$ for Design and Implementation Smells, respectively) suggest that meaningful reductions occur only in a small subset of commits.
In other words, AI agents can remove smells, but they do so inconsistently, and improvements are concentrated in exceptional cases rather than being routine.

Finding #9: Agentic-refactoring commits show small improvements in structural metrics, whereas changes in smell counts are statistically detectable but not practically meaningful.
As summarized in Table [8](#S5.T8), several class-level metrics improve after agentic refactoring, with the largest reductions concentrated in medium-level changes: Class LOC (median $\Delta=-15.25$), WMC (median $\Delta=-2.07$), Fan-Out (median $\Delta=-0.02$), and Fan-In (median $\Delta=-0.01$). These results indicate that agentic refactoring tends to simplify structural complexity (size and coupling) more reliably than it eliminates higher-level smell patterns.

Finding #10: Quality improvements are largest for medium-level refactorings, modest for low-level edits, and minimal for high-level signature-only changes.
Grouping by abstraction level, medium-level refactorings produce the most consistent gains (Table [8](#S5.T8)):
Class LOC and WMC drop meaningfully (medians $\Delta=-15.25$ and $-2.07$), and method-level LOC decreases (median $\Delta=-1.79$).
Low-level edits also reduce method LOC (median $\Delta=-0.42$) but show a slight increase in method cyclomatic complexity (median $\Delta=+0.08$), suggesting that these localized edits shorten methods without reducing their decision complexity.
High-level signature-only changes show near-zero medians across most metrics, which is consistent with interface adjustments rather than structural simplification.
Kruskal–Wallis tests across levels (FDR-adjusted) support these differences at $\alpha=0.05$.

| Metric | Low-level | Medium-level | High-level | 
|---|---|---|---|
|  | (code block) | (signature + block) | (signature) | 
| Class-Level – Depth of Inheritance Tree | – | 0.00 | 0.01 | 
| Class-Level – Fan-Out | – | -0.02 | 0.00 | 
| Class-Level – Fan-In | – | -0.01 | 0.00 | 
| Class-Level – Number of Methods | – | -0.10 | 0.01 | 
| Class-Level – Weighted Methods per Class | – | -2.07 | 0.03 | 
| Class-Level – Lines of Code | – | -15.25 | 0.10 | 
| Method-Level – Parameter Count | 0.00 | 0.01 | 0.11 | 
| Method-Level – Cyclomatic Complexity | 0.08 | 0.01 | 0.00 | 
| Method-Level – Lines of Code | -0.42 | -1.79 | 0.11 | 
| – Not applicable: Class-Level metrics are not measured for Low-level (code block) refactorings. |  |  |  | 

Finding #11: Structural refactorings (e.g., decomposition and modularization) show the largest metric reductions.
Analyzing median metric deltas by refactoring type reveals that refactorings introducing new structure or decomposing responsibilities have the largest metric reductions. For example, Extract Subclass yields large median reductions in Class LOC ($\Delta=-87.5$) and WMC ($\Delta=-11.5$), while Split Class similarly reduces Class LOC ($\Delta=-16.0$) and WMC ($\Delta=-4.0$).<sup>16</sup><sup>16</sup>
                16
                
                
                
              [https://github.com/Mont9165/Agent\_Refactoring\_Analysis/blob/main/outputs/designite/group\_heatmaps/refactoring\_heatmap\_sar\_median\_delta.csv](https://github.com/Mont9165/Agent_Refactoring_Analysis/blob/main/outputs/designite/group_heatmaps/refactoring_heatmap_sar_median_delta.csv)
These refactorings improve modularity and reduce class-level complexity by distributing responsibilities across more cohesive components. However, the metrics reported in this study are measured at the class level rather than the project level. While extraction-based refactorings reduce metrics for the refactored class (e.g., Extract Subclass yields Class LOC $\Delta$ = $-$87.5 and WMC $\Delta$ = $-$11.5), they necessarily create new classes that inherit part of the original complexity. Moreover, distributing logic across more classes can increase inter-class coupling (e.g., Fan-Out), even as intra-class complexity decreases. Fowler ([Fowler, 1999](#bib.bib21)) argues that distributing responsibilities across smaller, cohesive classes improves maintainability because each unit becomes independently comprehensible and testable, even if aggregate complexity does not decrease. Nevertheless, without project-level aggregation of metrics (e.g., summing WMC or LOC across all classes before and after the commit), our results should be interpreted as improvements to the refactored entity rather than definitive evidence of net project-level quality gains.
In contrast, refactorings that preserve overall structure, such as signature adjustments or local rewrites, tend to produce smaller metric shifts.
These findings indicate that the impact of agentic refactoring is strongly influenced by refactoring type. While structural decomposition refactorings drive measurable improvements, localized edits have a more limited effect on structural indicators.

Finding #12: Not all refactoring types improve measured metrics; some primarily support clarity or evolution.
Several high-frequency agentic refactoring types (e.g., identifier renames and type changes) show negligible before-and-after change in the analyzed structural metrics after FDR correction.
This does not imply that these refactorings lack value; rather, their main benefits (e.g., readability, naming consistency, API clarity) are not captured by the selected design-level indicators.
By contrast, transformation types with both semantic and structural effects may yield mixed outcomes.
For example, Move And Inline Method tends to reduce method LOC (median $\Delta=-0.5$) but can leave cyclomatic complexity unchanged, or even increase it slightly when logic is redistributed across helper methods.
These observations emphasize that metric-based evaluation should be interpreted together with developer intent (see Section [5.3](#S5.SS3)). Agentic refactoring is often used for code consistency and comprehension.

## 6. Implications

In this section, we discuss the implications of our findings for researchers, developers, and coding agent builders.

### 6.1. Implications for Researchers

Researchers should investigate the hidden burden of implicit refactoring on development workflows.
Section [5.1](#S5.SS1) shows that more than a third of refactoring instances (36.6%) occur in commits without explicit refactoring intent, which may indicate tangled changes. This suggests that agents frequently perform refactorings as a side effect of other tasks. Such tangling can increase review effort, as developers must validate both the primary task (e.g., a feature) and the incidental refactorings to ensure behavior is preserved. Prior work indicates that developers want to verify logic preservation ([Sergeyuk et al., 2025](#bib.bib45)), so a high volume of implicit refactoring could lengthen reviews and reduce trust. Future work should quantify this burden by analyzing review comments, merge latency, and revert rates for commits with implicit refactoring.

Researchers should create benchmarks for high-level refactoring.
Section [5.2](#S5.SS2) reports how often agents perform each type of refactoring, but not whether they perform it correctly. Assessing this requires curated benchmarks and gold standards for architectural refactorings (e.g., Extract Class, Introduce Parameter Object, Move Class). These refactorings change interfaces and require coordinated updates to callers, so correctness is harder to judge from frequency alone. Datasets should include ground-truth intent, behavior-preserving tests, and expected post-conditions (reduced WMC/fan-out).

Researchers should study the disconnect between agentic refactoring and measured quality outcomes.
The majority (86.9%) of agentic PRs are merged into the software projects (Section [4.2.5](#S4.SS2.SSS5)), and our findings reveal that 26.1% of agentic commits contain explicitly stated refactoring (Section [5.1](#S5.SS1)). However, traditional quality metrics show minimal improvement (Section [5.4](#S5.SS4)). Researchers should investigate this gap to understand whether these agentic refactorings (e.g., renaming variables) provide tangible benefits to human developers, such as improved comprehension or reduced cognitive load, or whether agents are engaging in low-value “code churn” that fails to address deeper structural issues.
In particular, our findings reveal that while 52.5% of agentic refactoring is motivated by maintainability (Section 5.3), the frequently occurring low-level operations primarily improve naming consistency and readability rather than structural metrics (Section 5.4). This suggests that current agents interpret “maintainability” narrowly as code-level cleanup rather than structural simplification. The benefits of these refactorings (e.g., reduced cognitive load, improved naming clarity) may be real but are not captured by traditional design-level indicators such as WMC or Fan-Out.

Researchers should validate long-term quality outcomes through longitudinal analysis for agentic refactorings.
Our before-and-after analysis of structural metrics (Section [5.4](#S5.SS4)) shows small but statistically significant improvements, particularly for medium-level changes (e.g., Class LOC median $\Delta=-15.25$, WMC median $\Delta=-2.07$). The core premise of refactoring, however, concerns long-term evolvability and maintainability. Although agentic refactoring is overwhelmingly motivated by maintainability (Section [5.3](#S5.SS3)), it does not consistently reduce design and implementation smells. Researchers should assess whether these structural gains translate into long-term benefits by conducting longitudinal studies that track defect density, post-release defects, and effort for future modifications.

### 6.2. Implications for Developers

Developers should demand commit hygiene from coding agents so that refactoring does not silently accompany behavioral changes.
More than a third of all detected refactoring instances (36.6%) appear in commits whose messages do not mention refactoring (Section [5.1](#S5.SS1)), indicating that agents frequently mix renames and restructurings with feature or bug-fix changes. Such tangled changes bias code review and downstream analyses ([Herzig et al., 2016](#bib.bib71)) and make behavior preservation harder to verify. Developers should therefore (i) instruct agents through agent context files ([Chatlatanagulchai et al., 2026](#bib.bib72)) to avoid out-of-scope refactoring, (ii) require cleanup changes to be isolated in separate commits or PRs, and (iii) highlight mixed-intent changes during review, potentially using automatic changeset decomposition ([Barnett et al., 2015](#bib.bib73)).

Developers should use coding agents for routine cleanup tasks.
Section [5.2](#S5.SS2) shows that agentic refactoring contains a slightly larger share of low-level refactorings than human refactoring (27.6% vs. 24.4%), and that its two most common operations are Rename Variable (7.6%) and Change Variable Type (6.8%). These findings suggest that developers already use current agents for localized, repetitive maintenance tasks, including naming cleanup, type modernization, and consistency updates.
Prior studies have shown that software maintenance often involves recurring change patterns that can be automated ([Dilhara et al., 2022](#bib.bib74); [Nguyen et al., 2013](#bib.bib75)). Coding agents may therefore reduce the manual effort required to apply these changes across a repository. For example, agents can conduct periodic repository-wide consistency sweeps, allowing developers to focus on reviewing and validating the resulting changes.

Developers may obtain the greatest value from coding agents by identifying architectural hotspots and assigning the restructuring to agents.
Not all refactoring types are equally effective (Section [5.4](#S5.SS4)). Structural refactorings (such as Extract Subclass and Split Class) produce larger reductions in class size and complexity than common low-level edits. This finding suggests an effective collaborative workflow in which developers identify maintainability problems and agents carry out the mechanical restructuring. In this workflow, developers provide the diagnosis, while agents perform the implementation.

### 6.3. Implications for Coding Agent Builders

Coding agent builders should equip agents with specialized tools to autonomously detect and fix design flaws.
A key finding in Section [5.4](#S5.SS4) is that agentic refactoring fails to consistently reduce the overall count of design and implementation smells (median $\Delta$ of 0.00). This suggests agents are overlooking specific flaws. Prior work on RepairAgent ([Bouzenia et al., 2025](#bib.bib20)) demonstrates that agents equipped with task-specific tools can autonomously perform automated program repair by gathering information, applying patches, and validating candidate fixes. Similarly, agentic refactoring could be improved by equipping agents with refactoring-specific analysis tools (e.g., DesigniteJava) and feeding their findings back into the planning loop. This setup would allow the agent to actively seek out smells, verify improvements, and autonomously decide when to run a smell scan, retrieve metrics, and re-invoke transformations.

Coding agent builders should generate the evidence reviewers need to assess both safety and value.
A generated refactoring should arrive with evidence for two distinct claims: that it preserves observable behavior, and that it advances the stated quality objective. For the former, agents should report the affected APIs and callers, the tests, builds, and differential checks that were run, and the scope and limitations of those checks. For the latter, agents should report how the indicators that match the stated objective changed; for readability-oriented changes, this evidence should not rely on structural metrics alone, which can remain unchanged even when clarity improves (Section [5.4](#S5.SS4)). When mixed changes cannot be avoided, the review interface should group behavior-changing edits separately from restructuring. Industrial deployments of automatic program repair follow the same approach: generated patches are integrated into existing CI and review workflows ([Marginean et al., 2019](#bib.bib66); [Urli et al., 2018](#bib.bib69); [Williams et al., 2024](#bib.bib70)), and practitioners assess them more readily when test reports, coverage information, and patch explanations accompany them ([Noller et al., 2022](#bib.bib67); [Winter et al., 2023](#bib.bib68)).

## 7. Threats to Validity

In this section, we discuss the threats to validity of our study about agentic refactoring.

### 7.1. Internal Validity

Threats to internal validity concern potential confounding factors that could influence our results. First, our study relies on automated tools for data analysis. RefactoringMiner ([Tsantalis et al., 2022](#bib.bib9); [Alikhanifard and Tsantalis, 2025](#bib.bib6)), which we used to identify refactoring operations, is known to produce both false positives and false negatives.
We classified RefactoringMiner’s 103 refactoring types into three abstraction levels based on their structural impact (Section 5.2.2): the catalog contains 58 high-level, 21 medium-level, and 24 low-level types, indicating that the catalog is not biased toward low-level operations. Furthermore, RefactoringMiner’s benchmark evaluation<sup>17</sup><sup>17</sup>
              17
              
              
              
            [https://github.com/tsantalis/RefactoringMiner/blob/master/documentation/accuracy.md](https://github.com/tsantalis/RefactoringMiner/blob/master/documentation/accuracy.md) shows uniformly high precision and recall across all abstraction levels, confirming that detection accuracy does not vary substantially between levels. The same tool is applied to both agentic and human refactoring data ([Horikawa et al., 2025](#bib.bib32)), ensuring that any residual detection characteristic affects both groups.
Similarly, DesigniteJava ([Sharma, 2024](#bib.bib10)), used for calculating code quality metrics, has its own inherent limitations. Although these tools are standard in empirical software engineering, their potential inaccuracies could have affected our quantitative results.
Second, for RQ3, we employed GPT-4.1-mini to automatically classify the purpose of each refactoring. To mitigate the risk of misclassification, two authors manually labeled a stratified sample of 100 refactoring commits (79 valid label pairs). Agreement between the two annotators was almost perfect (Cohen’s $\kappa$ = 0.83), and agreement between GPT-4.1-mini and the adjudicated human labels was substantial (Cohen’s $\kappa$ = 0.77). This suggests that while the automated classification may not be perfect, the resulting distribution of purposes is largely reliable.
Third, our identification of refactoring intent relies on keyword matching in commit messages (Section 4.2.4). This approach may miss commits with unstated refactoring intent and may include false positives from broad patterns (e.g., “fix\*” matching bug-fix commits that incidentally contain refactoring keywords). We mitigate this risk by requiring both keyword match and RefactoringMiner detection, but acknowledge that intent classification remains approximate. Consistent with this, GPT-4.1-mini judged 446 of the $3907$ agentic refactoring commits (11.4%) to be motivated by bug fixing rather than refactoring; these are excluded from the RQ3 motivation distribution.

### 7.2. Construct Validity

Construct validity threats relate to the alignment between our theoretical constructs and our measurements. First, our code quality analysis in $RQ_{4}$ measures metrics at the class level using DesigniteJava. Extraction-based refactorings (e.g., Extract Subclass, Split Class) reduce metrics for the refactored class but may redistribute rather than eliminate complexity at the project level. A project-level evaluation that aggregates metrics across all affected classes before and after each commit would be needed to fully assess the net impact on overall system quality. We leave this for future work.

Additionally, our analysis focuses on commits as the unit of analysis, as dictated by RefactoringMiner’s requirement to compare consecutive revisions. While we classify refactoring purpose (RQ3) using the PR title, commit message, and detected refactoring types, richer development artifacts such as PR discussions, code review comments, and issue context are not systematically analyzed. These artifacts could reveal, for example, whether a refactoring was initiated by the developer or autonomously by the agent. For RQ1, RQ2, and RQ4, the relevant data are the code changes and metrics themselves, which are not influenced by these artifacts. Nevertheless, qualitative analysis of PR discussions represents an important avenue for future research.

A primary concern is the definition of an agentic commit. We identify such commits based on keywords and author information from the commit history. However, it is challenging to ascertain the precise extent of human intervention; developers may modify, accept, or reject parts of AI-generated code before committing. To acknowledge this ambiguity, we explicitly frame our study as an analysis of human-AI collaborative refactoring rather than purely autonomous AI contributions.

### 7.3. External Validity

Threats to external validity concern the generalizability of our findings.
Our study is based on the AIDev dataset ([Li et al., 2025](#bib.bib12)), which involves a two-fold selection: it covers (i) only publicly available open-source software (OSS) repositories on GitHub and (ii) among those, only projects in which AI coding agents had already been adopted at the time of data collection. Although our commit collection covers repositories regardless of star count (see Section [4.1](#S4.SS1)), our findings therefore characterize the current refactoring practice of early adopters in public OSS. Proprietary or enterprise codebases, whose development practices, coding standards, and review processes may differ significantly, are not represented.

Furthermore, our analysis was limited to Java due to the maturity of RefactoringMiner (F-score of 99.5%) and DesigniteJava for code quality metrics, as well as the need for direct comparison
with prior human refactoring results ([Horikawa et al., 2025](#bib.bib32)). While multi-language refactoring detectors exist (e.g., RefDiff ([Silva et al., 2021](#bib.bib30))), they support fewer refactoring types. The prevalence and characteristics of agentic refactoring may differ in languages with distinct ecosystems (e.g., Python, TypeScript). The same caution applies to languages that are co-executable with Java on the JVM (e.g., Kotlin, Scala, and Groovy): although they interoperate with Java bytecode, their idioms, such as Kotlin’s data classes and null-safety constructs or Scala’s functional style, change both the need for and the shape of common refactorings, and refactoring-detection tools with accuracy comparable to RefactoringMiner are not yet available for them. Our findings thus apply most directly to Java, and extending this study across languages, including JVM languages, is an important direction for future work.
Therefore, caution should be exercised when generalizing our results to other contexts.

## 8. Conclusion

This study provides the first large-scale empirical analysis of refactoring in agentic software development, examining $51\,412$ refactoring instances produced in agentic coding workflows across real-world open-source Java projects. Our findings clarify the current capabilities, typical uses, and impacts of agentic refactoring in open-source Java projects that have adopted AI coding agents.

Our empirical results show that refactoring is a common and intentional activity for AI agents, explicitly targeted in 26.1% of agentic commits. This demonstrates that agents actively participate in software maintenance, frequently engaging in restructuring activities beyond feature implementation or bug fixing. The stated motivations are overwhelmingly focused on internal code quality: maintainability (52.5%) and readability (28.1%) account for over 80% of cases.

Although high-level refactorings are the largest abstraction-level category overall, the two most frequent individual agentic operations are low-level, consistency-oriented edits (Rename Variable and Change Variable Type). Compared to human refactoring, agentic refactoring has a slightly smaller share of high-level refactorings (52.4% vs. 54.9%) and a slightly larger share of low-level ones (27.6% vs. 24.4%).

Our quantitative assessment shows that agentic refactoring produces statistically significant but small structural improvements, particularly for medium-level changes that combine signature and block modifications. These include measurable reductions in Class Lines of Code (Class LOC median $\Delta=-15.25$) and Weighted Methods per Class (WMC median $\Delta=-2.07$). However, despite the goal of improving quality, agents currently fail to consistently reduce the overall count of known design and implementation smells.

In conclusion, agentic coding tools serve as cleanup partners in open-source Java projects, frequently used for localized refactoring and consistency improvements that support long-term maintainability. Future work can extend this evaluation to other languages, ecosystems, and proprietary settings. Moreover, to realize the vision of agents as “software architects,” significant advancements are needed to enable autonomous, architecturally-aware restructuring that consistently addresses higher-level design smells.

###### Acknowledgements.

We gratefully acknowledge the financial support of JSPS KAKENHI grants (JP24K02921, JP25K03100, JP26H02500), as well as JST BOOST grant (JPMJBS2423), JST ACT-X grant (JPMJAX26MH), JST ASPIRE grant (JPMJAP2415), JST CREST grants (JPMJCR23M1, JPMJCR26X7), and JST FOREST grant (JPMJFR252W). We also acknowledge the support of the Natural Sciences and Engineering Research Council of Canada (NSERC).
## References

- 
A novel refactoring and semantic aware abstract syntax tree differencing tool and a benchmark for evaluating the accuracy of diff tools.
ACM Transactions on Software Engineering and Methodology (TOSEM) 34 (2), pp. 40:1–40:63.
External Links: [Document](https://dx.doi.org/10.1145/3696002) Cited by: [§2.2](#S2.SS2.p1.1), [§4.2.1](#S4.SS2.SSS1.p1.1), [§4.2.3](#S4.SS2.SSS3.p1.1), [§7.1](#S7.SS1.p1.1).
- 
Can refactoring be self-affirmed?: an exploratory study on how developers document their refactoring activities in commit messages.
In Proceedings of the 3rd International Workshop on Refactoring (IWOR’19),
pp. 51–58.
External Links: [Document](https://dx.doi.org/10.1109/iwor.2019.00017) Cited by: [Table 2](#S4.T2), [Table 2](#S4.T2.5).
- 
How to refactor this code? an exploratory study on developer-chatgpt refactoring conversations.
In Proceedings of the 21st IEEE/ACM International Conference on Mining Software Repositories (MSR’24),
pp. 202–206.
External Links: [Document](https://dx.doi.org/10.1145/3643991.3645081) Cited by: [§1](#S1.p2.1).
- 
Is github’s copilot as bad as humans at introducing vulnerabilities in code?.
Empirical Software Engineering (EMSE) 28 (6), pp. 129.
External Links: [Document](https://dx.doi.org/10.1007/s10664-023-10380-1) Cited by: [§2.4](#S2.SS4.p1.1).
- 
Helping developers help themselves: automatic decomposition of code review changesets.
In Proceedings of the 37th IEEE/ACM International Conference on Software Engineering (ICSE’15),
pp. 134–144.
External Links: [Document](https://dx.doi.org/10.1109/ICSE.2015.35) Cited by: [§6.2](#S6.SS2.p1.1).
- 
When does a refactoring induce bugs? an empirical study.
In Proceedings of the 12th IEEE International Working Conference on Source Code Analysis and Manipulation (SCAM’12),
pp. 104–113.
External Links: [Document](https://dx.doi.org/10.1109/scam.2012.20) Cited by: [§1](#S1.p2.1), [§2.2](#S2.SS2.p2.1), [§5.4.1](#S5.SS4.SSS1.p1.1).
- 
An experimental investigation on the innate relationship between quality and refactoring.
Journal of Systems and Software 107, pp. 1–14.
External Links: [Document](https://dx.doi.org/10.1016/j.jss.2015.05.024) Cited by: [§2.2](#S2.SS2.p2.1).
- 
Together we are better: llm, IDE and semantic embedding to assist move method refactoring.
In Proceedings of the 41st IEEE International Conference on Software Maintenance and Evolution (ICSME’25),
pp. 1–13.
External Links: [Document](https://dx.doi.org/10.1109/ICSME64153.2025.00046) Cited by: [§1](#S1.p2.1).
- 
RepairAgent: an autonomous, llm-based agent for program repair.
In Proceedings of the 47th IEEE/ACM International Conference on Software Engineering (ICSE’25),
pp. 2188–2200.
External Links: [Document](https://dx.doi.org/10.1109/icse55347.2025.00157) Cited by: [§6.3](#S6.SS3.p1.1).
- 
Understanding the impact of refactoring on smells: a longitudinal study of 23 software projects.
In Proceedings of the 11th Joint Meeting on Foundations of Software Engineering (FSE’17),
pp. 465–475.
External Links: [Document](https://dx.doi.org/10.1145/3106237.3106259) Cited by: [§2.2](#S2.SS2.p2.1), [§4.2.1](#S4.SS2.SSS1.p1.1), [§4.2.3](#S4.SS2.SSS3.p2.1), [§5.4.1](#S5.SS4.SSS1.p1.1).
- 
Agent readmes: an empirical study of context files for agentic coding.
ACM Transactions on Software Engineering and Methodology (TOSEM).
External Links: [Document](https://dx.doi.org/10.1145/3840295) Cited by: [§6.2](#S6.SS2.p1.1).
- 
How does refactoring affect internal quality attributes?: A multi-project study.
In Proceedings of the 31st Brazilian Symposium on Software Engineering (SBES’17),
pp. 74–83.
External Links: [Document](https://dx.doi.org/10.1145/3131151.3131171) Cited by: [§2.1](#S2.SS1.p1.1).
- 
A metrics suite for object oriented design.
IEEE Transactions on Software Engineering (TSE) 20 (6), pp. 476–493.
External Links: [Document](https://dx.doi.org/10.1109/32.295895) Cited by: [§5.4.2](#S5.SS4.SSS2.p1.1).
- 
How do software developers use chatgpt? an exploratory study on github pull requests.
In Proceedings of the 21st IEEE/ACM International Conference on Mining Software Repositories (MSR’24),
pp. 212–216.
External Links: [Document](https://dx.doi.org/10.1145/3643991.3645084) Cited by: [§2.5](#S2.SS5.p1.1).
- 
An empirical study on the code refactoring capability of large language models.
ACM Transactions on Software Engineering and Methodology (TOSEM).
External Links: [Document](https://dx.doi.org/10.1145/3801158) Cited by: [§2.3](#S2.SS3.p1.1).
- 
GitHub copilot AI pair programmer: asset or liability?.
Journal of Systems and Software (JSS) 203, pp. 111734.
External Links: [Document](https://dx.doi.org/10.1016/j.jss.2023.111734) Cited by: [§2.4](#S2.SS4.p1.1).
- 
Empirical evaluation of the impact of object-oriented code refactoring on quality attributes: A systematic literature review.
IEEE Transactions on Software Engineering 44 (1), pp. 44–69.
External Links: [Document](https://dx.doi.org/10.1109/tse.2017.2658573) Cited by: [§2.1](#S2.SS1.p1.1).
- 
Applied nonparametric statistics.
Duxbury advanced series in statistics and decision sciences,  PWS-KENT Pub..
Cited by: [§5.4.2](#S5.SS4.SSS2.p2.1).
- 
Analyzing developer-chatgpt conversations for software refactoring: an exploratory study.
In Proceedings of the 21st IEEE/ACM International Conference on Mining Software Repositories (MSR’24),
pp. 207–211.
External Links: [Document](https://dx.doi.org/10.1145/3643991.3645082) Cited by: [§1](#S1.p2.1).
- 
Exploring chatgpt’s code refactoring capabilities: an empirical study.
Expert Systems with Applications 249, pp. 123602.
External Links: [Document](https://dx.doi.org/10.1016/j.eswa.2024.123602) Cited by: [§1](#S1.p2.1), [§2.3](#S2.SS3.p1.1), [§2.4](#S2.SS4.p1.1).
- 
Discovering repetitive code changes in python ML systems.
In Proceedings of the 44th IEEE/ACM International Conference on Software Engineering (ICSE’22),
pp. 736–748.
External Links: [Document](https://dx.doi.org/10.1145/3510003.3510225) Cited by: [§6.2](#S6.SS2.p2.1).
- 
Benchmarking Kappa: interrater agreement in software process assessments.
Empirical Software Engineering 4 (2), pp. 113–133.
External Links: [Document](https://dx.doi.org/10.1023/a%3A1009820201126) Cited by: [§5.3.2](#S5.SS3.SSS2.p2.1).
- 
Refactoring - improving the design of existing code.
 Addison-Wesley.
Cited by: [§1](#S1.p1.1), [§2.1](#S2.SS1.p1.1), [§5.4.3](#S5.SS4.SSS3.p4.1).
- 
Exact calculations of average power for the benjamini-hochberg procedure.
The International Journal of Biostatistics 4 (1).
External Links: [Document](https://dx.doi.org/10.2202/1557-4679.1103) Cited by: [§5.4.2](#S5.SS4.SSS2.p2.1).
- 
Agentic software engineering: foundational pillars and a research roadmap.
abs/2509.06216.
External Links: [Document](https://dx.doi.org/10.48550/arXiv.2509.06216) Cited by: [§1](#S1.p3.1), [§2.5](#S2.SS5.p1.1), [§5.1.1](#S5.SS1.SSS1.p1.1).
- 
The impact of tangled code changes on defect prediction models.
Empirical Software Engineering (EMSE) 21 (2), pp. 303–336.
External Links: [Document](https://dx.doi.org/10.1007/S10664-015-9376-6) Cited by: [§6.2](#S6.SS2.p1.1).
- 
How does test code differ from production code in terms of refactoring? an empirical study.
In Proceedings of the 41st IEEE International Conference on Software Maintenance and Evolution (ICSME’25),
pp. 779–784.
External Links: [Document](https://dx.doi.org/10.1109/icsme64153.2025.00079) Cited by: [§2.2](#S2.SS2.p2.1), [§5.2.1](#S5.SS2.SSS1.p1.1), [§5.2.2](#S5.SS2.SSS2.p3.1), [Table 5](#S5.T5.5.1.3), [§7.1](#S7.SS1.p1.1), [§7.3](#S7.SS3.p2.1).
- 
Does refactoring break tests and to what extent?.
In Proceedings of the 2021 IEEE International Conference on Software Maintenance and Evolution (ICSME 2021),
pp. 171–182.
External Links: [Document](https://dx.doi.org/10.1109/ICSME52107.2021.00022) Cited by: [§1](#S1.p2.1).
- 
An empirical investigation into the role of api-level refactorings during software evolution.
In Proceedings of the 33rd International Conference on Software Engineering (ICSE’11),
pp. 151–160.
External Links: [Document](https://dx.doi.org/10.1145/1985793.1985815) Cited by: [§2.1](#S2.SS1.p1.1).
- 
A field study of refactoring challenges and benefits.
In Proceedings of the ACM SIGSOFT 20th International Symposium on the Foundations of Software Engineering (FSE’12),
pp. 50.
External Links: [Document](https://dx.doi.org/10.1145/2393596.2393655) Cited by: [§2.1](#S2.SS1.p1.1), [§2.2](#S2.SS2.p2.1).
- 
An empirical study of refactoring challenges and benefits at microsoft.
IEEE Transactions on Software Engineering (TSE) 40 (7), pp. 633–649.
External Links: [Document](https://dx.doi.org/10.1109/tse.2014.2318734) Cited by: [§1](#S1.p1.1), [§2.1](#S2.SS1.p1.1), [Figure 4](#S5.F4), [Figure 4](#S5.F4.4), [§5.3.1](#S5.SS3.SSS1.p1.1), [§5.3.2](#S5.SS3.SSS2.p1.1), [§5.3.3](#S5.SS3.SSS3.p1.1).
- 
A data analysis study of code smells within java repositories.
In Proceedings of the 17th Conference on Computer Science and Intelligence Systems,
Vol. 32, pp. 313–318.
External Links: [Document](https://dx.doi.org/10.15439/2022f171) Cited by: [§5.4.2](#S5.SS4.SSS2.p1.1).
- 
The rise of AI teammates in software engineering (SE) 3.0: how autonomous coding agents are reshaping software engineering.
CoRR abs/2507.15003.
External Links: [Document](https://dx.doi.org/10.48550/arXiv.2507.15003) Cited by: [§1](#S1.p3.1), [§1](#S1.p4.1), [§2.5](#S2.SS5.p1.1), [§4.1](#S4.SS1.p1.1), [§7.3](#S7.SS3.p1.1).
- 
Ordinal Analysis of Behavioral Data.
In Handbook of Psychology,
pp. 635–661.
External Links: [Document](https://dx.doi.org/10.1002/0471264385.wei0225) Cited by: [§5.1.2](#S5.SS1.SSS2.p1.1).
- 
On a test of whether one of two random variables is stochastically larger than the other.
Annals of Mathematical Statistics 18, pp. 50–60.
External Links: [Document](https://dx.doi.org/10.1214/aoms/1177730491) Cited by: [§5.1.2](#S5.SS1.SSS2.p1.1).
- 
SapFix: automated end-to-end repair at scale.
In Proceedings of the 41st International Conference on Software Engineering: Software Engineering in Practice (ICSE-SEIP),
pp. 269–278.
External Links: [Document](https://dx.doi.org/10.1109/icse-seip.2019.00039) Cited by: [§6.3](#S6.SS3.p2.1).
- 
JDeodorant: clone refactoring.
In Proceedings of the 38th International Conference on Software Engineering Companion (ICSE’16),
pp. 613–616.
External Links: [Document](https://dx.doi.org/10.1145/2889160.2889168) Cited by: [§2.3](#S2.SS3.p1.1).
- 
Recommendation system for software refactoring using innovization and interactive dynamic optimization.
In Proceedings of the ACM/IEEE International Conference on Automated Software Engineering (ASE’14),
pp. 331–336.
External Links: [Document](https://dx.doi.org/10.1145/2642937.2642965) Cited by: [§1](#S1.p2.1).
- 
A case study on the impact of refactoring on quality and productivity in an agile team.
In Proceedings of the 2nd IFIP Central and East European Conference on Software Engineering Techniques,
Lecture Notes in Computer Science, Vol. 5082, pp. 252–266.
External Links: [Document](https://dx.doi.org/10.1007/978-3-540-85279-7%5F20) Cited by: [§1](#S1.p1.1), [§2.1](#S2.SS1.p1.1), [§2.2](#S2.SS2.p2.1).
- 
How we refactor, and how we know it.
IEEE Transactions on Software Engineering 38 (1), pp. 5–18.
External Links: [Document](https://dx.doi.org/10.1109/TSE.2011.41) Cited by: [§1](#S1.p2.1), [§2.2](#S2.SS2.p1.1), [§2.3](#S2.SS3.p1.1), [§4.2.1](#S4.SS2.SSS1.p1.1), [§4.2.3](#S4.SS2.SSS3.p2.1), [§5.2.2](#S5.SS2.SSS2.p1.1).
- 
A study of repetitiveness of code changes in software evolution.
In Proceedings of the 28th IEEE/ACM International Conference on Automated Software Engineering (ASE’13),
pp. 180–190.
External Links: [Document](https://dx.doi.org/10.1109/ASE.2013.6693078) Cited by: [§6.2](#S6.SS2.p2.1).
- 
Trust enhancement issues in program repair.
In Proceedings of the 44th International Conference on Software Engineering (ICSE’22),
pp. 2228–2240.
External Links: [Document](https://dx.doi.org/10.1145/3510003.3510040) Cited by: [§6.3](#S6.SS3.p2.1).
- 
Refactoring object-oriented frameworks.
Ph.D. Thesis, University of Illinois at Urbana-Champaign.
Cited by: [§1](#S1.p1.1).
- 
Search-based refactoring for software maintenance.
Journal of Systems and Software (JSS) 81 (4), pp. 502–516.
External Links: [Document](https://dx.doi.org/10.1016/j.jss.2007.06.003) Cited by: [§2.3](#S2.SS3.p1.1).
- 
An exploratory study on the relationship between changes and refactoring.
In Proceedings of the 25th International Conference on Program Comprehension (ICPC’17),
pp. 176–185.
External Links: [Document](https://dx.doi.org/10.1109/icpc.2017.38) Cited by: [§2.2](#S2.SS2.p3.1).
- 
Why do developers reject refactorings in open-source projects?.
ACM Transactions on Software Engineering and Methodology (TOSEM) 31 (2), pp. 23:1–23:23.
External Links: [Document](https://dx.doi.org/10.1145/3487062) Cited by: [§1](#S1.p2.1).
- 
Why developers refactor source code: A mining-based study.
ACM Transactions on Software Engineering and Methodology (TOSEM) 29 (4), pp. 29:1–29:30.
External Links: [Document](https://dx.doi.org/10.1145/3408302) Cited by: [§1](#S1.p1.1), [§2.2](#S2.SS2.p3.1).
- 
An empirical investigation into the impact of refactoring on regression testing.
In Proceedings of the 28th IEEE International Conference on Software Maintenance (ICSM’12),
pp. 357–366.
External Links: [Document](https://dx.doi.org/10.1109/icsm.2012.6405293) Cited by: [§1](#S1.p2.1).
- 
Take loads off your developers: automated user story generation using large language model.
In Proceedings of the 40th IEEE International Conference on Software Maintenance and Evolution (ICSME’24),
pp. 791–801.
External Links: [Document](https://dx.doi.org/10.1109/icsme58944.2024.00082) Cited by: [§2.5](#S2.SS5.p1.1).
- 
Exploring methods for evaluating group differences on the NSSE and other surveys: are the t-test and Cohen’sd indices the most appropriate choices.
In Proceedings of the Annual Meeting of the Southern Association for Institutional Research (SAIR’06),
pp. 1–51.
Cited by: [§5.1.2](#S5.SS1.SSS2.p1.1).
- 
Lost at C: A user study on the security implications of large language model code assistants.
In Proceedings of the USENIX Security Symposium 2023,
pp. 2205–2222.
Cited by: [§2.4](#S2.SS4.p1.1).
- 
Vibe coding vs. agentic coding: fundamentals and practical implications of agentic AI.
CoRR abs/2505.19443.
Cited by: [§1](#S1.p3.1).
- 
Toward understanding the impact of refactoring on program comprehension.
In Proceedings of the IEEE International Conference on Software Analysis, Evolution and
Reengineering (SANER’22),
pp. 731–742.
External Links: [Document](https://dx.doi.org/10.1109/saner53432.2022.00090) Cited by: [§1](#S1.p1.1).
- 
Using ai-based coding assistants in practice: state of affairs, perceptions, and ways forward.
Information and Software Technology (IST) 178, pp. 107610.
External Links: [Document](https://dx.doi.org/10.1016/j.infsof.2024.107610) Cited by: [§2.4](#S2.SS4.p1.1), [§6.1](#S6.SS1.p1.1).
- 
Mining and fusing productivity metrics with code quality information at scale.
In Proceedings of the 2023 IEEE International Conference on Software Maintenance and Evolution (ICSME’23),
pp. 563–567.
External Links: [Document](https://dx.doi.org/10.1109/icsme58846.2023.00073) Cited by: [§5.4.2](#S5.SS4.SSS2.p1.1).
- 
An automated extract method refactoring approach to correct the long method code smell.
Journal of Systems and Software (JSS) 187, pp. 111221.
Cited by: [§1](#S1.p2.1).
- 
Multi-faceted code smell detection at scale using designitejava 2.0.
In Proceedings of the 21st IEEE/ACM International Conference on Mining Software Repositories (MSR’24),
pp. 284–288.
External Links: [Document](https://dx.doi.org/10.1145/3643991.3644881) Cited by: [§4.2.1](#S4.SS2.SSS1.p1.1), [§5.4.2](#S5.SS4.SSS2.p1.1), [§7.1](#S7.SS1.p1.1).
- 
Refactoring programs using large language models with few-shot examples.
In Proceedings of the 30th Asia-Pacific Software Engineering Conference, (APSEC’23),
pp. 151–160.
External Links: [Document](https://dx.doi.org/10.1109/apsec60848.2023.00025) Cited by: [§1](#S1.p2.1).
- 
RefDiff 2.0: A multi-language refactoring detection tool.
IEEE Transactions on Software Engineering 47 (12), pp. 2786–2802.
External Links: [Document](https://dx.doi.org/10.1109/tse.2020.2968072) Cited by: [§2.2](#S2.SS2.p1.1), [§4.2.1](#S4.SS2.SSS1.p1.1), [§7.3](#S7.SS3.p2.1).
- 
Why we refactor? confessions of github contributors.
In Proceedings of the 24th ACM SIGSOFT International Symposium on Foundations of Software Engineering (FSE’16),
pp. 858–870.
External Links: [Document](https://dx.doi.org/10.1145/2950290.2950305) Cited by: [§1](#S1.p1.1), [§2.1](#S2.SS1.p1.1), [§2.2](#S2.SS2.p3.1).
- 
IntelliCode compose: code generation using transformer.
In Proceedings of the 28th ACM Joint European Software Engineering Conference
and Symposium on the Foundations of Software Engineering (FSE’20),
pp. 1433–1443.
External Links: [Document](https://dx.doi.org/10.1145/3368089.3417058) Cited by: [§2.4](#S2.SS4.p1.1).
- 
Bulk fixing coding issues and its effects on software quality: is it worth refactoring?.
In Proceedings of the 14th IEEE International Working Conference on Source Code Analysis
and Manipulation (SCAM’14),
pp. 95–104.
External Links: [Document](https://dx.doi.org/10.1109/scam.2014.18) Cited by: [§2.2](#S2.SS2.p2.1).
- 
Ten years of jdeodorant: lessons learned from the hunt for smells.
In Proceedings of the 25th International Conference on Software Analysis, Evolution and
Reengineering (SANER’18),
pp. 4–14.
External Links: [Document](https://dx.doi.org/10.1109/saner.2018.8330192) Cited by: [§2.3](#S2.SS3.p1.1).
- 
Identification of move method refactoring opportunities.
IEEE Transactions on Software Engineering (TSE) 35 (3), pp. 347–367.
External Links: [Document](https://dx.doi.org/10.1109/tse.2009.1) Cited by: [§1](#S1.p2.1).
- 
RefactoringMiner 2.0.
IEEE Transactions on Software Engineering 48 (3), pp. 930–950.
External Links: [Document](https://dx.doi.org/10.1109/tse.2020.3007722) Cited by: [§2.2](#S2.SS2.p1.1), [§4.2.1](#S4.SS2.SSS1.p1.1), [§4.2.3](#S4.SS2.SSS3.p1.1), [§7.1](#S7.SS1.p1.1).
- 
Unveiling chatgpt’s usage in open source projects: A mining-based study.
In Proceedings of the 21st IEEE/ACM International Conference on Mining Software Repositories (MSR’24),
pp. 571–583.
External Links: [Document](https://dx.doi.org/10.1145/3643991.3644918) Cited by: [§1](#S1.p2.1).
- 
How to design a program repair bot? Insights from the Repairnator project.
In Proceedings of the 40th International Conference on Software Engineering: Software Engineering in Practice (ICSE-SEIP),
pp. 95–104.
External Links: [Document](https://dx.doi.org/10.1145/3183519.3183540) Cited by: [§6.3](#S6.SS3.p2.1).
- 
A large-scale empirical exploration on refactoring activities in open source software projects.
Science of Computer Programming 180, pp. 1–15.
External Links: [Document](https://dx.doi.org/10.1016/j.scico.2019.05.002) Cited by: [§2.2](#S2.SS2.p1.1), [§2.3](#S2.SS3.p1.1), [§4.2.1](#S4.SS2.SSS1.p1.1), [§4.2.3](#S4.SS2.SSS3.p2.1).
- 
On the use of chatgpt for code review: do developers like reviews by chatgpt?.
In Proceedings of the 28th International Conference on Evaluation and
Assessment in Software Engineering (EASE’24),
pp. 375–380.
External Links: [Document](https://dx.doi.org/10.1145/3661167.3661183) Cited by: [§1](#S1.p2.1).
- 
On the use of agentic coding: an empirical study of pull requests on github.
ACM Transactions on Software Engineering and Methodology (TOSEM) 35 (10), pp. 1–24.
External Links: [Document](https://dx.doi.org/10.1145/3798166) Cited by: [§2.4](#S2.SS4.p1.1), [§3](#S3.p1.1).
- 
Individual comparisons by ranking methods.
Biometrics Bulletin 1 (6), pp. 80–83.
External Links: [Document](https://dx.doi.org/10.2307/3001968) Cited by: [§5.4.2](#S5.SS4.SSS2.p2.1).
- 
An empirical evaluation of refactoring.
e-Informatica Software Engineering Journal 1 (1), pp. 27–42.
Cited by: [§2.1](#S2.SS1.p1.1).
- 
User-centric deployment of automated program repair at Bloomberg.
In Proceedings of the 46th IEEE/ACM International Conference on Software Engineering: Software Engineering in Practice (ICSE-SEIP),
pp. 81–91.
External Links: [Document](https://dx.doi.org/10.1145/3639477.3639756) Cited by: [§6.3](#S6.SS3.p2.1).
- 
How do developers really feel about bug fixing? Directions for automatic program repair.
IEEE Transactions on Software Engineering 49 (4), pp. 1823–1841.
External Links: [Document](https://dx.doi.org/10.1109/tse.2022.3194188) Cited by: [§6.3](#S6.SS3.p2.1).
- 
Refactoring practice: how it is and how it should be supported - an eclipse case study.
In Proceedings of the 22nd IEEE International Conference on Software Maintenance (ICSM’06),
Vol. , pp. 458–468.
External Links: [Document](https://dx.doi.org/10.1109/icsm.2006.52) Cited by: [§2.2](#S2.SS2.p1.1).
