#************************************ (C) COPYRIGHT 2023 MSL ***********************************#
import sensor, image, time, utime,math, struct
import json
from pyb import LED,Timer
from struct import pack, unpack
import Message,Barcode,QRandBAR,Red_Detect
import Yellow_Detect
#初始化镜头
sensor.reset()
sensor.set_pixformat(sensor.RGB565)#设置相机模块的像素模式
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(10)#时钟
sensor.set_auto_whitebal(False)#若想追踪颜色则关闭白平衡
clock = time.clock()#初始化时钟

yellowDetect_to_BarcodePhoto_flag = True
BarcodePhoto_to_redDetect_flag = True
redDetect_to_QRcodePhoto_flag = True

#start = utime.ticks_ms()
#主循环
while(True):

    clock.tick()#时钟初始化
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
#************************************ (C) COPYRIGHT 2023 MSL ***********************************#
