# rag-pgvector

A minimal chunk → embed → store → retrieve pipeline over Postgres with the `pgvector` extension.

## What it is

The core loop behind almost every retrieval-augmented generation (RAG) system:

1. Split a document into overlapping text chunks.
2. Embed each chunk into a vector.
3. Store the chunks + vectors in a Postgres table with a `vector` column.
4. At query time, embed the question and pull the nearest chunks by cosine distance.

`rag.py` implements all four steps with a single embedding function you can swap out (OpenAI, BGE-M3, or any model that returns a fixed-size float vector).

## When to use it

- You have a document (or a small corpus) and need grounded, citeable answers instead of relying on model memory.
- You want the simplest possible RAG loop before adding a framework (LangChain, LlamaIndex) on top — understanding this ~80-line version makes every framework's abstractions easier to read.
- You already run Postgres and don't want a separate vector database.

## The gotcha it solves

**Naive chunking breaks retrieval before the LLM ever sees a bad answer.** Two mistakes show up constantly in first-pass RAG code:

- **Chunking with no overlap** — cuts sentences in half at chunk boundaries, so the fact you need ends up split across two chunks and neither one retrieves well.
- **No chunk metadata** — once you retrieve a chunk, you can't tell the user (or the model) which page/section it came from, so you can't cite it.

This skeleton chunks with overlap and keeps `(source, chunk_index)` metadata on every row, so retrieval results are traceable back to their origin — the minimum needed for an answer you can actually cite.

## How to run

This is an **illustrative skeleton**, not a package — read `rag.py` top to bottom, then adapt it into your project.

```bash
pip install psycopg2-binary numpy
# Postgres must have the pgvector extension installed:
#   CREATE EXTENSION IF NOT EXISTS vector;

export DATABASE_URL="postgresql://user:pass@localhost:5432/ragdb"
python rag.py
```

`rag.py` includes a `fake_embed()` placeholder so the script runs without any API key — swap it for a real embedding call (OpenAI `text-embedding-3-small`, a local BGE-M3 model, etc.) before using this for anything real.

## What's simplified here (not production-hardened)

- No retry/backoff on embedding calls.
- No batching — chunks are embedded one at a time.
- No re-ranking step after retrieval.
- Single-tenant: no `tenant_id` column or row-level security (see a multi-tenant RLS pattern if you need isolation between customers).
