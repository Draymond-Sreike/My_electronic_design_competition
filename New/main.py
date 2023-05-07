#************************************ (C) COPYRIGHT 2023 MSL ***********************************#
import sensor, image, time, utime,math, struct
import json
from pyb import LED,Timer
from struct import pack, unpack
import Message,Barcode,QRandBAR,Red_Detect,Red_Detect_Exposure
import Yellow_Detect
#初始化镜头
#sensor.reset()
#sensor.set_pixformat(sensor.RGB565)
#sensor.set_framesize(sensor.QVGA)
#sensor.skip_frames(10)#时钟
#sensor.set_auto_whitebal(False) # 若想追踪颜色则关闭白平衡
#sensor.set_auto_gain(True)      # 环境太暗时应开启自动增益以提高视野亮度
#clock = time.clock()#初始化时钟
EXPOSURE_TIME_SCALE = 1.0   # 曝光时间调整比例，设置曝光时间=初始曝光时间*EXPOSURE_TIME_SCALE
                            # 更改此值以调整曝光。试试10.0 / 0.1 /等
AUTO_WHITEBAL_FLAG = False  # 必须关闭自动增益控制和自动白平衡
AUTO_GAIN_FLAG = False      # 否则他们将更改图像增益以撤消您放置的任何曝光设置
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)  # 等待设置生效
print("Initial Exposure Time:%d us" % sensor.get_exposure_us())  # 打印初始曝光值，用于后续比较曝光值的变化
sensor.set_auto_whitebal(AUTO_WHITEBAL_FLAG)
sensor.set_auto_gain(AUTO_GAIN_FLAG)
sensor.skip_frames(time=500)    # 需要让以上设置生效
# 记录镜头参数设置完成后的当前曝光时间，后续用于倍乘
current_exposure_time_in_microseconds = sensor.get_exposure_us()
print("Current Exposure Time:%d us" % current_exposure_time_in_microseconds)
# 设置曝光时间为int(current_exposure_time_in_microseconds * EXPOSURE_TIME_SCALE)
# 默认情况下启用自动曝光控制（AEC）。调用以下功能可禁用传感器自动曝光控制。
# 另外“exposure_us”参数在AEC被禁用后覆盖自动曝光值。
sensor.set_auto_exposure(False,
    exposure_us=6576)
print("New exposure Time:%d us" % sensor.get_exposure_us())

yellowDetect_to_BarcodePhoto_flag = True
BarcodePhoto_to_redDetect_flag = True
redDetect_to_QRcodePhoto_flag = True

#start = utime.ticks_ms()
#主循环
while(True):
    #clock.tick()#时钟初始化
    #end = utime.ticks_ms()
    img = sensor.snapshot()
    # 接收串口数据
    Message.UartReadBuffer()
    if (Message.Ctr.WorkMode==1): # 识别黄色条形码#if(end - start < 5000):
        Yellow_Detect.yellow_Detect(img)
         #LED(1).on()
         #LED(2).off()
         #LED(3).off()
    elif (Message.Ctr.WorkMode==2): # 条形码拍照#elif(end - start < 30000):
        Yellow_Detect.alert_close()
        QRandBAR.BarcodePhoto()
         #LED(1).off()
         #LED(2).on()
         #LED(3).off()
    elif (Message.Ctr.WorkMode==3):#寻找红色杆子#elif(end - start < 35000):
        Red_Detect.red_Detect(img)
         #LED(1).off()
         #LED(2).off()
         #LED(3).on()
    elif(Message.Ctr.WorkMode==5): # 二维码拍照
        QRandBAR.QRcodePhoto()
         #LED(1).on()
         #LED(2).on()
         #LED(3).on()
    elif(Message.Ctr.WorkMode==6):  # 红色绕杆
        Red_Detect_Exposure.red_Detect(img)
#************************************ (C) COPYRIGHT 2023 MSL ***********************************#
