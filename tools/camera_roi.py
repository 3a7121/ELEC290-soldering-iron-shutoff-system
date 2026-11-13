"""
tools/camera_roi.py - choose the camera region of interest and D_present (CP3 open items).

Runs the presence detector live and prints results so the team can aim the
camera and ultrasonic sensor at the workstation.

TODO:
  [ ] Show a live preview with the ROI rectangle (only on a monitor attached
      to the Pi; nothing saved or sent - R4).
  [ ] Keys to move / resize the ROI; print the final (x, y, w, h) for config.py.
  [ ] Print detections per second and detection rate over a test session
      (seated, leaning, standing up, walking away).
  [ ] Also print ultrasonic distance alongside, to pick D_PRESENT_CM.
  [ ] Summary for CP3: detection rate, false absences, FPS on the Pi 4B.
"""


def main() -> int:
    """TODO"""
    raise NotImplementedError


if __name__ == "__main__":
    raise SystemExit(main())
