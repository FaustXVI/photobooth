from unittest.mock import Mock, call

from photobooth import Photobooth, Actions


def test_photobooth_quit():
    mock = Mock()
    mock.camera = Mock()
    mock.screen = Mock()
    mock.sleep = Mock()
    button = Mock()
    photobooth = Photobooth(mock.screen, mock.camera, button, mock.sleep)
    button.wait_for_event.side_effect = [Actions.QUIT]
    photobooth.start()
    mock.screen.show_image.assert_called()
    mock.camera.take_pictures.assert_not_called()


def test_photobooth_take_pictures():
    mock = Mock()
    mock.camera = Mock()
    mock.screen = Mock()
    mock.sleep = Mock()
    button = Mock()
    photobooth = Photobooth(mock.screen, mock.camera, button, mock.sleep)
    button.wait_for_event.side_effect = [Actions.TAKE_PICTURES, Actions.QUIT]
    mock.camera.capture_picture.side_effect = ["photo1", "photo2", "photo3"]
    photobooth.start()
    mock.screen.show_image.assert_called()
    mock.assert_has_calls([call.screen.update_display(message='1/3', size=500),
                           call.sleep(1),
                           call.camera.capture_picture(1),
                           call.screen.show_picture("photo1", 2),
                           call.screen.update_display(message='2/3', size=500),
                           call.sleep(1),
                           call.camera.capture_picture(2),
                           call.screen.show_picture("photo2", 2),
                           call.screen.update_display(message='3/3', size=500),
                           call.sleep(1),
                           call.camera.capture_picture(3),
                           call.screen.show_picture("photo3", 2)])
