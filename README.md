# oak-poe-rtsp-autoboot

This repository contains necessary files to create a RTSP stream for the OAK PoE Camera Series 1. For further documentation on the camera, please refer to here: 
https://docs.luxonis.com/projects/api/en/latest/

By full function, the total steps aims to create a RTSP stream once booting into a Linux System. This is done with the scope for the Raspberry Pi

## Installation

You need python3 to install necessary requirements. Navigate your terminal to the main directory and perform,

```shell
pip install -r requirements.txt
sudo apt-get install ffmpeg gstreamer-1.0 gir1.2-gst-rtsp-server-1.0 libgirepository1.0-dev gstreamer1.0-plugins-bad gstreamer1.0-plugins-good gstreamer1.0-plugins-base
python3 -m pip install -r requirements.txt
```
If you are running into issues due to version control (which shouldn't happen with this script), change the versions within requirements.txt to,

```
PyGObject
depthai
opencv-python
```


## Execution

Two seperate roads of steps to either execute an RTSP stream for the camera, or create an automated RTSP stream upon boot. The exact link for the RTSP stream is,
```sh
rtsp://localhost:8554/preview
```
for when executed correctly

### Simple RTSP Stream
Run main.py within the master directory,
```sh
python3 ./main.py
```
### Automated Boot RTSP Stream
Firstly, this is currently supported for Ubuntu/Debian based systems.

1) Edit the rtsp_stream.service file to input the directory to main.py and username. They're already labled for you to fillout. Square brackets must be removed.

2) Perform these systemctl commands one by one to enable your service,
```sh
sudo systemctl daemon-reload
sudo systemctl enable rtsp_stream.service
```
Now this service will be executed upon boot. To verify and check the service, you can perform,
```sh
sudo systemctl status rtsp_stream.service
```
Likely if you were following these steps, the service isn't up. This is because you didn't start the service (since you didn't reboot). Perform,
```sh
sudo systemctl start rtsp_stream.service
```



