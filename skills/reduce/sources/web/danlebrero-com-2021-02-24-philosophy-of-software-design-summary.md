# Book notes: A Philosophy of Software Design

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: Daniel Lebrero Berna
- Date: 2021-02-24
- Original location: https://danlebrero.com/2021/02/24/philosophy-of-software-design-summary/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
# Book notes: A Philosophy of Software Design

Book notes on John Ousterhout's "A Philosophy of Software Design"

These are my notes on [John Ousterhout](http://web.stanford.edu/~ouster/cgi-bin/home.php)’s [A Philosophy of Software Design](https://amzn.to/3rmPntd).

Some advice in the book goes against the current software dogma. The current dogma is the result of previous pains, and as it is usual, we have taken it to the extreme causing new pains.

The other interesting bit was that what I solve by doing Test-Driven Development, the author solves with [“Comment-First Development”](#ch-15). And all the excuses to not write comments listed by the author, are the same excuses to not write tests.

# Key Insights

- It’s easier to see design problems in someone else’s code than your own.
- Total complexity = Sum(complexity of part \* time spend on that part).
- Goal of good design: make system obvious.
- Complexity accumulates incrementally, hence:
  
  - Hard to remove.
  - Must adopt a “zero tolerance” philosophy.
- Better modules: interface much simpler than implementation (Deep modules).
- When designing modules focus on the knowledge that is needed to perform a task, not the order of the tasks.
- Adjacent layers with similar abstractions are a red flag with class decomposition.
- It is more important for a module to have a simple interface than a simple implementation.
- Each method should do one thing and do it completely.
  
  - Methods with hundreds of lines of code are fine if they have a simple signature and are easy to read.
- If it is hard to pick a simple name, maybe design is not clean.
- Comments should add precision or intuition.
- When changing code, if you are not making the design better, you are probably making it worse.
- Comments belong to the code, not the commit log.
- Poor designers spent most of their time chasing bugs in complicated and brittle code.

# TOC

# 

- The most fundamental problem in computer science is problem decomposition.
- This book is an opinion piece.
- The overall goals is to reduce complexity.

# 

- Fight complexity by:
  
  - Make code simpler and more obvious.
  - Encapsulate complexity in modules.
- SW design is never done.
- It’s easier to see design problems in someone else’s code than your own.

# 

- Complexity is anything related to the structure of a SW system that makes it hard to understand and modify.
- Total complexity = Sum(complexity of part \* time spend on that part).
- If you never have to touch one part, it adds little complexity.
- Complexity is more apparent to readers than writers.
- Symptoms of complexity:
  
  - Change amplification.
  - Cognitive load: How much you need to know to make a change.
  - Unknown unknowns.
- Goal of good design: make system obvious.
- Causes of complexity:
  
  - Dependencies.
  - Obscurity: when important information is not obvious.
- Complexity accumulates incrementally, hence:
  
  - Hard to remove.
  - Must adopt a “zero tolerance” philosophy.

# 

- Tactical vs strategic.
- Tactical tornado: prolific programmer who pumps out code far faster than others but works in a totally tactical (hacky) fashion.

# 

- Module = interface + implementation
- Better modules: interface much simpler than implementation (Deep modules).
- Interface: what a client needs to know in order to user the module correctly.
- Interface: formal (enforced by compiler) + informal (you need documentation for this).
- Abstraction: simplified view that omits *unimportant* details.
- Classitis:
  
  - Loads of tiny and simple classes that result in increased overall system complexity.
  - Java IO as an example.
- Interfaces should be designed to make the common case as simple as possible.

## 

- Information hiding is the most important technique for achieving deep modules:
  
  - Simplifies interface.
  - Easier to change implementation details.
- Avoid temporal decomposition:
  
  - When designing modules focus on the knowledge that is needed to perform a task, not the order of the tasks.
- Information hiding can often be improved by making a class slightly larger.
- HTTP server example: See [“Death by Specificity”](https://www.youtube.com/watch?v=VSdnJDO-xdg&t=32m32s) for the opposite view.

## 

- Make modules “somewhat general-purpose”:
  
  - Implementation reflects current needs.
  - Interface is general enough to support multiple uses.
- General-purpose is simpler. Do I disagree???
- Questions to find the right balance:
  
  - What is the simplest interface that will cover all my current needs?
  - In how many situations will this method be used?
    
    - Expectation: more than once.
  - Is this API easy to use for my current needs?
    
    - If not, it is too general.

## 

- Adjacent layers with similar abstractions are a red flag with class decomposition.
- Pass-through methods are bad because they contribute no new functionality.
- Pass-through variable:
  
  - Var passed through a long chain because a low level method needs it.
  - To fix:
    
    - Add it to an object already shared with the lower layer.
    - Store in global variable.
    - Pass around a context object.

## 

- It is more important for a module to have a simple interface than a simple implementation.
- Most modules have more users than developers.
- Configuration parameters push complexity upwards.
  
  - Try to computer reasonable defaults automatically.

## 

- Together if:
  
  - Share information.
  - Used together.
  - Overlap conceptually.
  - Hard to understand without the other.
  - Simplifies the interface.
  - Eliminate duplication.
- In general, developers tend to break up methods too much.
- Each method should do one thing and do it completely.
- Methods with hundreds of lines of code are fine if they have a simple signature and are easy to read.
- Red flag: if to understand the implementation of one part, you must understand the implementation of other part.

## 

- Exception handling is one of the worst sources of complexity.
- Exception handling is inherently more difficult to write.
- Reduce the number of places where exceptions must be handled:
  
  1. Define your APIs so there are no exceptions to handle:
    
    - Example [Windows vs Unix delete file in use](https://unix.stackexchange.com/questions/49299/what-is-linux-doing-differently-that-allows-me-to-remove-replace-files-where-win).
  2. Mask exception: low level code to handle exception.
    
    - Example: NFS client handing app if server is not responding. Disagree completely of this being a good example.
  3. Exception aggregation:
    
    - Bundle exceptions into one more generic that can be handled in the same way.
  4. Crash the app

## 

- Pick at least two approaches that are radically different.

## 

- The process of writing comments will improve the design.
  
  - Unfortunately, this view is not universally shared. :)
- Writing comments can be fun.
- Excuses:
  
  - Good code is self-documenting. A myth.
  - I don’t have time to write comments.
    
    - Future investment.
  - Comments get out of date:
    
    - Just remember to update them.
  - All the comments I have seen are worthless, so why bother?
    
    - Learn to write good comments.

## 

- Comments should add precision or intuition.
- Interface vs implementation comments.

## 

- Names should be:
  
  1. Precise: so that you dont need to read the doc (why write the doc then?)
  2. Consistent.
- If it is hard to pick a simple name, maybe design is not clean.

## 

- Same reasons as why to write tests first:
  
  1. They help design.
  2. You will have time to.
  3. It is more enjoyable.
  4. You may go faster.

## 

- If you are not making the design better, you are probably making it worse.
- Comments belong to the code, not the commit log.

## 

- Dont “improve” existing conventions. Probably not worth it.

## 

- Agile and TDD encourage tactical programming.

## 

- Simpler code tends to be faster.
- Design around the critical path.

## 

- Poor designers spent most of their time chasing bugs in complicated and brittle code.

[Follow @DanLebrero](https://twitter.com/DanLebrero)or share!
