"""
tools/hw_selftest.py - check every piece of hardware one at a time.

Run on the Pi after wiring, before running the service. Each step prints
PASS / FAIL so the result can go straight into the integration log.

TODO:
  [ ] LEDs: green, yellow, red on for 1 s each (ask the user to confirm).
  [ ] Buzzer: 0.5 s beep (and tone sweep if passive).
  [ ] Button: "press reset within 10 s" -> detects press.
  [ ] Thermocouple: print 5 readings + fault bits; FAIL on any fault.
  [ ] Ultrasonic: print 10 distances; FAIL if all time out.
  [ ] Camera: open, grab 30 frames, print FPS and presence result (no saving).
  [ ] Plug: GetStatus, print output + power; optional on/off click test.
  [ ] Heartbeat: send one heartbeat, confirm the script replies.
  [ ] Summary table at the end.
"""


def main() -> int:
    """TODO"""
    raise NotImplementedError


if __name__ == "__main__":
    raise SystemExit(main())
