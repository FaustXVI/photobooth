from unittest.mock import Mock

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
    photobooth = Photobooth(screen, camera, button)
    photobooth.start()
    screen.show_image.assert_called()
    camera.take_pictures.assert_called()
