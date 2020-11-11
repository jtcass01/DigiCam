#!/usr/bin/env python
"""unit_tests.py:"""

__author__ = "Jacob Taylor Cassady"
__email__ = "jacobtaylorcassady@outlook.com"

from unittest import TestCase, main, skip
from os.path import join, sep
from DigiCam.Camera import Camera

# Update with the path to your CameraControlCmd.exe file.  This is likely found within digiCamControl which is likely within one of your program directories.
CAMERA_CONTROL_CMD_PATH = join('C:' + sep, 'Program Files (x86)', 'digiCamControl', 'CameraControlCmd.exe')


class TestDigiCamControl(TestCase):
    """[summary]"""
    def test_camera_initialization(self) -> None:
        """[summary]"""
        Camera(control_cmd_location=CAMERA_CONTROL_CMD_PATH)

    @skip # Skipped by default because a camera must be connected for this test to pass.
    def test_setup(self) -> None:
        """[summary]"""
        test_camera = Camera(control_cmd_location=CAMERA_CONTROL_CMD_PATH)

        test_camera.setup(aperture='2.8', exposure_control='1', shutter_speed='1', iso='AUTO')

    @skip # Skipped by default because a camera must be connected for this test to pass.
    def test_capture(self) -> None:
        """[summary]"""
        test_camera = Camera(control_cmd_location=CAMERA_CONTROL_CMD_PATH)

        test_camera.capture_single_image(autofocus=True)


if __name__ == "__main__":
    main()