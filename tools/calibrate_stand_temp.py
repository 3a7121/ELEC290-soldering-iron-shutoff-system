"""
tools/calibrate_stand_temp.py - find T_hot, T_cool and the probe position (CP3 open item).

Logs MAX31855 stand temperature once per second to CSV while the iron is put
in the stand hot, left there, removed, and allowed to cool.

TODO:
  [ ] Read thermocouple every 1 s, write time, temp, fault bits to CSV.
  [ ] Phase labels typed by the user ("iron in", "iron out", "unplugged").
  [ ] Report: time to reach X C after the iron goes in; temperature when the
      iron is out but still hot; time to cool to room + Y C after unplugging.
  [ ] Suggest T_HOT_C (reached quickly with a hot iron in the stand) and
      T_COOL_C (safe to touch / iron genuinely cold), with a gap between them.
  [ ] Repeat for 2-3 probe positions and pick the best; photo for the report.
"""


def main() -> int:
    """TODO"""
    raise NotImplementedError


if __name__ == "__main__":
    raise SystemExit(main())
