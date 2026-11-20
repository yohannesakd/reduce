# Split flag cleanup between mechanical rewrites and judgment

**Source:** Uber Engineering, X article, October 2026. **Evidence:** the vendor's own report; no public diff. The article text was read through its background section. The pipeline details come from a search summary of the same post.

**Look for.** A feature flag that is fully rolled out.

**Observed.** Uber manages thousands of feature flags. After a rollout, the conditional branches and tests of a flag stay behind. One cleanup can touch dozens of files across boolean logic, helpers, call sites, configs, and tests.
Some tests are deleted. Others are rewritten around the new default. The post reports that agents also lose time parsing the dead code, so sessions run longer and cost more.
The system starts from the flag system of record, rewrites the code, fixes CI failures, and sends the diff to a separate agentic validator before a person reviews it.
Deterministic tools handle mechanical cases, such as removing a default that nothing uses. Agents handle the decisions, such as whether to delete or rewrite a test.

**Inferred practice.** Start from the system of record, not from the code. Remove the flag check, the unused branch, its helpers, and the tests of the unused state together. Use a deterministic rewrite where one exists, and judgment for tests. Validate with a reviewer that did not write the change.

**Applies when.** No kill switch, override, or season depends on the flag.

**Limits.** The report is from the company that built the system, and it gives no outcome numbers that this skill can reuse. Staleness is hard to decide. A flag can serve as a kill switch, or an override can still exist.

**Reduce fit.** `remove` across units, with the flag state as evidence in the check step. A kill switch that a source requires is `keep`.

[Uber post on X](../../sources/x/ubereng-2112604623454470476.md). [Search summary of the post](../../sources/web/uber-com-us-en-blog-ai-code-cleanup.md). [Piranha, the earlier tool](../../sources/web/eng-uber-com-piranha.md).
