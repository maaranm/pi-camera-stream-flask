from flask import Flask, render_template, Response, request, jsonify
import numpy as np
import cv2
from camera import VideoCamera
import time
import threading
import os

app = Flask(__name__)

#global variables to track if currently streaming and current camera type
camera_streaming = 'True'
cam_type = 'pi'
webcam = None
try:
    webcam = VideoCamera(cam_type)
    print('success')
except:
    camera_streaming = 'False'
    print('fail')

blankImg = cv2.imread('placeholder.jpg')
blankFrame = blankImg.tobytes()
#helper function to get camera frame or empty frame depending on streaming state
def gen():
    #get camera frame
    while True:
        if camera_streaming == 'True':
            global webcam
            frame = webca,=m.get_frame()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + blankFrame + b'\r\n\r\n')

            #end point for video feed
@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

#post endpoint for modifying streaming settings
@app.route('/modify_feed', methods=['POST'])
def modify_feed():
    global camera_streaming
    global cam_type
    global webcam
    #current post request parameters
    new_state = request.args.get('isStreaming')
    new_cam = request.args.get('camType')
    
    #change camera type between usb webcam and pi cam
    if (cam_type != new_cam):
        if(webcam != None):
            webcam.release()
        webcam = VideoCamera(new_cam)
    
    #comparing to string literals because python bool cast just converts any non-empty string to true
    if (camera_streaming != 'True') and (new_state == 'True'):
        webcam.start()
    elif (camera_streaming == 'True') and (new_state != 'True'):
        webcam.release()

    #update global variables
    camera_streaming = new_state
    cam_type = new_cam
    #return success resupsonse
    response = jsonify(success=True)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    

if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=False)


