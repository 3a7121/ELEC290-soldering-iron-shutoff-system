"""
faults.py - decides when the system must go to FAULT.

Design reference: CP2 Section 3, "Fault from ANY state" and "Residual risk".

Fault conditions from the design:
  1. Thermocouple fault flag from the MAX31855 (open, short to GND, short to VCC)
     OR no thermocouple data for THERMO_TIMEOUT_S (5 s)
  2. Both presence sources lost (camera gone AND ultrasonic gone), or the
     ultrasonic backup has been in use longer than ULTRASONIC_MAX_S (15 min)
  3. Plug unreachable, or OFF not confirmed after a cut-off command
  4. Heartbeat to the plug lost
Residual risk: a welded plug relay shows as "OFF not confirmed" (power still
flowing). The system can only alarm; a person must unplug the iron.

TODO:
  [ ] Implement FaultMonitor.update(...) that takes the latest health info
      from each module and returns the set of active faults.
  [ ] Give every fault a code + human message (for the log and for debugging).
  [ ] Decide how a fault "clears" (e.g. condition gone for N seconds) so FAULT
      -> CUT_OFF does not flicker. Pick N and add it to config.py.
  [ ] Treat "config.validate() failed" as a permanent fault at start-up.
  [ ] Add the welded-relay case explicitly: output reports false but power is
      still above P_OFF_W -> fault that never auto-clears until restart.
  [ ] Unit tests: tests/test_faults.py (each condition, clearing, flicker).
"""

from dataclasses import dataclass
from enum import Enum


class FaultCode(Enum):
    THERMO_FAULT = "thermocouple reports a fault"
    THERMO_TIMEOUT = "no thermocouple data"
    PRESENCE_LOST = "camera and ultrasonic both unavailable"
    ULTRASONIC_TOO_LONG = "ultrasonic backup used longer than allowed"
    PLUG_UNREACHABLE = "smart plug not reachable"
    OFF_NOT_CONFIRMED = "plug did not confirm OFF"
    HEARTBEAT_LOST = "heartbeat to plug failing"
    CONFIG_INVALID = "configuration incomplete"


@dataclass
class HealthSnapshot:
    """TODO: fill from sensors/plug each tick."""
    thermo_fault: bool
    seconds_since_thermo: float
    presence_available: bool
    seconds_on_ultrasonic: float
    plug_reachable: bool
    off_confirmed: bool | None
    heartbeat_ok: bool


class FaultMonitor:
    def update(self, health: HealthSnapshot, now: float) -> set[FaultCode]:
        """TODO: return active faults (empty set = no fault)."""
        raise NotImplementedError

    def is_cleared(self, now: float) -> bool:
        """TODO: True once no fault has been active for the clear delay."""
        raise NotImplementedError
