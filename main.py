"""
main.py - soldering iron automatic shut-off: main loop + state machine.

Hardware code lives in separate files, one per part; main.py only calls them:
    plug.py, heartbeat.py   smart plug control and the heartbeat to its watchdog script
    object_detect.py        camera presence (PresenceMonitor)
    buttons.py              kill and reset buttons
    display.py              TFT screen
    indicators.py           LEDs and buzzer

PLACEHOLDER:
    read_temperature() is a placeholder for the temperature reading. It returns
    a fixed 22 °C until the temperature sensor file (GY-906 / MLX90614) exists;
    then it should call that file and return °C, or None if the sensor fails.
"""

import math
import time
from datetime import datetime

import heartbeat
import plug
from buttons import Buttons
from display import Display
from indicators import Indicators
from object_detect import PresenceMonitor, CameraError

LEAVE_AFTER = 2 # seconds without a detection before someone counts as gone (smooths missed frames)
AWAY_TIMEOUT = 30 # seconds gone before the iron's power is cut
HOT_TEMPERATURE = 50 # °C, at or above this the iron counts as hot (set this from your own readings)
MAX_TEMPERATURE = 380 # °C, top of the MLX90614's range, so a reading this high can't be trusted
CHECK_INTERVAL = 0.2 # seconds between camera checks
PLUG_STARTUP_GRACE = 30 # seconds after start before a missing heartbeat counts as a plug fault (plug rejoining Wi-Fi)

IDLE, ACTIVE, AWAY, COOLING, FAULT, STOPPED = "IDLE", "ACTIVE", "AWAY", "COOLING", "FAULT", "STOPPED"

SCREEN_COLOURS = { # background colour for each state, as (red, green, blue)
    IDLE: (0, 110, 0),
    ACTIVE: (170, 90, 0),
    AWAY: (170, 90, 0),
    COOLING: (150, 0, 0),
    STOPPED: (90, 0, 0),
    FAULT: (200, 0, 0),
}

# Set up in main(). Each stays None if that part can't be started, and the system carries on without it.
screen = None
indicators = None
buttons = None


def log(message):
    print(f"[{datetime.now():%H:%M:%S}] {message}")


# ----- Hardware -----

def set_iron_power(on):
    """Switch the smart plug. Returns True if the plug accepted the command,
    False if it couldn't be reached (the caller treats that as a fault)."""
    log("Iron power ON" if on else "Iron power OFF")
    try:
        if on:
            plug.turn_on()
        else:
            plug.turn_off()
        return True
    except plug.PlugError as error:
        log(f"Plug error: {error}")
        return False


def read_temperature():
    return 22.0 # placeholder: pretends the iron is at room temperature
    # return thermometer.read() GY-906 (MLX90614) infrared sensor in °C, or None if the sensor fails


def update_indicators(state, hot, line1, line2):
    log(f"{state:<8} Screen: {line1:<16} | {line2}")
    if screen:
        screen.show(line1, line2, background=SCREEN_COLOURS[state])
    if indicators:
        indicators.show(state, hot)


def beep(times=1, length=0.1):
    if indicators:
        indicators.beep(times, length)


def alarm(on):
    if indicators:
        if on:
            indicators.alarm()
        else:
            indicators.quiet()


def check_buttons():
    """Returns (kill pressed, reset pressed) since the last check."""
    if not buttons:
        return False, False
    return buttons.kill_pressed(), buttons.reset_pressed()


def start(name, create):
    try:
        return create()
    except Exception as error:
        log(f"{name} not available ({error}), carrying on without it")
        return None


# ----- State machine -----

class Controller:
    def __init__(self):
        self.state = IDLE
        self.power_on = False
        self.away_since = 0.0
        self.fault_reason = ""
        self.shown = None
        self.started = time.monotonic() # for the plug start-up grace period
        set_iron_power(False) # always start from a safe state

    def step(self, person_present, now, kill=False, reset=False):
        if kill and self.state != STOPPED:
            self.change_to(STOPPED, now)
        elif reset and self.state in (STOPPED, FAULT):
            self.change_to(IDLE, now)

        if self.state in (STOPPED, FAULT):
            self.show(None, False, now)
            return # stays here until the reset button is pressed

        # The plug has stopped answering heartbeats: it can't be controlled.
        # (It also cuts power by itself within ~20 s once heartbeats stop reaching it.)
        if not heartbeat.heartbeat_ok() and now - self.started > PLUG_STARTUP_GRACE:
            self.fault("plug", now)
            return

        temperature = read_temperature()
        if temperature is None:
            self.fault("sensor", now)
            return
        if temperature > MAX_TEMPERATURE:
            self.fault("overheat", now)
            return

        hot = temperature >= HOT_TEMPERATURE

        if self.state == IDLE:
            if person_present:
                self.change_to(ACTIVE, now)
            elif hot:
                self.change_to(COOLING, now) # hot with the power off, e.g. after a restart

        elif self.state == ACTIVE:
            if not person_present:
                self.change_to(AWAY, now)

        elif self.state == AWAY:
            if person_present:
                self.change_to(ACTIVE, now)
            elif now - self.away_since > AWAY_TIMEOUT:
                self.change_to(COOLING, now)

        elif self.state == COOLING:
            if person_present:
                self.change_to(ACTIVE, now)
            elif not hot:
                self.change_to(IDLE, now)

        self.show(temperature, hot, now)

    def fault(self, reason, now):
        if self.state != FAULT:
            self.fault_reason = reason
            self.change_to(FAULT, now)
        self.show(None, False, now)

    def change_to(self, new_state, now):
        log(f"{self.state} -> {new_state}")
        old_state, self.state = self.state, new_state

        if new_state == ACTIVE:
            self.set_power(True)
        elif new_state == AWAY:
            self.away_since = now # power stays on during the countdown
        else:
            self.set_power(False)

        if self.state != new_state:
            return # set_power failed and moved us to FAULT; skip the beeps below

        if new_state == FAULT:
            alarm(True)
        elif new_state == STOPPED:
            alarm(False)
            beep(length=0.6) # kill switch pressed
        elif old_state in (FAULT, STOPPED):
            alarm(False)
            beep() # reset accepted
        elif new_state == AWAY:
            beep() # countdown started
        elif new_state == COOLING and old_state == AWAY:
            beep(times=2) # power has just been cut

    def set_power(self, on):
        if on != self.power_on:
            ok = set_iron_power(on)
            self.power_on = on
            if not ok:
                # Plug unreachable. If it can't be reached, heartbeats can't
                # reach it either, so the plug cuts power itself within ~20 s.
                self.fault("plug", time.monotonic())

    def show(self, temperature, hot, now):
        reading = f"Iron {temperature:.0f}C" if temperature is not None else "Iron ---C"

        if self.state == IDLE:
            lines = ("Ready", reading)
        elif self.state == ACTIVE:
            lines = ("Power ON", reading)
        elif self.state == AWAY:
            seconds_left = max(0, math.ceil(AWAY_TIMEOUT - (now - self.away_since)))
            lines = (f"Away: off in {seconds_left}s", reading)
        elif self.state == COOLING:
            lines = ("HOT! Don't touch", reading)
        elif self.state == STOPPED:
            lines = ("STOPPED", "Press reset")
        else:
            lines = (f"FAULT: {self.fault_reason}", "Fix, then reset")

        # Only update when something changed, so the screen isn't redrawn 5 times a second
        if (self.state, hot, lines) != self.shown:
            update_indicators(self.state, hot, *lines)
            self.shown = (self.state, hot, lines)


# ----- Main loop -----

def run(controller):
    """Watches the camera until it fails (raises CameraError)."""
    with PresenceMonitor(leave_after=LEAVE_AFTER) as presence:
        log("System running. Press Ctrl+C to stop.")
        while True:
            # Heartbeat first, every loop: the plug refuses to turn on until it
            # has heard one, and if this loop ever hangs the heartbeats stop
            # and the plug cuts power by itself.
            heartbeat.update()
            presence.update()
            kill, reset = check_buttons()
            controller.step(presence.person_present, time.monotonic(), kill, reset)
            time.sleep(CHECK_INTERVAL)


def wait_for_reset(controller):
    """After a camera fault, waits for the reset button before trying the camera again."""
    log("Waiting for the reset button (or Ctrl+C to quit)")
    while controller.state in (FAULT, STOPPED):
        heartbeat.update() # keep the plug's watchdog fed while waiting
        kill, reset = check_buttons()
        if kill or reset:
            controller.step(False, time.monotonic(), kill, reset)
        time.sleep(0.1)


def shut_down(controller):
    set_iron_power(False) # whatever happened, leave the iron off
    if indicators:
        indicators.close()
    if buttons:
        buttons.close()
    if screen:
        if controller.state not in (FAULT, STOPPED): # a fault or stop message stays on screen
            screen.show("System stopped", "Iron power OFF")
        screen.close()


def main():
    global screen, indicators, buttons
    screen = start("Screen", Display)
    indicators = start("LEDs and buzzer", Indicators)
    buttons = start("Buttons", Buttons)
    controller = Controller()

    try:
        while True:
            try:
                run(controller)
            except CameraError as error:
                log(f"Error: {error}")
                controller.fault("camera", time.monotonic())
                wait_for_reset(controller)
    except FileNotFoundError as error:
        log(f"Error: {error}")
        controller.fault("model", time.monotonic())
    except KeyboardInterrupt:
        log("Stopping")
    finally:
        shut_down(controller)


if __name__ == "__main__":
    main()
