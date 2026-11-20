# 4 Strategies To Remove Dead Code from your Ruby App

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: Stefanni Brasil
- Date: 2023-06-06
- Original location: https://thoughtbot.com/blog/how-to-remove-dead-code-ruby
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
*This post was originally published on the [hexdevs blog](https://www.hexdevs.com/posts/how-to-remove-dead-code-ruby/).*

It’s easy to believe that just because a feature is available, it is going to be used someday. But let’s face it: some features in production will go completely unnoticed and unused forever, but you still have to maintain them.

How much does it cost to carry all this dead code around?

After all, to keep these pointless features running, the business has to spend time and money to:

- keep these features working (maintenance costs)
- test and deploy them
- adjust them so they can interact with other features and not cause bugs
- provide user support and documentation

That’s why finding and deleting dead and redundant code is an important step to increasing the code quality of an application, according to [M. Scott Ford](https://www.hexdevs.com/posts/building-technical-wealth-legacy-code-m-scott-ford/).

In this post, you’ll learn 4 strategies to uncover dead code and delete it with total confidence from your Ruby application.

## 
    [1 - Find and Remove Dead Code with the Coverband Ruby Gem](#1---find-and-remove-dead-code-with-the-coverband-ruby-gem)
  

The scariest part of removing any code is… what if someone is indeed using it but there is no way for us to know?!

What if there was a way to identify which lines of code have actually been used in production, by real users?

That’s what the [Coverband Ruby Gem](https://github.com/danmayer/coverband) is all about. According to their README, Coverband is:

A gem to measure production code usage, showing a counter for the number of times each line of code that is executed. Coverband allows easy configuration to collect and report on production code usage. It reports in the background via a thread or can be used as Rack middleware, or manually configured to meet any need.


Coverband is easy to install and use. The dashboard is similar to SimpleCov (but don’t let that confuse you, it has nothing to do with *test* coverage).

The screenshot is from a real project dashboard used by a client. I left Coverband running for a couple of months. Eventually, it was clear that for a given feature X, no lines of code related to that feature were being used.

From the report, two columns stand out: `Runtime` and `Lines runtime`. No one was calling those files. Plus, if you subtract `Lines missed` from `Relevant lines`, it’s another indicator that these files are basically only being called when the app loads.

The client’s team said that the 6,000 lines of code could be removed, and they were happy to see them gone. It was a feature that didn’t go anywhere. It was hard to maintain it, and users didn’t really want it 😿

If this code was never analyzed and deleted, we wouldn’t have had the opportunity to learn from this mistake. And we would be carrying more than 6,000 lines of dead code.

## 
    [2 - Run a Ruby Static Code Analysis with the Debride Gem](#2---run-a-ruby-static-code-analysis-with-the-debride-gem)
  

[Debride Ruby gem](https://github.com/seattlerb/debride) is a tool for analyzing code for potentially uncalled/dead methods.

Similar to Coverband, it generates a report. The difference is that it generates a file listing methods that might not be used. Debride even has some cool features such as a Rails-specific domain knowledge flag, and auto-removal flags.

Here is an example of a Debride analysis file:

```
These methods MIGHT not be called:
User
  is_a_cat_owner?                     ./app/models/user.rb:229-230 (2)
  has_new_notifications?              ./app/models/user.rb:312-313 (2)
  has_old_notifications?              ./app/models/user.rb:316-317 (2)
  is_a_member?                        ./app/models/user.rb:140 (1)
```
Did you see the `MIGHT not be called` at the top of the file? That’s because Debride’s report is not 100% accurate. A method or class might be called dynamically at runtime. Plus, the methods might be called somewhere else outside the Ruby code. In this client’s project, for example, we have lots of methods being used only by the frontend.

As with Coverband, before you go out there removing code, do some due diligence work to figure out what’s really happening.

## 
    [3 - Wrap “Dead or Alive” Code with Feature Flags](#3---wrap-quotdead-or-alivequot-code-with-feature-flags)
  

Coverband and Debride are great tools to get started with removing dead code. Implementing a Code Audit with Feature Flags is another strategy for when they are not enough.

That’s when the business domain matters: some features are only used once a year, or seasonally. Examples: tax reports, medical reports, and yearly expense reports. How can you confidently remove dead features when the business requirements include seasonality?

Then you might be asking yourself: is this code *dead or alive*?

When you are unsure whether the code is not gonna come back screaming “I’m still alive!”, a solution is to wrap the entrypoint behind a Feature Flag, and turn it off.

If nobody complains and the feature flag doesn’t have to be enabled by next year (or longer, depending on the business’s lifecycle), then just delete the code wrapped by the feature flag. It’s dead.

## 
    [4 - Kill Dead Code with Well-Scoped Pull Requests](#4---kill-dead-code-with-well-scoped-pull-requests)
  

After doing the due diligence to confirm the removal of dead code, another strategy is to make your life easier by creating self-contained PRs.

Always make sure to create PRs that **only** affect the dead code. If you need to roll back the changes, it’s going to be easier to revert the PR.

💡 When you encounter other parts that can be safely deleted when removing dead code, write TODOs with the [TODO Or Die gem](https://github.com/searls/todo_or_die). Then open new PRs for each one of these TODOs. This will make your life easier.

With these strategies, you can focus on improving the code quality for the files that matter, instead of wasting time poking dead code. Plus, you’ll feel the joy of deleting lines of code.

All of these 4 strategies work great together. It’s like you’re a zombie detective!

Have you used any of these strategies before? What are you excited to try?

May the dead code Rest In Peace 🪦🧟
