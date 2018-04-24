import os
import io

#
import pyaudio
import wave
#

from sense_hat import SenseHat
from time import sleep


#
from pydub import AudioSegment
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
#

sense = SenseHat()

def recordAndT():
    sense.clear()
    red = (255, 0, 0)
    blue = (0, 0, 255)
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    #CHUNK = 1024
    CHUNK = 4096
    #CHUNK = 16384
    #CHUNK = 2048
    RECORD_SECONDS = 6
    WAVE_OUTPUT_FILENAME = "file.wav"
    print("-----------------------------------------------------------------")

    audio = pyaudio.PyAudio()

    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print "recording..."
    #ADD A SENSEHAT FEATURE
    sense.show_letter("R", blue)
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK, exception_on_overflow = False)
        frames.append(data)


    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
    print "finished recording"
    #ADD A SENSEHAT FEATURE
    sense.show_letter("S", red)

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    #convert to flac
    os.system("avconv -i file.wav -y -ar 48000 file.flac")

    #song = AudioSegment.from_way("test.flac")
    #song.export("testme.flac", format="flac")

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/pi/Google/VoiceCommands-a9071276f9cb.json"

    # Instantiates a clients
    client = speech.SpeechClient()

    # the name of the audio file to transcribe
    file_name = os.path.join(
        os.path.dirname('/'), 'home/pi/', 'file.flac')

    # loads the audio into memory
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=48000,
        language_code='en-US')

    # detects speech in the audio file
    response = client.recognize(config, audio)


    for result in response.results:
        print('Transcript: {}'.format(result.alternatives[0].transcript))
    #ADD A SENSEHAT FEATURE 
    #sense.show_message('Transcript: {}'.format(result.alternatives[0].transcript), red) #TODO: Get this working

    #Call Cloud Scriptss
        s = result.alternatives[0].transcript 
        s = s.lower()
        print(s)
        if 'forward' in s:
                #SHOW A 1 ON SENSEHAT
                sense.show_letter("1")
                print("The command 1(forward) will be sent to the Cloud")
                os.system('python /home/pi/CloudScripts/cloud1.py')
                #sleep(0.5);
                #sense.clear(); 
        elif 'backward' in s: 
                #SHOW A 2 ON SENSEHAT 
                sense.show_letter("2")
                print("The command 2(backward) will be sent to the Cloud")
                os.system('python /home/pi/CloudScripts/cloud2.py')
        elif 'left' in s:
                #SHOW A 3 ON SENSEHAT
                sense.show_letter("3")
                print("The command 3(left) will be sent to the Cloud")
                os.system('python /home/pi/CloudScripts/cloud3.py')
        elif 'right' in s:
                #SHOW A 4 ON SENSEHAT
                sense.show_letter("4")	
                print("The command 4(right) will be sent to the Cloud")
                os.system('python /home/pi/CloudScripts/cloud4.py')
        elif 'spin' in s:
                #SHOW A 5 ON SENSEHAT
                sense.show_letter("5")
                print("The command 5(spin) will be sent to the Cloud")
                os.system('python /home/pi/CloudScripts/cloud5.py')
        elif 'open google' in s:
                #SHOW A C ON SENSEHAT
                sense.show_letter("C")
                print("The command Open Google will be sent to the Cloud")
                os.system('python /home/pi/CloudScripts/cloudComp.py ' + s) 
        elif 'close browser' in s:
                #SHOW A C ON SENSEHAT
                sense.show_letter("C")
                print("The command Close Browser will be sent to the Cloud")
                os.system('python /home/pi/CloudScripts/cloudComp.py ' + s)
        elif  'open folder' in s:
                #SHOW A C ON SENSEHAT
                sense.show_letter("C")
                print("The command Open Folder will be sent to the Cloud")
                os.system('python /home/pi/CloudScripts/cloudComp.py ' + s)

        elif 'create file' in s:
                sense.show_letter("C")
                print("The command Create File will be sent to the Cloud")
                os.system('python /home/pi/CloudScripts/cloudComp.py '+ s)
        elif 'search google' in s:
                sense.show_letter("C")
                print("The command Search Google will be sent to the Cloud")
                os.system('python /home/pi/CloudScripts/cloudComp.py '+ s)
        elif 'open file' in s:
                sense.show_letter("C")
                print("The command Open File will be sent to the Cloud")
                os.system('python /home/pi/CloudScripts/cloudComp.py ' + s)
        else: 
                #SHOW A ? ON SENSEHAT
                X = [255, 0, 0]  # Red
                O = [255, 255, 255]  # White

                question_mark = [
                O, O, O, X, X, O, O, O,
                O, O, X, O, O, X, O, O,
                O, O, O, O, O, X, O, O,
                O, O, O, O, X, O, O, O,
                O, O, O, X, O, O, O, O,
                O, O, O, X, O, O, O, O,
                O, O, O, O, O, O, O, O,
                O, O, O, X, O, O, O, O
                ]

                sense.set_pixels(question_mark)
                print("Not Recognized Command")  


print("Press the joystick in the up direction for voice, or down to enter a gesture")
flagMain = True
while flagMain:

    sense.clear()
    blue = (0, 0, 255)
    sense.show_letter("B", blue)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    for event in sense.stick.get_events():
            if event.action == "pressed":
                #print("The joystick was {} {}".format(event.action, event.direction))
                if event.direction == "up":
                #if getJoystickMovement(movement) == "pushed_up":
                    sense.show_letter("V", red)
                    # Call to Voice Class Script --> Path may need to be altered
                    print("The joystick was {} {}".format(event.action, event.direction))
                    #os.system('sudo python /home/pi/Google/recordAndTranslateVoice.py')
                    recordAndT()
                    
                    flagMain = False

                elif event.direction == "down":
                    sense.show_letter("G", blue)
                    #return Gesture() --> Modify this to the path of the first Geature Method
                    print("The joystick was {} {}".format(event.action, event.direction))
                    os.system('sudo python /home/pi/examples/RTIMULib/python/Preprocessing.py')
                    flagMain = False
                else:
                    #sense.show_letter("T")
                    pass
    sleep(4)
