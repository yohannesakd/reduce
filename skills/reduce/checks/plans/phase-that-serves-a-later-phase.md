# A phase or abstraction that serves a later phase only

**Signal.** A plan phase that prepares an abstraction for a second implementation that no requirement names.

```text
Phase 2: Introduce NotificationStrategy interface and EmailStrategy.
Phase 3: Add SmsStrategy.            <- no accepted source requires SMS
```

**Decide with.** First classify what Phase 3 delivers, using the kinds in the [plan rules](../../guides/plan-rules.md#requirement-kinds).

- SMS that users receive is an observable result. With no accepted source, it is `added by plan`. Keep the SMS entry in the reduced plan, and report it as a product question.
  Apply the ladder to Phase 2 on its own. Each candidate must deliver both channels. If a plain function per channel delivers both with fewer concepts, the interface is `simplify`.
- A strategy that only the plan's implementer sees, such as an unused second class, is design. Which requirement entry fails without Phase 2? If only Phase 3 needs it, both phases are `remove`. Keep one concrete email sender.

A strategy with one implementation is a hypothetical seam.

**Keeps it when.** An accepted source requires the second channel, and the interface removes branches or duplicate code that the two channels would otherwise carry. Then Phase 2 stays, ordered before Phase 3.
