# A fresh design needs less

**Signal.** The current design has owners, layers, types, or steps that a design for the `required` behavior alone would not have. Local edits only polish an elaborate construction.

**Decide with.** Do not start from the current code. Sketch a fresh design from the feature's `required` inventory entries, or from the accepted requirements for a plan. Choose owners and data shapes before files.
Compare it with the current design: owners and types, names and flow, abstractions, errors and state, tests, duplicated rules, ordering, and coupling. Record each concrete difference with its benefit and tradeoff.
Both designs must meet the same acceptance checks.

**Keeps it when.** The fresh design is not simpler by concepts, branches, layers, or dependencies. Or the current design gives a structural benefit that the sketch loses. Moving or reformatting code alone is not an improvement.

**Source.** Andrej Karpathy reports generated code with bloated APIs, abstractions, and dead code. A request for a simpler construction gave about 100 lines in place of 1,000.
He recommends explicit success criteria and a simple, likely correct baseline before optimization. The line counts are his account, not a published measurement.
[Original X post](../../sources/x/karpathy-2015883857489522876.md), 26 January 2026. [Archived post](../../sources/web/jaytaylor-com-notes-node-1769465010000-html.md).
