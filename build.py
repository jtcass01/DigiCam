#!/usr/bin/env python
"""build.py:"""

__author__ = "Jacob Taylor Cassady"
__email__ = "jacobtaylorcassady@outlook.com"

from os import system

if __name__ == "__main__":
    system('pip uninstall DigiCam -y')
    system('pip install .')