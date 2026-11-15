# A behavior that nothing needs

**Signal.** An inventory entry has no consumer or unknown consumers, serves no capability or only a `questioned` one, or contradicts the purpose. Or a consumer reads the result but discards it, or shows and sends nothing because of it.

**Decide with.** For each such entry, find what input reaches it and how often, what fails without it, and who would notice.
Search for a counterexample: an input, state, or event order that reaches it, including retry, restore, and operator actions. Missing writers, elapsed time, or representable states alone prove neither reachability nor unreachability.
Removal of an `incidental` result is a contingent reduction: its effect is `intent`. The user decides, unless the design document already decides its capability: a design finding with the decision `autonomous`, or the user's answer.
An entry that contradicts the purpose is a suspected defect, not a reduction. In a full run, record it as a lead, as the packet says. In a quick run, list it in the report.

**Keeps it when.** A consumer, requirement, or reachable input needs the behavior. An `unknown` entry stays `unresolved`. It is never a removal.
