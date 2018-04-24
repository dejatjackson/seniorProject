# Import required libraries
import sys
import time
import RPi.GPIO as GPIO

# Use BCM GPIO references
# instead of physical pin numbers
# GPIO.setmode(GPIO.BCM)
mode=GPIO.getmode()
print " mode ="+str(mode)
GPIO.cleanup()

# Define GPIO signals to use
# Physical pins 11,15,16,18
# GPIO17,GPIO22,GPIO23,GPIO24

RightForward=16
RightBackward=18
LeftForward=11
LeftBackward=15
sleeptime=1

GPIO.setmode(GPIO.BOARD)
GPIO.setup(RightForward, GPIO.OUT)
GPIO.setup(RightBackward, GPIO.OUT)
GPIO.setup(LeftForward, GPIO.OUT)
GPIO.setup(LeftBackward, GPIO.OUT)

def backward(x):
    GPIO.output(RightBackward, GPIO.HIGH)
    GPIO.output(LeftBackward, GPIO.HIGH)
    print "forwarding running  motor "
    time.sleep(x)
    GPIO.output(RightBackward, GPIO.LOW)
    GPIO.output(LeftBackward, GPIO.LOW)


print "backward motor "
backward(2)

print "Stopping motor"
GPIO.cleanup()
