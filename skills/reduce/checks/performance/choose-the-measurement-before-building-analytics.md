# Choose the measurement before building an analytics system

**Source:** Walter, `@WalterAIBuilder`, X, 16 October 2026. **Evidence:** firsthand account and linked application; no diff.

**Look for.** An analytics, tracking, or metrics system that the code builds before it defines the one measurement that the product needs.

**Observed report.** For a popularity indicator, the author reports a proposed analytics architecture with APIs, event tracking, and data pipelines.
He proposes an image tag that requests a transparent pixel, with the server counting requests. He displays `New` while data remains insufficient.

**Inferred practice.** Define the measurement the product needs before choosing collection infrastructure.

**Applies when.** Request counts are adequate for the indicator.

**Limits.** The post supplies no code or test results. Pixel requests do not inherently measure unique visitors or engagement.

**Reduce fit.** The choice of measurement is a product decision. Use the case only for internal infrastructure that serves one measurement the target already shows.

[Original X report](../../sources/x/walteraibuilder-2110911524663627988.md). [Linked application](../../sources/web/webify-tools.md).
