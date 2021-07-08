import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

LED = 36

GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)

while 1:
    GPIO.output(LED, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(LED, GPIO.LOW)
    time.sleep(0.5)

GPIO.cleaup()
