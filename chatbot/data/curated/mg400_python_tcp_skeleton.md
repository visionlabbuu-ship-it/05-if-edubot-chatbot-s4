# MG400 Python TCP skeleton (connection-first, no motion)

Source note: Pattern aligned with official TCP-IP-4Axis-Python (`dobot_api.py`, `PythonExample.py`, README). Ports from the 4-axis remote-control stack (Dashboard 29999, Motion 30003, Feedback 30004).

## Goal

Connect from a PC, verify the Dashboard link, and optionally read status — **without** commanding real motion until the user explicitly enables it.

## Minimal safe skeleton (illustrative)

```python
# DRY-RUN FRIENDLY SKELETON — do not run motion on a real robot until workspace is verified.
# Confirm IP/ports against your robot and official TCP/IP 4-axis guide.

from dobot_api import DobotApiDashboard, DobotApiMove, DobotApiFeedBack  # names may match your SDK copy

ROBOT_IP = "192.168.2.6"  # typical LAN2 default; change if your robot differs
PORT_DASHBOARD = 29999
PORT_MOVE = 30003
PORT_FEEDBACK = 30004

def main():
    dash = None
    try:
        dash = DobotApiDashboard(ROBOT_IP, PORT_DASHBOARD)
        # Optional: print mode / error helpers available in your SDK version
        print("Dashboard connected. Prefer status/read APIs before any motion.")
        # Example (only if present in your SDK): dash.RobotMode() / GetErrorID()
        # DO NOT call EnableRobot / MovJ here in the default student skeleton.
    finally:
        if dash is not None:
            try:
                dash.close()
            except Exception:
                pass

if __name__ == "__main__":
    main()
```

## Recommended learning steps

1. Ping / reach robot IP on the correct LAN.
2. Open Dashboard only; list available status commands from `dobot_api.py`.
3. Clear alarms only after reading error meaning from alarm catalogs / guide.
4. Enable and motion only with supervision, low speed, and verified points.
5. Keep Feedback port optional for monitoring once connection is stable.

## Related sources to cite

- TCP/IP Remote Control Interface Guide (4-axis)
- TCP-IP-4Axis-Python README / `dobot_api.py` / `PythonExample.py`
- MG400 FAQ: network communication ports
- MG400 User Guide safety sections
