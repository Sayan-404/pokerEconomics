#!/bin/bash

echo -n "Do you want to fully initialise (or on AWS)(y/n)? "
read ch

if [ "$ch" = "y" ] || [ "$ch" = "yes" ]; then
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

echo "\e[0mIf any of the above commands resulted in an error, exit and restart script with initialisation on."

if [ -d ".env" ]; then
    echo -n "Existing environment found, do you want to delete it? (y/n)? "
    read ch
    if [ "$ch" = "y" ] || [ "$ch" = "yes" ]; then
        echo "Deleting existing environment."
        rm -rf .env
    fi
fi

# Create a Python virtual environment in the current directory
python3 -m venv .env

# Activate the virtual environment
source .env/bin/activate
echo "\e[32mThe Python virtual environment is created and activated.\e[0m"

echo "\e[33mPython requirements will be fetched and installed now.\e[0m"

# Install packages from requirements.txt if it exists
pip install --upgrade pip
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "\e[32mThe Python requirements are installed.\e[0m"
else
    echo "\e[31mrequirements.txt not found, skipping package installation.\e[0m"
fi

# compiling the shared library for evaluate cards
echo "\e[33mShared library for evaluate cards will be compiled now.\e[0m"

cd hand_evaluator
mkdir -p build
cd build
cmake ..
make pheval
cd ..
if [ -f "build/libpheval.0.6.0.dylib" ]; then
    mv build/libpheval.0.6.0.dylib build/libpheval.so.0.6.0
fi
g++ -fPIC --shared -std=c++11 -I include/ wrapper.cpp build/libpheval.so.0.6.0 -o wrapper.so
cd ..

cd poker_metrics/hand_strength
mkdir -p build
cd build
cmake ..
make pheval
cd ..
if [ -f "build/libpheval.0.6.0.dylib" ]; then
    mv build/libpheval.0.6.0.dylib build/libpheval.so.0.6.0
fi
g++ -fPIC --shared -std=c++11 -I include/ hs.c build/libpheval.so.0.6.0 -o hs.so
cd ../..

cd poker_metrics/potential
mkdir -p build
cd build
cmake ..
make pheval
cd ..
if [ -f "build/libpheval.0.6.0.dylib" ]; then
    mv build/libpheval.0.6.0.dylib build/libpheval.so.0.6.0
fi
g++ -fPIC --shared -std=c++11 -I include/ potential.c build/libpheval.so.0.6.0 -o pot.so

echo "\e[33mProcess complete, check above log for errors and restart if needed.\e[0m"
