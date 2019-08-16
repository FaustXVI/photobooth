from traps.trap import Trap


class HornTrap(Trap):
    def __init__(self, screen, camera, sleep, speakers):
        super().__init__(screen, camera)
        self.sleep = sleep
        self.speakers = speakers

    def run_trap(self, image_number):
        self.count_down(range(3, 2, -1))
        self.speakers.play_sound("sound/horn.wav")
        self.count_down(range(2, 0, -1))
        return [self.camera.take_picture(image_number)]
