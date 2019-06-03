import time

import os

from actionables import Actionables
from button import Button
from camera import Camera
from keyboard import Keyboard
from my_random import MyRandom
from photobooth import Photobooth, Actions
from screen import Screen
from speakers import Speaker

IMAGE_FOLDER = 'Photos'


def main():
    with Screen() as screen:
        with Button(12, Actions.TAKE_PICTURES) as picture_button:
            with Button(11, Actions.SELF_DESTRUCT) as destruction_button:
                screen.update_display(message='Folder Check...', size=100)
                os.makedirs(IMAGE_FOLDER, exist_ok=True)
                speakers = Speaker()
                with Camera(IMAGE_FOLDER) as camera:
                    actionables = Actionables([picture_button, destruction_button, Keyboard()])
                    Photobooth(screen, camera, actionables, time.sleep, speakers, MyRandom()).start()


if __name__ == '__main__':
    main()
