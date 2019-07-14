from traps.trap import Trap


class NoTrap(Trap):
    def __init__(self, screen, camera, sleep):
        super().__init__(screen, camera, sleep)

    def run(self, image_number):
        self.count_down(range(3, 0, -1))
        return [self.camera.take_picture(image_number)]
