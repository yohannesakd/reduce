import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1] / "skills/reduce"
FINDING = "Traced the entry and recorded the result."
EVERY_FEATURE = ["every-feature/" + name for name in (
    "fresh-design", "ladder", "behavior-nothing-needs", "refactoring")]
LANGUAGE = "languages/python"  # the language check of the fixture's app.py
ALWAYS = ("every-feature", "unrelated-changes", "plans", "languages")
TOPICS = [topic for topic in re.findall(r"^### `([^`]+)`", (SKILL / "checks/README.md").read_text(), re.M) if topic not in ALWAYS]
CHECKS_OF = {topic: re.findall(rf"\]\({topic}/([^)]+)\.md\)", (SKILL / "checks/README.md").read_text()) for topic in TOPICS}
RELEASED = re.compile(r"^=== Step 4-check for (F\d+) ", re.M)
PLANNED = re.compile(r"^### Check `(\S+)`|^  - `(\S+)` \(\S*/checks/\S+\.md\): ", re.M)  # a check in full, or its name, file, and pattern


def fill(path, sections, evidence="app.py:1"):
    text = path.read_text()
    text = re.sub(r"status: \nevidence:\n- \nfinding: ",
                  f"status: applied\nevidence:\n- {evidence}\nfinding: {FINDING}", text)
    for name, rows in sections.items():
        text = text.replace(f"## {name}\n", f"## {name}\n" + "".join(f"- {row}\n" for row in rows), 1)
    path.write_text(text)


def git(target, *args):
    subprocess.run(["git", "-C", str(target), "-c", "user.name=t", "-c", "user.email=t@example.invalid", *args], check=True)


class ReduceStepTest(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        root = Path(folder.name)
        self.script = SKILL / "scripts/reduce-step"
        self.config = root / "config/reduce/config.json"  # the driver keeps its configuration and its runs outside the skill
        self.runs = root / "state/reduce/runs"
        self.env = {**os.environ, "XDG_CONFIG_HOME": str(root / "config"), "XDG_STATE_HOME": str(root / "state")}
        self.target = root / "target"
        self.target.mkdir()
        (self.target / "app.py").write_text("def run():\n    return 1\n")
        git(self.target, "init", "-q")
        git(self.target, "add", ".")
        git(self.target, "commit", "-qm", "base")
        self.records = root / "records"
        self.slugs = {"F1": "F1-run", "F2": "F2-other"}

    def record(self, step, feature=None):
        if feature is None:
            return self.records / ("design.md" if step == "3-design" else f"{step}.md")
        return self.records / step / f"{self.slugs[feature]}.md"

    def packet(self, feature):
        return self.record("4-check", feature).with_suffix(".packet.md").read_text()

    def checks(self, feature):
        return self.record("4-check", feature).with_suffix(".checks.md").read_text()

    def planned(self, feature):
        return [full or listed for full, listed in PLANNED.findall(self.checks(feature))]

    def reply(self, feature, results=None, findings=(), by_topic=False, leads=()):
        """Fill a feature's reply: one `absent` line for the open review and for each planned check, unless `results` gives its finding IDs.
        With `by_topic`, each topic has one line in place of its checks."""
        results = results or {}
        names = ["open-review", *self.planned(feature)]
        if by_topic:
            names = [name for name in names if name.partition("/")[0] in ALWAYS or "/" not in name] + TOPICS
        lines = [f"{check} | {results.get(check, 'absent')} | app.py:1-2 | read the whole feature for this pattern" for check in names]
        record = self.record("4-check", feature)
        record.write_text("".join(line for line in record.read_text().splitlines(True) if not line.startswith("- ")))
        fill(record, {"Checks": lines, "Findings": list(findings) or ["none | no check found a reduction"], "Leads": list(leads)})

    def run_step(self, *args, ok=True):
        result = subprocess.run([sys.executable, str(self.script), *args, "--records", str(self.records)],
                                capture_output=True, text=True, env=self.env)
        if ok:
            self.assertEqual(result.returncode, 0, result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout)
        return result

    def start(self, playbook="codebase"):
        return self.run_step("start", "--playbook", playbook, "--target", str(self.target))

    def submit_scope(self, tool_results=()):
        self.start()
        fill(self.record("1-scope"), {"Features": ["F1 | Run | app.py | app.py:1", "F2 | Other | app.py | app.py:2"],
                                      "Sources": ["S1 | user | the request | \"reduce app.py\" | app.py:1"],
                                      "Tool results": list(tool_results)})
        return self.run_step("submit")

    def submit_design(self, findings=(), directions=(), decisions=()):
        self.run_step("next")  # a submit by item does not release the next step
        design = self.record("3-design")
        fill(design, {"Capabilities": ["C1 | core | run returns a value | F1; F2 | app.py:1"], "Findings": list(findings),
                      "Directions": list(directions), "Decisions": list(decisions)})
        design.write_text(design.read_text().replace("## Purpose\n", "## Purpose\nrun gives callers a value (S1).\n")
                          .replace("## Parent review\n", "## Parent review\nRead app.py. Confirmed each finding.\n"))
        return self.run_step("submit").stdout

    def submit_maps(self):
        self.run_step("release")
        for feature in ("F1", "F2"):
            fill(self.record("2-map", feature), {"Intent": ["gives callers a value"], "Inventory": ["B1 | returns 1; run() returns it | app.py:2"]})
            self.run_step("submit", "--item", f"2-map:{feature}")

    def submit_checks(self, findings=None, leads=None):
        """Submit every released check with `none`, or with the findings given for its feature and check, and the leads of its feature."""
        findings, leads = findings or {}, leads or {}
        while True:
            output = self.run_step("next").stdout
            match = RELEASED.search(output)
            if not match:
                return output
            feature = match[1]
            rows = findings.get(feature, {})
            self.reply(feature, {check: row.split(" | ")[0] for check, row in rows.items()}, rows.values(), by_topic=feature == "F2",
                       leads=leads.get(feature, ()))
            self.run_step("submit")

    def test_releases_one_step_and_rejects_an_unfilled_record(self):
        output = self.start().stdout
        self.assertIn("=== Step 1-scope |", output)
        self.assertNotIn("2-map", output)
        self.assertFalse((self.records / "2-map").exists())
        self.assertIn("`## Features` needs at least one row", self.run_step("submit", ok=False).stderr)

    def test_notes_do_not_block_and_a_changed_target_does(self):
        self.start()
        fill(self.record("1-scope"), {"Features": ["F01 | Run | app.py | `app.py:1-9`, see run()"]}, evidence="missing.py:4")
        output = self.run_step("submit").stdout
        self.assertIn("Accepted 1-scope.", output)
        self.assertIn("`missing.py`", output)
        self.assertIn("past the end of their file: `app.py:1-9`", output)
        self.assertNotIn("`app.py`", output.partition("Notes")[2].partition("===")[0])
        (self.target / "app.py").write_text("def run():\n    return 2\n")
        self.assertIn("target changed", self.run_step("submit", ok=False).stderr)

    def test_features_must_cover_every_file_and_name_files(self):
        (self.target / "lib.py").write_text("VALUE = 1\n")
        git(self.target, "add", "lib.py")
        git(self.target, "commit", "-qm", "lib")
        self.start()
        fill(self.record("1-scope"), {"Features": ["F1 | Run | app.py; missing/** | app.py:1", "F2 | Gone | missing/** | app.py:1"]})
        rejected = self.run_step("submit", ok=False).stderr
        self.assertIn("Feature F2: its paths match no file", rejected)
        self.assertNotIn("Feature F1", rejected)
        self.assertIn("1 file(s) are in no feature and not in `## Excluded`: lib.py", rejected)
        text = self.record("1-scope").read_text().replace("- F2 | Gone | missing/** | app.py:1\n", "").replace("app.py; missing/**", "*.py")
        self.record("1-scope").write_text(text)
        self.run_step("submit")
        fill(self.record("2-map", "F1"), {"Intent": ["gives callers a value"], "Inventory": ["I1 | returns 1 | app.py:2"]})
        self.assertIn("`## Inventory` has IDs without the prefix B: I1.", self.run_step("submit", ok=False).stderr)
        self.record("2-map", "F1").write_text(self.record("2-map", "F1").read_text().replace("- I1 |", "- B1 |"))
        self.assertIn("=== Step 3-design | unattended mode |", self.run_step("submit").stdout)
        self.assertIn("Packet: ", self.submit_design())
        self.assertEqual(self.planned("F1")[:len(EVERY_FEATURE) + 2], [*EVERY_FEATURE, LANGUAGE, f"{TOPICS[0]}/{CHECKS_OF[TOPICS[0]][0]}"])

    def test_code_playbook_covers_changed_untracked_and_deleted_files(self):
        (self.target / "old.py").write_text("OLD = 1\n")
        git(self.target, "add", "old.py")
        git(self.target, "commit", "-qm", "old")
        base = subprocess.run(["git", "-C", str(self.target), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
        git(self.target, "rm", "-q", "old.py")
        (self.target / "app.py").write_text("def run():\n    return 2\n")
        git(self.target, "commit", "-qam", "change")
        (self.target / "new.py").write_text("NEW = 1\n")
        self.start("code")
        fill(self.record("1-scope"), {"Revisions": [f"`{base}` (merge base) | HEAD"], "Features": ["F1 | Run | app.py | app.py:1"]})
        rejected = self.run_step("submit", ok=False).stderr
        self.assertIn("2 file(s) are in no feature and not in `## Excluded`: new.py, old.py", rejected)
        text = self.record("1-scope").read_text().replace("| app.py | app.py:1", "| app.py; new.py; old.py | app.py:1")
        self.record("1-scope").write_text(text)
        self.assertIn("=== Step 2-map for F1 Run |", self.run_step("submit").stdout)
        fill(self.record("2-map", "F1"), {"Intent": ["gives callers a value"], "Inventory": ["B1 | returns 2 | app.py:2",
                                                        "B2 | old constant; consumers unknown | old.py:1",
                                                        "B3 | new constant; no consumer found | new.py:1"]})
        self.assertNotIn("Notes", self.run_step("submit").stdout)
        self.submit_design()
        self.assertEqual(self.planned("F1")[:len(EVERY_FEATURE) + 1], EVERY_FEATURE + ["unrelated-changes/hunk-that-does-not-serve-the-problem"])
        self.assertIn("### Check `unrelated-changes/hunk-that-does-not-serve-the-problem`", self.checks("F1"))
        packet = self.packet("F1")
        self.assertIn("-    return 1\n+    return 2", packet)
        self.assertIn("Untracked new files, not in the diff: `new.py`", packet)
        self.assertNotIn("reduce-step", packet)
        self.assertNotIn(f"{SKILL}/SKILL.md", packet)
        self.assertIn(f"{SKILL}/guides/fixed-behavior.md#the-ladder", packet)

    def test_packets_hold_only_their_own_work_and_the_reply_needs_a_line_for_each_check(self):
        output = self.submit_scope(tool_results=["L1 | F1 (duplicate) | duplicate return | app.py:2", "L2 | F9 | stray | app.py:1"])
        self.assertIn("These tool results name no feature, so no check packet includes them: L2", output.stdout)
        mapped = self.record("2-map", "F1").with_suffix(".packet.md").read_text()
        self.assertIn(f"Write your record in: {self.record('2-map', 'F1')}", mapped)
        self.assertIn(f"Scope record, for the sources: {self.record('1-scope')}", mapped)
        self.assertNotIn("## Leads", mapped)  # only the design and check records take leads
        self.assertIn("<id, such as B1> | <result and consumers> | <evidence: path:line>", mapped)
        self.assertIn("## Intent", mapped)
        self.assertIn("<id, such as Q1> | <question> | <what you found: path:line> | <answer, or unanswered>", mapped)
        for judged in ("## Topics", "duplicate return", "required", "incidental", "disagree"):  # the map step describes, and judges nothing
            self.assertNotIn(judged, mapped)
        self.submit_maps()
        design = self.run_step("next").stdout
        self.assertIn("Give the packet to a subagent.", design)
        self.assertIn("Subagent model: standard.", design)
        packet = (self.records / "design.packet.md").read_text()
        self.assertIn("This run is in unattended mode.", packet)
        self.assertIn(f"- Scope record: {self.record('1-scope')}", packet)
        self.assertIn("Record it in `## Leads` of your record, numbered from N1.", packet)
        self.assertIn(f"- Map record of F2: {self.record('2-map', 'F2')}", packet)
        self.assertIn("## Purpose\n<!-- One paragraph", packet)
        self.submit_design(["X1 | reuse | parity | autonomous | F1:B1; F2:B1 | app.py:2 | one owner for the return",
                            "X2 | remove | intent | user | F1:B1 | app.py:2 | nothing reads the value"],
                           ["F1 | F2 owns the return; use it | X1"], ["X2 | Does anything read the value? | remove it | unanswered"])
        options = ["options-flags-and-settings/" + name for name in CHECKS_OF["options-flags-and-settings"]]
        self.assertEqual(self.planned("F1")[:len(EVERY_FEATURE) + 1], [*EVERY_FEATURE, "every-feature/tool-results"])
        self.assertTrue(set(options) < set(self.planned("F1")))
        self.run_step("next", "--item", "4-check:F2")
        self.assertEqual(self.planned("F2"), [check for check in self.planned("F1") if check != "every-feature/tool-results"])
        packet = self.packet("F1")
        self.assertIn("#### A fresh design needs less", self.checks("F1"))
        self.assertIn(f"  - `{options[0]}` ({SKILL}/checks/{options[0]}.md): ", self.checks("F1"))
        self.assertNotIn(f"### Check `{options[0]}`", self.checks("F1"))
        self.assertNotIn("A fresh design needs less", packet)
        self.assertIn(f"Checks file: {self.record('4-check', 'F1').with_suffix('.checks.md')}.\n", packet)
        self.assertIn("- L1 | F1 (duplicate) | duplicate return | app.py:2", packet)
        self.assertIn("Number your findings from X101.", packet)
        self.assertIn("Record it in `## Leads` of your record, numbered from N101.", packet)
        self.assertNotIn("## Revisions", packet)  # only a plan run has reference revisions
        self.assertIn("## Other features\n\nOther reviewers check these features. Search them for an owner of the same work.\n\n- F2 | Other | app.py\n", packet)
        self.assertIn("## Design document", packet)
        self.assertIn("run gives callers a value (S1).", packet)
        self.assertIn("- X2 | Does anything read the value? | remove it | unanswered", packet)
        self.assertIn("- F1 | F2 owns the return; use it | X1", packet)
        self.reply("F1", {"every-feature/ladder": "X101"}, ["X101 | remove | intent | whoever | B7 | app.py:2 | drop the return",
                                                              "A note: the map record has no B7."])
        record = self.record("4-check", "F1")
        # Another line's text names the check. That is not a line for the check.
        record.write_text(record.read_text().replace(f"- {options[3]} |", f"- notes/elsewhere | absent | app.py:1 | see {options[3]} |"))
        record.write_text(record.read_text().replace("- open-review | absent |", "- every-feature/fresh-design | absent | app.py:1 | after the open-review |"))
        rejected = self.run_step("submit", ok=False).stderr
        self.assertIn(f"`## Checks` has no line for `{options[3]}`", rejected)
        self.assertIn("`## Checks` has no line for `open-review`", rejected)
        self.assertIn("`## Findings`: the decision must be autonomous or user, not whoever.", rejected)
        self.assertEqual(rejected.count("\n- "), 3)
        record.write_text(record.read_text().replace("- notes/elsewhere |", f"- `{options[3].rpartition('/')[2]}` |")
                          .replace("| whoever |", "| `autonomous` (X1) |").replace("## Checks\n", "## Checks\n- open-review | absent | app.py:1 | asked what I would remove\n"))
        self.run_step("submit")

    def test_each_feature_gets_the_language_checks_of_its_files_and_the_design_packet_lists_them(self):
        files = {"web/form.ts": "export const a = 1\n", "web/view.tsx": 'import { Effect } from "effect"\n',
                 "svc/main.go": "package main\n", "lib/pool.c": "int a;\n", "bin/tool": "#!/usr/bin/env python3\n", "notes.md": "x\n"}
        for path, text in files.items():
            (self.target / path).parent.mkdir(exist_ok=True)
            (self.target / path).write_text(text)
        git(self.target, "add", ".")
        git(self.target, "commit", "-qm", "languages")
        self.start()
        fill(self.record("1-scope"), {"Features": ["F1 | Run | app.py; web/*; notes.md | app.py:1", "F2 | Other | svc/main.go; lib/pool.c; bin/tool | svc/main.go:1"],
                                      "Sources": ["S1 | user | the request | \"reduce app.py\" | app.py:1"]})
        self.run_step("submit")
        self.submit_maps()
        self.run_step("next")
        self.assertIn(f"- `languages/go`: {SKILL}/checks/languages/go.md", (self.records / "design.packet.md").read_text())
        self.submit_design()
        expected = {"F1": ["languages/typescript", "languages/react", "languages/effect", "languages/python"],
                    "F2": ["languages/go", "languages/python"]}
        for feature, languages in expected.items():
            self.run_step("next", "--item", f"4-check:{feature}")
            self.assertEqual(sorted(check for check in self.planned(feature) if check.startswith("languages/")), sorted(languages))
            for language in languages:
                self.assertIn(f"### Check `{language}`", self.checks(feature))
        self.reply("F2")
        record = self.record("4-check", "F2")
        record.write_text(record.read_text().replace("- languages/go | absent |", "- notes/go | absent |"))
        self.assertIn("`## Checks` has no line for `languages/go`", self.run_step("submit", "--item", "4-check:F2", ok=False).stderr)

    def test_release_lists_items_for_parallel_agents_and_submits_them_by_key(self):
        self.submit_scope()
        maps = json.loads(self.run_step("release").stdout)
        self.assertEqual(maps["model"], "standard")
        self.assertEqual(maps["subagents"], "feature")
        self.assertEqual([(group["feature"], group["record"], group["packet"]) for group in maps["features"]],
                         [("F1", "2-map/F1-run.md", "2-map/F1-run.packet.md"), ("F2", "2-map/F2-other.md", "2-map/F2-other.packet.md")])
        self.assertIn("is not in the current step, 2-map", self.run_step("submit", "--item", "4-check:F1", ok=False).stderr)
        for feature in ("F2", "F1"):
            fill(self.record("2-map", feature), {"Intent": ["gives callers a value"], "Inventory": ["B1 | returns 1 | app.py:2"]})
        self.assertIn("1 items of step 2-map are not submitted", self.run_step("submit", "--item", "2-map:F2").stdout)
        self.assertIn("Step 2-map is complete", self.run_step("submit", "--item", "2-map:F1").stdout)
        design = json.loads(self.run_step("release").stdout)
        self.assertEqual((design["step"], design["record"], design["packet"], design["features"]),
                         ("3-design", "design.md", "design.packet.md", []))
        self.submit_design()
        released = json.loads(self.run_step("release").stdout)["features"]
        self.assertEqual([(group["feature"], group["packet"], group["first_finding_id"]) for group in released],
                         [("F1", "4-check/F1-run.packet.md", "X101"), ("F2", "4-check/F2-other.packet.md", "X201")])
        self.reply("F2", {"every-feature/ladder": "X201"}, ["X201 | remove | parity | autonomous | B1 | app.py:2 | drop it"])
        self.run_step("submit", "--item", "4-check:F2")
        self.assertIn("is already submitted", self.run_step("submit", "--item", "4-check:F2", ok=False).stderr)
        self.reply("F1", {"every-feature/ladder": "X201"}, ["X201 | remove | parity | autonomous | B1 | app.py:2 | same | with a pipe"],
                   leads=["N201 | F2 | a second copy | app.py:2"])
        rejected = self.run_step("submit", "--item", "4-check:F1", ok=False).stderr  # the report keys findings and leads on their IDs
        self.assertIn("`## Findings` has IDs outside the numbers of this record: X201. Number them from X101.", rejected)
        self.assertIn("`## Leads` has IDs outside the numbers of this record: N201. Number them from N101.", rejected)
        self.reply("F1", {"every-feature/ladder": "X101"}, ["X101 | remove | parity | autonomous | B1 | app.py:2 | same | with a pipe"])
        draft = json.loads(self.run_step("findings", "--item", "4-check:F1").stdout)
        self.assertEqual([(row["id"], row["item"], row["finding"]) for row in draft], [("X101", "F1", "same | with a pipe")])
        self.run_step("submit", "--item", "4-check:F1")
        self.assertEqual([(row["id"], row["item"]) for row in json.loads(self.run_step("findings").stdout)], [("X101", "F1"), ("X201", "F2")])

    def test_complete_run_rewrites_the_tables_and_needs_a_report(self):
        self.submit_scope()
        self.submit_maps()
        self.run_step("next")
        fill(self.record("3-design"), {"Findings": ["X3 | simplify | parity | user | F1:B1; F2:B1 | app.py:1 | one module"]})
        rejected = self.run_step("submit", ok=False).stderr
        self.assertIn("`## Purpose` is empty", rejected)
        self.assertIn("`## Capabilities` needs at least one row", rejected)
        self.assertIn("`## Parent review` is empty", rejected)
        self.submit_design()
        self.assertIn("- X3 | simplify | parity | user", self.packet("F1"))
        output = self.submit_checks({"F1": {"every-feature/behavior-nothing-needs":
                                            "X101 | remove | intent | user | B1 | app.py:2 | remove the return"},
                                     "F2": {"every-feature/fresh-design":
                                            "X201 | simplify | parity | autonomous | B1 | app.py:1 | inline run"}},
                                    {"F2": ["N201 | F1 | the mapper saw a second copy | app.py:2"]})
        self.assertIn("=== Step 5-report |", output)
        review = self.records / "review.md"
        table = review.read_text()
        self.assertIn("| F1 Run | every-feature/behavior-nothing-needs | X101 |", table)
        self.assertIn("| F2 Other | every-feature/ladder | none |", table)
        self.assertIn("| F1 Run | open-review | none |", table)
        self.assertIn(f"| F2 Other | {TOPICS[0]}/{CHECKS_OF[TOPICS[0]][0]} | none |", table)  # from the line of its topic
        self.assertNotIn("missing", table)
        self.assertIn("| X101 | F1 | remove | intent | user | app.py:2 | remove the return |", table)
        self.assertIn("| X3 | design | simplify | parity | user | app.py:1 | one module |", table)
        fill(self.record("5-report"), {"Whole-target findings": ["W1 | prevent | parity | autonomous | X101 | app.py:1 | share one owner"]})
        rejected = self.run_step("submit", ok=False).stderr
        self.assertIn("review.md has no report", rejected)
        self.assertIn("`## Leads` has no row for these leads: N201.", rejected)
        self.assertNotIn("Dispositions", rejected)  # only a plan run writes reduced copies
        fill(self.record("5-report"), {"Leads": ["N201 | W1 | the shared owner removes it"]})
        edited = table.replace("| X101 | F1 | remove |", "| X101 | F1 | keep |")
        review.write_text(edited + "\nComplete. The review found two findings in two features. X101 removes the return, and X201 "
                          "inlines run. W1 shares one owner.\n\n## Decisions for you\n\nX101: remove the return?\n")
        self.assertIn("=== Step 6-close |", self.run_step("submit").stdout)
        final = review.read_text()
        self.assertIn("| X101 | F1 | remove |", final)
        self.assertNotIn("| X101 | F1 | keep |", final)
        self.assertIn("X101: remove the return?", final)
        fill(self.record("6-close"), {})
        self.run_step("status", "--final", ok=False)
        (self.target / "app.py").write_text("def run():\n    return 1\n\n")  # the close step applies findings
        self.assertIn("All steps are complete", self.run_step("submit").stdout)
        self.run_step("status", "--final")
        log = [json.loads(line) for line in (self.records / ".reduce-step/log.jsonl").read_text().splitlines()]
        self.assertEqual(len([e for e in log if e["event"] == "release"]), len([e for e in log if e["event"] == "submit"]))

    def test_plan_run_names_its_revisions_and_places_each_finding(self):
        self.run_step("start", "--playbook", "plan", "--target", str(self.target))
        scope = self.record("1-scope")
        fill(scope, {"Revisions": ["reference | app | 0000000 | an old build to port from"],
                     "Features": ["F1 | Run | app.py", "F2 | Other | app.py"]})
        self.assertIn("`## Revisions` needs a baseline row", self.run_step("submit", ok=False).stderr)
        scope.write_text(scope.read_text().replace("- reference |", "- baseline | app | HEAD | the source that the plan changes\n- reference |"))
        self.run_step("submit")
        self.run_step("release")
        for feature in ("F1", "F2"):
            fill(self.record("2-map", feature), {"Requirements": ["R1 | accepted | run returns 1 | app.py:2"]})
            self.run_step("submit", "--item", f"2-map:{feature}")
        self.submit_design(["X1 | reuse | parity | autonomous | F1:R1; F2:R1 | app.py:2 | one owner for the return"])
        packet = self.packet("F1")
        self.assertIn("Code that exists only at a reference revision is not in the baseline: using it is a port, not reuse.", packet)
        self.assertIn("- reference | app | 0000000 | an old build to port from", packet)
        self.submit_checks({"F1": {"every-feature/ladder": "X101 | remove | parity | autonomous | R1 | app.py:2 | drop the return"},
                            "F2": {"every-feature/ladder": "X201 | keep | parity | autonomous | R1 | app.py:2 | a caller reads it"}})
        report = self.record("5-report")
        fill(report, {"Whole-target findings": ["none | the features share no owner"]})
        review = self.records / "review.md"
        review.write_text(review.read_text() + "\nComplete. The review found two findings that change the plan: X1 gives the return "
                          "one owner, and X101 drops it. The reduced plan applies both.\n")
        rejected = self.run_step("submit", ok=False).stderr
        self.assertIn("`## Dispositions` has no row for these findings: X1, X101.", rejected)  # X201 keeps its unit
        fill(report, {"Dispositions": ["X1 | applied | reduced-plan.md, Phase 1", "X101 | applied | Phase 2 of `reduced-plan.md`."]})
        self.assertIn("these applied findings name no reduced copy that exists: X1, X101.", self.run_step("submit", ok=False).stderr)
        (self.records / "reduced-plan.md").write_text("Status: proposal, not accepted\n")
        self.assertIn("=== Step 6-close |", self.run_step("submit").stdout)

    def test_attended_run_in_the_runs_folder_uses_the_configured_models(self):
        result = subprocess.run([sys.executable, str(self.script), "start", "--playbook", "codebase", "--mode", "attended",
                                 "--target", str(self.target)], capture_output=True, text=True, env=self.env)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.records = Path(re.search(r"^Records directory: (.+)\. Pass it", result.stdout, re.M)[1])
        self.assertEqual(self.records.parent, self.runs)
        self.assertRegex(self.records.name, r"^target-[a-z0-9-]+-\d{8}-\d{4}$")
        self.assertIn(f"No configuration at {self.config}: every subagent uses your own model.", result.stdout)
        self.assertFalse(self.config.exists())  # only reduce-setup writes the configuration
        self.assertEqual([path.name for path in SKILL.iterdir() if path.name in ("config.json", "runs")], [])
        config = json.loads((SKILL / "config.example.json").read_text())
        self.config.parent.mkdir(parents=True)
        self.config.write_text(json.dumps({**config, "map": "cheap", "checks": "powerful"}))
        fill(self.record("1-scope"), {"Features": ["F1 | Run | app.py | app.py:1", "F2 | Other | app.py | app.py:2"]})
        self.run_step("submit")
        self.assertEqual(json.loads(self.run_step("release").stdout)["model"], "cheap")
        self.submit_maps()
        self.assertEqual(json.loads(self.run_step("release").stdout)["model"], "powerful")
        self.assertIn("This run is in attended mode.", (self.records / "design.packet.md").read_text())
        self.submit_design()
        self.assertEqual(json.loads(self.run_step("release").stdout)["model"], "powerful")
        self.config.write_text(json.dumps({**config, "checks": "large"}))
        self.assertIn("`checks` must be one of cheap, standard, powerful", self.run_step("next", ok=False).stderr)

    def test_config_validates_a_draft_and_prints_each_steps_models(self):
        def shown(*args):
            return subprocess.run([sys.executable, str(self.script), "config", *args], capture_output=True, text=True, env=self.env)
        missing = json.loads(shown().stdout)
        self.assertEqual((missing["exists"], missing["checks"], missing["models"]["t3"]["cheap"]), (False, "cheap", None))
        draft = self.target.parent / "draft.json"
        draft.write_text(json.dumps({"checks": "standard", "map_subagents": "one",
                                     "models": {"codex": {"cheap": ["a", "b"]}, "t3": {"powerful": {"provider": "p", "model": "m"}}}}))
        listed = json.loads(shown("--file", str(draft)).stdout)
        self.assertEqual((listed["checks"], listed["map_subagents"], listed["models"]["codex"]["cheap"]), ("standard", "one", ["a", "b"]))
        for bad, error in (({"check": "cheap"}, "unknown key check"), ({"models": {"pi": {}}}, "`models.pi` is not a harness"),
                           ({"models": {"t3": {"cheap": "m"}}}, "`models.t3.cheap` must be null"),
                           ({"models": {"codex": {"cheap": []}}}, "`models.codex.cheap` must be null"),
                           ({"models": {"codex": {"large": "m"}}}, "`models.codex` must map")):
            draft.write_text(json.dumps(bad))
            result = shown("--file", str(draft))
            self.assertEqual(result.returncode, 1)
            self.assertIn(error, result.stderr)
        self.assertEqual(json.loads(shown().stdout)["exists"], False)  # validating a draft writes nothing

    def test_a_folder_of_the_checkout_is_a_target_and_the_quick_packet_lists_its_diff(self):
        (self.target / "pkg").mkdir()
        (self.target / "pkg/core.py").write_text("CORE = 1\n")
        git(self.target, "add", ".")
        git(self.target, "commit", "-qm", "pkg")
        base = subprocess.run(["git", "-C", str(self.target), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
        (self.target / "pkg/core.py").write_text("CORE = 2\n")
        (self.target / "app.py").write_text("def run():\n    return 2\n")
        git(self.target, "commit", "-qam", "change")
        self.run_step("start", "--playbook", "code", "--mode", "quick", "--target", str(self.target / "pkg"))
        fill(self.record("1-scope"), {"Revisions": [f"{base} | HEAD"], "Features": ["F1 | Core | core.py | core.py:1; app.py:2; 127.0.0.1:80"]})
        output = self.run_step("submit").stdout  # app.py changed outside the folder, and needs no row
        self.assertNotIn("Notes", output)  # a folder target can cite the rest of its checkout, and an address is not a path
        packet = (self.records / "review.packet.md").read_text()
        self.assertIn("Files: `core.py`.", packet)
        self.assertIn(f"Read it with `git -C {self.target / 'pkg'} diff --relative {base} -- <file>`", packet)
        self.assertNotIn("+CORE = 2", packet)

    def test_quick_run_reviews_the_target_in_one_record(self):
        self.assertIn("code and codebase playbooks", self.run_step(
            "start", "--playbook", "plan", "--mode", "quick", "--target", str(self.target), ok=False).stderr)
        self.run_step("start", "--playbook", "codebase", "--mode", "quick", "--target", str(self.target))
        fill(self.record("1-scope"), {"Features": ["F1 | Run | app.py | app.py:1"]})
        output = self.run_step("submit").stdout
        self.assertIn("=== Step 2-quick | quick mode |", output)
        self.assertIn("without subagents", output)
        packet = (self.records / "review.packet.md").read_text()
        self.assertIn("## Feature F1: Run", packet)
        self.assertIn(f"Checks file: {self.records / 'review.checks.md'}. Read it only after your open review.", packet)
        self.assertNotIn("### Check", packet)
        packet = (self.records / "review.checks.md").read_text()
        self.assertIn("### Check `every-feature/ladder`", packet)
        self.assertNotIn("### Check `every-feature/tool-results`", packet)
        self.assertIn("  - `unused-code/unused-export-parameter-or-branch` (", packet)
        self.assertIn("checks/unused-code/unused-export-parameter-or-branch.md): ", packet)
        self.assertIn("## Topics to look over", packet)
        review = self.records / "review.md"
        lines = [f"{check} | absent | app.py:1-2 | read the whole target" for check in [*EVERY_FEATURE, LANGUAGE]]
        fill(review, {"Capabilities": ["C1 | core | run returns a value | B1 | app.py:1"],
                      "Inventory": ["B1 | F1 | required | returns 1; run() returns it | app.py:2"],
                      "Checks": lines + ["unused-code | X1 | app.py:2 | the return has no reader"],
                      "Findings": ["X1 | remove | intent | user | B1; C1 | app.py:2 | remove the return"]})
        errors = self.run_step("submit", ok=False).stderr
        self.assertIn("`## Intent` is empty", errors)
        self.assertIn("no line for `tests`", errors)
        self.assertIn("no line for `open-review`", errors)
        self.assertNotIn("no line for `unused-code", errors)
        self.assertNotIn("no line for `every-feature", errors)
        topics = [line[len("- `"):].partition("`")[0] for line in packet.partition("## Topics to look over")[2].splitlines()
                  if line.startswith("- `")]
        text = review.read_text().replace("## Intent\n", "## Intent\nrun gives callers a value.\n")
        text = text.replace("## From scratch\n", "## From scratch\nOne function.\n").replace("## Report\n", "## Report\nComplete. X1.\n")
        review.write_text(text.replace("## Checks\n", "## Checks\n- open-review | X1 | app.py:2 | asked what the target needs\n" + "".join(
            f"- {topic} | absent | app.py:1 | no pattern appears\n" for topic in topics if topic != "unused-code")))
        self.assertIn("=== Step 6-close |", self.run_step("submit").stdout)
        self.assertEqual([row["id"] for row in json.loads(self.run_step("findings").stdout)], ["X1"])

    def test_retrospective_finds_the_sessions_and_the_subagent_of_each_packet(self):
        home = self.records.parent / "home"
        session = "11111111-2222-3333-4444-555555555555"
        claude = home / ".claudep"
        self.env.update(HOME=str(home), CLAUDE_CONFIG_DIR=str(claude), CLAUDE_CODE_SESSION_ID=session)
        self.env.pop("CODEX_HOME", None)
        self.submit_scope()
        self.run_step("release")
        log = [json.loads(line) for line in (self.records / ".reduce-step/log.jsonl").read_text().splitlines()]
        self.assertEqual({entry["session"]["CLAUDE_CODE_SESSION_ID"] for entry in log}, {session})
        self.assertRegex(log[0]["skill"], r"^[0-9a-f]{16}$")

        def transcript(path, *entries):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("".join(json.dumps({"type": kind, "timestamp": log[-1]["time"], "message": {"content": text}}) + "\n"
                                    for kind, text in entries))
        parent = claude / "projects/-work" / f"{session}.jsonl"
        transcript(parent, ("user", "reduce app.py"), ("assistant", "Started the run."))
        packet = self.record("2-map", "F1").with_suffix(".packet.md")
        transcript(parent.with_suffix("") / "subagents/agent-a1.jsonl",
                   ("user", f"Read {packet}. Follow it, and write your reply in {self.record('2-map', 'F1')}."), ("assistant", "Wrote the map."))
        retro = [sys.executable, str(SKILL / "scripts/reduce-retro")]
        output = subprocess.run([*retro, "collect", "--records", str(self.records)], capture_output=True, text=True, env=self.env)
        self.assertEqual(output.returncode, 0, output.stderr)
        self.assertIn("Subagents matched: 1 of 2 packets.", output.stdout)
        text = (self.records / "retro/packet.md").read_text()
        self.assertIn(f"claude:{session}: {parent}", text)
        self.assertIn("| user | reduce app.py", text)
        self.assertIn(f"- brief: Read {packet}. Follow it, and write your reply in", text)
        self.assertIn("- last reply: Wrote the map.", text)
        self.assertIn(f"- no transcript for {packet.relative_to(self.records).as_posix().replace('F1-run', 'F2-other')}", text)

        reply = self.records / "retro/retro.md"
        recorded = [*retro, "record", "--records", str(self.records)]
        self.assertIn("## Observations has no rows", subprocess.run(recorded, capture_output=True, text=True, env=self.env).stderr)
        reply.write_text(reply.read_text().replace("## Observations\n", "## Observations\n- O1 | 2-map | slow | driver | new | log | late\n"))
        self.assertIn("kind 'slow'", subprocess.run(recorded, capture_output=True, text=True, env=self.env).stderr)
        reply.write_text(reply.read_text().replace("| slow |", "| friction |").replace("## Proposals\n", "## Proposals\n- none | one run\n"))
        for _ in range(2):  # a second record of the same run replaces its rows
            self.assertEqual(subprocess.run(recorded, capture_output=True, text=True, env=self.env).returncode, 0)
        ledger_path = self.records.parent / "state/reduce/ledger.jsonl"
        self.assertEqual([json.loads(line)["id"] for line in ledger_path.read_text().splitlines()], ["O1"])

        earlier = {"run": "earlier", "id": "O3", "step": "2-map:F3", "kind": "error", "cause": "driver", "observation": "late"}
        ledger_path.write_text(json.dumps(earlier) + "\n" + ledger_path.read_text())
        output = subprocess.run(recorded, capture_output=True, text=True, env=self.env).stdout
        self.assertIn("- 2 runs | 2-map | driver", output)  # the same step and cause in two runs, whatever the feature
        reply.write_text(reply.read_text().replace("- O1 | 2-map |", "- O1 | the map step |"))
        self.assertIn("is not a step name", subprocess.run(recorded, capture_output=True, text=True, env=self.env).stderr)


if __name__ == "__main__":
    unittest.main()
