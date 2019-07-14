from traps.trap import Trap


class HornTrap(Trap):
    def __init__(self, screen, camera, sleep, speakers):
        super().__init__(screen, camera, sleep)
        self.speakers = speakers

    def run_trap(self, image_number):
        self.count_down(range(3, 0, -1))
        self.speakers.play_sound("sound/horn.wav")
        self.sleep(1)
        return [self.camera.take_picture(image_number)]
