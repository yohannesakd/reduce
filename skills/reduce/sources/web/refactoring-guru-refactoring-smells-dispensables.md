# Dispensables

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: Alexander Shvets
- Original location: https://refactoring.guru/refactoring/smells/dispensables
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
# Dispensables

A dispensable is something pointless and unneeded whose absence would make the code cleaner, more efficient and easier to understand.

A method is filled with explanatory comments.

Two code fragments look almost identical.

Understanding and maintaining classes always costs time and money. So if a class doesn’t do enough to earn your attention, it should be deleted.

A data class refers to a class that contains only fields and crude methods for accessing them (getters and setters). These are simply containers for data used by other classes. These classes don’t contain any additional functionality and can’t independently operate on the data that they own.

A variable, parameter, field, method or class is no longer used (usually because it’s obsolete).

There’s an unused class, method, field or parameter.
