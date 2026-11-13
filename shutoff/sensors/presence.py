"""
presence.py - combines camera (primary) and ultrasonic (backup).

Design reference: CP2 Section 3, "Presence (primary)" / "Presence (backup)"
and the R5 RTM note (camera disconnect -> ultrasonic backup -> Fault after 15 min).

Rules:
  - Camera gives usable frames          -> use camera result; reset backup timer
  - No usable camera frame for 5 s      -> switch to ultrasonic
  - On ultrasonic for > 15 min total    -> report "too long" (faults.py -> FAULT)
  - Camera unusable AND ultrasonic unhealthy -> present = None (faults.py -> FAULT)

TODO:
  [ ] Implement PresenceManager.update(now) -> PresenceResult.
  [ ] Decide what "15 min" means if the camera flickers back for a moment:
      reset only after the camera has been good for some time (add to config).
  [ ] Report which source is in use (for LEDs/logging and for test evidence).
  [ ] Unit tests with fake camera / fake ultrasonic: tests/test_presence.py.
"""

from dataclasses import dataclass
from enum import Enum


class Source(Enum):
    CAMERA = "camera"
    ULTRASONIC = "ultrasonic"
    NONE = "none"


@dataclass
class PresenceResult:
    present: bool | None
    source: Source
    seconds_on_backup: float


class PresenceManager:
    def __init__(self, camera, ultrasonic):
        """TODO: store sources and timers."""
        raise NotImplementedError

    def update(self, now: float) -> PresenceResult:
        """TODO: apply the rules above."""
        raise NotImplementedError
