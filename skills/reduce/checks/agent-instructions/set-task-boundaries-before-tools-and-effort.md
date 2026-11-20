# Set task boundaries before selecting tools and effort

**Source:** Su, `@Sukiea1008`, X thread and proposed `AGENTS.md`. **Evidence:** community synthesis and proposed instructions; no comparative diff.

**Look for.** Agent instructions or skills that add layers, process, or tools before they state the task's intent, scope, and acceptance criteria.

**Observed.** The thread lists unnecessary abstraction, compatibility layers, duplicated implementations, excessive process, and unrelated tests.
It proposes stating intent, scope, exclusions, and acceptance criteria first, and requiring a current need for each design element.

**Inferred practice.** For each new layer, name the present requirement that needs it.

**Applies when.** Keep behavior needed for correctness, including implied behavior.

**Limits.** The author says Grok drafted the instructions and recommends testing them first. No published outcome proves their effect.
Its fixed model-effort prescriptions are hypotheses. Its treatment of Git rollback as automatically reversible also needs context.

**Reduce fit.** Map step: record the concepts and layers each item adds, and tie each to an inventory entry.

[Original synthesis](../../sources/x/sukiea1008-2093650953027383380.md). [Original instruction post](../../sources/x/sukiea1008-2093650959369187578.md). [Readable copy](../../sources/x/sukiea1008-2093650959369187578.md).
