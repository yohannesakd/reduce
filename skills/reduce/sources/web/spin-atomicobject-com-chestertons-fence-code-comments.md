# Chesterton's Fence and Explaining with Code Comments

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: Mattie Behrens
- Date: 2021-06-19
- Original location: https://spin.atomicobject.com/chestertons-fence-code-comments/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
I recently came across the idea of [Chesterton’s fence](https://www.chesterton.org/taking-a-fence-down/) and noticed that it was relevant to a project I’d worked on.

## The Urge to Rewrite and Remove

Not long ago, I was pairing with another developer. We were working together through a system neither of us had designed (but, of course, [we owned](https:/own-it-distributed-team/), nonetheless).

This system was struggling with heavy resource consumption. It had finally broken its limits, crashing because it ran out of memory. We needed to get its resource use down to a level where we could rely on it again.

As a result, we were in full “question everything” mode. We were trying to account for every wasteful activity. We hoped we’d find some unnecessary overhead that we could just do away with — and save the day.

The system was constructed out of a series of services. Each one took data and transformed or processed it in a specific way, creating input for the next service. At the end of the line, the finished product was uploaded.

Somewhere in the middle, we found a shining beacon of what looked like waste. It was accumulating an entire run’s worth of data in memory only to dump it back out again.

“This can go,” I said, thinking aloud to my pair. “I don’t see why this is written this way. It could be streaming the data without collecting it. It looks like this is just a remnant of a previous design.”

## Chesterton’s Fence in Our Codebase

I hadn’t yet heard of Chesterton’s fence at the time. Chesterton writes:

In the matter of reforming things, as distinct from deforming them, there is one plain and simple principle; a principle which will probably be called a paradox. There exists in such a case a certain institution or law; let us say, for the sake of simplicity, a fence or gate erected across a road.

The more modern type of reformer goes gaily up to it and says, “I don’t see the use of this; let us clear it away.” To which the more intelligent type of reformer will do well to answer: “If you don’t see the use of it, I certainly won’t let you clear it away. Go away and think. Then, when you can come back and tell me that you do see the use of it, I may allow you to destroy it.”


I ended up reading about this metaphorical fence a week or two later, on a Wikipedia bender. It struck me that this idea was relevant to the thought process I’d had while working through this system.

When we come into a system that exists already, we are likely to encounter things we don’t comprehend. We think of ourselves as modern, efficient developers, poised and ready to sweep the obsolete cruft away and deliver a well-oiled machine.

In reality, that old code often has a story to tell. It’s true that, sometimes, the story is that the developers were under pressure. Sometimes they hadn’t foreseen the problem they’d created that led us back to the code now.

But sometimes, the story is that they were confronted by a challenge. This challenge is something we don’t see now. Maybe it’s even a challenge they won’t remember anything about if we have the chance to ask them.

## The Unknown Risk of Tearing Down a Fence

We didn’t immediately tear out that piece of code. I considered how much work it might take and the fact that our product owner should prioritize this sort of work. And, of course, we considered *the risk* of unknown failures resulting from such a change.

My pair and I thought about it, trying to turn the unknown into a known. We leveraged our experience to consider what this particular part of the system could be doing that wasn’t immediately obvious.

We dug deeper and realized that the way it was implemented meant it was serving the purpose of a check on our data. It was stopping us from accumulating more than one item with the same key.

Without this piece of the system, the output of this step was just a stream of data items, which would have no such check. And though we didn’t expect our upstream output to generate duplicate keys, no property of the system actually *prevented* it.

We still ended up recommending the removal of that particular component to relieve the resource pressure. But we also took the time to identify what could happen and verify that we weren’t going to experience a change in behavior downstream if we removed that code.

My pair and I resolved our breakage anxiety. We gave our product owner solid and reliable information with which they could make a priority decision. We gained a better understanding of our system. And we knew that we didn’t take away a key robustness property.

## Code Comments as Signposts

Going through this exercise was not a waste. But we do want to consider how we might help future developers gain understanding faster.

This is exactly what code comments are for. We can post a sign next to our new, streamlined implementation, explaining the risk we identified and that we verified that we’d managed the risk. We could go downstream and add some commentary there, as well, pointing out exactly where and how this risk became a non-issue.

For fences that we build or ones we ultimately leave up, posting these markers will make it easier for people in the future to understand why we did what we did. Then, they can make decisions for themselves as to whether those fences stay or go.

In the end, we tore down that fence. But we left a marker showing future passersby that we’d understood why it was there. And, I hope, we helped them understand why they wouldn’t need to build a new one.
