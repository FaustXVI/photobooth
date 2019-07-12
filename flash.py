try:
    import RPi.GPIO as GPIO


    class Flash:
        def __init__(self, pin_number: int):
            self.pin_number = pin_number
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(pin_number, GPIO.OUT)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            GPIO.cleanup()

        def turn_on(self):
            GPIO.output(self.pin_number, GPIO.LOW)
            pass

        def turn_off(self):
            GPIO.output(self.pin_number, GPIO.HIGH)
            pass

except ImportError:
    class Flash:
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