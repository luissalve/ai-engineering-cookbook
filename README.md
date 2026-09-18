# AI Engineering Cookbook

A small, browsable library of production-AI patterns — each one self-contained, runnable, and written to be read in five minutes.

## Why this exists

Most public AI examples are either full frameworks (too much to read) or single-file hacks (too little to trust).
This cookbook sits in the middle: each pattern is small enough to read top-to-bottom yet complete enough to show the real shape of the problem — including the "gotcha" it solves.
It's a v1 scaffold: working skeletons and clear, honest extension points, not a finished product.

## Patterns

| Pattern | Language | What it demonstrates | How to run it offline | Status |
|---|---|---|---|---|
| [`rag-pgvector/`](./rag-pgvector/) | Python | Chunk → embed → store → retrieve pipeline over Postgres + pgvector, with overlapping chunks and `(source, chunk_index)` metadata for citeable retrieval | `pip install psycopg2-binary numpy`<br>`export DATABASE_URL="postgresql://user:pass@localhost:5432/ragdb"`<br>`python rag.py` | working |
| [`mcp-server-boilerplate/`](./mcp-server-boilerplate/) | TypeScript | Minimal Model Context Protocol server: one tool (`echo_upper`) registered with a `zod` input schema, validated before the handler runs, served over stdio | `npm install`<br>`npm run build`<br>`npm start` | working |
| [`voice-agent-skeleton/`](./voice-agent-skeleton/) | Python | FastAPI webhook bridging an incoming Twilio call to a voice agent — `POST /twilio/incoming-call` returns TwiML, `POST /elevenlabs/signed-url` issues a short-lived signed WebSocket URL. Described from README; `main.py` is not part of the public snapshot | `pip install fastapi uvicorn httpx`<br>`cp .env.example .env`<br>`uvicorn main:app --reload --port 8000` | scaffold |
| [`eval-harness/`](./eval-harness/) | Python | Tiny eval loop: `(input, expected_contains)` cases, a substring scorer, a pass/fail report with a pass rate. No API key required — the system under test is a stub | `python eval.py` | working |

## How the patterns fit together

These four are designed to compose. `rag-pgvector` ingests documents and exposes grounded retrieval. `mcp-server-boilerplate` exposes tools — including that retrieval — to any MCP-compatible LLM client over a standard protocol instead of a bespoke API. `voice-agent-skeleton` brings the same agent into a phone-call channel using Twilio for telephony and a per-call signed URL for the voice agent. `eval-harness` runs a regression check against any of the above so a prompt change or model swap can't silently degrade known cases. Every box in the diagram below is a folder in this repo.

```mermaid
flowchart LR
    Docs[Documents] --> RAG[rag-pgvector<br/>chunk + embed + retrieve]
    RAG --> Agent[Agent tools<br/>exposed via MCP]
    Agent --> Voice[voice-agent-skeleton<br/>Twilio + voice channel]
    Agent --> Evals[eval-harness<br/>regression checks]
```

## Conventions

- **Self-contained.** No pattern imports from another. Copy one folder into your project and adapt.
- **`.env.example` only.** Any required credential is documented in the pattern's README and supplied via environment variables; no secret is ever hardcoded.
- **No shared state.** Each pattern has its own dependencies, its own runtime, its own tests. There is no cross-pattern dependency graph.
- **Tests live next to code.** When a pattern has tests, they sit inside the pattern's folder so the folder stays copy-pasteable.
- **Honest about scope.** Every README states plainly what's simplified and what a real deployment would still need to add.

## Status & roadmap

This is a **v1 scaffold** — one commit per pattern, illustrative skeletons only. The next commits the maintainer plans to land are listed in [`CHANGELOG-PROPOSAL.md`](./CHANGELOG-PROPOSAL.md). In short: add a real pytest suite for `eval-harness`, add a Node test for `mcp-server-boilerplate`, add a CI matrix that exercises every pattern, and add a new high-signal pattern proposal.

## License

MIT — see [LICENSE](./LICENSE). Copy, adapt, and reuse freely.
