# Sub-Agent 1: Official Manuals and Downloads

## แหล่งทางการหลัก

- MG400 product page: https://www.dobot-robots.com/products/desktop-four-axis/mg400.html
- Download Center: https://www.dobot-robots.com/service/download-center
- Version compatibility: https://www.dobot-robots.com/insights/news/versions.html
- FAQ: https://www.dobot-robots.com/service/faq

## รายการเอกสาร/ไฟล์ Official Dobot ที่ควรเข้า RAG

| ชื่อเอกสาร/ไฟล์ | ประเภทข้อมูล | วันที่/เวอร์ชัน | URL แหล่งที่มา | เหมาะเอาเข้า RAG เพื่ออะไร | Priority |
|---|---|---|---|---|---|
| Dobot MG400 User Guide | User manual หลัก | Nov 16, 2023 | MG400 product page / Download Center | ฟังก์ชัน, technical specs, installation, maintenance | สูง |
| Dobot MG400 User Guide | User manual เก่า | Sep 20, 2023 | MG400 product page | เทียบ revision เก่า ไม่ควรเป็นคำตอบหลัก | กลาง |
| DOBOT MG400 Hardware User Guide | Hardware manual | Apr 11, 2023 | MG400 product page | wiring, hardware setup, I/O, installation safety | สูง |
| DOBOT MG400 Hardware User Guide V1.1 | Hardware manual เก่า | Oct 8, 2021 | MG400 product page | legacy setup เฉพาะเครื่อง/ซอฟต์แวร์เก่า | ต่ำ |
| DobotStudio Pro 2.8 User Guide (MG400&M1Pro) | Software manual | Apr 1, 2024 | Download Center | Blockly, Script, points, IO, coordinate | สูง |
| Dobot CRStudio APP User Guide (MG400&M1 Pro) V4.13.0_V2.14.0 | Mobile app guide | Apr 1, 2024 | Download Center | ใช้งาน CRStudio app สำหรับ MG400/M1 Pro | สูง |
| DOBOT Blockly User Guide (MG400&M1 Pro) | Programming guide | Oct 8, 2021 | MG400 product page | block programming | กลาง |
| DOBOT Lua Syntax Guide (MG400&M1 Pro) | Programming guide | Jun 14, 2021 | MG400 product page | Lua/script programming | สูง |
| TCP_IP Remote Control Interface Guide (4axis) | Secondary development/API | Apr 24, 2024 | MG400 product page / Download Center | API/TCP remote control ของ 4-axis | สูง |
| SDK (CR / MG400 / M1 Pro) | SDK/examples | Apr 18, 2022 | MG400 product page / Download Center | Java/C++/C#/Python/ROS/MATLAB/LabVIEW/Android demo | สูง |
| DobotStudio Pro 2.8 (V2.8.3.0) for Win64 | Control software | Dec 17, 2024 | MG400 product page | software version ล่าสุดที่พบสำหรับ MG400 | สูง |
| Android APP CRStudio v4.13.0 | Mobile control software | Feb 25, 2024 | MG400 product page | ใช้คู่กับ CRStudio APP guide | สูง |
| DOBOT MG400_End_Flange_3D | 3D model | Nov 8, 2021 | MG400 product page | end-effector/flange/fixture | กลาง |
| DOBOT MG400 Model (Creo4.0) | CAD model | Nov 8, 2021 | MG400 product page | simulation/layout/mechanical integration | กลาง |
| DOBOT MG400 Model (SolidWorks2014) | CAD model | Nov 8, 2021 | MG400 product page | simulation/layout/mechanical integration | กลาง |
| MG400 Parameter Document | Parameter/spec sheet | Jul 28, 2022 | Download Center | quick reference specs/parameters | กลาง |
| MG400 Training System User Guide | Training system manual | Feb 6, 2023 | Download Center | training system workflow/equipment | กลาง |
| MG400 Training System Demo Guides | Demo guides | Jun 16, 2023 | Download Center | lab/demo/project-based learning | กลาง |

## FAQ Official Dobot ที่ควรเก็บ

| FAQ | URL | ใช้ตอบเรื่อง | Priority |
|---|---|---|---|
| Which network communication ports are available on the MG400? | https://www.dobot-robots.com/service/faq/479.html | Modbus port 502, Lua debugger port 8172, LAN default IP | สูง |
| Which type of encoder does the ENC interface of the MG400 support? | https://www.dobot-robots.com/service/faq/482.html | ABZ encoder / conveyor tracking | กลาง |
| Does the MG400 use stepper or servo motors? | https://www.dobot-robots.com/service/faq/483.html | motor type | กลาง |
| Does the MG400 have brakes? | https://www.dobot-robots.com/service/faq/484.html | brakes J2/J3, absolute encoders | สูง |
| Does the MG400 have a control box? | https://www.dobot-robots.com/service/faq/485.html | all-in-one controller/control box | กลาง |
| Is there a cooling fan in the base of the MG400? | https://www.dobot-robots.com/service/faq/486.html | fan/thermal behavior | ต่ำ |
| What is the IP rating of the MG400? | https://www.dobot-robots.com/service/faq/487.html | IP20 rating | กลาง |
| What is MG400? | https://www.dobot-robots.com/service/faq/what-is-mg400.html | beginner overview | กลาง |

## ข้อควรระวัง

- MG400/M1 Pro มักอยู่ในคู่มือเดียวกัน ต้อง tag metadata เป็น `model_scope: MG400,M1Pro`
- อย่านำคู่มือ CR/Nova/6-axis มาใช้ตอบ MG400 โดยตรง
- DobotStudio Pro V4.x ใน Download Center ไม่ใช่สายหลักของ MG400; MG400 ใช้ DobotStudio Pro 2.8 เป็นหลักตามหน้า product
- TCP_IP Remote Control Interface Guide (4axis) เหมาะกว่า 6-axis guide สำหรับ MG400
- เอกสารเก่าปี 2021 ควรเก็บพร้อม version/date ไม่ให้กลายเป็นคำตอบหลัก
