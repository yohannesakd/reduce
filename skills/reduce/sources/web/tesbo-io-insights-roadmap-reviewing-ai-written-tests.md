# Reviewing AI-Written Tests: Six Failure Modes

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Date: 2026-08-24
- Original location: https://www.tesbo.io/insights/roadmap/reviewing-ai-written-tests
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
[Stage 6b · Specialise: AI as your instrument](/insights/roadmap#l6)

# Reviewing AI-written tests

Generated tests are confident, well-formatted, and frequently assert nothing meaningful. The failure modes are specific and learnable: tautological assertions, mocked-away logic, coverage of the happy path only. This is the job now.

Reviewing generated tests is a distinct skill from writing them, and it is now most of the job.

The reason is that generated tests look finished. They are well formatted, they have sensible names, they follow the framework's idioms, and they pass. None of that tells you whether they check anything.

There are six failure modes, they recur across every model and framework, and once you know them a review takes ten minutes rather than an hour.

## The terms you will hear

- **Tautological assertion.** A check that cannot fail, such as asserting a value equals itself.
- **Over-mocking.** Replacing so much of the system that the test exercises the mock rather than the code.
- **Snapshot test.** A stored copy of current output, compared on later runs.
- **Assertion strength.** How specific a check is. `toBe('35.99')` is strong, `toBeTruthy()` is weak.
- **Coverage theatre.** A suite with a high coverage number and little real checking.

## The six failure modes

**1. The tautology.** The test computes the expected value with the same code it is testing, so both sides always agree. Look for the code under test appearing on both sides of the assertion.

**2. Mocked-away logic.** Everything interesting is stubbed. The test asserts that the stub returned what the stub was told to return. Common when the generator could not work out how to set up real data.

**3. Happy path only.** One valid input, one success. No empty case, no boundary, no failure. This is the most common mode by a wide margin.

**4. A snapshot of today's behaviour.** With no oracle available, the generator runs the code and asserts whatever came out. If that behaviour is wrong, the bug is now locked in and protected by a test. The [test oracle](/insights/roadmap/test-oracles) problem, in a file.

**5. The weakened assertion.** `toContain` where `toBe` belonged. A regex loose enough to match anything. Often introduced when a strict assertion failed and the generator softened it to get a green run.

**6. Duplicate coverage.** Five tests exercising one path through slightly different setup. Costs runtime and maintenance, and adds no protection.

## Why it matters

Because a suite of weak tests is worse than a small suite of strong ones, and it looks better on every metric.

For example, a team generated 240 tests in an afternoon and coverage jumped from 41 to 78 per cent. Two months later a pricing defect reached production with the suite green. On review, 96 of those tests asserted only that a function returned something, and the pricing tests mocked the calculator they were meant to exercise. The number went up and the protection did not.

## The ten-minute review checklist

1. **Read the assertions first.** Skip the setup on the first pass. Weak assertions are visible immediately.
2. **Grep for the weak ones.** `toBeTruthy`, `toBeDefined`, `not.toBeNull`, `toContain` on numbers, bare `expect(result)`.
3. **Count the mocks per test.** More than two or three usually means the test is checking the mocks.
4. **Look for the missing cases.** Empty, boundary, failure, permission. Generated suites almost never include the last one.
5. **Check each expected value has a source.** If it came from running the code, mark it and go and find the real oracle.
6. **Break something on purpose.** Change one line in the product and confirm the test fails. This single step catches tautologies and over-mocking faster than reading ever will.
7. **Delete the duplicates.** Keep the clearest one of each group, which is the same discipline as [choosing what stays in a pack](/insights/roadmap/choosing-the-regression-pack).

The suite going green is the claim. Changing one line of the product and watching it go red is the evidence.


## A worked review

For example, here is a real review of twelve generated tests for the gift-card calculator.

```
GENERATED  12 tests for applyGiftCard()   review time: 11 minutes
KEPT (5)
  applies full balance when balance < total          strong, real values
  charges remainder to the card                      strong, exact 10.99
  rejects an already-spent code                      strong, checks message
  rounds .49 totals correctly                        strong, the risk case
  refuses a code from another customer               strong, I asked for this
REJECTED (7)
  1  expect(applyGiftCard(basket, card)).toBeTruthy()
     tautology. returns an object, so always truthy.        deleted
  2  mocks calculateTotal, mocks getCardBalance, then asserts
     the result equals the mocked balance
     over-mocked. tests the mocks.                          rewritten
     with real values, then found a real defect at .99
  3  three near-identical tests for a valid 25.00 card
     duplicates. kept one.                                  2 deleted
  4  expect(result.remaining).toContain('0')
     weakened. '0.01' and '10.00' both contain '0'.         fixed to
     toBe('0.00')
  5  snapshot of the confirmation object, generated by running
     the code as it is today
     no oracle. the snapshot includes the 1p rounding bug,
     so it would have protected the defect.                 deleted
BREAK TEST
  changed one line in applyGiftCard to add a penny.
  before review: 3 of 12 failed.
  after review:  5 of 5 failed.
  that difference is the whole value of the review.
```
The break test at the bottom is the most useful number on this page. Twelve tests caught a deliberate defect three times. Five reviewed tests caught it five times out of five.

## How to show you know it

- **A before-and-after break test.** Nine words and two numbers, and it ends the debate about generated test quality.
- **A rejected snapshot.** Explaining that a snapshot of current behaviour would have protected a real bug demonstrates you understand oracles.
- **A grep list.** Your own list of weak-assertion patterns for your framework. Small artefact, used every week.
- **A kept-to-rejected ratio.** "Twelve generated, five kept." Honest, and much more credible than enthusiasm.

## Questions

## Is it faster to write tests by hand than to review generated ones?

For a handful of cases, often yes. For volume, generate and review, because reviewing is quicker than typing once you know the six modes. The break test keeps you honest about which situation you are in.

## How do I stop the generator writing weak assertions?

Give it the expected values and an example of your house style, and say every test must have exactly one strong assertion. That is the [prompting](/insights/roadmap/prompting-for-test-work) fix, and it removes most of mode five.

## Should generated tests be marked as generated?

A short note in the pull request is enough. What matters more is that somebody reviewed them, and that the review is visible.

## What if coverage drops when I delete the weak ones?

Then coverage was measuring the wrong thing. Say so plainly, with the break-test numbers beside it. A lower number with real protection is the better position.

Mark this complete once you have done the practice in the guide, not merely once you have scrolled to the end. The tick stays in this browser; nothing is sent anywhere.
