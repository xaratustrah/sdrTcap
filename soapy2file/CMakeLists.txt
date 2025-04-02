cmake_minimum_required(VERSION 3.25)
project(soapy2file)

# Set C++ standard
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Add executable
add_executable(soapy2file soapy2file.cpp)

set(INCLUDE_DIRS 
    /usr/local/include 
    /usr/include 
    /tmp/gnuradio4/algorithm/include
    /tmp/gnuradio4/core/include
    /tmp/gnuradio4/meta/include
    /tmp/gnuradio4/block/basic/include
    /tmp/gnuradio4/block/electrical/include
    /tmp/gnuradio4/block/fileio/include
    /tmp/gnuradio4/block/filter/include
    /tmp/gnuradio4/block/fourier/include
    /tmp/gnuradio4/block/http/include
    /tmp/gnuradio4/block/math/include
    /tmp/gnuradio4/block/soapy/include
    /tmp/gnuradio4/block/testing/include
)
include_directories(${INCLUDE_DIRS})

#Link gnuradio-core in system path
find_library(GR_CORE NAMES gnuradio-core PATHS /usr/local/lib)
if(GR_CORE)
    #nothing
else()
    message(FATAL_ERROR "gnuradio-core not found! Please check installation of gnuradio4!")
endif()


# Fetch packages 
include(FetchContent)
FetchContent_Declare(
  fmt
  GIT_REPOSITORY https://github.com/fmtlib/fmt.git
  GIT_TAG 10.2.1)

FetchContent_Declare(
  pmt
  GIT_REPOSITORY https://github.com/gnuradio/pmt.git
  GIT_TAG e1a46cb61decb044f6ab0a58a77211beb3630340 # latest as of 2023-12-06
)

FetchContent_Declare(
  ut
  GIT_REPOSITORY https://github.com/boost-ext/ut.git
  GIT_TAG v2.0.1 # latest tag as of 2023-12-18
)

FetchContent_Declare(
  vir-simd
  GIT_REPOSITORY https://github.com/mattkretz/vir-simd.git
  GIT_TAG v0.4.0)

FetchContent_Declare(
  cpp-httplib
  GIT_REPOSITORY https://github.com/yhirose/cpp-httplib.git
  GIT_TAG v0.18.1)

FetchContent_MakeAvailable(
  fmt
  pmt
  ut
  vir-simd
  cpp-httplib)



add_library(pmtv INTERFACE)
target_include_directories(pmtv INTERFACE ${pmt_SOURCE_DIR}/include/)
target_link_libraries(pmtv INTERFACE)

add_library(vir INTERFACE)
target_include_directories(vir INTERFACE ${vir-simd_SOURCE_DIR}/)

find_package(Boost REQUIRED)
include_directories(${Boost_INCLUDE_DIRS})

find_package(fmt REQUIRED)
include_directories(${fmt_INCLUDE_DIRS})

find_package(SoapySDR CONFIG REQUIRED)
if (TARGET SoapySDR)
    #nothing
else ()
    message(FATAL_ERROR "SoapySDR development files not found: ${SoapySDR_FOUND}")
endif ()

target_include_directories(soapy2file PRIVATE ${cpp-httplib_SOURCE_DIR})



#Add magic_enum
if(NOT (TARGET magic_enum))
  add_library(magic_enum INTERFACE)
  target_include_directories(magic_enum ${CMAKE_EXT_DEP_WARNING_GUARD}
                             INTERFACE ${PROJECT_SOURCE_DIR}/third_party/magic_enum/)
endif()


#Add ut_benchmark
add_subdirectory(bench)

#Add fftw
set(FFTW_PREFIX ${CMAKE_CURRENT_BINARY_DIR}/fftw)
if(EMSCRIPTEN)
  set(FFTW_CFLAGS "${CFLAGS} -fPIC -w")
  set(FFTW_CONFIG
      cd
      ${FFTW_PREFIX}/src/
      &&
      emconfigure
      ./configure
      --enable-silent-rules
      --quiet
      --disable-fortran
      --prefix=${FFTW_PREFIX}/install)
  set(FFTW_BUILD
      emmake
      make
      -j
      CFLAGS=${FFTW_CFLAGS}
      --silent
      V=0
      &&
      emmake
      make
      install
      --silent
      V=0
      &&
      emmake
      make
      clean
      --silent
      V=0)
else()
  set(FFTW_CFLAGS "${CFLAGS} -fPIC -w -O3 -march=native -mtune=native")
  set(FFTW_CONFIG
      ${FFTW_PREFIX}/src/configure
      --enable-silent-rules
      --quiet
      --disable-fortran
      --prefix=${FFTW_PREFIX}/install)
  set(FFTW_BUILD
      make
      -j
      CFLAGS=${FFTW_CFLAGS}
      --silent
      V=0
      &&
      make
      install
      --silent
      V=0
      &&
      make
      clean
      --silent
      V=0)
endif()
set(FFTW_INSTALL_COMMAND ${FFTW_CONFIG} && ${FFTW_BUILD} && ${FFTW_CONFIG} --enable-float && ${FFTW_BUILD})

include(ExternalProject)
ExternalProject_Add(
  fftw_ext
  PREFIX ${FFTW_PREFIX}
  SOURCE_DIR ${FFTW_PREFIX}/src
  BINARY_DIR ${FFTW_PREFIX}/build
  INSTALL_DIR ${FFTW_INSTALL_DIR}
  STAMP_DIR ${FFTW_PREFIX}/stamp
  TMP_DIR ${FFTW_PREFIX}/tmp
  DOWNLOAD_DIR ${FFTW_PREFIX}/download
  LOG_DIR ${FFTW_PREFIX}/log
  URL "https://fftw.org/fftw-3.3.10.tar.gz"
  URL_MD5 8ccbf6a5ea78a16dbc3e1306e234cc5c
  CONFIGURE_COMMAND ${FFTW_INSTALL_COMMAND}
  BUILD_COMMAND ""
  INSTALL_COMMAND ""
  LOG_DOWNLOAD ON)

add_library(fftw INTERFACE)
target_link_libraries(
  fftw
  INTERFACE fftw3
  INTERFACE fftw3f
  INTERFACE m)
target_include_directories(fftw INTERFACE ${FFTW_PREFIX}/install/include ${PROJECT_BINARY_DIR})
target_link_directories(
  fftw
  INTERFACE
  ${FFTW_PREFIX}/install/lib
  ${FFTW_PREFIX}/install/lib64)
add_dependencies(fftw fftw_ext)

target_link_libraries(soapy2file 
  PUBLIC ${GR_CORE}
          ut-benchmark
          fftw
          magic_enum
          fmt
          pmtv
          ut
          vir-simd
          SoapySDR)
