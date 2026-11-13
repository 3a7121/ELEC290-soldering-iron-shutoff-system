"""
tests/test_shelly_client.py - plug RPC client (shelly_client.py). Supports R3.

Use a mocked `requests` (unittest.mock) - no real plug needed.

TODO:
  [ ] turn_off() sends Switch.Set with id=0, on=false
  [ ] get_status() parses output and apower
  [ ] timeout / connection error -> PlugUnreachable
  [ ] cut_off_and_confirm(): output False + power ~0 -> True
  [ ] cut_off_and_confirm(): output still True -> False
  [ ] cut_off_and_confirm(): output False but power high (welded relay) -> False
"""
