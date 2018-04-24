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

StepPinForward=16
StepPinBackward=18
sleeptime=1

GPIO.setmode(GPIO.BOARD)
GPIO.setup(StepPinForward, GPIO.OUT)
GPIO.setup(StepPinBackward, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)

def clockwise(x):
    GPIO.output(StepPinForward, GPIO.HIGH)
    GPIO.output(15, GPIO.HIGH)
    print "forwarding running  motor "
    time.sleep(x)
    GPIO.output(StepPinForward, GPIO.LOW)
    GPIO.output(15, GPIO.LOW)

def c_clockwise(x):
    GPIO.output(StepPinBackward, GPIO.HIGH)
    GPIO.output(11, GPIO.HIGH)
    print "backwarding running motor"
    time.sleep(x)
    GPIO.output(StepPinBackward, GPIO.LOW)
    GPIO.output(11, GPIO.LOW)

print "Moving Clockwise "
clockwise(1.2)
#print "Moving Counter Clockwise "
#c_clockwise(1.2)

print "Stopping motor"
GPIO.cleanup()
