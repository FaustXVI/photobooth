from unittest.mock import Mock, call

from traps.horn_trap import HornTrap


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
        call.camera.start_preview(),
        call.screen.update_display(message="3"),
        call.speakers.play_sound("sound/horn.wav"),
        call.screen.update_display(message="2"),
        call.screen.update_display(message="1"),
        call.camera.take_picture(1),
        call.camera.stop_preview()
    ])
    assert result == ["photo1"]
