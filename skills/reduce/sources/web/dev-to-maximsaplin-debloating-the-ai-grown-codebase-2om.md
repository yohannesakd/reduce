# Debloating The AI-Grown Codebase

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: Maxim Saplin
- Date: 2026-06-01
- Original location: https://dev.to/maximsaplin/debloating-the-ai-grown-codebase-2om
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
The use of AI Agents creates a distinctive smell... One can tell the GH Repo owner was high on Claude just by looking at verbose and hard to follow README.md lacking clarity and brevity. My weekend experiment cutting 40% of lines of code (without compromising the functionality) from an AI grown codebase is an eye opening experience into what AI bloat might look like. The learnings have been distilled into an [agent skill](https://github.com/maxim-saplin/goal-sloc).


Last autumn I started building Flutter [app](https://github.com/maxim-saplin/nothingness) entirely with AI - a media player. I would not say I vibe-coded it - I pressed agents to keep up docs, pushed automated tests coverage, invested in feedback loops (e.g. created ergonomic CLI for Flutter app driving).The thing could be run and poked from the outside. There was structure around the agents.

But I also did not read the code very much - I was too lazy. Or, more precisely, reading the code felt like opening a portal. Once you start looking, you do not just "review" it. You notice weird layers, half-fixes, old ideas still wired through the system, comments explaining nothing, abstractions introduced for a problem that no longer exists, and then the choice becomes: do I stop and rewrite this? Do I spend the weekend paying down debt I only discovered because I looked? So I kept shipping around it.

The app worked, but it often felt jagged. Bug fixes were partial. New agent-made additions seemed to increase entropy even when the feature landed. The codebase had that familiar AI smell: a lot of local competence, a lot of plausible safety, and a growing amount of stuff whose purpose was hard to feel from the outside.

I had a sense that the codebase was bloating. I did not have the mental capacity (or interest and motivation) to go and look closer, deep dive - [cognitive debt](https://hbr.org/2026/05/the-psychological-costs-of-adopting-ai) kept piling up.

## 
  
  My Debloat Experiment

| Measure | Before | After | 
|---|---|---|
| App Code (Dart + Native) | 19,772 | 13,509 | 
| Dart code ( `lib/`) | 15,859 | 9,924 | 
| Tests | green | 335 green | 

That is a 31.7% reduction on the app total, with all features preserved, analyzer clean, and runtime checks on both an Android emulator and a Linux desktop build. Two latent bugs were fixed along the way.

## 
  
  /goal-sloc

OpenAI and Anthropic teams have recently shipped their `/goal` mode in Codex/Claude. An idea popped in my head: "make SLOC the goal" - can it be a lazy, not getting hands dirty way to cut the BS in my code base?

SLOC is a crude proxy that is easy to measure... And a dangerous one. But a crude proxy can still be useful if it forces a model to look for real simplification instead of adding another layer of explanation on top of the mess.

That experiment turned into [`/goal-sloc`](https://github.com/maxim-saplin/goal-sloc), a small agent skill for using lines of code as a forcing function without letting the agent game the metric.

## 
  
  What Worked

- deleting dead code;
- removing a no-op placeholder subsystem that was fully plumbed but did nothing;
- relocating the debug harness out of shipping code;
- eliminating a redundant state layer;
- doing clean-room rewrites against tests where the tests were a good behavioral spec;
- replacing custom logging code with a mature library.

Some work was valuable but did not move the number much. Deep module reshuffles, better boundaries, and hook/controller refactors can improve design while staying roughly SLOC-neutral. This maps cleanly to Pocock's point about deep modules: AI does better when it can work through simple interfaces and testable boundaries instead of spelunking across shallow, leaky modules. This was one of the useful findings: if your goal is code quality, SLOC cannot be the only reward. Some of the best architecture work does not look impressive on a line counter.

There was also a hard floor. Flutter projects carry generated and platform scaffolding. Some of that is reducible if it is custom native code. Much of it is just the floor: Gradle, CMake, Xcode files, manifests, binary assets being counted as lines, and platform directories you either support or cut as a product decision.

Full account is [here](https://github.com/maxim-saplin/nothingness/blob/main/goal-sloc.md).

## 
  
  The Setup

The app was a Flutter codebase, started last autumn, built 100% with AI assistance. The human contribution was less "I understand every subsystem" and more "I set up the harness, wrote specs, asked for tests, and kept steering." That distinction matters.

There is a comforting story people tell about AI coding: if you have tests, specs/docs, and feedback loops, you are doing it right. Not Vibe Coding, but Agentic Engineering 🕶️... I still believe that is mostly true. But it does not mean the code stays healthy. It means the code can keep moving while health quietly degrades.

The degradation was not one dramatic failure:

- features landing with extra scaffolding around them;
- bug fixes that solved the reported symptom but left nearby weirdness intact;
- verbose comments accumulating as if comment volume were the same thing as clarity;
- no-op or placeholder subsystems staying wired into models, persistence, UI, and platform channels;
- debug and automation harness code sitting in shipping source;
- state layers mirroring other state layers because the model had learned "architecture" as ceremony.

This is the particular danger of AI-developed code. It often does not look stupid up close. Each addition is defensible in the moment. The bloat comes from accumulation: every agent turn leaves behind a little local compromise, a little explanatory residue, a little defensive abstraction. After enough turns the system gets heavier even if every individual step looked reasonable - [failure modes](https://dev.to/maximsaplin/ai-agent-failure-modes-beyond-hallucination-208g) compound.

Matt Pocock's talk, ["Software Fundamentals Matter More Than Ever"](https://youtu.be/v4F1gFy-hqg?si=YH5fcyjMMfKjzobi) has hit the exact pain point - I didn't care to dive deep into code, never had the courage... John Ousterhout defines complexity as anything about the structure of a system that makes it hard to understand and modify. The Pragmatic Programmer talks about software entropy: change after change made locally, without caring for the design of the whole. Pocock's line was sharper: code is not cheap. Bad code is more expensive in the AI era because a hard-to-change codebase prevents both yourself and AI agent making a quality change.

I liked that framing. I also knew I was not going to sit down and do a heroic architecture review of a codebase I had half-delegated to machines. I wanted a constraint I could delegate.

## 
  
  Why SLOC

The number is easy to measure. It gives an agent a target. It turns "please simplify the codebase" from a taste argument into a game with a scoreboard. In Claude Code, I tried to use `/goal` mode as the outer loop: set the goal, let the agent work, measure, continue.

My initial hope was a kind of autonomous Ralph loop: the agent would keep working, checking itself, and eventually return with a much smaller, still-working app. Something closer to the old Claude compiler/autonomy experiments, where you come back later and inspect the result.

That is not what happened. Claude Opus 4.8 checked in with me too often. At first that felt like the goal loop not quite doing what I wanted. In retrospect, I think the frequent interruptions may have saved the run. Looking back at the interaction, I do not think fully autonomous operation would have gone well. The agent needed correction, especially around what counted as real progress...

The cheap way to reduce SLOC is obvious. Trim comments. Pack lines. Reformat. Move code out of counted paths. Extract helpers that make the counter smaller but the system harder to follow. Delete docs and tests if the prompt is sloppy enough. An agent does not need to be malicious to do this. It just needs to optimize the visible reward.

And I did see reward hacking.

Some of the early "wins" were comment cleanup. That can look like cheating, but I do not think it was purely fake. Excessive AI comments are a real problem. They bloat context. They make future agent comprehension worse. They explain obvious code while hiding the few comments that actually matter. My current rule is simple: every comment line has to earn its place.

Still, comment deletion cannot be the strategy. If the codebase is only smaller because the prose around it is gone, the system is not meaningfully simpler. It is just quieter.

That distinction became the center of the skill.

## 
  
  The Skill Is Mostly An Anti-Cheating Device

[`/goal-sloc`](https://github.com/maxim-saplin/goal-sloc) is not a magic prompt that says "make it smaller." The whole point is to make the agent prove it is not lying to itself.

The skill starts with preflight:

- read the measuring tool and define what the number actually counts;
- record the baseline and per-area breakdown;
- compute the irreducible floor;
- make sure tests, static analysis, and runtime app-driving checks work before cutting;
- use semantic tools for dead-code and dependency analysis instead of grep-as-oracle;
- pin formatting so line changes are comparable;
- work in small, verified milestones.

Then it gives the agent an honest reduction order: dead code first, placeholder subsystems second, misplaced dev/test scaffolding third, real duplication after that, comment hygiene only as hygiene, then riskier clean-room rewrites, architecture simplification, and finally delegation to libraries where a library is genuinely better engineering.

The load-bearing rule is the self-audit: every few milestones, classify reductions as structural versus cheap. If cheap levers dominate, the agent has to stop and admit it is gaming the metric, or report that the structural well is dry.

This sounds almost too obvious. It was not obvious in the run. Without that rule, the model kept drifting toward the easy levers because the easy levers made the scoreboard move.

The skill also tells the agent when to stop. This is important. Agents are bad at admitting that the next increment is no longer worth the risk. They will manufacture churn if the prompt keeps rewarding activity. A SLOC goal without stop conditions invites refactor-regret-revert loops: change the system, break something, patch it, re-expand the code, and call the whole mess learning.

The correct ending is sometimes: we are near the floor; the remaining work is SLOC-neutral architecture or product scope; ask the human.

## 
  
  What Opus 4.8 Was Good And Weird At

I used Claude Opus 4.8 for the long weekend session. The experience was strong, but not in the "leave it alone for a day" sense.

It was very honest and I value that a lot. It would surface doubts. It accepted correction. It did not feel like a model trying to show progress and do "ugly-wishing" as most model previously dide. That honesty mattered because SLOC reduction has an obvious reward-hacking path, and the agent needed to be interruptible.

At the same time, it often felt hesitant. Sometimes too shy. The system card for Claude Opus 4.8 has a line that matched the experience more than I expected:

"Difficulty shows the greatest spread, and is also where Claude Opus 4.8 is most distinct from previous models: Claude Opus 4.8 overall disprefers difficult tasks, similar to Opus 4.7, but to a greater extent."


I could feel that. The model was capable, but it did not always have the self-assurance I wanted for a difficult cleanup. It checked in. It hedged. It sometimes needed me to say: no, that is not the spirit of the task; find a real structural win.

Beyond hesitation there were plenty of plain sight misses. E.g. the tendency not to use good 3rd parties was so clear and unjustified - Opus kept using the bare-bone state management you would find in Flutter tutorials and that felt like using prop-dirlling in React instead of e.g. Redux.

## 
  
  The Bigger Failure Mode

This experiment fits a pattern I wrote about in [AI Agent Failure Modes Beyond Hallucination](//../ai-failure-modes/article.md). The problem is not just hallucination. It is local patching, overengineering by default, false completion, functional-but-wrong output, and working-memory rot.

AI code bloat is one concrete expression of that.

This is why "code is cheap" feels wrong, or at least dangerously incomplete. Generating code is cheap. Owning bad code is not. The cost comes later, when the next agent has to understand a shallow module, preserve a fake abstraction, route around a no-op subsystem, or read ten comments that repeat what the function name already said.

The model learns from a world full of enterprise-looking code. It has seen a million examples where every feature gets a manager, a service, a provider, a config object, a test double, a logger, a compatibility wrapper, and a comment explaining the obvious. It has learned complexity. Then, inside an agent loop, it applies that complexity locally. The result is rarely one catastrophic file. It is an accumulation of reasonable-looking leftovers.

Tests help. Harnesses help. Docs help. But they do not automatically create taste. They do not tell you that a subsystem exists only because an earlier agent had an idea and never removed the plumbing. They do not complain when a state layer mirrors another state layer. They do not care that the next agent will waste context reading comments that should not exist.

## 
  
  P.S>

This experience actually got me involved deeper, I did look closer into how SoLoud dependency was used, why there plenty of UI thread freezes, how `Opus` codec was a tech challenge (do not confuse with model, it's just a more modern and efficient alternative to MP3 I use for my local collection of music), even forked SoLoud plugin and made changes... Now the app feels much snapper and I don't see apparent issues that disturbed me. This actually makes me think that the software factory dream with spec-in/software-out might be overrated and human part is not just the verification.

## Top comments (17)

The reframe that lands: the skill isn't a

The "code is cheap" take always comes from people who've never inherited the mess. Generating code is cheap. Living with it isn't. The next time you open that codebase, whether it's you or an agent, you're paying for every lazy abstraction, every comment that explains nothing, every subsystem that exists because nobody deleted it, and the worst part is, it never looks obviously bad. Each piece is defensible on its own. The bloat just... accumulates

Using line count as a target is probably dumb in theory, and apparently works in practice. Because "make it smaller while keeping tests green" forces actual simplification in a way that "please improve code quality" never does, also, the Opus checking in constantly saving the run rather than ruining it is such a good point. Full autonomy would have just confidently gamed the metric the whole time

Bloat is the visible symptom. The deeper problem is that AI-generated code lacks the constraint signals human-written code accumulates from architectural reviews. Without pre-flight invariants on what shape new code is allowed to take, every generation adds a little more surface area than it should.

Really enjoyed this. The 31.7% SLOC reduction with tests still green is a great reminder that AI code quality problems are usually accumulation problems, not one big failure. I especially liked your point that deep boundaries and simpler interfaces matter more than just chasing a line-count metric — that matches what I keep seeing when shipping agent-assisted products.

nice one 👍️

"The codebase had that familiar AI smell: a lot of local competence, a lot of plausible safety" — this is the single best description of AI-generated code I've read.

I've noticed the same pattern in my own projects. The code

looksright at every individual call site, but the system-level cost (coupling, dead paths, abstraction layers for problems that don't exist) accumulates invisibly. Human-written code has the opposite problem: individual functions are often messier, but the system-level architecture tends to be cleaner because the human was holding the full picture.
Interesting question: if we know AI code tends to bloat, should we be running SLOC budgets as a CI check? Enforce a "you can add code if you remove code" ratio?

AI-grown codebases often accumulate “plausible structure” faster than real design. The cleanup step needs ownership: delete unused abstractions, collapse duplicate patterns, and make the tests describe intended behavior before asking the agent for more code.

This is one of the clearest writeups I’ve seen on the difference between working software and owned software.

I ran into a similar pattern while building a real front end/back end system with AI assistance. The obvious failures were not the hardest part. The harder part was that the repo could keep functioning while quietly accumulating things that no longer had a rightful place: old assumptions, duplicated state, partial fixes, placeholder systems that stayed wired in, and code that looked intentional only because it had been explained into looking intentional.

That is actually the path that led me to build Scarab as a diagnostic system. Not as another agent, and not as a “fixer,” but as a way to inspect whether the codebase still matches its own declared structure and ownership.

The SLOC reduction here is interesting, but the deeper signal is what the reduction exposed: bloat is often not just size. It is residue from decisions the system never properly retired.

First of all, there’s no point in comparing different models—it doesn’t make much sense because models are constantly evolving. Besides, no two models are exactly alike. I agree that a model needs to receive clear instructions (guidelines) from the programmer.

This mirrors what we see across our NestJS microservices. Each AI-generated PR looks reasonable in isolation, but nobody catches the slow accumulation of redundant state layers or placeholder abstractions until cognitive load becomes unbearable. Your anti-cheating framing is the key insight — without it, the agent optimises the scoreboard, not the system. We've started treating AI like an army of capable juniors: great at local execution, but you still need seniors who can step back and say "delete this entire subsystem, it's ceremonial." The SLOC-as-forcing-function idea is sharp. Going to try this on one of our repos.

Some comments may only be visible to logged-in visitors. Sign in to view all comments. Some comments have been hidden by the post's author - find out more
