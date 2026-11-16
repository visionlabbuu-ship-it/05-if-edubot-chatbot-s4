"""Run evaluation questions against the local RAG index."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.rag import RagEngine

DEFAULT_QUESTIONS = [
    "MG400 payload และ working radius เท่าไร?",
    "MG400 ใช้ port อะไรบ้างสำหรับ dashboard, motion และ feedback?",
    "TCP/IP 4-axis guide ใช้กับ MG400 ได้ไหม?",
    "ก่อนสั่ง MovJ ต้องตรวจ safety อะไรบ้าง?",
    "ช่วยเขียน Python skeleton เชื่อม MG400 แบบยังไม่สั่ง motion",
    "What is MG400?",
    "EnableRobot command ทำอะไร?",
    "ถ้า robot มี error/alarm ต้องดูไฟล์อะไร?",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--no-llm", action="store_true", help="Only show retrieval snippets")
    parser.add_argument("--out", type=str, default="")
    args = parser.parse_args()

    engine = RagEngine()
    print(f"Chunks in index: {engine.chunk_count}")
    if engine.chunk_count == 0:
        print("Empty index. Run preprocess + ingest first.")
        return 1

    ok, msg = engine.ollama_available()
    print(f"Ollama: {msg}")

    results = []
    for q in DEFAULT_QUESTIONS:
        print("\n" + "=" * 72)
        print(f"Q: {q}")
        chunks = engine.retrieve(q, top_k=args.top_k)
        print(f"Retrieved: {len(chunks)}")
        for i, ch in enumerate(chunks, 1):
            print(f"  {i}. {ch.citation}  dist={ch.distance}")
        if args.no_llm:
            answer = engine._fallback_extractive(q, chunks, reason="--no-llm")
        else:
            answer = engine.generate(q, chunks)
        print("-" * 40)
        print(answer[:2000])
        results.append(
            {
                "question": q,
                "answer": answer,
                "citations": [c.citation for c in chunks],
                "distances": [c.distance for c in chunks],
            }
        )

    if args.out:
        out = Path(args.out)
        out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
