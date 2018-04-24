import pandas as pd 
import pickle
from sklearn import svm
from sklearn.metrics import confusion_matrix, classification_report
import csv
from sense_hat import SenseHat
import sys


class New_Gesture:
    
    def __init__(self):
        
        self.model = None
        self.data = None
        self.pickle_data = None


    def read_in_file(self):
        
        self.data = pd.read_csv('/home/pi/examples/RTIMULib_Data/new_gesture.csv')        
        return self.data


    # http://stackabuse.com/scikit-learn-save-and-restore-models
    def load_model(self):
        
        # read in saved model data from pickle file
        model_pkl = open('/home/pi/examples/RTIMULib/python/pickle_model.pkl', 'rb')
        #with open(pickle_file, 'rb') as file:
        #self.model2 = pickle.load(model_pkl)
        pickle_data = pickle.load(model_pkl)
        # self.model2 = pd.read_pickle()
        self.model = pickle_data
        model_pkl.close()
        
        return pickle_data


    def end_program(self):
        
        sense = SenseHat()
        sense.show_message(text_string="Thank you!", scroll_speed=0.05, text_colour=[0,0,128])
        print("Program has ended")
        sys.exit()


    #predicting from the model
    def predict_gesture(self, varx, quantx, vary, quanty, varz, quantz):
        from sense_hat import SenseHat
        import os, sys
        
        sense = SenseHat()
        if(self.model.predict([[varx, quantx, vary, quanty, varz, quantz]]))== 1:
            # gesture: down
            sense.show_letter("2")
            print("\nThe command 2 (backward) will be sent to the Cloud")
            os.system('python /home/pi/CloudScripts/cloud2.py')
            self.end_program()
            
        elif(self.model.predict([[varx, quantx, vary, quanty, varz, quantz]]))== 0:
            # gesture: circle
            sense.show_letter("5")
            print("\nThe command 5 (spin) will be sent to the Cloud")
            os.system('python /home/pi/CloudScripts/cloud5.py')
            self.end_program()
            
        elif(self.model.predict([[varx, quantx, vary, quanty, varz, quantz]]))== 4:
            # gesture: up
            sense.show_letter("1")
            print("\nThe command 1 (forward) will be sent to the Cloud")
            os.system('python /home/pi/CloudScripts/cloud1.py')
            self.end_program()
            
        elif(self.model.predict([[varx, quantx, vary, quanty, varz, quantz]]))== 2:
            # gesture: left
            sense.show_letter("3")
            print("\nThe command 3 (left) will be sent to the Cloud")
            os.system('python /home/pi/CloudScripts/cloud3.py')
            self.end_program()

        elif(self.model.predict([[varx, quantx, vary, quanty, varz, quantz]]))== 3:
            # gesture: right
            sense.show_letter("4")	
            print("\nThe command 4 (right) will be sent to the Cloud")
            os.system('python /home/pi/CloudScripts/cloud4.py')
            self.end_program()

            
        else:
            print("Not a recognized gesture")
            self.end_program()
                
        # print("Program has ended")
        # sys.exit()


# stackoverflow.com/questions/6757192/importing-a-function-from-a-class-in-another-file
if __name__ == '__main__':
    
    g1 = New_Gesture()
    g1.data = g1.read_in_file()
    g1.model = g1.load_model()
    print("New Gesture created")

    value1 = g1.data.loc[g1.data.index.min(), 'var_x']
    value2 = g1.data.loc[g1.data.index.min(), 'quant_x']
    value3 = g1.data.loc[g1.data.index.min(), 'var_y']
    value4 = g1.data.loc[g1.data.index.min(), 'quant_y']
    value5 = g1.data.loc[g1.data.index.min(), 'var_z']
    value6 = g1.data.loc[g1.data.index.min(), 'quant_z']
    print("Values stored")

    g1.predict_gesture(value1, value2, value3, value4, value5, value6)