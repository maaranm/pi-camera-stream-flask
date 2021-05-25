from flask import Flask, render_template, Response, request, jsonify
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
    while True:
        if camera_streaming:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(webcam),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/modify_feed', methods=['POST'])
def modify_feed():
    if not request.json:
        print('fuck')
    new_state = request.args.get('isStreaming')
    if (not camera_streaming) and new_state:
        webcam.start()
    elif camera_streaming and (not new_state):
        webcam.release()
    camera_streaming = new_state
    response = jsonify(success=True)
    return response
    

if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=False)


