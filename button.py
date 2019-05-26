import RPi.GPIO as GPIO
import time
import pygame

from photobooth import Actions


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
        while True:
            input_state = GPIO.input(self.pin_number)
            if input_state:
                return Actions.TAKE_PICTURES
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return Actions.QUIT
                    if event.key == pygame.K_DOWN:
                        return Actions.TAKE_PICTURES
            time.sleep(0.2)
