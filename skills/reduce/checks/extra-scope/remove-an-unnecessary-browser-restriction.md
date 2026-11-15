# Remove an unnecessary browser restriction, then verify the real inputs

**Source:** Simon Willison, Hacker News follow-up, 17 August 2026. **Evidence:** same task, two models, linked code, author-reported testing.

**Look for.** A restriction or option whose operation the task does not need.

**Observed.** Glimmer produced a smaller application that worked with the supplied same-origin image. It also inserted:

```js
img.crossOrigin = 'anonymous';
```

Willison identifies that line as the cause of failure with an external image URL. The task needs image display and dimensions, not pixel extraction.

**Inferred practice.** Remove a platform restriction only after checking which operation needs it. Verify representative external inputs before calling a smaller version equivalent.

**Applies when.** Inference: no required operation needs the restriction, and representative external inputs still work without it.

**Limits.** This is a human diagnosis of generated code. No corrected execution is published, and the comparison changes models and reasoning settings.

**Reduce fit.** Removing the line changes behavior for external images. The reduce skill reports it as a suspected defect and does not plan it.

[Author's comparison and diagnosis](https://news.ycombinator.com/item?id=49325621). [Glimmer transcript](https://gist.github.com/simonw/51e8ddb2ee597a5005fa63bd4927dbf0). [Generated HTML, assignment at line 64 when inspected](https://static.simonwillison.net/static/2026/glimmer-bbox.html).
