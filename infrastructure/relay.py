try:
    import RPi.GPIO as GPIO


    class Relay:
        def __init__(self, pin_number: int):
            self.pin_number = pin_number
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(pin_number, GPIO.OUT, initial = GPIO.LOW)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            GPIO.cleanup()

        def turn_on(self):
            GPIO.output(self.pin_number, GPIO.HIGH)
            pass

        def turn_off(self):
            GPIO.output(self.pin_number, GPIO.LOW)
            pass

except ImportError:
    class Relay:
        def __init__(self, pin_number: int):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

        def turn_on(self):
            pass

        def turn_off(self):
            pass