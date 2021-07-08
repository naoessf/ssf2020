import math as m
import serial
import operator
import RPi.GPIO as GPIO
from time import sleep

ser = serial.Serial(port = "/dev/ttyACM0", baudrate = 38400, timeout = 0.1)	

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
LED = 36
GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)
svmotor = GPIO.PWM(11, 50)
dcmotor = GPIO.PWM(12, 50)
svmotor.start(0)
dcmotor.start(0)
svmotor.ChangeDutyCycle(7.5)
dcmotor.ChangeDutyCycle(7.5)
sleep(2)

y0 = str(input("Start Point Latitude(raw_data) : "))
x0 = str(input("Start Point Longtitude(raw_data) : "))
x0 = float(x0)
y0 = float(y0)
print("Start Point Lat : {},{}".format(y0, x0))
    

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
                                        dcmotor.ChangeDutyCycle(8)
					if (y0 + 0.0021834) > (float(spliteddata[3])) and (x0 - 0.002163936) < (float(spliteddata[5])) : 
                                            if (float(spliteddata[8])) > 290 :
                                                svmotor.ChangeDutyCycle(7.2)
                                            elif 0 <= (float(spliteddata[8])) < 30 :
                                                svmotor.ChangeDutyCycle(6.7)
                                            elif (float(spliteddata[8])) < 290 :
                                                svmotor.ChangeDutyCycle(7.8)
                                            elif (str(spliteddata[8])) == " " :
                                                svmotor.ChangeDutyCycle(7.5)
                                        if {(y0 + 0.00349344) > (float(spliteddata[3])) and (x0 - 0.002163936) > (float(spliteddata[5]))} or {(y0 + 0.00524016) >  (float(spliteddata[3])) and (x0 - 0.002975412) > (float(spliteddata[5]))} : 
                                            if (float(spliteddata[8])) > 345 :
                                                svmotor.ChangeDutyCycle(7.2)
                                            elif 0 <= (float(spliteddata[8])) < 40 :
                                                svmotor.ChangeDutyCycle(7.2)
                                            elif (float(spliteddata[8])) < 345 :
                                                svmotor.ChangeDutyCycle(7.8)
                                            elif (str(spliteddata[8])) == " " :
                                                svmotor.ChangeDutyCycle(7.5)
                                        if {(y0 + 0.00349344) < (float(spliteddata[3])) < (y0 + 0.0065502) and (x0 - 0.000540984) > (float(spliteddata[5])) > (x0 - 0.002975412)} or {(y0 + 0.00524016) < (float(spliteddata[3])) < (y0 + 0.00807858) and (x0 - 0.001622952) > (float(spliteddata[5]))} :
                                            if (float(spliteddata[8])) > 120 :
                                                svmotor.ChangeDutyCycle(7.2)
                                            elif (float(spliteddata[8])) < 120 :
                                                svmotor.ChangeDutyCycle(7.8)
                                            elif (str(spliteddata[8])) == " " :
                                                svmotor.ChangeDutyCycle(7.5)
                                        if (y0 + 0.0021834) < (float(spliteddata[3])) < (y0 + 0.0065502) and (x0 - 0.000540984) < (float(spliteddata[5])) : 
                                            if (float(spliteddata[8])) > 347.5 :
                                                svmotor.ChangeDutyCycle(7.2)
                                            elif 0 <= (float(spliteddata[8])) < 40 :
                                                svmotor.ChangeDutyCycle(7.4)
                                            elif (float(spliteddata[8])) < 347.5 :
                                                svmotor.ChangeDutyCycle(7.8)
                                            elif (str(spliteddata[8])) == " " :
                                                svmotor.ChangeDutyCycle(7.5)
                                        if {(y0 + 0.0065502) < (float(spliteddata[3])) < (y0 + 0.01135368) and (x0 - 0.001622952) < (float(spliteddata[5]))} or {(y0 + 0.00807858) < (float(spliteddata[3])) < (y0 + 0.01135368) and (x0 - 0.004868856) > (float(spliteddata[5]))} : 
                                            if (float(spliteddata[8])) > 295 :
                                                svmotor.ChangeDutyCycle(7.2)
                                            elif (float(spliteddata[8])) < 295 :
                                                svmotor.ChangeDutyCycle(7.8)
                                            elif (str(spliteddata[8])) == " " :
                                                svmotor.ChangeDutyCycle(7.5)
                                        if {(y0 + 0.00807858) < (float(spliteddata[3])) < (y0 + 0.01353708) and (x0 - 0.004868856 > (float(spliteddata[5])))} or {(y0 + 0.01135368) < (float(spliteddata[3])) < (y0 + 0.01353708) and (x0 - 0.004868856 < (float(spliteddata[5])))} : 
                                            if (float(spliteddata[8])) > 20 :
                                                svmotor.ChangeDutyCycle(7.2)
                                            elif (float(spliteddata[8])) < 20 :
                                                svmotor.ChangeDutyCycle(7.8)
                                            elif 360 >= (float(spliteddata[8])) > 320 :
                                                svmotor.ChangeDutyCycle(8)
                                            elif (str(spliteddata[8])) == " " :
                                                svmotor.ChangeDutyCycle(7.5)
                                        if (y0 + 0.01462878) < (float(spliteddata[3])) : 
                                            svmotor.ChangeDutyCycle(7.5)
                                            dcmotor.ChangeDutyCycle(7.95)
                                            sleep(2)
                                            dcmotot.ChangeDutyCycle(7.5)

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
		
				return gps_data 
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

def Light(Light):
        GPIO.output(LED, GPIO.HIGH)
        sleep(0.1)
	GPIO.output(LED, GPIO.LOW)
        sleep(0.1)

while 1:
        Green = Light(Light)
	data = ser.readline()
	gps_data  = GPSparser(data) 
	print gps_data 

svmotor.stop()
dcmotor.stop()
GPIO.cleanup
