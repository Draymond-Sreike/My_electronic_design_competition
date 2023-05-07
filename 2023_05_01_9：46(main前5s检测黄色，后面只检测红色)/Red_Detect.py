import sensor, image, time,Message
from pyb import LED

IMG_CENTER_X=160
CENTER_ROI=(120,0,80,240)
CENTER_LINE_Y = (160,0,160,240)
CENTER_LINE_X = (0,120,320,120)

red_threshold   =(31, 61, 49, 79, 21, 65)# 出太阳，光照很好，背光一侧#(30, 60, 41, 80, 16, 61)#出太阳光照很好时，顺光一侧

# 寻找色块列表中最大的色块，使用这个函数一定要在色块列表中有元素才行，例如必须在if blobs_list:的条件下执行
def find_largest_blob(blobs_list):
    max_blob_pixels_value=0
    for now_blob in blobs_list:
        if now_blob[4] > max_blob_pixels_value:
            largest_blob=now_blob
            max_blob_pixels_value = now_blob[4]
    return largest_blob

def red_Detect(img):
    blobs = img.find_blobs([red_threshold],area_threshold=400,merge=False)
    if blobs:
        # 框出色块，大概率能框到红色物体
        max_blob=find_largest_blob(blobs)
        img.draw_rectangle(max_blob[0:4])
        img.draw_cross(max_blob[5], max_blob[6])
        img.draw_line(CENTER_LINE_Y,color=(0,0,255))
        img.draw_line(CENTER_LINE_X,color=(0,0,255))

        # 计算红色物体中心点与图像中心点的距离
        center_distance_err = max_blob[5] - IMG_CENTER_X

        if(CENTER_ROI[0]<max_blob[5] and max_blob[5]<(CENTER_ROI[0]+CENTER_ROI[2])):
            print("红色物体进入中心区域！距离中心点:",center_distance_err)
            Message.UartSendData(Message.My_Pack(0x03,0))
            # 红灯表示物体进入中心区域
            LED(1).on()
            LED(2).off()
            LED(3).off()
        else:
            print("红色物体进入视野！但还没有进入中心区域...距离中心点:",center_distance_err)
            # 白灯表示物体进入视野，但未进入中心区域
            LED(1).on()
            LED(2).on()
            LED(3).on()
            img.draw_rectangle(CENTER_ROI,color=(255,0,0))
    else:
        # 视野中没有红色色块则关灯
        LED(1).off()
        LED(2).off()
        LED(3).off()

if __name__ == '__main__':
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.skip_frames(10)
    sensor.set_auto_whitebal(False)
    clock = time.clock()

    while(True):
        clock.tick()
        img = sensor.snapshot()
        red_Detect(img)
