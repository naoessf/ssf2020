import math as m 
import math
import serial
import operator
import RPi.GPIO as GPIO
from time import sleep

#GPIO setup
#GPIO11 : Servo
#GPIO12 : DC
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
LED = 36
GPIO.setup(36, GPIO.OUT, initial=GPIO.LOW)
svmot = GPIO.PWM(11, 50)
dcmot = GPIO.PWM(12, 50)
svmot.start(0)
dcmot.start(0)
svmot.ChangeDutyCycle(7.5)
dcmot.ChangeDutyCycle(7.5)

#GET SERIAL
ser = serial.Serial(port = "/dev/ttyACM0", baudrate = 38400, timeout = 0.1)

y10 = str(input("first point latitude(raw_data) :"))
y11 = (y10[0:2]) 
y12 = (y10[2:]) 
y11 = float(y11)
y12 = float(y12)/60
y1 = y11 + y12
x10 = str(input("first point longtitude(raw_data) :"))
x11 = (x10[0:3])
x12 = (x10[3:])
x11 = float(x11)
x12 = float(x12)/60
x1 = x11 + x12

y20 = str(input("second point latitude(raw_data) :"))
y21 = (y20[0:2]) 
y22 = (y20[2:]) 
y21 = float(y21)
y22 = float(y22)/60
y2 = y21 + y22
x20 = str(input("second point longtitude(raw_data) :"))
x21 = (x20[0:3])
x22 = (x20[3:])
x21 = float(x21)
x22 = float(x22)/60
x2 = x21 + x22

y30 = str(input("third point latitude(raw_data) :"))
y31 = (y30[0:2]) 
y32 = (y30[2:]) 
y31 = float(y31)
y32 = float(y32)/60
y3 = y31 + y32
x30 = str(input("third point longtitude(raw_data) :"))
x31 = (x30[0:3])
x32 = (x30[3:])
x31 = float(x31)
x32 = float(x32)/60
x3 = x31 + x32

y40 = str(input("forth point latitude(raw_data) :"))
y41 = (y40[0:2])
y42 = (y40[2:]) 
y41 = float(y41)
y42 = float(y42)/60
y4 = y41 + y42
x40 = str(input("forth point longtitude(raw_data) :"))
x41 = (x40[0:3])
x42 = (x40[3:])
x41 = float(x41)
x42 = float(x42)/60
x4 = x41 + x42

y50 = str(input("fifth point latitude(raw_data) :"))
y51 = (y50[0:2]) 
y52 = (y50[2:]) 
y51 = float(y51)
y52 = float(y52)/60
y5 = y51 + y52
x50 = str(input("fifth point longtitude(raw_data) :"))
x51 = (x50[0:3])
x52 = (x50[3:])
x51 = float(x51)
x52 = float(x52)/60
x5 = x51 + x52

angle1_2 = 360 - m.atan((x2-x1)/(y1-y2))               
angle2_3 = 90 + m.atan((y3-y2)/(x2-x3))                 
angle3_4 = 360 - m.atan((x4-x3)/(y3-y4))                                 
angle4_5 = m.atan((x4-x5)/(y4-y5))                  

#GPS
def GPSparser(data):
    gps_data = list()
    idx_rmc = data.find('GNRMC')
    if data[idx_rmc:idx_rmc+5] == "GNRMC":
        data = data[idx_rmc:]
        print data
        if checksum(data):
            spliteddata = data.split(",")
            if spliteddata[2] == 'V':
                print "data invalid"
            
            elif spliteddata[2] == 'A':
                gps_data.append(float(spliteddata[1]))
                if spliteddata[4] == 'N':
                    gps_data.append(float(spliteddata[3]))

                    shiplong = str(spliteddata[5])[0:3]
                    shiplong2 = str(spliteddata[5])[3:]
                    shiplong = float(shiplong)
                    shiplong2 = float(shiplong2)/60
                    shiplongtitude = shiplong + shiplong2

                    shiplat = str(spliteddata[3])[0:2]
                    shiplat2 = str(spliteddata[3])[2:]
                    shiplat = float(shiplat)
                    shiplat2 = float(shiplat2)/60
                    shiplatitude = shiplat + shiplat

                    if x2 - 0.000022541 <= shiplongtitude <= x1 and y1 <= shiplatitude <= y3 + 0.000018195 and (270 <= shipangle <= 360 or 0 <= shipangle <= 90):
                        if shipangle < angle1_2:
                            print("right")
                            svmot.ChangeDutyCycle(9.3)
                            dcmot.ChangeDutyCycle(8)
                        elif shipangle > angle1_2:
                            print("left")
                            svmot.ChangeDutyCycle(6.7)
                            dcmot.ChangeDutyCycle(8)
                        elif shipangle == angle1_2:
                            print("straight")
                            svmot.ChangeDutyCycle(7.5)
                            dcmot.ChangeDutyCycle(8)
                        else: 
                            print("straight")
                            svmot.ChangeDutyCycle(7.5)
                            dcmot.ChangeDutyCycle(8)
                    if ((shiplongtitude <= x2 + 0.000022541 and y2 - 0.000018195 <= shiplatitude <= y2) or (shiplongtitude <= x2 and y2 <= shiplatitude <= y2 + 0.000018195)) and (0 <= shipangle <= 270):
                        print("turn left")
                        svmot.ChangeDutyCycle(6.5)
                        dcmot.ChangeDutyCycle(8)
                    if x2 + 0.000022541 <= shiplongtitude <= x3 - 0.000022541 and y3 - 0.000018195 <= shiplatitude <= y2 + 0.000018195 and 0 <= shipangle <= 270:
                        if shipangle < angle2_3:
                            print("right")
                            svmot.ChangeDutyCycle(9.3)
                            dcmot.ChangeDutyCycle(8)
                        elif shipangle > angle2_3:
                            print("left")
                            svmot.ChangeDutyCycle(6.7)
                            dcmot.ChangeDutyCycle(8)
                        elif shipangle == angle2_3:
                            print("straight")
                            svmot.ChangeDutyCycle(7.5)
                            dcmot.ChangeDutyCycle(8)
                    if x3 -  0.000022541 <= shiplongtitude <= x3 + 0.000022541 and y3 - 0.000018195 <= shiplatitude <= y3 + 0.000018195 and ((0 <= shipangle <= 90) or (270 <= shipanlge <= 360)):
                        print("turn right")
                        svmot.ChangeDutyCycle(9.5)
                        dcmot.ChangeDutyCycle(8)
                    if ((x2 + 0.000022541 <= shiplongtitude <= x3 and y2 - 0.000018195 <= shiplatitude <= y2) or (x2 <= shiplongtitude <= x3 and y2 <= shiplatitude <= y2 + 0.000018195) or (shiplongtitude <= x3 and y2 + 0.000018195 <= shiplatitude <= y4 - 0.000018195)) and (270 <= shipangle <= 360 or 0 <= shipangle <= 90):
                        if shipangle < angle3_4:
                            print("right")
                            svmot.ChangeDutyCycle(9.3)
                            dcmot.ChangeDutyCycle(8)
                        elif shipangle > angle3_4:
                            print("left")
                            svmot.ChangeDutyCycle(6.7)
                            dcmot.ChangeDutyCycle(8)
                        elif shipangle == angle3_4:
                            print("straight")
                            svmot.ChangeDutyCycle(7.5)
                            dcmot.ChangeDutyCycle(8)
                    if x4 - 0.000022541 <= shiplongtitude <= x4 + 0.000022541 and y4 - 0.000018195 <= shiplatitude <= y4 + 0.000018195 and (270 <= shipangle <= 360 or 0 <= shipangle <= 90):
                        print("turn left")
                        svmot.ChangeDutyCycle(6.5)
                        dcmot.ChangeDutyCycle(8)
                    if x4 + 0.000022541 <= shiplongtitude <= x3 and y4 - 0.000018195 <= shiplatitude <= y4 + 0.000018195:
                        print("turn right")
                        svmot.ChangeDutyCycle(9.5)
                        dcmot.ChangeDutyCycle(8)
                    if x4 - 0.000022541 <= shiplongtitude <= x5 + 0.000022541 and y4 + 0.000018195 <= shiplatitude <= y5 + 0.000018195  and (270 <= shipangle <= 360 or 0 <= shipangle <= 90):
                        if shipangle < angle4_5:
                            print("right")
                            svmot.ChangeDutyCycle(9.3)
                            dcmot.ChangeDutyCycle(8)
                        elif shipangle > angle4_5:
                            print("left")
                            svmot.ChangeDutyCycle(6.7)
                            dcmot.ChangeDutyCycle(8)
                        elif shipangle == angle4_5:
                            print("straight")
                            svmot.ChangeDutyCycle(7.5)
                            dcmot.ChangeDutyCycle(8)
                    
                else:
                    gps_data.append(-1.0*float(spliteddata[3]))

                if spliteddata[6] == 'E':
                    gps_data.append(float(spliteddata[5]))
                else:
                    gps_data.append(-1.0*float(spliteddata[5]))

                if not spliteddata[7] == '':
                    gps_data.append(float(spliteddata[7]))
                else:
                    gps_data.append(-1.0)
                if not spliteddata[8] == '':
                    gps_data.append(float(spliteddata[8]))
                else:
                    gps_data.append(-1.0)
                return gps_data
        else:
            print("checksum error")

def checksum(sentence):
    sentence = sentence.strip('\n')
    nmeadata,cksum = sentence.split('*',1)
    calc_cksum = reduce(operator.xor,(ord(s) for s in nmeadata), 0)
    print int(cksum, 16), calc_cksum
    if int(cksum, 16) == calc_cksum:
        return True
    else:
        return False

def Light(Light):
    GPIO.output(LED, GPIO.HIGH)
    sleep(0.01)
    GPIO.output(LED, GPIO.LOW)
    sleep(0.01)

while 1:
    pink = Light(Light)
    data = ser.readline()
    gps_data = GPSparser(data)    
    print gps_data

svmot.stop()
dcmot.stop()
GPIO.cleanup()