import locale
from unittest.mock import Mock, call

from traps.slow_trap import SlowTrap

def test_photobooth_slow():
    locale.setlocale(locale.LC_ALL, "fr_FR.utf8")
    mock = Mock()
    mock.camera = Mock()
    mock.screen = Mock()
    trap = SlowTrap(mock.screen, mock.camera)
    mock.camera.take_picture.side_effect = ["photo1"]
    result = trap.run(1)
    mock.assert_has_calls([
        call.camera.start_preview(),
        call.screen.update_display(message="3"),
        call.screen.update_display(message="2"),
        call.screen.update_display(message="1,5"),
        call.screen.update_display(message="1"),
        call.screen.update_display(message="0,5"),
        call.screen.update_display(message="0,25"),
        call.screen.update_display(message="0,1"),
        call.screen.update_display(message="0,01"),
        call.camera.take_picture(1),
        call.camera.stop_preview()
    ])
    assert result == ["photo1"]
