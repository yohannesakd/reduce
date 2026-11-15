# Debug or harness code in shipping source

**Signal.** `print` statements, test-automation hooks, or a debug harness in the production module.

```python
print("here", payload)
if os.environ.get("AUTOMATION_MODE"):
    install_test_hooks()
```

**Decide with.** An environment switch reads the runtime environment. Apply the environment rule in [Fixed behavior](../../guides/fixed-behavior.md#fixed-behavior).
Search CI, scripts, deployment config, and docs for the variable. If nothing sets it, `remove`. If a test setup sets it, move the hook into the test code (`prevent`).

**Keeps it when.** A production support runbook sets the variable.

**Sources.** [Debloating post](https://dev.to/maximsaplin/debloating-the-ai-grown-codebase-2om), [sloppylint](https://github.com/rsionnach/sloppylint).
