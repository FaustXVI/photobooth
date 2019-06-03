import locale
from enum import Enum


class Actions(Enum):
    TAKE_PICTURES = 1
    SELF_DESTRUCT = 2
    QUIT = 3


class Photobooth:
    def __init__(self, screen, camera, actionables, sleep, speakers, random):
        locale.setlocale(locale.LC_ALL, "fr_FR.utf8")
        self.random = random
        self.sleep = sleep
        self.screen = screen
        self.camera = camera
        self.actionables = actionables
        self.speakers = speakers

    def count_down(self, range):
        for x in range:
            self.screen.update_display("{:n}".format(x))
            self.sleep(1)

    def normal(self, image_number):
        self.count_down(range(3, 0, -1))
        return self.camera.take_picture(image_number)

    def fast(self, image_number):
        self.count_down(range(3, 1, -1))
        return self.camera.take_picture(image_number)

    def slow(self, image_number):
        self.count_down([3, 2, 1.5, 1, 0.5, 0.25, 0.1, 0.01])
        return self.camera.take_picture(image_number)

    def run_shoot_scenario(self, image_number: int):
        if self.random.is_normal():
            return self.camera.with_preview(image_number, self.normal)
        else:
            return self.camera.with_preview(image_number, self.random.choice([
                self.fast,
                self.slow,
            ]))

    def take_picture(self, image_number: int, number_of_pictures: int):
        self.screen.update_display(message=str(image_number) + '/' + str(number_of_pictures), size=500)
        self.sleep(1)
        picture = self.run_shoot_scenario(image_number)
        self.screen.show_picture(picture)
        self.sleep(3)
        return picture

    def take_pictures(self, number_of_pictures: int):
        return [self.take_picture(i, number_of_pictures) for i in range(1, 1 + number_of_pictures)]

    def destruct(self):
        self.speakers.play_sound('sound/self-destruct.ogg')
        self.sleep(4)
        picture = self.normal(1)
        self.screen.show_picture(picture)
        self.sleep(3)

    def start(self):
        action = Actions.TAKE_PICTURES
        while action != Actions.QUIT:
            self.screen.show_image('images/start_camera.jpg')
            action = self.actionables.wait_for_event()
            if action == Actions.TAKE_PICTURES:
                self.take_pictures(3)
            if action == Actions.SELF_DESTRUCT:
                self.destruct()
