# Shorter code can change behavior

**Source:** a September 2025 Reddit post. It contrasts Cursor's name-splitting pipeline with the author's direct first-character expression.

**Observed.** The shorter expression can produce `undefinedS` when the first name is missing. It can also throw for an empty name. The versions treat names that contain spaces differently.

**Lesson.** The correct reduction depends on the actual input and fallback requirements. Neither fewer lines nor human authorship proves correctness.

**Reduce fit.** Use this case in the check step to reject a reduction whose smaller code changes an inventory entry.

[Original code and objections](https://www.reddit.com/r/webdev/comments/1nbqrf7/public_announcement_ai_is_cool_and_all_but_please/).
