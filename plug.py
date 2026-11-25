
"""
plug.py - control the Shelly Plug US Gen4 from the Raspberry Pi.
 
Uses the plug's local HTTP RPC API: each command is an HTTP GET to
    http://<PLUG_IP>/rpc/<Method>?<params>
and the plug replies with JSON. No Shelly Cloud or internet is needed; the Pi
just has to be on the same network as the plug.
 
Usage from another script:
    import plug
 
    plug.turn_on()
    print(plug.get_power(), "W")
    print(plug.get_current(), "A")
    plug.turn_off()
 
Every function raises plug.PlugError if the plug can't be reached or sends
back something unexpected, so the caller can catch that one exception and
treat it as a fault.
"""
import config
import requests
 
# ---- Settings --------------------------------------------------------------
 
PLUG_IP = config.PLUG_IP  # change to the plug's IP on the Pi's network
SWITCH_ID = PLUG_SWITCH_ID              # the plug has one switch, number 0
TIMEOUT_S = HTTP_TIMEOUT_S            # give up if the plug doesn't answer in this time
 
 
class PlugError(Exception):
    """Raised for any problem talking to the plug (timeout, no connection,
    HTTP error, bad JSON)."""
    pass
 
 
# ---- Low-level helper -------------------------------------------------------
 
def _rpc(method, params=None):
    """Call one Shelly RPC method and return the JSON reply as a dict.
 
    Example: _rpc("Switch.GetStatus", {"id": 0}) sends
        GET http://<PLUG_IP>/rpc/Switch.GetStatus?id=0
    """
    url = f"http://{PLUG_IP}/rpc/{method}"
    try:
        r = requests.get(url, params=params, timeout=TIMEOUT_S)
    except requests.RequestException as e:
        # timeout, connection refused, no route to host...
        raise PlugError(f"{method}: can't reach plug at {PLUG_IP}: {e}") from e
 
    if r.status_code != 200:
        # The plug answered but rejected the request (bad method/parameter,
        # password required, ...). Include its message to help debugging.
        raise PlugError(f"{method}: HTTP {r.status_code}: {r.text[:200]}")
 
    try:
        return r.json()
    except ValueError as e:
        raise PlugError(f"{method}: reply was not JSON") from e
 
 
# ---- Reading ----------------------------------------------------------------
 
def get_status():
    """Return the plug's full switch status as a dict.
 
    API call: Switch.GetStatus
        GET http://<PLUG_IP>/rpc/Switch.GetStatus?id=0
    Useful keys:
        "output"  - True if the outlet is on, False if off
        "apower"  - power being drawn right now, in watts
        "current" - current, in amps
        "voltage" - mains voltage, in volts
    """
    return _rpc("Switch.GetStatus", {"id": SWITCH_ID})
 
 
def is_on():
    """True if the outlet is currently on (relay closed)."""
    return bool(get_status()["output"])
 
 
def get_power():
    """Power being drawn through the plug right now, in watts."""
    return float(get_status().get("apower", 0.0))
 
 
def get_current():
    """Current being drawn through the plug right now, in amps."""
    return float(get_status().get("current", 0.0))
 
 
def get_voltage():
    """Mains voltage at the plug, in volts."""
    return float(get_status().get("voltage", 0.0))
 
 
# ---- Switching ----------------------------------------------------------------
 
def _set_output(on):
    """Turn the outlet on or off. Returns whether it was on before.
 
    API call: Switch.Set
        GET http://<PLUG_IP>/rpc/Switch.Set?id=0&on=true   (or on=false)
    The reply is {"was_on": <previous state>}.
 
    Shelly expects lowercase "true"/"false". requests would send a Python
    bool as "True"/"False", so it's converted to a string here.
    """
    reply = _rpc("Switch.Set", {"id": SWITCH_ID, "on": "true" if on else "false"})
    return bool(reply.get("was_on", False))
 
 
def turn_on():
    """Turn the outlet on (power the iron). Returns whether it was already on."""
    return _set_output(True)
 
 
def turn_off():
    """Turn the outlet off (cut power to the iron). Returns whether it was on.
 
    This only sends the command. To be sure the power is really off, call
    get_status() a second or so afterwards and check that "output" is False
    and "apower" is about 0 W.
    """
    return _set_output(False)
 
 
# ---- Quick manual test: python3 plug.py ---------------------------------------
 
if __name__ == "__main__":
    import time
 
    print("status: ", get_status())
    print("turn_on, was on:", turn_on())
    time.sleep(1.0)  # the power reading lags the relay slightly
    print(f"on={is_on()}  power={get_power()} W  current={get_current()} A  "
          f"voltage={get_voltage()} V")
    print("turn_off, was on:", turn_off())
    time.sleep(1.0)
    print(f"on={is_on()}  power={get_power()} W")
 
