"""
tests/test_presence.py - camera/ultrasonic fallback (presence.py). Supports R5.

TODO:
  [ ] camera OK -> source CAMERA, uses camera result
  [ ] camera gives no usable frame for < 5 s -> still CAMERA (no switch yet)
  [ ] camera gives no usable frame for 5 s -> source ULTRASONIC
  [ ] on ULTRASONIC for 15 min -> seconds_on_backup >= 900 (faults.py -> FAULT)
  [ ] camera comes back -> source CAMERA, backup timer handling as decided
  [ ] camera AND ultrasonic both unhealthy -> present None, source NONE
"""
