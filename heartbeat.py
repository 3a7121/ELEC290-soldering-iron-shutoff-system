"""
heartbeat.py - Pi -> plug "I'm alive" signal.
 
The plug runs plug_watchdog.js, which turns the outlet off if it hasn't heard
a heartbeat for 20 s. This file sends that heartbeat: an HTTP GET to
 
    http://<PLUG_IP>/script/<SCRIPT_ID>/heartbeat
 
which is a URL created by the plug script (not part of Shelly's built-in API).
 
Usage from main.py - call update() once every pass of the main loop:
 
    import heartbeat
 
    while True:
        ...read sensors, run the state machine...
        heartbeat.update()                 # sends one every 5 s
        if not heartbeat.heartbeat_ok():
            ...enter Fault...
 
Because the heartbeat is sent from the main loop, a hung or crashed main loop
automatically stops the heartbeats, and the plug cuts power by itself.
 
Manual test (no main loop needed):  python3 heartbeat.py
"""
 
import time
 
import requests
 
import plug   # uses plug.PLUG_IP so the IP is only set in one place
 
# ---- Settings --------------------------------------------------------------
 
SCRIPT_ID = config.PLUG_SCRIPT_ID          # id of plug_watchdog.js on the plug (shown in the plug's Scripts page)
PERIOD_S = config.HEARTBEAT_PERIOD_S         # send a heartbeat this often
OK_WINDOW_S = config.HEARTBEAT_OK_WINDOW_S      # heartbeat_ok() is False if no success for this long (2 missed beats)
TIMEOUT_S = config.HTTP_TIMEOUT_S         # keep well under PERIOD_S so a slow reply can't delay the next beat
 
# ---- Internal state (only changed by the functions below) -------------------
 
_last_attempt = None    # time of the last send attempt (successful or not)
_last_success = None    # time of the last heartbeat the plug answered
 
 
def send_heartbeat():
    """Send one heartbeat now. Returns True if the plug answered, else False.
 
    HTTP call (created by plug_watchdog.js, not a built-in Shelly API):
        GET http://<PLUG_IP>/script/<SCRIPT_ID>/heartbeat   -> reply "ok"
    Never raises: a failed heartbeat is reported by heartbeat_ok() instead.
    """
    global _last_success
    url = f"http://{plug.PLUG_IP}/script/{SCRIPT_ID}/heartbeat"
    try:
        r = requests.get(url, timeout=TIMEOUT_S)
        if r.status_code == 200:
            _last_success = time.monotonic()
            return True
        # 404 here usually means the script isn't running or SCRIPT_ID is wrong
        return False
    except requests.RequestException:
        # timeout, plug unreachable, Wi-Fi down...
        return False
 
 
def update():
    """Call every main-loop pass. Sends a heartbeat if PERIOD_S has passed
    since the last attempt; otherwise does nothing and returns immediately."""
    global _last_attempt
    now = time.monotonic()
    if _last_attempt is None or now - _last_attempt >= PERIOD_S:
        _last_attempt = now
        send_heartbeat()
 
 
def heartbeat_ok():
    """True if the plug has answered a heartbeat within the last OK_WINDOW_S.
 
    False before the first successful heartbeat, and whenever the plug stops
    answering - main.py should treat False as a Fault (plug unreachable).
    """
    if _last_success is None:
        return False
    return time.monotonic() - _last_success <= OK_WINDOW_S
 
 
def seconds_since_success():
    """Seconds since the last successful heartbeat (None if never). For logging."""
    if _last_success is None:
        return None
    return time.monotonic() - _last_success
 
 
# ---- Manual test: python3 heartbeat.py --------------------------------------
# Sends heartbeats like main.py would. While it runs you can turn the plug on
# with its button; press Ctrl-C and the plug should turn itself off within ~20 s.
 
if __name__ == "__main__":
    print(f"Sending heartbeats to {plug.PLUG_IP} (script {SCRIPT_ID}) every {PERIOD_S:.0f} s. Ctrl-C to stop.")
    try:
        while True:
            ok = send_heartbeat()
            print(f"{time.strftime('%H:%M:%S')}  heartbeat {'ok' if ok else 'FAILED'}")
            time.sleep(PERIOD_S)
    except KeyboardInterrupt:
        print("\nStopped. The plug should turn the outlet off within about 20 s.")
 
