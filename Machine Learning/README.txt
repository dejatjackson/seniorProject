Machine Learning Scripts

The Machine Learning Scripts include Preprocessing.py, ML_Modeling.py and New_Gesture.py. 
Combined, these scripts work together to recognize gestures performed using the
Raspberry Pi 3. 
_________________
Python Libraries: 
	Numpy
	pandas
	Scikit-learn
	Matplotlib
	SenseHat
	os
	sys
	time
	datetime
	RTIMULib
	csv
	math
	pickle
	itertools

	Scikit-learn Libraries:

		svm
		preprocessing
		train_test_split
		confusion_matrix
		GridSearchCV
		classification_report
	
_________________
Preprocessing.py

This script gathers gesture data and formats the data into the correct format.
It was used initially to gather the data for training and testing the Machine Learning model.
Once the Machine Learning model was created, the Preprocessing script can be used to gather new gestures. 

_________________
ML_Modeling.py

This script learns on the initially gathered data and creates a Machine Learning model.
This model is saved as a pickle file on the Raspberry Pi, so that the model can later be applied to new gestures. 

_______________
New_Gesture.py  

This script imports the new gesture data from the csv file created in the Preprocessing script and loads the model from the saved pickle file.
It then applies the machine learning model to the new gesture data, corresponds the result of the machine learning with a numeric value representing the gesture, 
and sends the value as a message to the cloud.
