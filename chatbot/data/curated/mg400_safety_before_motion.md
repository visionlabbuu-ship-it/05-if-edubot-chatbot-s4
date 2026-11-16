# MG400 safety checklist before motion (MovJ / MovL / Jump)

Source note: Curated for RAG from MG400 User Guide safety sections, TCP/IP 4-axis practices, and project safety policy. Prefer official User Guide wording when both this card and the manual are retrieved.

## Before any motion command

1. **People out of reach** — establish guardrails / warning zone; do not enter the robot safety range while powered or about to move.
2. **Trained operator** — only trained personnel operate, install, or maintain.
3. **E-stop reachable** — know how to stop immediately.
4. **Workspace clear** — no tools, cables, or fixtures in the path; stay within workspace and avoid boundary extremes.
5. **Payload / tooling** — payload within rated limits; end-effector secured; eccentric load understood.
6. **Robot state** — no active alarms; clear errors only after understanding the cause; brakes / enable state correct.
7. **Speed low first** — first runs at low speed / reduced velocity; dry-run or simulation when available.
8. **Coordinate assumptions** — never run coordinates you did not teach or verify on *this* robot and tool frame.
9. **Supervision** — human watches the first executions of new programs.
10. **Stop on abnormality** — if motion looks wrong, stop first, then diagnose.

## Before EnableRobot / remote motion via TCP

- Confirm TCP mode and network settings.
- Prefer Dashboard connection and status read before motion port use.
- Do not chain EnableRobot → MovJ in student demos without an explicit clear-workspace confirmation.
- Generated code should default to connection-only or commented motion lines until the user opts in.

## Topics that always need a short safety warning in answers

- EnableRobot / DisableRobot
- MovJ, MovL, Jump, Arc, ServoJ/ServoP, jog
- I/O that drives grippers or actuators
- Collision detection level changes
- Payload / speed limit changes
- Emergency stop / safeguard stop recovery

## Out of scope for this card

Detailed electrical wiring and full risk assessment remain in the official User Guide and local site procedures.
