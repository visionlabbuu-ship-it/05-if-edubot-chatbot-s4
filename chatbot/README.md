# Dobot MG400 Local RAG Chatbot

Prototype chatbot สำหรับเรียนรู้/พัฒนาโครงงาน Dobot MG400  
ใช้ approved corpus ที่จัดเตรียมไว้ในเครื่อง + embedding ท้องถิ่น + (ถ้ามี) Ollama LLM

ชุด GitHub นี้ไม่รวม corpus ต้นฉบับหรือ ChromaDB ที่สร้างแล้ว ต้องกำหนดแหล่ง
เอกสารที่ได้รับอนุมัติบนเครื่องก่อนรัน preprocessing และ ingest

## สถาปัตยกรรม

```text
corpus/raw (full text-extractable set)
  → scripts/preprocess.py   # PDF/HTML/MD/code/JSON/Lua → chunks.jsonl
  → scripts/ingest.py       # ChromaDB + multilingual embeddings
  → app/streamlit_app.py    # Chat UI
  → Ollama (optional)       # สรุปคำตอบ; ถ้าไม่มีจะใช้ extractive mode
```

## เตรียมเครื่อง (ครั้งแรก)

1. Python 3.12+
2. GPU ที่แนะนำ: RTX 5070 Ti 16GB (หรือเทียบเท่า)
3. [Ollama](https://ollama.com) + โมเดล LLM แนะนำ:
   ```powershell
   ollama pull qwen3.5:9b   # default · เร็ว · รุ่นใหม่
   ollama pull qwen3:14b    # คุณภาพ / ทางเลือกใน sidebar
   ```
4. ติดตั้ง dependencies + ดึง embedding model:
   ```powershell
   cd chatbot
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   # pre-download HF embedding (ครั้งแรก)
   python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('Qwen/Qwen3-Embedding-0.6B')"
   ```
5. ตรวจ `.env` (ค่า default ชุดแนะนำอยู่แล้ว):
   - `OLLAMA_MODEL=qwen3.5:9b`
   - `EMBEDDING_MODEL=Qwen/Qwen3-Embedding-0.6B`
   - `CHROMA_COLLECTION=mg400_qwen3`

หรือรัน `.\scripts\install_models.ps1` เพื่อ pull LLM + warm embedding cache

ในหน้า Streamlit (sidebar) สามารถ **สลับโมเดล Ollama** ได้ทันทีโดยไม่ต้อง restart  
เปรียบเทียบ CLI: `python scripts/compare_models.py`

## สร้าง Knowledge Base

**Default = tight** (ตัด noise แล้ว แน่นกว่า full)

```powershell
cd chatbot
.\.venv\Scripts\Activate.ps1
python scripts/preprocess.py          # tight (แนะนำ)
python scripts/ingest.py --reset
```

ตัวเลือก preprocess:

| Flag | ความหมาย |
|------|----------|
| (default) / `--tight` | **แนะนำ** manuals + Studio + TCP + Python + demos + curated + FAQ(scrub) |
| `--full` | ชุดกว้าง: cases, C++/C#/ROS, alarms (ถ้า `--with-alarms`), chapters ซ้ำ |
| `--with-alarms` | ใส่ alarm JSON (ใช้ตอน debug error code) |
| `--core-only` | ชุดเล็กกว่า tight |
| `--dry-run` | แสดงรายการแหล่งข้อมูลอย่างเดียว |

ทดสอบคุณภาพ retrieval:

```powershell
python scripts/eval_retrieval_quality.py
```

## เปิด Chatbot

```powershell
cd chatbot
.\.venv\Scripts\Activate.ps1
streamlit run app\streamlit_app.py
```

หรือ `.\start_chatbot.ps1`  
เปิดเบราว์เซอร์ที่ URL ที่ Streamlit แสดง (ปกติ `http://localhost:8501`)

## ทดสอบ retrieval

```powershell
python scripts/evaluate.py --no-llm
python scripts/demo_ask.py
```

## ชุดเอกสารที่ ingest (tight — default)

**เก็บ**

- MG400 User Guide, DobotStudio Pro, CRStudio
- TCP/IP 4-axis guide + Python SDK (README, `dobot_api.py`, examples)
- Demo guides (dynamic/vision/conveyor/sorting/install) + Chapter2 palletizing + Lua
- FAQ หลัง scrub nav/footer
- Curated: product specs, TCP ports, safety checklist, Python skeleton

**ตัดออกจาก default (noise)**

- Case / marketing HTML
- Alarm JSON (~286 chunks เดิม) — เปิดด้วย `--with-alarms` ถ้าต้องการ
- C++ / C# / ROS trees
- Parameter PDF (scan ว่าง), palletizing PDF เสีย
- Training chapter PDFs ซ้ำ (เหลือ Ch2 + top-level demos)
- CAD / build / Chinese TCP duplicate

## ขนาด index (tight)

- ~46 แหล่ง → **~1,079 chunks** (full เดิม ~2,242)
- FAQ เหลือ ~10 chunks หลัง scrub (เดิม ~130)
- Collection: จาก `.env` (`CHROMA_COLLECTION`)

## Safety

- System prompt บังคับตอบจาก context + citation
- ไม่เดา payload/speed/coordinate/command
- โค้ด motion ควร dry-run / ความเร็วต่ำ และมีคนดูแล

## ขั้นถัดไป (optional)

- Hybrid search + rerank
- Intent-based metadata filter (ลด noise จาก alarm)
- OCR สำหรับ Parameter PDF / PDF เสีย
- Deploy Dify เมื่อ Docker Desktop พร้อม
