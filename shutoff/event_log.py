"""
event_log.py - logging for debugging and for verification evidence.

Every state change, fault, cut-off attempt and its confirmation should be
logged with a timestamp. These logs are the easiest evidence for the
verification tests in the RTM (e.g. "warning started after 180 s").

TODO:
  [ ] setup(): configure the `logging` module to write to stdout (journald
      captures it under systemd) and optionally to a rotating file.
  [ ] log_transition(old, new, reason) and log_fault(code) helpers.
  [ ] Never log camera frames or images (R4: frames stay on the Pi, nothing is
      stored or sent). Log only "present: yes/no" and detection timing.
  [ ] Add a CSV option for test runs (time, state, stand temp, power, present)
      so the team can plot results for CP3.
"""

import logging

log = logging.getLogger("shutoff")


def setup(level: int = logging.INFO) -> None:
    """TODO: handlers + format."""
    raise NotImplementedError


def log_transition(old, new, reason: str) -> None:
    """TODO"""
    raise NotImplementedError


def log_fault(code) -> None:
    """TODO"""
    raise NotImplementedError
