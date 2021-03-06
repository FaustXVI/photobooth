from unittest.mock import Mock, call

from traps.double_trap import DoubleTrap


def test_photobooth_double():
    mock = Mock()
    mock.camera = Mock()
    mock.screen = Mock()
    mock.sleep = Mock()
    trap = DoubleTrap(mock.screen, mock.camera, mock.sleep)
    mock.camera.take_picture.side_effect = ["photo1", "photo2"]
    result = trap.run(1)
    mock.assert_has_calls([
        call.camera.start_preview(),
        call.screen.update_display(message="3"),
        call.screen.update_display(message="2"),
        call.screen.update_display(message="1"),
        call.camera.take_picture(1),
        call.sleep(1),
        call.camera.take_picture(1),
        call.camera.stop_preview()
    ])
    assert result == ["photo1", "photo2"]
