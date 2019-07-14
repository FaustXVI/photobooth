from unittest.mock import Mock, call, ANY

from self_destruction import SelfDestruction


def test_photobooth_self_destruct():
    mock = Mock()
    mock.ioniser = Mock()
    mock.screen = Mock()
    mock.sleep = Mock()
    mock.speakers = Mock()
    mock.fan = Mock()
    mock.camera = Mock()
    self_destruction = SelfDestruction(mock.screen, mock.camera, mock.sleep, mock.speakers, mock.ioniser, mock.fan)
    mock.camera.take_picture.side_effect = ["photo1"]
    pictures = self_destruction.run()
    assert pictures == ["photo1"]
    mock.assert_has_calls([call.ioniser.turn_on(),
                           call.speakers.play_sound('sound/self-destruct.ogg'),
                           call.screen.update_display(message='WARNING', background_color='red', size=500),
                           call.sleep(2),
                           call.screen.update_display(message='self-destruction', background_color='red', size=400),
                           call.sleep(3),
                           call.screen.update_display(message="10", background_color='red'),
                           call.sleep(1),
                           call.screen.update_display(message="9", background_color='red'),
                           call.sleep(1),
                           call.screen.update_display(message="8", background_color='red'),
                           call.sleep(1),
                           call.screen.update_display(message="7", background_color='red'),
                           call.sleep(1),
                           call.screen.update_display(message="6", background_color='red'),
                           call.sleep(1),
                           call.screen.update_display(message="5", background_color='red'),
                           call.sleep(1),
                           call.screen.update_display(message="4", background_color='red'),
                           call.sleep(1),
                           call.fan.turn_on(),
                           call.screen.update_display(message="3", background_color='red'),
                           call.sleep(1),
                           call.screen.update_display(message="2", background_color='red'),
                           call.sleep(1),
                           call.screen.update_display(message="1", background_color='red'),
                           call.sleep(1),
                           call.fan.turn_off(),
                           call.screen.show_picture("images/bsod.png"),
                           call.sleep(1),
                           call.camera.take_picture(1),
                           call.ioniser.turn_off()])