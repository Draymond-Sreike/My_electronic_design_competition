import sensor, image, time, math, struct
import Message
from pyb import LED

Red_threshold =(20, 60, 12, 61, 12, 52)      #  红色
#Red_threshold = (15, 30, 10, 37, 0, 19)      #  红色
#Blue_threshold =(0, 48, -20, 59, -66, -28)   #  蓝色
#Green_threshold =(30, 100, -64, -8, -32, 32) #  蓝色

CENTER_LINE_Y = (320, 0, 320, 480)  # 中心交叉线(纵向)
CENTER_LINE_X = (0, 240, 640, 240)  # 中心交叉线(横向)
IMAGE_CENTER_X = 320
IMAGE_CENTER_Y = 240
CENTER_ROI = (280, 200,80,80)
class Dot(object):
    flag = 0
    color = 0
    x = 0
    y = 0

Dot=Dot()

#色块识别函数
#根据尺寸找到对应颜色的最大尺寸色块
#定义函数：找到画面中最大的指定色块
def FindMax(blobs):
    max_size=1
    if blobs:
        max_blob = 0
        for blob in blobs:
            blob_size = blob.w()*blob.h()
            #色块尺寸判断
            if ( (blob_size > max_size) & (blob_size > 100)   ) :#& (blob.density()<1.2*math.pi/4) & (blob.density()>0.8*math.pi/4)
               #宽度限幅
               if ( math.fabs( blob.w() / blob.h() - 1 ) < 2.0 ) :
                    #色块更新
                    max_blob=blob
                    #最大尺寸更新
                    max_size = blob.w()*blob.h()
        return max_blob

def LineFilter(src, dst):
  for i in range(0, len(dst), 1):
      dst[i] = src[i<<1]

#点检测
def DotCheck():
    img = sensor.snapshot(line_filter = LineFilter)#拍一张图像，line_filter是什么？？？
    red_blobs = img.find_blobs([Red_threshold], pixels_threshold=3, area_threshold=3, merge=True, margin=5)#识别红色物体
    max_blob=FindMax(red_blobs)#找到最大的那个

    if max_blob:
        # 画找出的色块
        img.draw_cross(max_blob.cx(), max_blob.cy())#物体中心画十字
        img.draw_rectangle(max_blob.rect())#画矩形框

        # 画区域标识
        img.draw_line(CENTER_LINE_Y, color=(0, 0, 255))
        img.draw_line(CENTER_LINE_X, color=(0, 0, 255))
        img.draw_rectangle(CENTER_ROI, color=(255,0,0))

        # 获取坐标并转换为与图像中心点的偏差值
        Dot.x = max_blob.cx()-IMAGE_CENTER_X    # 红色x坐标与中心x偏差（右为正，左为负）
        Dot.y = max_blob.cy()-IMAGE_CENTER_Y    # 红色y坐标与中心y偏差（上为正，下为负）
        Dot.flag = 1

        if (CENTER_ROI[0] < max_blob.cx() and  max_blob.cx() < (CENTER_ROI[0]+CENTER_ROI[2])) and (CENTER_ROI[1] < max_blob.cy() and  max_blob.cy() < (CENTER_ROI[1]+CENTER_ROI[3])):
            # 进入中心区域亮红灯
            LED(1).on()
            LED(2).off()
            LED(3).off()
        else:
            # 进入视野但未进入中心区域亮白灯
            LED(1).on()
            LED(2).on()
            LED(3).on()

    else:
        Dot.flag = 0

        LED(1).off()
        LED(2).off()
        LED(3).off()
    Message.UartSendData(Message.DotDataPack(Dot.color,Dot.flag,Dot.x,Dot.y))
    #数据打包不同，需要另写
    return Dot.flag

#串口发送数据给飞控

if __name__ == "__main__":
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)#设置相机模块的像素模式
    sensor.set_framesize(sensor.VGA)#设置相机分辨率160*120
    sensor.skip_frames(time=3000)#时钟
    sensor.set_auto_whitebal(False)#若想追踪颜色则关闭白平衡
    clock = time.clock()#初始化时钟

    #主循环
    while(True):
        clock.tick()#时钟初始化
        DotCheck()
#************************************ (C) COPYRIGHT 2019 ANO ***********************************#
