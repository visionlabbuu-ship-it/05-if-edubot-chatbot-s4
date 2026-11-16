"""Run ~50 use-case questions through RAG, write CSV + quality scores."""
from __future__ import annotations

import csv
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.rag import RagEngine

# category, question_th, expected_keywords (any hit helps), prefer_doc_types
CASES: list[dict] = [
    # --- A. Product / specs (1-8) ---
    {"id": 1, "cat": "spec", "q": "MG400 คืออะไร?", "kw": ["4", "desktop", "mg400", "robot", "compact", "แกน"], "types": ["manual", "faq", "datasheet", "cheat_sheet"]},
    {"id": 2, "cat": "spec", "q": "MG400 payload หรือน้ำหนักบรรทุกสูงสุดเท่าไร?", "kw": ["500", "750", "g", "payload", "load"], "types": ["manual", "datasheet", "faq", "cheat_sheet"]},
    {"id": 3, "cat": "spec", "q": "working radius หรือระยะเอื้อมของ MG400 เท่าไร?", "kw": ["440", "mm", "reach", "radius"], "types": ["manual", "datasheet", "cheat_sheet"]},
    {"id": 4, "cat": "spec", "q": "repeatability ของ MG400 เท่าไร?", "kw": ["0.05", "±", "repeat"], "types": ["manual", "datasheet", "cheat_sheet"]},
    {"id": 5, "cat": "spec", "q": "ขนาด base ของ MG400 กี่มิลลิเมตร?", "kw": ["190", "base"], "types": ["manual", "faq", "datasheet"]},
    {"id": 6, "cat": "spec", "q": "MG400 ได้มาตรฐาน IP ระดับไหน?", "kw": ["ip20", "ip 20", "20"], "types": ["faq", "manual"]},
    {"id": 7, "cat": "spec", "q": "MG400 ใช้มอเตอร์แบบ stepper หรือ servo?", "kw": ["servo"], "types": ["faq", "manual"]},
    {"id": 8, "cat": "spec", "q": "MG400 ต่างจาก Magician Pro อย่างไรคร่าวๆ?", "kw": ["magician", "mg400", "desktop", "industrial", "collaborative"], "types": ["faq", "manual", "case_study"]},
    # --- B. Safety (9-14) ---
    {"id": 9, "cat": "safety", "q": "ก่อนสั่ง MovJ ต้องตรวจ safety อะไรบ้าง?", "kw": ["safety", "workspace", "e-stop", "speed", "checklist", "โล่ง", "ความเร็ว"], "types": ["cheat_sheet", "manual"]},
    {"id": 10, "cat": "safety", "q": "ทำไมไม่ควรให้คนเข้าใกล้หุ่นตอนกำลังทำงาน?", "kw": ["safety", "range", "guard", "reach", "personnel", "อย่า", "ระยะ"], "types": ["manual", "cheat_sheet"]},
    {"id": 11, "cat": "safety", "q": "ก่อน EnableRobot ควรเตรียมอะไร?", "kw": ["enable", "error", "workspace", "tcp", "safety", "clear"], "types": ["cheat_sheet", "manual", "api_reference"]},
    {"id": 12, "cat": "safety", "q": "ถ้าจะรันโปรแกรมครั้งแรก ควรตั้งความเร็วอย่างไร?", "kw": ["low", "speed", "ช้า", "ต่ำ", "first", "reduce"], "types": ["cheat_sheet", "manual"]},
    {"id": 13, "cat": "safety", "q": "payload เกินสเปกแล้วอันตรายอย่างไร / ควรทำอย่างไร?", "kw": ["payload", "500", "load", "limit", "ไม่ควร", "within"], "types": ["manual", "cheat_sheet", "datasheet"]},
    {"id": 14, "cat": "safety", "q": "checklist ความปลอดภัยสั้นๆ ก่อนแล็บ MG400", "kw": ["e-stop", "workspace", "safety", "speed", "supervision", "checklist"], "types": ["cheat_sheet", "manual"]},
    # --- C. Network / ports (15-20) ---
    {"id": 15, "cat": "network", "q": "MG400 ใช้ TCP port อะไรสำหรับ dashboard motion และ feedback?", "kw": ["29999", "30003", "30004"], "types": ["cheat_sheet", "api_reference", "sdk_code"]},
    {"id": 16, "cat": "network", "q": "port 29999 ใช้ทำอะไร?", "kw": ["29999", "dashboard"], "types": ["cheat_sheet", "api_reference", "sdk_code"]},
    {"id": 17, "cat": "network", "q": "port 30003 ใช้ทำอะไร?", "kw": ["30003", "motion", "move", "mov"], "types": ["cheat_sheet", "api_reference"]},
    {"id": 18, "cat": "network", "q": "LAN1 และ LAN2 ของ MG400 IP default คืออะไร?", "kw": ["192.168.1.6", "192.168.2.6", "lan1", "lan2"], "types": ["faq", "cheat_sheet", "manual"]},
    {"id": 19, "cat": "network", "q": "port 502 บน MG400 ใช้ทำอะไร ห้ามทำอะไร?", "kw": ["502", "modbus"], "types": ["faq", "cheat_sheet"]},
    {"id": 20, "cat": "network", "q": "ถ้าเชื่อม TCP/IP ไม่ได้ ควรตรวจอะไรบ้าง?", "kw": ["ip", "lan", "tcp", "cable", "mode", "network", "ping", "port"], "types": ["cheat_sheet", "faq", "manual", "sdk_code"]},
    # --- D. TCP API / Python (21-30) ---
    {"id": 21, "cat": "python_api", "q": "ช่วยเขียน Python skeleton เชื่อม MG400 แบบยังไม่สั่ง motion", "kw": ["29999", "python", "dashboard", "connect", "dobot", "ip"], "types": ["cheat_sheet", "sdk_code", "api_reference"]},
    {"id": 22, "cat": "python_api", "q": "EnableRobot command ทำอะไร?", "kw": ["enable", "robot", "dashboard"], "types": ["api_reference", "sdk_code", "manual", "cheat_sheet"]},
    {"id": 23, "cat": "python_api", "q": "MovJ กับ MovL ต่างกันอย่างไรคร่าวๆ?", "kw": ["movj", "movl", "joint", "linear", "path", "joint"], "types": ["api_reference", "sdk_code", "software_manual"]},
    {"id": 24, "cat": "python_api", "q": "TCP/IP 4-axis guide ใช้กับ MG400 ได้ไหม?", "kw": ["4-axis", "4axis", "mg400", "tcp", "m1"], "types": ["api_reference", "sdk_code", "cheat_sheet"]},
    {"id": 25, "cat": "python_api", "q": "dobot_api.py มีคลาสหลักอะไรบ้างสำหรับควบคุม?", "kw": ["dashboard", "move", "feed", "dobot"], "types": ["sdk_code", "cheat_sheet"]},
    {"id": 26, "cat": "python_api", "q": "ลำดับการเชื่อมต่อ TCP ที่แนะนำก่อนสั่งเคลื่อนที่คืออะไร?", "kw": ["dashboard", "29999", "error", "enable", "connect", "status"], "types": ["cheat_sheet", "api_reference", "sdk_code"]},
    {"id": 27, "cat": "python_api", "q": "ClearError ใช้ตอนไหน?", "kw": ["clear", "error", "alarm", "fault"], "types": ["api_reference", "sdk_code", "manual"]},
    {"id": 28, "cat": "python_api", "q": "อ่านสถานะหุ่นหรือ feedback ผ่าน TCP ได้อย่างไร?", "kw": ["feedback", "30004", "status", "mode", "feed"], "types": ["api_reference", "sdk_code", "cheat_sheet"]},
    {"id": 29, "cat": "python_api", "q": "ตัวอย่าง Python อย่างเป็นทางการอยู่ไฟล์ไหน?", "kw": ["pythonexample", "dobot_api", "example", "readme"], "types": ["sdk_code", "cheat_sheet"]},
    {"id": 30, "cat": "python_api", "q": "นักศึกษาควรรัน motion จากโค้ดครั้งแรกอย่างไรให้ปลอดภัย?", "kw": ["low", "speed", "dry", "safety", "supervision", "ไม่", "connect"], "types": ["cheat_sheet", "manual"]},
    # --- E. Studio / software (31-36) ---
    {"id": 31, "cat": "studio", "q": "วิธีเริ่มใช้ DobotStudio Pro กับ MG400 คร่าวๆ", "kw": ["studio", "connect", "project", "dobotstudio", "software"], "types": ["software_manual", "manual"]},
    {"id": 32, "cat": "studio", "q": "CRStudio ใช้ทำอะไรกับ MG400?", "kw": ["crstudio", "app", "control", "mg400", "studio"], "types": ["software_manual", "manual"]},
    {"id": 33, "cat": "studio", "q": "ใน Studio สามารถโปรแกรมแบบไหนได้บ้าง เช่น graphical หรือ script?", "kw": ["blockly", "graphical", "lua", "script", "program", "teach"], "types": ["software_manual", "manual", "cheat_sheet"]},
    {"id": 34, "cat": "studio", "q": "drag-to-teach หรือ hand guiding บน MG400 ใช้ทำอะไร?", "kw": ["teach", "drag", "hand", "guide", "point"], "types": ["manual", "software_manual", "faq"]},
    {"id": 35, "cat": "studio", "q": "ก่อนเชื่อม Studio กับหุ่น ควรเช็ค network อะไร?", "kw": ["ip", "lan", "network", "connect", "192.168"], "types": ["manual", "software_manual", "faq", "cheat_sheet"]},
    {"id": 36, "cat": "studio", "q": "DobotStudio Pro กับ CRStudio ต่างกันอย่างไรในภาพรวม?", "kw": ["studio", "crstudio", "pc", "app", "software"], "types": ["software_manual", "manual"]},
    # --- F. Demo / projects (37-44) ---
    {"id": 37, "cat": "demo", "q": "ตัวอย่างโครงงาน palletizing กับ MG400 มีอะไรบ้าง?", "kw": ["pallet", "demo", "training"], "types": ["demo_guide", "demo_script"]},
    {"id": 38, "cat": "demo", "q": "dynamic palletizing ต่างจาก palletizing ธรรมดาอย่างไรคร่าวๆ?", "kw": ["dynamic", "pallet", "conveyor", "moving"], "types": ["demo_guide"]},
    {"id": 39, "cat": "demo", "q": "vision palletizing ใช้วิชันช่วยอะไร?", "kw": ["vision", "camera", "pallet", "detect", "image"], "types": ["demo_guide"]},
    {"id": 40, "cat": "demo", "q": "demo สายพาน conveyor กับ MG400 เกี่ยวกับอะไร?", "kw": ["conveyor", "belt", "sensor", "standard"], "types": ["demo_guide", "demo_script"]},
    {"id": 41, "cat": "demo", "q": "mobile phone chip sorting demo ทำอะไร?", "kw": ["chip", "sort", "phone", "sorting"], "types": ["demo_guide", "demo_script"]},
    {"id": 42, "cat": "demo", "q": "ถ้านักศึกษาจะเลือกโครง pick-and-place ง่าย ควรเริ่มจาก demo ไหน?", "kw": ["pallet", "conveyor", "pick", "demo", "training"], "types": ["demo_guide", "manual", "cheat_sheet"]},
    {"id": 43, "cat": "demo", "q": "training system installation ควรดูเอกสารไหน?", "kw": ["install", "training", "guide"], "types": ["demo_guide"]},
    {"id": 44, "cat": "demo", "q": "ใน training มีสคริปต์ Lua ตัวอย่างเรื่องอะไรบ้าง?", "kw": ["lua", "pallet", "conveyor", "led", "trajectory", "script"], "types": ["demo_script", "demo_guide"]},
    # --- G. Hardware FAQ / ops (45-48) ---
    {"id": 45, "cat": "hardware", "q": "MG400 มี control box แยกไหม?", "kw": ["all-in-one", "base", "controller", "integrated", "control box"], "types": ["faq", "manual"]},
    {"id": 46, "cat": "hardware", "q": "MG400 มีเบรก (brakes) ไหม?", "kw": ["brake", "brakes"], "types": ["faq", "manual"]},
    {"id": 47, "cat": "hardware", "q": "พัดลมระบายความร้อนที่ฐาน MG400 ทำหน้าที่อะไร?", "kw": ["fan", "cool", "base", "heat"], "types": ["faq", "manual"]},
    {"id": 48, "cat": "hardware", "q": "ENC interface หรือ encoder บน MG400 ใช้ทำอะไร?", "kw": ["enc", "encoder", "interface"], "types": ["faq", "manual"]},
    # --- H. Teaching / pedagogy (49-50) ---
    {"id": 49, "cat": "teaching", "q": "ออกแบบลำดับเรียน MG400 3 ครั้งแล็บสำหรับนักศึกษาวิศวกรรม ควรมีหัวข้ออะไร?", "kw": ["safety", "studio", "tcp", "python", "demo", "connect"], "types": ["cheat_sheet", "manual", "demo_guide", "software_manual"]},
    {"id": 50, "cat": "teaching", "q": "คำถามที่นักศึกษาควรถามตัวเองก่อนรันโค้ดสั่งหุ่นจริงมีอะไรบ้าง?", "kw": ["safety", "workspace", "speed", "coordinate", "payload", "supervision"], "types": ["cheat_sheet", "manual"]},
]


def score_row(
    case: dict,
    answer: str,
    chunks: list[dict],
) -> dict:
    ans_l = (answer or "").lower()
    blob = ans_l
    types: list[str] = []
    titles: list[str] = []
    for c in chunks:
        md = c.get("metadata") or {}
        types.append(str(md.get("doc_type") or ""))
        titles.append(str(md.get("doc_title") or ""))
        blob += " " + str(md.get("doc_title") or "").lower()
        blob += " " + str(c.get("text") or "")[:800].lower()

    kw_hits = [k for k in case["kw"] if k.lower() in blob]
    type_hit = any(t in case["types"] for t in types)
    noise = sum(1 for t in types if t in {"case_study", "error_code"})

    # Refusal / empty
    weak_phrases = [
        "ไม่พบข้อมูล",
        "not found",
        "no retrieved",
        "ไม่มีในเอกสาร",
        "cannot find",
    ]
    is_weak = any(p in ans_l for p in weak_phrases) or len((answer or "").strip()) < 40

    # Grounding: answer mentions something from keywords or citations present
    has_sources = "source" in ans_l or bool(titles)
    invent_risk = 0
    # Heuristic: if answer asserts a number not in blob context of top chunks text
    # (light check only for common false ports)
    if re.search(r"\b3000[0-2]\b|\b2999[0-8]\b", answer or "") and not any(
        x in blob for x in ["30000", "30001", "30002", "29998"]
    ):
        invent_risk = 1

    # Score 0-5
    score = 0
    if type_hit:
        score += 1
    if len(kw_hits) >= 1:
        score += 1
    if len(kw_hits) >= 2:
        score += 1
    if not is_weak and len((answer or "").strip()) >= 80:
        score += 1
    if has_sources and noise == 0:
        score += 1
    if invent_risk:
        score = max(0, score - 2)
    if is_weak:
        score = min(score, 2)

    if score >= 4:
        grade = "good"
    elif score == 3:
        grade = "ok"
    elif score == 2:
        grade = "weak"
    else:
        grade = "poor"

    notes = []
    if not type_hit:
        notes.append("doc_type ไม่ตรงกลุ่มที่คาด")
    if len(kw_hits) == 0:
        notes.append("ไม่เจอ keyword สำคัญในคำตอบ/context")
    if is_weak:
        notes.append("คำตอบสั้นหรือปฏิเสธ")
    if noise:
        notes.append(f"noise types={noise}")
    if invent_risk:
        notes.append("สงสัยตัวเลขพอร์ตผิด")
    if not notes:
        notes.append("ผ่านเกณฑ์อัตโนมัติ")

    return {
        "kw_hits": "|".join(kw_hits),
        "type_hit": type_hit,
        "noise": noise,
        "score_0_5": score,
        "grade": grade,
        "auto_notes": "; ".join(notes),
        "top_types": "|".join(types[:5]),
        "top_titles": " || ".join(titles[:5]),
    }


def main() -> int:
    out_dir = Path(__file__).resolve().parents[1] / "data" / "processed"
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "usecase_eval_50.csv"
    json_path = out_dir / "usecase_eval_50.json"
    summary_path = out_dir / "usecase_eval_50_summary.md"

    engine = RagEngine()
    ok_ollama, ollama_msg = engine.ollama_available()
    print(f"chunks={engine.chunk_count}")
    print(f"ollama={ok_ollama} {ollama_msg}")
    print(f"cases={len(CASES)}")

    rows: list[dict] = []
    t0 = time.time()

    for i, case in enumerate(CASES, 1):
        q = case["q"]
        print(f"[{i}/{len(CASES)}] {case['cat']}: {q[:60]}...")
        t1 = time.time()
        try:
            result = engine.ask(q, top_k=5)
            answer = result.get("answer") or ""
            chunks = result.get("chunks") or []
        except Exception as exc:  # noqa: BLE001
            answer = f"[ERROR] {exc}"
            chunks = []
        elapsed = round(time.time() - t1, 2)
        scored = score_row(case, answer, chunks)
        cites = " | ".join(
            (c.get("citation") or c.get("metadata", {}).get("doc_title") or "")
            for c in chunks[:5]
        )
        dists = " | ".join(
            f"{c.get('distance'):.3f}" if isinstance(c.get("distance"), (int, float)) else ""
            for c in chunks[:5]
        )
        row = {
            "id": case["id"],
            "category": case["cat"],
            "question": q,
            "answer": answer,
            "citations": cites,
            "distances": dists,
            "seconds": elapsed,
            "llm_used": ok_ollama and not answer.startswith("### คำตอบแบบ Extractive"),
            **scored,
        }
        rows.append(row)
        print(f"  -> grade={row['grade']} score={row['score_0_5']} ({elapsed}s)")

    # Write CSV
    fieldnames = [
        "id",
        "category",
        "question",
        "answer",
        "citations",
        "distances",
        "kw_hits",
        "type_hit",
        "noise",
        "score_0_5",
        "grade",
        "auto_notes",
        "top_types",
        "top_titles",
        "seconds",
        "llm_used",
    ]
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)

    json_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    # Summary
    n = len(rows)
    by_grade: dict[str, int] = {}
    by_cat: dict[str, list[int]] = {}
    for r in rows:
        by_grade[r["grade"]] = by_grade.get(r["grade"], 0) + 1
        by_cat.setdefault(r["category"], []).append(r["score_0_5"])

    avg = sum(r["score_0_5"] for r in rows) / n if n else 0
    good_ok = sum(1 for r in rows if r["grade"] in {"good", "ok"})
    weak_poor = [r for r in rows if r["grade"] in {"weak", "poor"}]

    lines = [
        "# Use-case evaluation (50 questions)",
        "",
        f"- Chunks in index: {engine.chunk_count}",
        f"- Ollama: {ollama_msg}",
        f"- Total time: {round(time.time() - t0, 1)}s",
        f"- Average score (0-5): **{avg:.2f}**",
        f"- good+ok: **{good_ok}/{n}** ({100 * good_ok / n:.0f}%)",
        f"- Grade counts: {by_grade}",
        "",
        "## By category (avg score)",
        "",
    ]
    for cat, scores in sorted(by_cat.items()):
        lines.append(f"- **{cat}**: {sum(scores)/len(scores):.2f} (n={len(scores)})")

    lines += ["", "## Weak / poor items", ""]
    if not weak_poor:
        lines.append("- (none)")
    else:
        for r in weak_poor:
            lines.append(
                f"- Q{r['id']} [{r['grade']}/{r['score_0_5']}] {r['question']} — {r['auto_notes']}"
            )

    lines += [
        "",
        "## Teaching readiness (auto)",
        "",
        "- ใช้เป็นผู้ช่วยสอน lab ได้ถ้า good+ok ≥ 70% และ safety/network/python ไม่ weak ยกชุด",
        f"- ผลรอบนี้ good+ok = {100 * good_ok / n:.0f}%",
        "",
        f"CSV: `{csv_path}`",
        f"JSON: `{json_path}`",
        "",
    ]
    summary_path.write_text("\n".join(lines), encoding="utf-8")

    print("\n" + "\n".join(lines))
    print(f"\nWrote:\n  {csv_path}\n  {json_path}\n  {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
