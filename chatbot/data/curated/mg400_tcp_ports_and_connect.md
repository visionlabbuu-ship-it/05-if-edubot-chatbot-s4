# MG400 TCP/IP ports and connection cheat-sheet

Source note: Curated from official TCP/IP 4-axis remote control docs, TCP-IP-4Axis-Python README/SDK, and official MG400 FAQ (network ports). Use this card when answering port / LAN / connection questions.

## Primary TCP ports (dashboard / motion / feedback)

Typical Dobot 4-axis (MG400 / M1 Pro) remote-control layout used by the official TCP/IP demos:

| Port  | Role        | Common use                                      |
|-------|-------------|-------------------------------------------------|
| 29999 | Dashboard   | Enable/disable, clear error, script, I/O, mode  |
| 30003 | Motion      | MovJ, MovL, Jump, Arc, relative moves, etc.     |
| 30004 | Feedback    | High-frequency robot status / feedback stream   |

Always confirm against the TCP/IP Remote Control Interface Guide (4-axis) and the SDK you are using if versions differ.

## Other network ports (FAQ)

From official MG400 FAQ (network communication ports):

- **502** — Modbus (default). Do not occupy it for other services.
- **8172** — Lua debugger. Do not occupy it.
- **LAN1** default IP `192.168.1.6` — used to connect the upper computer / software debugging (often not user-modifiable).
- **LAN2** default IP `192.168.2.6` — available for operator TCP communication by default. User may modify, but avoid putting it on network segment 1 to prevent conflict with LAN1.

## Safe connection checklist (before motion)

1. Power on robot; confirm E-stop released and workspace clear.
2. PC and robot on the same reachable network (usually LAN2 for TCP demos).
3. Enable TCP/IP remote mode in software if required by the guide version.
4. Open Dashboard (29999) first; check robot mode / errors.
5. ClearError / enable sequence only after confirming the official command order for your guide version.
6. Prefer read-only / connection-only tests before any MovJ/MovL.
7. Keep human supervision; start at low speed.

## What not to invent

- Do not invent alternate port numbers if they are not in retrieved official context.
- Do not mix CR / Nova / 6-axis port or command docs into MG400 answers.
