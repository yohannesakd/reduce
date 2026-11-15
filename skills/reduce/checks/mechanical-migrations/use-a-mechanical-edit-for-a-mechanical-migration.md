# Use a mechanical edit for a mechanical migration

**Source:** Dmitriy Kovalenko, `@neogoose_btw`, X, 7 July 2025. **Evidence:** reported editing cost and a proposed command; no linked repository diff.

**Look for.** A repeated syntax change across many files.

**Observed.** An engineer reportedly spent $38.45 with Claude Code to add `| null` to element type arguments in `React.useRef` calls. Kovalenko supplied one `sed` substitution instead. Normalized:

```tsx
// Before.
React.useRef<HTMLDivElement>(null);

// After.
React.useRef<HTMLDivElement | null>(null);
```

**Inferred practice.** A repeated syntax transformation can use one explicit rule instead of repeated model-directed edits.

**Applies when.** The rule covers the real syntax and nothing else.

**Limits.** This concerns editing effort, not excess final code. The regex is not a TypeScript parser and was not validated.
Use a parser-based codemod when source shapes exceed the rule's assumptions. Inspect the diff and run the type checks.

**Reduce fit.** In a plan phase that repeats one syntax change, name the mechanical transformation and its check.

[Original X post with the command and screenshot](https://x.com/neogoose_btw/status/1942231407994208638).
