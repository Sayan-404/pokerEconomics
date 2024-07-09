#!/bin/bash

echo -n "Do you want to fully initialise (or on AWS)(y/n)?: "
read ch

if [ "$ch" -eq "y" ] || [ "$ch" -eq "yes" ]; then
    # Update the package list
    sudo apt-get update -y

    # Upgrade all the installed packages to their latest version
    sudo apt-get upgrade -y

    # Install Python (Python 3 in this case)
    sudo apt-get install -y python3 python3-pip python3-venv

    # Install GCC and G++
    sudo apt-get install -y gcc g++ cmake

    # Install additional essential build tools
    sudo apt-get install -y build-essential
fi

# Verify installations
echo "\e[32mPython version:"
python3 --version

echo "GCC version:"
gcc --version

echo "G++ version:"
g++ --version

echo "The Python virtual environment is created and activated.\e[0m"

# Create a Python virtual environment in the current directory
python3 -m venv .env

# Activate the virtual environment
source .env/bin/activate

echo "\e[33mPython requirements will be fetched and installed now.\e[0m"

# Install packages from requirements.txt if it exists
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "\e[31mrequirements.txt not found, skipping package installation.\e[0m"
fi

echo "\e[32mThe Python requirements are installed.\e[0m"

# compiling the shared library for evaluate cards
echo "\e[33mShared library for evaluate cards will be compiled now.\e[0m"

cd hand_evaluator
mkdir -p build
cd build
cmake ..
make pheval
cd ..
mv build/libpheval.0.6.0.dylib build/libpheval.so.0.6.0
g++ -fPIC --shared -std=c++11 -I include/ wrapper.cpp build/libpheval.so.0.6.0 -o wrapper.so
cd ..

echo "\e[32mShared library for evaluate cards compiled.\e[0m"