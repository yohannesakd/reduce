# A feature flag that every user already has

**Signal.** A flag that is fully rolled out. The "off" branch runs for nobody.

```ts
if (flags.isEnabled("new_checkout")) {
  return newCheckout(cart);
} else {
  return legacyCheckout(cart);
}
```

**Decide with.** The flag system of record decides, not the code. Check the rollout state in every environment, tenant override, and config file. Check whether an operator still uses the flag as a kill switch.
Staleness is hard to decide, so do not infer it from the age of the flag.
A removal touches several kinds of unit. Plan them in one phase:

1. The flag check and the "off" branch.
2. `legacyCheckout` and its helpers, when no other caller exists.
3. Tests of the "off" state. Tests of the "on" state stay, with the flag setup removed.

```ts
return newCheckout(cart);
```

Mechanical tools handle the check removal. A person or agent decides each test: delete it, or rewrite it around the new default.

**Keeps it when.** The flag is a kill switch that a source requires. The flag is seasonal. A tenant override still exists.

**Sources.** [Uber AutoClean](https://x.com/UberEng/status/2112604623454470476), [Piranha](https://eng.uber.com/piranha/), [Uber post summary](https://www.uber.com/us/en/blog/ai-code-cleanup/).
