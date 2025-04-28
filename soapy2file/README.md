# soapy2file

A set of tools for using software defined radio based on Gnuradio4 and SoapySDR.
Copy from Gnuradio4. But can compiled with a gnuradio4 docker image.

1.Firstly, build an image with Dockerfile in /dockerfile.  
`cd dockerfile`  
`docker build -t image_name .`  
Here `.` means using the current directory as the build context. Change the `image_name` to whatever you want e.g. `gnuradio4`.  

2.Create a container with this image  
`xhost +local:docker`  
`docker run -it --rm \`  
`  -e DISPLAY=$DISPLAY \`  
`  -e XDG_RUNTIME_DIR=/tmp/runtime-root \`   
`  -e PULSE_SERVER=unix:/run/user/1000/pulse/native \`  
`  -v /run/user/1000/pulse:/run/user/1000/pulse \`  
`  -v /tmp/.X11-unix:/tmp/.X11-unix \`  
`  -v /path/to/sdrTcap:/tmp/sdrTcap \`  
`  --name container_name \`  
`  --device=/dev/bus/usb \`  
` image_name`  

The first command allow Docker containers to access your X11 display for using GQRX.   
`1000` is the user id checked by `id -u`.   
In principle, LimeSDR should in /dev/bus/usb so this command allow docker container use it.  
`-v /path/to/sdrTcap:/tmp/sdrTcap` command is to make the sdrTcap folder in your host system visable in container.Remerber to adjust the path.  
Also change the `image_name` and `container_name` to something good to memory.

3.After container is created, it will be automaticlly started. Inside the container, run  
`ls` then you shall see two folders: gnuradio4 sdrTcap.  
Then navigate to the sdrTcap with  
`cd sdrTcap/soapy2file`  
Run the building process with:
`mkdir build`  
`cd build`  
`cmake -G Ninja -DCMAKE_C_COMPILER=clang-18 -DCMAKE_CXX_COMPILER=clang++-18 -DCMAKE_BUILD_TYPE=Debug -DLLVM_USE_LINKER=lld ..`  
`ninja`  
Or cmake command if you want.  
Then you can close the container with `exit`. You can see the build diretory in your host system.
