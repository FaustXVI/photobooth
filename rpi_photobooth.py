import time

import os

from actionables import Actionables
from button import Button
from camera import Camera
from double_trap import DoubleTrap
from horn_trap import HornTrap
from no_trap import NoTrap
from relay import Relay
from keyboard import Keyboard
from my_random import MyRandom
from photobooth import Photobooth, Actions
from screen import Screen
from self_destruction import SelfDestruction
from slow_trap import SlowTrap
from speakers import Speaker
from speed_trap import SpeedTrap

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
        self_destruction = SelfDestruction(screen, camera, time.sleep, speakers, ioniser, fan)
        normal_mode = NoTrap(screen, camera, time.sleep)
        traps = [
            SlowTrap(screen, camera, time.sleep),
            SpeedTrap(screen, camera, time.sleep),
            DoubleTrap(screen, camera, time.sleep),
            HornTrap(screen, camera, time.sleep, speakers)
        ]
        Photobooth(screen, camera, actionables, time.sleep, normal_mode, traps, self_destruction, MyRandom()).start()


if __name__ == '__main__':
    main()
