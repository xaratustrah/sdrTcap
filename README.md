# sdrTcap
Time Series Capture System based on Software Defined Radios 

<div style="margin-left:auto;margin-right:auto;text-align:center">
<img src="https://raw.githubusercontent.com/xaratustrah/sdrTcap/master/rsrc/sdrTcap.jpg" width="512">
</div>  

*sdrTcap* is a collection of code based on [GNURadio4](https://github.com/fair-acc/gnuradio4) for accessing and processing digitised signals from [Software Defined Radio (SDR)](https://de.wikipedia.org/wiki/Software_Defined_Radio). The current version aims at working with [LIME SDR](https://limemicro.com/boards/limesdr/) and is based on the [SoapySDR](https://github.com/pothosware/SoapySDR/wiki) integration inside the GR4.

## sdr2file

This code is taken over from the examples available on the GR4 repositors. The [original version](https://raw.githubusercontent.com/fair-acc/gnuradio4/refs/heads/main/blocks/soapy/src/soapy_example.cpp) can be found on the [GR4 repository](https://github.com/fair-acc/gnuradio4/tree/main).

## sdr2zmq

This is a variation of the code above, but instead of writing to file, it continiously reads the SDR device to a ZMQ socket.

## Licensing

Please see the file [LICENSE.md](./LICENSE.md) for further information about how the content is licensed.

## Acknowledgements

This code is based on a previous work by Ralph Steinhagen [RalphSteinhagen@GitHUB](https://github.com/RalphSteinhagen), Alexander Krimm [wirew0rm@GitHUB](https://github.com/wirew0rm) and many others from the GNURadio team.

## Installation

### Preparation
Starting from a fresh image / ubuntu:

```
sudo apt install git cmake g++ libboost-all-dev libgmp-dev swig python3-numpy python3-mako python3-sphinx python3-lxml doxygen libfftw3-dev libsdl1.2-dev libgsl-dev libqwt-qt5-dev libqt5opengl5-dev python3-pyqt5 liblog4cpp5-dev libzmq3-dev python3-yaml python3-click python3-click-plugins python3-zmq python3-scipy python3-gi python3-gi-cairo gobject-introspection gir1.2-gtk-3.0

sudo apt install soapyosmo-common0.7 soapyremote-server soapysdr-module-airspy soapysdr0.7-module-airspy soapysdr-module-all soapysdr0.7-module-all soapysdr-module-audio soapysdr0.7-module-audio soapysdr-module-bladerf soapysdr0.7-module-bladerf soapysdr-module-hackrf soapysdr0.7-module-hackrf soapysdr-module-lms7 soapysdr0.7-module-lms7 soapysdr-module-mirisdr soapysdr0.7-module-mirisdr soapysdr-module-osmosdr soapysdr0.7-module-osmosdr soapysdr-module-redpitaya soapysdr0.7-module-redpitaya soapysdr-module-remote soapysdr0.7-module-remote soapysdr-module-rtlsdr soapysdr0.7-module-rtlsdr soapysdr-module-uhd soapysdr0.7-module-uhd soapysdr-tools
```

then comes:

```
sudo apt install uhd-host uhd-soapysdr limesuite limesuite-udev
```

you should be able to check your card by:

```
LimeUtil --find
SoapySDRUtil --info
SoapySDRUtil --find
```

you can also update the card by doing `sudo LimeUtil --update`, but this is not always recommended.

At this point, you sould also be able to use [GQRX](https://www.gqrx.dk/) which is a very nice code.

### Compilation
Steps:

```
mkdir build
cd build
cmake -G Ninja -DCMAKE_C_COMPILER=clang-18 -DCMAKE_CXX_COMPILER=clang++-18 -DCMAKE_BUILD_TYPE=Debug -DLLVM_USE_LINKER=lld ..
ninja
```




