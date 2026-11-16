# RAG Data Inventory for Dobot MG400 Chatbot

## ประเภทข้อมูลที่ต้องใช้

### A. Product/spec knowledge
ข้อมูลที่ต้องเก็บ:

- จำนวนแกน, payload, reach, repeatability
- range of motion, joint speed, weight, base size
- power, rated voltage, environment, communication interface
- drag-to-teach, collision detection, programming options

ใช้ตอบ:

- MG400 ทำอะไรได้บ้าง
- เหมาะกับ project แบบไหน
- ข้อจำกัดด้าน payload/reach/workspace คืออะไร

### B. Hardware/User Manual
ข้อมูลที่ต้องเก็บ:

- installation
- commissioning
- maintenance
- safety warnings
- I/O และ interface
- troubleshooting เบื้องต้น

ใช้ตอบ:

- เริ่มใช้งานเครื่องอย่างไร
- ต้องเช็คอะไรก่อนเปิดเครื่อง
- ดูแลรักษาและแก้ปัญหาเบื้องต้นอย่างไร

### C. Software operation
ข้อมูลที่ต้องเก็บ:

- DobotStudio Pro 2.8 guide
- CRStudio app guide สำหรับ MG400 & M1 Pro
- jog, teach point, project management
- Blockly/graphical programming
- Lua/script programming
- import/export project

ใช้ตอบ:

- วิธีสร้างโปรแกรมแรก
- วิธีตั้งจุดหยิบวาง
- วิธีสอน Blockly/Lua สำหรับผู้เรียน

### D. TCP/IP API and SDK
ข้อมูลที่ต้องเก็บ:

- TCP/IP 4-axis guide
- command list, parameter, return format
- dashboard/motion/feedback/error interfaces
- SDK demos: Python, C++, C#, Java, ROS, MATLAB, LabVIEW, Android
- network setup: IP, TCP/IP mode, port ที่เกี่ยวข้อง

ใช้ตอบ:

- เขียน Python ควบคุม MG400 อย่างไร
- คำสั่ง MovJ/MovL/DO/DI ใช้อย่างไร
- อ่านสถานะ/feedback/error อย่างไร

### E. Safety and guardrails
ข้อมูลที่ต้องเก็บ:

- emergency stop
- collision detection
- payload/speed/workspace limits
- safe start checklist
- safe code generation rules
- ห้ามรันคำสั่งจริงเมื่อไม่ทราบตำแหน่ง robot/end-effector/workpiece

ใช้ตอบ:

- checklist ก่อนรันโปรแกรม
- วิธีลดความเสี่ยง collision
- ทำให้ chatbot ไม่แนะนำ action อันตราย

### F. Project examples
ข้อมูลที่ต้องเก็บ:

- conveyor demo
- palletizing demo
- dynamic palletizing
- vision palletizing
- mobile phone chip sorting
- pick-and-place examples

ใช้ตอบ:

- แนะนำหัวข้อโครงงาน
- แตกงานเป็น hardware/software/data steps
- สร้าง lesson plan สำหรับนักเรียน/นักศึกษา

### G. Integration data
ข้อมูลที่ต้องเก็บ:

- digital input/output
- analog input/output ถ้ามีในเอกสาร
- Modbus TCP
- end-effector/gripper/suction cup
- camera/vision kit
- conveyor/encoder
- CAD/end flange/mounting

ใช้ตอบ:

- ต่อ sensor/gripper อย่างไร
- ออกแบบ end-effector อย่างไร
- เชื่อม conveyor/vision กับ MG400 อย่างไร

### H. Troubleshooting and FAQ
ข้อมูลที่ต้องเก็บ:

- network connection issues
- port occupied/DobotLink issue
- TCP/IP mode not enabled
- emergency stop/power down/error state
- calibration/home/auto-identification
- software compatibility

ใช้ตอบ:

- แก้ปัญหาเชื่อมต่อไม่ได้
- โปรแกรมรันไม่ได้เพราะ robot mode/error state
- ตรวจ version และเลือกคู่มือให้ตรง

## Metadata ที่ควรติดกับทุก chunk

- source_type: official_product_page / official_manual / official_download_center / official_github / reseller_doc / user_note
- product: MG400 / M1 Pro / CR / Nova / generic
- axis_family: 4-axis / 6-axis / unknown
- document_title
- version
- publish_date
- source_url
- language
- page_number หรือ section
- safety_critical: true/false
- code_related: true/false

## Retrieval policy ที่แนะนำ

- คำถาม safety/API/control command: ใช้เฉพาะ official source ก่อน
- ถ้ามีคำตอบจากเอกสาร CR/Nova และ MG400 ขัดกัน ให้เลือก MG400/4-axis
- ถ้าจะสร้าง code ให้ตอบพร้อม assumption, test mode, speed ต่ำ, safety checklist และไม่สั่งให้รันบน robot จริงทันที
- ให้ chatbot แสดง citation ทุกครั้งเมื่อเป็นข้อมูลสเปก, safety, wiring, API หรือ troubleshooting

## ชุดคำถามทดสอบหลัง ingest

- MG400 payload และ working radius เท่าไร
- จะเริ่มใช้งาน DobotStudio Pro กับ MG400 ต้องทำอะไรบ้าง
- TCP/IP 4-axis guide ใช้กับ MG400 ได้ไหม และต่างจาก CR/Nova อย่างไร
- ช่วยเขียน Python skeleton สำหรับเชื่อมต่อ MG400 แบบไม่สั่ง motion จริง
- ก่อนสั่ง MovJ ต้องตรวจ safety อะไรบ้าง
- ถ้าเชื่อมต่อ TCP/IP ไม่ได้ควรตรวจอะไร
- ช่วยเสนอหัวข้อโครงงาน pick-and-place ด้วย MG400 สำหรับนักศึกษา
