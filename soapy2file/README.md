# sdr

A set of tools for using software defined radio.  

1.Firstly, build an image with Dockerfile in dockerfiles/sdr/.  
Navigate to the directory containing this Dockerfile and run:  
`docker build -t image_name .`  
Here `.` means using the current directory as the build context. Change the `image_name` to whatever you want like `gnuradio4`.  

2.Create a container with this image  
`xhost +local:docker`  
`docker run -it \`  
`  -e DISPLAY=$DISPLAY \`  
`  -e XDG_RUNTIME_DIR=/tmp/runtime-root \`   
`  -e PULSE_SERVER=unix:/run/user/1000/pulse/native \`  
`  -v /run/user/1000/pulse:/run/user/1000/pulse \`  
`  -v /tmp/.X11-unix:/tmp/.X11-unix \`  
`  --name container_name \`  
`  --device=/dev/bus/usb \`  
` image_name`  

The first command allow Docker containers to access your X11 display for using GQRX. 
`1000` is the user id checked by `id -u`. 
In principle, LimeSDR should in /dev/bus/usb so this command allow docker container use it.  
Also change the `image_name` and `container_name` to something good to memory.

3.After container is created, it will be automaticlly started. Inside the container, run  
`LimeUtil --find` to check if LimeSDR device is connected to the container.  
Then navigate to the executable with  
`cd gnuradio4/build/blocks/soapy/src`  
Check with `ls`. The executable named "soapy_example" shoule be there.  
One can also use `gqrx` to use GQRX in this container.
