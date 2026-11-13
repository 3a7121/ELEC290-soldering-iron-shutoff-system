"""
gpio_map.py - pin assignments (BCM numbering), single source of truth.

Design reference: CP2 Section 3, "Proposed GPIO map (BCM / header pin)".

    Signal              BCM     Header  Notes
    MAX31855 CLK        GPIO11  23      SPI0 SCLK
    MAX31855 DO         GPIO9   21      SPI0 MISO
    MAX31855 CS         GPIO5   29      NOT a hardware CE pin (see TODO)
    MAX31855 VCC        3V3     17
    HC-SR04 TRIG        GPIO23  16
    HC-SR04 ECHO        GPIO24  18      through 330/470 ohm divider (5 V -> ~2.9 V)
    HC-SR04 VCC         5V      2
    Reset button        GPIO17  11      to GND, internal pull-up
    LED green           GPIO16  36
    LED yellow          GPIO20  38
    LED red             GPIO21  40
    Buzzer (NPN base)   GPIO18  12      via 1 kohm; GPIO18 can do hardware PWM

TODO:
  [ ] GPIO5 is not SPI0 CE0 (GPIO8) or CE1 (GPIO7). Either move CS to GPIO8
      (header 24) and let spidev drive it, or keep GPIO5 and drive CS by hand
      in thermocouple.py (spidev with no_cs). Decide and update the report.
  [ ] Confirm LED series resistor values and note them here.
  [ ] Confirm whether the buzzer is active (on/off) or passive (needs PWM tone).
  [ ] Check against the wiring photo / schematic once the board is built.
"""

# SPI (MAX31855)
TC_CLK = 11
TC_DO = 9
TC_CS = 5

# Ultrasonic (HC-SR04)
US_TRIG = 23
US_ECHO = 24

# User interface
BUTTON_RESET = 17
LED_GREEN = 16
LED_YELLOW = 20
LED_RED = 21
BUZZER = 18
