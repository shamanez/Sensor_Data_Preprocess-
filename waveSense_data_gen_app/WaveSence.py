import Leap
import sys
import time
import thread
import os
import pandas as pd
import numpy as np
import serial

TIME_TOLERANCE = 50000 #in us

path = os.path.dirname(os.path.realpath(__file__))

if(not os.path.isdir(os.path.join(path,'output'))):
        os.mkdir(os.path.join(path,'output'))

outDir =  os.path.join(path,'output')


def captureGest(frame1,listener):
    leap_frame1,curr_time1 = retreveLeapFrame(listener)
    valid = False
    frames_checking = []
    
    for i in range(3):
        line = ser.readline()
        values = [int(elem) for elem in line.split()]
        leap_frame, curr_time = retreveLeapFrame(listener)
        frames_checking.append([values,leap_frame,curr_time])
        Total = sum(values[:-1])
        if(Total != 9000):
            valid =True
    frames=[]
    frames.append([frame1,leap_frame1,curr_time1])
    frames.extend(frames_checking)

    isExit = False
    while(not isExit):
        line = ser.readline()
        values = [int(elem) for elem in line.split()]
        leap_frame,curr_time = retreveLeapFrame(listener)
        Total = sum(values[:-1])
        if(Total != 9000):
            frames.append([values,leap_frame,curr_time])
        elif(Total == 9000):
            frames_exiting=[]
            frames_exiting.append([values,leap_frame,curr_time])
            isExit = True
            for i in range(3):
                line = ser.readline()
                values = [int(elem) for elem in line.split()]
                leap_frame,curr_time = retreveLeapFrame(listener)
                frames_exiting.append([values,leap_frame,curr_time])
                Total = sum(values[:-1])
                if(Total != 9000):
                    isExit = False
            if(not isExit):
                frames.extend(frames_exiting)
    return frames
##    df = pd.DataFrame(frames)
##    df.columns = ['s1','s2','s3','s4','s5','s6','s7','s8','s9','frameID']
##    print(df)
##    ts =str(time.time())
##    name = ts[:-3]+ts[-2:]+'.csv'
##    print(name)
##    df.to_csv(os.path.join(outDir,name))

def retreveLeapFrame(listener):
    leap_frame = listener.curr_frame
    curr_time = int(time.time()*100000)
    if (len(leap_frame.hands) > 0 and abs(curr_time - leap_frame.timestamp)<TIME_TOLERANCE):
            return leap_frame
    else:
        while(abs(curr_time - leap_frame.timestamp)<TIME_TOLERANCE):
            leap_frame = listener.curr_frame
            if (len(leap_frame.hands)>0):
                return leap_frame

    return ((leap_frame,curr_time))
                
        
    
    print "curr time: %f, leap_frame timestamp: %f" % (curr_time*100000, leap_frame.timestamp)
    
class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    one_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
    
    def on_init(self,Controller):
        print "Initialized"
        self.curr_frame = None
        self.write_file = False
        self.counter = 0
        if(not os.path.isdir(os.path.join(path,'leapOut'))):
                os.mkdir(os.path.join(path,'leapOut'))
        self.leapOut = os.path.join(path,'leapOut')
        self.currWrFile = None
        self.hand_frames = []

    def on_connect(self,controller):
        #Enable Head Mount
        controller.set_policy(Leap.Controller.POLICY_OPTIMIZE_HMD);

    def on_disconnect(self,ontroller):
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def write_csv(self, frame):
        if(self.counter == 0):
                ts =str(int(time.time()*1000))
                self.currWrFile = ts+'.csv'
        if(self.counter == 56536):
                self.counter = 0

        self.hand_frames = []
        for hand in frame.hands:
##                print type(hand.palm_position)
                vect = hand.palm_position
                self.hand_frames.append([vect.x,vect.y,vect.z,hand.is_left,frame.timestamp])

        if(len(self.hand_frames) != 0):
                self.counter+=1
                df = pd.DataFrame(self.hand_frames)
                with open(os.path.join(self.leapOut,self.currWrFile),'a') as f:
                        df.to_csv(f,header=False)
                
    def on_frame(self, controller):
        frame = controller.frame()
        self.curr_frame = frame
        self.write_csv(frame)
##        print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
##              frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))


        
    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"
        
def write_frame(frames):
    dataframe_list = []
    
    for elem in frames:
        row = []
        row.extend(elem[0])
        row.append(elem[2])
        if elem[1].hands.is_empty:
                row.extend([-10000,-10000,-10000])
                row.append(0)
        else:
                for hand in elem[1].hands:
                        row.extend([hand.palm_position.x,hand.palm_position.y,hand.palm_position.z])
                        row.append(int(hand.is_left))
        row.append(elem[1].timestamp)
        dataframe_list.append(row)

    df2 = pd.DataFrame(dataframe_list)
    df2.columns = ['s1','s2','s3','s4','s5','s6','s7','s8','s9','frameID','sens_timestamp','x','y','z','isLeft','GT_timestamp']
    ts =str(int(time.time()*1000))
    fileName = ts+'.csv'

    df2.to_csv(os.path.join(outDir,fileName))
        
        
def main():
     # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."

    startListening = False
    while(not startListening):
        
        if(type(listener.curr_frame) != type(None)):
            print listener.curr_frame.id
            startListening = True
    
    try:
        frames = []
        while(True):
            line = ser.readline()
            if(len(line) <40):
                continue
            print "line", line, "lenLine: ", len(line)

            values = [int(elem) for elem in line.split()]
            Total = sum(values[:-1])
            if(Total != 9000):
                frames=captureGest(values,listener)
                write_frame(frames)
                for elem in frames:
                    print elem[0], type(elem[1].hands),
                    if elem[1].hands.is_empty:
                            print "(0,0,0)"
                    else:
                            for hand in elem[1].hands:
                                handType = "Left hand" if hand.is_left else "Right hand"
                                print "  %s, id %d, position: %s" % (
                                    handType, hand.id, hand.palm_position)
        
        
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)

if __name__ == "__main__":
    
    print "working script path: " + path +'\n' 
    try:
        print "opening Serial port"
        with serial.Serial('/dev/ttyUSB0',115200,timeout=1) as ser:
            print "opened"
            main()
            
    except KeyboardInterrupt:
        exit()
