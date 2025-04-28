FROM ubuntu:latest

# Set environment variable to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and install the required packages
RUN apt-get update && apt-get install -y \
    clang-18 \
    cmake \
    git \
    gnuradio \
    gqrx-sdr \
    hamradio-sdr \
    hamradio-tools \
    libboost-all-dev \
    liblimesuite-dev \
    libsoapysdr-dev \
    limesuite \
    limesuite-udev \
    ninja-build \
    python3-dev \
    python3-numpy \
    python3-pyqt5 \
    python3-scipy \
    python3-soapysdr \
    rtl-sdr \
    soapyosmo-common0.8 \
    soapyremote-server \
    soapysdr-tools \
    soapysdr0.8-module-airspy \
    soapysdr0.8-module-all \
    soapysdr0.8-module-audio \
    soapysdr0.8-module-bladerf \
    soapysdr0.8-module-hackrf \
    soapysdr0.8-module-lms7 \
    soapysdr0.8-module-mirisdr \
    soapysdr0.8-module-osmosdr \
    soapysdr0.8-module-redpitaya \
    soapysdr0.8-module-remote \
    soapysdr0.8-module-rtlsdr \
    soapysdr0.8-module-uhd \
    swig && \
    rm -rf /var/lib/apt/lists/*

# Clone the repository and build the project
WORKDIR /tmp
RUN git clone https://github.com/fair-acc/gnuradio4.git && \ 
    cd gnuradio4 && \
    mkdir build && \
    cd build && \
    cmake -G Ninja .. && \
    ninja && \
    ninja install
    
CMD ["bash"]
