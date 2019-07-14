from traps.trap import Trap


class NoTrap(Trap):
    def __init__(self, screen, camera):
        super().__init__(screen, camera)

    def run_trap(self, image_number):
        self.count_down(range(3, 0, -1))
        return [self.camera.take_picture(image_number)]
