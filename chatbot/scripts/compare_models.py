"""A/B compare Ollama models on the same MG400 RAG questions."""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.rag import RagEngine
from config import settings

DEFAULT_QUESTIONS = [
    "MG400 ใช้พอร์ต TCP อะไรบ้างสำหรับ Dashboard และ Feedback?",
    "MG400 payload และ working radius เท่าไร?",
    "ก่อนสั่ง MovJ ต้องตรวจ safety อะไรบ้าง?",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare Ollama models on RAG questions")
    parser.add_argument(
        "--models",
        default="qwen3.5:9b,qwen3:14b",
        help="Comma-separated Ollama model tags",
    )
    parser.add_argument("--top-k", type=int, default=4)
    args = parser.parse_args()
    models = [m.strip() for m in args.models.split(",") if m.strip()]

    engine = RagEngine()
    print(f"collection={settings.COLLECTION_NAME} chunks={engine.chunk_count}")
    print(f"embedding={settings.EMBEDDING_MODEL}")
    installed = engine.list_ollama_models()
    print(f"installed={installed}")
    print()

    for q in DEFAULT_QUESTIONS:
        print("=" * 72)
        print(f"Q: {q}")
        chunks = engine.retrieve(q, top_k=args.top_k)
        print("Sources:")
        for ch in chunks:
            d = ch.distance
            ds = f"{d:.3f}" if isinstance(d, (int, float)) else str(d)
            print(f"  - {ch.citation} (dist={ds})")
        print()

        for model in models:
            ok, msg = engine.ollama_available(model)
            print("-" * 72)
            print(f"MODEL: {model}  ({msg})")
            if not ok:
                print("SKIP: model not available")
                continue
            t0 = time.perf_counter()
            answer = engine.generate(q, chunks, model=model, think=False)
            dt = time.perf_counter() - t0
            print(f"time: {dt:.1f}s")
            print(answer[:1500])
            if len(answer) > 1500:
                print("...[truncated]...")
            print()
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
