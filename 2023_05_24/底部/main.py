#************************************ (C) COPYRIGHT 2019 ANO ***********************************#
import sensor, image, time, math, struct
import json
# from pyb import LED,Timer
from struct import pack, unpack
import Message, My_blob1

AUTO_WHITEBAL_FLAG = False  # 必须关闭自动增益控制和自动白平衡
AUTO_GAIN_FLAG = False      # 否则他们将更改图像增益以撤消您放置的任何曝光设置
EXPOSURE_TIME_SCALE = 0.5  # 曝光时间调整比例，设置曝光时间=初始曝光时间*EXPOSURE_TIME_SCALE
AUTO_EXPOSURE = True    # 自动曝光控制，True则自动调节曝光

#初始化镜头
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.VGA)
sensor.skip_frames(time=2000)  # 等待设置生效。
print("Initial Exposure Time:%d us" % sensor.get_exposure_us())


if AUTO_EXPOSURE == False:   # 自动曝光关闭
    print("Auto Exposure Close!")
    sensor.set_auto_whitebal(False)
    sensor.set_auto_gain(False)
    sensor.skip_frames(time=500)
    current_exposure_time_in_microseconds = sensor.get_exposure_us()
    print("Current Exposure Time:%d us" % current_exposure_time_in_microseconds)
    sensor.set_auto_exposure(False,
    exposure_us=int(current_exposure_time_in_microseconds * EXPOSURE_TIME_SCALE))
    # int(current_exposure_time_in_microseconds * EXPOSURE_TIME_SCALE)

else:   # 自动曝光开启
    print("Auto Exposure Open!")
    sensor.set_auto_whitebal(False)#若想追踪颜色则关闭白平衡

print("New exposure Time:%d us" % sensor.get_exposure_us())


clock = time.clock()
#主循环
while(True):
    clock.tick()#时钟初始化
    My_blob1.DotCheck()

    #My_uart.My_uart1_Send(bytearray([0x01]))
    #My_uart.My_uart1_Send('\r\n')



    #接收串口数据
    #Message.UartReadBuffer()
    #if Message.Ctr.WorkMode==1:#点检测，色块识别

    #My_blob1.DotCheck()

    #elif (Message.Ctr.WorkMode==2):#线检测，巡线

    #My_line7.LineCheck()

    #用户数据发送
    #Message.UartSendData(Message.UserDataPack(127,127,32767,32767,65536,65536,65536,65536,65536,65536))
    #计算程序运行频率
    #if Message.Ctr.IsDebug == 1:
      #  fps=int(clock.fps())
       # Message.Ctr.T_ms = (int)(1000/fps)

    #print('fps',fps,'T_ms',Message.Ctr.T_ms)

#************************************ (C) COPYRIGHT 2019 ANO ***********************************#
