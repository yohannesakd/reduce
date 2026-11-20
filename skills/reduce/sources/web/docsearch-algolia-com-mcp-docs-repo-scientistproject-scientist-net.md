# Scientist.NET Documentation · DocSearch MCP

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Date: 2026-08-01
- Original location: https://docsearch.algolia.com/mcp/docs/repo/scientistproject/scientist.net
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
### Core concepts: Control vs Candidate

master
Scientist.NET uses two primary abstractions to facilitate safe refactoring:

- **Control**: The existing, proven implementation. It is defined using the `experiment.Use()` method. The result of the `Use` block is what is ultimately returned to the caller of `Scientist.Science<T>`.
- **Candidate**: The new, refactored implementation being tested. It is defined using the `experiment.Try()` method. Scientist monitors the candidate for performance, correctness (result matching), and exceptions, but its output is not returned to the caller.

If no `Try` blocks are declared within an experiment, the Scientist machinery is bypassed and the control value is returned directly.
