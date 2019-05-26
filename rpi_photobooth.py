import pygame

from button import Button
from camera import Camera
from photobooth import Photobooth
from screen import Screen


def main():
    with Screen() as screen:
        with Button(22) as button:
            with Camera(screen) as camera:
                Photobooth(screen, camera, button).start()


if __name__ == '__main__':
    main()
