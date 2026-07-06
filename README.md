# AI Engineering Cookbook

A library of reusable, production-oriented AI patterns. Each recipe lives in its own folder, is self-contained, and ships with a short README plus one minimal, runnable code file — no framework, no hidden dependencies between recipes.

This is not a product and not a tutorial series. It's the set of patterns that come up repeatedly when building agentic and retrieval systems in production: chunk-and-embed pipelines, MCP servers, voice webhooks, eval loops. Each one here is an **illustrative skeleton** — the shape of a real solution, stripped of anything project-specific — meant to be copied into a real project and adapted, not run as-is against production traffic.

## Why this exists

Most "AI examples" on GitHub are either full frameworks (too much to read) or single-file hacks (too little to trust). This cookbook aims for the middle: small enough to read in five minutes, complete enough to see the real shape of the problem — including the part that usually gets glossed over (the "gotcha" each recipe solves).

## Patterns

| Pattern | Language | What it solves |
|---|---|---|
| [`rag-pgvector/`](./rag-pgvector/) | Python | Chunk → embed → store → retrieve pipeline over Postgres + pgvector |
| [`mcp-server-boilerplate/`](./mcp-server-boilerplate/) | TypeScript | Minimal Model Context Protocol (MCP) server template |
| [`voice-agent-skeleton/`](./voice-agent-skeleton/) | Python | Twilio call webhook bridged to an ElevenLabs Conversational AI agent |
| [`eval-harness/`](./eval-harness/) | Python | Tiny LLM eval loop: example cases + a scoring function + a pass/fail report |

## How to use this repo

1. Open the pattern folder closest to your problem.
2. Read its README — each one covers **what it is**, **when to use it**, **the gotcha it solves**, and **how to run it**.
3. Copy the folder into your project and adapt it. These are starting points, not installable packages — there is no shared runtime or dependency graph across patterns.
4. Nothing here needs real API keys to *read* — most recipes only need keys if you actually run them end-to-end. Any recipe that does need credentials uses a `.env.example` and never a hardcoded secret.

## Conventions across every recipe

- **Self-contained.** No recipe imports from another recipe.
- **Illustrative, not production-hardened.** Error handling, retries, auth, and observability are simplified or stubbed — each README states plainly what's cut and what a real deployment would add.
- **No secrets, no private code.** Every credential is a placeholder (`.env.example` or inline comment). Nothing here originates from, or reproduces, any client or employer codebase.
- **Small on purpose.** Each snippet is short enough to read top-to-bottom in a couple of minutes.

## License

MIT — see [LICENSE](./LICENSE). Copy, adapt, and reuse freely.
