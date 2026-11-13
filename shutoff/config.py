"""
config.py - every tunable number in one place.

Design reference: CP2 Section 3, "Behaviour (state machine, provisional values)",
"Assumptions" and "Open items for CP3".

All values below are PROVISIONAL (CP2). Values marked None are not known yet and
must be measured on the lab's irons / stand / camera before CP3. The service
should refuse to start (go to Fault) if any required value is still None.

TODO:
  [ ] Measure and fill in T_HOT_C and T_COOL_C (tools/calibrate_stand_temp.py).
      T_COOL_C must be below T_HOT_C (hysteresis band).
  [ ] Measure and fill in P_ON_W and P_OFF_W on the lab's irons
      (tools/measure_iron_power.py). Confirms assumption A1.
  [ ] Pick D_PRESENT_CM for the ultrasonic backup and CAMERA_ROI for the
      camera (tools/camera_roi.py).
  [ ] Validate the timers (3 min / 2 min / 5 s / 20 s / 15 min) during
      integration and record the evidence for CP3.
  [ ] Decide whether config is loaded from a file (e.g. /etc/shutoff/config.toml)
      so values can be changed without editing code. If so, add load() + checks.
  [ ] Add validate() that raises if a required value is None or inconsistent
      (e.g. T_COOL_C >= T_HOT_C, HEARTBEAT_PERIOD_S >= PLUG_WATCHDOG_S).
  [ ] Put the plug's IP / hostname here once the Pi-hosted network is set up.
"""

# ---- State machine timers (seconds) -------------------------------------
GRACE_S = 3 * 60            # Grace: user absent, green LED blinks
WARNING_S = 2 * 60          # Warning: yellow LED + buzzer, then cut power

# ---- Presence ------------------------------------------------------------
CAMERA_LOSS_S = 5           # no usable camera frame for this long -> use ultrasonic
ULTRASONIC_MAX_S = 15 * 60  # max time on ultrasonic backup before Fault
D_PRESENT_CM = None         # TODO: distance below which someone counts as present
CAMERA_INDEX = 0            # /dev/video0
CAMERA_ROI = None           # TODO: (x, y, w, h) region of interest in pixels

# ---- Iron-on sensing -----------------------------------------------------
T_HOT_C = None              # TODO: stand temperature meaning "iron on"
T_COOL_C = None             # TODO: stand temperature meaning "cooled down"
P_ON_W = None               # TODO: plug power meaning "iron energized" (30 s avg)
P_OFF_W = None              # TODO: "~0 W" level used to confirm cut-off
POWER_AVG_WINDOW_S = 30     # averaging window for plug power
THERMO_TIMEOUT_S = 5        # no thermocouple data for this long -> Fault

# ---- Smart plug / heartbeat ---------------------------------------------
PLUG_HOST = None            # TODO: e.g. "192.168.4.20" on the Pi-hosted network
PLUG_SWITCH_ID = 0
HTTP_TIMEOUT_S = 2.0
HEARTBEAT_PERIOD_S = 5      # Pi -> plug heartbeat (changed from 10 s for R5)
PLUG_WATCHDOG_S = 20        # plug turns outlet off if no heartbeat (changed from 60 s)
POWER_POLL_PERIOD_S = 1     # how often to read plug power

# ---- Main loop -----------------------------------------------------------
LOOP_PERIOD_S = 0.1         # TODO: confirm the camera detection rate supports this


def validate():
    """TODO: raise ValueError listing every missing / inconsistent value."""
    raise NotImplementedError
