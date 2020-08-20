#!/usr/bin/env python
# coding: utf-8

# # Data Pre-Processing

# ### Authors

# Sebastian Ebi, 2068091 
# Huidi Zhu, 1984436
# Calvin Antonius Tanama, 1813569
# Johan Krause, 1959166
# 

# ### Imports

# In[1]:


import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np
import math
import plotly.express as px


# ## Method Definitions

# In[2]:


def load_data_sets(data_path, label_path):
    
    # load data recordings from csv
    data_raw = pd.read_csv(data_path,sep=",", header=0)
    data_raw = data_raw.drop(['acc_x','acc_y','acc_z','roll', 'pitch', 'yaw','event'], axis=1)
    data_datetime = data_raw.copy()
    for row in range(0, len(data_datetime)):
        data_datetime.iloc[row, 0] = datetime.datetime.fromtimestamp(data_datetime.iloc[row, 0] / 1e3).strftime('%Y-%m-%d %H:%M:%S.%f')
    
    # load labels from csv
    data_labels = pd.read_csv(label_path, sep=";", header=0)
    reduced_data_labels = data_labels[['Time', 'trl', 'nosezone.touches', 'mouthzone.touches', 'eyezone.right eye', 'eyezone.left eye']].copy()
    reduced_data_labels.columns = ['timeAfterStart', 'isTouch', 'nose', 'mouth', 'rightEye', 'leftEye']
    return data_raw, data_datetime, reduced_data_labels


# In[3]:


#plot data of recordings
def plot_data_recordings(data, start, end):
    plt.figure(figsize=(20,10))
    for index in range(1,5):
        plt.plot(data.iloc[start:end, index], label=data.columns.values[index])
    plt.xlabel("time")
    plt.ylabel("EOG measurement")
    plt.legend()
    plt.savefig("data_recordings.png")
    plt.show()


# In[4]:


#get timestamp of recordings for each row
def get_timestamp_from_recording(data, row):
    return data.iloc[row, 0]


# In[5]:


#method to get one column with all labels. Labels: '1' = nose, '2' = mouth, '3' = right eye, '4' = left eye
def obtain_final_labels(reduced_data_label):
    labels = []
    record_start_index = math.inf
    
    for index in range(len(reduced_data_label)):


        if reduced_data_label.iloc[index, 1] == 1:
            if index < record_start_index:
                record_start_index = index

            touch_zone = np.argmax(reduced_data_label.iloc[index, 2:6]) + 2
            #touch_zone = np.argwhere(reduced_data_label.columns.values == touch_zone)[0][0]
        
            zone = reduced_data_label.columns[touch_zone]

            if zone == 'nose':
                label = 1
            elif zone == 'mouth':
                label = 2
            elif zone == 'rightEye':
                label = 3
            elif zone == 'leftEye':
                label = 4
            labels.append(label)

        else:
            if index > record_start_index:
                label = 0

                labels.append(label)

    reduced_data_label = reduced_data_label.drop(range(record_start_index), axis = 0)
    reduced_data_label = reduced_data_label.reset_index(drop=True)
    reduced_data_label['label'] = labels
    
    return reduced_data_label


# In[6]:


#method to method to recalculate time stamps in label data
def generated_timestamps_in_label_data(reduced_data_label, timestamp):
    reduced_data_label['timestamp'] = np.zeros(len(reduced_data_label), dtype=np.longlong)
    reduced_data_label.iloc[0,-1] = timestamp 
    for index in range(1, len(reduced_data_label)):
        reduced_data_label.iloc[index, -1] = reduced_data_label.iloc[0, -1] + (reduced_data_label.iloc[index, 0] - reduced_data_label.iloc[0,0]) * 1000
    return reduced_data_label


# In[7]:


#method to merge recording data with labels
def join_recordings_with_labels(data_raw, reduced_data_label):
    index_data=0
    #add ZeroColumn to the recording dataframe 
    data_raw['label'] = np.zeros(len(data_raw), dtype=np.int)

    for index_label in range(0, len(reduced_data_label) - 1):
        timestamp_label = reduced_data_label.iloc[index_label,-1]
        while index_data < len(data_raw):
            timestamp_data = data_raw.iloc[index_data,0]
            #compare data timestamp with label timestamp
            if timestamp_data < timestamp_label:
                index_data += 1
            elif timestamp_data >= timestamp_label:
                if timestamp_data < reduced_data_label.iloc[index_label + 1,-1]:
                    #add label of label data to the recordings data
                    data_raw.iloc[index_data, -1] = reduced_data_label.iloc[index_label, -2]
                    index_data += 1
                else:
                    break
    return data_raw


# In[8]:


def export_to_csv(dataset, path):
    dataset.to_csv(path, index = False, header=True, sep=';')
    return 'exported successfully'


# ## Apply Preprocessing

# In[9]:


raw, data_tmps, label_data = load_data_sets('2020-07-08_15-39-18.csv', '2020-07-08-15_37_09_Andrea_annotated.csv')


# In[10]:


raw.shape


# In[11]:


label_data.shape


# In[12]:


plot_data_recordings(data_tmps, 0,len(data_tmps))


# In[13]:


timestamp = get_timestamp_from_recording(raw, 1012)
timestamp


# In[14]:


label_data = obtain_final_labels(label_data)
label_data = generated_timestamps_in_label_data(label_data, timestamp)
data_with_labels = join_recordings_with_labels(raw, label_data)
data_with_labels


# In[30]:



df = data_with_labels

# Use directly Columns as argument. You can use tab completion for this!
fig = px.scatter(df, x=data_tmps['#timestamp'], y=df['left2'], color=df['label'])
fig.show()


# In[16]:


export_to_csv(data_with_labels, 'preprocessed_data_a_05.csv')


# # Cutting of Synchronization Gestures

# ## Imports

# In[17]:


import pandas as pd
import datetime
#import matplotlib.pyplot as plt
import numpy as np
#import math
#import plotly.express as px


# ## Method Definitions

# In[18]:


def read_data_sets(data_path):
    
    # load data recordings from csv
    data_raw = pd.read_csv(data_path,sep=";", header=0)
    return data_raw


# In[19]:


#method to find index for cutting of synchronization gesture (3 time nosetab)
def cut_anchor(data):
    nose_start_1 = False
    nose_end_1= False
    nose_start_2 = False
    nose_end_2= False
    nose_start_3 = False
    nose_end_3= False

    index = 0
    cut_index = 0
    while index <= len(data):
        label = data.iloc[index, -1]

        if nose_start_1 == False:
            if label == 1:
                nose_start_1 = True
        elif nose_start_1 == True and nose_end_1 == False:
            if label == 0:
                nose_end_1 = True
        elif nose_start_1 == True and nose_end_1 == True and nose_start_2 == False:
            if label == 1:
                nose_start_2 = True
        elif nose_start_1 == True and nose_end_1 == True and nose_start_2 == True and nose_end_2 == False:
            if label == 0:
                nose_end_2 = True
        elif nose_start_1 == True and nose_end_1 == True and nose_start_2 == True and nose_end_2 == True and nose_start_3 == False:   
            if label == 1:
                nose_start_3 = True
        elif nose_start_1 == True and nose_end_1 == True and nose_start_2 == True and nose_end_2 == True and nose_start_3 == True and nose_end_3 == False:
            if label == 0:
                nose_end_3 = True
        elif nose_start_1 == True and nose_end_1 == True and nose_start_2 == True and nose_end_2 == True and nose_start_3 == True and nose_end_3 == True:
            cut_index = index + 25
            break;
        index += 1
    return cut_index


# In[20]:


### Binarize Labels if necessary
def binarize_labels (data_raw):
    data_raw_reduced_bin = data_raw
    for index in range (0, len(data_raw_reduced)):
        if data_raw_reduced_bin.iloc[index, -1] != 0:
            data_raw_reduced_bin.iloc[index, -1] = 1
    return data_raw_reduced_bin


# In[21]:


def export_to_csv(dataset, path):
    dataset.to_csv(path, index = False, header=True, sep=';')
    return 'exported successfully'


# ## Apply Cutting of Synchronization Gestures

# In[22]:


data_raw = read_data_sets('preprocessed_data_a_05.csv')


# In[23]:


cut_index_front  = cut_anchor(data_raw)


# In[24]:


data_raw_reverse = data_raw.iloc[::-1].reset_index(drop=True)


# In[25]:


cut_index_back = cut_anchor(data_raw_reverse)


# In[26]:


data_raw_reduced = data_raw[cut_index_front:-cut_index_back]


# In[27]:


export_to_csv(data_raw_reduced, 'preprocessed_cut_05.csv')


# In[28]:


### Binarize Labels if necessary
def binarize_labels (data_raw)
    data_raw_reduced_bin = data_raw
    for index in range (0, len(data_raw_reduced)):
        if data_raw_reduced_bin.iloc[index, -1] != 0:
        data_raw_reduced_bin.iloc[index, -1] = 1
    return data_raw_reduced_bin


# In[ ]:


export_to_csv(data_raw_reduced_bin, 'preprocessed_cut_bin_05.csv')

