import sensor, image, time
AVERAGE_LIST_NUM = 3
####################求各个通道的稳定值(平均值)###########################
# 返回值是各个全局变量average值，是全局变量！！！没AVERAGE_LIST_NUM个值取一次平均值
Lmin_list = []
Lmin_average = 0
def get_Lmin_stable_value(Lmin):
    global Lmin_average
    Lmin_list.append(Lmin)
    if (len(Lmin_list) == AVERAGE_LIST_NUM):
        Lmin_average = sum(Lmin_list) / len(Lmin_list)
        Lmin_average = int(Lmin_average)
        Lmin_list.clear()

Lmax_list = []
Lmax_average = 0
def get_Lmax_stable_value(Lmax):
    global Lmax_average
    Lmax_list.append(Lmax)
    if (len(Lmax_list) == AVERAGE_LIST_NUM):
        Lmax_average = sum(Lmax_list) / len(Lmax_list)
        Lmax_average = int(Lmax_average)
        Lmax_list.clear()

Amin_list = []
Amin_average = 0
def get_Amin_stable_value(Amin):
    global Amin_average
    Amin_list.append(Amin)
    if (len(Amin_list) == AVERAGE_LIST_NUM):
        Amin_average = sum(Amin_list) / len(Amin_list)
        Amin_average = int(Amin_average)
        Amin_list.clear()

Amax_list = []
Amax_average = 0
def get_Amax_stable_value(Amax):
    global Amax_average
    Amax_list.append(Amax)
    if (len(Amax_list) == AVERAGE_LIST_NUM):
        Amax_average = sum(Amax_list) / len(Amax_list)
        Amax_average = int(Amax_average)
        Amax_list.clear()

Bmin_list = []
Bmin_average = 0
def get_Bmin_stable_value(Bmin):
    global Bmin_average
    Bmin_list.append(Bmin)
    if (len(Bmin_list) == AVERAGE_LIST_NUM):
        Bmin_average = sum(Bmin_list) / len(Bmin_list)
        Bmin_average = int(Bmin_average)
        Bmin_list.clear()

Bmax_list = []
Bmax_average = 0
def get_Bmax_stable_value(Bmax):
    global Bmax_average
    Bmax_list.append(Bmax)
    if (len(Bmax_list) == AVERAGE_LIST_NUM):
        Bmax_average = sum(Bmax_list) / len(Bmax_list)
        Bmax_average = int(Bmax_average)
        Bmax_list.clear()
##############################################################

COLOR_L_SCOPE = 20  # 自适应阈值L以众数为中心的波动范围(左右各一个COLOR_L_SCOPE值)
COLOR_A_SCOPE = 15  # 自适应阈值A以众数为中心的波动范围(左右各一个COLOR_A_SCOPE值)
COLOR_B_SCOPE = 20  # 自适应阈值B以众数为中心的波动范围(左右各一个COLOR_B_SCOPE值)
AUTO_DETECT_ROI = (120,90,80,60)

# 获取检测区域AUTO_DETECT_ROI中的阈值，并作为函数返回值roi_threshold
def roi_threshold_detect(img):
    statistics = img.get_statistics(roi=AUTO_DETECT_ROI)
    color_l = statistics.l_mode()
    color_a = statistics.a_mode()
    color_b = statistics.b_mode()
    #print(color_l,color_a,color_b)
    img.draw_rectangle(AUTO_DETECT_ROI)

    Lmin = color_l - COLOR_L_SCOPE
    if(Lmin < 0):
        Lmin = 0
    get_Lmin_stable_value(Lmin) # 将Lmin每AVERAGE_LIST_NUM次计算一次平均值得到Lmin_average

    Lmax = color_l + COLOR_L_SCOPE
    if(Lmax > 100):
        Lmax = 100
    get_Lmax_stable_value(Lmax) # 同理Lmax

    Amin = color_a - COLOR_L_SCOPE
    if (Amin < -128):
        Amin = -128
    get_Amin_stable_value(Amin)  # 将Amin每AVERAGE_LIST_NUM次计算一次平均值得到Amin_average

    Amax = color_a + COLOR_L_SCOPE
    if (Amax > 127):
        Amax = 127
    get_Amax_stable_value(Amax)

    Bmin = color_b - COLOR_B_SCOPE
    if(Bmin < -128):
        Bmin = -128
    get_Bmin_stable_value(Bmin)  # 将Bmin每AVERAGE_LIST_NUM次计算一次平均值得到Amin_average

    Bmax = color_b + COLOR_B_SCOPE
    if(Bmax > 127):
        Bmax = 127
    get_Bmax_stable_value(Bmax)

    roi_threshold = (Lmin_average,Lmax_average,Amin_average,Amax_average,Bmin_average,Bmax_average)
    print(roi_threshold)
    return roi_threshold
###########################################################

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
        roi_threshold_detect(img)
