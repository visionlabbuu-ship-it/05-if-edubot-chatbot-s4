"""Quick demo: ask the RAG chatbot several questions and print answers."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.rag import RagEngine


QUESTIONS = [
    "MG400 payload และ working radius เท่าไร?",
    "MG400 ใช้ port อะไรบ้างสำหรับ TCP/IP และ Modbus?",
    "EnableRobot command ทำอะไร?",
    "What is MG400?",
    "ก่อนสั่ง MovJ ต้องตรวจอะไรบ้าง?",
]


def main() -> int:
    engine = RagEngine()
    print(f"chunks: {engine.chunk_count}")
    print(f"ollama: {engine.ollama_available()}")
    print()

    for i, question in enumerate(QUESTIONS, 1):
        print("=" * 72)
        print(f"Q{i}: {question}")
        print("-" * 72)
        result = engine.ask(question)
        print(result["answer"])
        print()
        print("Top sources:")
        for chunk in result["chunks"][:3]:
            dist = chunk.get("distance")
            dist_s = f"{dist:.3f}" if isinstance(dist, (int, float)) else str(dist)
            print(f"  - {chunk['citation']} (dist={dist_s})")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
