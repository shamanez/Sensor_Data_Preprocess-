# Sensor_Data_Preprocess-
This is about how to write sensor readings in to  a csv in desired manner. The waveSence_data_gen_app folder contains the python script to record examples with the ground truth geneated by LeapMotion along with leapMotion API.

## 1. Instruction for Running app
**note:** *Insturctions were given for properly setuped LeapMotion SDK V2. For setting ud SDK see the instruction below in Sect. 2.*
go to the directory waveSence_data_gen_app

### **1.1 check the serial connection is working properly**

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

### **1.2 Checking Leapmotion connected and socket is working**

for using leapmotion SDK.V2 in *Ubuntu* after connecting the device manualy run ```sudo LeapControlPanel``` for the LeapMotion Control panel.

>if a popup says,
>*Leap Daemon is not Running you've to start mannualy*
Run ```sudo leapd``` 

When the Leap Daemon is properly working, By clicking the option: **Diognistic Visualizer** in the **Troubleshooting** tab of the **Leap Motion control panel**. This visualizer shows the data from the leapmotion device.

### **1.3 Running the script**

run the script simply by,
``` sudo  LD_PRELOAD=./libLeap.so python2.7 WaveSence.py ```

**note:** The version of the *libLeap.so* SDK is from the version (2.3.1+31549). In case of different version use relevent SDK files for ***Leap.py, Leap.pyc, LeapPython.so, libLeap.so***

## 2.leapMotion SDK 
### 2.1 Installation on Ubuntu
**note:** LeapMotion SDK supports python 2.7. 
1. Download LeapMotion SDK 2.3.1 from ```https://developer.leapmotion.com/sdk/v2/```
2. Extract the with ```tar -xaf LeapDeveloperKit*33747*.tgz```
3. ```cd LeapDeveloperKit*33747*```
4. ```sudo dpkg -i Leap*x64.deb```

### 2.1 using SDK with python 2.7 + testing 
>The Leapmotion SDK 2.3.1-33747 is not properly working on ubuntu. Therefore use the SDK of LeapDeveloperKit 2.3.1-31549 instead if SDK of LeapDeveloperKit 2.3.1-33747.

5. Download LeapDeveloperKit 2.3.1-31549 form ```https://developer-archive.leapmotion.com/downloads/external/skeletal-beta/linux?version=2.3.1.31549```
6. ```tar -xaf LeapDeveloperKit*31549*.tgz```
7. ```cd LeapDeveloperKit*31549*/LeapSDK```
8. ```sudo apt-get install swig g++ libpython2.7-dev```
9. ```cp include/Leap.i include/LeapNEW.i``` and Edit ```include/LeapNEW.i``` and replace every ```%}}``` by ```}}```
10. ```swig -c++ -python -o /tmp/LeapPython.cpp -interface LeapPython include/LeapNEW.i```

**testing the SDK**

11. ```mkdir python2.7_project```
12. ```cp -a lib/x64/libLeap.so lib/Leap.py samples/Sample.py python2.7_project/```
13. ```g++ -fPIC -I/usr/include/python2.7 -I./include /tmp/LeapPython.cpp lib/x64/libLeap.so -shared -o python2.7_project/LeapPython.so```
14. ```cd python2.7_project/```
15. ```LD_PRELOAD=./libLeap.so python2.7 Sample.py```

### 2.2 using SDK with python 3.5 + testing 
steps 5-10 are same as for python 2.7

11. ```sudo apt-get install libpython3.5-dev```
12. ```mkdir python3.5_project```
13. ```cp -a lib/x64/libLeap.so lib/Leap.py samples/Sample.py python3.5_project/```
14. ```2to3-3.5 -nw python3.5_project/Sample.py```
15.  ```g++ -fPIC -I/usr/include/python3.5m -I./include /tmp/LeapPython.cpp lib/x64/libLeap.so -shared -o python3.5_project/LeapPython.so```
16. ```cd python3.5_project/```
17. ```LD_PRELOAD=./libLeap.so python3.5 Sample.py```
