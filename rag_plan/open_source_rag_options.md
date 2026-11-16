# Open Source RAG Options

## คำแนะนำหลัก: Dify

เหมาะที่สุดสำหรับหัวข้อนี้ เพราะเป็นแพลตฟอร์ม open-source สำหรับสร้าง LLM app ที่รวม AI workflow, RAG pipeline, agent capabilities, model management, observability และ API ไว้ในระบบเดียว จุดสำคัญคือทำ chatbot ที่ ingest manual/API แล้วเปิดให้ผู้เรียนใช้งานได้เร็ว โดยไม่ต้องสร้าง backend/frontend เองทั้งหมด

เหมาะกับงานนี้เพราะ:

- มี Knowledge Base/RAG pipeline สำหรับ PDF, PPT และเอกสารทั่วไป
- มี Workflow และ Agent สำหรับทำ use case เช่น ถามตอบคู่มือ, ช่วยเขียนโค้ด TCP/IP, สร้าง checklist ก่อนรัน robot
- รองรับ model หลายแบบ ทั้ง cloud LLM และ self-hosted/OpenAI-compatible model
- มี API สำหรับฝัง chatbot เข้าระบบเรียนรู้หรือเว็บภายใน
- Deploy ด้วย Docker Compose ได้ เหมาะกับ prototype และต่อยอด production

ข้อควรระวัง:

- License เป็น Dify Open Source License based on Apache 2.0 with additional conditions ไม่ใช่ Apache 2.0 ล้วน ต้องอ่านเงื่อนไขก่อนใช้เชิงพาณิชย์
- ถ้าเอกสาร PDF มีตาราง/รูปเยอะมาก อาจต้องทดสอบคุณภาพ chunk/retrieval จริง

แหล่งอ้างอิง:
- https://github.com/langgenius/dify
- https://docs.dify.ai/

## ตัวเลือกที่ 2: RAGFlow

เหมาะถ้าเน้นคุณภาพ retrieval จากเอกสารเทคนิคที่ซับซ้อน เช่น PDF manual, ตาราง command, รูปภาพ, scanned copy หรือเอกสารหลายรูปแบบ จุดแข็งคือ deep document understanding, template-based chunking, citation และรองรับ data source หลากหลาย

เหมาะกับงานนี้เพราะ:

- ดีสำหรับ ingest คู่มือ/เอกสารเทคนิค Dobot ที่มีตาราง command, parameter และรูปประกอบ
- มี traceable citations ช่วยลด hallucination เมื่อ chatbot ตอบเรื่อง safety/API
- License Apache-2.0 ใช้งานยืดหยุ่นกว่า Dify ในบางบริบท

ข้อจำกัด:

- ถ้าต้องการทำ chatbot workflow/agent ครบทั้งระบบ อาจซับซ้อนกว่า Dify สำหรับทีมเริ่มต้น
- ควรใช้เมื่อพิสูจน์แล้วว่า Dify ตอบจาก PDF/manual ไม่ละเอียดพอ

แหล่งอ้างอิง:
- https://github.com/infiniflow/ragflow
- https://ragflow.io/

## ตัวเลือกที่ 3: AnythingLLM

เหมาะสำหรับ prototype แบบ local-first หรือ classroom demo ที่ต้องการ "ลากเอกสารแล้วคุยกับเอกสาร" เร็วที่สุด มี desktop app, document chat, agents, multi-user, vector database และ source citation

เหมาะกับงานนี้เพราะ:

- ตั้งค่าเร็ว เหมาะกับ demo และทดสอบชุดข้อมูล Dobot เบื้องต้น
- ใช้งาน local ได้ ลดความยุ่งยากเรื่อง server
- License MIT

ข้อจำกัด:

- ถ้าจะทำ workflow/agent เฉพาะทางหลายขั้นตอน อาจไม่ยืดหยุ่นเท่า Dify/Flowise
- เหมาะเป็นตัวทดลอง ไม่ใช่คำแนะนำหลักสำหรับระบบโครงงานที่ต้องออกแบบกระบวนการชัดเจน

แหล่งอ้างอิง:
- https://github.com/Mintplex-Labs/anything-llm
- https://anythingllm.com/

## ตัวเลือกที่ 4: Flowise

เหมาะถ้าต้องการสร้าง AI agent/RAG แบบ visual node และใช้สอน architecture ของ RAG/agent pipeline โดยตรง จุดแข็งคือเห็น graph/pipeline ชัดและปรับแต่ง chain ได้มาก

เหมาะกับงานนี้เพราะ:

- ใช้สอนแนวคิด retrieval, prompt, tools, agent, API call ได้ดี
- เหมาะกับการทดลองเชื่อม tool เช่น function สำหรับเรียก simulator หรือส่งคำสั่ง robot แบบ mock
- License Apache-2.0

ข้อจำกัด:

- ต้องออกแบบ flow เองมากกว่า Dify
- การจัดการ knowledge base/operations สำหรับผู้ใช้ทั่วไปอาจไม่สำเร็จรูปเท่า Dify

แหล่งอ้างอิง:
- https://github.com/FlowiseAI/Flowise
- https://flowiseai.com/

## สรุปเลือกใช้

เลือก Dify เป็น open source หลักสำหรับโครงงานนี้

เหตุผล: หัวข้อไม่ได้ต้องการแค่ RAG แต่ต้องการ "ผู้ช่วยอัจฉริยะ" ที่มี chatbot, workflow, agent, API และปรับ prompt/knowledge ได้ต่อเนื่อง Dify ครบที่สุดสำหรับทำต้นแบบและนำเสนอ ส่วน RAGFlow ควรเก็บไว้เป็นทางเลือกถ้าพบว่า ingestion PDF/manual ของ Dobot ต้องการความแม่นยำสูงกว่า
