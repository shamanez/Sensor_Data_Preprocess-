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
    leap_frame1 = retreveLeapFrame(listener)
    valid = False
    frames_checking = []
    
    for i in range(3):
        line = ser.readline()
        values = [int(elem) for elem in line.split()]
        leap_frame = retreveLeapFrame(listener)
        frames_checking.append([values,leap_frame])
        Total = sum(values[:-1])
        if(Total != 9000):
            valid =True
    frames=[]
    frames.append([frame1,leap_frame1])
    frames.extend(frames_checking)

    isExit = False
    while(not isExit):
        line = ser.readline()
        values = [int(elem) for elem in line.split()]
        leap_frame = retreveLeapFrame(listener)
        Total = sum(values[:-1])
        if(Total != 9000):
            frames.append([values,leap_frame])
        elif(Total == 9000):
            frames_exiting=[]
            frames_exiting.append([values,leap_frame])
            isExit = True
            for i in range(3):
                line = ser.readline()
                values = [int(elem) for elem in line.split()]
                leap_frame = retreveLeapFrame(listener)
                frames_exiting.append([values,leap_frame])
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

    return leap_frame
                
        
    
    print "curr time: %f, leap_frame timestamp: %f" % (curr_time*100000, leap_frame.timestamp)
    
class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    one_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self,Controller):
        print "Initialized"
        self.curr_frame = None

    def on_connect(self,controller):
        #Enable Head Mount
        controller.set_policy(Leap.Controller.POLICY_OPTIMIZE_HMD);

    def on_disconnect(self,ontroller):
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        frame = controller.frame()
        self.curr_frame = frame
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

def main():
     # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
##    Exit = False
##    prev_frame_id = -1
##    while(not Exit):
##        frame = listener.curr_frame
##        
##        if(type(frame) == type(None)):
##            print "type is none"
##            continue
##        elif(prev_frame_id != frame.id):
##            prev_frame_id = frame.id
##            if(len(frame.hands) > 0):
##                print "hand detected on frame id", frame.id
    startListening = False
    while(not startListening):
        if(type(listener.curr_frame) != type(None)):
            startListening = True
    
        
##    for i in range(1000000):
##        frame = retreveLeapFrame(listener)
##        print i
##        if(type(frame) != type(False)):
##            print frame.id
        
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
                for elem in frames:
                    print elem[0],
                    if type(elem[1]) == type(True):
                            print "(0,0)"
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
