import sensor, image, time, math, struct, pyb,QRcode
import json
from pyb import LED,Timer
from struct import pack, unpack
import Message,Photography,Barcode

times1=0
times2=0

#检测到条形码拍照
def BarcodePhoto():
    global times1
    if Barcode.ScanBarcode() and times1 ==0:
        times=1
        pyb.delay(100)
        Photography.Photography('BAR1.jpg',100)
        pyb.delay(100)
        Photography.Photography('BAR2.jpg',100)
        pyb.delay(100)
        Photography.Photography('BAR3.jpg',100)
        Message.UartSendData(Message.My_Pack(2,0,0))
    else:
         print('QwQ no BarCode QwQ')
#检测到条形码则连续拍三张照片，能扫码的边界距离为13.5cm

#检测到二维码拍照
def QRcodePhoto():
    global times2
    if  QRcode.ScanQRcode() and times2 ==0:
       times2=1
       pyb.delay(100)
       Photography.Photography('QR1.jpg',100)
       pyb.delay(100)
       Photography.Photography('QR2.jpg',100)
       pyb.delay(100)
       Photography.Photography('QR3.jpg',100)
       Message.UartSendData(Message.My_Pack(4,0,0))
    else:
         print('QwQno QRcode QwQ')
#检测到有二维码出现，拍照三张 ,能扫码的极限距离为16cm
