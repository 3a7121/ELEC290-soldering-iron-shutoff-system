"""
state_machine.py - the controller's behaviour. Pure logic, no hardware.

Design reference: CP2 Section 3, "Behaviour (state machine, provisional values)".

States:   IDLE, ATTENDED, GRACE, WARNING, CUT_OFF, FAULT
Super-state "iron on" = {ATTENDED, GRACE, WARNING}
Outer "Monitoring" box = every state; Fault can be entered from any of them.

Transitions to implement (from the CP2 design):
  - Start-up (any restart)            -> CUT_OFF
  - IDLE, iron on                     -> ATTENDED if present, else GRACE  (confirm vs diagram)
  - ATTENDED, presence lost           -> GRACE   (start 3 min timer, green blinks)
  - GRACE, presence back              -> ATTENDED
  - GRACE, 3 min elapsed              -> WARNING (start 2 min timer, yellow + buzzer)
  - WARNING, presence back            -> ATTENDED (warning ends when a person returns)
  - WARNING, 2 min elapsed            -> request Switch.Set off, then Switch.GetStatus:
                                         output false AND power ~0 W -> CUT_OFF, else FAULT
  - iron-on super-state, iron off     -> IDLE  (stand <= T_cool AND power < P_on)
  - CUT_OFF, stand cooled AND reset   -> IDLE
  - Reset button IGNORED in GRACE and WARNING
  - ANY state, fault condition        -> FAULT (see faults.py)
  - FAULT, fault cleared              -> CUT_OFF

TODO:
  [ ] Implement State enum and Inputs / Outputs dataclasses (below).
  [ ] Implement step(inputs, now) returning the new state + Outputs. Take `now`
      as an argument (monotonic seconds) so tests can fake time.
  [ ] Implement iron-on hysteresis: on if stand >= T_hot OR power_avg >= P_on;
      off if stand <= T_cool AND power_avg < P_on; otherwise keep previous value.
  [ ] Decide what IDLE does when iron on but nobody present (straight to GRACE?).
      Check it matches the state diagram in the report.
  [ ] Decide whether entering FAULT also commands the plug off (recommended),
      and what LEDs/buzzer show in FAULT (proposal: red + buzzer pattern).
  [ ] Define LED/buzzer output for every state (proposal: IDLE all off,
      ATTENDED green solid, GRACE green blink, WARNING yellow + buzzer,
      CUT_OFF red solid, FAULT red blink + buzzer). Confirm with the team.
  [ ] The cut-off confirm step is asynchronous (HTTP). Model it either as a
      short internal sub-state (e.g. CUTTING) or as a blocking call in main.py
      with a timeout. Document the choice.
  [ ] Log every transition (event_log.py) with reason and timestamp.
  [ ] Unit tests: tests/test_state_machine.py.
"""

from dataclasses import dataclass
from enum import Enum, auto


class State(Enum):
    IDLE = auto()
    ATTENDED = auto()
    GRACE = auto()
    WARNING = auto()
    CUT_OFF = auto()
    FAULT = auto()


IRON_ON_STATES = {State.ATTENDED, State.GRACE, State.WARNING}


@dataclass
class Inputs:
    """Snapshot of everything the state machine needs on one tick."""
    stand_temp_c: float | None      # None = no reading
    power_avg_w: float | None       # 30 s average from the plug
    present: bool | None            # None = no presence source available
    reset_pressed: bool             # edge, already debounced
    fault_active: bool              # from faults.FaultMonitor
    cutoff_confirmed: bool | None   # result of the OFF check, None = not checked


@dataclass
class Outputs:
    """What main.py should do after this tick."""
    green: str = "off"              # "off" | "on" | "blink"
    yellow: str = "off"
    red: str = "off"
    buzzer: str = "off"             # "off" | "on" | pattern name
    command_plug_off: bool = False
    request_cutoff_check: bool = False


class StateMachine:
    def __init__(self, now: float):
        # TODO: start in CUT_OFF (design: controller starts in Cut Off after any restart)
        self.state = State.CUT_OFF
        self.entered_at = now
        self.iron_on = False

    def step(self, inputs: Inputs, now: float) -> Outputs:
        """TODO: apply the transition list in the module docstring."""
        raise NotImplementedError

    def _update_iron_on(self, inputs: Inputs) -> bool:
        """TODO: hysteresis between T_hot/P_on and T_cool."""
        raise NotImplementedError

    def _transition(self, new_state: State, now: float, reason: str) -> None:
        """TODO: change state, reset timer, log the reason."""
        raise NotImplementedError

    def _outputs_for(self, state: State) -> Outputs:
        """TODO: LED / buzzer / plug outputs for each state."""
        raise NotImplementedError
