# SlopCodeBench: Benchmarking How Coding Agents Degrade Over Long-Horizon Iterative Tasks

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: Gabriel Orlanski, Devjeet Roy, Alexander Yun, Changho Shin, Alex Gu, Albert Ge, Dyah Adila, Nicholas Roberts, Frederic Sala, Aws Albarghouthi
- Date: 2026-03-25
- Original location: https://arxiv.org/abs/2603.24755
- Copied: 2026-11-20, from the arXiv HTML full text, converted to Markdown with trafilatura

## Text
# SlopCodeBench: Benchmarking How Coding Agents Degrade Over Long-Horizon Iterative Tasks

###### Abstract

Software development is iterative, yet agentic coding benchmarks hide design issues through their single-shot setup. Recent iterative benchmarks attempt to remedy this but heavily constrain an agent’s design decision space, making it impossible to faithfully measure how their decisions shape future extensions. We introduce SlopCodeBench, a benchmark of 36 problems and 196 checkpoints where agents repeatedly extend their own solutions. Unlike prior iterative benchmarks, our evolving specifications demand architectural decisions but leave internal structure to the agent. We measure two forms of degradation: structural erosion (concentrated complexity) and verbosity (redundant code). Evaluating 15 coding agents across open and closed models, we find that no agent fully solves any problem end-to-end, and the best agent passes 14.8% of checkpoints. Quality degrades across checkpoints, with structural erosion rising in 77% of trajectories and verbosity in 75.5%. Compared to 473 open-source Python repositories, agent code is 2.3x more verbose and 2.0x more eroded, and the human repositories degrade less often and by smaller margins across their git histories. Explicit quality guidance reduces initial verbosity and erosion by up to a third, without affecting degradation rates. SlopCodeBench provides the first measurement of code degradation under iterative extension, revealing that agents pass checkpoints while producing code that erodes and bloats with each turn.

## 1 Introduction

Every design decision in software engineering is a compromise with unknown future requirements. A code search program built around regular expressions works until the specification demands structural pattern matching, at which point the entire architecture must be rewritten. Existing coding-agent benchmarks systematically undermeasure this failure mode, evaluating models once against complete task specifications \[[28](#bib.bib27), [38](#bib.bib24), [58](#bib.bib42), [10](#bib.bib48)\]. They measure whether an agent can produce correct code for the current specification, not whether that code remains extensible under future change.

Under repeated editing, agent-generated code often deteriorates in recognizable ways. LLMs favor verbose constructions over concise idioms \[[22](#bib.bib65), [1](#bib.bib63)\], and agent-generated code carries redundant or unnecessary methods that reviewers routinely strip \[[15](#bib.bib29), [43](#bib.bib30), [62](#bib.bib33)\]. The resulting low-quality, high-volume code is often colloquially called “slop.” In traditional software engineering, such accumulation is associated with higher maintenance cost and slower modification \[[33](#bib.bib56), [34](#bib.bib64), [35](#bib.bib55)\], yet pass rates can remain stable even as the underlying code becomes harder to extend. Despite this large body of work, the standard agentic coding benchmarks cannot adequately measure this behavior because they focus on correctness in single-shot setups rather than on iterative evaluations.

Recent benchmarks push toward multi-turn or long-horizon coding, but none of them isolate *true iterative coding*. Some construct iterative tasks by decomposing monolithic solutions into dependency-ordered subproblems, thereby producing a self-contained testbed rather than a realistic setting in which the agent selects an architecture and must live with it later \[[60](#bib.bib21)\]. Others derive tasks from the commit histories of mature open-source repositories \[[57](#bib.bib31), [20](#bib.bib32), [13](#bib.bib40)\]. These are valuable for studying an agent’s ability to maintain or add narrow features in an existing codebase, but they fundamentally can not test iterative coding. Using human-built workspaces and historically realized evolution paths means the agent never pays the cost of its own early design decisions. In some cases, the task formulation is also tied to test- or oracle-derived signals, which further undercuts the benchmark’s ability to measure open-ended iterative design \[[13](#bib.bib40)\]. To properly measure this, a benchmark needs four things: the agent builds on its own prior code; problems specify only external behavior, not internal interfaces; a truly hidden test suite to prevent leaking architectural hints; and black-box contracts that are implementable in any language.

We therefore introduce SlopCodeBench (SCBench), a benchmark for measuring how code quality evolves as agents repeatedly extend *their own prior code* under changing specifications. SCBench contains 36 problems spanning 196 checkpoints. Each checkpoint specifies only observable behavior at a CLI or API boundary, leaving internal structure unconstrained and keeping the test suite hidden. The benchmark is language-agnostic by construction: specifications describe only CLI and API behavior. We evaluate the Python track in this paper. Beyond correctness, we track two trajectory-level quality signals: verbosity, which measures the growth of redundant or duplicated code, and structural erosion, which measures the concentration of complexity in already-complex functions. The former calculates the percent of lines that are either flagged by ast-grep patterns or are structural duplicates of other code. For erosion, we calculate the percentage of the overall cyclomatic complexity \[[39](#bib.bib58)\] that is contained in high-complexity functions.

Our contributions are:

1. 1\. 
SlopCodeBench <sup>1</sup><sup>1</sup> 1
                  
                  
                  
                Full problems and code are found at [scbench.ai](https://www.scbench.ai)a language-agnostic benchmark of 36 iterative software-development problems across 196 checkpoints. The state-of-the-art performance is 14.8% with no problem fully solved.
2. 2\. 
Two trajectory-level quality metrics, verbosity and structural erosion, to measure low-quality agent code. Structural Erosion rises in 77% of trajectories and verbosity in 75.5%.
3. 3\. 
Calibration against human code. Agent code is 2.3$\times$ more verbose and 2.0$\times$ more eroded than 473 open-source repositories. Per checkpoint, agent verbosity grows 6.6$\times$ and erosion grows 5.0$\times$ faster than that in human code.
4. 4\. 
Study on prompting techniques. Quality-aware prompts reduce initial verbosity but do not slow the degradation. Further, this results in an average 12.1% increase in the cost per checkpoint and a drop in correctness of 2.3 pp.

## 2 SlopCodeBench

SlopCodeBench contains 36 language-agnostic problems spanning 196 checkpoints. Each problem is specified solely in terms of observable behavior at a CLI or API boundary, so it can be evaluated in any implementation language. An agent implements the first specification from scratch, then repeatedly modifies and extends *its own prior code* as specifications evolve. Our focus is on measuring both correctness and code quality throughout that trajectory. The remainder of this section is structured as follows: 1) our desiderata, 2) how we constructed the dataset, 3) how we quantify quality issues, and 4) finally, conclude with our evaluation procedure.

### 2.1 Design Principles

The core goal of SlopCodeBench is to evaluate an agent’s ability to make design decisions that will directly influence the quality of their code. For this, we have a core set of design principles that every problem must follow. Without these, architectural details are leaked to the agent and corrupt the signal we explicitly want to measure. They are:

1. 1\.
2. 2\.
3. 3\. 
Black-box, language-agnostic problem design. Problems constrain only observable behavior, not implementation language or ecosystem. Following the principle that evaluation should not depend on a specific language’s ecosystem \[[68](#bib.bib45), [54](#bib.bib43), [10](#bib.bib48)\], outputs are evaluated solely via CLI or API interfaces, with normalization removing inconsequential differences in formatting and ordering. We evaluate only on Python due to cost.

In our running [code\_search](#S2) problem, $C_{1}$ specifies the CLI contract: \<root\_dir> --rules \<file> \[--encoding \<name>\], with output as JSON lines containing fields rule\_id, file, start, end, and match. The only prescribed internals are the input/output structures that the harness needs to supply inputs and parse outputs. Specifications add normalization guidance only where arbitrary choices could cause false failures, such as key ordering, text casing, or match-span sorting. In $C_{3}$, for example, an example fixes the sort order for multiple pattern matches even though the rule is not stated explicitly. This prevents penalizing inconsequential implementation choices.

### 2.2 Task Formulation

All of our problems are written by hand, either as novel tasks or inspired by popular repositories. Each problem $P$ is an ordered list of checkpoints $[C_{1},\ldots,C_{n}]$. At $C_{i}$, the agent $\pi_{\theta}$ receives only the $x_{i}$ and its previous workspace $y_{i-1}$, then produces an updated workspace $y_{i}$. At $C_{1}$, the agent starts from the empty workspace $y_{0}$.

|  | $\displaystyle y_{1}$ | $\displaystyle=\pi_{\theta}(x_{1},y_{0})$ |  | (1) | 
|  | $\displaystyle y_{2}$ | $\displaystyle=\pi_{\theta}(x_{2},y_{1})$ |  |  | 
|  | $\displaystyle\ldots$ |  |  |  | 
|  | $\displaystyle y_{i}$ | $\displaystyle=\pi_{\theta}(x_{i},y_{i-1})$ |  |  | 

Each checkpoint is a fresh feature starting from the prior checkpoint’s workspace. The agent must reason about changes solely from the code’s current structure, as we do not provide the prior conversation’s context. A poor architectural choice at checkpoint $i$ becomes the foundation for checkpoint $i+1$, and the agent must build on it. If a reference solution replaces the agent’s code between turns, the causal chain from early decisions to later degradation is removed. In SlopCodeBench, unlike other benchmarks \[[60](#bib.bib21), [61](#bib.bib20), [20](#bib.bib32)\], the agent’s workspace is carried forward to the next checkpoint, and quality is measured at every step.

##### Problem Construction.

Problems were authored by the paper’s authors through a two-phase process, with each problem reviewed by at least one author other than its drafter. In the proposal phase, an author drafted a problem along with its checkpoint partition; problems that did not meaningfully test design decisions, or that frontier agents could solve in a single shot, were removed from the pool. In the validation phase, we wrote the initial test suite and attempted each checkpoint with an agent, using these runs to identify and refine ambiguous or under-specified test cases. A final review pass confirmed that every problem was solvable in principle and that test suites matched the specifications. [Table 4](#A1.T4) details each problem and what design decisions are stressed.

### 2.3 Measuring Code Quality

Standard quality models decompose software quality into broad characteristics such as
maintainability, reliability, and portability \[[27](#bib.bib62)\]. We focus on two
trajectory-level failure modes that are computable at every checkpoint and comparable
across agents and problems. *Structural erosion* captures the concentration of
control-flow complexity in already-complex functions. *Verbosity* captures
duplicated and rule-flagged redundant code patterns. These metrics are computed
independently of functional correctness, letting us measure structural changes that
pass rates alone do not expose.

##### Structural erosion.

Agents under iteration tend to patch new logic into existing functions rather than distributing it across focused callables. [4](#LST4) shows how a function in code\_search at $C_{5}$ can grow to 117 lines with branches for each rule kind and each match source chained inside one loop. In the iterative paradigm, the clearest notion of erosion is haphazard edits to a function that patch functionality. These edits compound slowly until they become too large to work on. Thus, we define erosion as the fraction of the codebase’s total complexity mass that resides in high-complexity functions. To this end we first assign each callable a *complexity mass* that accounts for both its cyclomatic complexity (CC, \[[39](#bib.bib58)\]) and its size:

|  | $$ \text{mass}(f)=\text{CC}(f)\times\sqrt{\text{SLOC}(f)} $$ |  | (2) | 

where $\text{CC}(f)$ is the cyclomatic complexity of callable $f$ and $\text{SLOC}(f)$ is its source lines of code. The square root compresses the size factor so that complexity dominates rather than pure lines of code. Erosion is then the share of total mass held by functions exceeding a high-complexity threshold:

|  | $$ \text{Erosion}=\frac{\sum_{f\in\mathcal{F}}\mathbb{I}[\text{CC}(f)>10]\cdot\text{mass}(f)}{\sum_{f\in\mathcal{F}}\text{mass}(f)} $$ |  | (3) | 

where $\mathcal{F}$ is the set of all callables. We use a cutoff of 10 for CC following the established bounds in the popular code analysis tool [Radon](https://radon.readthedocs.io/en/latest/). In the solution to code\_search shown in [4](#LST4), the majority of decision-points have collapsed into find\_matches\_in\_file(), driving its mass upward even as the agent adds other functions around it.

##### Verbosity.

The other dimension of slop is code that is too *verbose*, copy-pasted, or unnecessary lines that do not add anything to the overall codebase. A typical code\_search fragment rebuilds the array rather than using filter, guards each iteration with empty-list checks, and assigns intermediate names used once. To capture both effects, we use a static verbosity score with two parts. First, we measure clear patterns of wasteful code generated by agents through constructing 137 targeted [AST-Grep](https://ast-grep.github.io) rules. These rules are based on observed cases of verbose code, best practices, and commonly cited anti-patterns on social media. Second, we measure structural duplication as clone lines normalized by LOC \[[30](#bib.bib72), [2](#bib.bib73)\]. The resulting score is

|  | $$ \text{Verbosity}=\frac{\|\{\text{AST-Grep Flagged Lines}\cup\text{Clone Lines}\}\|}{\text{LOC}} $$ |  | (4) | 

We deduplicate lines hit by multiple AST-grep rules before counting. This score is bounded in $[0,1]$, thus comparable across runs and independent of erosion. The two metrics measure different failure modes, so tracking both gives a fuller picture of the “slop” agents generate.

##### Alternative Metrics.

A natural alternative is to use existing software quality metrics directly. Composite metrics such as the Maintainability Index combine traditional measures into a single maintainability score \[[44](#bib.bib74)\]. While useful as broad summaries, they are less appropriate for measuring specific ways code changes over iterations. More targeted metrics also capture only part of the phenomenon: Cyclomatic Complexity measures independent control-flow paths \[[39](#bib.bib58)\], Cognitive Complexity penalizes control-flow breaks and nesting \[[12](#bib.bib76)\], the Chidamber-Kemerer suite measures class-level object-oriented design properties \[[16](#bib.bib75)\], clone metrics capture duplication \[[30](#bib.bib72), [2](#bib.bib73)\], and LOC captures code growth. In contrast, our goal is to separate two independent failure modes: code can become more verbose without concentrating complexity, and complexity can concentrate in some functions without much overall growth. We therefore measure structural erosion and verbosity separately rather than relying on a single aggregate maintainability score or fine-grained yet incomplete single-property metrics.

### 2.4 Evaluating Solutions

Every checkpoint’s tests interact with the solution only through subprocess or its served API. Test suites normalize outputs where needed and maintain held-out tests beyond the specification’s examples. Each test is categorized as:

- • 
Core — Functionality explicitly mentioned or shown in the specification.
- • 
Error — Failure-mode behaviors.
- • 
Functionality — Hidden tests that exhaustively check correctness.
- • 
Regression — All tests from prior checkpoints. $C_{1}$ has no regression tests.

The produced workspace $y_{i}$ is correct if all tests pass. Because regression tests carry earlier requirements forward, a mistake at $C_{2}$ can zero out later checkpoints even if later code partly works. To separate implementation quality from cascading failures, we also report correct in isolation (ISO) if $y_{i}$ passes all non-regression tests for $C_{i}$, and core correct (CORE) if it passes only the core tests. A problem is Partially solved if at least one checkpoint is strictly solved.

When an agent fails or crashes mid-problem, remaining checkpoints receive a correctness score of zero. Erosion and verbosity are computed only for checkpoints where the agent produced a workspace; missing checkpoints are excluded rather than imputed.

## 3 Iterative Evaluation of Coding Agents

This section reports empirical results on SlopCodeBench. The evaluation targets behaviors that arise once an agent edits its own code across multiple checkpoints, a regime that one-shot benchmarks do not exercise. Four research questions structure the experiments, each stated with its supporting result.

RQ1: Can agents iteratively extend their own design decisions? No configuration is able to produce a solution that passes every checkpoint for any problem. Each checkpoint’s cost rises without corresponding improvements to correctness.

RQ2: Does iteration cause agent code to degrade? Structural erosion increases in 77% of trajectories while verbosity increases in 75.5% of trajectories.

RQ3: How does agent degradation compare to repository histories? Compared to 473 Python repositories, agents produce code that is 2.0$\times$ more structurally eroded and 2.3$\times$ more verbose. Agents additionally exhibit significantly higher degradation, especially compared to pre-2024 commits.

RQ4: Can better prompts stop this behavior? Better prompts can reduce initial structural erosion by up to 62.3% and verbosity by up to 34.8%, but do not stop iterative degradation. The average quality velocity remains 1.3 percentage points per checkpoint. Different prompting methods additionally increase the cost per checkpoint by 12.1% on average.

##### Setup.

Each checkpoint runs in a fresh Docker container as a non-root user; only the working directory persists between checkpoints. Frontier models are trained for their provider’s harness rather than generalized agent loops, and most developers interact with agents through these CLI tools. We therefore evaluate in native harnesses rather than frameworks such as SWE-agent \[[65](#bib.bib28)\]. We evaluate 15 models across six providers in detail. Each run has a two-hour wall-clock limit, no turn or cost cap, and uses the just-solve prompt, which only instructs the agent to solve the problem and keep track of dependencies. Additional setup details are found in [Appendix C](#A3).

Problems range from 3 to 8 checkpoints, so raw checkpoint indices are not directly comparable across problems. For aggregation and visualization, we map each trajectory to one of five *progress phases*. The first checkpoint is always Start and the last is always Final. The remaining interior checkpoints are divided into three groups: Early, Mid, and Late. All per-phase statistics in this paper use this.

### 3.1 Solve Rates Stagnate as Cost Grows

[Table 8](#A4.T8)for the full set of runs.

|  | Solve Rate (%) |  |  |  | Cost & Time |  |  | Quality |  | 
| Model | Strict | Iso. | Core | Partial | $/CKPT | Net $ | Min/CKPT | Erosion | Verbosity | 
| Opus 4.5 | 9.2 | 17.3 | 57.7 | 25.0 | 2.53$\pm$1.57 | 492.40 | 7.2$\pm$3.7 | 0.70$\pm$0.20 | 0.43$\pm$0.18 | 
| Opus 4.6 | 9.7 | 20.9 | 67.3 | 27.8 | 3.17$\pm$2.82 | 620.80 | 13.1$\pm$12.9 | 0.75$\pm$0.15 | 0.44$\pm$0.19 | 
| Opus 4.7 | 8.2 | 20.9 | 65.8 | 36.1 | 2.17$\pm$1.83 | 425.34 | 6.8$\pm$5.0 | 0.76$\pm$0.17 | 0.48$\pm$0.21 | 
| Sonnet 4.6 | 7.1 | 16.8 | 57.7 | 27.8 | 1.96$\pm$1.97 | 383.83 | 14.2$\pm$14.2 | 0.75$\pm$0.20 | 0.44$\pm$0.19 | 
| GPT 5.2 Codex | 9.7 | 21.9 | 56.1 | 36.1 | 0.85$\pm$0.80 | 167.29 | 12.3$\pm$9.7 | 0.73$\pm$0.18 | 0.50$\pm$0.16 | 
| GPT 5.3 Codex | 11.2 | 26.0 | 60.7 | 41.7 | 0.66$\pm$0.49 | 129.65 | 7.7$\pm$4.6 | 0.64$\pm$0.19 | 0.46$\pm$0.18 | 
| GPT 5.3 Spark | 3.1 | 8.2 | 29.1 | 11.1 | 0.20$\pm$0.41 | 37.17 | 2.4$\pm$4.6 | 0.68$\pm$0.19 | 0.48$\pm$0.16 | 
| GPT 5.4 | 10.7 | 23.5 | 62.8 | 36.1 | 0.72$\pm$0.51 | 141.32 | 8.0$\pm$4.7 | 0.51$\pm$0.19 | 0.33$\pm$0.13 | 
| GPT 5.4 Mini | 5.1 | 13.8 | 53.1 | 22.2 | 0.45$\pm$0.35 | 89.03 | 6.2$\pm$3.8 | 0.66$\pm$0.17 | 0.42$\pm$0.12 | 
| GPT 5.5 | 14.8 | 28.1 | 66.8 | 50.0 | 1.51$\pm$0.81 | 295.59 | 6.0$\pm$2.4 | 0.49$\pm$0.20 | 0.32$\pm$0.12 | 
| Composer 2 | 6.1 | 16.3 | 52.6 | 13.9 | 0.44$\pm$0.44 | 86.31 | 8.8$\pm$8.3 | 0.72$\pm$0.15 | 0.45$\pm$0.17 | 
| GLM 5.1 | 9.7 | 13.8 | 40.3 | 30.6 | 1.47$\pm$1.45 | 288.85 | 31.4$\pm$20.0 | 0.71$\pm$0.17 | 0.41$\pm$0.18 | 
| Kimi K2.5 | 4.6 | 9.7 | 39.8 | 19.4 | 0.33$\pm$0.25 | 63.21 | 14.5$\pm$10.0 | 0.72$\pm$0.20 | 0.44$\pm$0.20 | 
| Kimi K2.6 | 10.7 | 18.9 | 51.0 | 33.3 | 0.74$\pm$0.64 | 133.18 | 26.9$\pm$20.7 | 0.76$\pm$0.20 | 0.51$\pm$0.22 | 
| MiniMax M2.7 | 2.0 | 4.1 | 28.1 | 8.3 | 0.34$\pm$0.23 | 65.79 | 11.9$\pm$6.8 | 0.73$\pm$0.16 | 0.47$\pm$0.17 | 

[Table 1](#S3.T1)summarizes solve rates across 15 models on SlopCodeBench. No agent *fully* solves any of the 36 problems. No run passes every test at every checkpoint end-to-end. GPT 5.5 achieves the highest strict solve rate at 14.8% and isolated solve rate peaks at 28.1%. Opus 4.5 achieves the highest core solve rate at 67.3%.

[Figure 2](#S3.F2)shows the gap between core and isolated pass rates widens from 2.5$\times$ to 5.4$\times$. Core pass rate falls from 64.6% to 35.5%. Functionality pass rate changes by less than six points, from 62.7% to 57.7%, while error pass rate drops from 80.1% to 62.2%.

Cost and context grow while code movement declines. Mean cost per checkpoint grows 2.2$\times$ from the start to end, while mean relative lines changed fall from 97.4% early to 29.5% late. Total recorded token accounting is 13.18B tokens. Normalized to 196 checkpoints, Composer 2 has the lowest token spend at 0.38B tokens, while Kimi K2.6 has the highest at 1.14B tokens.

### 3.2 Iterative Agent Trajectories Accumulate Quality Issues

[Figure 3](#S3.F3)highlights the changes in quality throughout frontier models’ trajectories on problems. Across all settings, structural erosion increases in 77% of trajectories, verbosity in 75.5%. The average number of functions with at least 10 cyclomatic complexity rises from 3.6 to 23.7 and mean maximum CC from 27.5 to 69.0. This behavior would be invisible without iterative evaluation.

Opus 4.7’s main() on [forge](https://www.scbench.ai/problems/forge) grows 7$\times$ in CC across 8 checkpoints, from 38 to 240 lines. The $C_{1}$ argparse call, shown in [6](#LST6), is replaced by a manual flag loop in which seven flags each get an identical pair of `--X val`/`--X=val` branches and no helper is extracted ([7](#LST7)). The accumulation over time highlights the key failure mode.

Verbosity behaves similarly to erosion. Structural duplication grows 96% while AST-grep violation density grows only 0.3%, reflecting the rewriting of existing code rather than fresh rule violations. Iterative evaluation makes accumulation visible; small structural choices are amplified by iteration rather than absorbed.

### 3.3 How does agent degradation compare to repository histories?

To answer this, we collect 473 Python repositories ranging from hobby projects under 100 stars to major frameworks with over 10k stars and 2M LOC, covering web frameworks, scientific computing, infrastructure, and utilities. For each repository, we randomly sample up to 30 source-modifying commits totaling 13667 commits. We treat each repository’s most recent commit at the time of collection as its current state for cross-sectional comparisons and the full commit sequence as analogous to an agent trajectory.

[Figure 4](#S3.F4)shows the human panel averages 0.19 verbosity and 0.34 erosion. Agent checkpoints sit 2.3$\times$ and 2.0$\times$ above those means. Only 18 of 473 repositories cross the agent verbosity mean. Agent verbosity grows by 0.0144 per checkpoint and erosion by 0.0264; the human medians are 0.0022 and 0.0053. Inside the iteration loop, agents accumulate verbosity roughly 7$\times$ faster and erosion 5$\times$ faster. Erosion rises in 77% of agent trajectories against 53% of human repositories.

| Group | $n$ | Verbosity | Erosion | 
|---|---|---|---|
| Hobby ($<100\bigstar$) | 114 | $0.21\pm 0.14$ | $0.33\pm 0.25$ | 
| Niche ($100\text{--}1\text{k}\bigstar$) | 124 | $0.19\pm 0.11$ | $0.32\pm 0.22$ | 
| Established ($1\text{k}\text{--}10\text{k}\bigstar$) | 120 | $0.18\pm 0.08$ | $0.33\pm 0.20$ | 
| Major ($\geq 10\text{k}\bigstar$) | 115 | $0.19\pm 0.10$ | $0.37\pm 0.19$ | 
| Human panel (all) | 473 | $0.19\pm 0.11$ | $0.34\pm 0.22$ | 
| Agent checkpoints | 2869 | $0.44\pm 0.18$ | $0.68\pm 0.20$ | 

For the 321 repositories with at least three commits in each of the pre- and post-January-2024 windows, within-repository medians shift by $+0.002$ for verbosity and $+0.014$ for erosion; 59% of these repositories are more eroded after 2024 than before. The shift is consistent with a small uptick in human-authored slop after agent assistance became common, and it remains far below what an agent accumulates in a single checkpoint. [Appendix D](#A4) extends this analysis.

### 3.4 Explicit Prompting Improves Initial Quality, But Still Degrades

We next evaluate whether prompt-side modifications can mitigate the degradation induced by iteration. Two prompts are tested against the just-solve  baseline. anti-slop ([9](#LST9)) enumerates verbosity and over-engineering patterns the agent should avoid. plan-first ([10](#LST10)) requires the agent to produce a written plan before generating code.

| Model | Prompt | Strict | Iso. | Core | Erosion | Verbosity | Cost | 
|---|---|---|---|---|---|---|---|
| GPT 5.3 Codex | Just-Solve | 11.2 | 26.0 | 60.7 | 0.64 | 0.46 | 0.66 | 
|  | Anti-Slop | 11.2 (+0.0) | 23.5 (-2.6) | 57.1 (-3.6) | 0.42 (-0.22) | 0.31 (-0.15) | 0.73 (+0.07) | 
|  | Plan-First | 8.2 (-3.1) | 21.4 (-4.6) | 62.2 (+1.5) | 0.55 (-0.10) | 0.40 (-0.06) | 0.68 (+0.02) | 
| GPT 5.4 | Just-Solve | 10.7 | 23.5 | 62.8 | 0.51 | 0.33 | 0.72 | 
|  | Anti-Slop | 9.2 (-1.5) | 25.5 (+2.0) | 61.2 (-1.5) | 0.28 (-0.23) | 0.24 (-0.09) | 0.90 (+0.18) | 
|  | Plan-First | 9.7 (-1.0) | 25.0 (+1.5) | 63.3 (+0.5) | 0.39 (-0.11) | 0.30 (-0.02) | 0.83 (+0.11) | 
| GPT 5.5 | Just-Solve | 14.8 | 28.1 | 66.8 | 0.49 | 0.32 | 1.51 | 
|  | Anti-Slop | 9.2 (-5.6) | 24.0 (-4.1) | 63.3 (-3.6) | 0.21 (-0.28) | 0.21 (-0.11) | 1.68 (+0.17) | 
|  | Plan-First | 8.2 (-6.6) | 24.0 (-4.1) | 67.3 (+0.5) | 0.29 (-0.21) | 0.25 (-0.06) | 1.61 (+0.11) | 

[Figure 5](#S3.F5)highlights that the magnitudes of structural erosion and verbosity are significantly lowered by prompt strategies. Under anti-slop, verbosity is lower than baseline by 27.5% on GPT 5.4, 35.6% on GPT 5.5, and 32.8% on GPT 5.3 Codex. Erosion is lower by 45.1%, 57.6%, and 34.3% respectively. Only with GPT 5.4 do we observe that quality *improves* from start to end with the anti-slop prompt.

This improved quality comes with some trade-offs, as highlighted in [Table 3](#S3.T3). Across models, the base just-solve prompt has the best strict performance with an average drop of 2.4 pp for anti-slop and 3.6 pp for plan-first. Core pass rate improves by 0.8 pp for plan-first. Both prompts raise the cost per checkpoint by 12.1% on average. Overall, prompting strategies trade capabilities for better initial quality, with little impact on the iterative degradation.

## 4 Related Work

##### Single-shot benchmarks.

##### Iterative and evolutionary benchmarks.

Prior iterative work severs accumulation through per-step scoring, clean prior-turn states, isolated modifications, or unchained long-horizon framing \[[70](#bib.bib19), [41](#bib.bib22), [60](#bib.bib21), [61](#bib.bib20), [74](#bib.bib67), [57](#bib.bib31)\]; [Chen et al. \[13\]](#bib.bib40) preserves history but draws from public repositories and inherits contamination risk. [Deng et al. \[20\]](#bib.bib32) chains agent code across 98 milestones with pass rates falling from 80% to 38%, yet evaluation stays pass/fail, and SLUMP \[[64](#bib.bib52)\] measures only final-artifact compliance. Verbosity and erosion require the agent’s own output to accumulate across many steps.

##### Quality degradation and code smells.

LLM code carries higher per-line cyclomatic complexity than human code, with redundant steps, duplication, and unnecessary conditionals its most prevalent smells \[[22](#bib.bib65), [1](#bib.bib63), [17](#bib.bib53)\]. Under repeated modification, outputs drift toward structural attractors, quality diverges across trajectories, and refinement introduces defects that tests miss \[[53](#bib.bib35), [15](#bib.bib29), [55](#bib.bib54), [14](#bib.bib36), [23](#bib.bib38), [11](#bib.bib57), [71](#bib.bib39), [29](#bib.bib37), [56](#bib.bib34), [43](#bib.bib30), [9](#bib.bib41)\]. Our metrics quantify these dynamics per checkpoint.

## 5 Conclusion

We present SlopCodeBench, an iterative benchmark designed to measure the quality of code produced by agents when they are forced to make design decisions. We follow explicit construction principles to create black-box problems with only external contracts described. To measure quality, we introduce structural erosion, complexity concentration, and verbosity, the fraction of code that is redundant. No agent is able to solve any of our 36 problems end-to-end, while the state-of-the-art solve rate is only 14.8% of 196 checkpoints. When forced to iterate, agents consistently degrade the codebase’s quality. In our maintained-repository calibration panel, agent checkpoints exhibit higher erosion and verbosity, and agent trajectories accumulate both metrics faster than those of sampled Python repository histories. Our analysis of prompting interventions finds that they can improve initial quality issues, but cannot stop the eroding behavior. SlopCodeBench is a first-of-its-kind iterative evaluation that allows proper investigation of how agents act when given decision autonomy.

## Acknowledgments and Disclosure of Funding

We thank Abtin Molavi, Amanda Xu, June Cho, Xavier Garcia, and Samuel Guo for feedback during the development of this project. We also thank the Terminal Bench team for their inspiration and feedback.

This work is supported by Snorkel AI through the Open Benchmarks Grants program. This work was additionally supported in part by DARPA and the NSF.

## References

- \[1\]
 (2025)
A taxonomy of inefficiencies in LLM-generated Python code.
External Links: [Document](https://dx.doi.org/10.48550/arXiv.2503.06327), [Link](https://arxiv.org/abs/2503.06327) Cited by: [Appendix E](#A5.SS0.SSS0.Px2.p1.1), [§1](#S1.p2.1), [§4](#S4.SS0.SSS0.Px3.p1.1).
- \[2\]
 (2023)
GPTCloneBench: a comprehensive benchmark of semantic clones and cross-language clones using gpt-3 model and semanticclonebench.
In 2023 IEEE International Conference on Software Maintenance and Evolution (ICSME),
Vol. , pp. 1–13.
External Links: [Document](https://dx.doi.org/10.1109/ICSME58846.2023.00013) Cited by: [§2.3](#S2.SS3.SSS0.Px2.p1.1), [§2.3](#S2.SS3.SSS0.Px3.p1.1).
- \[3\]
 (2024)
Swe-bench+: enhanced coding benchmark for llms.
arXiv preprint arXiv:2410.06992.
Cited by: [Appendix E](#A5.SS0.SSS0.Px3.p1.1), [item 2](#S2.I2.i2.p1.1).
- \[4\]
 (2025)
Claude code.
Note: CLI tool for agentic coding with Claude
External Links: [Link](https://docs.anthropic.com/en/docs/claude-code) Cited by: [§C.1](#A3.SS1.SSS0.Px3.p1.1).
- \[5\]
 (2025)
Claude opus 4.5 system card.
External Links: [Link](https://assets.anthropic.com/m/64823ba7485345a7/Claude-Opus-4-5-System-Card.pdf) Cited by: [Table 8](#A4.T8.6.1.3.1).
- \[6\]
 (2026)
Claude opus 4.6 system card.
External Links: [Link](https://anthropic.com/claude-opus-4-6-system-card) Cited by: [Table 8](#A4.T8.6.1.4.1).
- \[7\]
 (2026)
Claude opus 4.7 system card.
External Links: [Link](https://anthropic.com/claude-opus-4-7-system-card) Cited by: [Table 8](#A4.T8.6.1.5.1).
- \[8\]
 (2026)
Claude sonnet 4.6 system card.
External Links: [Link](https://anthropic.com/claude-sonnet-4-6-system-card) Cited by: [Table 8](#A4.T8.6.1.6.1).
- \[9\]
 (2026)
Novice developers produce larger review overhead for project maintainers while vibe coding.
External Links: [Link](https://arxiv.org/abs/2602.23905), [Document](https://dx.doi.org/10.48550/arXiv.2602.23905) Cited by: [Appendix E](#A5.SS0.SSS0.Px1.p1.1), [§4](#S4.SS0.SSS0.Px3.p1.1).
- \[10\]
 (2026)
SWE-rebench v2: language-agnostic swe task collection at scale.
External Links: 2602.23866,
[Link](https://arxiv.org/abs/2602.23866) Cited by: [Appendix E](#A5.SS0.SSS0.Px3.p1.1), [§1](#S1.p1.1), [item 3](#S2.I2.i3.p1.1).
- \[11\]
 (2025)
Show and tell: prompt strategies for style control in multi-turn LLM code generation.
External Links: [Document](https://dx.doi.org/10.48550/arXiv.2511.13972), [Link](https://arxiv.org/abs/2511.13972) Cited by: [Appendix E](#A5.SS0.SSS0.Px1.p1.1), [§4](#S4.SS0.SSS0.Px3.p1.1).
- \[12\]
 (2018)
Cognitive complexity — an overview and evaluation.
In 2018 IEEE/ACM International Conference on Technical Debt (TechDebt),
Vol. , pp. 57–58.
External Links: [Document](https://dx.doi.org/) Cited by: [§2.3](#S2.SS3.SSS0.Px3.p1.1).
- \[13\]
 (2026)
SWE-ci: evaluating agent capabilities in maintaining codebases via continuous integration.
External Links: 2603.03823,
[Link](https://arxiv.org/abs/2603.03823) Cited by: [§1](#S1.p3.1), [item 1](#S2.I2.i1.p1.1), [§4](#S4.SS0.SSS0.Px2.p1.1).
- \[14\]
 (2026)
SCAFFOLD-cegis: preventing latent security degradation in llm-driven iterative code refinement.
External Links: 2603.08520,
[Link](https://arxiv.org/abs/2603.08520) Cited by: [Appendix E](#A5.SS0.SSS0.Px1.p1.1), [§4](#S4.SS0.SSS0.Px3.p1.1).
- \[15\]
 (2025)
Evaluating software development agents: patch patterns, code quality, and issue complexity in real-world github scenarios.
In 2025 IEEE International Conference on Software Analysis, Evolution and Reengineering (SANER),
Vol. , pp. 657–668.
External Links: [Document](https://dx.doi.org/10.1109/SANER64311.2025.00068) Cited by: [Appendix E](#A5.SS0.SSS0.Px1.p1.1), [§1](#S1.p2.1), [§4](#S4.SS0.SSS0.Px3.p1.1).
- \[16\]
 (1994)
A metrics suite for object oriented design.
IEEE Transactions on Software Engineering 20 (6), pp. 476–493.
External Links: [Document](https://dx.doi.org/10.1109/32.295895) Cited by: [§2.3](#S2.SS3.SSS0.Px3.p1.1).
- \[17\]
 (2025)
Human-written vs. AI-generated code: a large-scale study of defects, vulnerabilities, and complexity.
External Links: [Document](https://dx.doi.org/10.48550/arXiv.2508.21634), [Link](https://arxiv.org/abs/2508.21634) Cited by: [Appendix E](#A5.SS0.SSS0.Px2.p1.1), [§4](#S4.SS0.SSS0.Px3.p1.1).
- \[18\]
 (1992)
The wycash portfolio management system.
Vol. 4, New York, NY, USA, pp. 29–30.
External Links: ISSN 1055-6400,
[Link](https://doi.org/10.1145/157710.157715), [Document](https://dx.doi.org/10.1145/157710.157715) Cited by: [Appendix E](#A5.SS0.SSS0.Px2.p1.1).
- \[19\]
 (2026)
Introducing composer 2.
External Links: [Link](https://cursor.com/blog/composer-2) Cited by: [Table 8](#A4.T8.6.1.19.1).
- \[20\]
 (2026)
EvoClaw: evaluating ai agents on continuous software evolution.
External Links: 2603.13428,
[Link](https://arxiv.org/abs/2603.13428) Cited by: [§1](#S1.p3.1), [item 1](#S2.I2.i1.p1.1), [§2.2](#S2.SS2.p1.3), [§4](#S4.SS0.SSS0.Px2.p1.1).
- \[21\]
 (2026)
NL2Repo-bench: towards long-horizon repository generation evaluation of coding agents.
External Links: 2512.12730,
[Link](https://arxiv.org/abs/2512.12730) Cited by: [Appendix E](#A5.SS0.SSS0.Px3.p1.1).
- \[22\]
 (2026)
What’s wrong with your code generated by large language models? an extensive study.
Science China Information Sciences.
External Links: [Document](https://dx.doi.org/10.1007/s11432-025-4632-8), [Link](https://arxiv.org/abs/2407.06153) Cited by: [Appendix E](#A5.SS0.SSS0.Px2.p1.1), [§1](#S1.p2.1), [§4](#S4.SS0.SSS0.Px3.p1.1).
- \[23\]
 (2026)
A differential fuzzing-based evaluation of functional equivalence in llm-generated code refactorings.
External Links: 2602.15761,
[Link](https://arxiv.org/abs/2602.15761) Cited by: [Appendix E](#A5.SS0.SSS0.Px1.p1.1), [§4](#S4.SS0.SSS0.Px3.p1.1).
- \[24\]
 (2025)
A hierarchical and evolvable benchmark for fine-grained code instruction following with multi-turn feedback.
External Links: 2507.00699,
[Link](https://arxiv.org/abs/2507.00699) Cited by: [Appendix E](#A5.SS0.SSS0.Px3.p1.1).
- \[25\]
 (2026)
LongCLI-Bench: a preliminary benchmark and study for long-horizon agentic programming in command-line interfaces.
Vol. abs/2602.14337.
External Links: [Document](https://dx.doi.org/10.48550/arXiv.2602.14337) Cited by: [Appendix E](#A5.SS0.SSS0.Px3.p1.1), [§4](#S4.SS0.SSS0.Px1.p1.1).
- \[26\]
 (1999)
Refactoring: improving the design of existing code.
 Addison-Wesley.
External Links: ISBN 978-0201485677
Cited by: [Appendix E](#A5.SS0.SSS0.Px2.p1.1).
- \[27\]
 (2013)
ISO / iec 25010 : 2011 systems and software engineering — systems and software quality requirements and evaluation ( square ) — system and software quality models.
External Links: [Link](https://api.semanticscholar.org/CorpusID:19022091) Cited by: [§2.3](#S2.SS3.p1.1).
- \[28\]
 (2024)
SWE-bench: can language models resolve real-world github issues?.
In The Twelfth International Conference on Learning Representations,
External Links: [Link](https://openreview.net/forum?id=VTF8yNQM66) Cited by: [Appendix E](#A5.SS0.SSS0.Px3.p1.1), [§1](#S1.p1.1), [item 2](#S2.I2.i2.p1.1), [§4](#S4.SS0.SSS0.Px1.p1.1).
- \[29\]
 (2026)
Are llms reliable code reviewers? systematic overcorrection in requirement conformance judgement.
External Links: 2603.00539,
[Link](https://arxiv.org/abs/2603.00539) Cited by: [Appendix E](#A5.SS0.SSS0.Px1.p1.1), [§4](#S4.SS0.SSS0.Px3.p1.1).
- \[30\]
 (2009)
Do code clones matter?.
In Proceedings of the 31st International Conference on Software Engineering,
ICSE ’09, USA, pp. 485–495.
External Links: ISBN 9781424434534,
[Link](https://doi.org/10.1109/ICSE.2009.5070547), [Document](https://dx.doi.org/10.1109/ICSE.2009.5070547) Cited by: [§2.3](#S2.SS3.SSS0.Px2.p1.1), [§2.3](#S2.SS3.SSS0.Px3.p1.1).
- \[31\]
 (2026)
Kimi k2.5: visual agentic intelligence.
External Links: 2602.02276,
[Link](https://arxiv.org/abs/2602.02276) Cited by: [Table 8](#A4.T8.6.1.22.1).
- \[32\]
 (2026)
Kimi K2.6.
External Links: [Link](https://moonshotai.com/kimi-k2.6) Cited by: [Table 8](#A4.T8.6.1.25.1).
- \[33\]
 (2020)
Code smells and refactoring: a tertiary systematic review of challenges and observations.
Journal of Systems and Software 167, pp. 110610.
External Links: ISSN 0164-1212,
[Document](https://dx.doi.org/https%3A//doi.org/10.1016/j.jss.2020.110610), [Link](https://www.sciencedirect.com/science/article/pii/S0164121220300881) Cited by: [Appendix E](#A5.SS0.SSS0.Px2.p1.1), [§1](#S1.p2.1).
- \[34\]
 (2021)
Architectural decay as predictor of issue- and change-proneness.
In 2021 IEEE 18th International Conference on Software Architecture (ICSA),
Vol. , pp. 92–103.
External Links: [Document](https://dx.doi.org/10.1109/ICSA51549.2021.00017) Cited by: [Appendix E](#A5.SS0.SSS0.Px2.p1.1), [§1](#S1.p2.1).
- \[35\]
 (2022)
Understanding software architecture erosion: a systematic mapping study.
Journal of Software: Evolution and Process 34 (3), pp. e2423.
External Links: [Document](https://dx.doi.org/https%3A//doi.org/10.1002/smr.2423), [Link](https://onlinelibrary.wiley.com/doi/abs/10.1002/smr.2423),
https://onlinelibrary.wiley.com/doi/pdf/10.1002/smr.2423
Cited by: [Appendix E](#A5.SS0.SSS0.Px2.p1.1), [§1](#S1.p2.1).
- \[36\]
 (2025)
FEA-bench: a benchmark for evaluating repository-level code generation for feature implementation.
In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers),
External Links: [Document](https://dx.doi.org/10.48550/arXiv.2503.06680) Cited by: [Appendix E](#A5.SS0.SSS0.Px3.p1.1), [§4](#S4.SS0.SSS0.Px1.p1.1).
- \[37\]
 (2025)
ProjectEval: a benchmark for programming agents automated evaluation on project-level code generation.
External Links: [Document](https://dx.doi.org/10.48550/arXiv.2503.07010) Cited by: [Appendix E](#A5.SS0.SSS0.Px3.p1.1).
- \[38\]
 (2026)
ProjDevBench: benchmarking ai coding agents on end-to-end project development.
External Links: 2602.01655,
[Link](https://arxiv.org/abs/2602.01655) Cited by: [Appendix E](#A5.SS0.SSS0.Px3.p1.1), [§1](#S1.p1.1).
- \[39\]
 (1976)
A complexity measure.
IEEE Transactions on Software Engineering SE-2 (4), pp. 308–320.
External Links: [Document](https://dx.doi.org/10.1109/TSE.1976.233837) Cited by: [§1](#S1.p4.1), [§2.3](#S2.SS3.SSS0.Px1.p1.1), [§2.3](#S2.SS3.SSS0.Px3.p1.1).
- \[40\]
 (2026)
Terminal-bench: benchmarking agents on hard, realistic tasks in command line interfaces.
In The Fourteenth International Conference on Learning Representations,
External Links: [Link](https://openreview.net/forum?id=a7Qa4CcHak) Cited by: [§C.1](#A3.SS1.SSS0.Px3.p1.1).
- \[41\]
 (2025)
RECODE-h: a benchmark for research code development with interactive human feedback.
Vol. abs/2510.06186.
External Links: [Document](https://dx.doi.org/10.48550/arXiv.2510.06186) Cited by: [§4](#S4.SS0.SSS0.Px2.p1.1).
- \[42\]
 (2026)
MiniMax M2.7: early echoes of self-evolution.
External Links: [Link](https://www.minimax.io/news/minimax-m27-en) Cited by: [Table 8](#A4.T8.6.1.26.1).
- \[43\]
 (2026)
Why agentic-PRs get rejected: a comparative study of coding agents.
External Links: [Document](https://dx.doi.org/10.48550/arXiv.2602.04226) Cited by: [Appendix E](#A5.SS0.SSS0.Px1.p1.1), [§1](#S1.p2.1), [§4](#S4.SS0.SSS0.Px3.p1.1).
- \[44\]
 (1992)
Metrics for assessing a software system’s maintainability.
In Proceedings Conference on Software Maintenance 1992,
Vol. , pp. 337–344.
External Links: [Document](https://dx.doi.org/10.1109/ICSM.1992.242525) Cited by: [§2.3](#S2.SS3.SSS0.Px3.p1.1).
- \[45\]
 (2025)
Addendum to GPT-5.2 system card: GPT-5.2-Codex.
External Links: [Link](https://openai.com/index/gpt-5-2-codex-system-card/) Cited by: [Table 8](#A4.T8.6.1.7.1).
- \[46\]
 (2025)
Codex CLI.
Note: CLI tool for agentic coding with OpenAI models
External Links: [Link](https://github.com/openai/codex) Cited by: [§C.1](#A3.SS1.SSS0.Px3.p1.1).
- \[47\]
 (2026)
GPT-5.3-Codex system card.
External Links: [Link](https://openai.com/index/gpt-5-3-codex-system-card/) Cited by: [Table 8](#A4.T8.6.1.8.1).
- \[48\]
 (2026)
GPT-5.4 thinking system card.
External Links: [Link](https://openai.com/index/gpt-5-4-thinking-system-card/) Cited by: [Table 8](#A4.T8.6.1.12.1).
- \[49\]
 (2026)
GPT-5.4 thinking system card.
Note: Includes March 17, 2026 addendum covering GPT-5.4 mini and nano
External Links: [Link](https://openai.com/index/gpt-5-4-thinking-system-card/) Cited by: [Table 8](#A4.T8.6.1.15.1).
- \[50\]
 (2026)
GPT-5.5 system card.
External Links: [Link](https://openai.com/index/gpt-5-5-system-card/) Cited by: [Table 8](#A4.T8.6.1.16.1).
- \[51\]
 (2026)
Introducing GPT-5.3-Codex-Spark.
Note: Research preview; safety coverage under the GPT-5.3-Codex System Card
External Links: [Link](https://openai.com/index/introducing-gpt-5-3-codex-spark/) Cited by: [Table 8](#A4.T8.6.1.11.1).
- \[52\]
 (1994)
Software aging.
In Proceedings of 16th International Conference on Software Engineering,
Vol. , pp. 279–287.
External Links: [Document](https://dx.doi.org/10.1109/ICSE.1994.296790) Cited by: [Appendix E](#A5.SS0.SSS0.Px2.p1.1).
- \[53\]
 (2026)
From restructuring to stabilization: a large-scale experiment on iterative code readability refactoring with large language models.
External Links: 2602.21833,
[Link](https://arxiv.org/abs/2602.21833) Cited by: [Appendix E](#A5.SS0.SSS0.Px1.p1.1), [§4](#S4.SS0.SSS0.Px3.p1.1).
- \[54\]
 (2025)
SWE-polybench: a multi-language benchmark for repository level evaluation of coding agents.
External Links: 2504.08703,
[Link](https://arxiv.org/abs/2504.08703) Cited by: [Appendix E](#A5.SS0.SSS0.Px3.p1.1), [item 3](#S2.I2.i3.p1.1), [§4](#S4.SS0.SSS0.Px1.p1.1).
- \[55\]
 (2025)
Investigating software aging in llm-generated software systems.
In 2025 IEEE 36th International Symposium on Software Reliability Engineering Workshops (ISSREW),
pp. 314–321.
External Links: [Link](http://dx.doi.org/10.1109/ISSREW67781.2025.00090), [Document](https://dx.doi.org/10.1109/issrew67781.2025.00090) Cited by: [Appendix E](#A5.SS0.SSS0.Px1.p1.1), [§4](#S4.SS0.SSS0.Px3.p1.1).
- \[56\]
 (2026)
More rounds, more noise: why multi-turn review fails to improve cross-context verification.
External Links: 2603.16244,
[Link](https://arxiv.org/abs/2603.16244) Cited by: [Appendix E](#A5.SS0.SSS0.Px1.p1.1), [§4](#S4.SS0.SSS0.Px3.p1.1).
- \[57\]
 (2026)
SWE-evo: benchmarking coding agents in long-horizon software evolution scenarios.
External Links: 2512.18470,
[Link](https://arxiv.org/abs/2512.18470) Cited by: [§1](#S1.p3.1), [§4](#S4.SS0.SSS0.Px2.p1.1).
- \[58\]
 (2026)
Vibe code bench: evaluating ai models on end-to-end web application development.
External Links: [Link](https://api.semanticscholar.org/CorpusID:286256067) Cited by: [§1](#S1.p1.1).
- \[59\]
 (2025)
CodeIF-bench: evaluating instruction-following capabilities of large language models in interactive code generation.
External Links: 2503.22688,
[Link](https://arxiv.org/abs/2503.22688) Cited by: [Appendix E](#A5.SS0.SSS0.Px3.p1.1).
- \[60\]
 (2026)
CodeFlowBench: a multi-turn, iterative benchmark for complex code generation.
External Links: 2504.21751,
[Link](https://arxiv.org/abs/2504.21751) Cited by: [§1](#S1.p3.1), [§2.2](#S2.SS2.p1.3), [§4](#S4.SS0.SSS0.Px2.p1.1).
- \[61\]
 (2026)
MaintainCoder: maintainable code generation under dynamic requirements.
In The Thirty-ninth Annual Conference on Neural Information Processing Systems,
External Links: [Link](https://openreview.net/forum?id=TIbQixHEFD) Cited by: [§2.2](#S2.SS2.p1.3), [§4](#S4.SS0.SSS0.Px2.p1.1).
- \[62\]
 (2026)
What to cut? predicting unnecessary methods in agentic code generation.
External Links: 2602.17091,
[Link](https://arxiv.org/abs/2602.17091) Cited by: [§1](#S1.p2.1).
- \[63\]
 (2026)
Evaluating and improving automated repository-level rust issue resolution with llm-based agents.
Vol. abs/2602.22764.
External Links: [Link](https://api.semanticscholar.org/CorpusID:286083036) Cited by: [Appendix E](#A5.SS0.SSS0.Px3.p1.1).
- \[64\]
 (2026)
When the specification emerges: benchmarking faithfulness loss in long-horizon coding agents.
External Links: 2603.17104,
[Link](https://arxiv.org/abs/2603.17104) Cited by: [§4](#S4.SS0.SSS0.Px2.p1.1).
- \[65\]
 (2024)
SWE-agent: agent-computer interfaces enable automated software engineering.
In The Thirty-eighth Annual Conference on Neural Information Processing Systems,
External Links: [Link](https://openreview.net/forum?id=mXpq6ut8J3) Cited by: [§3](#S3.SS0.SSS0.Px1.p1.1).
- \[66\]
 (2026)
SWE-abs: adversarial benchmark strengthening exposes inflated success rates on test-based benchmark.
External Links: 2603.00520,
[Link](https://arxiv.org/abs/2603.00520) Cited by: [§4](#S4.SS0.SSS0.Px1.p1.1).
- \[67\]
 (2026)
GLM-5.1: towards long-horizon tasks.
External Links: [Link](https://z.ai/blog/glm-5.1) Cited by: [Table 8](#A4.T8.6.1.20.1).
- \[68\]
 (2026)
Multi-SWE-bench: a multilingual benchmark for issue resolving.
In The Thirty-ninth Annual Conference on Neural Information Processing Systems Datasets and Benchmarks Track,
External Links: [Link](https://openreview.net/forum?id=MhBZzkz4h9) Cited by: [Appendix E](#A5.SS0.SSS0.Px3.p1.1), [item 3](#S2.I2.i3.p1.1), [§4](#S4.SS0.SSS0.Px1.p1.1).
- \[69\]
 (2025)
Benchmarking and studying the llm-based agent system in end-to-end software development.
External Links: 2511.04064,
[Link](https://arxiv.org/abs/2511.04064) Cited by: [Appendix E](#A5.SS0.SSS0.Px3.p1.1).
- \[70\]
 (2026)
SR-eval: evaluating llms on code generation under stepwise requirement refinement.
External Links: 2509.18808,
[Link](https://arxiv.org/abs/2509.18808) Cited by: [§4](#S4.SS0.SSS0.Px2.p1.1).
- \[71\]
 (2026)
An empirical study of interaction smells in multi-turn human-llm collaborative code generation.
External Links: 2603.09701,
[Link](https://arxiv.org/abs/2603.09701) Cited by: [Appendix E](#A5.SS0.SSS0.Px1.p1.1), [§4](#S4.SS0.SSS0.Px3.p1.1).
- \[72\]
 (2026)
SWE-agi: benchmarking specification-driven software construction with moonbit in the era of autonomous agents.
External Links: 2602.09447,
[Link](https://arxiv.org/abs/2602.09447) Cited by: [Appendix E](#A5.SS0.SSS0.Px3.p1.1).
- \[73\]
 (2024)
Commit0: library generation from scratch.
External Links: 2412.01769,
[Link](https://arxiv.org/abs/2412.01769) Cited by: [Appendix E](#A5.SS0.SSS0.Px3.p1.1), [§4](#S4.SS0.SSS0.Px1.p1.1).
- \[74\]
 (2025)
HumanEvo: an evolution-aware benchmark for more realistic evaluation of repository-level code generation.
External Links: 2406.06918,
[Link](https://arxiv.org/abs/2406.06918) Cited by: [§4](#S4.SS0.SSS0.Px2.p1.1).
- \[75\]
 (2026)
FeatureBench: benchmarking agentic coding for complex feature development.
In The Fourteenth International Conference on Learning Representations,
External Links: [Link](https://openreview.net/forum?id=41xrZ3uGuI) Cited by: [Appendix E](#A5.SS0.SSS0.Px3.p1.1).
- \[76\]
 (2025)
LessLeak-bench: a first investigation of data leakage in llms across 83 software engineering benchmarks.
External Links: 2502.06215,
[Link](https://arxiv.org/abs/2502.06215) Cited by: [§4](#S4.SS0.SSS0.Px1.p1.1).

## Appendix A Benchmark Details

### A.1 Code Search Checkpoint Specifications

This subsection provides the complete specifications for the first three checkpoints of the code\_search problem referenced in [section 2](#S2). Each specification appears exactly as presented to agents during evaluation.

#### A.1.1 Checkpoint 1: Python-only Exact and Regex Matching

#### A.1.2 Checkpoint 2: Multi-language Support with Filtering

#### A.1.3 Checkpoint 3: Structure-Aware Metavariable Patterns

| Problem | CPs | Design decisions stressed | 
|---|---|---|
| cfgpipe | 6 | Source-priority resolution, typed parsing boundaries, nested schema representation, watch and event architecture, redaction, and store-prefix composition. | 
| circuit\_eval | 8 | Circuit IR, parser separation across formats, two-valued versus three-valued logic, optimization pass pipeline, and equivalence checking. | 
| code\_search | 5 | Regex versus AST matching, metavariable representation, rewrite conflict handling, selector semantics, and language adapter boundaries. | 
| dag\_execution | 3 | DAG DSL parsing, task parameter model, execution ordering, cache key design, and per-task cache overrides. | 
| database\_migration | 5 | Migration operation model, rollback representation, dependency sorting, cycle errors, and constraint or index handling. | 
| datagate | 7 | Dataset ingestion abstraction, query and filter pipeline, pagination and export contracts, cache invalidation, runtime config, and access control. | 
| dynamic\_buffer | 4 | Example-to-transform inference, generated API shape, stateful transform classes, streaming buffers, and cache behavior. | 
| dynamic\_config\_service\_api | 4 | Versioned config storage, inheritance and deep merge rules, schema validation, approval workflow state, and policy enforcement. | 
| env\_manager | 5 | Declarative provisioning IR, OS-specific planning boundaries, deterministic output, module validation, profiles, and build-script generation. | 
| etl\_pipeline | 5 | Pipeline IR, expression language design, branching, reusable sub-pipeline parameters, and library loading. | 
| eve\_industry | 6 | SDE normalization, recipe graph representation, invention probability, ME and TE accounting, job scheduling, and recursive build planning. | 
| eve\_jump\_planner | 3 | Route graph modeling, fuel and fatigue costs, spatial distance calculations, cloak mechanics, and high-sec fallback routing. | 
| eve\_market\_tools | 4 | Market order ingestion, price-book aggregation, reprocessing yield math, hub optimization, and arbitrage or hauling profit ranking. | 
| eve\_route\_planner | 3 | Warp physics, route cost calculation, cargo manifest planning, multi-trip scheduling, and contract selection under constraints. | 
| execution\_server | 6 | Command execution boundaries, file tracking, output format abstraction, chain and hook semantics, cache keys, persistent environment concurrency, and job queue DAGs. | 
| file\_backup | 4 | Schedule schema, backup strategy abstraction, glob exclusion semantics, verification, incremental hashing, and destination layout. | 
| file\_merger | 4 | Multi-format reader abstraction, schema alignment, external sort strategy, partition and shard layout, and nested type flattening. | 
| file\_query\_tool | 5 | SQL parsing and execution planning, file table abstraction, joins, aggregation, window state, CTEs, and subquery scope. | 

| Problem | CPs | Design decisions stressed | 
|---|---|---|
| forge | 8 | Resource models for blueprints, allocations, units, modules, revision gates, strict JSON contracts, and admin access boundaries. | 
| l2m | 5 | LaTeX parsing depth, macro expansion, environment conversion rules, CLI flags, and KaTeX-compatible Markdown output. | 
| layered\_config\_synthesizer | 4 | Layer merge semantics, conflict resolution, fragment expansion, environment interpolation, multi-run manifests, and JSON Schema validation. | 
| log\_query | 5 | SQL-like grammar design, NDJSON streaming execution, aggregation and joins, schema label mapping, and subquery scope. | 
| meshctl | 8 | Declarative resource specs, persisted state shape, lifecycle and topology operations, security model, migrations, network exposure, and multi-region policy. | 
| metric\_transform\_lang | 5 | DSL parser and interpreter design, stream processing, aggregation and window state, temporal joins, and resumable execution. | 
| migrate\_configs | 5 | Rule engine design, multi-format parsing, inheritance and cycle detection, array pattern matching, relocation rules, and validation order. | 
| mocked\_http | 8 | Mock schema design, request matching, JSONPath evaluation, environment interpolation, validation strategy, and admin runtime behavior. | 
| mvvault | 6 | Versioned catalog schema handling, field-level history, sync and download boundaries, viewer routing, annotations, and auto-migration triggers. | 
| pwd\_manager | 5 | Vault storage and encryption boundary, unlock lifecycle, search and edit model, categories, clipboard integration, import or export, and locking behavior. | 
| recli | 8 | CLI command tree architecture, config inheritance, aliases, output formatting, file cache and SQLite persistence, container orchestration, upgrades, and system checks. | 
| rejector | 5 | Rate-limit scheduler, task and generation scheme abstractions, ICL setup representation, agentic tool-loop state, and multi-provider routing. | 
| sheeteval | 7 | Rule schema for grading, formula and dependency evaluation, fatal and concealed controls, threshold semantics, scenario check mode, and HTML reports. | 
| sith | 6 | Static versus interpreter-assisted analysis, symbol indexing, refactor safety, project root discovery, and environment or settings handling. | 
| test\_translator | 8 | Structured test spec parsing, generator per target language, test discovery, equality semantics, generate-before-test enforcement, and loop-as-test translation. | 
| textdrop | 6 | HTTP boundary validation, Markdown rendering, metadata and TOC extraction, static assets, auth and drain lifecycle, and storage backend abstraction. | 
| trajectory\_api | 5 | Trajectory data model, token and cost tracking, mutable updates with ETags, fork lineage, grammar parsing for tool calls, and sandboxed execution. | 
| xjq | 5 | Multi-format input detection, XPath and CSS selector dispatch, text extraction modes, file precedence, and XML or JSON output formatting. | 
| Total | 196 | 36 problems | 

## Appendix B Quality and Erosion Analysis

### B.1 Code Quality Examples

This subsection reproduces the two code\_search code fragments referenced in [subsection 2.3](#S2.SS3). [4](#LST4) illustrates structural erosion, and [5](#LST5) illustrates verbosity.

### B.2 Erosion Example: forge/main Across Eight Checkpoints

On forge, Opus 4.7’s main() grows 7$\times$ in cyclomatic complexity over 8 checkpoints, from CC 13 to CC 92, and from 38 to 240 lines. The increase is monotonic across every checkpoint. [6](#LST6) shows the $C_{1}$ implementation, a six-line argparse setup followed by a small dispatch ladder. [7](#LST7) shows the $C_{8}$ implementation, in which argparse has been removed and replaced with a manual while-loop that handles each flag in two parallel branches, one for the `--X val` form and one for `--X=val`. This pair of branches is repeated for seven flags before control passes to a nested resource-by-command dispatch ladder. No shared helper is introduced across the seven flag pairs, despite the per-flag template being uniform.

### B.3 Erosion Sensitivity

We vary the high-CC cutoff (8, 10, 12) and the size term (no size term, $\sqrt{\text{SLOC}}$, linear SLOC) around the reported erosion family. Across all nine variants, the result is stable: predictive correlation with next-checkpoint pass rate stays near zero, while predictive correlation with next-checkpoint cost stays positive.

| Metric | Pass | Cost | 
|---|---|---|
| Reported erosion | $-0.018$ | $0.167$ | 
| Best variant (CC > 12 + Linear SLOC) | $-0.136$ | $0.095$ | 
| LOC | $-0.212$ | $0.502$ | 
| Mean CC | $-0.046$ | $0.218$ | 
| Max CC | $-0.117$ | $0.356$ | 
| Clone Ratio | $-0.042$ | $0.114$ | 
| AST-grep hits / LOC | $-0.052$ | $0.151$ | 

Size-heavy baselines such as LOC and max CC remain stronger raw cost predictors, but the erosion-family conclusion does not depend on the exact threshold or size term.

## Appendix C Evaluation Setup

### C.1 Environment and Invocation

##### Harness version selection.

For each model we report the earliest publicly available harness version that supported that model and could execute the benchmark end-to-end. For older models whose launch-era harness was unavailable or incompatible, we used the nearest later compatible version.

##### Environment.

The container image installs all languages required by the problem set alongside a shared tooling baseline. We derived this baseline by identifying commands whose absence caused failures across all harnesses; commands that failed on only one harness were excluded to avoid biasing the environment toward a particular agent. Installed packages, shell history, and agent session data reset between checkpoints. The benchmark problems are language-agnostic by design, but current experiments evaluate only the Python track.

##### Invocation.

##### Reasoning effort.

For Codex we set the reasoning effort parameter to high. For Claude Code we configure the thinking-token budget via the environment variable following Anthropic’s published mapping.

### C.2 Agent Harness Versions

| Model | Harness | Version | Reasoning | 
| Opus 4.5 | Claude Code | 2.0.51 | high | 
| Opus 4.6 | Claude Code | 2.1.32 | high | 
| Sonnet 4.6 | Claude Code | 2.1.44 | high | 
| GPT 5.2 Codex | Codex CLI | 0.93.0 | high | 
| GPT 5.3 Codex | Codex CLI | 0.98.0 | high | 
| GPT 5.3 Spark | Codex CLI | 0.100.0 | high | 
| GPT 5.4 | Codex CLI | 0.110.0 | high | 
| GPT 5.4 Mini | Codex CLI | 0.110.0 | high | 
| Composer 2 | Cursor CLI | 2026.04.13-a9d7fb5 | none | 
| GLM 5.1 | Claude Code | 2.1.44 | high | 
| Kimi K2.5 | Claude Code | 2.1.44 | high | 
| Kimi K2.6 | Kimi CLI | 1.37.0 | high | 
| MiniMax M2.7 | Claude Code | 2.1.44 | high | 

### C.3 just-solve (Baseline)

The minimal baseline used for all primary evaluations. Each agent receives a Jinja template as its system prompt. The is\_continuation flag is false for the first checkpoint of a problem and true for all subsequent checkpoints. The checkpoint specification is injected verbatim via spec.

### C.4 anti\_slop

Explicitly instructs the agent to avoid verbose patterns, defensive over-engineering, and unnecessary abstractions.

### C.5 plan\_first

Requires the agent to plan its approach before writing code.

## Appendix D Results Continued

|  |  |  |  |  | Solve Rate (%) |  |  |  | Cost |  | Quality |  | 
| Model | Harness | Version | Think | Prompt | Strict | Iso. | Core | Partial | $/CKPT | Net $ | Erosion | Verbosity | 
| Opus 4.5 \[ [5](#bib.bib4)\] | Claude Code | 2.0.51 | High | Just Solve | 9.2 | 17.3 | 57.7 | 25.0 | 2.53$\pm$1.57 | 492.40 | 0.70$\pm$0.20 | 0.43$\pm$0.18 | 
| Opus 4.6 \[ [6](#bib.bib5)\] | Claude Code | 2.1.32 | High | Just Solve | 9.7 | 20.9 | 67.3 | 27.8 | 3.17$\pm$2.82 | 620.80 | 0.75$\pm$0.15 | 0.44$\pm$0.19 | 
| Opus 4.7 \[ [7](#bib.bib6)\] | Claude Code | 2.1.111 | High | Just Solve | 8.2 | 20.9 | 65.8 | 36.1 | 2.17$\pm$1.83 | 425.34 | 0.76$\pm$0.17 | 0.48$\pm$0.21 | 
| Sonnet 4.6 \[ [8](#bib.bib3)\] | Claude Code | 2.1.44 | High | Just Solve | 7.1 | 16.8 | 57.7 | 27.8 | 1.96$\pm$1.97 | 383.83 | 0.75$\pm$0.20 | 0.44$\pm$0.19 | 
| GPT 5.2 Codex \[ [45](#bib.bib8)\] | Codex CLI | 0.93.0 | High | Just Solve | 9.7 | 21.9 | 56.1 | 36.1 | 0.85$\pm$0.80 | 167.29 | 0.73$\pm$0.18 | 0.50$\pm$0.16 | 
| GPT 5.3 Codex \[ [47](#bib.bib9)\] | Codex CLI | 0.98.0 | High | Anti-Slop | 11.2 | 23.5 | 57.1 | 41.7 | 0.73$\pm$0.50 | 143.04 | 0.42$\pm$0.20 | 0.31$\pm$0.12 | 
| GPT 5.3 Codex | Codex CLI | 0.98.0 | High | Just Solve | 11.2 | 26.0 | 60.7 | 41.7 | 0.66$\pm$0.49 | 129.65 | 0.64$\pm$0.19 | 0.46$\pm$0.18 | 
| GPT 5.3 Codex | Codex CLI | 0.98.0 | High | Plan First | 8.2 | 21.4 | 62.2 | 33.3 | 0.68$\pm$0.45 | 134.03 | 0.55$\pm$0.24 | 0.40$\pm$0.17 | 
| GPT 5.3 Spark \[ [51](#bib.bib10)\] | Codex CLI | 0.100.0 | High | Just Solve | 3.1 | 8.2 | 29.1 | 11.1 | 0.20$\pm$0.41 | 37.17 | 0.68$\pm$0.19 | 0.48$\pm$0.16 | 
| GPT 5.4 \[ [48](#bib.bib11)\] | Codex CLI | 0.110.0 | High | Anti-Slop | 9.2 | 25.5 | 61.2 | 38.9 | 0.90$\pm$0.78 | 176.46 | 0.28$\pm$0.16 | 0.24$\pm$0.09 | 
| GPT 5.4 | Codex CLI | 0.110.0 | High | Just Solve | 10.7 | 23.5 | 62.8 | 36.1 | 0.72$\pm$0.51 | 141.32 | 0.51$\pm$0.19 | 0.33$\pm$0.13 | 
| GPT 5.4 | Codex CLI | 0.110.0 | High | Plan First | 9.7 | 25.0 | 63.3 | 38.9 | 0.83$\pm$0.61 | 163.65 | 0.39$\pm$0.19 | 0.30$\pm$0.12 | 
| GPT 5.4 Mini \[ [49](#bib.bib12)\] | Codex CLI | 0.110.0 | High | Just Solve | 5.1 | 13.8 | 53.1 | 22.2 | 0.45$\pm$0.35 | 89.03 | 0.66$\pm$0.17 | 0.42$\pm$0.12 | 
| GPT 5.5 \[ [50](#bib.bib13)\] | Codex CLI | 0.124.0 | High | Anti-Slop | 9.2 | 24.0 | 63.3 | 38.9 | 1.68$\pm$0.83 | 329.65 | 0.21$\pm$0.15 | 0.21$\pm$0.08 | 
| GPT 5.5 | Codex CLI | 0.124.0 | High | Just Solve | 14.8 | 28.1 | 66.8 | 50.0 | 1.51$\pm$0.81 | 295.59 | 0.49$\pm$0.20 | 0.32$\pm$0.12 | 
| GPT 5.5 | Codex CLI | 0.124.0 | High | Plan First | 8.2 | 24.0 | 67.3 | 30.6 | 1.61$\pm$0.72 | 316.26 | 0.29$\pm$0.18 | 0.25$\pm$0.12 | 
| Composer 2 \[ [19](#bib.bib14)\] | Cursor CLI | 2026.04.13-a9d7fb5 | None | Just Solve | 6.1 | 16.3 | 52.6 | 13.9 | 0.44$\pm$0.44 | 86.31 | 0.72$\pm$0.15 | 0.45$\pm$0.17 | 
| GLM 5.1 \[ [67](#bib.bib15)\] | Claude Code | 2.1.44 | High | Just Solve | 9.7 | 13.8 | 40.3 | 30.6 | 1.47$\pm$1.45 | 288.85 | 0.71$\pm$0.17 | 0.41$\pm$0.18 | 
| GLM 5.1 | OpenCode | 1.4.3 | High | Just Solve | 5.6 | 8.2 | 20.4 | 19.4 | 0.59$\pm$0.99 | 107.39 | 0.70$\pm$0.22 | 0.45$\pm$0.20 | 
| Kimi K2.5 \[ [31](#bib.bib16)\] | OpenCode | 1.4.3 | None | Just Solve | 4.6 | 8.7 | 31.6 | 16.7 | 0.53$\pm$0.80 | 104.77 | 0.71$\pm$0.18 | 0.46$\pm$0.18 | 
| Kimi K2.5 | Claude Code | 2.1.44 | High | Just Solve | 3.6 | 7.1 | 29.6 | 16.7 | 1.07$\pm$0.96 | 210.36 | 0.71$\pm$0.18 | 0.43$\pm$0.19 | 
| Kimi K2.5 | Kimi CLI | 1.37.0 | High | Just Solve | 4.6 | 9.7 | 39.8 | 19.4 | 0.33$\pm$0.25 | 63.21 | 0.72$\pm$0.20 | 0.44$\pm$0.20 | 
| Kimi K2.6 \[ [32](#bib.bib17)\] | Kimi CLI | 1.37.0 | High | Just Solve | 10.7 | 18.9 | 51.0 | 33.3 | 0.74$\pm$0.64 | 133.18 | 0.76$\pm$0.20 | 0.51$\pm$0.22 | 
| MiniMax M2.7 \[ [42](#bib.bib7)\] | Claude Code | 2.1.44 | High | Anti-Slop | 2.6 | 4.1 | 29.1 | 11.1 | 0.33$\pm$0.21 | 64.92 | 0.51$\pm$0.22 | 0.38$\pm$0.15 | 
| MiniMax M2.7 | OpenCode | 1.4.3 | None | Just Solve | 1.5 | 3.6 | 21.9 | 5.6 | 0.27$\pm$0.36 | 53.36 | 0.75$\pm$0.20 | 0.45$\pm$0.20 | 
| MiniMax M2.7 | Claude Code | 2.1.44 | High | Just Solve | 2.0 | 4.1 | 28.1 | 8.3 | 0.34$\pm$0.23 | 65.79 | 0.73$\pm$0.16 | 0.47$\pm$0.17 | 

### D.1 Human Panel construction

The temporal panel spans 473 maintained Python repositories sampled across web frameworks, scientific computing, infrastructure tools, machine-learning libraries, and command-line utilities. Repositories are stratified by GitHub star tier: Hobby ($<100\bigstar$, $n{=}114$), Niche ($100$–$1\text{k}\bigstar$, $n{=}124$), Established ($1$–$10\text{k}\bigstar$, $n{=}120$), and Major ($\geq 10\text{k}\bigstar$, $n{=}115$). For each repository we sample up to 30 source-touching commits across its history, totaling 13667 checkpoints between 1990 and 2026. Checkpoints with empty source trees or failed metric runs are dropped before analysis. Each repository’s most recent checkpoint serves as its HEAD snapshot for the calibration band reported in [subsection 3.3](#S3.SS3). [Table 2](#S3.T2) reports HEAD verbosity and erosion by tier and against agent checkpoints.

##### Pre- vs. post-ChatGPT temporal check.

The panel straddles 2022, so post-ChatGPT commits could in principle include LLM-assisted contributions. Pre-ChatGPT checkpoints ($n{=}9705$) have a median verbosity of 0.155 versus 0.166 for post-ChatGPT checkpoints ($n{=}3962$). The shift is real but small relative to the agent gap (mean verbosity 0.44). The same comparison anchored at January 2024 yields medians of 0.156 versus 0.168 for verbosity and 0.278 versus 0.319 for erosion.

##### Within-repository agent-era shift.

A cross-section across the 2024 boundary mixes new repositories in with old ones. Restricting to the 321 repositories with at least three checkpoints in each era, the median within-repository verbosity shift is $+0.002$ and the erosion shift is $+0.014$. 55% of these repositories are more verbose post-2024 and 59% are more eroded. The signal is consistent with a small uptick in human-authored slop after agent-assisted contributions became common, but it is dwarfed by the agent-side trajectory growth reported in [subsection 3.3](#S3.SS3).

##### First-to-last growth.

For repositories with at least five sampled commits, 256 of 378 ($68{}\%$) end with higher verbosity than they started, with median first-to-last growth of 36%. Erosion rises in 103 of 196 ($53{}\%$) repositories. Per-checkpoint slope is 0.0022 for verbosity and 0.0053 for erosion across the human panel, against 0.0144 and 0.0264 for agent trajectories.

##### Notable outliers.

huggingface/transformers (verbosity 0.451, erosion 0.473) and fastapi/fastapi (0.273, 0.219) are the most prominent verbosity outliers in the panel, both above the agent verbosity mean. The high transformers verbosity is driven by per-architecture file duplication (one model implementation per family). At the other end, pallets/flask (0.111, 0.209) and scikit-learn/scikit-learn (0.094, 0.407) are large, mature projects with low verbosity and middling erosion. scipy/scipy (0.145, 0.441) sits at the high end of human erosion, still well below the agent mean.

## Appendix E Extended Related Work

##### Quality degradation under multi-turn coding.

LLM-generated code degrades under repeated modification. Code converges toward structural attractors \[[53](#bib.bib35)\], quality diverges across agents and runs \[[15](#bib.bib29), [55](#bib.bib54), [11](#bib.bib57)\], and refinement introduces defects that correctness testing does not catch \[[14](#bib.bib36), [23](#bib.bib38)\]. Interaction failure modes compound these effects \[[71](#bib.bib39), [29](#bib.bib37), [56](#bib.bib34)\]; agent-generated code has become a practical integration burden \[[43](#bib.bib30), [9](#bib.bib41)\].

##### Code quality metrics.

LLM code has higher cyclomatic complexity per line than human-written code \[[22](#bib.bib65)\], though aggregate CC can fall while vulnerabilities rise \[[17](#bib.bib53)\]. [Abbassi et al. \[1\]](#bib.bib63) extend the code smell taxonomy to LLM outputs, finding redundant steps, duplication, and unnecessary conditionals most prevalent. Code smells are well-studied in software engineering \[[26](#bib.bib59), [33](#bib.bib56)\]; software aging \[[52](#bib.bib61)\] and technical debt \[[18](#bib.bib60)\] describe how structural degradation accumulates under modification, with [Li et al. \[35\]](#bib.bib55) and [Le et al. \[34\]](#bib.bib64) documenting this in long-lived systems.

##### Benchmark landscape.

Beyond the paradigm established by [Jimenez et al. \[28\]](#bib.bib27), the evaluation landscape spans three waves. The first broadens language and domain coverage through extensions \[[3](#bib.bib46), [68](#bib.bib45), [63](#bib.bib47), [10](#bib.bib48), [54](#bib.bib43)\]. Instruction-following benchmarks evaluate compliance across conversation turns \[[59](#bib.bib25), [24](#bib.bib23)\] but assess each response independently. A second wave targets feature-level development from existing repositories \[[36](#bib.bib26), [75](#bib.bib71)\]. A third wave builds entire projects from scratch: [Zhao et al. \[73\]](#bib.bib66) generate libraries from specifications with interactive test feedback, several benchmarks construct full repositories from natural-language requirements \[[38](#bib.bib24), [69](#bib.bib68), [21](#bib.bib69), [72](#bib.bib70), [37](#bib.bib44)\], and [Feng et al. \[25\]](#bib.bib49) spans from-scratch construction through refactoring. Tasks grow larger and harder across all three waves; evaluation in each case is a single artifact assessed against a fixed specification.
