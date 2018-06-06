import os

class Camera(object):
    """
    Class Description:
    Camera Object used to communicate with cameras connected to the computer.

    Author(s):
    Jacob Taylor Cassady

    Dates: 
    Created - 6/5/18
    Updated - 6/5/18
    """
    def __init__(self, control_cmd_location = None, save_folder_path=None, script_path = None, image_type=None, image_name=None):
        # Initialize variables
        self.control_cmd_location = self.set_control_cmd_location(control_cmd_location)
        self.save_folder = self.set_save_folder(save_folder_path)
        self.script_location = self.set_script_path(script_path)
        self.image_type = self.set_image_type(image_type)
        self.image_name = image_name
        self.image_index = 0


    def set_control_cmd_location(self, control_cmd_location=None):
        """
        Function Description:
        Sets the location of CameraControlCmd.exe which is used to command a camera from the command line using the program DigiCamControl.

        Author(s):
        Jacob Taylor Cassady

        Dates:
        Created - 6/5/18
        Updated - 6/5/18
        """
        if control_cmd_location is None:
            control_cmd_location = "\"C:\\Program Files (x86)\\digiCamControl\\CameraControlCmd.exe\""

        return control_cmd_location

    def command_camera(self, command):
        """
        Function Description:
        Creates a call to the camera using DigiCamControl

        Author(s):
        Jacob Taylor Cassady

        Dates:
        Created - 6/5/18
        Updated - 6/5/18
        """
        os.system(self.control_cmd_location + " /filename "  + self.save_folder + self.image_name + str(self.image_index) + self.image_type +  " " + command)

    def run_script(self, script_name):
        os.system(self.control_cmd_location + " " + self.script_location + script_name)

    def set_save_folder(self, folder_path=None):
        """
        Function Description:
        Sets the folder path for saving images taken using this class.  If no folder path is given, a preset relative path is used.

        Author(s):
        Jacob Taylor Cassady

        Dates:
        Created - 6/5/18
        Updated - 6/5/18
        """
        if folder_path is None:
            folder_path = os.path.dirname(os.path.realpath(__file__)) + os.path.sep +".." + os.path.sep + "Camera" + os.path.sep + "Images" + os.path.sep

        return folder_path

    def set_script_path(self, script_path=None):
        """
        Function Description:
        Sets the path for CameraScripts used to control the camera.  If no path is given, a preset relative path is used.

        Author(s):
        Jacob Taylor Cassady

        Dates:
        Created - 6/5/18
        Updated - 6/5/18
        """
        if script_path is None:
            script_path = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + ".." + os.path.sep + "Camera" + os.path.sep + "CameraScripts" + os.path.sep

        print(script_path)

        return script_path

    def set_image_type(self, image_type=None):
        """
        Function Description:
        Sets the image type.  If none is given, the default CannonRaw2 image type is used.

        Author(s):
        Jacob Taylor Cassady

        Dates:
        Created - 6/5/18
        Updated - 6/5/18
        """
        if image_type == "jpeg" or image_type == "jpg":
            return ".jpg"
        else:
            return ".CR2"

    def capture_single_image(self, autofocus=False):
        """
        Function Description:
        Captures a single image.  Iterates the image index to ensure a unique name for each image taken.

        Author(s):
        Jacob Taylor Cassady

        Dates:
        Created - 6/5/18
        Updated - 6/5/18
        """
        if autofocus:
            self.command_camera("/capture")
        else:
            self.command_camera("/capturenoaf")
        self.image_index += 1

    def capture_multiple_images(self, image_count):
        """
        Function Description:
        Captures an n number of images by repeatedly calling the capture_single_image function n times where n is the parameter image_count.

        Author(s):
        Jacob Taylor Cassady

        Dates:
        Created - 6/5/18
        Updated - 6/5/18
        """
        for capture in range(image_count):
            self.capture_single_image()

if __name__ == "__main__":
    test_cam = Camera(image_type="jpeg", image_name="test_image")

    test_cam.run_script("test.dccscript")
#    test_cam.capture_multiple_images(10)