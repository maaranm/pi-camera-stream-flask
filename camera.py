import cv2
import imutils
import time
import numpy as np

class VideoCamera(object):
    def __init__(self):
        self.vs = cv2.VideoCapture(0)
        time.sleep(2.0)

    def __del__(self):
        self.vs.stop()

    def release(self):
    	self.vs.release()

    def start(self):
    	self.vs = cv2.VideoCapture(0)

    def get_frame(self):
        _, frame = self.vs.read()
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
