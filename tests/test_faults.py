"""
tests/test_faults.py - fault detection (faults.py).

TODO (one test per fault code):
  [ ] MAX31855 fault bit -> THERMO_FAULT
  [ ] 5 s without thermocouple data -> THERMO_TIMEOUT (4.9 s -> no fault)
  [ ] camera and ultrasonic both lost -> PRESENCE_LOST
  [ ] > 15 min on ultrasonic -> ULTRASONIC_TOO_LONG
  [ ] plug unreachable -> PLUG_UNREACHABLE
  [ ] OFF not confirmed / welded relay -> OFF_NOT_CONFIRMED (does not auto-clear)
  [ ] heartbeat failing -> HEARTBEAT_LOST
  [ ] config with None values -> CONFIG_INVALID
  [ ] fault clears only after the clear delay (no flicker)
"""
