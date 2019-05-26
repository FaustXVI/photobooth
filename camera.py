import picamera
import pygame
import time
import os

from screen import Screen

HD_RESOLUTION = (1920, 1080)

PHOTO_FOLDER = 'Photos'
IMAGE_FOLDER = os.path.join(PHOTO_FOLDER, 'images')
IMAGE_WIDTH = 550
IMAGE_HEIGHT = 360


class Camera:
    def __init__(self, screen: Screen):
        screen.update_display(message='Folder Check...')
        os.makedirs(IMAGE_FOLDER, exist_ok=True)
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

    def capture_picture(self, count_down_photo: str, image_number: int):
        self.screen.update_display(message=count_down_photo, size=500)
        time.sleep(1)
        self.screen.update_display()
        self.screen.reset()
        pygame.display.flip()
        self.camera.start_preview()

        for x in range(3, -1, -1):
            if x == 0:
                self.screen.update_display(message="PRENEZ LA POSE", background_color="black")
            else:
                self.screen.update_display(message=str(x), background_color="black", size=800)
            time.sleep(1)

        self.screen.update_display()
        ts = time.time()
        filename = os.path.join(IMAGE_FOLDER, str(image_number) + "_" + str(ts) + '.jpg')
        self.camera.capture(filename)
        self.camera.stop_preview()
        self.screen.show_picture(filename, 2)
        return filename

    def take_pictures(self):
        number_of_pictures = 3
        for i in range(1, 1 + number_of_pictures):
            self.capture_picture(count_down_photo=str(i) + '/' + str(number_of_pictures), image_number=i)
