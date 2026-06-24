#laptop_alarm.py

import sys

def trigger_laptop_alarm():
    print("🚨 PLAYING LAPTOP AUDIO ALARM...")
    try:
        if sys.platform == "win32":
            import winsound
            for _ in range(30): winsound.Beep(2500, 500)
    except Exception as e: print(f"Could not trigger audio: {e}")

