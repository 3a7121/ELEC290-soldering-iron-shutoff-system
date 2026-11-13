"""
heartbeat.py - Pi -> plug "I'm alive" signal every 5 s.

Design reference: CP2 Section 3, "Plug-side watchdog script": outlet off if no
heartbeat for 20 s; heartbeat every 5 s (changed from 10 s / 60 s so R5's
30 s limit is met). The plug side lives in shelly/plug_watchdog.js.

If the Pi crashes, hangs, loses Wi-Fi or the service stops, heartbeats stop and
the plug cuts the iron by itself within 20 s.

TODO:
  [ ] Pick the heartbeat mechanism and match it in plug_watchdog.js:
        (a) call an HTTP endpoint the script registers
            (GET http://<plug>/script/<id>/heartbeat), or
        (b) write a KVS value / virtual component the script watches.
      (a) is simplest and gives an immediate reply to confirm delivery.
  [ ] Run in a background thread: send every HEARTBEAT_PERIOD_S, record the
      time of the last successful send.
  [ ] Only send while the main loop is healthy (main loop sets a flag each
      tick; if the flag is stale, stop sending so the plug cuts power).
  [ ] heartbeat_ok(now): False if no successful send for > ~2 periods
      (faults.py -> HEARTBEAT_LOST). Choose the exact threshold.
  [ ] Test: stop the service / pull the Pi's power and time how long the plug
      takes to turn off (should be <= 20 s, well under R5's 30 s). Record it.
"""

import threading


class Heartbeat:
    def __init__(self, plug_client, period_s: float):
        """TODO"""
        raise NotImplementedError

    def start(self) -> None:
        """TODO: start the background thread."""
        raise NotImplementedError

    def stop(self) -> None:
        """TODO: stop sending (the plug will cut power after 20 s)."""
        raise NotImplementedError

    def mark_loop_alive(self, now: float) -> None:
        """TODO: called by main loop each tick."""
        raise NotImplementedError

    def heartbeat_ok(self, now: float) -> bool:
        """TODO"""
        raise NotImplementedError
