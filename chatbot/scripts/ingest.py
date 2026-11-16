"""Ingest preprocessed chunks into a local Chroma vector store."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from tqdm import tqdm

from config import settings


def load_chunks(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest chunks into ChromaDB")
    parser.add_argument("--reset", action="store_true", help="Drop and recreate collection")
    parser.add_argument("--batch-size", type=int, default=32)
    args = parser.parse_args()

    if not settings.CHUNKS_PATH.exists():
        print(f"Missing chunks file: {settings.CHUNKS_PATH}")
        print("Run: python scripts/preprocess.py")
        return 1

    chunks = load_chunks(settings.CHUNKS_PATH)
    if not chunks:
        print("No chunks to ingest.")
        return 1

    settings.CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Embedding model: {settings.EMBEDDING_MODEL}")
    ef = SentenceTransformerEmbeddingFunction(
        model_name=settings.EMBEDDING_MODEL,
    )

    client = chromadb.PersistentClient(path=str(settings.CHROMA_DIR))
    if args.reset:
        try:
            client.delete_collection(settings.COLLECTION_NAME)
            print(f"Deleted collection: {settings.COLLECTION_NAME}")
        except Exception:  # noqa: BLE001
            pass

    collection = client.get_or_create_collection(
        name=settings.COLLECTION_NAME,
        embedding_function=ef,
        metadata={"hnsw:space": "cosine"},
    )

    # Clear existing ids if re-ingesting without full delete
    existing = collection.count()
    if existing and not args.reset:
        print(f"Collection already has {existing} items. Use --reset to rebuild.")
        # still allow append of missing? For simplicity rebuild when not empty without reset
        print("Rebuilding collection for a clean index...")
        client.delete_collection(settings.COLLECTION_NAME)
        collection = client.get_or_create_collection(
            name=settings.COLLECTION_NAME,
            embedding_function=ef,
            metadata={"hnsw:space": "cosine"},
        )

    batch_size = args.batch_size
    for i in tqdm(range(0, len(chunks), batch_size), desc="ingest"):
        batch = chunks[i : i + batch_size]
        ids = [c["id"] for c in batch]
        documents = [c["text"] for c in batch]
        metadatas = []
        for c in batch:
            md = {
                "doc_title": str(c.get("doc_title") or ""),
                "doc_type": str(c.get("doc_type") or ""),
                "source_path": str(c.get("source_path") or ""),
                "robot_model": str(c.get("robot_model") or "mg400"),
                "axis_family": str(c.get("axis_family") or "4-axis"),
                "applicability": str(c.get("applicability") or ""),
                "priority": str(c.get("priority") or ""),
                "safety_level": str(c.get("safety_level") or "normal"),
                "source_type": str(c.get("source_type") or ""),
                "doc_version": str(c.get("doc_version") or ""),
                "language": str(c.get("language") or ""),
                "section": str(c.get("section") or ""),
                "page": str(c.get("page") if c.get("page") is not None else ""),
                "code_related": str(bool(c.get("code_related", False))),
            }
            # Chroma metadata values must be str/int/float/bool
            metadatas.append(md)
        collection.upsert(ids=ids, documents=documents, metadatas=metadatas)

    print(f"Ingested {collection.count()} chunks into {settings.CHROMA_DIR}")
    print(f"Collection: {settings.COLLECTION_NAME}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
