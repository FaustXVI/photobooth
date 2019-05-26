from enum import Enum


class Actions(Enum):
    TAKE_PICTURES = 1
    QUIT = 2


class Photobooth:
    def __init__(self, screen, camera, button, sleep, random):
        self.random = random
        self.sleep = sleep
        self.screen = screen
        self.camera = camera
        self.button = button

    def normal(self, image_number):
        for x in range(3, -1, -1):
            if x == 0:
                self.screen.update_display(message="PRENEZ LA POSE")
            else:
                self.screen.update_display(message=str(x), size=800)
            self.sleep(1)
        return self.camera.take_picture(image_number)

    def speed(self, image_number):
        for x in range(3, 1, -1):
            self.screen.update_display(message=str(x), size=800)
            self.sleep(1)
        return self.camera.take_picture(image_number)

    def run_shoot_scenario(self, image_number: int):
        return self.camera.with_preview(image_number, self.random.choice([
            self.normal,
            self.speed,
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

    def start(self):
        action = Actions.TAKE_PICTURES
        while action != Actions.QUIT:
            self.screen.show_image('images/start_camera.jpg')
            action = self.button.wait_for_event()
            if action == Actions.TAKE_PICTURES:
                self.take_pictures(3)
