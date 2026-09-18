# Changelog Proposal

Proposed next commits for `ai-engineering-cookbook`. Each entry is small, verifiable, and has an offline-runnable acceptance check. Commits are listed in suggested landing order.

---

## 1. `test(eval-harness): add pytest suite with fixture-based case set`

**Why first.** Adds the first real automated test in the repo, on the pattern with the fewest moving parts, so the CI matrix in commit 3 can rely on it.

**Files touched**
- `eval-harness/tests/test_eval.py` (new)
- `eval-harness/requirements-dev.txt` (new)
- `eval-harness/README.md` (extended "How to run" with the test command)

**What changes**
- Adds a pytest suite that loads `eval.py` as a module via `importlib` (no packaging required), exercises `score()` and `run_eval()` against fixture cases, and asserts that the shipped `CASES` list still all passes against its own stub.
- Introduces `requirements-dev.txt` with `pytest>=8.0` as the only test-only dependency. Pytest is unavoidable for a pytest suite and lives in a dev requirements file, not the runtime path — `eval.py` itself still uses only the standard library.

**Acceptance check (offline)**
```bash
cd eval-harness
pip install -r requirements-dev.txt
pytest -q
# Expected: all tests pass.
```

**Estimated size:** ~95 lines added across 3 files (test ~85 lines, requirements-dev.txt ~7 lines, README delta ~3 lines).

---

## 2. `test(mcp-server-boilerplate): add vitest suite for tool registration`

**Files touched**
- `mcp-server-boilerplate/test/server.test.ts` (new)
- `mcp-server-boilerplate/package.json` (added `vitest` to `devDependencies`, added `test` script)
- `mcp-server-boilerplate/README.md` (extended "How to run" with `npm test`)

**What changes**
- Spawns the server over `@modelcontextprotocol/sdk`'s `InMemoryTransport` (already in the runtime SDK, no new runtime dep) and asserts that `ListToolsRequestSchema` returns exactly one tool (`echo_upper`) with the expected name, description, and required input field.
- Sends a valid `CallToolRequestSchema` request and asserts the uppercased text comes back.
- Sends a request with empty `text` and asserts the response has `isError: true` and a structured validation message — covering the "gotcha" the README calls out.
- `vitest` is added as a `devDependency` only; no runtime dep change.

**Acceptance check (offline)**
```bash
cd mcp-server-boilerplate
npm install
npm test
# Expected: vitest reports all tests passing.
```

**Estimated size:** ~150 lines added across 3 files.

---

## 3. `ci: add GitHub Actions matrix (Python 3.12 + Node 22) for all patterns`

**Files touched**
- `.github/workflows/ci.yml` (new)

**What changes**
- A single matrix workflow triggered on `push` and `pull_request` that:
  - Sets up Python 3.12 and Node 22 on `ubuntu-latest`.
  - For `eval-harness`: installs test deps and runs `pytest -q`.
  - For `mcp-server-boilerplate`: runs `npm ci && npm test`.
  - For `rag-pgvector`: installs `psycopg2-binary numpy` and runs `python -c "import psycopg2, numpy"` (placeholder smoke check; a real `rag-pgvector/test_smoke.py` is a follow-up).
  - For `voice-agent-skeleton`: installs `fastapi uvicorn httpx` and runs `python -c "import fastapi, uvicorn, httpx"` (placeholder; `main.py` is not in the public snapshot, so end-to-end is a follow-up).
- Adds no new dependencies; this commit is workflow-only.

**Acceptance check (offline)**
```bash
python -c "import yaml; data = yaml.safe_load(open('.github/workflows/ci.yml')); print(list(data['jobs'].keys()))"
# Expected: a list containing one job (e.g. ['test']) that fans out to the four patterns.
```

**Estimated size:** ~70 lines added, 1 file.

---

## 4. `docs(patterns): add observability pattern proposal (LLM cost / latency)`

**Files touched**
- `patterns-proposed/llm-observability/README.md` (new, **proposal only**)

**What changes**
- Adds a `patterns-proposed/` directory and a README-only design note for an LLM cost-and-latency observability skeleton. The note proposes a small decorator-style wrapper that records `(timestamp, model, prompt_tokens, completion_tokens, latency_ms, request_id, status)` rows to a local SQLite file per run and prints a per-model summary (total cost from an inline `PRICING` dict, p50 / p95 latency) at the end.
- **No code is shipped.** This is a proposal for maintainer review before implementation; the file is explicitly labelled "proposal — not implemented" and is not referenced from the root patterns table.

**Why this pattern.** Every other pattern here either generates tokens (`eval-harness`, `voice-agent-skeleton`), retrieves documents (`rag-pgvector`), or brokers tool calls (`mcp-server-boilerplate`). A thin wrapper that adds a cost/latency envelope to any of them is the smallest credible observability story the cookbook can ship without committing to a vendor.

**Acceptance check (offline)**
```bash
test -f patterns-proposed/llm-observability/README.md
grep -q "Status: proposal" patterns-proposed/llm-observability/README.md
# Expected: file exists and is labelled as a proposal.
```

**Estimated size:** ~75 lines added, 1 file.

---

## 5. `docs: add CONTRIBUTING.md and pull request template`

**Files touched**
- `CONTRIBUTING.md` (new)
- `.github/PULL_REQUEST_TEMPLATE.md` (new)

**What changes**
- Short contributor guide: one paragraph on what belongs here (a single self-contained pattern that fits in one folder), how to run the test matrix locally, and a checklist that mirrors the conventions in the root README (self-contained, `.env.example` only, tests next to code, no invented features).
- A PR template that asks the author to tick the same boxes before review.

**Acceptance check (offline)**
```bash
test -f CONTRIBUTING.md && test -f .github/PULL_REQUEST_TEMPLATE.md
grep -q "self-contained" CONTRIBUTING.md
grep -q ".env.example" .github/PULL_REQUEST_TEMPLATE.md
# Expected: both files exist and reference the repo conventions.
```

**Estimated size:** ~60 lines added across 2 files.
