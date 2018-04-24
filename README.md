# Iot Voice & Gesture Control System: Proof of concept implementation

### Getting Started:
#### Robot:
This folder includes all the scripts that control the robot motors. Files include: left.py, right.py, spin.py, forward.py and backward.py

#### Cloud:
This folder includes all the scripts that publish the numbers 1 to 5 to the cloud.  Files include: cloud1.py, cloud2.py, cloud3.py, cloud4.py, cloud5.py and cloudComp.py

#### Machine learning:
This folder includes all the scripts that include the preprocessing and the machine learning model. 

#### Web Application
This folder includes all the scripts that control the web application features, a bonus feature of this project. Files include: down.html, up.html, left.html, right.html, spin.html

#### Computer Controls:
This folder includes the script to control the computer. This is a bonus feature of this project.  The computer controls file subscribes to the cloud and controls features of the computer such as file explorer and firefox. Files include: comp.py

#### main.py:
This script includes all the functions for the voice implementation as well as the controls for whether a voice control or a gesture will be executed on a joystick pressed event.  


### Prerequisites:
* 2 x Raspberry Pi 3 
* Sense HAT
* Google Voice API
* USB Microphone
* Makerfire 4-Wheel Car Chassis
* L298N Motor Drive Controller
* AWS IoT


### Built With:
Python
-Libraries include:
* numpy
* pandas
* scikit-learn
* matplotlib
* pyaudio
* wave
* google.cloud
* pydub
* sense_hat
* time
* AWSIoTPythonSDK


### Authors:
Deja Jackson,
Zoe Cesar,
Amanda Norris,
Khadijah Mahaley,
Nathaniel Klein,
Richmond Mensah


### License:
This project is not licensed


### Acknowledgments:
* Dr. Mingon Kang
* Dr. Selena He
