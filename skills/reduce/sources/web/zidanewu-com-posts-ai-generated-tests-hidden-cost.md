# The Hidden Cost of AI-Generated Tests — Why 90% Coverage Means Nothing

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: Zidane
- Date: 2026-03-20
- Original location: https://zidanewu.com/posts/ai-generated-tests-hidden-cost/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
We hit 95% test coverage on a service and felt good about it. Three weeks later, a bug in that exact service caused a production incident. The bug was in a code path that was — technically — covered.

That’s when I started paying closer attention to what our AI-generated tests actually test.

## Table of Contents[#](#table-of-contents)

## The Coverage Illusion[#](#the-coverage-illusion)

Coverage tools measure lines executed, not logic verified. An AI can write a test that calls a function, asserts that it returns something, and walks away with a green checkmark — without ever checking whether that something is correct.

When I ask Claude or Copilot to “write tests for this function,” I get tests fast. Often 80% of them are fine. But the remaining 20% create a false sense of security that’s worse than no tests at all.

The problem isn’t AI. Coverage numbers were already a flawed metric before AI got involved. AI just accelerates the accumulation of low-quality tests that look impressive in dashboards.

## Tautological Tests: When Tests Prove Nothing[#](#tautological-tests-when-tests-prove-nothing)

A tautological test asserts what the code already does, not what the code should do.

Here’s a simplified version of what we found:

```
def calculate_discount(price, user_tier):
    if user_tier == "premium":
        return price * 0.8
    return price
# AI-generated test
def test_calculate_discount():
    result = calculate_discount(100, "premium")
    assert result == calculate_discount(100, "premium")  # asserts against itself
```
That’s a contrived example, but real versions are only slightly more subtle: asserting that a function returns what it returns, not what it *should* return based on business logic.

The test passes. Coverage ticks up. The function could return anything and the test would still pass.

## Implementation Coupling: Brittle by Design[#](#implementation-coupling-brittle-by-design)

When AI generates tests by reading the implementation, it tends to mirror the implementation structure. Refactor the internals while keeping the behavior identical — a completely valid engineering move — and the tests break. Now you have tests that signal false negatives on correct code.

This erodes trust in the test suite. Engineers start ignoring failing tests because “it’s probably just an implementation detail change.” That attitude is how real bugs sneak through.

Tests should document expected behavior from the outside. AI-generated tests often document how the function works internally. Those are different things.

## The Edge Cases AI Consistently Misses[#](#the-edge-cases-ai-consistently-misses)

AI is good at the happy path. It’s mediocre at edge cases and bad at domain-specific invariants that only exist in your system.

Common gaps I’ve seen:

- **Boundary conditions** — off-by-one errors at limits, empty collections, zero values
- **Concurrency** — tests that pass in isolation but fail under load or parallel execution
- **State accumulation** — what happens when the same function runs multiple times on the same object
- **Integration assumptions** — mocks that don’t reflect how real dependencies actually behave

The last one is particularly insidious. You can have a perfectly tested service that fails the moment it hits a real database because the mocks were too optimistic.

## What the Three-Week Bug Looked Like[#](#what-the-three-week-bug-looked-like)

Back to the incident. We had a data processing pipeline with a function that handled null values in an input stream. The function had tests. Coverage was 95%.

The bug: when two specific null-adjacent conditions appeared in sequence — a pattern we’d seen in production data but hadn’t encoded as a test — the function produced a subtly wrong output instead of raising an error.

The AI had generated tests for null input, for normal input, for various edge values. It had not generated a test for that specific temporal ordering of conditions, because that required knowing something about the upstream data source that wasn’t visible in the function signature.

That domain knowledge lived in someone’s head and in a Slack thread from eight months ago. The AI had no access to either.

## The Tradeoffs You Have to Accept[#](#the-tradeoffs-you-have-to-accept)

I’m not saying stop using AI for tests. Calibrate your expectations.

**What AI does well:**

- Generating boilerplate test structure quickly
- Happy path coverage
- Reducing time to get from zero to first draft

**What AI does poorly:**

- Understanding business invariants not in the code
- Generating tests based on historical bug patterns
- Writing integration tests that reflect real external behavior
- Thinking adversarially about your system

The speed-vs-depth tradeoff is real. AI gives you fast, shallow tests. For many utility functions, that’s fine. For anything touching money, data integrity, or external systems, shallow tests are dangerous because they create the illusion of coverage.

There’s also a team culture risk: if engineers stop thinking critically about test quality because “the AI wrote it,” you’ve made your codebase more fragile while making the coverage dashboard happier.

## A Practical Review Checklist[#](#a-practical-review-checklist)

When reviewing AI-generated tests, I check for:

1. Does the assertion reference the expected value directly — not the function itself?
2. Would this test fail if the implementation had a subtle bug?
3. Is there a test for behavior at the boundary — one below, one above?
4. Are the mocks behaving like the real dependency would?
5. Does this function have domain-specific invariants the AI couldn’t have known?

If the answer to #5 is yes, someone with domain knowledge needs to write those tests. AI can’t.

For context on how AI fits into a broader review process, see [how I structure AI code review](/posts/ai-code-review-2026/) and [common AI code generation mistakes](/posts/ai-code-generation-mistakes/).

## Final Take[#](#final-take)

95% coverage felt like a milestone. It turned out to be a false floor.

AI-generated tests are a productivity tool, not a quality guarantee. The coverage number is useful for tracking gross gaps — not for certifying correctness. Treat AI-generated tests like a first draft that needs a critical read, not a finished product.

The three-week bug cost us more than the time we saved generating those tests quickly. That math only needs to happen once.
