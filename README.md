# Sensor_Data_Preprocess-
This is about how to write sensor readings in to  a csv in desired manner. The waveSence_data_gen_app folder contains the python script to record examples with the ground truth geneated by LeapMotion along with leapMotion API.

## 1. Instruction for Running app
**note:** *Insturctions were given for properly setuped LeapMotion SDK V2. For setting ud SDK see the instruction below*
go to the directory waveSence_data_gen_app

**1.1 check the serial connection is working properly**
if the connection is working correctly running *(given in sect 1.3)*
will give terminal message like,
```
  opening Serial port
  opened
  Initialized
  Press Enter to quit...
```
if any serial Execption like,
```
raise SerialException(msg.errno, "could not open port %s: %s" % (self._port, msg))
serial.serialutil.SerialException: [Errno 2] could not open port /dev/ttyUSB#: [Errno 2] No such file or directory: '/dev/ttyUSB#'
```
occured, check the connection with an external serial monitor with baud rate:115200.
if it's working well check the **lineNumber:193**
```serial.Serial('/dev/ttyUSB0',115200,timeout=1)``` is correctly stating the usb serial device.

**1.2 Checking Leapmotion connected and socket is working**
for using leapmotion SDK.V2 in *Ubuntu* after connecting the device manualy run ```sudo LeapControlPanel``` for the LeapMotion Control panel.

>if a popup says,
>*Leap Daemon is not Running you've to start mannualy*
Run ```sudo leapd``` 

When the Leap Daemon is properly working, By clicking the option: **Diognistic Visualizer** in the **Troubleshooting** tab of the **Leap Motion control panel**. This visualizer shows the data from the leapmotion device.

**1.3 Running the script**
run the script simply by,
``` sudo  LD_PRELOAD=./libLeap.so python2.7 WaveSence.py ```
**note:** The version of the *libLeap.so* SDK is from the version (2.3.1+31549). Incase of different version use relevent SDK files for ***Leap.py, Leap.pyc, LeapPython.so, libLeap.so***


