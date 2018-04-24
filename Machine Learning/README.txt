Machine Learning Scripts

The Machine Learing Scripts include Preprocessing.py, ML_Modeling.py and New_Gesture.py. 
Combined, these scripts work together to accurately recognize gestures performed using the
Raspberry Pi 3. 
_________________
Python Libraries: 
	Numpy
	pandas
	Scikit-learn
	Matplotlib
	Pydub
	Sense_hat
	os
	sys
	time
	datetime
	RTMLIB
	csv
	math
	pickle
	itertools

_________________
Preprocessing.py

This script formats the data in the correct format to the Machine Learning model. 

_________________
ML_Modeling.py

This script contains the information with the Machine Learning Model.
This model is saved as a pickle file on the Pi, so that the values can later be applied to new gestures. 
_______________
New_Gesture.py

This script corresponds a new gesture, if recognized, with a value and sends the message to a cloud. 

	