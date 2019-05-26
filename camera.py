import picamera
import time
import os

from screen import Screen

HD_RESOLUTION = (1920, 1080)

IMAGE_WIDTH = 550
IMAGE_HEIGHT = 360


class Camera:
    def __init__(self, screen: Screen, pictures_folder):
        self.pictures_folder = pictures_folder
        self.screen = screen
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

    def capture_picture(self, image_number: int):
        self.screen.reset()
        self.camera.start_preview()

        for x in range(3, -1, -1):
            if x == 0:
                self.screen.update_display(message="PRENEZ LA POSE", background_color="black")
            else:
                self.screen.update_display(message=str(x), background_color="black", size=800)
            time.sleep(1)

        self.screen.reset()
        ts = time.time()
        filename = os.path.join(self.pictures_folder, str(image_number) + "_" + str(ts) + '.jpg')
        self.camera.capture(filename)
        self.camera.stop_preview()
        return filename
