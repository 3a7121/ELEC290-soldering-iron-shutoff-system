"""
camera.py - USB webcam (UVC) primary presence sensor.

Design reference: CP2 Section 3, "Presence (primary)": one USB webcam on or
near the Pi, facing the user at ONE workstation. Microphone unused.
R4 (privacy): frames are processed on the Pi only. Nothing is stored or sent.

TODO:
  [ ] Open the camera with OpenCV (cv2.VideoCapture(CAMERA_INDEX)), low
      resolution (e.g. 320x240) to keep detection fast on the Pi 4B.
  [ ] Choose a detection method and justify it in the report:
        - face detection (Haar cascade / OpenCV DNN face model), or
        - person detection (HOG + SVM), or
        - motion in the region of interest (frame differencing) as a fallback.
      Compare detection rate and speed on the Pi (CP3 open item).
  [ ] Crop to CAMERA_ROI (config.py) before detecting.
  [ ] Implement get_presence() -> (present: bool | None, frame_ok: bool).
      frame_ok False when read() fails, frame is black/frozen, etc.
  [ ] Track time of last usable frame (presence.py needs the 5 s rule).
  [ ] Optional smoothing: "present" if detected in k of the last n frames,
      so one missed frame does not start Grace.
  [ ] Run capture in its own thread so a slow USB read never stalls the loop.
  [ ] R4: never call cv2.imwrite / send frames anywhere; release the frame
      after processing. Keep the mic disabled. Note this in the report.
  [ ] Handle the camera being unplugged and re-plugged (reopen with backoff).
"""


class Camera:
    def __init__(self, index: int, roi=None):
        """TODO: open the device, set resolution, load the detector."""
        raise NotImplementedError

    def get_presence(self) -> tuple[bool | None, bool]:
        """TODO: (present, frame_ok) from the latest frame."""
        raise NotImplementedError

    def seconds_since_usable_frame(self, now: float) -> float:
        """TODO"""
        raise NotImplementedError

    def close(self) -> None:
        """TODO: release the device."""
        raise NotImplementedError
