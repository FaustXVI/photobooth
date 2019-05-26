from threading import Thread

from button import Button
from camera import Camera
from screen import Screen


def main(threadName, *args):
    screen = Screen()
    with Button(22) as button:
        with Camera(screen) as camera:
            while True:
                screen.show_image('images/start_camera.jpg')
                button.wait_for_event()
                camera.take_pictures()


# launch the main thread
Thread(target=main, args=('Main', 1)).start()
