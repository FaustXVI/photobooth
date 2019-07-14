from unittest.mock import Mock, call

from traps.no_trap import NoTrap


def test_photobooth_normal():
    mock = Mock()
    mock.camera = Mock()
    mock.screen = Mock()
    trap = NoTrap(mock.screen, mock.camera)
    mock.camera.take_picture.side_effect = ["photo1"]
    result = trap.run(1)
    mock.assert_has_calls([
        call.camera.start_preview(),
        call.screen.update_display(message="3"),
        call.screen.update_display(message="2"),
        call.screen.update_display(message="1"),
        call.camera.take_picture(1),
        call.camera.stop_preview()
    ])
    assert result == ["photo1"]
