# Test whether each standing instruction changes behavior

**Source:** Matt Pocock, X and his public skill repository. **Evidence:** inspectable guidance; no controlled code-quality result.

**Look for.** Agent instructions or skills that repeat model defaults or other instructions.

**Observed.** Pocock describes skills with generic instructions that repeat model defaults or duplicate other instructions.
He proposes removing one candidate instruction, rerunning a representative task, and comparing the result.

**Inferred practice.** Keep instructions that change a relevant decision. Consolidate repeated rules.
His repository makes the pruning test relative to the model. Keep project knowledge that the environment cannot supply directly.

**Applies when.** Judge the intended behavior and check unrelated tasks.

**Limits.** Replies dispute his claims about model defaults. One unchanged output proves little; instruction removal needs repeated task evidence.

**Reduce fit.** When the target is agent instructions, the behavior is the agent's decisions. Prove a removal with [Compare instructions with a controlled baseline](compare-instructions-with-a-controlled-baseline.md)'s controlled comparison.

[Original X post](https://x.com/mattpocockuk/status/2069784839474032896). [Indexed copy and replies](https://remaja.twstalker.com/mattpocockuk/status/2069784839474032896). [Pinned guidance, especially “Pruning”](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/productivity/writing-for-agents/SKILL.md).
