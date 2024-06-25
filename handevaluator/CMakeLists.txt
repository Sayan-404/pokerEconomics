cmake_minimum_required(VERSION 3.12)
project(phevaluator_bindings)

# Set C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find Pybind11 package
add_subdirectory(pybind11)
# find_package(pybind11 REQUIRED)

# Set paths to phevaluator headers
include_directories(include)

# Add executable target
pybind11_add_module(phevaluator_bindings bindings.cpp)

# Link the phevaluator library
target_link_libraries(phevaluator_bindings PRIVATE ${CMAKE_SOURCE_DIR}/libpheval.a)
