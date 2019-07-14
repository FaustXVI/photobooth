from traps.trap import Trap


class SelfDestruction():
    def __init__(self, screen, camera, sleep, speakers, ioniser, fan):
        self.screen = screen
        self.camera = camera
        self.sleep = sleep
        self.speakers = speakers
        self.ioniser = ioniser
        self.fan = fan

    def count_down(self, range):
        for x in range:
            self.screen.update_display(message="{:n}".format(x), background_color="red")
            self.sleep(1)

    def run(self):
        self.ioniser.turn_on()
        self.speakers.play_sound('sound/self-destruct.ogg')
        self.screen.update_display(message='WARNING', background_color='red', size=500)
        self.sleep(2)
        self.screen.update_display(message='self-destruction', background_color='red', size=400)
        self.sleep(3)
        self.count_down(range(10, 3, -1))
        self.fan.turn_on()
        self.count_down(range(3, 0, -1))
        self.fan.turn_off()
        self.screen.show_picture("images/bsod.png")
        self.sleep(1)
        picture = self.camera.take_picture(1)
        self.ioniser.turn_off()
        return [picture]
