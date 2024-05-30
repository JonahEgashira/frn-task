#!/bin/bash
# Setup script for creating a virtual environment and installing dependencies

# Exit immediately if a command exits with a non-zero status.
set -e

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source ./venv/bin/activate

# Install the required packages
pip3 install -r requirements.txt

echo "Setup completed successfully!"
