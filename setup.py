__author__ = 'sandro'
from distutils.core import setup

setup(
    author='Sandro Covo',
    author_email="sandro@covo.ch",
    packages=['brainfuck'],
    scripts=['scripts/pyfuck'],
    name="Pyfuck",
    description="Brainfuck interpreter written in python"
)