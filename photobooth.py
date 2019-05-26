from enum import Enum


class Actions(Enum):
    TAKE_PICTURES = 1
    QUIT = 2


class Photobooth:
    def __init__(self, screen, camera, button, sleep):
        self.sleep = sleep
        self.screen = screen
        self.camera = camera
        self.button = button

    def normal(self, image_number):
        for x in range(3, -1, -1):
            if x == 0:
                self.screen.update_display(message="PRENEZ LA POSE", background_color="black")
            else:
                self.screen.update_display(message=str(x), background_color="black", size=800)
        self.sleep(1)
        return self.camera.take_picture(image_number)

    def capture_picture(self, image_number: int):
        return self.camera.with_preview(image_number, self.normal)

    def take_pictures(self, number_of_pictures):
        for i in range(1, 1 + number_of_pictures):
            self.screen.update_display(message=str(i) + '/' + str(number_of_pictures), size=500)
            self.sleep(1)
            picture = self.capture_picture(i)
            self.screen.show_picture(picture, 2)

    def start(self):
        action = Actions.TAKE_PICTURES
        while action != Actions.QUIT:
            self.screen.show_image('images/start_camera.jpg')
            action = self.button.wait_for_event()
            if action == Actions.TAKE_PICTURES:
                self.take_pictures(3)
