# Dobot MG400 Sources

## Official sources ที่ควรรวบรวมก่อน

### 1. MG400 product page
URL: https://www.dobot-robots.com/products/desktop-four-axis/mg400.html

ข้อมูลสำคัญ:

- MG400 เป็น desktop grade industrial collaborative robot แบบ 4 แกน
- payload 500 g และ maximum payload 750 g
- working radius 440 mm
- repeatability +-0.05 mm
- communication interface: TCP/IP, Modbus TCP
- มี drag-to-teach, collision detection, Lua และ graphical programming
- หน้าเดียวกันมีรายการ User Manual, Control Software, 3D Model, FAQ และ demo guides

ประโยชน์ต่อ RAG:

- ใช้เป็น source หลักสำหรับตอบภาพรวม สเปก ข้อจำกัด และ use case
- ใช้ทำ metadata product/spec ที่ chatbot ควรอ้างอิงเสมอ

### 2. Dobot Download Center
URL: https://www.dobot-robots.com/service/download-center

ข้อมูลสำคัญ:

- เป็น index ทางการสำหรับ manual, control software, secondary development, 3D model และไฟล์อื่นๆ
- ควรกรอง Product Model = MG400 และ Data Type ตามชนิดไฟล์

ประโยชน์ต่อ RAG:

- ใช้เป็นแหล่งค้นเวอร์ชันล่าสุดก่อนนำเอกสารเข้า knowledge base
- ใช้ตรวจว่าเอกสารไหนเป็นของ MG400/M1 Pro, CR/Nova หรือ Magician เพื่อไม่ปนกัน

### 3. Dobot MG400 User Guide
อยู่ใน Download Center และ product page

ข้อมูลสำคัญ:

- เอกสารวันที่ Nov 16, 2023
- อธิบาย functions, technical specifications, installation guide และ maintenance ของ MG400

ประโยชน์ต่อ RAG:

- เป็นเอกสารแกนหลักสำหรับผู้เรียน: ติดตั้ง ใช้งาน ดูแลรักษา ข้อควรระวัง และสเปก

### 4. DobotStudio Pro 2.8 User Guide (MG400 & M1 Pro)
อยู่ใน Download Center และ product page

ข้อมูลสำคัญ:

- เอกสารวันที่ Apr 1, 2024
- คู่มือ PC software V2.8 สำหรับ MG400 & M1 Pro

ประโยชน์ต่อ RAG:

- ใช้ตอบคำถามการเชื่อมต่อ robot, jog, teach point, Blockly/graphical programming, Lua/script และ project workflow

### 5. DobotStudio Pro 2.8 (V2.8.3.0) for Win64
อยู่ใน Download Center และ product page

ข้อมูลสำคัญ:

- วันที่ Dec 17, 2024
- ปรับปรุง Auto-identification สำหรับ MG400
- เพิ่ม safety checks ระหว่าง Auto-identification
- แจ้งเตือนเมื่อ DobotLink port ถูกใช้งาน

ประโยชน์ต่อ RAG:

- ใช้ทำคำตอบ troubleshooting และ version awareness
- ให้ chatbot ตรวจ software version ก่อนแนะนำวิธีแก้ปัญหา

### 6. TCP_IP Remote Control Interface Guide (4axis)
Official Download Center: https://www.dobot-robots.com/service/download-center
GitHub: https://github.com/Dobot-Arm/TCP-IP-Protocol-4AXis

ข้อมูลสำคัญ:

- เอกสาร secondary development interface สำหรับ 4-axis robots
- GitHub repo ระบุ MG400/M1Pro โดยตรง
- มีไฟล์ TCP_IP Remote Control Interface Guide (4axis)_20240419_en.pdf

ประโยชน์ต่อ RAG:

- เป็น source หลักสำหรับตอบเรื่อง TCP/IP command, parameter, return format, port, motion command, I/O, error และ feedback
- ต้องแยกจากเอกสาร CR/Nova 6-axis อย่างชัดเจน

### 7. SDK (CR / MG400 / M1 Pro)
อยู่ใน Download Center

ข้อมูลสำคัญ:

- Suitable for secondary development ของ Dobot collaborative robot CR/MG400/M1Pro
- Based on TCP/IP protocol
- รองรับ Java, C++, C#, Python, ROS, MATLAB, LabVIEW, Android demo

ประโยชน์ต่อ RAG:

- ใช้สำหรับตอบเชิง coding และสร้างตัวอย่างโค้ด
- ใช้เตรียม use case หลายภาษา โดยเริ่มจาก Python ก่อน

### 8. Training System Demo Guides
อยู่ใน MG400 product page / Download Center

เอกสารที่ควรเก็บ:

- MG400 Training System Standard Conveyor Demo Guide
- MG400 Training System Mobile Phone Chip Sorting Demo Guide
- MG400 Training System Dynamic Palletizing Demo Guide
- MG400 Training System Vision Palletizing Demo Guide
- MG400 Training System Palletizing Demo Guide
- MG400 Training System Installation Guide

ประโยชน์ต่อ RAG:

- ใช้ให้ chatbot แนะนำ project idea และ workflow แบบ practical
- เหมาะสำหรับหัวข้อโครงงาน เช่น pick-and-place, sorting, conveyor, palletizing, vision integration

### 9. 3D/CAD/Dimension resources
อยู่ใน MG400 product page / Download Center

ข้อมูลที่ควรเก็บ:

- MG400 model
- end flange 3D/dimension
- base size, working range, mounting dimension

ประโยชน์ต่อ RAG:

- ใช้ตอบเรื่องออกแบบ end-effector, mounting, clearance, workspace, simulation และ collision planning

## แหล่งเสริมที่ใช้ได้แต่ต้อง tag เป็น non-primary

### Trossen Robotics TCP/IP protocol docs
URL: https://docs.trossenrobotics.com/dobot_cr_cobots_docs/tcpip_protocol/functions.html

ประโยชน์:

- HTML อ่านง่าย ค้น command ได้สะดวก
- ใช้เทียบ format หรือช่วยค้นเร็ว

ข้อควรระวัง:

- เป็นเอกสาร CR-Series ไม่ใช่ official MG400 โดยตรง
- สำหรับคำตอบ safety/API ของ MG400 ต้องยึด official 4-axis guide ก่อน

## ข้อควรระวังสำคัญ

- แยกเอกสาร 4-axis สำหรับ MG400/M1Pro ออกจากเอกสาร CR/Nova 6-axis
- เก็บ metadata ทุกไฟล์: product, document title, version, publish date, source URL, language, file type
- อย่าให้ chatbot สร้างคำสั่งควบคุม robot จริงโดยไม่มี safety checklist
- คำตอบเกี่ยวกับ motion/API ต้องระบุว่าให้ทดสอบใน simulation/mock หรือ speed ต่ำก่อนเสมอ
- ตรวจ firmware/software/controller version ก่อนตอบวิธีแก้ปัญหา
