from unittest.mock import Mock, call

from photobooth import Photobooth, Actions


def test_photobooth_quit():
    screen = Mock()
    camera = Mock()
    button = Mock()
    button.wait_for_event.side_effect = [Actions.QUIT]
    photobooth = Photobooth(screen, camera, button)
    photobooth.start()
    screen.show_image.assert_called()
    camera.take_pictures.assert_not_called()


def test_photobooth_take_picture():
    screen = Mock()
    camera = Mock()
    button = Mock()
    button.wait_for_event.side_effect = [Actions.TAKE_PICTURES, Actions.QUIT]
    camera.capture_picture.side_effect = ["photo1", "photo2", "photo3"]
    photobooth = Photobooth(screen, camera, button)
    photobooth.start()
    screen.show_image.assert_called()
    camera.capture_picture.assert_has_calls([call(count_down_photo='1/3', image_number=1),
                                             call(count_down_photo='2/3', image_number=2),
                                             call(count_down_photo='3/3', image_number=3)])
    screen.show_picture.assert_has_calls([call("photo1",2),
                                          call("photo2",2),
                                          call("photo3",2)])
