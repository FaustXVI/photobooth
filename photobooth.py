from threading import Thread

from button import Button
from camera import Camera
from screen import Screen


class Photobooth:
    def __init__(self, screen: Screen, camera: Camera, button: Button):
        self.screen = screen
        self.camera = camera
        self.button = button

    def start(self):
        while True:
            self.screen.show_image('images/start_camera.jpg')
            self.button.wait_for_event()
            self.camera.take_pictures()


def main():
    screen = Screen()
    with Button(22) as button:
        with Camera(screen) as camera:
            Photobooth(screen, camera, button).start()


if __name__ == '__main__':
    main()
