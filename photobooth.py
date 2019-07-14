import locale
from enum import Enum


class Actions(Enum):
    TAKE_PICTURES = 1
    SELF_DESTRUCT = 2
    QUIT = 3


class Photobooth:
    def __init__(self, screen, camera, actionables, sleep, normal_mode, traps, self_destruct, random):
        locale.setlocale(locale.LC_ALL, "fr_FR.utf8")
        self.random = random
        self.sleep = sleep
        self.screen = screen
        self.camera = camera
        self.actionables = actionables
        self.self_destruct = self_destruct
        self.traps = traps
        self.normal_mode = normal_mode

    def run_shoot_scenario(self, image_number: int):
        if self.random.is_normal():
            return self.camera.with_preview(image_number, self.normal_mode)
        else:
            return self.camera.with_preview(image_number, self.random.choice(self.traps))

    def take_picture(self, image_number: int, number_of_pictures: int):
        self.screen.update_display(message=str(image_number) + '/' + str(number_of_pictures), size=500)
        self.sleep(1)
        pictures = self.run_shoot_scenario(image_number)
        for picture in pictures:
            self.screen.show_picture(picture)
            self.sleep(3)
        return pictures

    def take_pictures(self, number_of_pictures: int):
        return [self.take_picture(i, number_of_pictures) for i in range(1, 1 + number_of_pictures)]

    def destruct(self):
        pictures = self.self_destruct.run()
        for picture in pictures:
            self.screen.show_picture(picture)
            self.sleep(3)
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
