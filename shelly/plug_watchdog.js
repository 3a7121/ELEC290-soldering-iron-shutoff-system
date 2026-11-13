// plug_watchdog.js - runs ON the Shelly Plug US Gen4 (Shelly scripts are
// JavaScript/mJS, not Python, so this one file is .js).
//
// Design reference: CP2 Section 3, "Plug-side watchdog script": outlet off if
// no heartbeat for 20 s. The Pi sends a heartbeat every 5 s
// (shutoff/plug/heartbeat.py). This is the last line of defence if the Pi
// crashes, hangs, or drops off Wi-Fi.
//
// TODO:
//   [ ] Register an HTTP endpoint for the heartbeat, e.g.
//         HTTPServer.registerEndpoint("heartbeat", function (req, res) { ... });
//       -> reachable at http://<plug>/script/<script-id>/heartbeat
//       (must match the mechanism chosen in heartbeat.py)
//   [ ] On each heartbeat: record Shelly.getComponentStatus("sys").uptime
//       (or restart a one-shot Timer.set(20000, false, ...)).
//   [ ] Every second (Timer.set(1000, true, ...)) or on timer expiry: if no
//       heartbeat for 20 s and the switch is on ->
//         Shelly.call("Switch.Set", { id: 0, on: false });
//   [ ] Also cut power if the switch is turned ON (button/app) while no
//       heartbeat has been received recently - otherwise someone could
//       power the iron with the Pi off. Decide with the team.
//   [ ] Set the script to run on boot (Script.SetConfig enable=true) and
//       confirm it survives a plug power cycle.
//   [ ] Upload with tools/configure_plug.py or the plug's web UI.
//   [ ] Test: stop heartbeats and time the cut-off (expect <= 20 s).

let WATCHDOG_MS = 20000;
let lastHeartbeat = 0;  // TODO: initialise so the outlet stays off until the Pi checks in

// TODO: endpoint registration

// TODO: periodic check
