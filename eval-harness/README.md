# eval-harness

A tiny LLM eval loop: a list of example cases, a scoring function, and a pass/fail report.

## What it is

A ~70-line harness that runs a set of `(input, expected)` cases through a function under test (a prompt, a chain, an agent — anything that takes text in and returns text out), scores each output against its expectation, and prints a summary with a pass rate. No framework, no external eval service — just the loop every eval tool (promptfoo, Braintrust, etc.) wraps under the hood.

## When to use it

- You changed a prompt or swapped a model and need a fast, repeatable check that you didn't regress known cases — before reaching for a full eval platform.
- You want to understand what an eval framework actually does before adopting one.
- You need a lightweight regression check inside CI for a small, stable set of cases.

## The gotcha it solves

**"It looks right" is not a test.** Without a harness, prompt changes get validated by eyeballing one or two outputs, which misses regressions on cases you didn't happen to check. The two things this skeleton forces you to do:

- **Write down expected behavior before changing anything** — each case states what a correct answer must contain, so "did this get better or worse" has an actual answer.
- **Score with a function, not a vibe** — the scorer here is a simple substring/keyword check, but the harness is structured so you can swap in an LLM-as-judge scorer later without changing the loop itself.

## How to run

This is an **illustrative skeleton** — the scorer is intentionally simple (substring matching), not an LLM-as-judge. Swap `score()` for something stronger (embedding similarity, an LLM grader) once the loop itself is proven out.

```bash
python eval.py                       # runs the eval loop on the shipped cases

pip install -r requirements-dev.txt  # one-time: installs pytest for the test suite
pytest -q                            # runs the automated test suite in tests/
```

No API key required — the "system under test" in `eval.py` is a stub function so the harness runs standalone. Replace `system_under_test()` with a real call to your prompt/agent/chain.

## What's simplified here (not production-hardened)

- Scoring is substring matching, not semantic similarity or an LLM judge.
- No parallelism — cases run sequentially.
- No persistence — results print to stdout; a real harness would log runs over time to track regressions.
