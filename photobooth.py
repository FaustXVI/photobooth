import picamera
import pygame
import time
import os
import PIL.Image
import RPi.GPIO as GPIO

from threading import Thread
from pygame.locals import *
from time import sleep
from PIL import Image, ImageDraw

from camera import Camera
from screen import Screen

BUTTON_PIN = 22

GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUTTON_PIN, GPIO.IN)

def wait_for_event():
    global pygame
    no_event = True
    while no_event:
        input_state = GPIO.input(BUTTON_PIN)
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


def main(threadName, *args):
    screen = Screen()
    with Camera(screen) as camera:
        while True:
            screen.show_image('images/start_camera.jpg')
            wait_for_event()
            camera.take_pictures(screen, camera)
        GPIO.cleanup()


# launch the main thread
Thread(target=main, args=('Main', 1)).start()
