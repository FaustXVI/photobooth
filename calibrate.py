import configparser
import locale
from enum import Enum

from infrastructure.actionables import Actionables
from infrastructure.camera import Camera
from infrastructure.keyboard import Keyboard
from infrastructure.relay import Relay
from infrastructure.screen import Screen
from photobooth import Actions

def main():
    config = configparser.ConfigParser()
    config.read('config')
    gpio = config['gpio']
    with Screen() as screen, \
        Relay(int(gpio['flash'])) as flash, \
        Camera('Photos', flash) as camera:
            actionables = Actionables([Keyboard()])
            camera.start_preview()
            action = Actions.TAKE_PICTURES
            while action != Actions.QUIT:
                action = actionables.wait_for_event()


if __name__ == '__main__':
    main()