"""
tests/conftest.py - shared pytest fixtures.

Goal: every piece of LOGIC (state machine, presence, iron sensing, faults,
plug client) can be tested on a laptop with no Pi, no camera, no plug.

TODO:
  [ ] FakeClock fixture: .now, .advance(seconds). Pass clock.now into step()/update().
  [ ] FakeCamera, FakeUltrasonic, FakeThermocouple with settable return values.
  [ ] FakePlug (or mock `requests`) that can be told: reachable / unreachable,
      output after Switch.Set, power reading (incl. welded-relay case).
  [ ] Run with:  python3 -m pytest -q
"""
