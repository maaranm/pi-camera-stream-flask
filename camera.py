import cv2
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
import numpy as np

class VideoCamera(object):
    def __init__(self, type):
        self.cam_type = type
        if self.cam_type == 'pi':
            self.vs = PiVideoStream().start()
        else:
            self.vs = cv2.VideoCapture(0)
        time.sleep(2.0)

    def __del__(self):
        if self.cam_type == 'pi':
            self.vs.stop()
        else:
            self.vs.release()

    def release(self):
    	if self.cam_type == 'pi':
    		self.vs.stop()
    	else:
    		self.vs.release()

    def start(self):
        if self.cam_type == 'pi':
            self.vs = PiVideoStream().start()
        else:
    	    self.vs = cv2.VideoCapture(0)

    def get_frame(self):
        if self.cam_type == 'pi':
            frame = self.vs.read()
        else:
            _, frame = self.vs.read()
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
