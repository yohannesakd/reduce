# Deliver the requested component instead of several expanded variants

**Source:** Ponytail's published countdown example. **Attribution:** controlled model-output comparison, not a handwritten human replacement. The capture date is not established.

**Look for.** Several variants, extra features, or usage examples delivered for one request.

**Required behavior.** Provide a React component that counts down from a supplied number of seconds.

**Observed, unguided output.** Several implementations: basic timer, advanced timer, custom hook, styled timer, CSS, and usage examples, with controls, formatting, callbacks, and animations.

**Observed, guided output.** Remaining-seconds state, timer setup, cleanup, and display, without the additional features.

```text
Before
  Countdown + controls + formatted clock + callbacks + hook
  + styled variant + animations + CSS + multiple usage examples

After
  Remaining seconds + one timer effect + cleanup + display
```

**Inferred lesson.** Simplicity starts with selecting the required behavior. Removing optional features reduces product scope; compressing their code does not.

**Applies when.** Inference: the request names the required behavior, and no requirement traces to the extra variants or features.

**Limits.** The reported 267-to-9 comparison counts code across several unguided variants. It is not a reduction of one 267-line component with identical features.
A smaller feature set is equivalent only when the omitted behavior was not required.

**Reduce fit.** Removing reachable features is a product decision. The reduce skill keeps them and reports them.
The reduce skill removes a variant only when no entry point exposes it, such as an unexported or unused copy.

**Supporting experiment.** Ponytail's experiment dated 7 October 2026 compares 39 tasks under different instructions, with five runs per task and condition.
Its date-picker task reports median source sizes of 335 lines without the skill and 10 with Ponytail 5. The smaller approach reuses an existing input and the browser's date control.
This supports reuse of a platform feature. It does not establish identical customization or browser behavior.
Only 18 tasks had executable hidden correctness checks. The date-picker task was in the code-size group, with model-judged completeness.

[Verbatim outputs and original task](../../sources/github/dietrichgebert-ponytail-examples-react-countdown-md.md). [Dated methodology and per-task results](../../sources/github/dietrichgebert-ponytail-benchmarks-results-2026-10-07-agentic-md.md).
