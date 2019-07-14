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
    mock.screen = Mock()
    mock.traps = [Mock()]
    mock.normalMode = Mock()
    button = Mock()
    photobooth = Photobooth(mock.screen, button, mock.normalMode, mock.traps, Mock(), Mock(), FakeRandom([], []))
    button.wait_for_event.side_effect = [Actions.QUIT]
    photobooth.start()
    mock.screen.show_image.assert_called()


def test_photobooth_take_pictures():
    mock = Mock()
    mock.screen = Mock()
    mock.trap = Mock()
    mock.normalMode = Mock()
    button = Mock()
    mock.cluster = Mock()
    photobooth = Photobooth(mock.screen, button, mock.normalMode, [mock.trap], Mock(), mock.cluster,
                            FakeRandom([True, False, True], [0]))
    button.wait_for_event.side_effect = [Actions.TAKE_PICTURES, Actions.QUIT]
    mock.normalMode.run.side_effect = [["photo1"], ["photo3"]]
    mock.trap.run.side_effect = [["photo2"]]
    mock.cluster.upload.side_effect = [True]
    photobooth.start()
    mock.screen.show_image.assert_called()
    mock.assert_has_calls([call.screen.update_display(message='1/3', size=500),
                           call.normalMode.run(1),
                           call.screen.show_picture("photo1"),
                           call.screen.update_display(message='2/3', size=500),
                           call.trap.run(2),
                           call.screen.show_picture("photo2"),
                           call.screen.update_display(message='3/3', size=500),
                           call.normalMode.run(3),
                           call.screen.show_picture("photo3"),
                           call.screen.update_display(message='Uploading to cluster...', size=100, duration=0),
                           call.cluster.upload(["photo1", "photo2", "photo3"])])


def test_photobooth_self_destruct():
    mock = Mock()
    mock.self_destruct = Mock()
    mock.screen = Mock()
    button = Mock()
    mock.traps = [Mock()]
    mock.normalMode = Mock()
    mock.cluster = Mock()
    photobooth = Photobooth(mock.screen, button, mock.normalMode, mock.traps, mock.self_destruct, mock.cluster,
                            FakeRandom([True, False, True], [0]))
    button.wait_for_event.side_effect = [Actions.SELF_DESTRUCT, Actions.QUIT]
    mock.self_destruct.run.side_effect = [["photo1"]]
    mock.cluster.upload.side_effect = [True]
    photobooth.start()
    mock.screen.show_image.assert_called()
    mock.assert_has_calls([call.self_destruct.run(),
                           call.screen.show_picture("photo1"),
                           call.screen.update_display(message='Uploading to cluster...', size=100, duration=0),
                           call.cluster.upload(["photo1"])])


def test_photobooth_upload_failed():
    mock = Mock()
    mock.self_destruct = Mock()
    mock.screen = Mock()
    button = Mock()
    mock.traps = [Mock()]
    mock.normalMode = Mock()
    mock.cluster = Mock()
    photobooth = Photobooth(mock.screen, button, mock.normalMode, mock.traps, mock.self_destruct, mock.cluster,
                            FakeRandom([True, False, True], [0]))
    button.wait_for_event.side_effect = [Actions.SELF_DESTRUCT, Actions.QUIT]
    mock.self_destruct.run.side_effect = [["photo1"]]
    mock.cluster.upload.side_effect = [False]
    photobooth.start()
    mock.screen.show_image.assert_called()
    mock.assert_has_calls([call.self_destruct.run(),
                           call.screen.show_picture("photo1"),
                           call.screen.update_display(message='Uploading to cluster...', size=100, duration=0),
                           call.cluster.upload(["photo1"]),
                           call.screen.update_display(message='Failed :(', size=100)
                           ])
   