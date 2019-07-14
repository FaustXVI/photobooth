from traps.trap import Trap


class DoubleTrap(Trap):
    def __init__(self, screen, camera, sleep):
        super().__init__(screen, camera, sleep)

    def run(self, image_number):
        self.count_down(range(3, 0, -1))
        first_picture = self.camera.take_picture(image_number)
        self.sleep(1)
        second_picture = self.camera.take_picture(image_number)
        return [first_picture, second_picture]
