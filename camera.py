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


(screen, background) = create_screen()


def create_camera(screen):
    c = picamera.PiCamera(resolution=screen.get_size(),
                          framerate=30,
                          sensor_mode=1)
    c.rotation = 0
    c.hflip = True
    c.vflip = False
    c.brightness = 50
    c.preview_alpha = 120
    c.preview_fullscreen = True
    return c


camera = create_camera(screen)


# A function to handle keyboard/mouse/device input events
def input(events):
    for event in events:  # Hit the ESC key to quit the slideshow.
        if (event.type == QUIT or
                (event.type == KEYDOWN and event.key == K_ESCAPE)):
            pygame.quit()


def InitFolder(imagefolder):
    UpdateDisplay(Message='Folder Check...')
    os.makedirs(imagefolder, exist_ok=True)


def UpdateDisplay(Message="", Numeral="", CountDownPhoto="", BackgroundColor="white"):
    # init global variables from main thread
    global screen
    global background

    background.fill(pygame.Color(BackgroundColor))
    if (Message != ""):
        font = pygame.font.Font(None, 100)
        text = font.render(Message, 1, (227, 157, 200))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        textpos.centery = background.get_rect().centery
        background.blit(text, textpos)

    if (Numeral != ""):
        font = pygame.font.Font(None, 800)
        text = font.render(Numeral, 1, (227, 157, 200))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        textpos.centery = background.get_rect().centery
        background.blit(text, textpos)

    if (CountDownPhoto != ""):
        font = pygame.font.Font(None, 500)
        text = font.render(CountDownPhoto, 1, (227, 157, 200))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        textpos.centery = background.get_rect().centery
        background.blit(text, textpos)

    screen.blit(background, (0, 0))

    pygame.display.flip()
    return


def ShowPicture(file, delay):
    background.fill((0, 0, 0))
    img = pygame.image.load(file)
    img = pygame.transform.scale(img, screen.get_size())  # Make the image full screen
    background.blit(img, (0, 0))
    screen.blit(background, (0, 0))
    pygame.display.flip()  # update the display
    time.sleep(delay)


# display one image on screen
def show_image(image_path):
    screen.fill(pygame.Color("white"))  # clear the screen	
    img = pygame.image.load(image_path)  # load the image
    img = img.convert()
    x = (screen_info.current_w / 2) - (img.get_width() / 2)
    y = (screen_info.current_h / 2) - (img.get_height() / 2)
    screen.blit(img, (x, y))
    pygame.display.flip()


def CapturePicture(CountDownPhoto):
    global imagecounter
    global screen
    global background
    UpdateDisplay(CountDownPhoto=CountDownPhoto)
    time.sleep(1)
    UpdateDisplay()
    background.fill(pygame.Color("black"))
    screen.blit(background, (0, 0))
    pygame.display.flip()
    camera.start_preview()

    for x in range(3, -1, -1):
        if x == 0:
            UpdateDisplay(Message="PRENEZ LA POSE", BackgroundColor="black")
        else:
            UpdateDisplay(Numeral=str(x), BackgroundColor="black")
        time.sleep(1)

    UpdateDisplay()
    imagecounter = imagecounter + 1
    ts = time.time()
    filename = os.path.join(IMAGE_FOLDER, str(imagecounter) + "_" + str(ts) + '.jpg')
    camera.capture(filename)
    camera.stop_preview()
    ShowPicture(filename, 2)
    return filename


def TakePictures():
    global imagecounter
    global screen
    global background
    global TotalImageCount

    input(pygame.event.get())
    filename1 = CapturePicture(CountDownPhoto="1/3")
    filename2 = CapturePicture(CountDownPhoto="2/3")
    filename3 = CapturePicture(CountDownPhoto="3/3")

    UpdateDisplay(Message="Attendez svp...")

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
    UpdateDisplay()
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
    InitFolder(IMAGE_FOLDER)
    InitFolder(FINALS_FOLDER)
    while True:
        show_image('images/start_camera.jpg')
        WaitForEvent()
        time.sleep(0.2)
        TakePictures()
    GPIO.cleanup()


# launch the main thread
Thread(target=main, args=('Main', 1)).start()
