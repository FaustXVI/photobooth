class Trap:
    def __init__(self, screen, camera, sleep):
        self.sleep = sleep
        self.screen = screen
        self.camera = camera

    def count_down(self, range):
        for x in range:
            self.screen.update_display(message="{:n}".format(x), background_color="black")
            self.sleep(1)

    def run(self, image_number):
        self.camera.start_preview()
        pictures = self.run_trap(image_number)
        self.camera.stop_preview()
        return pictures

    def run_trap(self, image_number):
        pass
