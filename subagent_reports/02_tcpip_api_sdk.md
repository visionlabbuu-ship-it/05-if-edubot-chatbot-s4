# Sub-Agent 2: TCP/IP API and SDK

## Official sources สำหรับ corpus หลัก

| แหล่งข้อมูล | URL | สถานะต่อ MG400/4-axis | หมายเหตุ |
|---|---|---|---|
| Dobot-Arm GitHub org | https://github.com/Dobot-Arm | Official | GitHub ของ Dobot |
| TCP-IP-Protocol-4AXis | https://github.com/Dobot-Arm/TCP-IP-Protocol-4AXis | ตรงกับ MG400/M1Pro | มี PDF `TCP_IP Remote Control Interface Guide (4axis)_20240419_en.pdf` |
| TCP-IP-4Axis-Python | https://github.com/Dobot-Arm/TCP-IP-4Axis-Python | ตรงกับ MG400/M1Pro | Python package เหมาะสุดสำหรับ code generation |
| TCP-IP-4Axis-CPP | https://github.com/Dobot-Arm/TCP-IP-4Axis-CPP | ตรงกับ MG400/M1Pro | C++ package |
| TCP-IP-4Axis-CSharp | https://github.com/Dobot-Arm/TCP-IP-4Axis-CSharp | ตรงกับ MG400/M1Pro | C# demo/package |
| MG400_ROS | https://github.com/Dobot-Arm/MG400_ROS | ตรงกับ MG400 | ใช้เสริมสำหรับ ROS |
| Dobot Download Center | https://www.dobot-robots.com/service/download-center | Official | มี Secondary Development |

## แหล่งเสริมที่ไม่ใช่ MG400 โดยตรง

| แหล่งข้อมูล | URL | ใช้กับ | วิธีใช้ใน RAG |
|---|---|---|---|
| TCP-IP-Python-V4 | https://github.com/Dobot-Arm/TCP-IP-Python-V4 | CRA/E6, V4 controller | reference_only |
| TCP-IP-Python-V3 | https://github.com/Dobot-Arm/TCP-IP-Python-V3 | CR/Nova V3 | reference_only |
| TCP-IP-Protocol-6AXis-V4 | https://github.com/Dobot-Arm/TCP-IP-Protocol-6AXis-V4 | CRA/E6 6-axis V4 | ห้ามปนกับ MG400 |
| TCP-IP-Protocol-6AXis-V3 | https://github.com/Dobot-Arm/TCP-IP-Protocol-6AXis-V3 | CR/Nova 6-axis V3 | reference_only |

## Repo/File สำคัญที่ควร ingest

- `TCP-IP-Protocol-4AXis`
  - PDF EN: `TCP_IP Remote Control Interface Guide (4axis)_20240419_en.pdf`
  - PDF CN: `TCP_IP远程控制接口文档（4轴）_20240419_cn.pdf`
- `TCP-IP-4Axis-Python`
  - `README-EN.md`
  - `dobot_api.py`
  - `PythonExample.py`
  - `main.py`
  - `files/alarm_controller.json`
  - `files/alarm_servo.json`

## Command/API category ที่ chatbot ควรรู้

### Network/Port/Connection

- LAN1: `192.168.1.6`
- LAN2: `192.168.2.6`
- Wi-Fi: `192.168.9.1`
- TCP `29999`: Dashboard/control commands
- TCP `30003`: Motion commands
- TCP `30004`: Feedback stream
- PC ต้องอยู่ subnet เดียวกับ robot
- Robot ต้องตั้งเป็น TCP/IP mode ใน DobotStudio Pro

### Dashboard / Control

- EnableRobot, DisableRobot, ClearError, ResetRobot
- SpeedFactor, User, Tool, RobotMode
- PayLoad / SetPayload
- RunScript, StopScript, PauseScript, ContinueScript
- EmergencyStop
- GetErrorID, GetAngle, GetPose
- PositiveSolution, InverseSolution
- SetCollisionLevel

### Motion

- MovJ, MovL, JointMovJ
- RelMovJ, RelMovL
- MovLIO, MovJIO
- Arc, Circle
- MoveJog
- Sync, SyncAll
- RelMovJUser, RelMovLUser, RelJointMovJ, MovJExt

### Speed/Acceleration/Path

- AccJ, AccL
- SpeedJ, SpeedL
- Arch, CP, LimZ

### I/O และ Modbus

- DO, DOExecute, DOGroup, DI
- ToolDO, ToolDOExecute, ToolDI
- GetHoldRegs, SetHoldRegs
- ModbusCreate, ModbusClose
- GetInBits, GetInRegs, GetCoils, SetCoils

### Feedback / Robot State

- robot_mode, digital_input_bits, digital_outputs
- speed_scaling, program_state, safety_status
- q_actual, tool_vector_actual, TCP_speed_actual
- motor_temperatures
- userCoordinate, toolCoordinate
- isRunQueuedCmd, isPauseCmdFlag
- BrakeStatus, EnableStatus, DragStatus, RunningStatus, ErrorStatus, JogStatus, RobotType

### Error/Alarm

- ClearError
- GetErrorID
- alarm_controller.json
- alarm_servo.json

## Chunking strategy

- PDF API guide: 1 chunk ต่อ 1 command, ไม่ chunk ข้าม command
- `dobot_api.py`: 1 chunk ต่อ function/class method
- README: แยก network setup, dependencies, run demo, troubleshooting, safety notes
- Examples: 1 chunk ต่อ workflow
- Alarm JSON: 1 chunk ต่อ alarm/error id

## Safety guardrails

- ห้ามให้ LLM สั่ง motion โดยตรงโดยไม่มี human confirmation
- ก่อน motion ต้องตรวจ connection, RobotMode, ErrorStatus, E-stop, workspace/safe bounds และ speed ต่ำ
- default เป็น dry-run/simulation
- ห้ามเดา coordinate, speed, payload, Modbus register
- code examples ควรมี timeout, try/finally, close socket, logging
- แยก MG400 4-axis จาก CR/Nova 6-axis เสมอ
