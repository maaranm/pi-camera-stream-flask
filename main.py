from flask import Flask, render_template, Response, request
from camera import VideoCamera
import time
import threading
import os

webcam = VideoCamera()

# App Globals (do not edit)
app = Flask(__name__)

camera_streaming = True

@app.route('/')
def index():
    return render_template('index.html') #you can customze index.html here

def gen(camera):
    #get camera frame
    while camera_streaming:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(webcam),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/modify_feed', methods=['POST'])
def modify_feed():
    if not request.json:
        print('fuck')
    camera_streaming = request.data
    print(camera_streaming)
    

if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=False)


