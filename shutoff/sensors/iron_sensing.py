"""
iron_sensing.py - is the iron on? (stand temperature OR plug power)

Design reference: CP2 Section 3, "Iron-on sensing" and assumption A1
(an energized iron draws more than P_on averaged over 30 s).

  iron on  = stand_temp >= T_HOT_C  OR  power_avg_30s >= P_ON_W
  iron off = stand_temp <= T_COOL_C AND power_avg_30s <  P_ON_W
  otherwise keep the previous value (hysteresis)

TODO:
  [ ] Implement PowerAverager: keep (time, watts) samples from the plug,
      return the average over the last POWER_AVG_WINDOW_S. Handle gaps
      (missing polls) by time-weighting, not just averaging samples.
  [ ] Implement IronDetector.update(stand_temp, power_avg) -> bool with the
      hysteresis above. Decide behaviour when one input is None
      (proposal: use the other one alone; faults.py handles the missing one).
  [ ] Implement stand_cooled(stand_temp) for the CUT_OFF -> IDLE rule.
  [ ] Unit tests: tests/test_iron_sensing.py.
  [ ] CP3: measure P_on and the "off" power on the lab's irons; confirm A1
      (idle irons with a thermostat may cycle - check the 30 s average stays
      above P_on while the iron is on).
"""


class PowerAverager:
    def __init__(self, window_s: float):
        """TODO"""
        raise NotImplementedError

    def add(self, now: float, watts: float) -> None:
        """TODO"""
        raise NotImplementedError

    def average(self, now: float) -> float | None:
        """TODO: None if not enough data in the window."""
        raise NotImplementedError


class IronDetector:
    def __init__(self, t_hot: float, t_cool: float, p_on: float):
        """TODO"""
        raise NotImplementedError

    def update(self, stand_temp_c: float | None, power_avg_w: float | None) -> bool:
        """TODO: hysteresis rule above."""
        raise NotImplementedError

    def stand_cooled(self, stand_temp_c: float | None) -> bool:
        """TODO"""
        raise NotImplementedError
