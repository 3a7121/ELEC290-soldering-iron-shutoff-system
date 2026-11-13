"""
thermocouple.py - MAX31855 + K-type thermocouple on the iron STAND.

Design reference: CP2 Section 3, "Iron-on sensing" and GPIO map
(CLK GPIO11, DO GPIO9, CS GPIO5, 3.3 V). Probe is insulated and mounted on
the stand, not on the iron.

MAX31855 basics: read-only SPI, 32 bits per read.
  bits 31..18  thermocouple temperature, 14-bit signed, 0.25 C/LSB
  bit  16      fault flag (any fault)
  bits 15..4   internal (cold-junction) temperature, 12-bit signed, 0.0625 C/LSB
  bit  2       SCV  short to VCC
  bit  1       SCG  short to GND
  bit  0       OC   open circuit (probe disconnected)
Max conversion time ~100 ms, so read at <= 10 Hz.

TODO:
  [ ] Resolve the CS pin question in gpio_map.py (GPIO5 vs hardware CE0).
  [ ] Implement read_raw() with spidev (SPI0, mode 0, <= 5 MHz) or the
      adafruit-circuitpython-max31855 library.
  [ ] Implement decode(raw) -> Reading (temp, internal temp, fault bits).
      Pure function, so it can be unit tested with known bit patterns.
  [ ] Track the time of the last good reading (faults.py needs "5 s without data").
  [ ] Reject obviously bad values (e.g. jumps > X C between reads) -> count as no data.
  [ ] Optional: median of the last 3 readings to reduce noise.
  [ ] CP3: pick probe position on the stand and measure stand temperature vs
      time with the iron in / out (tools/calibrate_stand_temp.py).
  [ ] CP3: check whether the MAX31855 breakout has its own regulator and input
      capacitor; add a 0.1 uF cap near VCC if not.
"""

from dataclasses import dataclass


@dataclass
class Reading:
    temp_c: float | None
    internal_c: float | None
    fault: bool
    open_circuit: bool
    short_gnd: bool
    short_vcc: bool
    timestamp: float


def decode(raw: int, timestamp: float) -> Reading:
    """TODO: decode the 32-bit frame described above."""
    raise NotImplementedError


class Thermocouple:
    def __init__(self, spi_bus: int = 0, spi_device: int = 0):
        """TODO: open SPI (and set up manual CS if CS stays on GPIO5)."""
        raise NotImplementedError

    def read(self) -> Reading:
        """TODO: read_raw() + decode(); update last_good_time."""
        raise NotImplementedError

    def seconds_since_good(self, now: float) -> float:
        """TODO: used by faults.py for the 5 s timeout."""
        raise NotImplementedError

    def close(self) -> None:
        """TODO"""
        raise NotImplementedError
