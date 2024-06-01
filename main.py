#################################################################
# THIS STRUCTURE IS REFERENCED BY DEPTHAI
# Copyright (c) 2020 Luxonis
#################################################################

#################################################################
# IMPORTS AND DEFINITIONS
#################################################################
from RTSP import RTSPServer
import depthai as dai

#################################################################
# GLOBAL VARIABLES AND DEFINITIONS
#################################################################
FPS_MAX = 30

def main():
    
    #Set RTSP Server from RTSP and create dai pipeline
    server = RTSPServer()
    pipeline = dai.Pipeline()

    #Set FPS Max to
    FPS = FPS_MAX

    #Create color camera pipeline
    colorCam = pipeline.create(dai.node.ColorCamera)
    colorCam.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
    colorCam.setInterleaved(True)
    colorCam.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)
    colorCam.setFps(FPS_MAX)

    #Create video encoder pipeline
    videnc = pipeline.create(dai.node.VideoEncoder)
    videnc.setDefaultProfilePreset(FPS_MAX, dai.VideoEncoderProperties.Profile.H265_MAIN)
    colorCam.video.link(videnc.input)

    #Create XLinkOUT Pipeline and set bitstream
    veOut = pipeline.create(dai.node.XLinkOut)
    veOut.setStreamName("encoded")
    videnc.bitstream.link(veOut.input)

    #Logic Tree to Obtain DepthAI Device
    device_infos = dai.Device.getAllAvailableDevices()
    if len(device_infos) == 0:
        raise RuntimeError("No DepthAI device found!")
    else:
        print("Available devices:")
        for i, info in enumerate(device_infos):
            print(f"[{i}] {info.getMxId()} [{info.state.name}]")
        if len(device_infos) == 1:
            device_info = device_infos[0]
        else:
            val = input("Which DepthAI Device you want to use: ")
            try:
                device_info = device_infos[int(val)]
            except:
                raise ValueError("Incorrect value supplied: {}".format(val))

    with dai.Device(pipeline, device_info) as device:
        encoded = device.getOutputQueue("encoded", maxSize=30, blocking=False)
        print("Setup finished, RTSP stream available under \"rtsp://localhost:8554/preview\"")
        while True:
            data = encoded.get().getData()
            server.send_data(data)

if __name__ == "__main__":
    main()
     