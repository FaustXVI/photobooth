import time

import os

from button import Button
from camera import Camera
from my_random import MyRandom
from photobooth import Photobooth
from screen import Screen

IMAGE_FOLDER = 'Photos'

def main():
    with Screen() as screen:
        with Button(22) as button:
            screen.update_display(message='Folder Check...', size=100)
            os.makedirs(IMAGE_FOLDER, exist_ok=True)
            with Camera(IMAGE_FOLDER) as camera:
                Photobooth(screen, camera, button, time.sleep, MyRandom()).start()


if __name__ == '__main__':
    main()
