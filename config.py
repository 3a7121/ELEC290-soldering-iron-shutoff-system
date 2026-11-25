PLUG_IP = "10.184.67.170"     # phone hotspot for now; change to the fixed IP on the Pi's network
PLUG_SWITCH_ID = 0            # the plug has one switch, number 0
PLUG_SCRIPT_ID = 1            # id of plug_watchdog.js in the plug's Scripts page
HTTP_TIMEOUT_S = 2.0          # give up on a plug request after this long
 
HEARTBEAT_PERIOD_S = 5.0      # Pi -> plug heartbeat interval
HEARTBEAT_OK_WINDOW_S = 10.0  # no answered heartbeat for this long -> Fault
PLUG_WATCHDOG_S = 20          # set in plug_watchdog.js (WATCHDOG_S); listed here for reference only
 
