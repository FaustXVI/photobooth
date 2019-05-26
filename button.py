import RPi.GPIO as GPIO
import time


class Button:
    def __init__(self, pin_number: int):
        self.pin_number = pin_number
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin_number, GPIO.IN)

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        GPIO.cleanup()

    def wait_for_event(self):
        global pygame
        no_event = True
        while no_event:
            input_state = GPIO.input(self.pin_number)
            if input_state:
                no_event = False
                return
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                    if event.key == pygame.K_DOWN:
                        no_event = False
                        return
            time.sleep(0.2)
