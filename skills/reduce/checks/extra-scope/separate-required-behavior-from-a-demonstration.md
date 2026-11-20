# Separate required behavior from an unsolicited demonstration

**Source:** Simon Willison, 16 August 2026. **Evidence:** firsthand experiment with prompts, generated HTML, and reported results.

**Look for.** An interface, demonstration, or sample scene that the request did not ask for, next to the required behavior.

**Required behavior.** Accept an image URL and JSON boxes. Scale coordinates from 0–1,000 and display labelled rectangles over the image.

**Observed.** Qwen added a substantial interface and an unrequested canvas-generated pelican scene. Willison calls it overengineering; the scene does not implement coordinate scaling.

**Applies when.** Keep behavior needed for correctness, including implied behavior.

**Limits.** No successful human rewrite is shown. Disabling reasoning produced misplaced boxes, so reduced effort did not keep correctness automatically.

**Reduce fit.** A reachable demonstration is behavior. Report it. Remove it only when no entry point exposes it.

[Report and results](../../sources/web/simonwillison-net-2026-aug-16-qwen-38-27b.md). [Original prompt and generated implementation](../../sources/github/gist-121ad098860028b2fab603fa12da1fd9.md).
