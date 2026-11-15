# Reuse a protocol implementation instead of rebuilding it

**Source:** ARIES PR 90, opened 14 October and merged 19 October 2026. **Attribution:** verified simplification; AI authorship of the old code is unproven.

**Look for.** Custom code implements a standard format, protocol, or platform feature: parsing or encoding, a network protocol, retry with backoff, argument parsing, or a polyfill for a supported API.

**Required behavior.** Exchange WebSocket messages with the gateway while respecting cancellation and message limits.

**Observed, expanded approach.** A local HTTP upgrade handshake, connection setup, frame masking, payload lengths, opcode checks, and close-frame validation.

**Observed, human-directed change.** Replace the protocol machinery with Gorilla WebSocket. Keep application-specific cancellation, size limits, and text validation.

```text
Before
  Application -> custom handshake + custom encoder/decoder -> socket

After
  Application-specific limits and cancellation -> Gorilla WebSocket
```

**Other forms.** A hand-written CSV, URL, date, or version parser. A retry loop with custom backoff next to a client that retries. A polyfill for an API that every supported runtime has.

```ts
const query = Object.fromEntries(url.split("?")[1].split("&").map(p => p.split("=")));
// existing: new URL(url).searchParams
```

**Measured scope.** The production WebSocket file changes by +73/−313 lines. Related tests change and expand; the overall PR is not a net code reduction.

**Inferred lesson.** Give standard mechanics to an existing implementation, and keep application policy at the application boundary. Reuse moves complexity; it does not erase it.

**Applies when.** The library supports every protocol behavior that the inventory needs.

**Limits.** The replacement also changes protocol support, so exact equivalence is not established. Evaluate the dependency's behavior and cost alongside the removed code.

**Reduce fit.** `reuse`. The new dependency is an item. Prove each protocol entry in the inventory against the library before you plan the change.

[PR](https://github.com/hyscale-lab/ARIES/pull/90). [Protocol replacement commit](https://github.com/hyscale-lab/ARIES/commit/e215f33b1e).
