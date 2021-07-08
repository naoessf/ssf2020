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
count = int(input('Count of Check Point : '))

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

                    f = count - 1
                    while f >= 0:
                        print(f)
                        if f == 0:
                            break
                        elif f != 0:
                            if latitude[f-1] <= shiplatitude <= latitude[f] and longtitude[f-1] <= shiplongtitude <= longtitude[f]:
                                if shipangle > angle[f-1]:
                                    svmot.ChangeDutyCycle(6)
                                    dcmot.ChangeDutyCycle(8.5)
                                    print("left 1")
                                    f -= 1
                                    break
                                elif shipangle < angle[f-1]:
                                    svmot.ChangeDutyCycle(10)
                                    dcmot.ChangeDutyCycle(8.5)
                                    print("right 1")
                                    f -= 1
                                    break
                                else:
                                    svmot.ChangeDutyCycle(7.5)
                                    dcmot.ChangeDutyCycle(8.5)
                                    print("straight 1")
                                    f -= 1
                                    break
                            if f == 0:
                                break
                                if latitude[f] - 0.000018195 <= shiplatitude <= latitude[f] + 0.000018195 and longtitude[f] - 0.00002254 <= shiplongtitude <= longtitude[f] + 0.00002254:
                                    break
                                if f != count - 1:
                                    if latitude[f] <= shiplatitude <= latitude[f+1] and longtitude[f] <= shiplatitude <= longtitude[f+1]:
                                        break
                            elif latitude[f] - 0.000018195 <= shiplatitude <= latitude[f] + 0.000018195 and longtitude[f] - 0.00002254 <= shiplongtitude <= longtitude[f] + 0.00002254:
                                if shipangle > angle[f]:
                                    svmot.ChangeDutyCycle(6)
                                    dcmot.ChangeDutyCycle(8.5)
                                    print("left 2")
                                    f -= 1
                                    break
                                elif shipangle < angle[f]:
                                    svmot.ChangeDutyCycle(10)
                                    dcmot.ChangeDutyCycle(8.5)
                                    print("right 2")
                                    f -= 1
                                    break
                                else:
                                    svmot.ChangeDutyCycle(7.5)
                                    dcmot.ChangeDutyCycle(8.5)
                                    print("straight 2")
                                    f -= 1
                                    break
                            if f == 0:
                                break

                            #If Range Out
                            if not (latitude[f-1] <= shiplatitude <= latitude[f] and longtitude[f-1] <= shiplongtitude <= longtitude[f]):
                                if f == 0:
                                    break
                                #1 Quadrant
                                if latitude[f]<shiplatitude and longtitude[f-1]>shiplongtitude:
                                    svmot.ChangeDutyCycle(10)
                                    dcmot.ChangeDutyCycle(8)
                                    print("right")
                                    f -= 1
                                    if f == 0:
                                        break
                                    break
                                if longtitude[f-1]<shiplongtitude<longtitude[f] and shiplatitude>latitude[f]:
                                    svmot.ChangeDutyCycle(10)
                                    dcmot.ChangeDutyCycle(8)
                                    print("right")
                                    f -= 1
                                    if f == 0:
                                        break
                                    break
                                if longtitude[f]<shiplongtitude and latitude[f]<shiplatitude:
                                    f -= 1
                                    if f == 0:
                                        break
                                    break
                                if shiplongtitude<longtitude[f-1] and latitude[f-1]<shiplatitude<latitude[f]:
                                    svmot.ChangeDutyCycle(10)
                                    dcmot.ChangeDutyCycle(8)
                                    print("right")
                                    f -= 1
                                    if f == 0:
                                        break
                                    break
                                if longtitude[f]<shiplongtitude and latitude[f-1]<shiplatitude<latitude[f]:
                                    svmot.ChangeDutyCycle(6)
                                    dcmot.ChangeDutyCycle(8)
                                    f -= 1
                                    if f == 0:
                                        break
                                    break
                                if shiplongtitude<longtitude[f-1] and shiplatitude<latitude[f-1]:
                                    svmot.ChangeDutyCycle(10)
                                    dcmot.ChangeDutyCycle(8)
                                    print("right")
                                    f -= 1
                                    if f == 0:
                                        break
                                    break
                                if longtitude[f-1]<shiplongtitude<longtitude[f] and shiplatitude<latitude[f-1]:
                                    svmot.ChangeDutyCycle(6)
                                    dcmot.ChangeDutyCycle(8)
                                    f -= 1
                                    if f == 0:
                                        break
                                    break
                                if longtitude[f]<shiplongtitude and shiplatitude<latitude[f-1]:
                                    svmot.ChangeDutyCycle(6)
                                    dcmot.ChangeDutyCycle(8)
                                    f -= 1
                                    if f == 0:
                                        break
                                    break
                                #2 Quadrant
                                if shiplongtitude<longtitude[f] and shiplatitude>latitude[f]:
                                    f -= 1
                                    if f == 0:
                                        break
                                    break
                                if longtitude[f]<shiplongtitude<longtitude[f-1] and latitude[f]<shiplatitude:
                                    svmot.ChangeDutyCycle(6)
                                    dcmot.ChangeDutyCycle(8)
                                    f -= 1
                                    if f == 0:
                                        break
                                    break
                                if longtitude[f-1]<shiplongtitude and latitude[f]<shiplatitude:
                                    svmot.ChangeDutyCycle(6)
                                    dcmot.ChangeDutyCycle(8)
                                    f -= 1
                                    if f == 0:
                                        break
                                    break
                                if shiplongtitude<longtitude[f] and latitude[f-1]<shiplatitude<latitude[f]:
                                    svmot.ChangeDutyCycle(10)
                                    dcmot.ChangeDutyCycle(8)
                                    print("right")
                                    f -= 1
                                    if f == 0:
                                        break
                                    break
                                if longtitude[f-1]<shiplongtitude and latitude[f-1]<shiplatitude<latitude[f]:
                                    svmot.ChangeDutyCycle(6)
                                    dcmot.ChangeDutyCycle(8)
                                    f -= 1
                                    if f == 0:
                                        break
                                    break
                                if shiplongtitude<longtitude[f] and latitude[f-1]>shiplatitude:
                                    svmot.ChangeDutyCycle(10)
                                    dcmot.ChangeDutyCycle(8)
                                    print("right")
                                    f -= 1
                                    if f == 0:
                                        break
                                    break
                                if longtitude[f]<shiplongtitude<longtitude[f-1] and shiplatitude<latitude[f-1]:
                                    svmot.ChangeDutyCycle(10)
                                    dcmot.ChangeDutyCycle(8)
                                    print("right")
                                    f -= 1
                                    if f == 0:
                                        break
                                    break
                                if longtitude[f-1]<shiplongtitude and shiplatitude<latitude[f-1]:
                                    svmot.ChangeDutyCycle(6)
                                    dcmot.ChangeDutyCycle(8)
                                    f -= 1
                                    if f == 0:
                                        break
                                    break
                                #3 Quadrant
                                if shiplongtitude<longtitude[f] and shiplatitude>latitude[f-1]:
                                    svmot.ChangeDutyCycle(6)
                                    dcmot.ChangeDutyCycle(8)
                                    f -= 1
                                    if f == 0:
                                        break
                                    break
                                if longtitude[f]<shiplongtitude<longtitude[f-1] and latitude[f-1]<shiplatitude:
                                    svmot.ChangeDutyCycle(6)
                                    dcmot.ChangeDutyCycle(8)
                                    f -= 1
                                    if f == 0:
                                        break
                                    break
                                if longtitude[f-1]<shiplongtitude and latitude[f-1]<shiplatitude:
                                    svmot.ChangeDutyCycle(6)
                                    dcmot.ChangeDutyCycle(8)
                                    f -= 1
                                    if f == 0:
                                        break
                                    break
                                if shiplongtitude<longtitude[f] and latitude[f]<shiplatitude<latitude[f-1]:
                                    svmot.ChangeDutyCycle(6)
                                    dcmot.ChangeDutyCycle(8)
                                    f -= 1
                                    if f == 0:
                                        break
                                    break
                                if longtitude[f-1]<shiplongtitude and latitude[f]<shiplatitude<latitude[f-1]:
                                    svmot.ChangeDutyCycle(10)
                                    dcmot.ChangeDutyCycle(8)
                                    print("right")
                                    f -= 1
                                    if f == 0:
                                        break
                                    break
                                if shiplongtitude<longtitude[f] and shiplatitude<latitude[f]:
                                    f -= 1
                                    if f == 0:
                                        break
                                    break
                                if longtitude[f]<shiplongtitude<longtitude[f-1] and shiplatitude<latitude[f]:
                                    svmot.ChangeDutyCycle(10)
                                    dcmot.ChangeDutyCycle(8)
                                    print("right")
                                    f -= 1
                                    if f == 0:
                                        break
                                    break
                                if longtitude[f-1]<shiplongtitude and shiplatitude<latitude[f]:
                                    svmot.ChangeDutyCycle(10)
                                    dcmot.ChangeDutyCycle(8)
                                    print("right")
                                    f -= 1
                                    if f == 0:
                                        break
                                    break
                                #4 Quadrant
                                if shiplongtitude<longtitude[f-1] and latitude[f-1]<shiplatitude:
                                    svmot.ChangeDutyCycle(10)
                                    dcmot.ChangeDutyCycle(8)
                                    print("right")
                                    f -= 1
                                    if f == 0:
                                        break
                                    break
                                if longtitude[f-1]<shiplongtitude<longtitude[f] and latitude[f-1]<shiplatitude:
                                    svmot.ChangeDutyCycle(10)
                                    dcmot.ChangeDutyCycle(8)
                                    print("right")
                                    f -= 1
                                    if f == 0:
                                        break
                                    break
                                if longtitude[f]<shiplongtitude and latitude[f-1]<shiplatitude:
                                    svmot.ChangeDutyCycle(10)
                                    dcmot.ChangeDutyCycle(8)
                                    print("right")
                                    f -= 1
                                    if f == 0:
                                        break
                                    break
                                if shiplongtitude<longtitude[f-1] and latitude[f]<shiplatitude<latitude[f-1]:
                                    svmot.ChangeDutyCycle(6)
                                    dcmot.ChangeDutyCycle(8)
                                    f -= 1
                                    if f == 0:
                                        break
                                    break
                                if longtitude[f]<shiplongtitude and latitude[f]<shiplatitude<latitude[f-1]:
                                    svmot.ChangeDutyCycle(10)
                                    dcmot.ChangeDutyCycle(8)
                                    print("right")
                                    f -= 1
                                    if f == 0:
                                        break
                                    break
                                if shiplongtitude<longtitude[f-1] and shiplatitude<latitude[f]:
                                    svmot.ChangeDutyCycle(6)
                                    dcmot.ChangeDutyCycle(8)
                                    f -= 1
                                    if f == 0:
                                        break
                                    break
                                if longtitude[f-1]<shiplongtitude<longtitude[f] and shiplatitude<latitude[f]:
                                    svmot.ChangeDutyCycle(6)
                                    dcmot.ChangeDutyCycle(8)
                                    f -= 1
                                    if f == 0:
                                        break
                                    break
                                if longtitude[f]<shiplongtitude and shiplatitude<latitude[f]:
                                    f -= 1
                                    if f == 0:
                                        break
                                    break

                            else:
                                print("continue")
                                f -= 1
                                continue

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