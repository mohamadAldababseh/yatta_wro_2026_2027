from threading import Thread
import cv2
import imutils

class WebcamVideoStream:
    def __init__(self, src=0):
        imgsz = (1920, 1080)
        self.stream = cv2.VideoCapture(src)
        if type(imgsz) is tuple:
            self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, imgsz[0])
            self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, imgsz[1])
        self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
        self.stream.set(cv2.CAP_PROP_FPS, 120)
        (self.grabbed, self.frame) = self.stream.read()
        self.frame2 = self.frame
        self.stopped = False

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return
            (self.grabbed, self.frame) = self.stream.read()
            self.frame2 = imutils.resize(self.frame, width=800)

    def read(self):
        return self.frame2

    def stop(self):
        self.stopped = True
