from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json
import sys

filename = sys.argv[1:]
mes = ""
for i in range(len(filename)):
    mes += filename[i] + " " 
    
print(mes)
# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = AWSIoTMQTTClient("GesturePi")
myAWSIoTMQTTClient.configureEndpoint("a2zgnpn7ya2td1.iot.us-east-2.amazonaws.com", 8883)
myAWSIoTMQTTClient.configureCredentials("/home/pi/deviceSDK/certs/root.pem", "/home/pi/deviceSDK/certs/91479dd32d-private.pem.key", "/home/pi/deviceSDK/certs/91479dd32d-certificate.pem.crt")

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and publish to AWS IoT
myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.publish("commands/1", mes, 1)
time.sleep(2)
