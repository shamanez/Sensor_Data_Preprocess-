
# coding: utf-8

# In[1]:


import os
import pandas as pd
import matplotlib.pyplot as plt
import cmath


# In[2]:


data_output = '../waveSense_data_gen_app/output'
data_lepOut = '../waveSense_data_gen_app/leapOut'
pict_folder = 'images'

if not os.path.isdir(pict_folder):
    os.mkdir(pict_folder)
    


# In[3]:


csv_files = []
for f in os.listdir(data_output):
    if(os.path.splitext(f)[1].lower()=='.csv'):
        csv_files.append(f)


# In[6]:

x_count =0
sensor_data = []
gt = []
for f in csv_files:
    #print f
    df = pd.read_csv(os.path.join(data_output,f))
    plt.close("all")
    sensor_df =df.iloc[1:,1:10]
    gt_df = df.iloc[1:,12:15]
    #print "sensor df\n",sensor_df
    sensor_val = []
    gt_val = []
    
    for i in xrange(0,9):
        sensor_val.append(list(sensor_df.iloc[:,i]))

    for i in xrange(3):
        gt_val.append(list(gt_df.iloc[:,i]))

    if(len(sensor_data)== 0):
        sensor_data.extend(sensor_val)
        gt.extend(gt_val)

    else:
        for i in xrange(0,9):
            sensor_data[i].extend(sensor_val[i])
        for i in xrange(3):
            gt[i].extend(gt_val[i])

    #for i in range(9):
    #    print sensor_data[i]


    x_count +=len(sensor_val[0])
    #print(x)
    
    #f1, axarr1 = plt.subplots(2, 1)
    #mng1 = plt.get_current_fig_manager()
    
    #for j in range(9):
    #    print sensor_val[j]
    #    plt.plot(x,sensor_val[j],label=str(j))
    #plt.plot(x,sensor_val[0],label='1') 
    #plt.set_title("sensor values")
    
    #mng1.full_screen_toggle()
    #mng1.resize(*mng1.window.maxsize())
    #plt.legend()
    #plt.show()
    #print sensor_val
x = list(range(x_count))
#print len(sensor_data),
#for i in range(9):
#    print len(sensor_data[i]),
#print len(x)
#print len(gt[0])

f1, axarr1 = plt.subplots(4, 1)
mng1 = plt.get_current_fig_manager()
mng1.full_screen_toggle()
for i in xrange(3):
    for j in xrange(len(gt[i])):
        if(gt[i][j]<=-1000):
            gt[i][j] = -200
        elif(gt[i][j]>= 1000):
            gt[i][j] = 200

    print gt[i]

for i in xrange(3):
    if(i==0):
        lbl = 'x'
    elif(i==1):
        lbl = 'y'
    else:
        lbl = 'z'

    axarr1[0].plot(x,gt[i],label=lbl)



for j in xrange(9):
        #print sensor_val[j]
        if(j/3 == 0):
            axarr1[1].plot(x,sensor_data[j],label=str(j))
        elif(j/3==1):
            axarr1[2].plot(x,sensor_data[j],label=str(j))
        else:
            axarr1[3].plot(x,sensor_data[j],label=str(j))

axarr1[0].legend()
axarr1[1].legend()
axarr1[2].legend()
axarr1[3].legend()
plt.show()
