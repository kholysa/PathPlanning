# A* Path Planning Package
# Overview
This is a simple package to plan a path for a quadcopter. It exposes 2 methods

1) Set barriers
2) Get Path

# Installation

Requires:
- Python 3.6
- pip
- python venv

## Linux & windows & MacOS environments
1) Create a python virtual environment somewhere in your documents. Run the Instructions below OR follow this guide https://docs.python.org/3/tutorial/venv.html

a) Run this command `python3 -m venv venvName` to create a python3 virtual environment.

b) Run this command cd `venvName` to move into the virtual environement.

c) (Linux only, required)Run this command source `myenv\Scripts\activate` to source the virtual environment's python installation. Your terminal should now show your venvName before each line.

d) (Windows only, required)Run this command source `bin/activate` to source the virtual environment's python installation. Your terminal should now show your venvName before each line.

2) Install the requried pip packages. Run the Instructions below

a) (Linux only, optional)Run this command `which pip`. Make sure the output points to a file that is in your venv.

b) Run this command `pip install matplotlib numpy` to install the required packages.
