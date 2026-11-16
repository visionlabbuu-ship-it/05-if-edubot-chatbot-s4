# Data Collection and Ingest Plan

## เป้าหมาย

เตรียมข้อมูลสำหรับสร้าง RAG chatbot ที่ช่วยเรียนรู้และพัฒนาโครงงาน Dobot MG400 โดยเน้นความถูกต้องจาก official sources, แยก version/model ชัดเจน และลดความเสี่ยงจากคำตอบผิดด้าน safety/API

## โครงสร้าง corpus ที่แนะนำ

### 01_manuals_high_priority

ไฟล์ที่ต้องเก็บ:

- Dobot MG400 User Guide, Nov 16, 2023
- DOBOT MG400 Hardware User Guide, Apr 11, 2023
- DobotStudio Pro 2.8 User Guide (MG400 & M1Pro), Apr 1, 2024
- Dobot CRStudio APP User Guide (MG400 & M1 Pro), Apr 1, 2024

ใช้ตอบ:

- installation
- maintenance
- safety
- commissioning
- teach point
- jog
- Blockly/Lua/script workflow

Chunking:

- ใช้ parent-child chunking
- แยกตาม section/procedure
- รักษาตารางและ warning/caution ให้อยู่ใน chunk เดียวกันเท่าที่ทำได้

### 02_api_sdk_high_priority

ไฟล์/Repo ที่ต้องเก็บ:

- https://github.com/Dobot-Arm/TCP-IP-Protocol-4AXis
- https://github.com/Dobot-Arm/TCP-IP-4Axis-Python
- `TCP_IP Remote Control Interface Guide (4axis)_20240419_en.pdf`
- `dobot_api.py`
- `README-EN.md`
- `PythonExample.py`
- `main.py`
- `files/alarm_controller.json`
- `files/alarm_servo.json`

ใช้ตอบ:

- Python control skeleton
- command syntax
- port mapping
- robot feedback/state
- error/alarm explanation
- safe code generation

Chunking:

- PDF API guide: 1 chunk ต่อ 1 command
- code: 1 chunk ต่อ class/function
- alarm JSON: 1 chunk ต่อ alarm/error id
- examples: 1 chunk ต่อ workflow

### 03_demo_project_learning

ไฟล์ที่ต้องเก็บ:

- MG400 Training System Installation Guide
- Standard Conveyor Demo Guide
- Palletizing Demo Guide
- Dynamic Palletizing Demo Guide
- Vision Palletizing Demo Guide
- Mobile Phone Chip Sorting Demo Guide
- MG400 Training System User Guide

ใช้ตอบ:

- แนะนำหัวข้อโครงงาน
- สร้าง workflow/pseudocode
- ระบุ equipment/prerequisites
- troubleshooting สำหรับ lab
- rubric/assessment

Chunking:

- แยกตาม demo
- แยก hardware setup, software workflow, pseudocode, safety, troubleshooting

### 04_faq_troubleshooting

แหล่งที่ต้องเก็บ:

- https://www.dobot-robots.com/service/faq/479.html
- https://www.dobot-robots.com/service/faq/482.html
- https://www.dobot-robots.com/service/faq/483.html
- https://www.dobot-robots.com/service/faq/484.html
- https://www.dobot-robots.com/service/faq/485.html
- https://www.dobot-robots.com/service/faq/486.html
- https://www.dobot-robots.com/service/faq/487.html
- https://www.dobot-robots.com/service/faq/what-is-mg400.html

ใช้ตอบ:

- network ports
- encoder/conveyor tracking
- brake/control box/fan/IP rating
- beginner overview

Chunking:

- 1 FAQ ต่อ 1 chunk
- tag topic และ priority

### 05_cad_reference

ไฟล์ที่ต้องเก็บ:

- DOBOT MG400_End_Flange_3D
- DOBOT MG400 Model (Creo4.0)
- DOBOT MG400 Model (SolidWorks2014)
- MG400 Parameter Document

ใช้ตอบ:

- end-effector design
- mounting
- workspace planning
- simulation/digital twin

Chunking:

- ถ้าไฟล์ CAD ingest ตรงไม่ได้ ให้ทำ metadata และ text summary จาก dimension/parameter docs

## Dify setup ที่แนะนำ

1. ใช้ Dify เป็นตัวหลัก
2. สร้าง Knowledge Base แบบ High Quality
3. เปิด Hybrid Search
4. เปิด rerank เมื่อต้องการ production accuracy
5. เปิด Citation and Attribution ใน chatbot app
6. ใช้ metadata filter แยก `robot_model`, `axis_family`, `doc_type`, `safety_level`, `applicability`
7. ใช้ prompt บังคับตอบจาก context และไม่เดาข้อมูล safety/API

## Evaluation gate ก่อนถือว่า corpus ใช้งานได้

ผ่านเมื่อ:

- คำถาม spec ตอบถูกและอ้าง official source
- คำถาม API ดึง command/port ถูกจาก 4-axis docs ไม่ปน CR/Nova
- คำถาม safety มี warning และ citation
- คำถามที่ไม่มีในเอกสาร ระบบตอบว่าไม่พบ ไม่ hallucinate
- โค้ดตัวอย่าง default เป็น read-only หรือ dry-run ก่อน motion
- retrieval ไม่ดึงเอกสารเก่าเป็นคำตอบหลักเมื่อมีเอกสารใหม่กว่า

## Risk register

| Risk | ผลกระทบ | วิธีควบคุม |
|---|---|---|
| PDF extraction พังจากตาราง/diagram | ตอบ API/safety ผิด | แปลงเป็น Markdown/structured text, preview chunk, ใช้ RAGFlow ทดสอบ |
| เอกสาร MG400 ปน CR/Nova | command/safety ผิดรุ่น | metadata `axis_family`, `applicability`, filter ใน prompt/workflow |
| LLM เดาค่า coordinate/speed | เสี่ยงต่อ robot จริง | safety prompt, dry-run default, human confirmation |
| version ปนกัน | คำตอบไม่ตรง software/firmware | metadata `doc_version`, `publish_date`, priority ล่าสุด |
| ภาษาไทยถามเอกสารอังกฤษ | retrieval พลาด | ใช้ multilingual embedding และชุดคำถามทดสอบไทย/อังกฤษ |
| Dify license | ติดเงื่อนไขเชิงพาณิชย์ | ตรวจ Dify Open Source License ก่อนใช้งานจริง |

## Next action checklist

- [ ] ดาวน์โหลดไฟล์ official manual/API/demo จาก Dobot
- [ ] clone หรือดาวน์โหลด official GitHub repos ที่เกี่ยวข้อง
- [ ] สร้าง metadata sheet สำหรับทุกไฟล์
- [ ] แปลง PDF เป็น Markdown/text และตรวจตารางสำคัญ
- [ ] ingest ชุด high priority เข้า Dify
- [ ] ทดสอบ retrieval ด้วย evaluation questions
- [ ] ปรับ chunking/metadata/rerank
- [ ] ตัดสินใจว่าจะใช้ RAGFlow ช่วย parse PDF หรือไม่
