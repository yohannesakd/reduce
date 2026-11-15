# Call a guaranteed method directly

**Source:** Javad Rahmatzadeh, GNOME extension reviewer, 6 December 2025. **Attribution:** reported AI output and an explicit human replacement.

**Look for.** A check or catch guards a state that a contract already excludes: a check that a required method exists, optional access on a value that cannot be null, a default for a value that is always set, or a catch around code that cannot fail.

**Required behavior.** Run the parent object's cleanup method when destroying the child object.

**Observed, AI approach.** Check whether the parent method exists, then wrap the call in a catch that logs the exception. The reviewer reports repeated submissions with this pattern.

```js
destroy() {
    try {
        if (typeof super.destroy === 'function') super.destroy();
    } catch (e) { console.warn(`${e.message}`); }
}
```

**Observed, human implementation.** Use the known parent contract:

```js
destroy() {
    super.destroy();
}
```

**Other forms.**

```ts
if (typeof this.render === "function") this.render();
const name = user?.name ?? "";   // the type requires user and user.name
```

```python
if hasattr(self, "close"):
    self.close()
```

**Why the human code is better.** It removes a check for an impossible missing-method case. It also avoids turning an unexpected cleanup failure into an ordinary warning.

**Inferred lesson.** A verified contract can remove branches introduced by uncertainty. Check guarantees at the responsible boundary, then let internal code use them.

**Applies when.** The parent class or framework guarantees the method on every supported version.

**Limits.** The versions differ when cleanup throws: the shorter version exposes the failure. This case does not justify removing recovery from fallible operations.

**Reduce fit.** The existence check is `remove` when the contract holds. Removing the catch changes behavior when cleanup throws.
The reduce skill keeps the catch. The swallowed failure is a suspected defect, and no source requires the warning. Its removal is a contingent reduction for the user's decision, with the consumer search recorded.

[Original report and both implementations](https://blogs.gnome.org/jrahmatzadeh/2025/12/06/ai-and-gnome-shell-extensions/).
