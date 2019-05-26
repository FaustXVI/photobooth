from enum import Enum

class Actions(Enum):
    TAKE_PICTURES = 1
    QUIT = 2


class Photobooth:
    def __init__(self, screen, camera, button):
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
