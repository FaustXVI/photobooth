from unittest.mock import Mock, call, ANY

from photobooth import Photobooth, Actions

NUMBER_OF_TRAPS = 2


class FakeRandom:
    def __init__(self, isNormals, choices):
        self.isNormalIndex = 0
        self.isNormals = isNormals
        self.choiceIndex = 0
        self.choices = choices

    def choice(self, array):
        result = array[self.choices[self.choiceIndex]]
        self.choiceIndex = self.choiceIndex + 1
        return result

    def is_normal(self):
        result = self.isNormals[self.isNormalIndex]
        self.isNormalIndex = self.isNormalIndex + 1
        return result


def test_photobooth_quit():
    mock = Mock()
    mock.camera = Mock()
    mock.screen = Mock()
    mock.sleep = Mock()
    button = Mock()
    photobooth = Photobooth(mock.screen, mock.camera, button, mock.sleep, FakeRandom([], []))
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
    photobooth = Photobooth(mock.screen, mock.camera, button, mock.sleep, FakeRandom([True, False, True], [0]))
    button.wait_for_event.side_effect = [Actions.TAKE_PICTURES, Actions.QUIT]
    mock.camera.with_preview.side_effect = ["photo1", "photo2", "photo3"]
    photobooth.start()
    mock.screen.show_image.assert_called()
    mock.assert_has_calls([call.screen.update_display(message='1/3', size=500),
                           call.sleep(1),
                           call.camera.with_preview(1, photobooth.normal),
                           call.screen.show_picture("photo1"),
                           call.sleep(3),
                           call.screen.update_display(message='2/3', size=500),
                           call.sleep(1),
                           call.camera.with_preview(2, photobooth.fast),
                           call.screen.show_picture("photo2"),
                           call.sleep(3),
                           call.screen.update_display(message='3/3', size=500),
                           call.sleep(1),
                           call.camera.with_preview(3, photobooth.normal),
                           call.screen.show_picture("photo3"),
                           call.sleep(3), ])


def test_photobooth_random_senario_normal():
    camera = Mock()
    photobooth = Photobooth(Mock(), camera, Mock(), Mock(), FakeRandom([True], []))
    photobooth.run_shoot_scenario(1)
    camera.assert_has_calls([call.with_preview(1, photobooth.normal)])


def test_photobooth_random_senario_fast():
    for i in range(0, NUMBER_OF_TRAPS):
        camera = Mock()
        photobooth = Photobooth(Mock(), camera, Mock(), Mock(), FakeRandom([False], [i]))
        photobooth.run_shoot_scenario(1)
        camera.assert_has_calls([call.with_preview(1, ANY)])


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
    result = photobooth.fast(1)
    mock.assert_has_calls([
        call.screen.update_display(message="3", size=800),
        call.sleep(1),
        call.screen.update_display(message="2", size=800),
        call.sleep(1),
        call.camera.take_picture(1)
    ])
    assert result == "photo1"


def test_photobooth_slow():
    mock = Mock()
    mock.camera = Mock()
    mock.screen = Mock()
    mock.sleep = Mock()
    photobooth = Photobooth(mock.screen, mock.camera, Mock(), mock.sleep, Mock())
    mock.camera.take_picture.side_effect = ["photo1"]
    result = photobooth.slow(1)
    mock.assert_has_calls([
        call.screen.update_display(message="3", size=800),
        call.sleep(1),
        call.screen.update_display(message="2", size=800),
        call.sleep(1),
        call.screen.update_display(message="1,5", size=800),
        call.sleep(1),
        call.screen.update_display(message="1", size=800),
        call.sleep(1),
        call.screen.update_display(message="0,5", size=800),
        call.sleep(1),
        call.screen.update_display(message="0,25", size=800),
        call.sleep(1),
        call.screen.update_display(message="0,1", size=800),
        call.sleep(1),
        call.screen.update_display(message="0,01", size=800),
        call.sleep(1),
        call.camera.take_picture(1)
    ])
    assert result == "photo1"
