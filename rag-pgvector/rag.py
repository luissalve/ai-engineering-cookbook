"""
rag.py — illustrative skeleton: chunk -> embed -> store -> retrieve over pgvector.

Not production-hardened. No retries, no batching, no auth. Swap `embed()` for a
real embedding model before using this against real traffic.

Setup:
    CREATE EXTENSION IF NOT EXISTS vector;
    CREATE TABLE IF NOT EXISTS chunks (
        id SERIAL PRIMARY KEY,
        source TEXT NOT NULL,
        chunk_index INT NOT NULL,
        content TEXT NOT NULL,
        embedding VECTOR(8)   -- dimension must match your embedding model
    );
"""

import os
import re

import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://user:pass@localhost:5432/ragdb")

CHUNK_SIZE = 400      # characters per chunk
CHUNK_OVERLAP = 80    # characters shared between consecutive chunks
EMBED_DIM = 8          # keep tiny for this skeleton; a real model is 384-3072 dims


def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into overlapping chunks so a fact near a boundary isn't lost."""
    text = re.sub(r"\s+", " ", text).strip()
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start = end - overlap
    return [c for c in chunks if c]


def fake_embed(text: str) -> list[float]:
    """
    Placeholder embedding: deterministic hash -> fixed-size float vector.
    Replace with a real call, e.g.:
        openai.embeddings.create(model="text-embedding-3-small", input=text)
        or a local BGE-M3 / sentence-transformers model.
    """
    seed = sum(ord(c) for c in text)
    return [((seed * (i + 1)) % 997) / 997.0 for i in range(EMBED_DIM)]


def store_chunks(conn, source: str, chunks: list[str], embed_fn=fake_embed) -> None:
    with conn.cursor() as cur:
        for i, chunk in enumerate(chunks):
            vector = embed_fn(chunk)
            cur.execute(
                """
                INSERT INTO chunks (source, chunk_index, content, embedding)
                VALUES (%s, %s, %s, %s)
                """,
                (source, i, chunk, vector),
            )
    conn.commit()


def retrieve(conn, query: str, top_k: int = 3, embed_fn=fake_embed) -> list[dict]:
    """Return the top_k chunks nearest the query embedding by cosine distance."""
    query_vector = embed_fn(query)
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT source, chunk_index, content, embedding <=> %s::vector AS distance
            FROM chunks
            ORDER BY distance ASC
            LIMIT %s
            """,
            (query_vector, top_k),
        )
        rows = cur.fetchall()
    return [
        {"source": r[0], "chunk_index": r[1], "content": r[2], "distance": r[3]}
        for r in rows
    ]


def main() -> None:
    conn = psycopg2.connect(DATABASE_URL)

    sample_doc = (
        "NovAIFlow builds production AI systems: voice agents, multi-agent "
        "orchestration, and retrieval-augmented generation over pgvector. "
        "Each pattern is designed to be small, self-contained, and honest "
        "about what it does not yet handle."
    )

    chunks = chunk_text(sample_doc)
    store_chunks(conn, source="sample_doc.txt", chunks=chunks)

    results = retrieve(conn, query="What does NovAIFlow build?", top_k=2)
    for r in results:
        print(f"[{r['source']}#{r['chunk_index']}] (distance={r['distance']:.4f})")
        print(f"  {r['content']}\n")

    conn.close()


if __name__ == "__main__":
    main()
