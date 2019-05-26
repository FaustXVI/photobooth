import time

import os
import random

from button import Button
from camera import Camera
from photobooth import Photobooth
from screen import Screen

IMAGE_FOLDER = 'Photos'


class MyRandom:
    def __init__(self):
        self.random = random

    def choice(self, array):
        return self.choice(array)

    def is_normal(self):
        return self.random.randint(1, 10) != 1


def main():
    with Screen() as screen:
        with Button(22) as button:
            screen.update_display(message='Folder Check...')
            os.makedirs(IMAGE_FOLDER, exist_ok=True)
            with Camera(IMAGE_FOLDER) as camera:
                Photobooth(screen, camera, button, time.sleep, MyRandom()).start()


if __name__ == '__main__':
    main()
