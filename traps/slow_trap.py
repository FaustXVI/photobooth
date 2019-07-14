class SlowTrap:
    def __init__(self, screen, camera, sleep):
        self.sleep = sleep
        self.screen = screen
        self.camera = camera

    def count_down(self, range, background_color='black'):
        for x in range:
            self.screen.update_display(message="{:n}".format(x), background_color=background_color)
            self.sleep(1)

    def run(self, image_number):
        self.count_down([3, 2, 1.5, 1, 0.5, 0.25, 0.1, 0.01])
        return [self.camera.take_picture(image_number)]
