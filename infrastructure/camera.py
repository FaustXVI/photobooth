from infrastructure.relay import Relay

try:
    from datetime import datetime
    import picamera
    import os

    HD_RESOLUTION = (1920, 1080)

    IMAGE_WIDTH = 550
    IMAGE_HEIGHT = 360


    class Camera:
        def __init__(self, pictures_folder, flash: Relay):
            self.flash = flash
            self.pictures_folder = pictures_folder
            self.camera = picamera.PiCamera(resolution=HD_RESOLUTION,
                                            framerate=30,
                                            sensor_mode=5)
            self.camera.rotation = 0
            self.camera.hflip = True
            self.camera.vflip = False
            self.camera.brightness = 50
            self.camera.preview_alpha = 120
            self.camera.preview_fullscreen = True

        def __enter__(self):
            self.camera.__enter__()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.camera.__exit__(exc_type, exc_val, exc_tb)

        def take_picture(self, image_number: int):
            time = datetime.now().strftime("%H_%M_%S")
            filename = os.path.join(self.pictures_folder, time + "_" + str(image_number) + '.jpg')
            self.flash.turn_on()
            self.camera.capture(filename)
            self.flash.turn_off()
            return filename

        def start_preview(self):
            self.camera.start_preview()

        def stop_preview(self):
            self.camera.stop_preview()

except ImportError:

    class Camera:
        def __init__(self, pictures_folder, flash: Relay):
            self.pictures_folder = pictures_folder

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

        def take_picture(self, image_number: int):
            return "images/unicorns.jpg"

        def start_preview(self):
            pass

        def stop_preview(self):
            pass
