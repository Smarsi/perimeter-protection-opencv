# perimeter-protection-opencv
Python + OpenCV used as security system to alarm perimeter invasion

# To download the weights file use:

> wget https://pjreddie.com/media/files/yolov3.weights

or access in the browser
https://pjreddie.com/media/files/yolov3.weights


# For windows:

Change the branch to windows:

> git checkout windows


# How to run the project

<b>First of all you need to download the weights file and put into the project's directory (same path as the other yolo files listed here)</b>

### On Linux:

> python3 main.py --video /dev/video0 --config ./yolov3.cfg --classes ./yolov3.txt --weights ./yolov3.weights

Change "/dev/video0" for your camera number

### On Windows:

> py main.py --video 0 --config .\yolov3.cfg --classes .\yolov3.txt --weights .\yolov3.weights

Change "--video 0" for your camera number on windows


### How to use

When program starts you need to draw a protected area on the image using the mouse (just click and drag to draw a rectangle).
Every time a intrusor get shot inside this protected area the system will write "Invasor detectado" on the screen.
