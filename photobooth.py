from enum import Enum
import pygame

from button import Button
from camera import Camera
from screen import Screen


class Actions(Enum):
    TAKE_PICTURES = 1
    QUIT = 2


class Photobooth:
    def __init__(self, screen: Screen, camera: Camera, button: Button):
        self.screen = screen
        self.camera = camera
        self.button = button

    def start(self):
        action = Actions.TAKE_PICTURES
        while action != Actions.QUIT:
            self.screen.show_image('images/start_camera.jpg')
            action = self.button.wait_for_event()
            if action == Actions.TAKE_PICTURES:
                self.camera.take_pictures()


def main():
    screen = Screen()
    with Button(22) as button:
        with Camera(screen) as camera:
            Photobooth(screen, camera, button).start()
            pygame.quit()


if __name__ == '__main__':
    main()
