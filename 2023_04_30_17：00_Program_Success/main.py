# Untitled - By: win10 - 周六 4月 29 2023

import sensor, image, time,Yellow_Detect,Red_Detect

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(10)
sensor.set_auto_whitebal(False)
sensor.set_auto_gain(False) # 关闭自动增益，低照度时有需要再开启
clock = time.clock()

while(True):
    clock.tick() # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot() # Take a picture and return the image.

    Yellow_Detect.yellow_Detect(img)
    Red_Detect.red_Detect(img)

#sensor.reset()
#sensor.set_pixformat(sensor.RGB565)
#sensor.set_framesize(sensor.QVGA)
#sensor.skip_frames(10)
#sensor.set_auto_whitebal(False)
#clock = time.clock()
#LED(1).on()
#LED(2).on()
#LED(3).on()

#while(True):
    #clock.tick()
    #img = sensor.snapshot()
    #Yellow_Detect(img)
