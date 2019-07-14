class HornTrap:
    def __init__(self, screen, camera, sleep, speakers):
        self.sleep = sleep
        self.screen = screen
        self.camera = camera
        self.speakers = speakers

    def count_down(self, range, background_color='black'):
        for x in range:
            self.screen.update_display(message="{:n}".format(x), background_color=background_color)
            self.sleep(1)

    def run(self, image_number):
        self.count_down(range(3, 0, -1))
        self.speakers.play_sound("sound/horn.wav")
        self.sleep(1)
        return [self.camera.take_picture(image_number)]
