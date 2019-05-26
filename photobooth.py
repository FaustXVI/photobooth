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

from screen import Screen

HD_RESOLUTION = (1920, 1080)

PHOTO_FOLDER = 'Photos'
IMAGE_FOLDER = os.path.join(PHOTO_FOLDER, 'images')
BUTTON_PIN = 22
IMAGE_WIDTH = 550
IMAGE_HEIGHT = 360

GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUTTON_PIN, GPIO.IN)


def create_camera():
    c = picamera.PiCamera(resolution=HD_RESOLUTION,
                          framerate=30,
                          sensor_mode=5)
    c.rotation = 0
    c.hflip = True
    c.vflip = False
    c.brightness = 50
    c.preview_alpha = 120
    c.preview_fullscreen = True
    return c

def capture_picture(screen: Screen, camera, count_down_photo, image_number):
    screen.update_display(message=count_down_photo, size=500)
    time.sleep(1)
    screen.update_display()
    screen.reset()
    pygame.display.flip()
    camera.start_preview()

    for x in range(3, -1, -1):
        if x == 0:
            screen.update_display(message="PRENEZ LA POSE", background_color="black")
        else:
            screen.update_display(message=str(x), background_color="black", size=800)
        time.sleep(1)

    screen.update_display()
    ts = time.time()
    filename = os.path.join(IMAGE_FOLDER, str(image_number) + "_" + str(ts) + '.jpg')
    camera.capture(filename)
    camera.stop_preview()
    screen.show_picture(filename, 2)
    return filename


def take_pictures(screen: Screen, camera):
    number_of_pictures = 3
    for i in range(1, 1 + number_of_pictures):
        capture_picture(screen=screen, camera=camera,
                        count_down_photo=str(i) + '/' + str(number_of_pictures),
                        image_number=i)


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
    with create_camera() as camera:
        screen.update_display(message='Folder Check...')
        os.makedirs(IMAGE_FOLDER, exist_ok=True)
        while True:
            screen.show_image('images/start_camera.jpg')
            wait_for_event()
            take_pictures(screen, camera)
        GPIO.cleanup()


# launch the main thread
Thread(target=main, args=('Main', 1)).start()
