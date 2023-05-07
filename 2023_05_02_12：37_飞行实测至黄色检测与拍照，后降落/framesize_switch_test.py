# Hello World Example
#
# Welcome to the OpenMV IDE! Click on the green run arrow button below to run the script!

import sensor, image, time,utime

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.VGA)   # Set frame size to QVGA (320x240)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.
swtich_flag = 1
start = utime.ticks_ms()
while(True):
    clock.tick()                    # Update the FPS clock.
    end = utime.ticks_ms()
    if((end - start > 3000) and (swtich_flag == 1)):
        sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
        sensor.skip_frames(10)#时钟
        swtich_flag = 0
    img = sensor.snapshot()         # Take a picture and return the image.
    print(clock.fps())              # Note: OpenMV Cam runs about half as fast when connected
                                    # to the IDE. The FPS should increase once disconnected.
