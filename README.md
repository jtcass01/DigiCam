<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/jtcass01/DigiCam">
    <img src="https://github.com/jtcass01/StatusLogger/blob/master/images/StatueOfLiberty_StarryNightVanGogh_ImageTransfer.png" alt="Logo">
  </a>

  <h3 align="center">DigiCam</h3>

  <p align="center">
    A Python library for controlling DSLR cameras using the open source program digiCamControl. Please see <a href="http://digicamcontrol.com/">digicamcontrol.com</a> for more information.
    <br />
    <br />
    <a href="https://github.com/jtcass01/DigiCam/issues">Report Bug</a>
    &middot;
    <a href="https://github.com/jtcass01/DigiCam/issues">Request Feature</a>
  </p>
</p>

<p align="center">
  <a href="https://pypi.org/project/DigiCam/"><img src="https://img.shields.io/pypi/v/DigiCam.svg" alt="PyPI version"></a>
  <a href="https://pypi.org/project/DigiCam/"><img src="https://img.shields.io/pypi/pyversions/DigiCam.svg" alt="Supported Python versions"></a>
  <a href="https://github.com/jtcass01/DigiCam/actions/workflows/test.yml"><img src="https://github.com/jtcass01/DigiCam/actions/workflows/test.yml/badge.svg" alt="Test status"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-GPL--3.0-blue.svg" alt="License"></a>
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li>
      <a href="#usage">Usage</a>
      <ul>
        <li><a href="#take-a-single-photo">Take a single photo</a></li>
        <li><a href="#choose-where-photos-are-saved">Choose where photos are saved</a></li>
        <li><a href="#configure-the-camera">Configure the camera</a></li>
        <li><a href="#shoot-a-sequence">Shoot a sequence</a></li>
      </ul>
    </li>
    <li><a href="#api-reference">API Reference</a></li>
    <li><a href="#troubleshooting">Troubleshooting</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

## Getting Started

### Prerequisites

DigiCam is a wrapper around digiCamControl's command line interface, so it is **Windows only**.

1. Download digiCamControl [here](http://digicamcontrol.com/download) and select *digiCamControl Stable Version*.
2. Install it. By default the command line executable lands at:
   ```
   C:\Program Files (x86)\digiCamControl\CameraControlCmd.exe
   ```
3. Connect your camera by USB and confirm digiCamControl sees it. digiCamControl locates the port automatically.

You will pass the path to `CameraControlCmd.exe` into `Camera`, so make a note of where yours ended up.

### Installation

From PyPI:

```bash
pip install DigiCam
```

Or from source:

```bash
git clone https://github.com/jtcass01/DigiCam.git
cd DigiCam
pip install .
```

## Usage

### Take a single photo

```python
from DigiCam import Camera

# Replace with the absolute or relative path to your CameraControlCmd executable.
camera_control_cmd_path = 'C:\\Program Files (x86)\\digiCamControl\\CameraControlCmd.exe'

camera = Camera(control_cmd_location=camera_control_cmd_path)

camera.capture_single_image(autofocus=True)
```

### Choose where photos are saved

`save_folder` is created for you if it does not exist. `collection_name` is prefixed to every
filename, and an index is appended so each shot is unique — the example below writes
`sunset_0.jpg`, `sunset_1.jpg`, and so on.

```python
camera = Camera(control_cmd_location=camera_control_cmd_path,
                image_type='jpg',
                collection_name='sunset',
                save_folder='D:\\photos\\2026-08-11')

camera.capture_single_image()
```

Supported `image_type` values are `'jpg'`/`'jpeg'`, `'png'`, `'raw'`, and `'.CR2'`. Anything
else falls back to `.jpg`.

### Configure the camera

Settings are pushed to the camera by generating a `.dccscript` and running it. Any setting left
as `None` is not sent, so the camera keeps its current value for that property.

```python
from DigiCam import Camera

camera = Camera(control_cmd_location=camera_control_cmd_path)

settings = Camera.Settings(aperture='2.8',
                           exposure_control='1',
                           shutter_speed='1/125',
                           iso='400')

camera.setup(settings)
camera.capture_single_image()
```

Values are passed through to digiCamControl verbatim, so they must be values your camera
actually supports. `iso='AUTO'` is accepted by most bodies.

### Shoot a sequence

`frequency` is in images per second, so `frequency=0.5` waits two seconds between shots.

```python
# 60 frames, one every two seconds.
camera.capture_multiple_images(image_count=60, frequency=0.5)
```

## API Reference

### `Camera(control_cmd_location, image_type=None, collection_name='', save_folder=getcwd())`

| Argument | Type | Description |
| --- | --- | --- |
| `control_cmd_location` | `str` | Path to `CameraControlCmd.exe`. Required. |
| `image_type` | `str \| None` | `'jpg'`, `'png'`, `'raw'`, or `'.CR2'`. Defaults to `.jpg`. |
| `collection_name` | `str` | Prefix for every captured filename. |
| `save_folder` | `str` | Directory for captured images. Created if missing. |

| Method | Description |
| --- | --- |
| `capture_single_image(autofocus=False)` | Captures one image and increments the image index. |
| `capture_multiple_images(image_count, frequency=1.0)` | Captures `image_count` images at `frequency` images per second. |
| `setup(settings, setup_script_name='setup.dccscript')` | Generates a setup script from `settings` and runs it. |
| `generate_setup_script(settings, setup_script_name)` | Writes the `.dccscript` without running it. |
| `run_script(script_name)` | Runs an existing `.dccscript`. |
| `command_camera(command)` | Sends a raw digiCamControl command. |

### `Camera.Settings(aperture=None, exposure_control=None, shutter_speed=None, iso=None)`

Holds the camera properties written into a setup script. `to_dict()` returns them keyed by the
property names digiCamControl expects.

## Troubleshooting

**`AssertionError: Unable to locate: ...`** — the path you passed is not `CameraControlCmd.exe`.
Check under `C:\Program Files (x86)\digiCamControl\` and `C:\Program Files\digiCamControl\`. Note
that `CameraControlCmd.exe` is the command line tool, not `CameraControl.exe`.

**Nothing happens and no image appears** — digiCamControl commands fail silently. Run the same
command by hand to see its output:

```bash
"C:\Program Files (x86)\digiCamControl\CameraControlCmd.exe" /capturenoaf
```

**The camera is not detected** — make sure the camera is in a mode that allows tethered capture and
is not mounted as a mass storage device. If the digiCamControl GUI is open, try closing it; the GUI
and the command line tool can compete for the camera.

**Captures fail with autofocus on** — a camera that cannot achieve focus refuses the shot. Use
`capture_single_image(autofocus=False)` to capture regardless of focus.

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Tests that need digiCamControl installed, or a camera connected, are skipped automatically, so
the suite passes on a fresh clone:

```bash
python -m unittest discover -s test -v
```

<!-- LICENSE -->
## License

Distributed under the GPL-3.0 License. See `LICENSE` for more information.

<!-- CONTACT -->
## Contact

Jacob Taylor Cassady - jacobtaylorcassady@outlook.com

Project Link: [https://github.com/jtcass01/DigiCam](https://github.com/jtcass01/DigiCam)
