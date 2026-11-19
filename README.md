# Reduce

Reduce is an agent skill that finds what a code change, codebase, or implementation plan can remove, reuse, or simplify. It keeps the required behavior.

The package has two skills:

- `reduce` runs the review in gated steps with its driver, `skills/reduce/scripts/reduce-step`. After a run, `skills/reduce/scripts/reduce-retro` collects the driver log, the records, and the transcripts of the parent and its subagents for a retrospective.
- `reduce-setup` asks which models the reduce subagents use, then writes `~/.config/reduce/config.json`.

## Install

```sh
npx skills add yohannesakd/reduce -g -y
```

The command installs both skills in `~/.agents/skills`, and links them for each detected agent, such as Claude Code. It needs Node.js, Python 3, and Git.
To install for one agent only, add `--agent claude-code` or `--agent codex`.

Then ask your agent to run `reduce-setup`. Without a configuration, every reduce subagent uses the parent agent's model.

## Test

```sh
python3 -m unittest discover tests
```

## Licenses

The design references in `skills/reduce/design` come from pstack and `mattpocock/skills`. Their MIT notices are in [skills/reduce/design/LICENSES.md](skills/reduce/design/LICENSES.md).

The refactoring check and the language checks adapt the PufferLib refactoring guide and the public style guides and documentation that [skills/reduce/guides/rule-sources.md](skills/reduce/guides/rule-sources.md) lists, with their licenses.
