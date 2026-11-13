"""
main.py - the single Python 3 service that runs on the Raspberry Pi 4B.

Design reference: CP2 Section 3, "Selected parts" (one Python 3 service under
systemd with auto-restart and hardware watchdog).

Main loop, once per LOOP_PERIOD_S:
  1. Read stand temperature (sensors/thermocouple.py)
  2. Read plug power and keep the 30 s average (plug/shelly_client.py,
     sensors/iron_sensing.py)
  3. Get presence: camera first, ultrasonic backup (sensors/presence.py)
  4. Read the reset button edge (ui/button.py)
  5. Update faults (faults.py)
  6. Step the state machine (state_machine.py)
  7. Apply outputs: LEDs, buzzer, plug off / cut-off check (ui/, plug/)
  8. Pet the systemd watchdog (service_health.py)
The heartbeat to the plug runs on its own thread (plug/heartbeat.py).

TODO:
  [ ] Build all objects in build_system() (real hardware) and keep a way to
      build them with fakes for testing on a laptop.
  [ ] Call config.validate() first; if it fails, go straight to FAULT.
  [ ] Make the plug OFF at start-up (plug initial_state = off and controller
      starts in CUT_OFF) before anything else.
  [ ] Implement run_loop(); keep each tick short, never block on HTTP for
      longer than HTTP_TIMEOUT_S.
  [ ] Catch exceptions per tick: log, go to FAULT, keep running. Only exit on
      SIGTERM (then LEDs off, buzzer off, leave the plug OFF).
  [ ] Start / stop the heartbeat thread cleanly.
  [ ] Measure loop timing on the Pi with the camera running (CP3 open item:
      detection rate on the Pi).
"""

import signal
import sys


def build_system():
    """TODO: create sensors, plug client, heartbeat, UI, fault monitor, state machine."""
    raise NotImplementedError


def run_loop(system) -> None:
    """TODO: the 8-step loop described above."""
    raise NotImplementedError


def shutdown(system) -> None:
    """TODO: LEDs/buzzer off, stop threads, leave plug OFF, close camera/SPI/GPIO."""
    raise NotImplementedError


def main() -> int:
    # TODO: set up logging (event_log.setup()), handle SIGTERM/SIGINT
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
    system = build_system()
    try:
        run_loop(system)
    finally:
        shutdown(system)
    return 0
