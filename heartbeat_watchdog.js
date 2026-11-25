// plug_watchdog.js - runs ON the Shelly Plug US Gen4, not on the Pi.
//
// Last line of defence: if the Pi crashes, hangs, loses power or drops off
// Wi-Fi, its heartbeats stop and this script turns the outlet off by itself.
//
//   - The Pi calls  GET http://<plug-ip>/script/<script-id>/heartbeat  every 5 s
//     (heartbeat.py). This script creates that URL.
//   - No heartbeat for 20 s  -> outlet off.
//   - Outlet turned on (plug button / app / RPC) while no heartbeat is
//     arriving -> switched straight back off, so the iron can't be powered
//     while the Pi isn't watching.
//   - Script (re)start -> outlet off, until the Pi checks in.
//
// Worst case from the Pi's last heartbeat to power off:
//   20 s timeout + up to 1 s until the next check + 1 s uptime resolution = ~22 s
//
// Install: plug web page (http://<plug-ip>) -> Scripts -> create script,
// paste this file, Save, Start, and turn on "Run on startup".
// The script id (usually 1 for the first script) goes in heartbeat.py.
//
// Written without arrow functions or template strings to stay inside the
// JavaScript subset Shelly scripts support.

let WATCHDOG_S = 20;   // cut power after this many seconds without a heartbeat
let CHECK_MS = 1000;   // how often to check, in milliseconds

let alive = false;     // true while heartbeats are arriving
let lastBeat = 0;      // plug uptime (s) of the last heartbeat

// Seconds since the plug booted. Used as the clock because it keeps counting
// even without internet time (the plug has no NTP on the Pi's network).
function now() {
    return Shelly.getComponentStatus("sys").uptime;
}

// Turn the outlet off. Shelly API call: Switch.Set, same as the Pi uses.
function cutOff(reason) {
    print("watchdog: outlet off (" + reason + ")");
    Shelly.call("Switch.Set", { id: 0, on: false });
}

// Create the heartbeat URL: http://<plug-ip>/script/<script-id>/heartbeat
// Every request to it marks the Pi as alive and records the time.
HTTPServer.registerEndpoint("heartbeat", function (request, response) {
    if (!alive) {
        print("watchdog: heartbeat received, Pi is alive");
    }
    alive = true;
    lastBeat = now();
    response.code = 200;
    response.body = "ok";
    response.send();   // must reply, or the Pi's request waits until its timeout
});

// Once a second: if heartbeats have stopped for too long, cut power.
Timer.set(CHECK_MS, true, function () {
    if (alive && now() - lastBeat > WATCHDOG_S) {
        alive = false;
        cutOff("no heartbeat for " + WATCHDOG_S + " s");
    }
});

// Watch for the outlet being turned on. If the Pi isn't sending heartbeats,
// switch it straight back off.
// Status events look like: { component: "switch:0", delta: { output: true, ... } }
Shelly.addStatusHandler(function (event) {
    if (event.component === "switch:0" && event.delta && event.delta.output === true) {
        if (!alive) {
            cutOff("turned on with no heartbeat");
        }
    }
});

// Fail safe on start: outlet off until the Pi checks in.
cutOff("script started");
