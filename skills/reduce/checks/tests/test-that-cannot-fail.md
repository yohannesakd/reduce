# A test that cannot fail for the right reason

**Signal.** A test whose assertion repeats the code, checks a mock, or passes when the behavior breaks.

Review each test with these six failure modes. Each has a review test that settles it.

| Failure mode | Example | Review test |
| --- | --- | --- |
| Tautology | `assert total(items) == sum(i.price for i in items)` repeats the code under test | Does the code under test appear on both sides? |
| Mocked-away logic | `patch("shop.pricing.calc_total", return_value=100)` then `assert checkout(cart).total == 100` | Does the test fail when the real logic behind each mock breaks? If a mock replaces the logic that the test names, the test checks the mock. |
| Happy path only | One valid input, one success | Which empty, boundary, failure, and permission cases are missing? |
| Snapshot of current behavior | `assert out == {"id": 7, ...}` pasted from a run | Does each expected value have a source other than the code? |
| Weakened assertion | `expect(result).toBeDefined()` | Search for `toBeTruthy`, `toBeDefined`, and `toContain` on numbers. |
| Duplicate coverage | Five tests that follow one path with small setup changes | Group by path. For each test, name the regression that only it detects. A test with no such regression is a candidate for `remove`. |

**Decide with.** Break the code on purpose. Choose a defect that violates the behavior that the test names, on the inputs that the test uses. For a test of totals, change the sum, not the empty-input branch.
If the test stays green, it does not prove that behavior. Treat that as missing evidence. Rewrite the test, or find another check that detects the defect. Give the test `remove` only when the kept checks detect every material regression that it detects.
A surviving mutation of an unrelated branch says nothing about the test.
A generated suite can raise coverage without protection: one report counted 96 of 240 generated tests that asserted only that something was returned.

**Keeps it when.** It fails when the behavior breaks and passes when only internals change.

**Sources.** [Tesbo](../../sources/web/tesbo-io-insights-roadmap-reviewing-ai-written-tests.md), [Zidane Wu](../../sources/web/zidanewu-com-posts-ai-generated-tests-hidden-cost.md), [Daniel Moka⚡](../../sources/x/dmokafa-2114977298122244116.md).
