"""
shelly_client.py - local HTTP RPC to the Shelly Plug US Gen4.

Design reference: CP2 Section 3, "Switching element" and the Warning -> Cut Off
rule (Switch.Set off, then Switch.GetStatus; Cut Off only if output is false
and power ~0 W, otherwise Fault). R3.

Gen2+/Gen4 RPC over HTTP (no cloud), e.g.:
  GET http://<plug>/rpc/Switch.Set?id=0&on=false
  GET http://<plug>/rpc/Switch.GetStatus?id=0
      -> {"id":0, "output":false, "apower":0.0, "voltage":..., "current":..., ...}
  GET http://<plug>/rpc/Switch.SetConfig?id=0&config={"initial_state":"off"}
  GET http://<plug>/rpc/Shelly.GetDeviceInfo

TODO:
  [ ] Implement _rpc(method, params) with `requests`, timeout HTTP_TIMEOUT_S,
      raising PlugUnreachable on timeout / connection error / bad JSON.
  [ ] Implement turn_off(), get_status() -> PlugStatus(output, power_w).
  [ ] Implement cut_off_and_confirm(): turn_off(), wait ~1 s, get_status(),
      return True only if output is False AND power_w <= P_OFF_W. Retry the
      status read a couple of times before deciding.
  [ ] Detect welded relay: output False but power_w > P_OFF_W -> return False
      and let faults.py raise OFF_NOT_CONFIRMED.
  [ ] Decide if the controller ever turns the plug ON (e.g. on reset from
      CUT_OFF -> IDLE) or if the user re-enables it with the plug's button.
      The design only covers turning OFF; confirm with the team.
  [ ] Verify the exact RPC field names against the Gen4 API docs on the real
      plug (Shelly.GetDeviceInfo, then Switch.GetStatus) before relying on them.
  [ ] Enable plug authentication (digest auth) if the network is shared; add
      credentials to config.
  [ ] Unit tests with a fake HTTP server or mocked requests: tests/test_shelly_client.py.
  [ ] CP3: confirm the plug's Canadian certification mark.
"""

from dataclasses import dataclass


class PlugUnreachable(Exception):
    pass


@dataclass
class PlugStatus:
    output: bool
    power_w: float


class ShellyClient:
    def __init__(self, host: str, switch_id: int = 0, timeout_s: float = 2.0):
        """TODO"""
        raise NotImplementedError

    def _rpc(self, method: str, params: dict | None = None) -> dict:
        """TODO: GET /rpc/<method>, return parsed JSON."""
        raise NotImplementedError

    def get_status(self) -> PlugStatus:
        """TODO: Switch.GetStatus -> output, apower."""
        raise NotImplementedError

    def turn_off(self) -> None:
        """TODO: Switch.Set on=false."""
        raise NotImplementedError

    def cut_off_and_confirm(self, p_off_w: float) -> bool:
        """TODO: see module docstring."""
        raise NotImplementedError

    def ensure_initial_state_off(self) -> None:
        """TODO: Switch.SetConfig initial_state=off (also done by tools/configure_plug.py)."""
        raise NotImplementedError
