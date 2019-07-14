class Trap:
    def __init__(self, screen, camera):
        self.screen = screen
        self.camera = camera

    def count_down(self, range):
        for x in range:
            self.screen.update_display(message="{:n}".format(x))

    def run(self, image_number):
        self.camera.start_preview()
        pictures = self.run_trap(image_number)
        self.camera.stop_preview()
        return pictures

    def run_trap(self, image_number):
        pass
