try:
    import RPi.GPIO as GPIO


    class Button:
        def __init__(self, pin_number: int, action):
            self.pin_number = pin_number
            self.action = action
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(pin_number, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

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

except ImportError:
    class Button:
        def __init__(self, pin_number: int, action):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

        def next_action(self):
            return None
