"""
button.py - reset button (GPIO17 to GND, internal pull-up).

Design reference: CP2 Section 3: Cut Off -> Idle only when the stand has cooled
AND reset is pressed. Reset is ignored in Grace and Warning (the state machine
enforces that; this module only reports presses).

TODO:
  [ ] Implement with gpiozero.Button(pin, pull_up=True, bounce_time=0.05).
  [ ] pressed_since_last_check() -> bool: latch a press from the callback and
      clear it when read, so a short press between loop ticks is not missed.
  [ ] Decide if a long press (e.g. 3 s) is needed instead of a tap, to avoid
      accidental resets. Note the choice in the report.
  [ ] Test the wiring with tools/hw_selftest.py.
"""


class ResetButton:
    def __init__(self, pin: int):
        """TODO"""
        raise NotImplementedError

    def pressed_since_last_check(self) -> bool:
        """TODO"""
        raise NotImplementedError

    def close(self) -> None:
        """TODO"""
        raise NotImplementedError
