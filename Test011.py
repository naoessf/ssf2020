#import select
import operator
from time import sleep
import math as m
import serial
import RPi.GPIO as GPIO

#GPIO Setup
#GPIO11 : Servo
#GPIO12 : DC
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
svmot = GPIO.PWM(11, 50)
dcmot = GPIO.PWM(12, 50)
svmot.start(0)
dcmot.start(0)
svmot.ChangeDutyCycle(7.5)
dcmot.ChangeDutyCycle(7.5)

#get Serial
ser = serial.Serial(port = "/dev/ttyACM0", baudrate = 38400, timeout = 0.1)

#GPS data of Start Point
y00 = str(input("Start Point Latitude(raw_data) : "))
x00 = str(input("Start Point Longtitude(raw_data) : "))
y01 = y00[0:2]
y02 = y00[2:]
x01 = x00[0:3]
x02 = x00[3:]
y01 = float(y01)
y02 = float(y02)
x01 = float(x01)
x02 = float(x02)
y03 = y02/60.000000
x03 = x02/60.000000
y0 = y01 + y03
x0 = x01 + x03
print("Start Point Lat, Long(degree) : {},{}".format(y0, x0))

#GPS data of First Point
y10 = str(input("First Point Latitude(raw_data) : "))
x10 = str(input("First Point Longtitude(raw_data) : "))
y11 = y10[0:2]
y12 = y10[2:]
x11 = x10[0:3]
x12 = x10[3:]
y11 = float(y11)
y12 = float(y12)
x11 = float(x11)
x12 = float(x12)
y13 = y12/60.00000
x13 = x12/60.00000
y1 = y11 + y13
x1 = x11 + x13
print("First Point Lat, Long(degree) : {},{}".format(y1, x1))
degree = 0

#Get Degree of N
dx = x1 - x0
dy = y1 - y0
print("dx = {}, dy = {}".format(dx, dy))

if x1 == x0 and y1 > y0:
    degree == 0
elif x1 > x0 and y1 > y0:
    degree = m.degrees(m.atan(dx/dy))
elif x1 > x0 and y1 == y0:
    degree == 90
elif x1 > x0 and y1 < y0:
    degree = 180 - abs(m.degrees(m.atan(dx/dy)))
elif x1 == x0 and y1 < y0:
    degree == 180
elif x1 < x0 and y1 < y0:
    degree = 180 + abs(m.degrees(m.atan(dx/dy)))
elif x1 < x0 and y1 == y0:
    degree == 270
elif x1 < x0 and y1 > y0:
    degree = 360 - abs(m.degrees(m.atan(dx/dy)))
print(degree)

#GPS data of Check point
count = 5

Latpoint = []
latpoint = []
latitude = []
for a in range(0,count):
    Y = str(input("{} Latitude of Check Point(raw_data): ".format(a+1)))
    Latpoint.append(Y[0:2])
    latpoint.append(Y[2:])
    latitude.append(Y)
Latpoint = list(map(float, Latpoint))
latpoint = list(map(float, latpoint))
latitude = list(map(float, latitude))

Latitude = []
for b in range(0,count):
    Y0 = float(Latpoint[b]) + (float(latpoint[b])/60)
    Latitude.append(Y0)

Longpoint = []
longpoint = []
longtitude = []
for c in range(0,count):
    X = str(input("{} Longtitude of Check Point(raw_data): ".format(c+1)))
    Longpoint.append(X[0:3])
    longpoint.append(X[3:])
    longtitude.append(X)
Longpoint = list(map(float, Longpoint))
longpoint = list(map(float, longpoint))
longtitude = list(map(float, longtitude))

Longtitude = []
for d in range(0,count):
    X0 = float(Longpoint[d]) + (float(longpoint[d]/60))
    Longtitude.append(X0)
print(Latitude)
print(Longtitude)

#Get Angle of Each Check Point
ang = 0
angle = []
for e in range(0,count-1):
    Dx = Longtitude[e+1] - Longtitude[e]
    Dy = Latitude[e+1] - Latitude[e]
    if Longtitude[e+1] == Longtitude[e] and Latitude[e+1] > Latitude[e]:
        ang == 0
    elif Longtitude[e+1] > Longtitude[e] and Latitude[e+1] > Latitude[e]:
        ang = m.degrees(m.atan(Dx/Dy))
    elif Longtitude[e+1] > Longtitude[e] and Latitude[e+1] == Latitude[e]:
        ang == 90
    elif Longtitude[e+1] > Longtitude[e] and Latitude[e+1] < Latitude[e]:
        ang = 180 - abs(m.degrees(m.atan(Dx/Dy)))
    elif Longtitude[e+1] == Longtitude[e] and Latitude[e+1] < Latitude[e]:
        ang == 180
    elif Longtitude[e+1] < Longtitude[e] and Latitude[e+1] < Latitude[e]:
        ang = 180 + abs(m.degrees(m.atan(Dx/Dy)))
    elif Longtitude[e+1] < Longtitude[e] and Latitude[e+1] == Latitude[e]:
        ang == 270
    elif Longtitude[e+1] < Longtitude[e] and Latitude[e+1] > Latitude[e]:
        ang = 360 - abs(m.degrees(m.atan(Dx/Dy)))
    angle.append(ang)
print(angle)
dcmot.ChangeDutyCycle(8.5)
#GPSparser
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

                if spliteddata[4] == 'N' :
                    gps_data.append(float(spliteddata[3]))
                else:
                    gps_data.append( -1.0*float(spliteddata[3]))

                if spliteddata[6] == 'E' :
                    gps_data.append(float(spliteddata[5]))
                else:
                    gps_data.append(-1.0*float(spliteddata[5]))

                if not spliteddata[7] == '':
                    gps_data.append(float(spliteddata[7]))
                else :
                    gps_data.append(-1.0)
                if not spliteddata[8] == '':
                    gps_data.append(float(spliteddata[8]))
                else :
                    gps_data.append(-1.0)

                #Ship Control
                #svmot : 6~7.5~10
                #dcmot : 3~7.5~12
                if not spliteddata[8] == '':
                    shipangle = float(spliteddata[8])
                    shiplatitude = float(spliteddata[3])
                    shiplongtitude = float(spliteddata[5])

                    #0-1
                    if latitude[0] <= shiplatitude <= latitude[1] and longtitude[0] <= shiplongtitude <= longtitude[1]:
                        if latitude[1] <= shiplatitude <= latitude[2] and longtitude[1] <= shiplongtitude <= longtitude[2]:
                            break
                        if latitude[1] - 0.000018195 <= shiplatitude <= latitude[1] + 0.000018195 and longtitude[1] - 0.000022541 <= shiplongtitude <= longtitude[1] + 0.000022541:
                            break
                        if shipangle > angle[0]:
                            svmot.ChangeDutyCycle(6.5)
                            dcmot.ChangeDutyCycle(8)
                            print("Left 1")
                            break
                        elif shipangle < angle[0]:
                            svmot.ChangeDutyCycle(9.5)
                            dcmot.ChangeDutyCycle(8)
                            print("Right 1")
                            break
                        elif shipangle == angle[0]:
                            svmot.ChangeDutyCycle(7.5)
                            dcmot.ChangeDutyCycle(8.5)
                            print("Straight 1")
                            break

                    if latitude[0] <= shiplatitude <= latitude[1] and longtitude[0] <= shiplongtitude <= longtitude[1] and latitude[1] <= shiplatitude <= latitude[2] and longtitude[1] <= shiplongtitude <= longtitude[2]:
                        if latitude[1] - 0.000018195 <= shiplatitude <= latitude[1] + 0.000018195 and longtitude[1] - 0.000022541 <= shiplongtitude <= longtitude[1] + 0.000022541:
                            break
                        if 0 < angle[0] < 90:
                            if 0 < shipangle < 90:
                                if shipangle > angle[0]:
                                    svmot.ChangeDutyCycle(6.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Left 1.3")
                                    break
                                elif shipangle < angle[0]:
                                    svmot.ChangeDutyCycle(9.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Right 1.3")
                                    break
                                else:
                                    break
                        if 90 < angle[0] < 180:
                            if 90 < shipangle < 180:
                                if shipangle > angle[0]:
                                    svmot.ChangeDutyCycle(6.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Left 1.3")
                                    break
                                elif shipangle < angle[0]:
                                    svmot.ChangeDutyCycle(9.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Right 1.3")
                                    break
                                else:
                                    break
                        if 180 < angle[0] < 270:
                            if 180 < shipangle < 270:
                                if shipangle > angle[0]:
                                    svmot.ChangeDutyCycle(6.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Left 1.3")
                                    break
                                elif shipangle < angle[0]:
                                    svmot.ChangeDutyCycle(9.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Right 1.3")
                                    break
                                else:
                                    break
                        if 270 < angle[0] < 360:
                            if 270 < shipangle < 360:
                                if shipangle > angle[0]:
                                    svmot.ChangeDutyCycle(6.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Left 1.3")
                                    break
                                elif shipangle < angle[0]:
                                    svmot.ChangeDutyCycle(9.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Right 1.3")
                                    break
                                else:
                                    break
                        if 0 < angle[1] < 90:
                            if 0 < shipangle < 90:
                                if shipangle > angle[1]:
                                    svmot.ChangeDutyCycle(6.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Left 2.3")
                                    break
                                elif shipangle < angle[1]:
                                    svmot.ChangeDutyCycle(9.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Right 2.3")
                                    break
                                else:
                                    break
                        if 90 < angle[1] < 180:
                            if 90 < shipangle < 180:
                                if shipangle > angle[1]:
                                    svmot.ChangeDutyCycle(6.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Left 2.3")
                                    break
                                elif shipangle < angle[1]:
                                    svmot.ChangeDutyCycle(9.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Right 2.3")
                                    break
                                else:
                                    break
                        if 180 < angle[1] < 270:
                            if 180 < shipangle < 270:
                                if shipangle > angle[1]:
                                    svmot.ChangeDutyCycle(6.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Left 2.3")
                                    break
                                elif shipangle < angle[1]:
                                    svmot.ChangeDutyCycle(9.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Right 2.3")
                                    break
                                else:
                                    break
                        if 270 < angle[1] < 360:
                            if 270 < shipangle < 360:
                                if shipangle > angle[1]:
                                    svmot.ChangeDutyCycle(6.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Left 2.3")
                                    break
                                elif shipangle < angle[1]:
                                    svmot.ChangeDutyCycle(9.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Right 2.3")
                                    break
                                else:
                                    break

                    if latitude[1] - 0.000018195 <= shiplatitude <= latitude[1] + 0.000018195 and longtitude[1] - 0.000022541 <= shiplongtitude <= longtitude[1] + 0.000022541:
                        if shipangle > angle[1]:
                            svmot.ChangeDutyCycle(6.5)
                            dcmot.ChangeDutyCycle(8)
                            print("Left 1.6")
                            break
                        if shipangle < angle[1]:
                            svmot.ChangeDutyCycle(8.5)
                            dcmot.ChangeDutyCycle(8)
                            print("Right 1.6")
                            break

                    #1-2
                    if latitude[1] <= shiplatitude <= latitude[2] and longtitude[1] <= shiplongtitude <= longtitude[2]:
                        if latitude[2] <= shiplatitude <= latitude[3] and longtitude[2] <= shiplongtitude <= longtitude[3]:
                            break
                        if latitude[2] - 0.000018195 <= shiplatitude <= latitude[2] + 0.000018195 and longtitude[2] - 0.000022541 <= shiplongtitude <= longtitude[2] + 0.000022541:
                            break
                        if shipangle > angle[1]:
                            svmot.ChangeDutyCycle(6.5)
                            dcmot.ChangeDutyCycle(8)
                            print("Left 1")
                            break
                        elif shipangle < angle[1]:
                            svmot.ChangeDutyCycle(9.5)
                            dcmot.ChangeDutyCycle(8)
                            print("Right 1")
                            break
                        elif shipangle == angle[1]:
                            svmot.ChangeDutyCycle(7.5)
                            dcmot.ChangeDutyCycle(8.5)
                            print("Straight 1")
                            break

                    if latitude[1] <= shiplatitude <= latitude[2] and longtitude[1] <= shiplongtitude <= longtitude[2] and latitude[2] <= shiplatitude <= latitude[3] and longtitude[2]] <= shiplongtitude <= longtitude[3]:
                        if latitude[2] - 0.000018195 <= shiplatitude <= latitude[2] + 0.000018195 and longtitude[2] - 0.000022541 <= shiplongtitude <= longtitude[2] + 0.000022541:
                            break
                        if 0 < angle[1] < 90:
                            if 0 < shipangle < 90:
                                if shipangle > angle[1]:
                                    svmot.ChangeDutyCycle(6.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Left 1.3")
                                    break
                                elif shipangle < angle[1]:
                                    svmot.ChangeDutyCycle(9.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Right 1.3")
                                    break
                                else:
                                    break
                        if 90 < angle[1] < 180:
                            if 90 < shipangle < 180:
                                if shipangle > angle[1]:
                                    svmot.ChangeDutyCycle(6.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Left 1.3")
                                    break
                                elif shipangle < angle[1]:
                                    svmot.ChangeDutyCycle(9.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Right 1.3")
                                    break
                                else:
                                    break
                        if 180 < angle[1] < 270:
                            if 180 < shipangle < 270:
                                if shipangle > angle[1]:
                                    svmot.ChangeDutyCycle(6.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Left 1.3")
                                    break
                                elif shipangle < angle[1]:
                                    svmot.ChangeDutyCycle(9.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Right 1.3")
                                    break
                                else:
                                    break
                        if 270 < angle[1] < 360:
                            if 270 < shipangle < 360:
                                if shipangle > angle[1]:
                                    svmot.ChangeDutyCycle(6.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Left 1.3")
                                    break
                                elif shipangle < angle[1]:
                                    svmot.ChangeDutyCycle(9.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Right 1.3")
                                    break
                                else:
                                    break
                        if 0 < angle[2] < 90:
                            if 0 < shipangle < 90:
                                if shipangle > angle[2]:
                                    svmot.ChangeDutyCycle(6.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Left 2.3")
                                    break
                                elif shipangle < angle[2]:
                                    svmot.ChangeDutyCycle(9.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Right 2.3")
                                    break
                                else:
                                    break
                        if 90 < angle[2] < 180:
                            if 90 < shipangle < 180:
                                if shipangle > angle[2]:
                                    svmot.ChangeDutyCycle(6.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Left 2.3")
                                    break
                                elif shipangle < angle[2]:
                                    svmot.ChangeDutyCycle(9.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Right 2.3")
                                    break
                                else:
                                    break
                        if 180 < angle[2] < 270:
                            if 180 < shipangle < 270:
                                if shipangle > angle[2]:
                                    svmot.ChangeDutyCycle(6.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Left 2.3")
                                    break
                                elif shipangle < angle[2]:
                                    svmot.ChangeDutyCycle(9.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Right 2.3")
                                    break
                                else:
                                    break
                        if 270 < angle[2] < 360:
                            if 270 < shipangle < 360:
                                if shipangle > angle[2]:
                                    svmot.ChangeDutyCycle(6.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Left 2.3")
                                    break
                                elif shipangle < angle[2]:
                                    svmot.ChangeDutyCycle(9.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Right 2.3")
                                    break
                                else:
                                    break

                    if latitude[2] - 0.000018195 <= shiplatitude <= latitude[2] + 0.000018195 and longtitude[2] - 0.000022541 <= shiplongtitude <= longtitude[2] + 0.000022541:
                        if shipangle > angle[2]:
                            svmot.ChangeDutyCycle(6.5)
                            dcmot.ChangeDutyCycle(8)
                            print("Left 1.6")
                            break
                        if shipangle < angle[2]:
                            svmot.ChangeDutyCycle(8.5)
                            dcmot.ChangeDutyCycle(8)
                            print("Right 1.6")
                            break


                    #2-3
                    if latitude[2] <= shiplatitude <= latitude[3] and longtitude[2] <= shiplongtitude <= longtitude[3]:
                        if latitude[3] <= shiplatitude <= latitude[4] and longtitude[3] <= shiplongtitude <= longtitude[4]:
                            break
                        if latitude[3] - 0.000018195 <= shiplatitude <= latitude[3] + 0.000018195 and longtitude[3] - 0.000022541 <= shiplongtitude <= longtitude[3] + 0.000022541:
                            break
                        if shipangle > angle[2]:
                            svmot.ChangeDutyCycle(6.5)
                            dcmot.ChangeDutyCycle(8)
                            print("Left 1")
                            break
                        elif shipangle < angle[2]:
                            svmot.ChangeDutyCycle(9.5)
                            dcmot.ChangeDutyCycle(8)
                            print("Right 1")
                            break
                        elif shipangle == angle[2]:
                            svmot.ChangeDutyCycle(7.5)
                            dcmot.ChangeDutyCycle(8.5)
                            print("Straight 1")
                            break

                    if latitude[2] <= shiplatitude <= latitude[3] and longtitude[2] <= shiplongtitude <= longtitude[3] and latitude[2] <= shiplatitude <= latitude[3] and longtitude[2] <= shiplongtitude <= longtitude[3]:
                        if latitude[2] - 0.000018195 <= shiplatitude <= latitude[3] + 0.000018195 and longtitude[2] - 0.000022541 <= shiplongtitude <= longtitude[3] + 0.000022541:
                            break
                        if 0 < angle[2] < 90:
                            if 0 < shipangle < 90:
                                if shipangle > angle[2]:
                                    svmot.ChangeDutyCycle(6.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Left 1.3")
                                    break
                                elif shipangle < angle[2]:
                                    svmot.ChangeDutyCycle(9.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Right 1.3")
                                    break
                                else:
                                    break
                        if 90 < angle[2] < 180:
                            if 90 < shipangle < 180:
                                if shipangle > angle[2]:
                                    svmot.ChangeDutyCycle(6.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Left 1.3")
                                    break
                                elif shipangle < angle[2]:
                                    svmot.ChangeDutyCycle(9.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Right 1.3")
                                    break
                                else:
                                    break
                        if 180 < angle[2] < 270:
                            if 180 < shipangle < 270:
                                if shipangle > angle[2]:
                                    svmot.ChangeDutyCycle(6.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Left 1.3")
                                    break
                                elif shipangle < angle[2]:
                                    svmot.ChangeDutyCycle(9.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Right 1.3")
                                    break
                                else:
                                    break
                        if 270 < angle[2] < 360:
                            if 270 < shipangle < 360:
                                if shipangle > angle[2]:
                                    svmot.ChangeDutyCycle(6.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Left 1.3")
                                    break
                                elif shipangle < angle[2]:
                                    svmot.ChangeDutyCycle(9.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Right 1.3")
                                    break
                                else:
                                    break
                        if 0 < angle[3] < 90:
                            if 0 < shipangle < 90:
                                if shipangle > angle[3]:
                                    svmot.ChangeDutyCycle(6.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Left 2.3")
                                    break
                                elif shipangle < angle[3]:
                                    svmot.ChangeDutyCycle(9.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Right 2.3")
                                    break
                                else:
                                    break
                        if 90 < angle[3] < 180:
                            if 90 < shipangle < 180:
                                if shipangle > angle[3]:
                                    svmot.ChangeDutyCycle(6.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Left 2.3")
                                    break
                                elif shipangle < angle[3]:
                                    svmot.ChangeDutyCycle(9.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Right 2.3")
                                    break
                                else:
                                    break
                        if 180 < angle[3] < 270:
                            if 180 < shipangle < 270:
                                if shipangle > angle[3]:
                                    svmot.ChangeDutyCycle(6.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Left 2.3")
                                    break
                                elif shipangle < angle[3]:
                                    svmot.ChangeDutyCycle(9.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Right 2.3")
                                    break
                                else:
                                    break
                        if 270 < angle[3] < 360:
                            if 270 < shipangle < 360:
                                if shipangle > angle[3]:
                                    svmot.ChangeDutyCycle(6.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Left 2.3")
                                    break
                                elif shipangle < angle[3]:
                                    svmot.ChangeDutyCycle(9.5)
                                    dcmot.ChangeDutyCycle(8)
                                    print("Right 2.3")
                                    break
                                else:
                                    break

                    if latitude[3] - 0.000018195 <= shiplatitude <= latitude[3] + 0.000018195 and longtitude[3] - 0.000022541 <= shiplongtitude <= longtitude[3] + 0.000022541:
                        if shipangle > angle[3]:
                            svmot.ChangeDutyCycle(6.5)
                            dcmot.ChangeDutyCycle(8)
                            print("Left 1.6")
                            break
                        if shipangle < angle[3]:
                            svmot.ChangeDutyCycle(8.5)
                            dcmot.ChangeDutyCycle(8)
                            print("Right 1.6")
                            break


                    #3-4
                    if latitude[3] <= shiplatitude <= latitude[4] and longtitude[3] <= shiplongtitude <= longtitude[4]:
                        if latitude[3] - 0.000018195 <= shiplatitude <= latitude[3] + 0.000018195 and longtitude[3] - 0.000022541 <= shiplongtitude <= longtitude[3] + 0.000022541:
                            break
                        if shipangle > angle[3]:
                            svmot.ChangeDutyCycle(6.5)
                            dcmot.ChangeDutyCycle(8)
                            print("Left 1")
                            break
                        elif shipangle < angle[3]:
                            svmot.ChangeDutyCycle(9.5)
                            dcmot.ChangeDutyCycle(8)
                            print("Right 1")
                            break
                        elif shipangle == angle[3]:
                            svmot.ChangeDutyCycle(7.5)
                            dcmot.ChangeDutyCycle(8.5)
                            print("Straight 1")
                            break

                return gps_data
            print (spliteddata) 
        else :
            print "checksum error"

def checksum(sentence):
    sentence = sentence.strip('\n')
    nmeadata, cksum = sentence.split('*',1)
    calc_cksum = reduce(operator.xor, (ord(s) for s in nmeadata), 0)
    print int(cksum,16), calc_cksum
    if int(cksum,16) == calc_cksum:
        return True 
    else:
        return False 

while True: 
    data = ser.readline()
    gps_data = GPSparser(data)

svmot.stop()
dcmot.stop()
GPIO.cleanup()