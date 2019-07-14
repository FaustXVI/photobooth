from unittest.mock import Mock, call, ANY

from photobooth import Photobooth, Actions

NUMBER_OF_TRAPS = 4


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
    mock.traps = [Mock()]
    mock.normalMode = Mock()
    button = Mock()
    photobooth = Photobooth(mock.screen, mock.camera, button, mock.sleep,  mock.normalMode, mock.traps, Mock(), FakeRandom([], []))
    button.wait_for_event.side_effect = [Actions.QUIT]
    photobooth.start()
    mock.screen.show_image.assert_called()
    mock.camera.take_pictures.assert_not_called()


def test_photobooth_take_pictures():
    mock = Mock()
    mock.camera = Mock()
    mock.screen = Mock()
    mock.sleep = Mock()
    mock.traps = [Mock()]
    mock.normalMode = Mock()
    button = Mock()
    photobooth = Photobooth(mock.screen, mock.camera, button, mock.sleep, mock.normalMode, mock.traps, Mock(),
                            FakeRandom([True, False, True], [0]))
    button.wait_for_event.side_effect = [Actions.TAKE_PICTURES, Actions.QUIT]
    mock.camera.with_preview.side_effect = [["photo1"], ["photo2"], ["photo3"]]
    photobooth.start()
    mock.screen.show_image.assert_called()
    mock.assert_has_calls([call.screen.update_display(message='1/3', size=500),
                           call.sleep(1),
                           call.camera.with_preview(1, mock.normalMode),
                           call.screen.show_picture("photo1"),
                           call.sleep(3),
                           call.screen.update_display(message='2/3', size=500),
                           call.sleep(1),
                           call.camera.with_preview(2, mock.traps[0]),
                           call.screen.show_picture("photo2"),
                           call.sleep(3),
                           call.screen.update_display(message='3/3', size=500),
                           call.sleep(1),
                           call.camera.with_preview(3, mock.normalMode),
                           call.screen.show_picture("photo3"),
                           call.sleep(3), ])


def test_photobooth_self_destruct():
    mock = Mock()
    mock.self_destruct = Mock()
    mock.camera = Mock()
    mock.screen = Mock()
    mock.sleep = Mock()
    mock.ioniser = Mock()
    mock.fan = Mock()
    button = Mock()
    mock.traps = [Mock()]
    mock.normalMode = Mock()
    photobooth = Photobooth(mock.screen, mock.camera, button, mock.sleep,
                            mock.normalMode,mock.traps,
                            mock.self_destruct,
                            FakeRandom([True, False, True], [0]))
    button.wait_for_event.side_effect = [Actions.SELF_DESTRUCT, Actions.QUIT]
    mock.self_destruct.run.side_effect = [["photo1"]]
    photobooth.start()
    mock.screen.show_image.assert_called()
    mock.assert_has_calls([call.self_destruct.run(),
                           call.screen.show_picture("photo1"),
                           call.sleep(3) ])

