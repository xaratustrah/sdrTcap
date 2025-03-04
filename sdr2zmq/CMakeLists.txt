cmake_minimum_required(VERSION 3.10)

# Project name and version
project(sdr2zmq VERSION 1.0)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Use Ninja as the build system
set(CMAKE_GENERATOR "Ninja")

# Find necessary packages
find_package(Boost REQUIRED)
find_package(fmt REQUIRED)
find_package(Gnuradio4 REQUIRED)
find_package(SPDLOG REQUIRED)

# Add executable
add_executable(sdr2zmq main.cpp)

# Link necessary libraries
target_link_libraries(sdr2zmq
    Boost::boost
    fmt::fmt
    Gnuradio4::gnuradio
    Gnuradio4::soapy
    Gnuradio4::zeromq
    Gnuradio4::testing
    spdlog::spdlog
)

# Include directories
target_include_directories(sdr2zmq PRIVATE
    ${Boost_INCLUDE_DIRS}
    ${FMT_INCLUDE_DIRS}
    ${GNURADIO_INCLUDE_DIRS}
    ${SPDLOG_INCLUDE_DIRS}
)

# Set properties for the target
set_target_properties(sdr2zmq PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED ON
)

# Print a message
message(STATUS "CMake configuration is done. To build the project, run 'cmake --build .'.")
