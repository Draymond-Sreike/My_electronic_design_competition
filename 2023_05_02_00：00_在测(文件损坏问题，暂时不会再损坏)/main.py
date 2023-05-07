#************************************ (C) COPYRIGHT 2019 ANO ***********************************#
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

start = utime.ticks_ms()
#主循环
while(True):
    clock.tick()#时钟初始化
    end = utime.ticks_ms()
    img = sensor.snapshot()
    ##接收串口数据
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

    #if (Message.Ctr.WorkMode==1): # 识别黄色条形码#if(end - start < 5000):
    #Yellow_Detect.yellow_Detect(img)

    #elif (Message.Ctr.WorkMode==2): # 条形码拍照#elif(end - start < 30000):
        #Yellow_Detect.alert_close()
    ##if(yellowDetect_to_BarcodePhoto_flag == True):
        ### 将黄灯距离报警指示灯关闭，并将图像格式更换为VGA以便于接下来的条形码拍照
        ##Yellow_Detect.alert_close()
        ##sensor.set_framesize(sensor.QVGA)
        ##sensor.skip_frames(time=1000)
        ### sensor.set_auto_gain(False)      # 必须关闭此功能，以防止图像冲洗…
        ### sensor.set_auto_whitebal(False)  # 必须关闭此功能，以防止图像冲洗…
        ##yellowDetect_to_BarcodePhoto_flag = False
        #QRandBAR.BarcodePhoto()

    #elif (Message.Ctr.WorkMode==3):#寻找红色杆子#elif(end - start < 35000):
        ##if(BarcodePhoto_to_redDetect_flag == True):
            ##sensor.set_framesize(sensor.QVGA)
            ##sensor.skip_frames(10)
            ### sensor.set_auto_whitebal(False)#若想追踪颜色则关闭白平衡
            ##BarcodePhoto_to_redDetect_flag = False
        #Red_Detect.red_Detect(img)

    #else: # 二维码拍照
    ##if(redDetect_to_QRcodePhoto_flag == True):
        ##sensor.set_framesize(sensor.QVGA)
        ##sensor.skip_frames(time=1000)
        ## sensor.set_auto_gain(False)      # 必须关闭此功能，以防止图像冲洗…
        ## sensor.set_auto_whitebal(False)  # 必须关闭此功能，以防止图像冲洗…
        ##redDetect_to_QRcodePhoto_flag = False
        #QRandBAR.QRcodePhoto()

    #计算程序运行频率
    """
    if Message.Ctr.IsDebug == 1:
        fps=int(clock.fps())
        Message.Ctr.T_ms = (int)(1000/fps)
        print('fps',fps,'T_ms',Message.Ctr.T_ms)

    """
#************************************ (C) COPYRIGHT 2019 ANO ***********************************#
