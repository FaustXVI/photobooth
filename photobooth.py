import locale
from enum import Enum


class Actions(Enum):
    TAKE_PICTURES = 1
    SELF_DESTRUCT = 2
    QUIT = 3


class Photobooth:
    def __init__(self, screen, actionables, normal_mode, traps, self_destruct, random):
        locale.setlocale(locale.LC_ALL, "fr_FR.utf8")
        self.random = random
        self.screen = screen
        self.actionables = actionables
        self.self_destruct = self_destruct
        self.traps = traps
        self.normal_mode = normal_mode

    def run_shoot_scenario(self, image_number: int):
        if self.random.is_normal():
            return self.normal_mode.run(image_number)
        else:
            return self.random.choice(self.traps).run(image_number)

    def take_picture(self, image_number: int, number_of_pictures: int):
        self.screen.update_display(message=str(image_number) + '/' + str(number_of_pictures), size=500)
        pictures = self.run_shoot_scenario(image_number)
        self.show_pictures(pictures)
        return pictures

    def show_pictures(self,pictures):
        for picture in pictures:
            self.screen.show_picture(picture)

    def take_pictures(self, number_of_pictures: int):
        return [self.take_picture(i, number_of_pictures) for i in range(1, 1 + number_of_pictures)]

    def destruct(self):
        pictures = self.self_destruct.run()
        self.show_pictures(pictures)
        return pictures

    def start(self):
        action = Actions.TAKE_PICTURES
        while action != Actions.QUIT:
            self.screen.show_image('images/start_camera.jpg')
            action = self.actionables.wait_for_event()
            if action == Actions.TAKE_PICTURES:
                self.take_pictures(3)
            if action == Actions.SELF_DESTRUCT:
                self.destruct()
