"""
ultrasonic.py - HC-SR04 backup presence sensor.

Design reference: CP2 Section 3, "Presence (backup)" and GPIO map
(TRIG GPIO23, ECHO GPIO24 through 330/470 ohm divider, 5 V supply).

Only used when the camera has given no usable frame for 5 s, and only for
at most 15 min; after that the system goes to Fault (logic in presence.py).

HC-SR04 basics: 10 us HIGH pulse on TRIG; ECHO goes HIGH for a time equal to
the round trip. distance_cm = echo_seconds * 34300 / 2. Range ~2-400 cm.
No echo within ~38 ms means nothing in range. Wait >= 60 ms between pings.

TODO:
  [ ] Implement measure_cm() with gpiozero.DistanceSensor (simplest) or
      RPi.GPIO / lgpio edge timing. Return None on timeout.
  [ ] Median of 3-5 pings to reject spikes.
  [ ] is_present(): distance < D_PRESENT_CM (config.py).
  [ ] is_healthy(): False if every ping in the last few seconds timed out or
      gave impossible values (lets faults.py detect "both sources lost").
  [ ] CP3: aim the sensor at the user's seat and pick D_PRESENT_CM
      (tools/camera_roi.py also logs ultrasonic distances).
  [ ] Verify the divider output on ECHO is <= 3.3 V with a meter (~2.9 V expected).
"""


class Ultrasonic:
    def __init__(self, trig_pin: int, echo_pin: int):
        """TODO: set up GPIO."""
        raise NotImplementedError

    def measure_cm(self) -> float | None:
        """TODO: one filtered distance, or None."""
        raise NotImplementedError

    def is_present(self) -> bool | None:
        """TODO: None if no valid reading."""
        raise NotImplementedError

    def is_healthy(self) -> bool:
        """TODO"""
        raise NotImplementedError

    def close(self) -> None:
        """TODO"""
        raise NotImplementedError
