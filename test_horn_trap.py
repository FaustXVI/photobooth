from unittest.mock import Mock, call, ANY

from horn_trap import HornTrap


def test_photobooth_horn():
    mock = Mock()
    mock.camera = Mock()
    mock.screen = Mock()
    mock.sleep = Mock()
    mock.speakers = Mock()
    trap = HornTrap(mock.screen, mock.camera, mock.sleep, mock.speakers)
    mock.camera.take_picture.side_effect = ["photo1"]
    result = trap.run(1)
    mock.assert_has_calls([
        call.screen.update_display(message="3", background_color="black"),
        call.sleep(1),
        call.screen.update_display(message="2", background_color="black"),
        call.sleep(1),
        call.screen.update_display(message="1", background_color="black"),
        call.sleep(1),
        call.speakers.play_sound("sound/horn.wav"),
        call.sleep(1),
        call.camera.take_picture(1)
    ])
    assert result == ["photo1"]
