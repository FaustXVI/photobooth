from enum import Enum


class Actions(Enum):
    TAKE_PICTURES = 1
    QUIT = 2


class Photobooth:
    def __init__(self, screen, camera, button):
        self.screen = screen
        self.camera = camera
        self.button = button

    def take_pictures(self, number_of_pictures):
        for i in range(1, 1 + number_of_pictures):
            picture = self.camera.capture_picture(count_down_photo=str(i) + '/' + str(number_of_pictures),
                                                  image_number=i)
            self.screen.show_picture(picture, 2)

    def start(self):
        action = Actions.TAKE_PICTURES
        while action != Actions.QUIT:
            self.screen.show_image('images/start_camera.jpg')
            action = self.button.wait_for_event()
            if action == Actions.TAKE_PICTURES:
                self.take_pictures(3)
