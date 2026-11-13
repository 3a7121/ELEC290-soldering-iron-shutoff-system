"""
tools/measure_iron_power.py - find P_on and the "off" power level (CP3 open item).

Logs plug power once per second to CSV while someone runs the iron through:
plugged in but off -> heating up -> idle at set temperature -> in use -> off.

TODO:
  [ ] Poll Switch.GetStatus every 1 s, write time, apower, 30 s average to CSV.
  [ ] Let the user type a label ("heating", "idle", "off") to mark phases.
  [ ] At the end print min / max / mean per phase and the lowest 30 s average
      while the iron was on -> suggest P_ON_W below that with margin.
  [ ] Print the max power while "off" -> suggest P_OFF_W above that.
  [ ] Repeat for every iron model in the lab; record results for CP3 and to
      confirm assumption A1.
"""


def main() -> int:
    """TODO"""
    raise NotImplementedError


if __name__ == "__main__":
    raise SystemExit(main())
