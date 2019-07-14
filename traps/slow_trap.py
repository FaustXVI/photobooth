from traps.trap import Trap


class SlowTrap(Trap):
    def __init__(self, screen, camera, sleep):
        super().__init__(screen, camera, sleep)

    def run(self, image_number):
        self.count_down([3, 2, 1.5, 1, 0.5, 0.25, 0.1, 0.01])
        return [self.camera.take_picture(image_number)]
