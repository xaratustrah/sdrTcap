cmake_minimum_required(VERSION 3.10)
project(soapy2file)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Add executable
add_executable(soapy2file soapy2file.cpp)

# Find and include Boost
find_package(Boost REQUIRED)
include_directories(${Boost_INCLUDE_DIRS})

# Find and include fmt
find_package(fmt REQUIRED)
include_directories(${fmt_INCLUDE_DIRS})

# Find and include GNURadio
find_package(Gnuradio REQUIRED)
include_directories(${GNURadio_INCLUDE_DIRS})

# Add GNURadio components
find_package(GnuradioComponents REQUIRED Scheduler fileio soapy testing)
include_directories(${GnuradioComponents_INCLUDE_DIRS})

# Link libraries
target_link_libraries(soapy2file
    ${Boost_LIBRARIES}
    fmt::fmt
    ${GNURadio_LIBRARIES}
    ${GnuradioComponents_LIBRARIES}
)

# Add any other necessary libraries
# target_link_libraries(soapy2file <other_libraries>)
