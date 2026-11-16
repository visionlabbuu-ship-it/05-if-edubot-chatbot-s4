# Research Round 1 Summary

หัวข้อ: ผู้ช่วยอัจฉริยะเพื่อการเรียนรู้และพัฒนาโครงงานด้วย Dobot/MG400 ผ่าน LLM/Chatbot
วันที่สรุป: 2026-07-09

## สรุปภาพรวม

รอบนี้สั่ง sub-agent 4 สายไปเก็บข้อมูลแยกกัน และได้ข้อมูลครบสำหรับเริ่มออกแบบ corpus และ RAG architecture แล้ว

1. Official manuals/downloads: ได้รายการเอกสารทางการของ Dobot MG400 จาก product page, Download Center, FAQ และ version compatibility
2. TCP/IP API & SDK: ได้ repo official GitHub สำหรับ MG400/M1Pro 4-axis โดยตรง รวม Python SDK, API guide, alarm files และ command category
3. Demo/use cases: ได้ชุด demo/training guide และหัวข้อโครงงานที่เหมาะกับผู้เรียนหลายระดับ
4. RAG implementation: ได้แนวทางใช้ Dify เป็นตัวหลัก พร้อม chunking, metadata, citation, evaluation และข้อจำกัด

## ข้อสรุปหลัก

เลือก Dify เป็นตัวหลักสำหรับทำ chatbot/RAG เพราะเหมาะกับงานนี้ที่สุดในเชิงระบบสำเร็จรูป: Knowledge Base, Workflow/Agent, API, citation, metadata, retrieval testing และ deploy/self-host ได้

ใช้ RAGFlow เป็นตัวช่วยทดสอบ ingestion ถ้า PDF ของ Dobot มีตาราง/diagram/scanned pages แล้ว Dify extract ไม่ดีพอ

AnythingLLM เหมาะทำ prototype local เร็วๆ ส่วน Flowise เหมาะถ้าต้องการโชว์หรือสอน pipeline แบบ node graph

## แหล่งข้อมูลหลักที่ได้

### Dobot Official

- MG400 product page: https://www.dobot-robots.com/products/desktop-four-axis/mg400.html
- Dobot Download Center: https://www.dobot-robots.com/service/download-center
- Dobot FAQ: https://www.dobot-robots.com/service/faq
- Version compatibility: https://www.dobot-robots.com/insights/news/versions.html
- Dobot Academy: https://www.dobot-robots.com/service/academy

### Dobot Official GitHub

- Dobot-Arm org: https://github.com/Dobot-Arm
- TCP-IP-Protocol-4AXis: https://github.com/Dobot-Arm/TCP-IP-Protocol-4AXis
- TCP-IP-4Axis-Python: https://github.com/Dobot-Arm/TCP-IP-4Axis-Python
- TCP-IP-4Axis-CPP: https://github.com/Dobot-Arm/TCP-IP-4Axis-CPP
- TCP-IP-4Axis-CSharp: https://github.com/Dobot-Arm/TCP-IP-4Axis-CSharp
- MG400_ROS: https://github.com/Dobot-Arm/MG400_ROS

### RAG / LLM Platform

- Dify GitHub: https://github.com/langgenius/dify
- Dify Docs: https://docs.dify.ai/
- RAGFlow GitHub: https://github.com/infiniflow/ragflow
- AnythingLLM GitHub: https://github.com/Mintplex-Labs/anything-llm
- Flowise GitHub: https://github.com/FlowiseAI/Flowise

## ข้อมูล Dobot/MG400 ที่ควรเก็บเข้า RAG

### Priority สูง

- Dobot MG400 User Guide, Nov 16, 2023
- DOBOT MG400 Hardware User Guide, Apr 11, 2023
- DobotStudio Pro 2.8 User Guide (MG400 & M1Pro), Apr 1, 2024
- Dobot CRStudio APP User Guide (MG400 & M1 Pro) V4.13.0 / V2.14.0, Apr 1, 2024
- TCP_IP Remote Control Interface Guide (4axis), Apr 24, 2024 / file date 20240419
- SDK / official GitHub TCP-IP-4Axis-Python
- DobotStudio Pro 2.8 V2.8.3.0 for Win64, Dec 17, 2024
- FAQ เฉพาะ MG400: network ports, encoder, brakes, control box, fan, IP rating

### Priority กลาง

- Blockly User Guide (MG400 & M1 Pro)
- Lua Syntax Guide (MG400 & M1 Pro)
- MG400 Parameter Document
- 3D/CAD files: end flange, Creo model, SolidWorks model
- Training System User Guide และ Installation Guide
- Demo guides: Standard Conveyor, Palletizing, Dynamic Palletizing, Vision Palletizing, Mobile Phone Chip Sorting
- MG400_ROS ถ้ามี use case ROS

### Priority ต่ำ / อ้างอิงเสริม

- Leaflet/brochure
- คู่มือเก่า เช่น Hardware User Guide V1.1 ปี 2021
- CR/Nova/6-axis docs ใช้เป็น reference_only เท่านั้น ห้ามใช้ตอบ MG400 โดยตรง
- แหล่ง reseller/tutorial/video ภายนอก ใช้เป็น non-primary

## ข้อมูล API/SDK ที่ได้

แหล่ง canonical สำหรับ API คือ `TCP-IP-Protocol-4AXis` และ `TCP-IP-4Axis-Python` เพราะตรงกับ MG400/M1Pro 4-axis

Command/API category ที่ chatbot ต้องรู้:

- Network/connection: IP, subnet, TCP/IP mode, ports 29999/30003/30004
- Dashboard/control: EnableRobot, DisableRobot, ClearError, ResetRobot, RobotMode, SpeedFactor, GetPose, GetAngle, GetErrorID
- Motion: MovJ, MovL, JointMovJ, RelMovJ, RelMovL, MoveJog, Arc, Circle, Sync
- Speed/path: AccJ, AccL, SpeedJ, SpeedL, Arch, CP, LimZ
- I/O/Modbus: DO, DI, ToolDO, ToolDI, ModbusCreate, GetHoldRegs, SetHoldRegs
- Feedback/state: robot_mode, program_state, safety_status, q_actual, tool_vector_actual, ErrorStatus, EnableStatus, RunningStatus
- Error/alarm: alarm_controller.json, alarm_servo.json, error_id mapping

## Demo/use cases ที่ได้

เหมาะนำไปทำ corpus สำหรับ project-based learning:

- Pick-and-place แบบ drag-to-teach
- Palletizing grid 3x3 / 4x4
- Conveyor pick-and-place พร้อม sensor trigger
- Dashboard ตรวจสถานะ robot ผ่าน TCP/IP
- Sorting ตามสี/ตำแหน่งด้วย vision
- Dynamic palletizing จาก conveyor
- Vision palletizing
- Mobile phone chip sorting / quality inspection
- Digital twin/simulation + real robot deployment
- LLM chatbot ที่ช่วยสร้าง workflow, code template และ safety checklist

## RAG Architecture ที่แนะนำ

- Platform: Dify self-host หรือ Dify Cloud
- Knowledge Base: High Quality index
- Retrieval: Hybrid Search + rerank สำหรับ production
- Chunking: Parent-child สำหรับ manual/procedure, 1 chunk ต่อ 1 command สำหรับ API docs
- Citation: เปิด Citation and Attribution ทุกคำตอบ
- Metadata: บังคับใช้ metadata ตั้งแต่แรกเพื่อแยก MG400/4-axis ออกจาก M1Pro/CR/Nova
- Safety: ใช้ system prompt ห้ามเดาค่า speed, payload, coordinate, command syntax และให้ตอบจาก retrieved context เท่านั้น

## Metadata ที่ควรใช้

- source_type: official_product_page, official_manual, official_download_center, official_github, official_faq, official_case, non_primary
- robot_model: mg400, m1pro, cr, nova
- axis_family: 4-axis, 6-axis
- doc_type: manual, api_reference, sdk_code, safety, troubleshooting, error_code, demo_guide, faq, cad
- doc_title
- doc_version
- publish_date / effective_date
- source_url
- language
- section
- page_start / page_end
- api_category
- command_name
- safety_level: normal, caution, warning, critical
- applicability: direct_mg400, mg400_m1pro, cr_nova_only, reference_only
- priority: high, medium, low

## สิ่งที่ยังต้องทำต่อ

1. ดาวน์โหลดไฟล์จริงจาก Dobot Download Center และ official GitHub
2. แปลง PDF/manual/API guide เป็น Markdown หรือ structured text สำหรับ chunking
3. แยก corpus เป็นชุด: manuals, software guides, api_sdk, demo_projects, faq_troubleshooting, safety, cad_reference
4. สร้าง metadata CSV/JSON สำหรับทุกไฟล์
5. ทดลอง ingest เข้า Dify และทดสอบ retrieval ด้วยคำถามประเมิน
6. ถ้า Dify extract ตาราง/API/error code ไม่ดี ให้ทดสอบ RAGFlow เฉพาะ parsing/retrieval

## คำถามทดสอบ RAG รอบแรก

- MG400 payload, maximum payload, working radius และ repeatability เท่าไร
- MG400 ใช้ port อะไรบ้างสำหรับ Modbus, dashboard, motion และ feedback
- TCP/IP 4-axis guide ใช้กับ MG400 ได้ไหม
- ถ้าจะเขียน Python เชื่อม MG400 แบบยังไม่สั่ง motion ต้องทำอย่างไร
- ก่อนสั่ง MovJ ต้องตรวจ safety อะไรบ้าง
- ถ้า robot มี error/alarm ต้องใช้ข้อมูลจากแหล่งไหนแก้ปัญหา
- แนะนำหัวข้อโครงงาน beginner/intermediate/advanced สำหรับ MG400
- ข้อมูล CR/Nova ใช้ตอบ MG400 ได้หรือไม่ และต้อง tag อย่างไร
