# Retrospective

Find what one reduce run teaches about the skill, and propose changes to the skill. Do not change the skill.

The packet holds the evidence: the driver's timeline, the names of the records, the parent's part of its session transcript, a summary of each subagent, and the observations of earlier runs.
Read the records and the transcripts that the packet names when an observation needs them. Read the current skill files before you propose a change to them.

1. **R.1** In `## Outcome`, state what the user asked for, what the run delivered, and what the user did with the result. Use the parent transcript.
2. **R.2** Find where the run lost time or quality. A run that did not finish can still teach: find where it stopped and why. Look for these signals:
   - a rejected record, or a record submitted again
   - a long gap in the timeline, compared with the other steps
   - a step or a check that the parent or a subagent did not do as written
   - a subagent that failed, retried, used the wrong model, or wrote outside its record
   - a finding that the parent review corrected or removed, or that the user rejected
   - a question to the user that the records could answer
   - a result that the user corrected, or did not use
3. **R.3** Record the things that worked, as `worked` rows, when a later change could break them. Every row has an `O` ID.
4. **R.4** Give each observation one cause:
   - `guidance-inadequate`: the skill's words were missing, unclear, or wrong. Name the file.
   - `guidance-not-followed`: the words were clear, and the agent did not do them.
   - `driver`: the step driver allowed, rejected, or printed the wrong thing.
   - `model`: the configured model class could not do the step.
   - `harness`: the tool that ran the agents failed.
   - `target`: the target itself caused it. The skill needs no change.
   - `none`: a `worked` row.
5. **R.5** In the `recurs` column, write the IDs of the earlier observations with the same step and cause, such as `3f2a1c9e0b4d7a61:O2`. Write `new` when there is none.
6. **R.6** Propose a change only for a cause in the skill or the driver, and only when the observation recurs or its cause is structural. Prefer a driver check over another instruction. For `guidance-not-followed`, first ask whether the driver can make the step impossible to skip.
7. **R.7** Write each proposal in general words. The skill's repository is public: do not put the target's names, paths, code, or the user's words in a proposal.
8. **R.8** In `## Not visible`, record the evidence that the packet did not hold, such as a subagent session on another host.

In the step column, write one step name, such as `1-scope` or `4-check:F2`, or `run` for the whole run. The ledger counts recurrence by step and cause.
Every row cites its evidence: a timeline line, a record, or a transcript entry with its time.
The user decides each proposal. Apply an approved proposal in the skill's maintained source, not in an installed copy.
