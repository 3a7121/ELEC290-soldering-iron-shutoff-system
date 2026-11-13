# TODO: Soldering Iron Auto Shut-Off Software

Work through it roughly in phase order. Phases 2 and 3 can run in parallel: drivers need the hardware, logic doesn't. Each item names the file that holds the detailed checklist. Put initials next to an item when you take it.

## Phase 0: Decisions to settle first
- [ ] Thermocouple CS pin: GPIO5 (manual CS) or move to GPIO8/CE0. Update the report if it changes. (`gpio_map.py`)
- [ ] Buzzer type: active or passive. (`ui/buzzer.py`)
- [ ] LED and buzzer meaning for **every** state, not just Grace/Warning. (`state_machine.py`, `ui/leds.py`)
- [ ] From Idle with the iron on and nobody present: go to Attended or straight to Grace? Match the state diagram. (`state_machine.py`)
- [ ] Does entering Fault also command the plug OFF? (recommended) (`state_machine.py`)
- [ ] Does the controller ever turn the plug ON, or does the user do it? (`plug/shelly_client.py`)
- [ ] Should the plug script block the outlet being turned on while no heartbeat is arriving? (`shelly/plug_watchdog.js`)
- [ ] Heartbeat mechanism: script HTTP endpoint vs KVS. (`plug/heartbeat.py`, `shelly/plug_watchdog.js`)
- [ ] Camera detection method (face / person / motion). (`sensors/camera.py`)
- [ ] Reset: short tap or long press? (`ui/button.py`)
- [ ] How faults clear (delay before Fault → Cut Off). (`faults.py`, `config.py`)

## Phase 1: Pi and network setup
- [ ] Raspberry Pi OS installed, SPI enabled, hardware watchdog on. (`deploy/setup_pi.sh`)
- [ ] Pi-hosted private 2.4 GHz network starting on boot (A5).
- [ ] Plug joined to the Pi network with a fixed IP → `config.PLUG_HOST`.
- [ ] Python packages installed. (`requirements.txt`)
- [ ] Repo cloned on the Pi; everyone can push/pull.

## Phase 2: Drivers (need hardware)
- [ ] MAX31855 read + decode + fault bits. (`sensors/thermocouple.py`)
- [ ] HC-SR04 distance + health. (`sensors/ultrasonic.py`)
- [ ] Webcam capture thread + presence detection, no frames saved (R4). (`sensors/camera.py`)
- [ ] Shelly RPC: status, off, cut-off confirm, initial_state off. (`plug/shelly_client.py`)
- [ ] Plug watchdog script on the plug. (`shelly/plug_watchdog.js`, `tools/configure_plug.py`)
- [ ] LEDs, buzzer, button. (`ui/`)
- [ ] Hardware self-test passes for every part. (`tools/hw_selftest.py`)

## Phase 3: Logic (laptop is fine)
- [ ] Config values + `validate()`. (`config.py`)
- [ ] 30 s power averager + iron-on hysteresis. (`sensors/iron_sensing.py`)
- [ ] Camera → ultrasonic fallback, 5 s / 15 min rules. (`sensors/presence.py`)
- [ ] Fault monitor, all 8 fault codes. (`faults.py`)
- [ ] State machine, all transitions. (`state_machine.py`)
- [ ] Heartbeat thread. (`plug/heartbeat.py`)
- [ ] Logging + CSV test logs. (`event_log.py`)
- [ ] Fakes + unit tests passing. (`tests/`)

## Phase 4: Integration
- [ ] Main loop wiring everything together. (`main.py`)
- [ ] systemd notify + watchdog petting. (`service_health.py`)
- [ ] Install and enable the service. (`deploy/shutoff.service`)
- [ ] Measure loop rate / detection rate with the camera running.
- [ ] Measure Pi current with a USB-C meter (~2.0 A expected on a 3 A supply).

## Phase 5: Verification tests (record results for CP3)
- [ ] Full sequence: leave → Grace at once → Warning at 3:00 → Cut Off at 5:00, OFF confirmed.
- [ ] Return during Grace and during Warning → back to Attended, alarm stops (R2).
- [ ] Reset ignored during Grace/Warning; Cut Off → Idle only when cooled AND reset.
- [ ] Unplug camera → ultrasonic within 5 s → Fault after 15 min (R5).
- [ ] Unplug thermocouple → Fault within 5 s.
- [ ] Kill the service / pull Pi power → plug off within 20 s (R5 30 s limit).
- [ ] Hang the service (`kill -STOP`) → systemd restarts it → starts in Cut Off.
- [ ] Plug unreachable (turn off Wi-Fi) → Fault.
- [ ] Restart the plug → outlet comes back OFF.

## Phase 6: CP3 measurements (open items from CP2)
- [ ] T_hot, T_cool and probe position. (`tools/calibrate_stand_temp.py`)
- [ ] P_on and the "off" power level on the lab's irons; confirms A1. (`tools/measure_iron_power.py`)
- [ ] Validate 3 min / 2 min / 5 s / 20 s / 15 min.
- [ ] D_present and camera ROI. (`tools/camera_roi.py`)
- [ ] Detection rate on the Pi.
- [ ] Plug's Canadian certification mark.
- [ ] Whether the MAX31855 module has its own regulator and input capacitor.

## Report / RTM updates (from CP2 notes)
- [ ] R5 verification: camera disconnect → ultrasonic backup → Fault after 15 min (not "power cut").
- [ ] R2: warning ends when a person returns or power is cut; reset ignored during warnings.
- [ ] R3 status: Shelly Plug US Gen4 (not Shelly Plus).
- [ ] R4 status: frames processed on the Pi, nothing sent (remove "encrypting camera data").
- [ ] Add any pin / behaviour changes from Phase 0 to Section 3.
