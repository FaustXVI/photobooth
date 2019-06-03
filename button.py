import RPi.GPIO as GPIO

from photobooth import Actions


class Button:
    def __init__(self, pin_number: int, action=Actions.TAKE_PICTURES):
        self.pin_number = pin_number
        self.action = action
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin_number, GPIO.IN)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        GPIO.cleanup()

    def next_action(self):
        input_state = GPIO.input(self.pin_number)
        if input_state:
            return self.action
        else:
            return None
