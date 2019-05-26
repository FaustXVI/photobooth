import picamera
import time
import os

HD_RESOLUTION = (1920, 1080)

IMAGE_WIDTH = 550
IMAGE_HEIGHT = 360


class Camera:
    def __init__(self, pictures_folder):
        self.pictures_folder = pictures_folder
        self.camera = picamera.PiCamera(resolution=HD_RESOLUTION,
                                        framerate=30,
                                        sensor_mode=5)
        self.camera.rotation = 0
        self.camera.hflip = True
        self.camera.vflip = False
        self.camera.brightness = 50
        self.camera.preview_alpha = 120
        self.camera.preview_fullscreen = True

    def __enter__(self):
        self.camera.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.camera.__exit__(exc_type, exc_val, exc_tb)

    def take_picture(self, image_number: int):
        ts = time.time()
        filename = os.path.join(self.pictures_folder, str(image_number) + "_" + str(ts) + '.jpg')
        self.camera.capture(filename)
        return filename

    def with_preview(self, i, f):
        self.camera.start_preview()
        result = f(i)
        self.camera.stop_preview()
        return result
