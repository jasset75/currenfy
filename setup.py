import os
import sys
from setuptools import find_packages, setup


CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 6)
CURRENFY_VERSION = '1.0.0'

if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================

This version of Currenfy requires Python {}.{}, but you're trying to
install it on Python {}.{}
""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))
    sys.exit(1)

req_filename = './requirements-prod.txt'

with open(req_filename) as f:
    install_requires = f.read().strip().split('\n')



setup(
    name='currenfy',
    version=CURRENFY_VERSION,
    python_requires='>={}.{}'.format(*REQUIRED_PYTHON),
    install_requires=install_requires
)
