#/usr/bin/env python
"""setup.py Installs DigiCam Python Library"""

__author__ = "Jacob Taylor Cassady"
__email__ = "jacobtaylorcassady@outlook.com"

from setuptools import setup, find_packages

if __name__ == "__main__":
    with open("README.md", 'r') as fh:
        long_description = fh.read()

    setup(
        name="DigiCam",
        version='0.1',
        author=__author__,
        author_email=__email__,
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/jtcass01/DigiCam',
        packages=find_packages(),
        classifiers=[
            'Programming Language :: Python :: 3',
            'License :: GNU General Public License :: V3',
            'Operating System :: OS Independent'
        ],
        python_requires='>=3.6'
    )