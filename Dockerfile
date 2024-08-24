# Use the latest Python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /pokerEconomics

# Copy the local files to the Docker image
COPY . .

# Install necessary build tools
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Set up and activate the Python virtual environment
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    if [ -f "requirements.txt" ]; then pip install -r requirements.txt; else echo "requirements.txt not found, skipping package installation."; fi

# Compile the shared library for evaluate cards
RUN . venv/bin/activate && \
    cd hand_evaluator && \
    rm -rf build/CMakeCache.txt && \
    mkdir -p build && \
    cd build && \
    cmake .. && \
    make pheval && \
    cd .. && \
    g++ -fPIC --shared -std=c++11 -I include/ wrapper.cpp build/libpheval.so -o wrapper.so && \
    cd ..

# Compile the hand strength shared library
RUN . venv/bin/activate && \
    cd poker_metrics/hand_strength && \
    rm -rf build/CMakeCache.txt && \
    mkdir -p build && \
    cd build && \
    cmake .. && \
    make pheval && \
    cd .. && \
    g++ -fPIC --shared -std=c++11 -I include/ hs.c build/libpheval.so -o hs.so && \
    cd ../..

# Compile the potential shared library
RUN . venv/bin/activate && \
    cd poker_metrics/potential && \
    rm -rf build/CMakeCache.txt && \
    mkdir -p build && \
    cd build && \
    cmake .. && \
    make pheval && \
    cd .. && \
    g++ -fPIC --shared -std=c++11 -I include/ potential.c build/libpheval.so -o pot.so

# Final working directory
WORKDIR /pokerEconomics

# Entry point command
CMD ["bash"]
