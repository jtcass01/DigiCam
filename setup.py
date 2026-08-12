#/usr/bin/env python
"""setup.py Installs DigiCam Python Library"""

__author__ = 'Jacob Taylor Cassady'
__email__ = 'jacobtaylorcassady@outlook.com'

from re import search, MULTILINE
from setuptools import setup, find_packages


def read_version() -> str:
    """Single-source the version from DigiCam/__init__.py."""
    with open('DigiCam/__init__.py', 'r', encoding='utf-8') as fh:
        match = search(r"^__version__ = ['\"]([^'\"]+)['\"]", fh.read(), flags=MULTILINE)
    assert match is not None, 'Unable to locate __version__ in DigiCam/__init__.py'
    return match.group(1)


if __name__ == '__main__':
    with open('README.md', 'r', encoding='utf-8') as fh:
        long_description = fh.read()

    setup(
        name='DigiCam',
        version=read_version(),
        author=__author__,
        author_email=__email__,
        description='Control a DSLR camera from Python using digiCamControl.',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/jtcass01/DigiCam',
        project_urls={
            'Bug Tracker': 'https://github.com/jtcass01/DigiCam/issues',
            'Source': 'https://github.com/jtcass01/DigiCam',
            'digiCamControl': 'http://digicamcontrol.com/',
        },
        license='GPL-3.0',
        keywords=['dslr', 'camera', 'digicamcontrol', 'photography', 'tethered', 'timelapse'],
        packages=find_packages(exclude=['test', 'test.*']),
        package_data={'DigiCam': ['py.typed']},
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Operating System :: Microsoft :: Windows',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            'Programming Language :: Python :: 3.12',
            'Topic :: Multimedia :: Graphics :: Capture',
            'Typing :: Typed',
        ],
        python_requires='>=3.7'
    )
