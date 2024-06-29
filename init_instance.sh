#!/bin/bash

# Update the package list
sudo apt-get update -y

# Upgrade all the installed packages to their latest version
sudo apt-get upgrade -y

# Install Python (Python 3 in this case)
sudo apt-get install -y python3 python3-pip python3-venv

# Install GCC and G++
sudo apt-get install -y gcc g++

# Install additional essential build tools
sudo apt-get install -y build-essential

# Create a Python virtual environment in the current directory
python3 -m venv .env

# Activate the virtual environment
source .env/bin/activate

# Install packages from requirements.txt if it exists
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "requirements.txt not found, skipping package installation."
fi

# Verify installations
echo "Python version:"
python3 --version

echo "GCC version:"
gcc --version

echo "G++ version:"
g++ --version

echo "Setup complete! The Python virtual environment is created and activated."
