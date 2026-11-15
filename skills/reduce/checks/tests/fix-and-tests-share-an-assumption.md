# A fix and its tests share one wrong assumption

**Signal.** The tests were written by the same author, in the same session, from the same reading of the code.

**Decide with.** Keep one reproduction that a person checked against the required behavior. For a fix, it fails on the base revision and passes on the reduced code.
For a structural reduction, the check passes on both revisions. Then it must be a check that the person traced to a required entry, not a snapshot of the current output.
Mark an inventory entry that only generated tests prove as `confirmed by run`, with the limit stated.

**Keeps it when.** A person traced the test to a required entry. For a fix, the test also fails on the base revision and passes on the reduced code.

**Sources.** [@mjovanovictech](https://x.com/mjovanovictech/status/2115746465511362615), [Anaconda](https://www.anaconda.com/blog/deslopping-ai-code).
