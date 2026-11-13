"""
leds.py - green / yellow / red status LEDs.

Design reference: CP2 Section 3, "User interface" and GPIO map
(green GPIO16, yellow GPIO20, red GPIO21).
Known from the design: Grace = green blinks; Warning = yellow (+ buzzer).

TODO:
  [ ] Implement with gpiozero.LED (supports .on(), .off(), .blink()).
  [ ] set(green, yellow, red) taking "off" | "on" | "blink" from state_machine.Outputs.
      Only change an LED when its mode changes (calling blink() every tick
      restarts the blink).
  [ ] Agree the LED meaning for every state with the team and put the table in
      the README and report (proposal is in state_machine.py).
  [ ] all_off() for shutdown.
  [ ] Self-test pattern at start-up (all on 1 s) - also used by tools/hw_selftest.py.
"""


class Leds:
    def __init__(self, green_pin: int, yellow_pin: int, red_pin: int):
        """TODO"""
        raise NotImplementedError

    def set(self, green: str, yellow: str, red: str) -> None:
        """TODO"""
        raise NotImplementedError

    def self_test(self) -> None:
        """TODO"""
        raise NotImplementedError

    def all_off(self) -> None:
        """TODO"""
        raise NotImplementedError
