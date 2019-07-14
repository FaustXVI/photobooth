from unittest.mock import Mock, call

from traps.speed_trap import SpeedTrap


def test_photobooth_speed():
    mock = Mock()
    mock.camera = Mock()
    mock.screen = Mock()
    mock.sleep = Mock()
    trap = SpeedTrap(mock.screen, mock.camera, mock.sleep)
    mock.camera.take_picture.side_effect = ["photo1"]
    result = trap.run(1)
    mock.assert_has_calls([
        call.screen.update_display(message="3", background_color="black"),
        call.sleep(1),
        call.screen.update_display(message="2", background_color="black"),
        call.sleep(1),
        call.camera.take_picture(1)
    ])
    assert result == ["photo1"]
