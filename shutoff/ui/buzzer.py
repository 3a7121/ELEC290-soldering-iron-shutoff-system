"""
buzzer.py - piezo buzzer switched by an NPN transistor from 5 V.

Design reference: CP2 Section 3, "User interface" and GPIO map
(GPIO18 -> 1 kohm -> NPN base; buzzer between 5 V and collector).
GPIO HIGH = transistor on = buzzer on.

Buzzer sounds during Warning. R2 note: the warning ends when a person returns
or power is cut; the reset button is ignored during warnings.

TODO:
  [ ] Find out if the piezo is ACTIVE (just switch on/off -> gpiozero.Buzzer)
      or PASSIVE (needs a tone -> gpiozero.TonalBuzzer or PWM on GPIO18, ~2-4 kHz).
  [ ] Implement patterns: "off", "warning" (e.g. 0.5 s on / 0.5 s off),
      "fault" (distinct pattern, e.g. fast triple beep). Only restart a pattern
      when it changes.
  [ ] Check loudness in the lab (can it be heard over fume extractors?).
  [ ] off() for shutdown - make sure the buzzer is never left on after exit.
"""


class Buzzer:
    def __init__(self, pin: int):
        """TODO"""
        raise NotImplementedError

    def set(self, pattern: str) -> None:
        """TODO: "off" | "warning" | "fault"."""
        raise NotImplementedError

    def off(self) -> None:
        """TODO"""
        raise NotImplementedError
