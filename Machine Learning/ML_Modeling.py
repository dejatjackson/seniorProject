import pandas as pd
import numpy as np
from sklearn import svm
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.metrics import confusion_matrix
import itertools
import pickle
from csv import writer
import csv
import itertools
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
import os

class GestureML:
    
    def __init__(self):
        
        self.y_fit = None
        self.y_pred = None
    
    
    def read_in_file(self):
        
        csv_var = pd.read_csv('/home/pi/examples/RTIMULib_Data/all_gestures/rtimu_var.csv')
        return csv_var
    
    # This function prints and plots the confusion matrix. Normalization can be applied by setting `normalize=True`.
    #http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html
    def plot_confusion_matrix(self, cm, classes, normalize=False, title='Confusion matrix', cmap=plt.cm.Blues):
       
        if normalize:
            cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
            print("Normalized confusion matrix")
        else:
            print('Confusion matrix, without normalization')

        print(cm)

        plt.imshow(cm, interpolation='nearest', cmap=cmap)
        plt.title(title)
        plt.colorbar()
        tick_marks = np.arange(len(classes))
        plt.xticks(tick_marks, classes, rotation=45)
        plt.yticks(tick_marks, classes)

        fmt = '.2f' if normalize else 'd'
        thresh = cm.max() / 2.
        for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
            plt.text(j, i, format(cm[i, j], fmt),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")

        plt.tight_layout()
        plt.ylabel('True label')
        plt.xlabel('Predicted label')

    
    def build_model(self):
        
        #read the csv in
        csv_var = self.read_in_file()
        print("\nvar values head {}".format(csv_var.head()))

        # Specify label inputs for the model
        csv_var_Y = csv_var.iloc[:,-1]
        
        print("Shape and values of csv_var_labels: {} \n {}".format(csv_var_Y.shape, csv_var_Y.head()))

        #Feature values of the dataset
        csv_var_X = csv_var.iloc[:,:-1]
        
        print("csv_var_feature_values {}".format(csv_var_X))
        
        # TODO: create a LabelEncoder object and fit it to each feature in csv_var_Y

        # 1. INSTANTIATE
        # encode labels with value between 0 and n_classes-1.
        le = preprocessing.LabelEncoder()

        # 2/3. FIT AND TRANSFORM
        csv_var_labels = le.fit_transform(csv_var_Y)
        csv_var_labels = csv_var_labels.reshape(-1,1)
        print("csv_var_labels2: {}".format(csv_var_labels))

        # TODO: create a OneHotEncoder object, and fit it to all of csv_var_labels

        # 1. INSTANTIATE
        enc = preprocessing.OneHotEncoder()

        # 2. FIT
        enc.fit(csv_var_labels)
        
        # 3. Transform
        onehotlabels = enc.transform(csv_var_labels).toarray()
        onehotlabels.shape

        onehotlabels

        #transform to useable values for the ML model
        onehotlabels = [np.where(r==1)[0][0] for r in onehotlabels]
        onehotlabels

        # Feature names
        csv_var_features = csv_var.columns.values[1:].tolist()
        csv_var_features
        
        #test, train, and split
        x_train, x_test, y_train, y_test = train_test_split(csv_var_X, onehotlabels, test_size = 0.20, random_state = 0)
        x_test

        '''
        # Fit the default SVM model used initially
        model = svm.SVC(kernel='rbf', decision_function_shape = 'ovo')
        # x_train2 from csv_var_x; y_train2 from onehotlabels3
        y_fit = model.fit(x_train, y_train)
        y_pred = y_fit.predict(x_test)
        
        print("Detailed classified report:")
        print()
        print("The model is trained on the full development set.")
        print("The scores are computed on the full evaluation set.")
        y_true, y_pred = y_test, model.predict(x_test)
        print(classification_report(y_true, y_pred))
        self.save_model()
        '''
        
        # Use GridSearch and 5-Fold CV to find the best model config and test on that
        parameters = [{'kernel': ['rbf'],
                       'gamma': [1e-4, 1e-3, 0.01,0.1, 0.2, 0.3],
                       'C': [1, 10, 100, 1000]},
                      {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]
        print("# Tuning hyper-parameters")
        print()
        
        model = GridSearchCV(svm.SVC(decision_function_shape='ovo'), parameters, cv=5)
        model.fit(x_train,y_train)
        
        print("Best parameters set found on development set:")
        print()
        print(model.best_params_)
        print()
        print("Grid scores on training set:")
        print()
        means = model.cv_results_['mean_test_score']
        stds = model.cv_results_['std_test_score']
        for mean, std, params in zip(means, stds, model.cv_results_['params']):
            print("%0.3f (+/-%0.03f) for %r"
                  % (mean, std * 2, params))
        
        #refitting model based on ideal params
        refit_model = model.best_estimator_
        print(refit_model)
        y_fit = model
        y_pred = y_fit.predict(x_test)
        
        print("Detailed classified report:")
        print()
        print("The model is trained on the full development set.")
        print("The scores are computed on the full evaluation set.")
        y_true, y_pred = y_test, model.predict(x_test)
        print(classification_report(y_true, y_pred))

        # Compute confusion matrix
        cnf_matrix = confusion_matrix(y_test, y_pred)
        np.set_printoptions(precision=2)
        
        # Plot non-normalized confusion matrix
        classnames = ['Forward', 'Backward', 'Left', 'Right', 'Circle']
        plt.figure()
        self.plot_confusion_matrix(cnf_matrix, classes=classnames, title='Confusion matrix, without normalization')
        plt.show()
        
        # Plot normalized confusion matrix
        plt.figure()
        self.plot_confusion_matrix(cnf_matrix, classes=classnames, normalize=True, title='Normalized confusion matrix')
        plt.show()
        
        # store values to instance of class
        self.y_fit = y_fit
        self.y_pred = y_pred

        # save the model to pickle file
        self.save_model()
        
    # Save model - write model data to pickle
    def save_model(self):
        
        # http://stackabuse.com/scikit-learn-save-and-restore-models
        pkl_filename = "pickle_model.pkl"
        model_pkl = open(pkl_filename, 'wb')
        pickle.dump(self.y_fit, model_pkl, 2)
        print("Location of pickle file: ")
        print(os.path.abspath("pickle_model.pkl"))
        model_pkl.close()


if __name__ == '__main__':
    
     create_model = GestureML()
     create_model.build_model()
     