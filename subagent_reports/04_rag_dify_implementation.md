# Sub-Agent 4: RAG / Dify Implementation

## Dify docs ที่เกี่ยวข้อง

- Dify Knowledge: https://docs.dify.ai/en/cloud/use-dify/knowledge/readme
- Quick Create Knowledge: https://docs.dify.ai/en/cloud/use-dify/knowledge/create-knowledge/introduction
- Upload Local Files: https://docs.dify.ai/en/cloud/use-dify/knowledge/create-knowledge/import-text-data/readme
- Chunk Settings: https://docs.dify.ai/en/cloud/use-dify/knowledge/create-knowledge/chunking-and-cleaning-text
- Index/Retrieval Settings: https://docs.dify.ai/en/cloud/use-dify/knowledge/create-knowledge/setting-indexing-methods
- Metadata: https://docs.dify.ai/en/cloud/use-dify/knowledge/metadata
- Integrate Knowledge in Apps: https://docs.dify.ai/en/cloud/use-dify/knowledge/integrate-knowledge-within-application
- Test Retrieval: https://docs.dify.ai/en/cloud/use-dify/knowledge/test-retrieval
- Dify GitHub: https://github.com/langgenius/dify

## Dify capability ที่ใช้กับงานนี้

- Knowledge Base/RAG สำหรับ retrieve chunks และ generate answer
- หลาย knowledge bases ต่อ app
- document upload จาก local files, webpages, Notion หรือ API
- chunk mode: General และ Parent-child
- High Quality index, hybrid search, rerank
- metadata filter ใน chatbot/chatflow/workflow
- Citation and Attribution ใน app
- retrieval records และ test retrieval
- Docker Compose self-host

## เทียบ open source RAG

| ประเด็น | Dify | RAGFlow | AnythingLLM | Flowise |
|---|---|---|---|---|
| จุดแข็ง | app/workflow/RAG/API ครบ | document understanding/PDF/scanned docs | local-first ง่าย | visual low-code flow |
| PDF | ดีระดับทั่วไป | แข็งกว่าในเอกสารซับซ้อน | ใช้ง่าย | ต้องออกแบบ loader/splitter |
| Citation | เปิดใน app ได้ | traceable citations | source citations | ต้องออกแบบเองมากกว่า |
| Deploy | Docker Compose, RAM >= 4 GiB | Docker Compose, RAM >= 16 GB | Docker/self-host | Docker/npm, Node >= 20 |
| License | Dify Open Source License | Apache-2.0 | MIT | Apache-2.0 |
| บทบาท | ตัวหลัก | benchmark/backup PDF parsing | prototype local | custom flow/teaching |

## Architecture ที่แนะนำ

- Dify เป็น application layer: chatbot UI/API, workflow/chatflow, citation, monitoring/logs, feedback
- Knowledge Base: High Quality + Hybrid Search + rerank
- Chunking: Parent-child สำหรับ technical manual/procedure
- PDF/API table ที่ซับซ้อน: แปลงเป็น Markdown/structured text ก่อน ingest ถ้าจำเป็น
- เปิด Citation and Attribution ทุกคำตอบ
- ใช้ metadata filter ตาม robot_model, doc_type, safety_level, version, applicability

## Metadata policy

- robot_model: mg400
- doc_type: manual, api_reference, safety, troubleshooting, error_code, faq
- doc_version
- language
- source_url / source_file
- section
- safety_level: normal, caution, warning, critical
- validated: true/false
- effective_date
- page_start/page_end

## Safety prompt skeleton

```text
คุณเป็นผู้ช่วยด้าน Dobot MG400 ที่ตอบจากเอกสารที่ retrieve มาเท่านั้น
- ถ้าไม่มีข้อมูลใน context ให้ตอบว่าไม่พบข้อมูลในเอกสาร และเสนอหัวข้อที่ควรตรวจสอบ
- สำหรับคำสั่งที่เกี่ยวกับความปลอดภัย การเคลื่อนที่ calibration, payload, emergency stop ต้องให้คำเตือนและอ้างอิงแหล่งที่มา
- ห้ามเดาค่าพารามิเตอร์, torque, payload, speed, coordinate, command syntax
- ถ้าผู้ใช้ขอขั้นตอนปฏิบัติ ให้ตอบเป็นลำดับขั้น สั้น ชัด และระบุ precondition
- ถ้าคำถามเกี่ยวกับการ execute command จริง ให้แนะนำ simulation/low speed และยืนยันพื้นที่ปลอดภัยก่อน
- ทุกคำตอบต้องมี citation/source จาก Knowledge Base
```

## Evaluation questions

- MG400 payload สูงสุดเท่าไร และมีข้อจำกัดอะไร
- วิธี home หุ่นยนต์ MG400 ต้องทำอย่างไร
- ถ้า emergency stop ถูกกด ต้อง reset อย่างไร
- Alarm/error code X หมายถึงอะไร และแก้อย่างไร
- TCP/IP หรือ Modbus ตั้งค่ายังไง
- ห้ามทำอะไรขณะ robot arm กำลังเคลื่อนที่
- MG400 calibration ต้องทำเมื่อไหร่
- ถามคำถามที่ไม่มีในเอกสาร แล้วระบบตอบว่าไม่พบหรือ hallucinate

## Risks

- PDF extraction risk จากตาราง/diagram
- safety hallucination
- chunking ผิดจน procedure ขาด context
- metadata ไม่เข้มทำให้เอกสารเก่า/ใหม่ปนกัน
- Dify license ต้องตรวจสำหรับเชิงพาณิชย์
- rerank เพิ่ม latency/cost
- multilingual retrieval ต้องทดสอบเพราะผู้ใช้ถามไทยแต่เอกสารอังกฤษ

## Recommendation

ใช้ Dify เป็นตัวหลัก และใช้ RAGFlow เป็น benchmark/backup สำหรับ PDF parsing ถ้าตารางหรือ scanned pages ทำให้ retrieval คุณภาพต่ำ
