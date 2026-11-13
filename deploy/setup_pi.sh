#!/usr/bin/env bash
# setup_pi.sh - one-time Raspberry Pi 4B setup (Raspberry Pi OS).
# This is a CHECKLIST with suggested commands, not a tested script yet.
# Run steps by hand the first time, then turn it into a real script.
#
# TODO:
#   [ ] Enable SPI:                 sudo raspi-config nonint do_spi 0
#   [ ] Hardware watchdog:          add "dtparam=watchdog=on" to /boot/firmware/config.txt
#                                   set RuntimeWatchdogSec=15 in /etc/systemd/system.conf
#   [ ] Packages:                   sudo apt install python3-gpiozero python3-spidev \
#                                     python3-opencv python3-requests python3-pytest
#                                   (or pip install -r requirements.txt in a venv)
#   [ ] User groups:                sudo usermod -aG gpio,spi,video pi
#   [ ] Private 2.4 GHz network hosted by the Pi (assumption A5), e.g. with
#       NetworkManager on Bookworm:
#         sudo nmcli device wifi hotspot ifname wlan0 ssid <SSID> password <PASS> band bg
#       then make it start on boot (nmcli connection modify Hotspot connection.autoconnect yes)
#   [ ] Give the plug a fixed address (DHCP reservation or static IP on the plug);
#       put it in shutoff/config.py PLUG_HOST.
#   [ ] Configure the plug: python3 tools/configure_plug.py
#   [ ] Install the service: see deploy/shutoff.service
#   [ ] Power the Pi from an UNSWITCHED outlet (assumption A4), 3 A USB-C supply.
#   [ ] Check power with a USB-C meter during integration (~2.0 A expected).

set -euo pipefail
echo "setup_pi.sh is a checklist - read the comments and run the steps by hand."
