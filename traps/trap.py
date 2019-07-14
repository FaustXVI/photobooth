class Trap:
    def __init__(self, screen, camera, sleep):
        self.sleep = sleep
        self.screen = screen
        self.camera = camera

    def count_down(self, range, background_color='black'):
        for x in range:
            self.screen.update_display(message="{:n}".format(x), background_color=background_color)
            self.sleep(1)

