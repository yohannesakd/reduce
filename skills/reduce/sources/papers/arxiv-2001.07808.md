# A Comprehensive Study of Bloated Dependencies in the Maven Ecosystem

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: César Soto-Valero, Nicolas Harrand, Martin Monperrus, Benoit Baudry
- Date: 2020-01-21
- Original location: https://arxiv.org/abs/2001.07808v1
- Copied: 2026-11-20, from the arXiv HTML full text, converted to Markdown with trafilatura

## Text
# A Comprehensive Study of Bloated Dependencies in

the Maven Ecosystem

###### Abstract

Build automation tools and package managers have a profound influence on software development. They facilitate the reuse of third-party libraries, support a clear separation between the application’s code and its external dependencies, and automate several software development tasks. However, the wide adoption of these tools introduces new challenges related to dependency management.
In this paper, we propose an original study of one such challenge: the emergence of *bloated dependencies*.

Bloated dependencies are libraries that the build tool packages with the application’s compiled code but that are actually not necessary to build and run the application. This phenomenon artificially grows the size of the built binary and increases maintenance effort. We propose a tool, called DepClean, to analyze the presence of bloated dependencies in Maven artifacts. We analyze $9,639$ Java artifacts hosted on Maven Central, which include a total of $723,444$ dependency relationships. Our key result is that $75.1\%$ of the analyzed dependency relationships are bloated. In other words, it is feasible to reduce the number of dependencies of Maven artifacts up to $1/4$ of its current count. We also perform a qualitative study with $30$ notable open-source projects. Our results indicate that developers pay attention to their dependencies and are willing to remove bloated dependencies: $18$/$21$ answered pull requests were accepted and merged by developers, removing $131$ dependencies in total.

###### Keywords:

Dependency management Software reuse Debloating Program analysis
## 1 Introduction

Software reuse, a long time advocated software engineering practice [Naur and Randell (1969)](#bib.bib28); [Krueger (1992)](#bib.bib18), has boomed in the last years thanks to the widespread adoption of build automation and package managers [Cox (2019)](#bib.bib9).
Package managers provide both a large pool of reusable packages, a.k.a. libraries, as well as systematic ways to declare what are the packages on which an application depends. Examples of such package management systems include Maven for Java, npm for Node.js, or Cargo for Rust. Build tools automatically fetch all the packages that are needed to compile, test, and deploy an application.

Package managers boost software reuse by creating a clear separation between the application and its third-party dependencies. Meanwhile, they introduce new challenges for the developers of software applications, who now need to manage those third-party dependencies [Cox (2019)](#bib.bib9) to avoid entering into the so-called “dependency hell”. These challenges relate to ensuring high quality dependencies [Salza et al. (2019)](#bib.bib35), maintaining the dependencies up-to-date [Bavota et al. (2015)](#bib.bib3), or making sure that heterogeneous licences are compatible [Wu et al. (2017)](#bib.bib42).

Our work focuses on one specific challenge of dependency management: the existence of *bloated dependencies*. This refers to packages that are declared as dependencies for an application, but that are actually not necessary to build or run it. The major issue with bloated dependencies is that the final deployed binary file includes more code than necessary: an artificially large binary is an issue when the application is sent over the network (e.g., web applications) or it is deployed on small devices (e.g., embedded systems). Bloated dependencies could also embed vulnerable code that can be exploited, while being actually useless for the application [Gkortzis et al. (2019)](#bib.bib12). Overall, bloated dependencies needlessly increase the difficulty of managing and evolving software applications.

We propose a novel, unique, and large scale analysis about bloated dependencies.
So far, research on bloated dependencies has been only touched with a study of copy-pasted dependency declarations by McIntosh and colleagues [McIntosh et al. (2014)](#bib.bib25). Our previous work gives preliminary results on this topic in the context of Java [Harrand et al. (2019)](#bib.bib13). To our knowledge, there is no systematic analysis of the presence of bloated dependencies nor about the importance of this problem for developers.

Our work focuses on Maven, the most popular package manager and automatic build system for Java and languages that compile to the JVM. In Maven, developers declare dependencies in a specific file, called the POM file. In order to analyze thousands on artifacts on Maven Central, the largest repository of Java artifacts, manual analysis is not a feasible solution. To overcome this problem, we have designed and implemented a tool called DepClean, that performs an automatic analysis of dependencies usage in Maven projects. Given an application and its POM file, DepClean collects the complete dependency tree (the list of dependencies declared in the POM, as well as the transitive dependencies) and analyzes the bytecode of the artifact and all its dependencies to determine the presence of bloated dependencies. Finally, DepClean generates a variant of the POM in which bloated dependencies are removed.

Armed with DepClean, we structure our analysis of bloated dependencies in two parts. First, we automatically analyse $9,639$ artifacts and their $723,444$ dependencies. We found that $75.1\%$ of these dependencies are bloated, mostly due to transitive dependencies and the complexities of dependency management in multi-module projects. Second, we perform a user study involving $30$ artifacts, for which the code is available as open-source on GitHub and which are actively maintained. For each project, we use DepClean to generate a POM file without bloated dependencies and submitted the changes as a pull request to the project. Notably, our work yielded $18$ merged pull requests by open-source developers and $131$ bloated dependencies were removed.

To summarize, this paper makes the following contributions:

- • 
A comprehensive study of bloated dependencies in the context of the Maven package manager. We are the first to quantify the magnitude of bloat on a large scale ($9,639$ Maven artifacts) showing that $75.1\%$ of dependencies are bloated.
- • 
A tool called DepClean to automatically analyze and remove bloated dependencies in Java applications packaged with Maven. DepClean can be used in future research on package management as well as by practitioners.
- • 
A qualitative assessment of the opinion of developers regarding bloated dependencies. Through the submission of pull requests to notable open-source projects, we show that developers care about removing dependency bloat: $18$/$21$ of answered pull requests have been merged, removing $131$ bloated dependencies.

The remainder of this paper is structured as follows. [Section 2](#S2) introduces the key concepts about dependency management with Maven and presents a illustrative example. [Section 3](#S3) introduces the new terminology and describes the implementation of DepClean. [Section 4](#S4) presents the research questions that drive our study, as well as the methodology followed. [Section 5](#S5) covers our experimental results for each research question. Sections [6](#S6) and [7](#S7) provide a comprehensive discussion of the results obtained and present the threats to the validity of our study. Section [8](#S8) concludes this paper and provides future research directions.

## 2 Background

In this section, we provide an overview of the Maven package management system and present the essential terminology for this work. Then, we illustrate these concepts with a concrete example.

### 2.1 Maven Dependency Management Terminology

Maven is a popular package manager and build automation tool for Java projects and other languages that compile to the JVM (e.g., Scala, Kotlin, Groovy, Clojure, or JRuby). Maven supports developers in the management of the software build, from compilation to deployment ([Varanasi and Belida, 2014](#bib.bib40)). Maven relies on a specific configuration file in XML format, known as the POM (acronym for “Project Object Model”), that allows customizing all the build lifecycle. This POM file contains information about the project and all the configuration details utilized by Maven during its different building phases (e.g., *compile*, *test*, *package*, *install*, and *deploy*). As in object-oriented programming, POM files can inherit from a base POM, known as the Maven parent POM.

Maven Project.
A Maven project is a set of source code files and configuration files. There are two ways of designing a Maven project: as a *single-module*, or as a *multi-module* project. The first has a single POM file, which may include all the configurations needed to package the project as a single artifact (JAR file). The latter allows to separately build multiple artifacts in a certain specific order through a so-called aggregator POM. In multi-module projects, developers can define in a common parent POM the dependencies used by all the modules, this facilitates the update of dependency versions at once. The Maven *reactor algorithm*<sup>1</sup><sup>1</sup>
              1
              
              
              
            [https://maven.apache.org/guides/mini/guide-multiple-modules.html](https://maven.apache.org/guides/mini/guide-multiple-modules.html) ensures a deterministic build order in multi-module projects.

Maven Artifact. In this paper, we refer to *artifacts* as compiled Maven projects that have been deployed to some external binary code repository for later reuse. In Maven, artifacts are typically packaged as JAR files, which contain Java bytecode, incl. public API members. Each artifact is uniquely identified with a triplet ($G$:$A$:$V$), where $G$ is the groupId that identifies the organization that develops the artifact, $A$ is the artifactId that identifies the name of the library (or the module in the case of multi-module projects), and $V$ corresponds to its version, which follows the Maven versioning scheme<sup>2</sup><sup>2</sup>
              2
              
              
              
            [https://maven.apache.org/pom.html#Version\_Order\_Specification](https://maven.apache.org/pom.html#Version_Order_Specification). Currently, the most popular public repository to host Maven artifacts is the Maven Central repository. Artifacts in Maven Central are immutable, i.e., once deployed, they cannot be modified nor updated. Accordingly, all the versions of a given library remain permanently available in the repository [Soto-Valero et al. (2019)](#bib.bib39).

Dependency Resolution.
The dependency resolution mechanism is a core feature of Maven. It works in two steps:
(1) it determines the set of dependencies required to build an individual artifact, and
(2) it fetches dependencies that are not present locally from external repositories such as Maven Central. Maven constructs a *dependency tree*, which represents the dependency relationships between the POMs of the resolved dependencies. One can distinguish between three types of Maven dependencies: direct, inherited, and transitive. Direct dependencies are those explicitly declared in the POM file of the project or of the module. Inherited dependencies are those declared in the parent POM. Transitive dependencies are those dependencies obtained from the transitive closure of direct and inherited dependencies. Maven relies on the *dependency mediation algorithm*<sup>3</sup><sup>3</sup>
              3
              
              
              
            [https://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html](https://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html) to determine what version of an artifact is chosen when multiple versions of the same dependency are present in the dependency tree.

### 2.2 A Brief Journey in the Dependencies of the Jxls Library

In this section, we illustrate the concepts introduced previously with one concrete example:
Jxls <sup>4</sup><sup>4</sup>
              4
              
              
              
            [http://jxls.sourceforge.net](http://jxls.sourceforge.net), an open source Java library for generating Excel reports. Jxls uses a special XLS template markup to define the output formatting and data layout for the reports. It is implemented as a multi-module Maven project with a parent POM: jxls-project, composed of three modules: jxls, jxls-examples, and jxls-poi.

[1](#LST1)shows an excerpt of the POM file of the jxls-poi module, version $1.0.15$. It declares jxls-project as its parent POM in lines $1-5$ and a direct dependency towards the poi Apache library in lines $10-14$. [Figure 1](#S2.F1) depicts an excerpt of its Maven dependency tree (we do not show testing dependencies here, such as JUnit, to make the figure more readable). Nodes in blue, pink, and yellow represent direct, inherited, and transitive dependencies, respectively, for the jxls-poi artifact (as reported by the dependency:tree Maven plugin). As we observe, it explicitly declares three direct dependencies: commons-jexl, jxls, and poi, while artifacts jcl-over-slf4j and slf4j-api are inherited dependencies of jxls-poi because they are declared in its parent POM. Since the artifact poi depends on Apache commons-codec and Apache commons-collections4, these artifacts are automatically added to the classpath of jxls-poi as transitive dependencies.

The library jcl-over-slf4j declares a dependency towards slf4j-api, version 1.7.12, which is omitted by Maven since it is already added from the jxls-project parent POM. On the other hand, Jxls declares dependencies to version 1.7.26 of jcl-over-slf4j and slf4j-api, but the lower version 1.7.12 was chosen over it since it is nearer to the root in the dependency tree and, by default, Maven resolves version conflicts with a nearest-wins strategy. Once Maven finishes the dependency resolution, the classpath of jxls-poi includes the following artifacts: poi, commons-codec, commons-collections4, commons-jexl, commons-logging, jxls, commons-jex13, commons-beanutils, commons-collections, logback-core, jcl-over-slf4j, and slf4j-api. The goal of our work is to determine if all the artifacts in the classpath of Maven projects such as jxls-poi are actually needed to build and run those projects.

## 3 Bloated Dependencies

In this section, we introduce the key concept presented and studied in the rest of this paper: bloated dependencies. Then we describe our methodology to study bloated dependencies, as well as our tooling to automatically detect and remove them from Maven projects.

### 3.1 Novel Concepts

Dependencies among Maven artifacts form a graph, according to the information declared in their POMs. The Maven Dependency Graph (MDG) is defined as follows:

###### Definition 1

(Maven Dependency Graph) The MDG is a vertex-labelled graph, where vertices are Maven artifacts (uniquely identified by their $G$:$A$:$V$ coordinates), and edges represent dependency relationships among them. Formally, the MDG is defined as $\mathcal{G=(\mathcal{V},\mathcal{E})}$, where:

- • 
$\mathcal{V}$ is the set of artifacts in the Maven Central repository
- • 
$\mathcal{E}\subseteq\mathcal{V}\times\mathcal{V}$ represent the set of directed edges that determine dependency relationships between each artifact $v\in\mathcal{V}$ and its dependencies

Each artifact in the MDG has its own Maven Dependency Tree (MDT), which is the transitive closure of all the dependencies needed to build the artifact, as resolved by Maven.

###### Definition 2

(Maven Dependency Tree) The MDT of an artifact $v\in\mathcal{V}$ is a directed acyclic graph of artifacts, with $v$ as the root node, and a set of edges $\mathcal{E}$ representing dependency relationships between them.

In this work, we introduce the novel concept of *bloated dependency* as follows:

###### Definition 3

(Bloated Dependency) An artifact $p$ is said to have a bloated dependency relationship $\varepsilon_{b}\in\mathcal{E}$ if there is a path in its MDT, between $p$ and any dependency $d$ of $p$, such as none of the elements in the API of $d$ are used, directly or indirectly, by $p$.

In order to reason about bloated dependencies, we extend the MDT to model the dependency trees of Maven artifact depending on usage relationships. To do so, we introduce edge labels to represent two types of dependency edge statuses: used or bloated. Consequently, we define the Dependency Usage Tree (DUT) as follows:

###### Definition 4

(Dependency Usage Tree) The DUT, defined as $\mathcal{G=(\mathcal{V},\mathcal{E},\mathcal{r})}$, is an extension of the MDG that implements a dependency usage labelling function, which assigns one of the following six dependency usage types to the relationship between Maven artifacts and their dependencies in the MDT: $\mathcal{r}:\mathcal{E}\rightarrow\{\text{ud, ui, ut, bd, bi, bt}\}$ such that:

|  | $$ \mathcal{r}(\langle p,d\rangle)=\begin{cases}\text{ud},&\text{if }d\text{ is used and it is directly declared by }p\\ \text{ui},&\text{if }d\text{ is used and it is inherited from a parent of }p\\ \text{ut},&\text{if }d\text{ is used and it is resolved transitively by }p\\ \text{bd},&\text{if }d\text{ is bloated and it is directly declared by }p\\ \text{bi},&\text{if }d\text{ is bloated and it is inherited from a parent of }p\\ \text{bt},&\text{if }d\text{ is bloated and it is resolved transitively by }p\\ \end{cases} $$ |  | 

### 3.2 Example

[Figure 2](#S3.F2)illustrates how the dependency usage function creates a DUT for the example presented in [Figure 1](#S2.F1). If we analyze the bytecode contained in jxls-poi, no references to any API member in the direct dependencies commons-jexl (explicitly declared in the POM) and sl4j (inherited from its parent POM) can be found. Therefore, according to [4](#Thmdefinition4), they are labelled as bloated-direct (bd) and bloated-inherited (bi) dependencies, respectively. According to the bytecode usage analysis, the direct dependency commons-jexl can be safely removed directly from the POM, while the inherited dependency sl4j can be safely removed in the parent. Indeed, after analyzing the Git history of Jxls, we found that these changes were made in the POM by the authors of the project in a later released version of this library<sup>5</sup><sup>5</sup>
              5
              
              
              
            https://bitbucket.org/leonate/jxls/commits/607c10e84336e08b5ba9fd12a21b3f450cf733d3#chg-jxls-poi/pom.xml.

Now let us consider dependencies obtained transitively through the Maven dependency resolution mechanism. commons-codec and commons-collections are included by transitive closure from jxls-poi, but they are never used, directly in its bytecode or indirectly through a used API member of its dependencies. Therefore, these bloated-transitive (bt) dependencies are not necessary to build jxls-poi.

To sum up, the set of dependencies of a given Maven artifact can be partitioned into six dependency usage types, according to two criteria: (1) the dependency usage status (used or bloated), and (2) the dependency type (direct, inherited, or transitive). [Table 1](#S3.T1) summarizes this partition for jxls-poi.

[Subsection 2.2](#S2.SS2).

|  | Used | Bloated | 
| Direct | poi, jxls | commons-jexl | 
| Inherited | jcl-over-sl4j | sl4j-api | 
| Transitive | commons-beanutils,logback-core, | commons-logging, commons-collections, | 
|  | commons-collections4 | commons-codec, commons-jexl3 | 

### 3.3 DepClean: A Tool for Detecting and Removing Bloated Dependencies

For our study, we design and implement a specific tool called DepClean. An overview of DepClean is shown in [Figure 3](#S3.F3), it works as follows. It receives as inputs a built Maven project and a repository of artifacts, then it extracts the dependency tree of the projects and constructs a DUT to identify the set of dependencies that are actually used by the project. DepClean has two outputs:
(1) it returns a report with the usage status of all types of dependencies, and (2) it produces an alternative version of the POM file ($\text{{POM}{} }_{d}$) with all the bloated dependencies removed (i.e., the XML node of the bloated dependency is removed).

Algorithm [1](#alg1) details the main procedure of DepClean. The algorithm receives as input a Maven artifact $p$ that includes a set of dependencies in its dependency tree, denoted as $DT$, and returns a report of the usage status of its dependencies and a debloated version of its POM. Notice that DepClean computes two transitive closures: over the Maven dependency tree (line [1](#alg1)) and over the call graph of API members (line [1](#alg1)).

The algorithm first copies the POM file of $p$, resolving all its direct and transitive dependencies locally, and obtaining the dependency tree (lines [1](#alg1) and [1](#alg1)). If $p$ is a module of a multi-module project, then all the dependencies declared in its parent POM are included as direct dependencies of $p$.
Then, the algorithm proceeds to construct a set with the dependencies that are actually used by $p$ (line [1](#alg1)).

Algorithm [2](#alg2) explains the bytecode analysis. The detection component statically analyzes the bytecode of $p$ and all its dependencies to check which API members are being referenced by the artifact, either directly or indirectly. Notice that it behaves differently if the included artifact is a direct, inherited, or a transitive dependency. If none of the API members of a dependency $d\in DT$ are called, even indirectly via transitive dependencies, then $d$ is considered to be bloated and we proceed to remove it.

In Maven, we remove bloated dependencies in two different ways: (1) if the bloated dependency is explicitly declared in the POM, then we remove its declaration clause directly (line [1](#alg1) in Algorithm [1](#alg1)),
or (2) if the bloated dependency is inherited from a parent POM or induced transitively, then we excluded it in the POM (line [1](#alg1) in Algorithm [1](#alg1)). This exclusion consists in adding an \<exclusion> clause inside a direct dependency declaration, with the *groupId* and *artifactId* of the transitive dependency to be excluded. Excluded dependencies are not added to the classpath of the artifact by way of the dependency in which the exclusion was declared.

DepClean is implemented in Java as a Maven plugin that extends the maven-dependency-analyzer<sup>6</sup><sup>6</sup>
                6
                
                
                
              [http://maven.apache.org/shared/maven-dependency-analyzer](http://maven.apache.org/shared/maven-dependency-analyzer) tool maintained by the Apache foundation. For the construction of the dependency tree, DepClean relies on the maven-dependency-plugin with the copy-dependencies and tree goals. Internally, DepClean addresses some of the key aspects of static analysis in Java. It relies on the ASM<sup>7</sup><sup>7</sup>
              7
              
              
              
            [https://asm.ow2.io](https://asm.ow2.io) library to visit all the .class files in order to register bytecode calls towards classes, methods, fields, and annotations among Maven artifacts.
To do so, we define a customized parser that reads entries in the constant pool table of .class files directly, in case it contains special references that ASM does not support. This allows the plugin to statically capture reflection calls that are based on string literals and concatenations.
DepClean adds unique features to the maven-dependency-analyzer to detect and report transitive and inherited bloated dependencies, and to produce a debloated version of the POM file. DepClean is open-source and reusable from Maven Central, the source code is available at [https://github.com/castor-software/depclean](https://github.com/castor-software/depclean).

## 4 Experimental Methodology

In this section, we present the research questions that articulate our study. We also describe the experimental protocols used to select and analyze Maven artifacts for an assessment of the impact of bloated dependencies in this ecosystem.

### 4.1 Research Questions

Our investigation of bloated dependencies in the Maven ecosystem is composed of four research questions grouped in two parts. In the first part, we perform a large scale quantitative study to answer the following research questions:

- • 
RQ1: How frequently do bloated dependencies occur? With this research question, we aim at quantifying the amount of bloated dependencies among $9,639$ Maven artifacts. We measure direct, inherited and transitive dependencies to provide an in-depth assessment of the dependency bloat in the Maven ecosystem.
- • 
RQ2: How do the reuse practices affect bloated dependencies? In this research question, we analyze bloated dependencies with respect to two distinctive aspects of reuse in the Maven ecosystem: the additional complexity of the Maven dependency tree caused by transitive dependencies, and the choice of a multi-module architecture.

The second part of our study focuses on $30$ notable Maven projects and presents the qualitative feedback about how developers react to bloated dependencies, and to the solutions provided by DepClean. It is guided by the following research questions:

- • 
RQ3: To what extent are developers willing to remove bloated-direct dependencies? Direct dependencies are those that are explicitly declared in the POM. Hence, those dependencies are easy to remove since it only requires the modification of a POM that developers can easily change. In this research question, we use DepClean to detect and fix bloated-direct dependencies. Then, we communicate the results to the developers. We report on their feedback.
- • 
RQ4: To what extent are developers willing to exclude bloated-transitive dependencies? Transitive dependencies are those not explicitly declared in the POM but induced from other dependencies. We exchange with developers about such cases. This gives unique insights about how developers react to excluding transitive dependencies from their projects.

### 4.2 Experimental Protocols

#### 4.2.1 Protocol of the Quantitative Study (RQ1 & RQ2)

[Figure 4](#S4.F4)shows our process to build a dataset of Maven artifacts in order to answer RQ1 and RQ2. Steps 
①
 and 
②
 focus on the collection of a representative set of Maven artifacts: we sample our study subjects from the whole Maven Dependency Graph, then we resolve the dependencies of each study subject. In steps 
③
 and 
④
, we analyze dependency usages with DepClean and compute the set of metrics to answer RQ1 and RQ2.

①

Filter artifacts.
In the first step, we leverage the Maven Dependency Graph (MDG) from previous research ([Benelallam et al., 2019](#bib.bib4)), a graph database that captures the complete dependency relationships between artifacts in Maven Central at a given point in time. Then, we randomly select a representative sample of $14,699$ Maven artifacts. Representativeness is achieved by sampling over the probability distribution of the number of dependencies per artifact in the MDG, per the recommendation of Shull  ([Shull et al., 2007](#bib.bib38), Chapter 8.3.1). From the sampled artifacts, we select as study subjects all the artifacts that meet the following additional criteria. This results in a dataset of $9,639$ artifacts.

- • 
Public API: The subjects must contain at least one .class file with one or more public methods, i.e., can be reused via external calls to their API.
- • 
Diverse: The subjects all have different *groupId* and *artifactId*, i.e., they belong to different Maven projects.
- • 
Reused: The subjects are used by at least one client via direct declaration.
- • 
Complex: The subjects have at least one direct dependency with *compile* scope, i.e., we can analyze the dependency tree and the reused artifacts.
- • 
Latest: The subjects are the latest released version at the time of the experiment (October, 2019).

②

Resolve dependencies. In the second step, we download the binaries of all the selected artifacts and their POMs from Maven Central and we resolve all their direct and transitive dependencies to a local repository. To ensure the consistency of our analysis, we discard the artifacts that depend on libraries hosted in external repositories. In case of any other error when downloading some dependency, we exclude the artifact from our analysis.

[Table 2](#S4.T2)shows the descriptive statistics about $9,639$ artifacts in our dataset for RQ1 and RQ2. The dataset includes $44,488$ direct, $180,693$ inherited, and $498,263$ transitive dependency relationships ($723,444$ in total). We report about their dependencies with *compile* scope, since those dependencies are necessary to build the artifacts. Columns #C, #M, and #F give the distribution of the number of classes, methods, and fields per artifact (we count both the public and private API members). The size of artifacts varies, from small artifacts with one single class (e.g., org.elasticsearch.client:transport:6.2.4), to large libraries with thousands of classes (e.g., org.apache.hive:hive-exec:3.1.0). In total, we analyze the bytecode of more than $30$ millions of API members. Columns #D, #I, and #T accounts for the distributions of direct, inherited, and transitive dependencies, respectively. com.bbossgroups.pdp:pdp-system:5.0.3.9 is the artifact with the largest number of declared dependencies in our dataset, with $148$ dependency declarations in its POM file, while be.atbash.json:octopus-accessors-smart:0.9.1 has the maximum number of transitive dependencies: $1,776$. Interestingly, the distributions of direct and transitive dependencies are notably different, the total number of transitive dependencies is an order of magnitude larger than direct dependencies, with mean of $20$ and $4$, respectively.

|  | API Members |  |  | Dependencies |  |  | 
|  | #C | #M | #F | #D | #I | #T | 
| Min. | $1$ | $1$ | $0$ | $1$ | $0$ | $0$ | 
| 1st-Q | $10$ | $63$ | $21$ | $2$ | $0$ | $6$ | 
| Median | $32$ | $231$ | $75$ | $4$ | $2$ | $20$ | 
| 3rd-Q | $111$ | $891$ | $279$ | $7$ | $18$ | $59$ | 
| Max. | $47,241$ | $435,695$ | $129,441$ | $148$ | $453$ | $1,776$ | 
| Total | $2,397,879$ | $22,633,743$ | $6,510,584$ | $44,488$ | $180,693$ | $498,263$ | 

③

Dependency usage analysis.
This is the first step to answer RQ1 and RQ2: collect the status of all dependency relationships for each artifact in our dataset.
For each artifact, we first unpack its JAR file, as well as its dependencies. Then, for each JAR file, we analyze all the bytecode calls to API class members using DepClean. This provides a Dependency Usage Tree (DUT) for each artifact, on which each dependency relationship is labeled with one of the six categories as we illustrated in [Table 1](#S3.T1): bloated-direct (bd), bloated-inherited (bi), bloated-transitive (bt), used-direct (ud), used-inherited (ui), or used-transitive (ut).

④

Collect dependency usage metrics. This last step consists of collecting a set of metrics about the global presence of bloated dependencies. We focus on the presence of bloat with respect to the complexity of the Maven dependency trees, and with respect to the multi-module Maven architecture.

In RQ1, we analyze our dataset as a whole, looking at the usage status of dependency relationships from two perspectives.

*Global distribution of dependency usage.* This is the normalized distribution of each category of dependency usage, over each dependency relationship of each of the $9,639$ artifacts in our dataset.

*Distribution of dependency usage type, per artifact.* For each of the six types of dependency usage, we compute the normalized ratio over the total number of dependency relationships for each artifact in our dataset.

In RQ2, we analyze how the specific reuse strategies of Maven relate to the presence of bloated dependencies. First, we relate bloated dependencies to the complexity of the Maven dependency tree of each artifact, according to the following metrics.

*Bloated dependencies w.r.t. the number of transitive dependencies.* For each artifact that has at least one transitive dependency, we determine the relation between the ratio of transitive dependencies and the ratio of bloated dependencies.

*Bloated-transitive dependencies w.r.t. to the height of the dependency tree.* Given an artifact and its Maven dependency tree, the height of the tree is the longest path between the root and its leaves. To compute this metric, we group our artifacts according to the height of their tree. The maximum dependency tree height that we observed is 14. However, there are only 58 artifacts with a tree higher than 10. So, we group all artifacts with height $\geq 10$. For each subset of artifact with the same height, we compute the size of the subset and the distribution of bloated-transitive dependencies of each artifact in the subset.

Second, we distinguish the presence of bloated dependencies between single and multi-module Maven projects, according to the following metrics:

*Global distribution of dependency usage in a single or multi-module project.* We present two plots that measure the distribution of each type of dependency usage in the set of single and multi-module projects. It is to be noted that the plot for single-module projects does not include bloated-inherited (bi) and used-inherited (ui) dependencies since they have no inherited dependencies.

*Distribution of dependency usage type, per artifact, in a single or multi-module project.* We present two plots that provide six distributions each: the distribution of each type of dependency usage type for artifacts that are in a single-module or multi-module project.

#### 4.2.2 Protocol of the Qualitative Study (RQ3 & RQ4)

In RQ3 and RQ4, we perform a qualitative assessment about the relevance of bloated dependencies for the developers of open-source projects. We systematically select $30$ notable open-source projects hosted on GitHub to conduct this analysis. We query the GitHub API to list all the Java projects ordered by their number of stars. Then, we randomly select a set of projects that fulfil all the following criteria: ($1)$ we can build them successfully with Maven, ($2)$ the last commit was at the latest in October 2019, ($3)$ they declare at least one dependency in the POM, ($4)$ they have a description in the README about how to contribute through pull requests, and ($5)$ they have more than $100$ stars on GitHub.

[Table 3](#S4.T3)shows the selected $30$ projects per those criteria, to which we submitted at least one pull request. They are listed in decreasing order of stars on GitHub. The first column shows the name of the project as declared on GitHub, followed by the name of the targeted module if the project is multi-module. Notice that in the case of jenkins we submitted two pull requests targeting two distinct modules: core and cli. Columns two to four describe the projects according to its category as assigned to the corresponding released artifact in Maven Central, the number of commits in the master branch in October 2019, and the number of starts at the moment of conducting this study. Columns five to seven report about the total number of direct, inherited, and transitive dependencies included in the dependency tree of each considered project.

| Project | Description |  |  | Dependencies |  |  | 
|  | Category | #Commits | #Stars | #D | #I | #T | 
| jenkins \[core\] | Automation Server | 29,040 | 14,578 | 51 | 2 | 87 | 
| jenkins \[cli\] | Automation Server | 29,040 | 14,578 | 17 | 2 | 0 | 
| mybatis-3 \[mybatis\] | Relational Mapping | 3,145 | 12,196 | 23 | 0 | 51 | 
| flink \[core\] | Streaming | 19,789 | 11,260 | 14 | 10 | 34 | 
| checkstyle \[checkstyle\] | Code Analysis | 8,897 | 8,897 | 18 | 0 | 36 | 
| auto \[common\] | Meta-programming | 1,081 | 8,331 | 8 | 0 | 24 | 
| neo4j \[collections\] | Graph Database | 66,602 | 7,069 | 8 | 2 | 21 | 
| CoreNLP | NLP | 15,544 | 6,812 | 23 | 0 | 45 | 
| moshi \[moshi-kotlin\] | JSON Library | 793 | 5,731 | 14 | 0 | 21 | 
| async-http-client \[http-client\] | HTTP Client | 4,034 | 5,233 | 29 | 16 | 130 | 
| error-prone \[core\] | Defects Detection | 4,015 | 4,915 | 44 | 0 | 35 | 
| alluxio \[core-transport\] | Database | 30,544 | 4,442 | 6 | 14 | 73 | 
| javaparser \[symbol-solver-logic\] | Code Analysis | 6,110 | 2,784 | 3 | 0 | 8 | 
| undertow \[benchmarks\] | Web Server | 4,687 | 2,538 | 10 | 0 | 19 | 
| wc-capture \[driver-openimaj\] | Webcam | 629 | 1,618 | 3 | 0 | 84 | 
| teavm \[core\] | Compiler | 2,334 | 1,354 | 9 | 0 | 9 | 
| handlebars \[markdown\] | Templates | 916 | 1,102 | 6 | 0 | 13 | 
| jooby \[jooby\] | Web Framework | 2,462 | 1,083 | 23 | 0 | 68 | 
| tika \[parsers\] | Parsing library | 4,650 | 929 | 81 | 0 | 67 | 
| orika \[eclipse-tools\] | Object Mapping | 970 | 864 | 3 | 0 | 3 | 
| spoon \[core\] | Meta-programming | 2,971 | 840 | 16 | 2 | 59 | 
| accumulo \[core\] | Database | 10,314 | 763 | 26 | 1 | 51 | 
| couchdb-lucene | Text Search | 1,121 | 752 | 25 | 0 | 112 | 
| jHiccup | Profiling | 215 | 519 | 4 | 0 | 1 | 
| subzero \[server\] | Cryptocurrency | 158 | 499 | 6 | 0 | 100 | 
| vulnerability-tool \[shared\] | Security | 1,051 | 324 | 6 | 4 | 2 | 
| para \[core\] | Cloud Framework | 1,270 | 310 | 47 | 2 | 112 | 
| launch4j-maven-plugin | Deployment Tool | 316 | 194 | 7 | 0 | 61 | 
| jacop | CP Solver | 1,158 | 155 | 7 | 0 | 9 | 
| selenese-runner-java | Interpreter | 1,688 | 117 | 23 | 0 | 148 | 
| commons-configuration | Config library | 3,159 | 100 | 31 | 0 | 49 | 

We answer RQ3 according to the following protocol: first, we run DepClean and try to build the artifact with the debloated POM file; second, we analyze the history of the project to propose a relevant change to the developers; third, we propose a change in the POM file in the form of a pull request; four, we discuss the pull request through GitHub. [Figure 5](#S4.F5) shows an excerpt of the diff of such a change. Since our submitted pull requests represent a small modification in the POM, they have a good chance to be reviewed by developers and discussed before being merged or rejected.

In the first step of the protocol, we use DepClean to obtain a report about the usage of dependencies. We analyze dependencies with both compile and test scope. Once a bloated-direct dependency is found, we remove it directly in the POM and proceed to build the project. If the project builds successfully after the removal (all the tests pass), we submit the pull request with the corresponding change. If after the removal of the dependency the build fails, then we consider the dependency as used dynamically and do not suggest to remove it. In the case of multi-module projects, with bloated dependencies in several modules, we submitted a single pull request per module.

For each pull request, we analyze the Git history of the POM file to determine when the bloated dependency was declared or modified. Our objective is to collect information in order to understand how the dependencies of the projects change during their evolution. This allows us to prepare a more informative pull request message and to support our discussion with developers. We also report on the benefits of tackling these bloated dependencies by describing the differences between the original and the debloated packaged artifact of the project in terms of the size of the bundle and the complexity of its dependency tree, when the difference was significant.
Each pull request includes an explanatory message. [Figure 6](#S4.F6) shows an example of the pull request message submitted to the project Undertow<sup>8</sup><sup>8</sup>
                8
                
                
                
              [https://github.com/undertow-io/undertow](https://github.com/undertow-io/undertow). The message explains the motivations of the proposed change, as well as the negative impact of keeping these bloated dependencies in the project.

To answer RQ4, we follow the same pull request submission protocol as for RQ3. We use DepClean to detect bloated-transitive dependencies and submit pull requests suggesting the addition of the corresponding exclusion clauses in each project POM. [Figure 7](#S4.F7) shows an example of a pull request message submitted to the project Apache Accumulo<sup>9</sup><sup>9</sup>
                9
                
                
                
              [https://github.com/apache/accumulo](https://github.com/apache/accumulo), while [Figure 8](#S4.F8) shows an excerpt of the commit proposing the exclusion of the transitive dependency org.apache.httpcomponents:httpcore from the direct dependency org.apache.thrift:libthrift in its POM.

Additional information related to the selected projects and the research methodology employed is publicly available as part of our replication package at [https://github.com/castor-software/depclean-experiments](https://github.com/castor-software/depclean-experiments).

## 5 Experimental Results

We now present the results of our in-depth analysis of bloated dependencies in the Maven ecosystem.

### 5.1 RQ1: How frequently do bloated dependencies occur?

In this first research question, we investigate the status of all the dependency relationships of the $9,639$ Maven artifacts under study.

[Figure 9](#S5.F9)shows the overall status of the $723,444$ dependency relationships in our dataset. The x-axis represents the percentages, per usage type, of all the dependencies considered in the studied artifacts. The first observation is that the bloat phenomenon is massive: $543,610$ ($75.1\%$) of all dependencies are bloated, they are not needed to compile and run the code. This bloat is divided into three separate categories: $19,673$ ($2.7\%$) are bloated-direct dependency relationships (explicitly declared in the POMs); $111,649$ ($15.4\%$) are bloated-inherited dependency relationships from parent module(s); and $412,288$ ($57\%$) are bloated-transitive dependencies.

Consequently, [Figure 9](#S5.F9) shows that $75.1\%$ of the relationships (edges in the dependency usage tree) are bloated dependencies. Note that this observation does not mean that $723,444$ artifacts are unnecessary and can be removed from Maven Central. The same artifact can occur in several DUTs and can be part of a bloated dependency relationship in some DUTs and part of a used relationships in the other DUTs.

In the following, we discuss in more detail and give examples to illustrate the occurrence of the three types of bloated dependency relationships analyzed.

Bloated-direct. We found that $2.7\%$ of the dependencies declared in the POM file of the studied artifacts are not used at all via bytecode calls. As an example, the Apache Ignite<sup>10</sup><sup>10</sup>
              10
              
              
              
            [https://github.com/apache/ignite](https://github.com/apache/ignite) project has deployed an artifact: org.apache.ignite:ignite-zookeeper:2.4.0, which contains only one class in its bytecode: TcpDiscoveryZookeeperIpFinder, and it declares a direct dependency in the POM towards slf4j, a widely used Java logging library. However, if we analyze the bytecode of ignite-zookeeper, no call to any API member of sl4j exist and therefore it is a bloated-direct dependency. After a manual inspection of the commit history of the POM, we found that sl4j was extensively used across all the modules of Apache Ignite at the early stages of the project, but it was later replaced by a dedicated logger, and its declaration remained intact in the POM.

Bloated-inherited. In our dataset, a total of $4,963$ artifacts are part of multi-module Maven projects. Each of these artifacts declares a set of dependencies in its POM file, and also inherits a set of dependencies from a parent POM. DepClean marks those inherited dependencies are either bloated-inherited or used-inherited. Our dataset includes a total of $111,649$ dependency relationships labeled as bloated-inherited, which represents $15.4\%$ of all dependencies under study and 61.8% of the total of inherited dependencies. For example, the artifact org.apache.drill:drill-protocol:1.14.0 inherits dependencies commons-codec and commons-io from its parent POM org.apache.drill:drill-root:1.14.0, however, those dependencies are not used in this module, and therefore they are bloated-inherited dependencies.

Bloated-transitive. In our dataset, bloated-transitive dependencies represent the majority of the bloated dependency relationships: $412,288$ ($57\%$). This type of bloat is a natural consequence of the Maven dependency resolution mechanism, which automatically resolves all the dependencies whether they are explicitly declared in the POM file of the project or not. Transitive dependencies are the most common type of dependency relationships, having a direct impact on the growth of the dependency trees. This type of bloat is the most common in the Maven ecosystem. For example, the artifact org.eclipse.milo:sdk-client:0.2.1 ships the transitive dependency gson in its MDT, induced from its direct dependency towards bsd-parser-core. However, the part of bsd-parser-core used by sdk-client does not calls any API member of gson, and therefore it is a bloated-transitive dependency.

In the following, we discuss the dependencies that are actually used. We observe that direct dependencies represent only $3.4\%$ of the total of dependencies in our dataset. This means that the majority of the dependencies that are necessary to build Maven artifacts are not declared explicitly in the POM files of these artifacts.

It is interesting to note that $85,975$ of the dependencies used by the artifacts under study are transitive dependencies. This kind of dependency usage occurs in two different scenarios: (1) the artifact uses API members of some transitive dependencies, without declaring them in its own POM file; or (2) the transitive dependency is a necessary provider for another artifact in the dependency tree.

We now discuss an example of the first scenario based on the org.apache.streams:streams-filters:0.6.0 artifact from the Apache Streams<sup>11</sup><sup>11</sup>
              11
              
              
              
            [https://streams.apache.org](https://streams.apache.org) project. It contains two classes: VerbDefinitionDropFilter and VerbDefinitionKeepFilter. [2](#LST2) shows part of the source code of the class VerbDefinitionDropFilter, which imports the class PreCondition from library guava (line [2](#lstnumberx18)) and uses its static method checkArgument in line [8](#lstnumberx24) of method process. However, if we inspect the POM of streams-filters, we notice that there is no dependency declaration towards guava. It declares a dependency towards streams-core, which in turn depends on the streams-utils artifact that has a direct dependency towards guava. Hence, guava is a used-transitive dependency of streams-filters, called from its source code.

Let us now present an example of the second scenario. [3](#LST3) shows an excerpt of the class AuditTask included in the artifact org.duracloud:auditor:4.4.3, from the project DuraCloud<sup>12</sup><sup>12</sup>
              12
              
              
              
            [https://duraspace.org](https://duraspace.org). In line [6](#lstnumberx34), the method getPropsSerializer instantiates the JaxbJsonSerializer object that belongs to the direct dependency org.duracloud:common-json:4.4.3. This object in turns creates an ObjectMapper from the transitive dependency jackson-mapper-asl. Hence, jackson-mapper-asl is a necessary, transitive provider for org.duracloud:auditor:4.4.3.

[Figure 10](#S5.F10)shows the distributions of dependency usage types per artifact. The figure presents superimposed log-scaled box-plots and violin-plots of the number of dependency relationships corresponding to the six usage types studied. Box-plots indicate the standard statistics of the distribution (i.e., lower/upper inter-quartile range, max/min values, and outliers), while violin plots indicate the entire distribution of the data.

We observe that the distributions of the bloated-direct (bd) and bloated-transitive (bt) dependencies vary greatly.
Bloated-direct dependencies are distributed between $0$ and $1$ (1st-Q and 3rd-Q), with a median of $0$; whereas the second ranges between $2$ and $41$ (1st-Q and 3rd-Q), with a median of $11$. These values are in line with the statistics presented in [Table 2](#S4.T2), since the number of direct and transitive dependencies in general differ approximately by one order of magnitude.
Overall, from the $9,639$ Maven artifacts studied, $3,472$ ($36\%$) have at least one bloated-direct dependency, while $8,305$ ($86.2\%$) have at least one bloated-transitive.

On the other hand, the inter-quartile range of bloated-direct (bd) dependencies is more compact than the used-direct (ud). In other words, the dependencies declared in the POM are mostly used. This result is expected, since developers have more control over the edition (adding/removing dependencies) of the POM file of their artifact.

The median number of used-transitive (ut) dependencies is significantly lower than the median number of bloated-transitive (bt) dependencies ($2$, vs. $11$). This suggests that the the default dependency resolution mechanism of Maven is suboptimal.

The number of outliers in the box-plots differs for each usage type. Notably, the bloated-direct dependencies have more outliers (in total, $25$ artifacts have more than $100$ bloated-direct dependencies). In particular, the artifact com.bbossgroups.pdp:pdp-system:5.0.3.9 has the maximum number of bloated-direct dependencies: $133$, out of the $147$ declared in its POM. The total number of artifacts with at least one bloated-direct dependency in our dataset is $2,298$, which represents $23.8\%$ of the $9,639$ studied artifacts.

Implications: Since developers have more control over direct dependencies, up to $17,673$ ($2.7\%$) of dependencies can be removed directly from the POM of Maven artifacts, in order to obtain smaller binaries and reduced attack surface. RQ3 will explore the willingness of developers to do so.

### 5.2 RQ2: How do the reuse practices affect bloated dependencies?

Most of the bloated dependencies in our dataset are either transitive ($57\%$) or inherited ($15.4\%$). In this research question, we investigate how the reuse practices that lead to those types of dependencies relate to the type of bloated dependency that emerges in Maven artifacts.

[Figure 11](#S5.F11)shows the distributions, in percentages, of the direct, inherited, and transitive dependencies for the $9,639$ studied artifacts. The artifacts are sorted, from left to right, in increasing order according to the ratio of direct dependencies. The y-axis indicates the ratio of each type of dependency for a give artifact. First, we observe that $4,967$ artifacts belong to multi-module projects. Among these artifacts, the extreme case (far left of the plot) is org.janusgraph:janusgraph-berkeleyje:0.4.0, which declares $1.4\%$ of its dependencies in its POM, while the $48.6\%$ of dependencies are inherited from parent POM files, and $50\%$ are transitive. Second, we observe that the ratio of transitive dependencies is not equally distributed. On the right side of the plot, $879$ ($9.1\%$) artifacts have no transitive dependency (they have $100\%$ direct dependencies). Meanwhile, $5,561$ ($57.7\%$) artifacts have more than $50\%$ transitive dependencies. The extreme case is org.apereo.cas:cas-server-core-api-validation:6.1.0, with $77.6\%$ transitive dependencies.

#### 5.2.1 Transitive dependencies

[Figure 12](#S5.F12)plots the relation between the ratio of transitive dependencies and the ratio of bloated dependencies. The key insight in this figure is that the larger concentration of artifacts is skewed to the top right corner. This indicates that artifacts with a high percentage of transitive dependencies also tend to exhibit higher percentages of bloated dependencies. Indeed, both variables are positively correlated, according to the Spearman’s rank correlation test ($\rho$ = 0.65, p-value \< $0.01$).

[Figure 13](#S5.F13)shows the distribution of the ratio of transitive bloated dependencies according to the height of the dependency tree. The artifact in our dataset with the largest height is top.wboost:common-base-spring-boot-starter:3.0.RELEASE, with a height of $14$.

The bar plot on top of [Figure 13](#S5.F13) indicates the number of artifacts that have the same height. We observe that most of the artifacts have a height of $4$: $2,226$ artifacts in total. Considering the number of dependencies, this suggests that the dependency trees tend to be wider than deep. This is because any dependency that already appears at a level closer to the root will be omitted by Maven if it is referred to at a deeper level.

Looking at the $58$ artifacts with height $\geq 10$, we notice that most of them belong to multi-module projects, and declare other modules in the same project as their direct dependencies. This is a regular practice of multi-module projects, which allows to release each module as an independent artifact. Meanwhile, this drastically increase the complexity of dependency trees. For example, the artifact org.wso2.carbon.devicemgt:org.wso2.carbon.apimgt.handlers:3.0.192 is the extreme case of this practice in our dataset, with a dependency tree of height $11$ and two direct dependencies towards other modules of the same project that in turn depends on other modules of this project. As a result, this artifact has $342$ bloated-transitive and $87$ bloated-inherited dependencies, and is part of a multi-module project with a total of $79$ modules released in Maven Central.

The plot in [Figure 13](#S5.F13) shows a clear increasing trend of bloated-transitive dependencies as the height of the dependency tree increases. For artifacts with a dependency tree of height greater than $9$, at least $28\%$ of their transitive dependencies are bloated, while the median of the percentages of bloated-transitive dependencies for artifacts with height larger than $5$ is more than $50\%$. This finding confirms and complements the results of [Figure 12](#S5.F12), showing that the complexity of the dependency tree is directly related to the occurrence of bloat.

In order to validate the graphical finding, we perform a Spearman’s rank correlation test between the number of bloated-transitive dependencies and the size of the dependency tree, i.e., the number of nodes in each tree. We found that there is a significant positive correlation between both variables ($\rho$ =0.67, p-value \< $0.01$).
This confirms that the actual usage of transitive dependencies decreases with the increasing complexity of the dependency tree. This result is aligned with our previous study that suggest that most of the public API members of transitive dependencies are not used by its clients ([Harrand et al., 2019](#bib.bib13)).

In summary, our results point to the excess of transitive dependencies as one of the fundamental causes of the existence of bloated dependencies in the Maven ecosystem.

#### 5.2.2 Single-module vs. multi-module

Let us investigate on the differences between single and multi-module architectures with respect to the presence of bloated dependencies. [Figure 14](#S5.F14) compares the distributions of bloated and used dependencies between multi-module and single-module artifacts in our dataset. We notice that, in general, multi-module artifacts have slightly more bloat than single-module, precisely $3.1\%$ more (the percentage of bloat in single-module is $5.8\%+67.3\%=73.1\%$ vs. $0.9\%+24.2\%+51.1\%=76.2\%$ in multi-module). More interestingly, we observe that a majority of the inherited dependencies are bloated: $24.2\%$ of the dependencies among multi-module project are bloated-inherited (bi), while only $15\%$ are used-inherited (ui). This suggest that most of the dependencies inherited by Maven artifacts that belong to multi-module artifacts are not used by these modules.

We observe that the percentage of bloated-direct dependencies in multi-module artifacts is very small ($0.9\%$) in comparison with single-module ($5.8\%$). Meanwhile, the percentage of bloated-transitive dependencies in single-module ($67.3\%$) is larger than in multi-module ($51.1\%$). This is due to the “shift” of a part of direct and transitive dependencies into inherited dependencies when using a parent POM. Indeed, the “shift” from direct to inherited is the main motivation for having a parent POM: to have one single declaration of dependencies for many artifacts instead of letting each artifact manage their own dependencies.

This “shift” in the nature of dependencies between single and multi-module artifacts is further emphasized in [Figure 15](#S5.F15). This plot shows superimposed log scaled box-plots and violin-plots comparing the distributions of the number of distinct dependency usage types per artifact, for single-module (top part of the figure) and multi-module (bottom part).

We observe that multi-module artifacts have less bloated-direct (1st-Q = 0, median = 0, 3rd-Q = 0) and less bloated-transitive (1st-Q = 2, median = 9, 3rd-Q = 40), compared to single-modules, as shown in [Figure 15](#S5.F15). However, multi-module artifacts have a considerably larger number of bloated-inherited dependencies instead (1st-Q = 1, median = 5, 3rd-Q = 20). The extreme case in our dataset is the artifact co.cask.cdap:cdap-standalone:4.3.4, with $326$ bloated-inherited dependencies in total.

In summary, the multi-module architecture in Maven projects contributes to limit redundant dependencies and facilitates the consistent versioning of dependencies in large projects.
However, it introduces two challenges for developers.
First, it leads to the emergence of bloated-inherited dependencies because of the friction of maintaining a common parent POM file: it is more difficult to remove dependencies from a parent POM than from an artifact’s own POM.
Second, it is more difficult for developers to be aware of and understand the dependencies that are inherited from the parent POM. This calls for better tooling and user interfaces to help developer grasp their inherited dependencies, which is virtually absent in the current Maven tooling ecosystem.

Implications: Developers should carefully consider reusing artifacts with several dependencies because they introduce bloat. They should also contemplate the risks of having bloated dependencies when considering adopting a multi-module architecture.

### 5.3 RQ3: To what extent are developers willing to remove bloated-direct dependencies?

In this research question, our goal is to see how developers react when made aware of bloated-direct dependencies in their projects. We do this by proposing the removal of bloated-direct dependencies to lead developers of mature open-source projects, as described in [Subsection 4.2.2](#S4.SS2.SSS2).

[Table 4](#S5.T4)shows the list of $18$ pull requests submitted. Each pull request proposes the removal of at least one bloated-direct dependency in the POM. We received response from developers for $15$ pull request. The first and second columns in the table show the name of the project and the URL to the pull request on GitHub. Columns three and four represent the number of bloated dependencies removed in the POM and the total number of dependencies removed from the dependency tree with the proposed change, incl. transitive ones. The last column shows the status of the pull request (
✓
 accepted, 
✓
<sup>⋆</sup> accepted with changes, 
✗
 rejected, or 
✴
 pending). The last row represent the acceptance rate calculated with respect to the projects with response, i.e., the total number of dependencies removed divided by the number of proposed removals. For example, for project undertow we propose the removal of $6$ bloated dependencies in its module benchmarks. As a result of this change, $17$ transitive dependencies were removed from the dependency tree the module.

Overall, from the pull requests with responses from developers, $14/15$ were accepted and merged. In total, $68$ dependencies were removed from the dependency trees of the projects. This result demonstrates the relevance of handling bloated-direct dependencies for developers, and the practical usefulness of DepClean.

Let us now summarize the developer feedback. First, all developers agreed about the importance of refining the projects’ POMs. This is reflected in the positive comments received. Second, their quick responses suggest that it is easy for them to understand the issues associated with the presence of bloated-direct dependencies in their projects. In $8/15$ projects, the response time was less than $24$ hours, which is an evidence that developers consider this type of improvement as a priority.

Our results also evidence the fact that we, as external contributors to those projects, were able to identify the problem and propose a solution using DepClean. In the following, we discuss four cases of pull requests that are particularly interesting and the feedback provided by developers.

- \*Status of the pull request: 
✓
 Accepted. 
✓
<sup>⋆</sup> Accepted with changes. 
✗
 Rejected.
✴
 Pending.

#### 5.3.1 jenkins

DepClean detects that jtidy and commons-codec are bloated-direct dependencies present in the modules core and cli of jenkins. jtidy is a HTML syntax checker and pretty printer. commons-codec is an Apache library that provides an API to encode/decode from various formats such as Base64 and Hexadecimal.

Developers were reluctant to remove jtidy due to their concerns of affecting the users of jenkins, which could be potential consumers of this dependency.
After further inspection, they found that the class HTMLParser of the nis-notification-lamp-plugin<sup>13</sup><sup>13</sup>
                  13
                  
                  
                  
                [https://github.com/jenkinsci/nis-notification-lamp-plugin](https://github.com/jenkinsci/nis-notification-lamp-plugin) project relies on jtidy transitively for performing HTML parsing.

Developers also pointed out the fact that there is no classloader isolation in jenkins, and hence all dependencies in its core module automatically become part of its public API. A developer also referred to issues related to past experiences removing unused dependencies. He argued that external projects have depended on that inclusion and their builds were broken by such a removal. For example, the Git client plugin mistakenly included Java classes from certain Apache contrib authentication classes. When they removed the dependency, some downstream consumers of the library were affected, and they had to include the dependency directly.

Consequently, we received the following feedback from an experienced developer of jenkins:

*“We’re not precluded from removing an unused dependency, but I think that the project values compatibility more than removal of unused dependencies, so we need to be careful that removal of an unused dependency does not cause a more severe problem than it solves.”*

After some discussions, developers agreed with the removal of commons-codec in module cli. Our pull request was edited by the developers and merged to the master branch one month after.

#### 5.3.2 checkstyle

DepClean identifies the direct dependency junit-jupiter-engine as bloated. This is a test scope dependency that was added to the POM of checkstyle when migrating integration tests to JUnit 5. The inclusion of this dependency was necessary due to the deprecation of junit-platform-surefire-provider in the Surefire Maven plugin. However, the report of DepClean about this bloated-direct dependency was a false positive. The reason for this output occurs because junit-jupiter-engine is commonly used through reflective calls that cannot be captured at the bytecode level.

Although this pull request was rejected, developers expressed interest in DepClean, which is encouraging. They also proposed a list of features for the improvement of our tool. For example, the addition of an exclusion list in the configuration of DepClean for dependencies that are known to be used dynamically, improvements on the readability of the generated report, and the possibility of causing the build process to fail in case of detecting the presence of any bloated dependency. We implemented each of the requested functionalities in DepClean. As a result, developers opened and issue to integrate DepClean in the Continuous Integration (CI) pipeline of checkstyle, in order to automatically manage their bloated dependencies<sup>14</sup><sup>14</sup>
                14
                
                
                
              [https://github.com/checkstyle/checkstyle/issues/7307](https://github.com/checkstyle/checkstyle/issues/7307).

#### 5.3.3 alluxio

DepClean detects that the direct dependency grpc-netty, declared in the module alluxio-core-transport is bloated. [Figure 16](#S5.F16) shows that this dependency also induces a total of $10$ transitive dependencies that are not used ($4$ of them are omitted by Maven due to their duplication in the dependency tree). Developers accepted our pull request and also manifested their interest on using DepClean for managing unused dependencies in the future.

#### 5.3.4 undertow

DepClean detects a total of 6 bloated-direct dependencies in the benchmarks module of the project undertow: undertow-servlet, undertow-websockets-jsr, jboss-logging-processor, xnio-nio, jmh-generator-annprocess, and httpmime. In this case, we received a rapid positive response from the developers two days after the submission of the pull request. Removing the suggested bloated-direct dependencies has a significant impact on the size of the packaged JAR artifact of the undertow-benchmarks module. We compare the sizes of the bundled JAR before and after the removal of those dependencies: the binary size reduction represents more than 1MB. It is worth mentioning that this change also reduced the complexity of the dependency tree of the module.

Implications: Removing bloated-direct dependencies is relevant for developers and it is perceived as a valuable contribution. This type of change in the POM files are small, and they can have a significant impact on the dependency tree of Maven projects.

### 5.4 RQ4: To what extent are developers willing to exclude bloated-transitive dependencies?

In this research question, our goal is to see how developers react when made aware of bloated-transitive dependencies. We do this by proposing the exclusion of bloated-transitive dependencies to them, as described in [Subsection 4.2.2](#S4.SS2.SSS2).

[Table 5](#S5.T5)shows the list of $13$ pull requests submitted. Each pull request proposes the exclusion of at least one transitive dependency in the POM. We received response from developers for $8$ pull requests. The first and second columns show the name of the project and the URL to the pull request on GitHub. Columns three and four represent the number of bloated-transitive dependencies explicitly excluded and the total number of dependencies removed in the dependency tree as resulting from the exclusion. The last column shows the status of the pull request (
✓
 accepted, 
✗
 rejected, or 
✴
 pending). The last row represents the acceptance rate with respect to the projects with response. For example, for the project spoon we propose the exclusion of four-bloated transitive dependencies in its core module. As a result of this change, $31$ transitive dependencies were removed from the dependency tree of this module.

Overall, from the pull requests with responses from developers, $4$ were accepted and $4$ were rejected. In total, $63$ bloated dependencies were removed from the dependency trees of $4$ projects. We notice that the accepted pull requests involve those projects for which the exclusion of transitive dependencies also represents the removal of a large number of other dependencies from the dependency tree. This result suggests that developers are more careful concerning this type of contributions.

As in RQ3, we obtained valuable feedback from developers about the pros and cons of excluding bloated-transitive dependencies. In the following, we provide unique qualitative insights about the most interesting cases and explain the feedback obtained from developers to the research community.

- \*Status of the pull request: ✓ Accepted. ✗ Rejected. ✴ Pending.

#### 5.4.1 jenkins

DepClean detects the bloated-transitive dependencies constant-pool-scanner and eddsa in the module core of jenkins. These bloated dependencies were induced through the direct dependencies remoting and cli, respectively. In the message of the pull request, we explain how their exclusion contributes to make the core of jenkins slimmer and the dependency tree clearer.

Although both dependencies were confirmed as unused in the core module of jenkins, developers rejected our pull request. They argue that excluding such dependencies has no valuable repercussion for the project and might actually affect its clients, which is correct. For example, constant-pool-scanner is used by external components, e.g., the class RemoteClassLoader in the remoting<sup>15</sup><sup>15</sup>
                  15
                  
                  
                  
                [https://github.com/jenkinsci/remoting](https://github.com/jenkinsci/remoting) project relies on this library to inspect the bytecode of remote dependencies.

As shown in the following quote from an experienced developer of Jenkins, there is a general consensus on the usefulness of removing bloated dependencies, but developers need strong facts to support the removal of transitive dependencies:

*“Dependency removals and exclusions are really useful, and my recommendation would be to avoid them if there is no substantial gain.”*

#### 5.4.2 auto

DepClean reports on the bloated-transitive dependencies listenablefuture and auto-value-annotations in module auto-common of the Google auto project. We proposed the exclusion of these dependencies and submitted a pull request with the POM change.

Developers express several concerns related to the exclusion of these dependencies. For example, a developer believes that it is not worth maintaining exclusion lists for dependencies that cause no problem. They point out that although listenableFuture is a single class file dependency, its presence in the dependency tree is vital to the project, since it overrides the version of the guava library that have many classes. Therefore, the inclusion of this dependency is a strategy followed by guava to narrow the access to the interface ListenableFuture and not to the whole library<sup>16</sup><sup>16</sup>
                16
                
                
                
              [https://groups.google.com/forum/#!topic/guava-announce/Km82fZG68Sw/discussion](https://groups.google.com/forum/#!topic/guava-announce/Km82fZG68Sw/discussion).

On the other hand, developers agree that auto-value-annotations is bloated. However, they keep it, arguing that it is a test-only dependency, and they prefer to keep annotation-only dependencies and let end users exclude them when desired.

The response from developers suggests that bloated dependencies with test scope are perceived as less harmful. This is reasonable since test dependencies are only available during the test, compilation, and execution phases and are not shipped transitively in the JAR of the artifact. However, we believe that although it is a developers’ decision whether they keep this type of bloated dependency or not, the removal of testing dependencies is regularly a desirable refactoring improvement.

#### 5.4.3 moshi

DepClean detects that the bloated-transitive dependency kotlin-stdlib-common is present in the dependency tree of modules moshi-kotlin, moshi-kotlin-codegen, and moshi-kotlin-tests of project moshi. This dependency is induced from a common dependency of these modules: kotlin-stdlib.

Developers rejected our pull requests, arguing that excluding such transitive dependency prevents the artifacts from participating in the proper dependency resolution of their clients. They suggest that clients interested in reducing the size of their projects can use specialized shrinking tools, such as ProGuard<sup>17</sup><sup>17</sup>
                17
                
                
                
              [https://www.guardsquare.com/en/products/proguard](https://www.guardsquare.com/en/products/proguard), for this purpose.

Although the argument of developers is valid, we believe that delegating the task of bloat removal to their library clients imposes an unnecessary burden on them. On the other hand, recent studies reveal that library clients do not widely adopt the usage of dependency analysis tools for quality analysis purposes [Nguyen et al. (2020)](#bib.bib29).

#### 5.4.4 spoon

DepClean detects that the transitive dependencies org.eclipse.core.resources, org.eclipse.core.runtime, org.eclipse.core.filesystem, and org.eclipse.text org.eclipse.jdt.core are bloated. All of these transitive dependencies were induced by the inclusion of the direct dependency org.eclipse.jdt.core, declared in the POM of core module of the spoon library.

[Table 6](#S5.T6)shows how the exclusion of these bloated-transitive dependencies has a positive impact on the size and the number of classes of the library. As we can see, by excluding these dependencies the size of the jar-with-dependencies of the core module of spoon is trimmed from $16.2$MB to $12.7$MB, which represents a significant reduction in size of $27.6\%$. After considering this improvements, the developers confirmed the relevance of this change and merged our pull request into the master branch of the project.

|  | JAR Size(MB) | #Classes | 
| Before | $16.2$ | $7,425$ | 
| After | $12.7$ | $5,593$ | 
| Reduction(%) | $27.6\%$ | $24.7\%$ | 

#### 5.4.5 accumulo

DepClean detects the bloated-transitive dependencies listenablefuture, httpcore and netty in the core module of Apache accumulo. These dependencies were confirmed as bloated by the developers. However, they manifested their concerns regarding their exclusion, as expressed in the following comment:

*“I’m not sure I want us to take on the task of maintaining an exclusion set of transitive dependencies from all our deps POMs, because those can change over time, and we can’t always know which transitive dependencies are needed by our dependencies.”*.

After the discussion, developers decided to accept and merge the pull request. Overall, developers considered that the proposal is a good idea. They suggest that it would be better to approach the communities of each of the direct dependencies that they use, and encourage them to mark those dependencies as *optional*, thus they would not be automatically inherited by their users.

#### 5.4.6 para

DepClean detects the bloated-transitive dependency flexmark-jira-converter. This dependency is induced through the direct dependency flexmark-ext-emoji, declared in the core module of the para project. Our further investigation on the Maven dependency tree of this module revealed that this bloated dependency adds a total of $19$ additional dependencies to the dependency tree of the project, of which $15$ are detected as duplicated by Maven.

Because of this large number (19) of bloated-transitive dependencies removed, developers accepted the pull request and merged the change into the master branch of the project the same day of the pull request submission.

Implications: The handling of bloated-transitive dependencies is a topic with no clear consensus among developers. Developers consider this kind of bloat as relevant, but they are concerned about the maintenance of a list of exclusion directives. Some developers agree to remove them based on practical facts (e.g., JAR size reduction) while other developers prefer to keep bloated-transitive dependencies in order to avoid the potential negative impact on their clients.

## 6 Discussion

In this section, we discuss the implications of our findings and the threats to the validity of the results obtained.

### 6.1 Implications of Results

Our study of bloat in POM files complements previous studies about the challenges and risks of dependency management for security. In this context, bloated dependencies represent an unnecessary additional source of vulnerabilities, opening the door to potential attackers which may exploit code segments that could not have been reached otherwise [Mitropoulos et al. (2014)](#bib.bib26); [Gkortzis et al. (2019)](#bib.bib12). The complexity of dependency management systems is a critical engineering concern since dependency issues can scale through entire ecosystems. For example, in 2027, the Equifax data breach<sup>18</sup><sup>18</sup>
              18
              
              
              
            [https://www.equifaxsecurity2017.com](https://www.equifaxsecurity2017.com) caused by a vulnerability in a Java library impacted the personal information of 147 million American citizens. Various initiatives have emerged to cope with this issue. GitHub tracks dependency vulnerability reports from various sources<sup>19</sup><sup>19</sup>
              19
              
              
              
            [https://help.github.com/en/articles/about-security-alerts-for-vulnerable-dependencies](https://help.github.com/en/articles/about-security-alerts-for-vulnerable-dependencies) and provides security alerts to affected repositories; dependabot<sup>20</sup><sup>20</sup>
              20
              
              
              
            [https://dependabot.com/](https://dependabot.com/) automatically submits pull requests to suggest dependency updates. DepClean can complement these security scanning solutions in order to determine if a dependency can be removed rather than upgraded.

Our results indicate that most of the dependency bloat is due to transitive dependencies and the Maven dependency heritage mechanism. The official Maven dependency management guidelines<sup>21</sup><sup>21</sup>
              21
              
              
              
            [https://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html](https://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html) encourage developers to take control over the dependency resolution process via their explicit declaration in the POM file. This is a good practice to provide better documentation for the project and to keep one artifact’s dependencies independent from the choices of other libraries down the dependency tree. Dependencies declared in this way have priority over the Maven mediation mechanism, allowing developers to have a clear knowledge about which library version they are expecting to be used through transitive dependencies. However, since backward compatibility is not always guaranteed, having fixed transitive dependency versions, and therefore non-declared dependencies, still remains as a widely extended practice. In this context, the introduction of the module construct in Java 9 provides a higher level of aggregation above packages. This new language element, if largely adopted, may help to reduce the transitive explosion of dependencies. Indeed, this mechanism forces developers to declare explicitly what other modules are required to use in a given module. This leads to two benefits: (1) it enables reuse declaration at a finer grain than dependencies, and (2) it makes the debloat techniques described in this work safer as it constrains reflection to white-listed modules.

Our results show that even notable open-source projects, which are maintained by development communities with strict development rules, are affected by dependency bloat. Developers confirmed and removed most of the reported bloated-direct dependencies detected by DepClean. However, they are more careful about excluding bloated-transitive dependencies. The addition of exclusion clauses to the POM files is perceived by some developers as an unnecessary maintainability burden. Interestingly, our quantitative results indicate that bloated-transitive dependency relationships represent the largest portion of bloated dependencies, yet, our qualitative study reveals that these bloated relationships are also the ones that developers find the most challenging to handle and reason about. Overall, this work opens the door to new research opportunities on debloating POMs and other build files.

### 6.2 Threats to Validity

In the following, we discuss about construct, internal and external threats to the validity of our study.

Construct validity. The threats to construct validity are related to the novel concept of bloated dependencies and the metrics utilized for its measurement. For example, the DUT constructed by DepClean could be incomplete due to issues during the resolution of the dependencies. We mitigate this threat by building DepClean on top of Maven plugins to collect the information about the dependency relationships. We also exclude from the study those artifacts for which we were unable to retrieve the full dependency usage information.

It is possible that developers repackage a library as a bundle JAR file along with its dependencies, or copy the source code of dependencies directly into their source code, in order to avoid dependency related issues. Consequently, DepClean will miss such dependencies, as they are not explicitly declared in the POM file. Thus, the analysis of dependencies can underestimate the part of bloated dependencies. However, considering the size of our dataset and the feedback obtained from actively maintained projects, we believe that these corner cases do not affect our main results.

Internal validity. The threats to internal validity are related to the effectiveness of DepClean to detect bloated dependencies. The dynamic features of the Java programming language, e.g., reflection or dynamic class loading present particular challenges for any automatic analysis of Java source code ([Landman et al., 2017](#bib.bib21); [Lindholm et al., 2014](#bib.bib23)). Since DepClean statically analyzes bytecode, anything that does not get into the bytecode is not detected (e.g., constants, annotations with source-only retention police, links in Javadocs), which can lead to false positives. To mitigate this threat, DepClean can detect classes or class members that are created or invoked dynamically using basic constructs such as class.forName("someClass") or class.getMethod("someMethod", null). We also use an exclusion list of dependencies that are known to be used only dynamically.

External validity. The relevance of our findings in other software ecosystems is one threat to external validity. Our observations about bloated dependencies are based on Java and the Maven ecosystem and our findings are restricted to this scope. More studies on other dependency management systems are needed to figure out whether our findings can be generalized. Another external threat relates to the representativeness of the projects considered for the qualitative study. To mitigate this threat, we submitted pull requests to a set of diverse, mature, and popular open-source Java projects that belong to distinct communities and cover various application domains. This means that we contributed to improving the dependency management of projects that are arguably among the best of the open-source Java world, which aims to get as strong external validity as possible.

## 7 Related Work

In this work, we propose the first systematic large-scale analysis of bloat in the Maven ecosystem. Here, we discuss the related works in the areas of software debloating and dependency management.

### 7.1 Analysis and Mitigation of Software Bloat

Previous studies have shown that software tends to grow over time, whether or not there is a need for it [Holzmann (2015)](#bib.bib15); [Quach et al. (2017)](#bib.bib32). Consequently, software bloat appears as a result of the natural increase of software complexity, e.g., the addition of non-essential features to programs ([Brooks, 1987](#bib.bib6)). This phenomenon comes with several risks: it makes software harder to understand and maintain, increases the attack surface, and degrades the overall performance.
Our paper contributes to the analysis and mitigation of a novel type of software bloat: *bloated dependencies*.

Celik et al. ([Celik et al., 2016](#bib.bib8)) presented Molly, a build system to lazily retrieve dependencies in CI environments and reduce build time. For the studied projects, the build time speed-up reaches $45\%$ on average compared to Maven. DepClean operates differently than Molly: it is not an alternative to Maven as Molly is, but a static analysis tool that allows Maven users to have a better understanding and control about their dependencies.

Yu et al. ([Yu et al., 2003](#bib.bib43)) investigated the presence of unnecessary dependencies in header files of large C projects. Their goal was to reduce build time. They proposed a graph-based algorithm to statically remove unused code from applications. Their results show a reduction of build time of $89.70\%$ for incremental builds, and of $26.38\%$ for fresh builds. Our work does not focus on build performance, we analyze the pervasiveness of dependency bloat across a vast and modern ecosystem of Maven packages.

In recent years, there has been a notable interest in the development of debloating techniques for program specialization. The aim is to produce a smaller, specialized version of programs that consume fewer resources while hardening security [Azad et al. (2019)](#bib.bib1). They range from debloating command line programs written in C ([Sharif et al., 2018](#bib.bib37)), to the specialization of JavaScript frameworks [Vázquez et al. (2019)](#bib.bib41) and
fully fledged containerized platforms ([Rastogi et al., 2017](#bib.bib33)). Most debloating techniques are built upon static analysis and are conservative in the sense that they focus on trimming unreachable code [Jiang et al. (2016)](#bib.bib17), others are more aggressive and utilize advanced dynamic analysis techniques to remove potentially reachable code ([Heath et al., 2019](#bib.bib14)). Our work addresses the same challenges at a coarser granularity. DepClean removes unused dependencies, which is, according to our empirical results, a significant cause of program bloat.

Qiu et al. [Qiu et al. (2016)](#bib.bib31) empirically shows evidence that a considerable proportion of API members are not widely used, i.e., many classes, methods, and fields of popular libraries are not used in practice. Nguyen et al. [Pham et al. (2016)](#bib.bib30) implement a bytecode based analysis tool to learn about the actual API usage of Android frameworks.
Lämmel et al. [Lämmel et al. (2011)](#bib.bib20) perform a large-scale study on API usage based on the migration of AST code segments. Other studies have focused on understanding how developers use APIs on the daily basis [Roover et al. (2013)](#bib.bib34); [Bauer et al. (2014)](#bib.bib2). Some of the motivations include improving API design [Myers and Stylos (2016)](#bib.bib27); [Harrand et al. (2019)](#bib.bib13) and increasing developers productivity [Lim (1994)](#bib.bib22).
All these studies hint at the presence of bloat in APIs. Yet, none of the aforementioned studies investigated the reaction of developers to bloated dependencies. In this paper, we complement the quantitative study of dependency bloat in Maven Central with practical insights gathered from our contributions to recognized open-source projects.

### 7.2 Dependency Management in Software Ecosystems

Library reuse and dependency management has become mainstream in software development. McIntosh et al. ([McIntosh et al., 2012](#bib.bib24)) analyze the evolution of automatic build systems for Java (ANT and Maven). They found that Java build systems follow linear or exponential evolution patterns in terms of size and complexity. In this context, we interpret bloated dependencies as a consequence of the tendency of build automation systems of evolving towards open-ended complexity over time.

Decan et al. ([Decan et al., 2019](#bib.bib11); [Decan et al., 2017](#bib.bib10)) studied the fragility of packaging ecosystems caused by the increasing number of transitive dependencies. Their findings corroborate our results, showing that most clients have few direct dependencies but a high number of transitive dependencies. They also found that popular libraries tend to have larger dependency trees. However, their work focuses primarily on the relation between the library users and their direct providers and does not take into account the inherited or transitive dependencies of those providers. We are the first, to the best of our knowledge, to conduct an empirical analysis of bloated dependencies in the Maven ecosystem considering both, users and providers, as potential sources of software bloat.

Bezemer et al. ([Bezemer et al., 2017](#bib.bib5)) performed a study of unspecified dependencies, i.e., dependencies that are not explicitly declared in the build systems. They found that these unspecified dependencies are subtle and difficult to detect in make-based build systems. Seo et al. ([Seo et al., 2014](#bib.bib36)) analyzed over 26 millions builds in Google to investigate the causes, types of errors made, and resolution efforts to fix the failing builds. Their results indicate that, independent of the programming language, dependency errors are the most common cause of failures, representing more than two thirds of fails for Java. Based on our results, we hypothesize that removing dependency bloat would reduce spurious CI errors related to dependencies.

Jezek et al. [Jezek and Dietrich (2014)](#bib.bib16) describe, with practical examples, the issues caused by transitive dependencies in Maven. They propose a static analysis approach for finding missing, redundant, incompatible, and conflicting API members in dependencies. Their experiments, based on a dataset of $29$ Maven projects, show that problems related to transitive dependency are common in practice. They identify the use of wrong dependency scopes as a primary cause of redundancy. Our quantitative study extends this work to the scale of the Maven Central ecosystem, and provides additional evidence about the persistence of the dependency redundancy problem.

Callo et al. ([Callo Arias et al., 2011](#bib.bib7)) performed a systematic review about dependency analysis solutions in software-intensive systems. Bavota et al. ([Bavota et al., 2015](#bib.bib3)) studied performed an empirical study on the evolution of declared dependencies in the Apache community. They found that build system specifications tend to grow over time unless explicit effort is put into refactoring them. Our qualitative results complement previous studies that present empirical evidence that developers do not systematically update their dependency configuration files [McIntosh et al. (2014)](#bib.bib25); [Kula et al. (2018)](#bib.bib19).

## 8 Conclusion

In this work, we presented a novel conceptual analysis of a phenomenon originated from the practice of software reuse, which we coined as *bloated dependencies*. This type of dependency relationship between software artifacts is two-side intriguing: from the perspective of the dependency management systems that are unable to avoid it, and from the standpoint of developers who declare dependencies but do not use them in their applications.

We performed a quantitative and qualitative study of bloated dependencies in the Maven ecosystem. To do so, we implemented a tool, DepClean, which analyzes the bytecode of an artifact and all its dependencies that are resolved by Maven. As a result of the analysis, DepClean provides a report of the bloated dependencies, as well as a new version of its POM file which removes the bloat. We use DepClean to analyze the $723,444$ dependency relationships of $9,639$ artifacts in Maven Central. Our results reveal that $2.7\%$ of them are bloated ($2.7\%$ are direct dependencies, $15.4\%$ are inherited from parent POMs, and $11.9\%$ are transitive dependencies). Based on these results, we distilled two possible causes: the cascade of unwanted transitive dependencies induced by direct dependencies, and the dependency heritage mechanism of multi-module Maven projects.

We complement our quantitative study of bloated dependencies with an in-depth qualitative analysis of $21$ mature Java projects. We use DepClean to analyze these projects and submit the results obtained as pull request on GitHub. Our results indicate that developers are willing to remove bloated-direct dependencies: $14$ out of $15$ answered pull requests were accepted and merged by the developers in their code base. On the other hand, we found that developers tend to be skeptical regarding the exclusion of bloated-transitive dependencies: $4$ out of $8$ answered pull requests were accepted. Overall, the feedback from developers reveals that the removal of bloated dependencies clearly worth the additional analysis and effort.

Our study stresses the need to engineer, i.e., analyze, maintain, test POM files. The feedback from developers shows interest in DepClean to address this challenge. While the tool is robust enough to analyze a variety of real-world projects, developers now ask questions related to the methodology for dependency debloating, e.g., when to analyze bloat? (in every build, in every release, after every POM change), who is responsible for debloat of direct or transitive dependencies? (the lead developers, any external contributor), how to properly managing complex dependency trees to avoid dependency conflicts? These methodological questions are part of the future work to further consolidate DepClean.

## References

- Azad et al. \[2019\]
B. A. Azad, P. Laperdrix, and N. Nikiforakis.
Less is more: Quantifying the security benefits of debloating web
applications.
In *Proceedings of the 28th USENIX Conference on Security
Symposium*, SEC, page 1697–1714, USA, 2019. USENIX Association.
ISBN 9781939133069.
- Bauer et al. \[2014\]
V. Bauer, J. Eckhardt, B. Hauptmann, and M. Klimek.
An Exploratory Study on Reuse at Google.
In *Proceedings of the 1st International Workshop on Software
Engineering Research and Industrial Practices*, SERIP, pages 14–23, New
York, NY, USA, 2014. ACM.
ISBN 978-1-4503-2859-3.
doi: 10.1145/2593850.2593854.
URL [http://doi.acm.org/10.1145/2593850.2593854](http://doi.acm.org/10.1145/2593850.2593854).
- Bavota et al. \[2015\]
G. Bavota, G. Canfora, M. Di Penta, R. Oliveto, and S. Panichella.
How the apache community upgrades dependencies: an evolutionary
study.
*Empirical Software Engineering*, 20(5):1275–1317, Oct 2015.
ISSN 1573-7616.
doi: 10.1007/s10664-014-9325-9.
URL [https://doi.org/10.1007/s10664-014-9325-9](https://doi.org/10.1007/s10664-014-9325-9).
- Benelallam et al. \[2019\]
A. Benelallam, N. Harrand, C. Soto-Valero, B. Baudry, and O. Barais.
The Maven Dependency Graph: a Temporal Graph-based Representation of
Maven Central.
In *16th International Conference on Mining Software
Repositories (MSR)*, Montreal, Canada, 2019. IEEE/ACM.
- Bezemer et al. \[2017\]
C.-P. Bezemer, S. McIntosh, B. Adams, D. M. German, and A. E. Hassan.
An empirical study of unspecified dependencies in make-based build
systems.
*Empirical Software Engineering*, 22(6):3117–3148, Dec 2017.
ISSN 1573-7616.
doi: 10.1007/s10664-017-9510-8.
URL [https://doi.org/10.1007/s10664-017-9510-8](https://doi.org/10.1007/s10664-017-9510-8).
- Brooks \[1987\]
F. P. Brooks.
No silver bullet essence and accidents of software engineering.
*Computer*, 20(4):10–19, Apr. 1987.
ISSN 0018-9162.
doi: 10.1109/MC.1987.1663532.
URL [https://doi.org/10.1109/MC.1987.1663532](https://doi.org/10.1109/MC.1987.1663532).
- Callo Arias et al. \[2011\]
T. B. Callo Arias, P. van der Spek, and P. Avgeriou.
A practice-driven systematic review of dependency analysis solutions.
*Empirical Software Engineering*, 16(5):544–586, Oct 2011.
doi: 10.1007/s10664-011-9158-8.
URL [https://doi.org/10.1007/s10664-011-9158-8](https://doi.org/10.1007/s10664-011-9158-8).
- Celik et al. \[2016\]
A. Celik, A. Knaust, A. Milicevic, and M. Gligoric.
Build system with lazy retrieval for java projects.
In *Proceedings of the 2016 24th ACM SIGSOFT International
Symposium on Foundations of Software Engineering*, FSE, pages 643–654, New
York, NY, USA, 2016. ACM.
ISBN 978-1-4503-4218-6.
doi: 10.1145/2950290.2950358.
URL [http://doi.acm.org/10.1145/2950290.2950358](http://doi.acm.org/10.1145/2950290.2950358).
- Cox \[2019\]
R. Cox.
Surviving software dependencies.
*Communications of the ACM*, 62(9):36–43,
2019.
URL [http://delivery.acm.org/10.1145/3350000/3347446/p36-cox.pdf?ip=130.237.224.202&id=3347446&acc=OA&key=74F7687761D7AE37%2EE53E9A92DC589BF3%2E4D4702B0C3E38B35%2E5945DC2EABF3343C&\_\_acm\_\_=1575959910\_051299ecdd4bf0a7442ae3476bd0e750](http://delivery.acm.org/10.1145/3350000/3347446/p36-cox.pdf?ip=130.237.224.202&id=3347446&acc=OA&key=74F7687761D7AE37%2EE53E9A92DC589BF3%2E4D4702B0C3E38B35%2E5945DC2EABF3343C&__acm__=1575959910_051299ecdd4bf0a7442ae3476bd0e750).
- Decan et al. \[2017\]
A. Decan, T. Mens, and M. Claes.
An Empirical Comparison of Dependency Issues in OSS Packaging
Ecosystems.
In *2017 IEEE 24th International Conference on Software
Analysis, Evolution and Reengineering*, SANER, pages 2–12, Feb 2017.
doi: 10.1109/SANER.2017.7884604.
- Decan et al. \[2019\]
A. Decan, T. Mens, and P. Grosjean.
An empirical comparison of dependency network evolution in seven
software packaging ecosystems.
*Empirical Software Engineering*, 24(1):381–416, Feb 2019.
ISSN 1573-7616.
doi: 10.1007/s10664-017-9589-y.
URL [https://doi.org/10.1007/s10664-017-9589-y](https://doi.org/10.1007/s10664-017-9589-y).
- Gkortzis et al. \[2019\]
A. Gkortzis, D. Feitosa, and D. Spinellis.
A double-edged sword? software reuse and potential security
vulnerabilities.
In X. Peng, A. Ampatzoglou, and T. Bhowmik, editors, *Reuse in
the Big Data Era*, pages 187–203, Cham, 2019. Springer International
Publishing.
ISBN 978-3-030-22888-0.
- Harrand et al. \[2019\]
N. Harrand, A. Benelallam, C. Soto-Valero, O. Barais, and B. Baudry.
Analyzing 2.3 million maven dependencies to reveal an essential core
in apis.
*arXiv preprint arXiv:1908.09757*, 2019.
- Heath et al. \[2019\]
B. Heath, N. Velingker, O. Bastani, and M. Naik.
PolyDroid: Learning-Driven Specialization of Mobile Applications.
*arXiv e-prints*, art. arXiv:1902.09589, Feb 2019.
- Holzmann \[2015\]
G. J. Holzmann.
Code inflation.
*IEEE Software*, 1(2):10–13, 2015.
- Jezek and Dietrich \[2014\]
K. Jezek and J. Dietrich.
On the use of static analysis to safeguard recursive dependency
resolution.
In *2014 40th EUROMICRO Conference on Software Engineering and
Advanced Applications*, pages 166–173, Aug 2014.
doi: 10.1109/SEAA.2014.35.
- Jiang et al. \[2016\]
Y. Jiang, D. Wu, and P. Liu.
Jred: Program customization and bloatware mitigation based on static
analysis.
In *2016 IEEE 40th Annual Computer Software and Applications
Conference (COMPSAC)*, volume 1, pages 12–21, June 2016.
doi: 10.1109/COMPSAC.2016.146.
- Krueger \[1992\]
C. W. Krueger.
Software reuse.
*ACM Comput. Surv.*, 24(2):131–183, June
1992.
ISSN 0360-0300.
doi: 10.1145/130844.130856.
URL [https://doi.org/10.1145/130844.130856](https://doi.org/10.1145/130844.130856).
- Kula et al. \[2018\]
R. G. Kula, D. M. German, A. Ouni, T. Ishio, and K. Inoue.
Do developers update their library dependencies?
*Empirical Software Engineering*, 23(1):384–417, Feb 2018.
ISSN 1573-7616.
doi: 10.1007/s10664-017-9521-5.
URL [https://doi.org/10.1007/s10664-017-9521-5](https://doi.org/10.1007/s10664-017-9521-5).
- Lämmel et al. \[2011\]
R. Lämmel, E. Pek, and J. Starek.
Large-scale, AST-based API-usage Analysis of Open-source Java
Projects.
In *Proceedings of the 2011 ACM Symposium on Applied Computing*,
SAC ’11, pages 1317–1324, New York, NY, USA, 2011. ACM.
ISBN 978-1-4503-0113-8.
doi: 10.1145/1982185.1982471.
URL [http://doi.acm.org/10.1145/1982185.1982471](http://doi.acm.org/10.1145/1982185.1982471).
- Landman et al. \[2017\]
D. Landman, A. Serebrenik, and J. J. Vinju.
Challenges for Static Analysis of Java Reflection - Literature
Review and Empirical Study.
In *2017 IEEE/ACM 39th International Conference on Software
Engineering (ICSE)*, pages 507–518, May 2017.
doi: 10.1109/ICSE.2017.53.
- Lim \[1994\]
W. C. Lim.
Effects of reuse on quality, productivity, and economics.
*IEEE Software*, 11(5):23–30, 1994.
ISSN 0740-7459.
doi: 10.1109/52.311048.
- Lindholm et al. \[2014\]
T. Lindholm, F. Yellin, G. Bracha, and A. Buckley.
*The Java virtual machine specification*.
Pearson Education, 2014.
- McIntosh et al. \[2012\]
S. McIntosh, B. Adams, and A. E. Hassan.
The evolution of java build systems.
*Empirical Software Engineering*, 17(4):578–608, Aug 2012.
ISSN 1573-7616.
doi: 10.1007/s10664-011-9169-5.
URL [https://doi.org/10.1007/s10664-011-9169-5](https://doi.org/10.1007/s10664-011-9169-5).
- McIntosh et al. \[2014\]
S. McIntosh, M. Poehlmann, E. Juergens, A. Mockus, B. Adams, A. E. Hassan,
B. Haupt, and C. Wagner.
Collecting and leveraging a benchmark of build system clones to aid
in quality assessments.
In *Companion Proceedings of the 36th International Conference
on Software Engineering*, ICSE Companion 2014, page 145–154, New York, NY,
USA, 2014. Association for Computing Machinery.
ISBN 9781450327688.
doi: 10.1145/2591062.2591181.
URL [https://doi.org/10.1145/2591062.2591181](https://doi.org/10.1145/2591062.2591181).
- Mitropoulos et al. \[2014\]
D. Mitropoulos, V. Karakoidas, P. Louridas, G. Gousios, and D. Spinellis.
The bug catalog of the maven ecosystem.
In *Proceedings of the 11th Working Conference on Mining
Software Repositories*, MSR 2014, pages 372–375, New York, NY, USA, 2014.
ACM.
ISBN 978-1-4503-2863-0.
doi: 10.1145/2597073.2597123.
URL [http://doi.acm.org/10.1145/2597073.2597123](http://doi.acm.org/10.1145/2597073.2597123).
- Myers and Stylos \[2016\]
B. A. Myers and J. Stylos.
Improving API usability.
*Communications of the ACM*, 59(6):62–69,
2016.
- Naur and Randell \[1969\]
P. Naur and B. Randell, editors.
*Software Engineering: Report of a Conference Sponsored by the
NATO Science Committee, Garmisch, Germany, 7-11 Oct. 1968, Brussels,
Scientific Affairs Division, NATO*.
Newcastle University, 1969.
- Nguyen et al. \[2020\]
P. T. Nguyen, J. Di Rocco, D. Di Ruscio, and M. Di Penta.
Crossrec: Supporting software developers by recommending third-party
libraries.
*Journal of Systems and Software*, 161:110460, 2020.
- Pham et al. \[2016\]
H. V. Pham, P. M. Vu, T. T. Nguyen, et al.
Learning API usages from bytecode: a statistical approach.
In *Proceedings of the 38th International Conference on Software
Engineering*, pages 416–427. ACM, 2016.
- Qiu et al. \[2016\]
D. Qiu, B. Li, and H. Leung.
Understanding the API usage in Java.
*Information and software technology*, 73:81–100,
2016.
- Quach et al. \[2017\]
A. Quach, R. Erinfolami, D. Demicco, and A. Prakash.
A multi-os cross-layer study of bloating in user programs, kernel and
managed execution environments.
In *Proceedings of the 2017 Workshop on Forming an Ecosystem
Around Software Transformation*, pages 65–70. ACM, 2017.
- Rastogi et al. \[2017\]
V. Rastogi, D. Davidson, L. De Carli, S. Jha, and P. McDaniel.
Cimplifier: Automatically debloating containers.
In *Proceedings of the 2017 11th Joint Meeting on Foundations of
Software Engineering*, ESEC/FSE 2017, pages 476–486, New York, NY, USA,
2017. ACM.
ISBN 978-1-4503-5105-8.
doi: 10.1145/3106237.3106271.
URL [http://doi.acm.org/10.1145/3106237.3106271](http://doi.acm.org/10.1145/3106237.3106271).
- Roover et al. \[2013\]
C. D. Roover, R. Lämmel, and E. Pek.
Multi-dimensional exploration of API usage.
In *21st International Conference on Program Comprehension*,
ICPC, pages 152–161, 2013.
doi: 10.1109/ICPC.2013.6613843.
- Salza et al. \[2019\]
P. Salza, F. Palomba, D. Di Nucci, A. De Lucia, and F. Ferrucci.
Third-party libraries in mobile apps.
*Empirical Software Engineering*, Aug 2019.
ISSN 1573-7616.
doi: 10.1007/s10664-019-09754-1.
URL [https://doi.org/10.1007/s10664-019-09754-1](https://doi.org/10.1007/s10664-019-09754-1).
- Seo et al. \[2014\]
H. Seo, C. Sadowski, S. Elbaum, E. Aftandilian, and R. Bowdidge.
Programmers’ build errors: A case study (at google).
In *Proceedings of the 36th International Conference on Software
Engineering*, ICSE 2014, pages 724–734, New York, NY, USA, 2014. ACM.
ISBN 978-1-4503-2756-5.
doi: 10.1145/2568225.2568255.
URL [http://doi.acm.org/10.1145/2568225.2568255](http://doi.acm.org/10.1145/2568225.2568255).
- Sharif et al. \[2018\]
H. Sharif, M. Abubakar, A. Gehani, and F. Zaffar.
Trimmer: Application specialization for code debloating.
In *Proceedings of the 33rd ACM/IEEE International Conference on
Automated Software Engineering*, ASE 2018, pages 329–339, New York, NY, USA,
2018. ACM.
ISBN 978-1-4503-5937-5.
doi: 10.1145/3238147.3238160.
URL [http://doi.acm.org/10.1145/3238147.3238160](http://doi.acm.org/10.1145/3238147.3238160).
- Shull et al. \[2007\]
F. Shull, J. Singer, and D. I. Sjøberg.
*Guide to Advanced Empirical Software Engineering*.
Springer-Verlag, Berlin, Heidelberg, 2007.
ISBN 184800043X.
- Soto-Valero et al. \[2019\]
C. Soto-Valero, A. Benelallam, N. Harrand, O. Barais, and B. Baudry.
The Emergence of Software Diversity in Maven Central.
In *16th International Conference on Mining Software
Repositories*, MSR 2019, pages 1–10, New York, NY, USA, 2019. ACM.
doi: 10.1145/2597073.2597097.
URL [http://doi.acm.org/10.1145/2597073.2597097](http://doi.acm.org/10.1145/2597073.2597097).
- Varanasi and Belida \[2014\]
B. Varanasi and S. Belida.
*Maven Dependency Management*, pages 15–22.
Apress, Berkeley, CA, 2014.
ISBN 978-1-4842-0841-0.
doi: 10.1007/978-1-4842-0841-0\_3.
URL [https://doi.org/10.1007/978-1-4842-0841-0\_3](https://doi.org/10.1007/978-1-4842-0841-0_3).
- Vázquez et al. \[2019\]
H. Vázquez, A. Bergel, S. Vidal, J. D. Pace, and C. Marcos.
Slimming javascript applications: An approach for removing unused
functions from javascript libraries.
*Information and Software Technology*, 107:18–29,
2019.
ISSN 0950-5849.
doi: https://doi.org/10.1016/j.infsof.2018.10.009.
URL [http://www.sciencedirect.com/science/article/pii/S0950584918302210](http://www.sciencedirect.com/science/article/pii/S0950584918302210).
- Wu et al. \[2017\]
Y. Wu, Y. Manabe, T. Kanda, D. M. German, and K. Inoue.
Analysis of license inconsistency in large collections of open source
projects.
*Empirical Software Engineering*, 22(3):1194–1222, Jun 2017.
ISSN 1573-7616.
doi: 10.1007/s10664-016-9487-8.
URL [https://doi.org/10.1007/s10664-016-9487-8](https://doi.org/10.1007/s10664-016-9487-8).
- Yu et al. \[2003\]
Y. Yu, H. Dayani-Fard, and J. Mylopoulos.
Removing false code dependencies to speedup software build processes.
In *Proceedings of the 2003 Conference of the Centre for
Advanced Studies on Collaborative Research*, CASCON, pages 343–352. IBM
Press, 2003.
URL [http://dl.acm.org/citation.cfm?id=961322.961375](http://dl.acm.org/citation.cfm?id=961322.961375).
