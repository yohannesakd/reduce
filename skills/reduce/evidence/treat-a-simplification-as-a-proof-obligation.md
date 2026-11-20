# Treat a simplification as a proof obligation

**Source:** Jeffrey Emanuel, `@doodlestein`, X, 2026, and the public listing of the skill. **Evidence:** the author's own post and the listing. The listing is partly behind a subscription. The skill's files were not inspected, and no diff or result is available.

**Look for.** A reduction claim that needs a proof, not a judgment.

**Observed.** The skill states "no proof, no delete". Each candidate gets a written card that says why the old and new code behave the same. An auditor challenges the card before any edit, and a machine gate checks the result.
It never merges clones that have different reasons to change. It logs each rejected candidate with its reason.

**Inferred practice.** A claim that a smaller program is equivalent needs a baseline, a written reason, and a gate that a machine checks. A rejection log stops the same candidate from returning.

**Applies when.** The inventory inputs cover the behavior that the claim touches.

**Limits.** The score threshold in the listing has no evidence behind it in this file, and the skill is far larger than this one: 98 files by the author's count. This skill does not adopt the threshold. Line count stays a secondary measure.

**Reduce fit.** Proof in the check step. The gate, the card, and the rejection log are in [Baseline and gates](execution-checks.md#baseline-and-gates). The clone types are in [A clone, by degree of similarity](../checks/duplicates-and-existing-code/clone-by-similarity.md).

[Author's post](../sources/x/doodlestein-2047808489838329993.md). [Skill listing](../sources/web/jeffreys-skills-md-skills-simplify-and-refactor-code-isomorphically.md).
