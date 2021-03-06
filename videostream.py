from camerastream import CameraStream


class VideoStream:
    def __init__(self, usePiCamera, width, height, camPort):
        if usePiCamera:
            from picamerastream import PiCameraStream
            self.stream = PiCameraStream(width, height, framerate=30)
        else:
            self.stream = CameraStream(width, height, camPort)
    def start(self):
        return self.stream.start()

    def update(self):
        self.stream.update()
    def getFrame(self):
        return self.stream.getFrame()
    def stop(self):
        self.stream.stop()
