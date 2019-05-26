from unittest.mock import Mock, call

from photobooth import Photobooth, Actions


class FakeRandom:
    def __init__(self, i):
        self.i = i

    def choice(self, array):
        return array[self.i]


def test_photobooth_quit():
    mock = Mock()
    mock.camera = Mock()
    mock.screen = Mock()
    mock.sleep = Mock()
    button = Mock()
    photobooth = Photobooth(mock.screen, mock.camera, button, mock.sleep, FakeRandom(0))
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
    photobooth = Photobooth(mock.screen, mock.camera, button, mock.sleep, FakeRandom(0))
    button.wait_for_event.side_effect = [Actions.TAKE_PICTURES, Actions.QUIT]
    mock.camera.with_preview.side_effect = ["photo1", "photo2", "photo3"]
    photobooth.start()
    mock.screen.show_image.assert_called()
    mock.assert_has_calls([call.screen.update_display(message='1/3', size=500),
                           call.sleep(1),
                           call.camera.with_preview(1, photobooth.normal),
                           call.screen.show_picture("photo1", 2),
                           call.screen.update_display(message='2/3', size=500),
                           call.sleep(1),
                           call.camera.with_preview(2, photobooth.normal),
                           call.screen.show_picture("photo2", 2),
                           call.screen.update_display(message='3/3', size=500),
                           call.sleep(1),
                           call.camera.with_preview(3, photobooth.normal),
                           call.screen.show_picture("photo3", 2)])


def test_photobooth_random_senario_normal():
    camera = Mock()
    photobooth = Photobooth(Mock(), camera, Mock(), Mock(), FakeRandom(0))
    photobooth.run_shoot_scenario(1)
    camera.assert_has_calls([call.with_preview(1, photobooth.normal)])


def test_photobooth_random_senario_speed():
    camera = Mock()
    photobooth = Photobooth(Mock(), camera, Mock(), Mock(), FakeRandom(1))
    photobooth.run_shoot_scenario(1)
    camera.assert_has_calls([call.with_preview(1, photobooth.speed)])


def test_photobooth_normal():
    mock = Mock()
    mock.camera = Mock()
    mock.screen = Mock()
    mock.sleep = Mock()
    photobooth = Photobooth(mock.screen, mock.camera, Mock(), mock.sleep, Mock())
    mock.camera.take_picture.side_effect = ["photo1"]
    result = photobooth.normal(1)
    mock.assert_has_calls([
        call.screen.update_display(message="3", size=800),
        call.sleep(1),
        call.screen.update_display(message="2", size=800),
        call.sleep(1),
        call.screen.update_display(message="1", size=800),
        call.sleep(1),
        call.screen.update_display(message="PRENEZ LA POSE"),
        call.sleep(1),
        call.camera.take_picture(1)
    ])
    assert result == "photo1"


def test_photobooth_speed():
    mock = Mock()
    mock.camera = Mock()
    mock.screen = Mock()
    mock.sleep = Mock()
    photobooth = Photobooth(mock.screen, mock.camera, Mock(), mock.sleep, Mock())
    mock.camera.take_picture.side_effect = ["photo1"]
    result = photobooth.speed(1)
    mock.assert_has_calls([
        call.screen.update_display(message="3", size=800),
        call.sleep(1),
        call.screen.update_display(message="2", size=800),
        call.sleep(1),
        call.camera.take_picture(1)
    ])
    assert result == "photo1"
