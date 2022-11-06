<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/jtcass01/DigiCam">
    <img src="https://github.com/jtcass01/StatusLogger/blob/master/images/StatueOfLiberty_StarryNightVanGogh_ImageTransfer.png" alt="Logo">
  </a>

  <h3 align="center">DigiCam</h3>

  <p align="center">
    A python library for controlling DSLR cameras using the open source program DigiCamControl. Please see: <a href="http://digicamcontrol.com/">http://digicamcontrol.com/</a> for more information.
    <br />
    <a href="https://github.com/jtcass01/DigiCam"><strong>Explore the docs �</strong></a>
    <br />
    <br />
    <a href="https://github.com/jtcass01/DigiCam/issues">Report Bug</a>
    �
    <a href="https://github.com/jtcass01/DigiCam/issues">Request Feature</a>
  </p>
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#install-digicamcontrol">Install digiCamControl</a></li>
        <li><a href="#install-digicam">Install DigiCam</a></li>
        <li><a href="#building-the-digicam-library">Building the DigiCam Library</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

## Install digiCamControl
digiCamControl can be downloaded [here](http://digicamcontrol.com/download).  Please select 'digiCamControl Stable Version'.

## Install DigiCam
Download the DigiCam source code from [here](https://github.com/jtcass01/DigiCam) or using the following git system call.
```bash
git clone https://github.com/jtcass01/DigiCam.git
```

## Building the DigiCam library
Locate the DigiCam directory.  Run build.py from this directory with the following system call.
```bash
python build.py
```

## Usage
Note: digiCamControl should locate the cpu port connected to a camera automatically.
```python
from DigiCam.Camera import Camera

# Replace the below path with the absolute or relative path to your CameraControlCmd executable.
camera_control_cmd_path = 'C:\\Program Files (x86)\\digiCamControl\\CameraControlCmd.exe'

test_camera = Camera(control_cmd_location=camera_control_cmd_path)

test_camera.capture_single_image(autofocus=True)
```

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->
## License

Distributed under the GPL-3.0 License. See `LICENSE` for more information.


<!-- CONTACT -->
## Contact

Jacob Taylor Cassady - [@Jacob_Cassady](https://twitter.com/Jacob_Cassady) - jacobtaylorcassady@outlook.com

Project Link: [https://github.com/jtcass01/DigiCam](https://github.com/jtcass01/StepperMotor)
