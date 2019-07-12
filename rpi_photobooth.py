import time

import os

from actionables import Actionables
from button import Button
from camera import Camera
from relay import Relay
from keyboard import Keyboard
from my_random import MyRandom
from photobooth import Photobooth, Actions
from screen import Screen
from speakers import Speaker

IMAGE_FOLDER = 'Photos'


def main():
    with Screen() as screen, \
            Button(12, Actions.TAKE_PICTURES) as picture_button, \
            Button(11, Actions.SELF_DESTRUCT) as destruction_button, \
            Relay(13) as ioniser, \
            Relay(15) as fan, \
            Relay(7) as flash, \
            Camera(IMAGE_FOLDER, flash) as camera:
        screen.update_display(message='Folder Check...', size=100)
        os.makedirs(IMAGE_FOLDER, exist_ok=True)
        speakers = Speaker()
        actionables = Actionables([picture_button, destruction_button, Keyboard()])
        Photobooth(screen, camera, actionables, time.sleep, speakers, ioniser, fan, MyRandom()).start()


if __name__ == '__main__':
    main()
