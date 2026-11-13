"""
service_health.py - systemd watchdog + Pi hardware watchdog.

Design reference: CP2 Section 3, "one Python 3 service under systemd
(auto-restart, hardware watchdog)".

Two layers:
  - systemd service watchdog: the service must call notify("WATCHDOG=1")
    more often than WatchdogSec in deploy/shutoff.service, or systemd kills
    and restarts it.
  - Pi hardware watchdog (bcm2835_wdt): systemd pets it via RuntimeWatchdogSec
    in /etc/systemd/system.conf; if the whole OS hangs, the Pi reboots.
  After either restart the controller starts in CUT_OFF and the plug's own
  20 s watchdog has already turned the outlet off.

TODO:
  [ ] Implement ready() -> sd_notify("READY=1") once hardware is initialised.
  [ ] Implement pet() -> sd_notify("WATCHDOG=1"); call it from the main loop
      only when the loop is actually healthy (not from a separate thread).
  [ ] Use the `sdnotify` package or write to $NOTIFY_SOCKET directly.
  [ ] Make it a no-op when not running under systemd (laptop testing).
  [ ] Document the hardware watchdog setup in deploy/setup_pi.sh and test it
      (e.g. kill -STOP the service and confirm restart; record for CP3).
"""


def ready() -> None:
    """TODO: tell systemd the service is up."""
    raise NotImplementedError


def pet() -> None:
    """TODO: tell systemd the loop is alive."""
    raise NotImplementedError
