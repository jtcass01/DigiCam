#!/usr/bin/env python
"""
Camera.py:

This script encapsulates operations to control a DSLR camera using the DigiCamControl's command
line interface. The script allows users to configure camera settings such as aperture, exposure
control, shutter speed, and ISO through the Camera.Settings class.

It supports the generation of XML-based setup scripts to configure the camera, execution of
these scripts, and direct command interaction with the camera. Image capture functionality,
both single and multiple, is provided, with optional autofocus control. Captured images can be
saved to a specified directory, and are automatically given unique names based on a collection
name and an incrementing image index.
"""
from __future__ import annotations

__author__ = 'Jacob Taylor Cassady'
__email__ = 'jacobtaylorcassady@outlook.com'

from os import system, getcwd, makedirs
from os.path import isfile
from time import sleep
from typing import Union, IO, Optional, Dict


class Camera:
    """Camera class object.  Used to control a DSLR camera using digiCamControl's command line
    interface."""

    def __init__(self, control_cmd_location: str, image_type: Optional[str] = None,
                 collection_name: str = '', save_folder: str = getcwd()):
        """Constructor.

        Args:
            control_cmd_location (str): The absolute or relative path to CameraControlCmd.exe.
            If using a Windows OS is likely held within ProgramFiles\\digiCamControl\\.

            image_type (Optional[str], optional): A string representing the image type to be
            captured.  Defaults to '.CR2' when None is passed.

            collection_name (str, optional): A string to be appended to the front of ever image
            taken. Defaults to ''.

            save_folder (str, optional): The absolute or relative path to the directory where
            images are to be saved. Defaults to getcwd()."""
        assert isfile(control_cmd_location), 'Unable to locate: ' + control_cmd_location \
            + '. Please ensure this is the correct path to CameraControlCmd.exe. ' \
            + 'It is likely held within Program Files\\digiCamControl\\'

        # Initialize variables
        self.control_cmd_location = control_cmd_location
        self.image_type = self.set_image_type(image_type)
        self.image_index = 0
        self.collection_name = collection_name
        self.save_folder = save_folder

    def setup(self, settings: Camera.Settings, setup_script_name: str = 'setup.dccscript'):
        """Drives the setup of the camera given a set of settings.  Autocodes the setup
        script and runs it.

        Args:
            settings (Camera.Settings): Each setting from this object is
            written to the provided file.

            setup_script_name (str): represents the name of the setup script.
            This script is used to configure the camera with the provided settings.
            The script name defaults to 'setup.dccscript'."""
        self.generate_setup_script(settings=settings, setup_script_name=setup_script_name)
        self.run_script(script_name=setup_script_name)

    def generate_setup_script(self, settings: Camera.Settings, setup_script_name: str):
        """Generates the setup script to set the aperture, exposure_control, shutter_speed,
        and iso of the camera if any of these values are passed.

        Args:
            settings (Camera.Settings): Each setting from this object is
            written to the provided file.

            setup_script_name (str): represents the name of the setup script.
            This script is used to configure the camera with the provided settings.
            The script name defaults to 'setup.dccscript'."""
        # Generate the setup script at the script location with the given setup_script_name
        with open(setup_script_name, 'w+', encoding='utf-8') as file:
            file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            file.write('<dccscript>\n')
            file.write(' '*2 + '<commands>\n')
            self.write_settings(file=file, settings=settings)
            file.write(' '*2 + '</commands>\n')
            file.write('</dccscript>')

    def write_settings(self, file: IO, settings: Camera.Settings) -> None:
        """Writes the passed dictionary of settings to the passed file.  If a
        setting has a value of None, it is passed over.

        Args:
            file (IO): Used to write the camera settings into the setup script.

            settings (Camera.Settings): Each setting from this object is
            written to the provided file."""
        # Write each setting in the settings dictionary to the file as long as the setting is not None
        for setting_name, setting in dict(settings).items():
            if setting is not None:
                file.write(' '*3 + f"<setcamera property=\"{setting_name}\" value=\"{setting}\"/>\n")

    def command_camera(self, command: str) -> None:
        """Creates a call to the camera using DigiCamControl

        Args:
            command (str): represents a command that should be sent to the
            camera using the DigiCamControl command line interface."""
        # Enforce directory location
        makedirs(self.save_folder, exist_ok=True)

        # Build image name
        image_name = self.collection_name + '_' + str(self.image_index) + self.image_type
        # Command Camera
        system(f'\"{self.control_cmd_location}\" /filename {self.save_folder}{image_name} {command}')

    def run_script(self, script_name: str) -> None:
        """Runs the passed script within the script location.

        Args:
            script_name (str): The name of the script that should be run to
            configure the camera."""
        # Make call to operating system
        system(f'{self.control_cmd_location} {script_name}')

    @staticmethod
    def set_image_type(image_type: Union[str, None] = None) -> str:
        """Sets the image type.  If none is given, the default .jpg is used.

        Args:
            image_type (Union[str, None], optional):  string that represents
            the type of image to be captured (for example, 'jpg', 'raw',
            'png', '.CR2'). If no image type is provided, the default is
            'jpg'. Defaults to None.

        Returns:
            str: A string representing the image type.  If none is given, the
            default .jpg is used."""
        if image_type in ['jpeg', 'jpg']:
            return '.jpg'

        if image_type == 'raw':
            return '.RAW'

        if image_type == 'png':
            return '.png'

        if image_type == '.CR2':
            return 'CR2'

        return '.jpg'

    def capture_single_image(self, autofocus: bool = False) -> None:
        """Captures a single image.  Iterates the image index to ensure a unique
        name for each image taken.

        Args:
            autofocus (bool, optional): Determines whether autofocus should be
            enabled when capturing the image. The default is False, meaning
            autofocus is not enabled unless specified. Defaults to False."""
        # Make the correct camera command depending on autofocus being enabled.
        if autofocus:
            self.command_camera('/capture')
        else:
            self.command_camera('/capturenoaf')

        # Increment the image index
        self.image_index += 1

    def capture_multiple_images(self, image_count: int, frequency: float = 1.0):
        """Captures an n number of images by repeatedly calling the capture_single_image
        function n times where n is the parameter image_count.

        Args:
            image_count (int): Specifies the number of images to be captured.

            frequency (float, optional): The frequency at which images should be captured."""
        assert frequency > 0, 'frequency must be greater than 0.'

        # Iterate over the image_count capturing a single image every time.
        for _ in range(image_count):
            self.capture_single_image()

            sleep(1/frequency)

    class Settings:
        """A helper class that holds various camera settings, such as aperture,
        exposure control, shutter speed, and ISO. These settings are used to
        configure the camera before capturing images."""

        def __init__(self, aperture: Optional[str] = None,
                     exposure_control: Optional[str] = None,
                     shutter_speed: Optional[str] = None,
                     iso: Optional[Union[int, str]] = None) -> None:
            self.aperture: Optional[str] = aperture
            self.exposure_control: Optional[str] = exposure_control
            self.shutter_speed: Optional[str] = shutter_speed
            self.iso: Optional[str] = iso

        def __dict__(self) -> Dict[str, Union[None, str, int]]:
            return {'aperature': self.aperture,
                    'ec': self.exposure_control,
                    'shutter': self.shutter_speed,
                    'iso': self.iso}


if __name__ == '__main__':
    pass
