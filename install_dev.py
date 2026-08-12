#!/usr/bin/env python
"""install_dev.py: Reinstalls DigiCam from source.

Named install_dev.py rather than build.py because a build.py at the repository root
shadows the PyPA 'build' package, which breaks 'python -m build' and the release workflow."""

__author__ = 'Jacob Taylor Cassady'
__email__ = 'jacobtaylorcassady@outlook.com'

from os import system

if __name__ == '__main__':
    system('pip uninstall DigiCam -y')
    system('pip install .')
