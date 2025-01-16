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
