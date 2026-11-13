"""
tests/test_iron_sensing.py - power averaging and iron-on detection (iron_sensing.py).

TODO:
  [ ] PowerAverager: constant 20 W for 30 s -> average 20 W
  [ ] PowerAverager: samples older than 30 s are dropped
  [ ] PowerAverager: missing samples handled (time-weighted)
  [ ] PowerAverager: not enough data -> None
  [ ] IronDetector: hot stand alone -> on
  [ ] IronDetector: power >= P_on alone -> on (stand cold, e.g. iron out of the stand)
  [ ] IronDetector: cool stand AND low power -> off
  [ ] IronDetector: between T_cool and T_hot -> keeps previous value
  [ ] IronDetector: one input None -> behaviour as decided
"""
