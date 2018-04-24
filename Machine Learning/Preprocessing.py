import sys, getopt
import RTIMU                            # for gathering fused sensor data
import os                               # for accessing the local os
import time                             # for getting the current time (time.now())
import timeit                           # for timing our code;  use timeit.timeit() to return num of seconds
from datetime import datetime           # to be able to call datetime.now(), and to get time deltas
from sense_hat import SenseHat          # for gathering sense_hat data
import numpy as np                      # for handling data correctly
import pandas as pd                     # for 2-D data manipulation
import math                             # for converting angles to degrees using math.degrees()
import csv
from csv import writer

ROWS_PER_GESTURE = 100

# interpolates data when there are fewer than 100 rows of data collected for a given gesture
# interpolates based on time, thus requiring the time to be moved into the index
def interpolate(df):

    print("Dtypes: {}".format(df.dtypes))
    print("Shape: {}".format(df.shape))
    
    # rounds the times so they are consistent.  This allows for the next steps to occur without errors,
    # and sets things up for data smoothing.
    df['time'] = np.round(df['time'].astype(np.int64), -8).astype('datetime64[ns]')
    
    # moves the time column into the index so it can be referenced for the resampling to follow,
    # but also keeps it as a column
    df.set_index('time', drop=True, inplace=True)
    print("\nHere you can see that the time column has been moved to the index")
                            
    for col in df.columns:
        df[col] = pd.to_numeric(df[col])

    # resamples the data by inserting a new row halfway in time between each row in the df.
    # This causes NaNs to appear in all the quantitative columns for these inserted rows
    # df = df.resample('5L').mean()
    df = df.resample('10L').mean()
    
    # Interpolates the data from the quantitative columns using the change in time as a reference
    df.interpolate(method='time', inplace=True)
    print("\nAnd here is the newly interpolated data: ")
    print("\nHead: ")
    print(df.head())
    print("\nTail: ")
    print(df.tail())

    # Reset the index to a column so if we have to call interpolate again we won't get an
    # 'Cannot reindex from a duplicate axis' error
    df.index.name = 'time'
    df.reset_index(inplace=True)
    
    return df


def check_dataframe_length(df):

    if len(df) < ROWS_PER_GESTURE:
        
        print("Initial length of dataframe : {}".format(len(df)))
        while len(df) < ROWS_PER_GESTURE:
            df = interpolate(df)
            print("Current length of dataframe: {}".format(len(df)))
            if len(df) > ROWS_PER_GESTURE:
                print("Now it's too long")
                break

    if len(df) >= ROWS_PER_GESTURE:
        df = df[:100]
        flag = pd.Series(['A']*100)
        df = pd.concat([df,flag], axis=1)
        df.columns = ['time', 'x', 'y', 'z', 'flag']
        df.loc[df.index.max(), 'flag'] = 'B'
        print("Changed last value of dataframe to 'B'")
        print("Final length of dataframe: {}".format(len(df)))

    print("Printing dataframe tail after cutting to 100 rows")
    print(df.tail())

    return df


# calculates and gets the vars and quant differences
def get_vars_and_quants(df):

    rtimu_vars_and_quants = []
    third_quant = int(len(df)*.75)
    for col in df.columns:
        rtimu_vars_and_quants.append(df[col].var())
        value = df[third_quant:third_quant + 1][col][third_quant]
        rtimu_vars_and_quants.append(value - df[col][0])

    return pd.DataFrame(pd.Series(rtimu_vars_and_quants).values.reshape(-1,6),
                                            columns=['var_x', 'quant_x', 'var_y', 'quant_y', 'var_z', 'quant_z'])


# WRITE DATA TO FILES
def append_df_to_csv_rtimu_var(df, csv_file_path_rtimu_var, sep):
    
    if not os.path.isfile(csv_file_path_rtimu_var):
        df.to_csv(csv_file_path_rtimu_var, mode='a', index=False, sep=sep)
    else:
        df.to_csv(csv_file_path_rtimu_var, mode='a', index=False, sep=sep, header=False)
    print("\nWriting rtimu_var_and_quants data to csv is complete")


def main():
    
    sys.path.append('.')

    # RTIMULib
    SETTINGS_FILE = "RTIMULib"

    print("Using settings file " + SETTINGS_FILE + ".ini")
    if not os.path.exists(SETTINGS_FILE + ".ini"):
        print("Settings file does not exist, will be created")

    s = RTIMU.Settings(SETTINGS_FILE)
    imu = RTIMU.RTIMU(s)

    print("IMU Name: " + imu.IMUName())

    if not imu.IMUInit():
        print("IMU Init Failed")
        sys.exit(1)
    else:
        print("IMU Init Succeeded")

    # this is a good time to set any fusion parameters

    imu.setSlerpPower(0.02)
    imu.setGyroEnable(True)
    imu.setAccelEnable(True)
    imu.setCompassEnable(True)

    poll_interval = imu.IMUGetPollInterval()
    print("Recommended Poll Interval: %dmS\n" % poll_interval)

    # Sense Hat
    sense = SenseHat()
    print("SenseHat has been activated")
    sense.clear()

    csv_file_path_rtimu_var = "/home/pi/examples/RTIMULib_Data/all_gestures/rtimu_var.csv"
    
    # ROWS_PER_GESTURE = 100
    print("Entering outer while loop")
    flag_outer = True
    while flag_outer:
        for event in sense.stick.get_events():
            rtimu_data = []  # rti_data list
            if event.action == "pressed":
                flag_inner = True
                while flag_inner:
                    for event in sense.stick.get_events():
                        if event.action == "held":
                            sense.show_letter("S")  # "S" for start

                            # while imu.IMURead():
                            if imu.IMURead():
                            
                                data = imu.getIMUData()
                                fusionPose = data["fusionPose"]

                                rtimu_data.append(datetime.now())
                                
                                # must store fusion data converted to  math.degrees()
                                for tup, value in enumerate(fusionPose):
                                    # print("Tuple: {}, value: {} ".format(tup, value))
                                    rtimu_data.append(math.degrees(value))

                        if event.action == "released":

                            sense.show_letter("E")  # "E" for end

                            rtimu_data_df = pd.DataFrame(pd.Series(rtimu_data).values.reshape(-1, 4),
                                                         columns=['time', 'x', 'y', 'z'])

                            # convert 'time' column to datetime64[ns]
                            rtimu_data_df.time = pd.to_datetime(rtimu_data_df.time)

                            # CHECK AND ADJUST LENGTH OF DATA FRAME AS NECESSARY
                            rtimu_data_df = check_dataframe_length(rtimu_data_df)

                            # Create a reduced dataframe containing only the numerical columns
                            # when interpolating on time
                            reduced_df = rtimu_data_df.drop(['time', 'flag'], axis=1)
                            
                            # Get & Store variances and (75th quantile - first value) values
                            rtimu_vars_and_quants_df = get_vars_and_quants(reduced_df)
                            
                            # WRITE DATA TO FILES
                            
                            # write rtimu_vars_and_quants_df to csv for original training and testing data
                            # append_df_to_csv_rtimu_var(rtimu_vars_and_quants_df, csv_file_path_rtimu_var, sep=',')
                            
                            # write new gesture data to file
                            rtimu_vars_and_quants_df.to_csv('/home/pi/examples/RTIMULib_Data/new_gesture.csv',
                                                            mode='w', index=False, sep=",")
                            
                            sense.clear()
                            
                            # call to initialize machine learning
                            # os.system('sudo python /home/pi/examples/RTIMULib/python/ML_Modeling.py')
                            
                            # call to predict on new gesture
                            os.system('sudo python /home/pi/examples/RTIMULib/python/New_Gesture.py')
                            sys.exit()
                            
                            # Prepare for new gesture when in loop (not needed)
                            
                            # rtimu_data[:] = []
                            # print("rtimu_data: {}".format(rtimu_data))
                            # rtimu_data_df.drop(rtimu_data_df.index, inplace=True)
                            # print(rtimu_data_df.empty)
                            # educed_df.drop(reduced_df.index, inplace=True)
                            # print(reduced_df.empty)
                            # rtimu_vars_and_quants_df.drop(rtimu_vars_and_quants_df.index, inplace=True)
                            # print(rtimu_vars_and_quants_df.empty)
                            # print("Press the joystick and make another gesture!")
                        # break

    flag_outer = False          
    sys.exit()
    
main()
