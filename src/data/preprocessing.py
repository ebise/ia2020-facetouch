import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np
import glob

def loaddata():
  file_paths = '../data/raw/'
  filenames = glob.glob(file_paths+"*[0-9].csv",recursive = True)
  list_of_dfs = [pd.read_csv(filename) for filename in filenames]
  data_list = []
  for dataframe, filename in zip(list_of_dfs, filenames):
    dataframe=dataframe.drop(columns=['acc_x','acc_y','acc_z','roll', 'pitch', 'yaw','event'])
    data_datetime = dataframe.copy()
    data_datetime['#timestamp']=data_datetime['#timestamp'] / 1e3
    data_datetime['#timestamp']=data_datetime['#timestamp'].apply(lambda x: pd.datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S.%f'))
    data_list.append(data_datetime)
  labelfilenames = glob.glob(file_paths+"*.txt",recursive = True)
  list_of_labeldfs = [pd.read_csv(filename, sep=";") for filename in labelfilenames]
  label_list = []
  for dataframe, filename in zip(list_of_labeldfs, labelfilenames):
      data_label=dataframe[['Time', 'anchor:status','trl', 'nosezone.touches', 'mouthzone.touches', 'eyezone.right eye', 'eyezone.left eye']].copy()
      data_label.columns = ['timeAfterStart','anchor', 'isTouch', 'nose', 'mouth', 'rightEye', 'leftEye']
      label_list.append(data_label)
  return data_list, label_list

#def labeling(data_df,label_df):


