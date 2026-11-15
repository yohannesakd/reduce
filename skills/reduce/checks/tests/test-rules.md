# Tests

**Signal.** The feature has a test, fixture, mock, or test helper, or a test expectation that changed.

**Decide with.** Map each test to the inventory entries that it proves. Then apply the rules below, rung by rung.

**Keeps it when.** The test fails when the behavior breaks, passes when only internals change, and no kept check detects every material regression that it detects.

A lasting test protects material behavior or a shared contract that future work could plausibly break.
It must fail when that behavior breaks and pass when only internals change.
Map inventory IDs to proving tests. Before removal, record covered behavior and equivalent remaining protection.

| Rung | Test decision |
|---|---|
| `remove` | No behavior/shared contract protected, or a kept check detects every material regression it detects |
| `prevent` | Type, schema, or compiler makes the failure impossible |
| `reuse` | Extend an existing test proving the behavior |
| `simplify` | Merge cases for one behavior; remove irrelevant internal assertions, mocks, and fixtures |
| `keep` | Smallest proof at the boundary the behavior reaches |

Private structure, framework behavior, impossible states, incidental call order, and removed code suggest removal; trace the actual contract first.
Keep mocks/order assertions protecting required interactions or ordering. Two tests of one behavior can detect different regressions.
Source, types, or scratch checks can settle local/temporary/structural work without lasting tests.
For uncovered material behavior, first extend an existing test; use scratch proof when lasting infrastructure is disproportionate, recording limits.
Compare outside-target tests covering the same behavior. Record other weak tests as follow-ups.
Trace a broken implementation through the test's inputs. When execution is needed, plant it in permitted scratch.
A green result does not prove protection.
Never accept a changed expected value in a test as a reduction. A changed expected value needs a source that requires the new result.
