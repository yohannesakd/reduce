# Fixed behavior and the ladder

The steps, the packets, and the checks cite these rules: the class of each result, the decisions that the user owns, and the rungs.

## Fixed behavior

Preserve required and incidental results, structural goals, and representative resource use in parity reductions.
A result is `required` when a contract or a consumer outside the target needs it, or a `core` or `supporting` capability needs it. A consumer needs a result only when it uses it to show, send, store, or decide something.
A result is `incidental` when no consumer needs it, or it serves only a `questioned` capability, and authorized searches find no other need. Tests and documents that the target itself adds describe a result; alone, they do not make it `required`.
The map step records each result and its consumers, without a class. The design step lists the capabilities and their needs. The reviewer of a feature classes each result from these two records.
A result is `unknown` when its consumers cannot be established.
The design document decides a `questioned` capability: an answer to keep it makes it `supporting`. An answer to remove it, or a design finding with the decision `autonomous`, makes its results `incidental`, and their removal is decided.
Leave unknown consumers unresolved. Passing tests establish only covered behavior.
A replacement that runs in another place needs a run there when it reads the user, directory, variables, PATH, or permissions.
Intent reductions change behavior on purpose. Report them separately, with the behavior they change and the owner who decides.
A contingent reduction removes an `incidental` result, or depends on an owner's answer. It is an intent reduction.
Decide small parity wins yourself. Ask the design questions only in attended mode, in the design step. Escalate other intent reductions and critical areas to the user as questions at the end of the review; do not stop the run for them.
When implementation is requested, apply `autonomous` findings. Apply `user` findings only after the user decides.

## The ladder

Apply these rungs in order to parts, features, and the whole target:

| Rung | Decision |
|---|---|
| `remove` | No preserved result or demonstrated structural benefit needs it |
| `prevent` | A lower-level fix removes the need while preserving other users |
| `reuse` | Existing code, framework, or dependency owns the work |
| `simplify` | Restructure, with justified additions when useful |
| `keep` | Supported alternatives are worse |
| `unresolved` | Name the missing evidence and deciding check |
