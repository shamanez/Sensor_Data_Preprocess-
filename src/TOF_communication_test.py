import os
import pandas as pd
import numpy as np
import serial
import threading
import time

path = os.path.dirname(os.path.realpath(__file__))

if(not os.path.isdir(os.path.join(path,'output'))):
        os.mkdir(os.path.join(path,'output'))

outDir =  os.path.join(path,'output')

def captureGest(frame1):
    valid = False
    frames_checking = []
    for i in range(3):
        line = ser.readline()
        values = [int(elem) for elem in line.split()]
        frames_checking.append(values)
        Total = sum(values[:-1])
        if(Total != 9000):
            valid =True
    frames=[]
    frames.append(frame1)
    frames.extend(frames_checking)

    isExit = False
    while(not isExit):
        line = ser.readline()
        values = [int(elem) for elem in line.split()]
        
        Total = sum(values[:-1])
        if(Total != 9000):
            frames.append(values)
        elif(Total == 9000):
            frames_exiting=[]
            frames_exiting.append(values)
            isExit = True
            for i in range(3):
                line = ser.readline()
                values = [int(elem) for elem in line.split()]
                frames_exiting.append(values)
                Total = sum(values[:-1])
                if(Total != 9000):
                    isExit = False
            if(not isExit):
                frames.extend(frames_exiting)
    
    df = pd.DataFrame(frames)
    df.columns = ['s1','s2','s3','s4','s5','s6','s7','s8','s9','frameID']
    print(df)
    ts =str(time.time())
    name = ts[:-3]+ts[-2:]+'.csv'
    print(name)
    df.to_csv(os.path.join(outDir,name))
    
def main():
        
        while(True):
            line = ser.readline()
            if(len(line) <10):
                continue
            print line
            values = [int(elem) for elem in line.split()]
            Total = sum(values[:-1])
            if(Total != 9000):
                captureGest(values)
    
if __name__ == "__main__":
       
    
    print "working script path: " + path +'\n' 
    try:
        print "opening Serial port"
        with serial.Serial('/dev/ttyUSB0',115200,timeout=1) as ser:
            print "opened"
            main()
    except KeyboardInterrupt:
        print "interupted/n"
        exit()
