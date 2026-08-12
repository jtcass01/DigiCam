#!/usr/bin/env python
"""test_DigicamControl.py: Unit tests for the DigiCam Camera wrapper.

Tests that require digiCamControl to be installed, or a camera to be physically
connected, are skipped automatically so that a fresh clone passes out of the box.
Set the DIGICAM_CMD_PATH environment variable to point at your own
CameraControlCmd.exe if it lives somewhere other than the default location."""

__author__ = 'Jacob Taylor Cassady'
__email__ = 'jacobtaylorcassady@outlook.com'

from unittest import TestCase, main, skip, skipUnless
from os import environ
from os.path import join, isfile, sep
from sys import executable
from tempfile import TemporaryDirectory

from DigiCam import Camera

# Update with the path to your CameraControlCmd.exe file. This is likely found within
# digiCamControl which is likely within one of your program directories.
CAMERA_CONTROL_CMD_PATH = environ.get(
    'DIGICAM_CMD_PATH',
    join('C:' + sep, 'Program Files (x86)', 'digiCamControl', 'CameraControlCmd.exe'))

DIGICAM_INSTALLED = isfile(CAMERA_CONTROL_CMD_PATH)
REASON = f'digiCamControl not found at {CAMERA_CONTROL_CMD_PATH}'


class TestSetupScript(TestCase):
    """Tests for setup script generation. These need no camera and no digiCamControl
    install -- any existing file satisfies the constructor's path check, so the
    current Python interpreter is used as a stand-in executable."""

    def test_settings_are_written_to_script(self) -> None:
        """Every non-None setting should appear as a setcamera element."""
        with TemporaryDirectory() as directory:
            camera = Camera(control_cmd_location=executable, save_folder=directory)
            settings = Camera.Settings(aperture='2.8', iso='400')
            script_path = join(directory, 'setup.dccscript')

            camera.generate_setup_script(settings=settings, setup_script_name=script_path)

            with open(script_path, 'r', encoding='utf-8') as file:
                script = file.read()

        self.assertIn('<dccscript>', script)
        self.assertIn('value="2.8"', script)
        self.assertIn('value="400"', script)
        self.assertTrue(script.rstrip().endswith('</dccscript>'))

    def test_none_settings_are_omitted(self) -> None:
        """Settings left as None should not be written to the script."""
        with TemporaryDirectory() as directory:
            camera = Camera(control_cmd_location=executable, save_folder=directory)
            script_path = join(directory, 'setup.dccscript')

            camera.generate_setup_script(settings=Camera.Settings(iso='400'),
                                         setup_script_name=script_path)

            with open(script_path, 'r', encoding='utf-8') as file:
                script = file.read()

        self.assertIn('"iso"', script)
        self.assertNotIn('"ec"', script)
        self.assertNotIn('"shutter"', script)

    def test_aperture_uses_the_digicamcontrol_property_name(self) -> None:
        """The setting keys must match the property names digiCamControl expects."""
        keys = Camera.Settings(aperture='2.8').to_dict().keys()

        self.assertIn('aperture', keys)
        self.assertNotIn('aperature', keys)

    def test_image_type_defaults_to_jpg(self) -> None:
        """An unrecognised or absent image type should fall back to .jpg."""
        self.assertEqual(Camera.set_image_type(None), '.jpg')
        self.assertEqual(Camera.set_image_type('jpeg'), '.jpg')
        self.assertEqual(Camera.set_image_type('png'), '.png')


class TestDigiCamControl(TestCase):
    """Tests that talk to a real digiCamControl install."""

    @skipUnless(DIGICAM_INSTALLED, REASON)
    def test_camera_initialization(self) -> None:
        """The constructor should accept a valid CameraControlCmd.exe path."""
        Camera(control_cmd_location=CAMERA_CONTROL_CMD_PATH)

    @skip('Requires a camera to be connected.')
    def test_setup(self) -> None:
        """Pushes a set of settings to a connected camera."""
        test_camera = Camera(control_cmd_location=CAMERA_CONTROL_CMD_PATH)
        test_setting: Camera.Settings = Camera.Settings(aperture='2.8', exposure_control='1',
                                                        shutter_speed='1', iso='AUTO')

        test_camera.setup(test_setting)

    @skip('Requires a camera to be connected.')
    def test_capture(self) -> None:
        """Captures a single image on a connected camera."""
        test_camera = Camera(control_cmd_location=CAMERA_CONTROL_CMD_PATH)

        test_camera.capture_single_image(autofocus=True)


if __name__ == '__main__':
    main()
