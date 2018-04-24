
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json
import os
import sys


# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")
    response = message.payload
    if response == "1":
        print("Pybot will begin moving forwards.\n")
        os.system('sudo python /home/pi/Scripts/robot/forward.py')
    elif response == "2":
        print ("Pybot will begin moving backwards.\n")
        os.system('python /home/pi/Scripts/robot/backward.py')
    elif response == "3":
        print ("Pybot will begin moving left.\n")
        os.system('sudo python /home/pi/Scripts/robot/left.py')
    elif response == "4":
        print ("Pybot will begin moving right.\n")
        os.system('python /home/pi/Scripts/robot/right.py')
    elif response == "5":
        print ("Pybot will begin moving right.\n")
        os.system('python /home/pi/Scripts/robot/spin.py')
    else:
        print ("Command not recognized.\n")
    

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = AWSIoTMQTTClient("Robot")
myAWSIoTMQTTClient.configureEndpoint("a2zgnpn7ya2td1.iot.us-east-2.amazonaws.com", 8883)
myAWSIoTMQTTClient.configureCredentials("/home/pi/aws-iot-device-sdk-python/certs/root.pem", "/home/pi/aws-iot-device-sdk-python/certs/066cedb29b-private.pem.key", "/home/pi/aws-iot-device-sdk-python/certs/066cedb29b-certificate.pem.crt")

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

#Test
#myAWSIoTMQTTClient.customCallback = customCallback, does not work
# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
print("Connection Established")
#myAWSIoTMQTTClient.publish("commands/1", "test", 1)
myAWSIoTMQTTClient.subscribe("commands/1", 1, customCallback)

def looper():
    while True:
        time.sleep(5)

looper()

#customCallback(None, None, None)



