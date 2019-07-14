import locale
from unittest.mock import Mock, call

from slow_trap import SlowTrap

def test_photobooth_slow():
    locale.setlocale(locale.LC_ALL, "fr_FR.utf8")
    mock = Mock()
    mock.camera = Mock()
    mock.screen = Mock()
    mock.sleep = Mock()
    trap = SlowTrap(mock.screen, mock.camera, mock.sleep)
    mock.camera.take_picture.side_effect = ["photo1"]
    result = trap.run(1)
    mock.assert_has_calls([
        call.screen.update_display(message="3", background_color="black"),
        call.sleep(1),
        call.screen.update_display(message="2", background_color="black"),
        call.sleep(1),
        call.screen.update_display(message="1,5", background_color="black"),
        call.sleep(1),
        call.screen.update_display(message="1", background_color="black"),
        call.sleep(1),
        call.screen.update_display(message="0,5", background_color="black"),
        call.sleep(1),
        call.screen.update_display(message="0,25", background_color="black"),
        call.sleep(1),
        call.screen.update_display(message="0,1", background_color="black"),
        call.sleep(1),
        call.screen.update_display(message="0,01", background_color="black"),
        call.sleep(1),
        call.camera.take_picture(1)
    ])
    assert result == ["photo1"]
