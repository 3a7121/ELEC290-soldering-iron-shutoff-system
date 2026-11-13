# Soldering Iron Automatic Shut-Off: Controller Software

ELEC 290 group project. The software structure follows the **CP2 System Design & Architecture (Section 3, v5)**.

**Status:** skeleton only. Every file contains a docstring explaining what it does, which part of the design it implements, and a `TODO` checklist. Function bodies raise `NotImplementedError`. The full task list is in [`TODO.md`](TODO.md).

## What the system does

A Raspberry Pi 4B watches one soldering workstation. When the iron is on and nobody is there, it waits (**Grace**, 3 min, green LED blinks), then warns (**Warning**, 2 min, yellow LED + buzzer), then cuts power to the iron through a Wi-Fi smart plug and checks that the power really went off (**Cut Off**). If anything goes wrong (a sensor, the plug, or the network), it goes to **Fault**. The plug has its own watchdog: if the Pi stops sending heartbeats for 20 s, the plug turns the iron off by itself.

## Hardware (from CP2)

| Part | Role | Interface |
|---|---|---|
| Raspberry Pi 4B | Controller, hosts private 2.4 GHz Wi-Fi | One Python 3 service under systemd |
| USB webcam (UVC) | Presence, primary | USB, OpenCV |
| HC-SR04 | Presence, backup (camera lost > 5 s, max 15 min) | GPIO23 TRIG, GPIO24 ECHO (divider) |
| K-type thermocouple + MAX31855 | Iron-on sensing (on the **stand**) | SPI: GPIO11 CLK, GPIO9 DO, GPIO5 CS |
| Shelly Plug US Gen4 | Switches the iron, measures power | Local HTTP RPC + on-plug script |
| Reset button | Cut Off → Idle (when stand cooled) | GPIO17 (pull-up) |
| LEDs green / yellow / red | Status | GPIO16 / GPIO20 / GPIO21 |
| Piezo buzzer (via NPN) | Warning / Fault alarm | GPIO18 |

## File structure

```
soldering-shutoff/
├── README.md                  this file
├── TODO.md                    full task list, by phase
├── requirements.txt
├── shutoff/                   the service (python3 -m shutoff)
│   ├── __main__.py            entry point
│   ├── main.py                main loop: read → decide → act → pet watchdog
│   ├── config.py              all timers and thresholds (T_hot, P_on, ... still TBD)
│   ├── gpio_map.py            pin assignments
│   ├── state_machine.py       Idle / Attended / Grace / Warning / Cut Off / Fault
│   ├── faults.py              when to go to Fault
│   ├── service_health.py      systemd + hardware watchdog
│   ├── event_log.py           logging (evidence for verification)
│   ├── sensors/
│   │   ├── thermocouple.py    MAX31855 driver
│   │   ├── ultrasonic.py      HC-SR04 driver
│   │   ├── camera.py          webcam presence detection (on-Pi only)
│   │   ├── presence.py        camera primary, ultrasonic backup
│   │   └── iron_sensing.py    stand temp OR 30 s plug power, with hysteresis
│   ├── plug/
│   │   ├── shelly_client.py   Switch.Set / Switch.GetStatus, cut-off confirm
│   │   └── heartbeat.py       5 s heartbeat to the plug
│   └── ui/
│       ├── leds.py
│       ├── buzzer.py
│       └── button.py
├── shelly/
│   └── plug_watchdog.js       runs ON the plug: off if no heartbeat for 20 s
├── deploy/
│   ├── shutoff.service        systemd unit (auto-restart, watchdog)
│   └── setup_pi.sh            one-time Pi setup checklist
├── tools/                     run by hand during integration / CP3 measurements
│   ├── hw_selftest.py         check each part after wiring
│   ├── configure_plug.py      initial_state=off, upload watchdog script
│   ├── measure_iron_power.py  find P_on and "off" power
│   ├── calibrate_stand_temp.py find T_hot, T_cool, probe position
│   └── camera_roi.py          camera ROI, detection rate, D_present
└── tests/                     pytest, run on any laptop with fakes
    ├── conftest.py
    ├── test_state_machine.py
    ├── test_presence.py
    ├── test_iron_sensing.py
    ├── test_faults.py
    └── test_shelly_client.py
```

**Why it's split this way:** the logic (`state_machine`, `faults`, `presence`, `iron_sensing`) never touches hardware directly. It takes readings and a time value as inputs. That means most of the system can be written and tested on a laptop before the Pi is wired, and team members can work on drivers and logic in parallel.

## How the pieces connect

```
 camera ─┐
         ├─ presence ─────────┐
 ultrasonic ┘                 │
                              ▼
 thermocouple ─┐        ┌────────────┐       LEDs / buzzer
               ├─ iron ─▶   state    ├──────▶ plug off + confirm
 plug power ───┘ sensing│   machine  │
                        └─────▲──────┘
 reset button ────────────────┤
 faults (all of the above) ───┘
 heartbeat thread ──────────────────────────▶ plug watchdog script (20 s)
```

## Traceability (requirements → code)

Only requirements mentioned in the CP2 architecture notes are listed. The RTM owner should complete this table.

| Req | What the code does | Where |
|---|---|---|
| R2 | Warning alarm; ends when a person returns or power is cut; reset ignored during warnings | `state_machine.py`, `ui/buzzer.py` |
| R3 | Power switched by the Shelly Plug US Gen4 over local RPC | `plug/shelly_client.py` |
| R4 | Camera frames processed on the Pi only; nothing stored or sent | `sensors/camera.py`, `event_log.py` |
| R5 | 30 s limit: 5 s heartbeat / 20 s plug watchdog; camera loss → ultrasonic → Fault after 15 min | `plug/heartbeat.py`, `shelly/plug_watchdog.js`, `sensors/presence.py` |

## Running (once implemented)

On the Pi:
```bash
# one-time setup: follow deploy/setup_pi.sh
python3 tools/hw_selftest.py          # check wiring
python3 tools/configure_plug.py --host <plug-ip>
python3 -m shutoff                    # run in the foreground
sudo systemctl enable --now shutoff   # run as a service
journalctl -u shutoff -f              # watch the log
```

On any computer:
```bash
python3 -m pytest -q
```

## Safety notes

- The controller **always starts in Cut Off** and the plug's `initial_state` is **off**, so a restart never turns the iron back on.
- The plug's own watchdog cuts power if the Pi disappears. Test this before trusting the system.
- **Residual risk:** a welded relay in the plug can be *detected* (power still flowing after OFF) but not fixed by software. The system alarms in Fault and a person must unplug the iron.
- Power the Pi from an unswitched outlet (A4).

## Assumptions (from CP2)

A1 an energized iron draws more than P_on averaged over 30 s · A2 one system per workstation · A3 120 V iron far below 15 A · A4 Pi adapter on an unswitched outlet · A5 private Pi-hosted 2.4 GHz network.
