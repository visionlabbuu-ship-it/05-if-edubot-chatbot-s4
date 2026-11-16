"""Score retrieval quality for tight vs full corpus (no LLM required)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.rag import RagEngine

# question -> any of these tokens should appear in top citations/doc_types/text
CASES = [
    {
        "q": "MG400 payload และ working radius เท่าไร?",
        "want_any": ["500", "440", "payload", "reach", "working radius", "spec", "user guide", "product"],
        "prefer_types": ["datasheet", "manual", "cheat_sheet", "faq"],
    },
    {
        "q": "MG400 ใช้ port อะไรบ้างสำหรับ dashboard motion feedback?",
        "want_any": ["29999", "30003", "30004", "dashboard", "port"],
        "prefer_types": ["cheat_sheet", "api_reference", "faq", "sdk_code"],
    },
    {
        "q": "ก่อนสั่ง MovJ ต้องตรวจ safety อะไรบ้าง?",
        "want_any": ["safety", "checklist", "e-stop", "workspace", "enable", "movj", "guard"],
        "prefer_types": ["cheat_sheet", "manual"],
    },
    {
        "q": "วิธีเริ่มใช้ DobotStudio Pro กับ MG400",
        "want_any": ["studio", "dobotstudio", "project", "connect", "teach"],
        "prefer_types": ["software_manual", "manual"],
    },
    {
        "q": "ตัวอย่างโครงงาน palletizing กับ MG400",
        "want_any": ["pallet", "palletizing", "demo", "training"],
        "prefer_types": ["demo_guide", "demo_script"],
    },
    {
        "q": "เขียน Python เชื่อม TCP แบบยังไม่สั่ง motion",
        "want_any": ["python", "dobot_api", "29999", "skeleton", "dashboard", "tcp"],
        "prefer_types": ["cheat_sheet", "sdk_code", "api_reference"],
    },
    {
        "q": "EnableRobot command ทำอะไร?",
        "want_any": ["enablerobot", "enable", "dashboard", "29999", "robot"],
        "prefer_types": ["api_reference", "sdk_code", "cheat_sheet"],
    },
    {
        "q": "TCP/IP 4-axis guide ใช้กับ MG400 ได้ไหม?",
        "want_any": ["4-axis", "4axis", "mg400", "tcp", "m1"],
        "prefer_types": ["api_reference", "sdk_code", "manual", "cheat_sheet"],
    },
]


def score_case(engine: RagEngine, case: dict, top_k: int = 5) -> dict:
    chunks = engine.retrieve(case["q"], top_k=top_k)
    parts: list[str] = []
    for c in chunks:
        parts.append(str(c.metadata.get("doc_title") or ""))
        parts.append(str(c.metadata.get("doc_type") or ""))
        parts.append((c.text or "")[:1200])
    blob = " ".join(parts).lower()
    types = [c.metadata.get("doc_type") for c in chunks]
    titles = [c.metadata.get("doc_title") for c in chunks]

    hits = [w for w in case["want_any"] if w.lower() in blob]
    type_hit = any(t in case.get("prefer_types", []) for t in types)
    # noise: case_study / error_code when not wanted
    noise = sum(1 for t in types if t in {"case_study", "error_code"})
    ok = len(hits) >= 1 and type_hit
    return {
        "question": case["q"],
        "ok": ok,
        "hits": hits,
        "type_hit": type_hit,
        "noise_chunks": noise,
        "types": types,
        "titles": titles,
        "top_dist": chunks[0].distance if chunks else None,
    }


def main() -> int:
    engine = RagEngine()
    print(f"chunks={engine.chunk_count}")
    stamp_path = Path(__file__).resolve().parents[1] / "data" / "processed" / "ingest_mode.json"
    if stamp_path.exists():
        print("mode_stamp=", stamp_path.read_text(encoding="utf-8"))

    results = [score_case(engine, c) for c in CASES]
    passed = sum(1 for r in results if r["ok"])
    noise = sum(r["noise_chunks"] for r in results)
    print(f"\nPASS {passed}/{len(results)}  noise_chunks_in_top={noise}")
    for r in results:
        flag = "OK" if r["ok"] else "FAIL"
        print(f"\n[{flag}] {r['question']}")
        print(f"  hits={r['hits']} type_hit={r['type_hit']} noise={r['noise_chunks']}")
        for t, title in zip(r["types"], r["titles"]):
            print(f"  - [{t}] {title}")

    out = Path(__file__).resolve().parents[1] / "data" / "processed" / "eval_quality.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWrote {out}")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
