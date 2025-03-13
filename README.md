# sdrTcap
Time Series Capture System based on Software Defined Radios 

<div style="margin-left:auto;margin-right:auto;text-align:center">
<img src="https://raw.githubusercontent.com/xaratustrah/sdrTcap/master/rsrc/sdrTcap.jpg" width="512">
</div>  

*sdrTcap* is a collection of code for long term capturing of RF signals using software defined radio and storing them continously on the hard disk. It has been tested using NESDR-Mini-2+, NESDR Nano 2 and NESDR SMArt v5. More info about these devices can be found on the [NooELEC website](https://support.nooelec.com/hc/en-us/articles/360005805834-NESDR-Series).


## rtl2file

This is a pure python code that utilizes the RTL-SDR driver.


#### Installation

Before you install this code, make sure the driver is installed on your system:

```
sudo apt install -y rtl-sdr
```

You should be able to use the device as a normal user. If you have permission problems, please follow the instructions available [on this site](https://pysdr.org/content/rtlsdr.html#rtl-sdr-background). In short:

first find out the vendor ID of your device using `lsusb`, which will look something like this:

```
Bus 003 Device 017: ID 0bda:2838 Realtek Semiconductor Corp. RTL2838 DVB-T
```

then you create a file `/etc/udev/rules.d/10-rtl-sdr.rules` with the content from the vendor ID:

```
SUBSYSTEM=="usb", ATTRS{idVendor}=="0bda", ATTRS{idProduct}=="2838", MODE="0666"
```

then restart `udev`:

```
sudo udevadm control --reload-rules
sudo udevadm trigger
```

## soapy2file

This code is like the above, with the difference - as the name suggests - of using the Soapy driver. This code is taken over from the examples available on the GR4 repositors. The [original version](https://raw.githubusercontent.com/fair-acc/gnuradio4/refs/heads/main/blocks/soapy/src/soapy_example.cpp) can be found on the [GR4 repository](https://github.com/fair-acc/gnuradio4/tree/main). It is based on [GNURadio4](https://github.com/fair-acc/gnuradio4) for accessing and processing digitised signals from [Software Defined Radio (SDR)](https://de.wikipedia.org/wiki/Software_Defined_Radio). The current version aims at working with [LIME SDR](https://limemicro.com/boards/limesdr/) and is based on the [SoapySDR](https://github.com/pothosware/SoapySDR/wiki) integration inside the GR4.

#### Installation

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


Compilation steps:

```
mkdir build
cd build
cmake -G Ninja -DCMAKE_C_COMPILER=clang-18 -DCMAKE_CXX_COMPILER=clang++-18 -DCMAKE_BUILD_TYPE=Debug -DLLVM_USE_LINKER=lld ..
ninja
```

#### Docker image

TBD


## Licensing

Please see the file [LICENSE.md](./LICENSE.md) for further information about how the content is licensed.


