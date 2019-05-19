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

PHOTO_FOLDER = 'Photos'
FINALS_FOLDER = os.path.join(PHOTO_FOLDER, 'finals')
IMAGE_FOLDER = os.path.join(PHOTO_FOLDER, 'images')
TEMPLATE_FOLDER = os.path.join(PHOTO_FOLDER, 'Template')
BUTTON_PIN = 25
IMAGE_WIDTH = 550
IMAGE_HEIGHT = 360
TEMPLATE_TOP_RIGHT = (625, 30)
TEMPLATE_BOTTOM_LEFT = (55, 410)
TEMPLATE_BOTTOM_RIGHT = (625, 410)

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

TotalImageCount = 0
imagecounter = 0


def create_screen():
    pygame.init()
    pygame.mouse.set_visible(False)
    screen_info = pygame.display.Info()
    screen_dimensions = (screen_info.current_w, screen_info.current_h)
    s = pygame.display.set_mode(screen_dimensions, pygame.FULLSCREEN)
    b = pygame.Surface(s.get_size()).convert()
    return s, b


def create_camera(a_screen):
    c = picamera.PiCamera(resolution=a_screen.get_size(),
                          framerate=30,
                          sensor_mode=5)
    c.rotation = 0
    c.hflip = True
    c.vflip = False
    c.brightness = 50
    c.preview_alpha = 120
    c.preview_fullscreen = True
    return c


# A function to handle keyboard/mouse/device input events
def check_escape(events):
    for event in events:  # Hit the ESC key to quit the slideshow.
        if (event.type == QUIT or
                (event.type == KEYDOWN and event.key == K_ESCAPE)):
            pygame.quit()


def init_folder(screen, background, folder):
    update_display(screen=screen, background=background, message='Folder Check...')
    os.makedirs(folder, exist_ok=True)


def update_display(screen, background, message="", background_color="white", size=100):
    background.fill(pygame.Color(background_color))
    if message != "":
        font = pygame.font.Font(None, size)
        text = font.render(message, 1, (227, 157, 200))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        textpos.centery = background.get_rect().centery
        background.blit(text, textpos)

    screen.blit(background, (0, 0))

    pygame.display.flip()
    return


def ShowPicture(screen, background, file, delay):
    background.fill((0, 0, 0))
    img = pygame.image.load(file)
    img = pygame.transform.scale(img, screen.get_size())  # Make the image full screen
    background.blit(img, (0, 0))
    screen.blit(background, (0, 0))
    pygame.display.flip()  # update the display
    time.sleep(delay)


# display one image on screen
def show_image(screen, background, image_path):
    screen.fill(pygame.Color("white"))  # clear the screen	
    img = pygame.image.load(image_path)  # load the image
    img = img.convert()
    (screen_width, screen_height) = screen.get_size()
    x = (screen_width / 2) - (img.get_width() / 2)
    y = (screen_height / 2) - (img.get_height() / 2)
    screen.blit(img, (x, y))
    pygame.display.flip()


def CapturePicture(screen, background, camera, count_down_photo):
    global imagecounter
    update_display(screen=screen, background=background, message=count_down_photo, size=500)
    time.sleep(1)
    update_display(screen=screen, background=background)
    background.fill(pygame.Color("black"))
    screen.blit(background, (0, 0))
    pygame.display.flip()
    camera.start_preview()

    for x in range(3, -1, -1):
        if x == 0:
            update_display(screen=screen, background=background, message="PRENEZ LA POSE", background_color="black")
        else:
            update_display(screen=screen, background=background, message=str(x), background_color="black", size=800)
        time.sleep(1)

    update_display(screen=screen, background=background)
    imagecounter = imagecounter + 1
    ts = time.time()
    filename = os.path.join(IMAGE_FOLDER, str(imagecounter) + "_" + str(ts) + '.jpg')
    camera.capture(filename)
    camera.stop_preview()
    ShowPicture(screen, background, filename, 2)
    return filename


def TakePictures(screen, background, camera):
    global TotalImageCount

    check_escape(pygame.event.get())
    filename1 = CapturePicture(screen=screen, background=background, camera=camera, count_down_photo="1/3")
    filename2 = CapturePicture(screen=screen, background=background, camera=camera, count_down_photo="2/3")
    filename3 = CapturePicture(screen=screen, background=background, camera=camera, count_down_photo="3/3")

    update_display(screen=screen, background=background, message="Attendez svp...")

    image1 = PIL.Image.open(filename1)
    image2 = PIL.Image.open(filename2)
    image3 = PIL.Image.open(filename3)
    TotalImageCount = TotalImageCount + 1

    bgimage = PIL.Image.open(os.path.join(TEMPLATE_FOLDER, "template.png"))
    bgimage.paste(image1, TEMPLATE_TOP_RIGHT)
    bgimage.paste(image2, TEMPLATE_BOTTOM_RIGHT)
    bgimage.paste(image3, TEMPLATE_BOTTOM_LEFT)
    # Create the final filename
    ts = time.time()
    Final_Image_Name = os.path.join(FINALS_FOLDER, "Final_" + str(TotalImageCount) + "_" + str(ts) + ".jpg")
    # Save it to the usb drive
    bgimage.save(Final_Image_Name)
    update_display(screen=screen, background=background)
    time.sleep(1)


def WaitForEvent():
    global pygame
    NotEvent = True
    while NotEvent:
        input_state = GPIO.input(BUTTON_PIN)
        if input_state == False:
            NotEvent = False
            return
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_DOWN:
                    NotEvent = False
                    return
        time.sleep(0.2)


def main(threadName, *args):
    (screen, background) = create_screen()
    camera = create_camera(screen)
    init_folder(screen, background, IMAGE_FOLDER)
    init_folder(screen, background, FINALS_FOLDER)
    while True:
        show_image(screen, background, 'images/start_camera.jpg')
        WaitForEvent()
        time.sleep(0.2)
        TakePictures(screen, background, camera)
    GPIO.cleanup()


# launch the main thread
Thread(target=main, args=('Main', 1)).start()
