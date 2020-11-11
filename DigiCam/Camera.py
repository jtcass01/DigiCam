#!/usr/bin/env python
"""Camera.py:"""

__author__ = "Jacob Taylor Cassady"
__email__ = "jacobtaylorcassady@outlook.com"

from os import system, getcwd
from os.path import isfile
from typing import Union, IO

from DigiCam.FileSystem import FileSystem


class Camera(object):
    """Camera class object.  Used to control a DSLR camera using digiCamControl's command line interface."""
    def __init__(self, control_cmd_location: str, image_type: Union[str, None] = None, collection_name: str = "", save_folder: Union[str] = getcwd()):
        """Constructor.

        Args:
            control_cmd_location (str): The absolute or relative path to CameraControlCmd.exe.  If using a Windows OS is likely held within ProgramFiles\\digiCamControl\\.
            image_type (Union[str, None], optional): A string representing the image type to be captured.  Defaults to '.CR2' when None is passed.
            collection_name (str, optional): A string to be appended to the front of ever image taken. Defaults to "".
            save_folder (Union[str], optional): The absolute or relative path to the directory where images are to be saved. Defaults to getcwd()."""
        assert isfile(control_cmd_location), "Unable to locate: " + control_cmd_location + '. Please ensure this is the correct path to CameraControlCmd.exe. ' \
                                            + 'It is likely held within Program Files\\digiCamControl\\'

        # Initialize variables
        self.control_cmd_location = control_cmd_location
        self.image_type = self.set_image_type(image_type)
        self.image_index = 0
        self.collection_name = collection_name
        self.save_folder = save_folder

    def setup(self, aperture: Union[str, None] = None, exposure_control: Union[str, None] = None, shutter_speed: Union[str, None] = None,
              iso: Union[int, str, None] = None, setup_script_name: str = "setup.dccscript"):
        """Drives the setup of the camera given a set of settings.  Autocodes the setup script and runs it.

        Args:
            aperture (Union[str, None], optional): [description]. Defaults to None.
            exposure_control (Union[str, None], optional): [description]. Defaults to None.
            shutter_speed (Union[str, None], optional): [description]. Defaults to None.
            iso (Union[int, str, None], optional): [description]. Defaults to None.
            setup_script_name (str, optional): [description]. Defaults to "setup.dccscript"."""
        self.generate_setup_script(setup_script_name=setup_script_name, aperture=aperture, exposure_control=exposure_control,
                                   shutter_speed=shutter_speed, iso=iso)
        self.run_script(script_name=setup_script_name)

    def generate_setup_script(self, setup_script_name: str, aperture: Union[str, None] = None, exposure_control: Union[str, None] = None, 
                              shutter_speed: Union[str, None] = None, iso: Union[int, str, None] = None):
        """Generates the setup script to set the aperture, exposure_control, shutter_speed, and iso of the camera if any of these values are passed.

        Args:
            setup_script_name (str): [description]
            aperture (Union[str, None], optional): [description]. Defaults to None.
            exposure_control (Union[str, None], optional): [description]. Defaults to None.
            shutter_speed (Union[str, None], optional): [description]. Defaults to None.
            iso (Union[int, str, None], optional): [description]. Defaults to None."""
        # Compile the settings into a dictionary
        settings = {"aperture" : aperture,
                    "ec" : exposure_control,
                    "shutter" : shutter_speed,
                    "iso" : iso}

        # Enforce directory location
        FileSystem.enforce_path(self.script_location)

        # Generate the setup script at the script location with the given setup_script_name
        with open(self.script_location + setup_script_name, "w+") as file:
            file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            file.write("<dccscript>\n")
            file.write(" "*2 + "<commands>\n")
            self.write_settings(file, settings)
            file.write(" "*2 + "</commands>\n")
            file.write("</dccscript>")

    def write_settings(self, file: IO, settings: dict) -> None:
        """Writes the passed dictionary of settings to the passed file.  If a setting has a value of None, it is passed over.

        Args:
            file (IO): [description]
            settings (dict): [description]"""
        # Write each setting in the settings dictionary to the file as long as the setting is not None
        for setting in settings.keys():
            if settings[setting] is not None:
                file.write(" "*3 + "<setcamera property=\"" + str(setting) + "\" value=\"" + str(settings[setting]) + "\"/>\n")

    def command_camera(self, command: str) -> None:
        """Creates a call to the camera using DigiCamControl

        Args:
            command (str): [description]"""
        # Enforce directory location
        FileSystem.enforce_path(self.save_folder)

        # Build image name
        image_name = self.collection_name + "_" + str(self.image_index) + self.image_type
        # Command Camera
        system('\"' + self.control_cmd_location + "\" /filename "  +  self.save_folder + image_name +  " " + command)

    def run_script(self, script_name: str) -> None:
        """Runs the passed script within the script location.

        Args:
            script_name (str): [description]"""
        # Enforce directory location
        FileSystem.enforce_path(self.script_location)

        # Make call to operating system
        system(self.control_cmd_location + " " + self.script_location + script_name)

    @staticmethod
    def set_image_type(image_type: Union[str, None] = None) -> str:
        """Sets the image type.  If none is given, the default .jpg is used.

        Args:
            image_type (Union[str, None], optional): [description]. Defaults to None.

        Returns:
            str: A string representing the image type.  If none is given, the default .jpg is used."""
        if image_type == "jpeg" or image_type == "jpg":
            return ".jpg"
        elif image_type == 'raw':
            return ".RAW"
        elif image_type == 'png':
            return ".png"
        elif image_type == '.CR2':
            return 'CR2'
        else:
            return ".jpg"

    def capture_single_image(self, autofocus: bool = False) -> None:
        """Captures a single image.  Iterates the image index to ensure a unique name for each image taken.

        Args:
            autofocus (bool, optional): [description]. Defaults to False."""
        # Make the correct camera command depending on autofocus being enabled.
        if autofocus:
            self.command_camera("/capture")
        else:
            self.command_camera("/capturenoaf")

        # Increment the image index
        self.image_index += 1

    def capture_multiple_images(self, image_count):
        """Captures an n number of images by repeatedly calling the capture_single_image function n times where n is the parameter image_count.

        Args:
            image_count ([type]): [description]"""
        # Iterate over the image_count capturing a single image every time.
        for capture in range(image_count):
            self.capture_single_image()


if __name__ == "__main__":
    pass