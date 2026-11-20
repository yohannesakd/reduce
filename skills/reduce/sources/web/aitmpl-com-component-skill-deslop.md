# Deslop — Skills for Claude Code | Claude Code Templates

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Date: 2026-11-19
- Original location: https://www.aitmpl.com/component/skill/deslop
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
[View on GitHub](https://github.com/davila7/claude-code-templates/blob/main/cli-tool/components/skills/sentry/deslop)

## Remove AI Code Slop

Check the diff against main and remove all AI-generated slop introduced in this branch.

### What to Remove

- Extra comments that a human wouldn't add or are inconsistent with the rest of the file
- Extra defensive checks or try/catch blocks that are abnormal for that area of the codebase (especially if called by trusted/validated codepaths)
- Casts to `any` to get around type issues
- Inline imports in Python (move to top of file with other imports)
- Any other style that is inconsistent with the file

### Process

1. Get the diff against main: `git diff main...HEAD`
2. Review each changed file for slop patterns
3. Remove identified slop while preserving legitimate changes
4. Report a 1-3 sentence summary of what was changed

### Scanned by NVIDIA SkillSpector

Automated static analysis (no LLM) · v2.12.0 · 2026-11-19

0 observations

SkillSpector looks for patterns such as shell commands, credential access, network calls or unpinned dependencies. An observation is something worth reading in the files before you install, not a confirmed vulnerability. Components that run code locally, like hooks, MCP servers and security tooling, naturally show more of them. Open one to see the lines it points at.

No observations.

Learn more about [NVIDIA SkillSpector](https://github.com/NVIDIA/skillspector) or [how components are reviewed](/security).

### Agent compatibility

Checked by NVIDIA SkillEvaluator Harness Check · v1.0.1 · 2026-11-18

How each agent reads this skill once it is installed, from the agents' documented loading rules. No agent was run. A note means the agent loads the skill but changes part of its text, or drops it.

- Claude Codeloads
- Codexloads
- Copilot CLIloads
- OpenCodeloads
- Hermesloads
- OpenClawloads

Every agent loads this skill as written. No notes.

Learn more about [NVIDIA SkillEvaluator](https://github.com/NVIDIA/SkillEvaluator).
