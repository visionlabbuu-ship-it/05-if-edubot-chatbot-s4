# Sub-Agent 3: Demo Use Cases and Project Topics

## Official demo/training sources

| หมวด | เอกสาร/หน้า | ใช้กับ RAG เรื่อง | URL |
|---|---|---|---|
| Product overview | MG400 product page | สเปก, ข้อจำกัด, use case, software, API | https://www.dobot-robots.com/products/desktop-four-axis/mg400.html |
| Training system | MG400 Training System User Guide | ชุดฝึก, workflow, อุปกรณ์ | https://www.dobot-robots.com/service/download-center |
| Demo guide | MG400 Training System Installation Guide | installation, wiring, calibration | https://www.dobot-robots.com/service/download-center |
| Demo guide | Standard Conveyor Demo Guide | conveyor pick/place, timing, sensor/IO | https://www.dobot-robots.com/service/download-center |
| Demo guide | Palletizing Demo Guide | palletizing, pattern, coordinate | https://www.dobot-robots.com/service/download-center |
| Demo guide | Dynamic Palletizing Demo Guide | object/conveyor moving | https://www.dobot-robots.com/service/download-center |
| Demo guide | Vision Palletizing Demo Guide | camera/vision + palletizing | https://www.dobot-robots.com/service/download-center |
| Demo guide | Mobile Phone Chip Sorting Demo Guide | sorting / inspection / electronics use case | https://www.dobot-robots.com/service/download-center |

## Demo corpus ที่ควรใช้

| Demo | ระดับ | chatbot ควรสอนได้ | ข้อมูลที่ต้อง index |
|---|---|---|---|
| Standard Conveyor Demo | Beginner-Intermediate | หยิบจากสายพาน, sensor sync, timing | wiring, IO mapping, flowchart, speed, calibration, troubleshooting |
| Palletizing Demo | Beginner | วาง grid/pallet pattern | coordinate, teach point, pallet pattern, gripper, safe height, loop pseudocode |
| Dynamic Palletizing | Intermediate-Advanced | วางชิ้นงานที่เคลื่อนที่ | encoder/sensor trigger, offset, timing, queue, error handling |
| Vision Palletizing | Advanced | vision detect + robot placement | calibration, coordinate transform, confidence threshold |
| Mobile Phone Chip Sorting | Intermediate-Advanced | sorting / inspection | vision criteria, bin mapping, reject logic, pick order |
| Training System Installation | Foundation | ติดตั้งชุดฝึกก่อนทดลอง | BOM, layout, wiring, power/network, calibration checklist |

## ไอเดียโครงงาน

| Level | หัวข้อ | ต้องใช้ข้อมูล | อุปกรณ์ |
|---|---|---|---|
| Beginner | Pick-and-place drag-to-teach | MG400 User Guide, DobotStudio Pro Guide | MG400, gripper/suction, ชิ้นงาน |
| Beginner | Palletizing grid 3x3/4x4 | Palletizing Demo, Blockly/Lua | MG400, gripper, tray |
| Beginner | Chatbot ช่วยสร้าง pseudocode palletizing | software guide, Lua guide | PC + RAG |
| Intermediate | Conveyor pick-and-place พร้อม sensor | Conveyor Demo, IO section | MG400, conveyor, sensor, gripper |
| Intermediate | Sorting ด้วย vision | Vision guide, Sorting demo | camera/vision kit, lighting |
| Intermediate | Dashboard ตรวจสถานะ robot ผ่าน TCP/IP | TCP/IP guide, SDK | MG400, PC, network |
| Intermediate | Error recovery lab | User Guide, alarm/log section | MG400, safety setup |
| Advanced | Dynamic palletizing | Dynamic Palletizing, TCP/IP/Modbus | conveyor, sensor/encoder |
| Advanced | Vision palletizing แบบเลือก pattern | Vision Palletizing, SDK | camera, pallet, lighting |
| Advanced | LLM chatbot สร้าง workflow/code/safety checklist | manual + demo + API + SDK | RAG backend, Dobot docs |
| Advanced | Closed-loop quality inspection + sorting | Mobile Phone Chip Sorting | camera, tray/bin |
| Advanced | Digital twin/simulation + real robot | TCP/IP API, 3D model | PC, MG400, simulator |

## Data สำหรับ project-based chatbot

- hardware_setup
- robot_specs
- software_workflow
- programming
- demo_workflows
- pseudocode_templates
- coordinate_systems
- safety
- troubleshooting
- assessment rubric
- project_metadata: level, equipment, time, prerequisites, expected output, extension ideas

## แหล่งเสริม

- Dobot Academy: https://www.dobot-robots.com/service/academy
- Bristol Robotics Laboratory case study: https://www.dobot-robots.com/insights/case-studies/driving-innovation-at-bristol-robotics-laboratory.html
- Sabanci University case study: https://www.dobot-robots.com/insights/case-studies/sabanc-university.html
- Dobot Palletizing: https://www.dobot-robots.com/apply/palletizing.html
- Dobot Sorting: https://www.dobot-robots.com/applications/sorting.html

แหล่งภายนอกอื่นควร tag เป็น `non_primary` และใช้เป็นแรงบันดาลใจเท่านั้น ไม่ใช้แทน manual/API official
