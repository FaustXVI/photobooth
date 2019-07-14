class DoubleTrap:
    def __init__(self, screen, camera, sleep):
        self.sleep = sleep
        self.screen = screen
        self.camera = camera

    def count_down(self, range, background_color='black'):
        for x in range:
            self.screen.update_display(message="{:n}".format(x), background_color=background_color)
            self.sleep(1)

    def run(self, image_number):
        self.count_down(range(3, 0, -1))
        first_picture = self.camera.take_picture(image_number)
        self.sleep(1)
        second_picture = self.camera.take_picture(image_number)
        return [first_picture, second_picture]
