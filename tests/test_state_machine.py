"""
tests/test_state_machine.py - behaviour tests for state_machine.py.

These are the core verification tests; name each one after the behaviour so
the RTM can point at them.

TODO (one test each):
  [ ] starts in CUT_OFF after construction
  [ ] CUT_OFF -> IDLE needs BOTH stand cooled AND reset (each alone does nothing)
  [ ] IDLE -> ATTENDED when iron turns on with a person present
  [ ] ATTENDED -> GRACE when person leaves; green blinks
  [ ] GRACE -> ATTENDED when person returns before 3 min
  [ ] GRACE -> WARNING at exactly 3 min; yellow + buzzer
  [ ] WARNING -> ATTENDED when person returns (R2 wording: warning ends on return)
  [ ] WARNING at 2 min -> plug off requested -> confirmed -> CUT_OFF
  [ ] WARNING at 2 min -> OFF not confirmed (still drawing power) -> FAULT
  [ ] reset button ignored in GRACE and WARNING
  [ ] iron turns off (stand <= T_cool AND power < P_on) in any iron-on state -> IDLE
  [ ] iron-on hysteresis: temperature between T_cool and T_hot keeps previous value
  [ ] fault from every state -> FAULT
  [ ] FAULT cleared -> CUT_OFF (never straight to IDLE)
"""
