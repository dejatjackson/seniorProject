import os
import sys
#sys.path.insert(0, os.path.dirname(AWSIoTPythonSDK.__file__))
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json
import webbrowser
from os.path import join

firefox_path="C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe"


def web_forward(): #opens web application
    webbrowser.register('firefox', None,webbrowser.BackgroundBrowser(firefox_path),1)
    webbrowser.get("firefox").open("file:///" + os.path.realpath("up.html"))
def web_backward(): #opens web application
    webbrowser.register('firefox', None,webbrowser.BackgroundBrowser(firefox_path),1)
    webbrowser.get("firefox").open("file:///" + os.path.realpath("down.html"))
def web_spin(): #opens web applicaton
    webbrowser.register('firefox', None,webbrowser.BackgroundBrowser(firefox_path),1)
    webbrowser.get("firefox").open("file:///" + os.path.realpath("spin.html"))
def web_left(): #opens web application
    webbrowser.register('firefox', None,webbrowser.BackgroundBrowser(firefox_path),1)
    webbrowser.get("firefox").open("file:///" + os.path.realpath("left.html"))
def web_right(): #opens web application 
    webbrowser.register('firefox', None,webbrowser.BackgroundBrowser(firefox_path),1)
    webbrowser.get("firefox").open("file:///" + os.path.realpath("right.html"))

def open_file(file): #opens a file
    try:
        print("Opening File")
        os.startfile("C:\\Users\\Deja T. Jaxson\\Desktop\\Senior_Project\\"+ file)
    except Exception as e:
        print(e)

#def search_file_system(f):
    #for root, dirs, files in os.walk('C:\\'):
        #if f in files:
            #final = join(root, f)
            #print(final)
            #print("found: %s" % join(root, f))
            #return final

def open_folder(str): #open a specific file
    os.startfile("C:\\Users\\Deja T. Jaxson\\Desktop\\Senior_Project\\"+str)

def create_new_file(name): #create a new file
    path = "C:\\Users\\Deja T. Jaxson\\Desktop\\Senior_Project\\"
   
    try:
        file = open(join(path,name),'w')
        #file.close()
        print("Opening File")
        os.startfile("C:\\Users\\Deja T. Jaxson\\Desktop\\Senior_Project\\"+ name)


    except:
        print("File not created")

def search_google(word): #using firefox so I can use chrome to have other tabs open for the project demo
    firefox_path="C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe"
    webbrowser.register('firefox', None,webbrowser.BackgroundBrowser(firefox_path),1)
    webbrowser.get("firefox").open_new_tab("https://www.google.com.tr/search?q={}".format(word))

def open_google(): #this just opens google
    firefox_path="C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe"
    word = "Testing"
    webbrowser.register('firefox', None,webbrowser.BackgroundBrowser(firefox_path),1)
    webbrowser.get("firefox").open_new_tab("https://www.google.com")

def close_browser(): #closes firefox broswer and all open tabs
    browserExe = "firefox.exe"
    os.system("taskkill /F /IM " + browserExe)



# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")
    response = message.payload
    if 'open google'  in response:
        print("Command: Open Google ")
        open_google()
    elif 'close browser' in response:
        print("Command: Close Broswer ")
        close_browser()
    elif 'open folder' in response:
        result = []
        result = response.split(" ")
        f = result[2]
        print("Command: Open Folder " + f)
        open_folder(f);
    elif 'create file' in response:
        result = []
        result = response.split(" ")
        f = result[2]
        print("Command: Create File " + f)
        create_new_file(f);
    elif 'search google' in response:
        result = []
        result = response.split(" ")
        s = result[2]
        print("Command: Google " + s)
        search_google(s)
    elif 'open file' in response:
        result = []
        result = response.split(" ")
        s = result[2]
        print("Command: Open File " + s)
        #open_file(search_file_system(s))
        open_file(s)
    elif '1' in response:
        print("Command: Web Application on Forward")
        web_forward()
    elif '2' in response:
        print("Command: Web Application on Backward")
        web_backward()
    elif '3' in response:
        print("Command: Web Application on Left")
        web_left()
    elif '4' in response:
        print("Command: Web Application on Right")
        web_right()
    elif '5' in response:
        print("Command: Web Application on Spin")
        web_spin()
    else:
        print("Command Not Recognized")

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = AWSIoTMQTTClient("DT_Comp")
myAWSIoTMQTTClient.configureEndpoint("a2zgnpn7ya2td1.iot.us-east-2.amazonaws.com", 8883)
myAWSIoTMQTTClient.configureCredentials("C:\\Users\\Deja T. Jaxson\\Desktop\\Senior_Project\\certroot.pem.key", "C:\\Users\\Deja T. Jaxson\\Desktop\\Senior_Project\\5c85b1b16f-private.pem.key", "C:\\Users\\Deja T. Jaxson\\Desktop\\Senior_Project\\5c85b1b16f-certificate.pem.crt")

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

#Test
#myAWSIoTMQTTClient.customCallback = customCallback, does not work
# Connect and subscribe to AWS IoT
print "Connection Establishing"
myAWSIoTMQTTClient.connect()
print "Connection Established"
#myAWSIoTMQTTClient.publish("commands/1", "test", 1)
myAWSIoTMQTTClient.subscribe("commands/1", 1, customCallback)

def looper():
    while True:
        time.sleep(5)

looper()

#customCallback(None, None, None)
