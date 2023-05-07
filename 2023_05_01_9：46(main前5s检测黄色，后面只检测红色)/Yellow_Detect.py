import sensor, image, time, utime,Message
from pyb import LED
from pyb import Timer
timer4 = Timer(4, freq=10)

CENTER_ROI = (100, 0, 120, 240)         # 中心区域，黄色物体进入该区域就给飞控发标志位
CENTER_LINE_Y = (160,0,160,240)     # 中心交叉线(纵向)
CENTER_LINE_X = (0,120,320,120)     # 中心交叉线(横向)
DISTANCE_LIST_NUM = 5                # 每DISTANCE_LIST_NUM组“距离”的数据求一次平均值
ALERT_DISTANCE = 30                     # 报警距离(cm)，小于该距离就黄灯闪烁报警
distance_list = []                                  # 用于存储计算距离平均值的距离数据
distance_average = 0                            # 距离平均值

# 测距比例，KL:色块长度比例，KW:色块宽度比例
KL = 1320
KW = 660

yellow_threshold = (15, 100, -40, 20, 29, 68)

# def value_adjust_K(distanceValue_between_block_and_sensor):
#     global KL, KW

# 寻找色块列表中最大的色块，使用这个函数一定要在色块列表中有元素才行，例如必须在if blobs_list:的条件下执行
def find_largest_blob(blobs_list):
    max_blob_pixels_value = 0
    for now_blob in blobs_list:
        if now_blob[4] > max_blob_pixels_value:
            largest_blob = now_blob
            max_blob_pixels_value = now_blob[4]
    return largest_blob

# 灯闪烁中断程序
yellow_led_glitter_mode = 0    # 默认不占有灯的控制权，即自由模式
def yellow_led_glitter_mode_set(t):  # 作为定时器的回调函数这个参数t是必要的！
    if (yellow_led_glitter_mode == 0):  # 自由模式
        pass
    elif (yellow_led_glitter_mode == 1):    # 常亮模式，黄灯常量
        LED(1).on()
        LED(2).on()
        LED(3).off()
    else:                               # 闪烁模式，黄灯闪烁
        LED(1).toggle()
        LED(2).toggle()
        LED(3).off()

timer4.callback(yellow_led_glitter_mode_set)    # 中断时执行()括号中的函数

def alert_close():
    timer4.deinit()
# 黄色异物检测
def yellow_Detect(img):
    global distance_average,yellow_led_glitter_mode
    blobs = img.find_blobs([yellow_threshold], area_threshold=250, merge=True)
    if blobs:
        # 框出色块，大概率能框到黄色异物
        max_blob = find_largest_blob(blobs)
        img.draw_rectangle(max_blob[0:4])
        img.draw_cross(max_blob[5], max_blob[6])
        img.draw_line(CENTER_LINE_Y,color=(0,0,255))
        img.draw_line(CENTER_LINE_X,color=(0,0,255))

        # 计算黄色物体的距离，每DISTANCE_LIST_NUM次得到的数据取平均值distance_average，作为有效数据
        distance_L = KL / max_blob[2]
        distance_W = KW / max_blob[3]
        distance = (distance_L + distance_W) / 2
        distance_list.append(distance)
        if(len(distance_list)==DISTANCE_LIST_NUM):
            distance_average = sum(distance_list) / len(distance_list)
            distance_average = int(distance_average)
            distance_list.clear()

        if (CENTER_ROI[0] < max_blob[5] and max_blob[5] < (CENTER_ROI[0] + CENTER_ROI[2])):
            # 距离20cm的时候测量值是最准的，距离40cm有时测量值约为34cm
            #print("长：", max_blob[2], "宽：", max_blob[3], "距离(判L)：", distance_L, "距离(判W)", distance_W,"距离(平均)", distance, "cm")

            Message.UartSendData(Message.My_Pack(0x01, distance_average))   # 将距离值打包发给飞控

            if (distance_average <= ALERT_DISTANCE):
            # 黄色异物在ALERT_DISTANCE报警距离内则闪烁
                print("靠近黄色物体！！！距离:",distance_average,"cm")
                yellow_led_glitter_mode = 2
            else:
            # 黄色异物不在报警距离内则不闪烁，黄灯常量
                print("黄色物体进入中心区域！", "距离:", distance_average, "cm")
                yellow_led_glitter_mode = 1
        else:
            yellow_led_glitter_mode = 0 # 定时器中断交出灯的控制权
            # 白灯表示物体出现在视野，但未进入中心区域
            LED(1).on()
            LED(2).on()
            LED(3).on()
            print("黄色物体进入视野！但还没有进入中心区域...")
            img.draw_rectangle(CENTER_ROI, color=(255, 255, 0))
    else:
        yellow_led_glitter_mode = 0 # 定时器中断交出灯的控制权
        # 无黄色色块在视野中被识别则关灯
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

    #start = utime.ticks_ms()
    while(True):
        clock.tick()
        img = sensor.snapshot()
        end = utime.ticks_ms()
        yellow_Detect(img)
        #if(end - start > 5000):
            #alert_close()
