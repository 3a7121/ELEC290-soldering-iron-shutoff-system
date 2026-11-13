"""
tools/configure_plug.py - one-time Shelly Plug US Gen4 setup from the Pi.

Design reference: CP2 Section 3: plug configured initial_state = off; plug-side
watchdog script; local HTTP RPC only.

TODO:
  [ ] Print Shelly.GetDeviceInfo (model, firmware) to confirm it is the Gen4.
  [ ] Switch.SetConfig id=0 config={"initial_state": "off"}.
  [ ] Upload shelly/plug_watchdog.js: Script.Create, Script.PutCode (in chunks),
      Script.SetConfig enable=true, Script.Start. Print the script id so it can
      go into config.py (needed for the heartbeat URL).
  [ ] Optionally disable cloud and set an auth password (Shelly.SetAuth).
  [ ] Read back every setting and print PASS/FAIL.
  [ ] Usage: python3 tools/configure_plug.py --host 192.168.x.y
"""


def main() -> int:
    """TODO"""
    raise NotImplementedError


if __name__ == "__main__":
    raise SystemExit(main())
