# Dobot MG400 LLM/RAG Project

This is the standalone IF-EDUBOT S4 Chatbot/RAG repository. It is separate from
the ARC runtime and does not directly control a robot. See
[the repository guide](docs/REPOSITORY_GUIDE.md) and
[evaluation limits](docs/EVALUATION_AND_LIMITS.md).

หัวข้อ: ผู้ช่วยอัจฉริยะเพื่อการเรียนรู้และพัฒนาโครงงานด้วย Dobot/MG400 ผ่าน LLM/Chatbot

## สถานะปัจจุบัน (2026-07-14)

มี **local RAG chatbot prototype พร้อมใช้** ในโฟลเดอร์ `chatbot/`

- Knowledge Base (default **tight**): **~1,079 chunks / 46 เอกสาร**
  - ตัด noise: case HTML, alarms, C++/C#/ROS, PDF เสีย/scan, chapter ซ้ำ
  - เก็บ: User Guide, Studio/CRStudio, TCP+Python, demos+Lua, FAQ(scrub), curated cards
  - Full corpus ยังใช้ได้ด้วย `python scripts/preprocess.py --full`
- Vector store: ChromaDB + intent re-rank
- Embedding: `paraphrase-multilingual-MiniLM-L12-v2` (ไทย/อังกฤษ)
- LLM: Ollama `llama3.2` (fallback extractive + citation)
- UI: Streamlit

### เปิด chatbot

```powershell
cd chatbot
.\start_chatbot.ps1
```

หรือทีละขั้น:

```powershell
cd chatbot
.\.venv\Scripts\Activate.ps1
python scripts/preprocess.py
python scripts/ingest.py --reset
streamlit run app/streamlit_app.py
```

เปิดเบราว์เซอร์ที่ `http://localhost:8501`

## แผน platform (ระยะยาว)

- ใช้ **Dify** เป็นแพลตฟอร์มหลักเมื่อ Docker Desktop พร้อม (Knowledge Base + Workflow/Agent + API)
- ใช้ **RAGFlow** เป็นตัวเลือกสำรองถ้า PDF ตาราง/สแกนยาก
- ใช้ local prototype นี้สำหรับพัฒนา/ทดลอง corpus และ safety prompt ก่อน

## โครงสร้างโปรเจกต์

- `chatbot/` — local RAG chatbot (preprocess, ingest, Streamlit UI)
- `corpus/` — approved source corpus is supplied locally and is intentionally excluded from this GitHub preparation copy
- `rag_plan/open_source_rag_options.md` — เปรียบเทียบ RAG open source
- `sources/dobot_mg400_sources.md` — แหล่งข้อมูล Dobot/MG400
- `notes/rag_data_inventory.md` — ประเภทข้อมูลและ metadata
- `DATA_COLLECTION_AND_INGEST_PLAN.md` — แผน ingest
- `RESEARCH_ROUND_1_SUMMARY.md` — สรุปวิจัยรอบ 1

วันที่จัดทำ: 2026-07-09 · อัปเดต chatbot prototype: 2026-07-14
