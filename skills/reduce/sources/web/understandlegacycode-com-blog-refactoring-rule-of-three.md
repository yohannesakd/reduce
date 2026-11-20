# Don't make Clean Code harder to maintain, use the Rule of Three - Change Messy Software Without Breaking It

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: Nicolas Carlo
- Date: 2026-01-01
- Original location: https://understandlegacycode.com/blog/refactoring-rule-of-three/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
# Don't make Clean Code harder to maintain, use the Rule of Three

*Struggling with Legacy Code and not enough time to clean it up?*

⛑️️

**[My First Aid Kit](/first-aid-kit)** can help you rescue any codebase

**quickly**and

**safely**!

“How do you justify more code being written by following clean code practices?”


This is a question I see asked now and then when people try to apply [Clean Code](https://www.oreilly.com/library/view/clean-code/9780136083238/) principles to their existing codebase.

I think it’s a legitimate one.

When you start refactoring Legacy Code, it’s normal to extract things into smaller methods. Then you extract methods into classes. Soon enough, you may feel that what could be a 30 lines method is now spread across different classes.

And you wonder if that is *actually* more maintainable.

Maybe you’re a small team. Maybe you have to support a relatively large (and undocumented) codebase that you inherited.

It’s a good thing to seek for code maintainability 👍

The mistake is to think that code maintainability is related to the count of lines of code (LOC). LOC might be an interesting metric, but it’s not the important one!

**Don’t use LOC as a metric for code maintainability.**

## Short code isn’t more readable.

If you have a doubt about it, then you should take a look at [Code Golf](https://en.wikipedia.org/wiki/Code_golf).

When you’re golfing, your goal is to find clever tricks to achieve the same feature in the minimal amount of code characters:

```
// 31 characters 😞
Math.floor(Math.random() * 100)
// 21 characters 🙂
~~(Math.random()*100)
// 19 characters 😄
Math.random()*100|0
```
But of course, **this is a strawman argument!**

I’m sure you don’t mean to code-golf your production code.

However, there’s an important principle you need to keep in mind:

Code is not how you tell the computer what to do; it is how you tell another programmer what you want the computer to do.


In short: **write code for other people to read.**

Easy-to-understand code is easy-to-maintain code.

Still, aren’t we smart enough to read long functions? What’s good in adding a bunch of use-once helper functions for readability’s sake?

If these questions resonate with you, there’s a secret you need know…

## Premature refactoring is the root of many bad things

Any practice taken to the extreme can be harmful.

Even “Clean Code” principles.

You’re onto something. Yes, it’s possible to refactor the code following best practices and yet make it harder to maintain. If you encapsulate a conditional for the sake of it, then maybe it’s not helping!

No, you shouldn’t extract everything into “use-once helper functions for readability sake”. That doesn’t help if you need to read the body of these functions whenever you read the code. It just gets in the way.

What you should do, is **to create the correct abstractions**.

Correct abstractions correctly separate responsibilities. They clarify the intent of the code. They prevent code duplication.

When you find the correct abstractions, you can feel these 4 classes are actually simpler to maintain than the original 30 lines of code.

But finding the correct abstractions is really hard. Therefore, that’s what you should focus on.

### Bad abstraction is worse than duplication

Have you heard about [Don’t Repeat Yourself (DRY)](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) principle?

It’s a pearl of common development wisdom, and it’s very valid. It’s also often misunderstood.

2 pieces of code can look the same, still represent different concepts. Different abstractions. In such a case, duplication is accidental. Keeping the duplication *is* better.

“Duplication is far cheaper than the wrong abstraction”

– Sandi Metz, [All the little things](https://youtu.be/8bZh5LMaSmE)


When should you extract the code into a function/method/class? When should you keep the duplication? How do you know you have a correct abstraction?

## Use the “Rule of Three”

Also called Write Everything Twice (WET). Pun intended.

“Three strikes and you refactor”


The refactoring [Rule of Three](<https://en.wikipedia.org/wiki/Rule_of_three_(computer_programming)>) is a rule of thumb you can use when you’re in doubt.

Wait until you see the duplication happening a third time before you introduce your abstraction. With more occurrences, it will be easier to find the commonalities to extract.

Follow the Rule of Three. It makes it easier to find correct abstractions.

## Go beyond the Rule of Three

The Rule of Three is here to remind you that **it’s fine to have duplication**.

It’s also a bit dogmatic. Just like Clean Code principles, don’t blindly apply it 100% of the time.

Sometimes, you might not find the correct abstraction, even with 3 duplicated occurrences. Don’t force an over-abstraction into the codebase. If you can’t give it a clear name, it’s not clear enough.

In doubt, it’s fine to break the rule. **Wait for more duplication.**

Prefer duplication over the wrong abstraction. Don’t create an abstraction for the sake of it.

If your abstraction is bad, you’ll have to bend its implementation with [boolean parameters](https://understandlegacycode.com/blog/what-is-wrong-with-boolean-parameters) and `if` statements to cover new use cases. That’s a hint, a warning that you’re not going in the right direction.

It’s also fine if you don’t find the abstraction already. You can still refactor it later when you have more context. Just wait for it!

Written by   [**Nicolas Carlo**](https://bsky.app/profile/nicoespeon.com)  
who lives and works in Montreal, Canada 🍁

He founded the   [Software Crafters Montreal](https://guild.host/software-crafters-montreal)  
community which cares about building maintainable softwares.

## Similar articles that will help you…

[Keeping dependencies up-to-date](/blog/keeping-dependencies-up-to-date)

My recipe for recovering from outdated dependencies and keeping healthy habits

[Should we stick to old patterns or sacrifice consistency?](/blog/consistency-or-progress)

Consistency is great! But over time, it's hard to keep a codebase consistent. Here's my approach to adopt changes without creating a mess.

[Is it fine to use "AND" in a function name?](/blog/improving-legacy-function-names)

Finding a better name for a function is hard, especially when people have contradictory opinions on what a good name looks like…

[Are functions that simply call another function a bad design choice?](/blog/are-wrapper-functions-bad-design)

Let's see how you end up with these while trying to refactor Legacy Code and what you can do about that.

[← Find more tips to work with Legacy Code](/)
