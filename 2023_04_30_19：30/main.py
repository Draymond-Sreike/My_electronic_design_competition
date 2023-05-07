# Untitled - By: win10 - 周六 4月 29 2023

import sensor, image, time,Yellow_Detect,Red_Detect,Treshold_Detect

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(10)
sensor.set_auto_whitebal(False)
#sensor.set_auto_gain(False) # 关闭自动增益，低照度时有需要再开启,这个功能相当于加亮
clock = time.clock()

while(True):
    clock.tick() # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot() # Take a picture and return the image.
    Yellow_Detect.yellow_Detect(img)
    Red_Detect.red_Detect(img)
    #Treshold_Detect.roi_threshold_detect(img)
