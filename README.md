# DigiCam
A python library for controlling DSLR cameras using the open source program DigiCamControl. Please see: [http://digicamcontrol.com/](http://digicamcontrol.com/) for more information.

## Installing digiCamControl
digiCamControl can be downloaded [here](http://digicamcontrol.com/download).  Please select 'digiCamControl Stable Version'.

## Installing DigiCam
Download the DigiCam source code from [here](https://github.com/jtcass01/DigiCam) or using the following git system call.
```bash
git clone https://github.com/jtcass01/DigiCam.git
```

## Building the DigiCam library
Locate the DigiCam directory.  Run build.py from this directory with the following system call.
```bash
python build.py
```

## Simple Usage Example
Note: digiCamControl should locate the cpu port connected to a camera automatically.
```python
from DigiCam.Camera import Camera

# Replace the below path with the absolute or relative path to your CameraControlCmd executable.
camera_control_cmd_path = 'C:\\Program Files (x86)\\digiCamControl\\CameraControlCmd.exe'

test_camera = Camera(control_cmd_location=camera_control_cmd_path)

test_camera.capture_single_image(autofocus=True)
```
