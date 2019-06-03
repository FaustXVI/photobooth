from unittest.mock import Mock

from actionables import Actionables
from photobooth import Actions


def test_actionable_with_one_action():
    fake_button = Mock()
    fake_button.next_action.side_effect = [Actions.QUIT]
    actionables = Actionables([fake_button])
    assert actionables.wait_for_event() == Actions.QUIT


def test_actionable_with_waiting():
    fake_button = Mock()
    fake_button.next_action.side_effect = [None, Actions.QUIT]
    actionables = Actionables([fake_button])
    assert actionables.wait_for_event() == Actions.QUIT


def test_actionable_with_first_input_action():
    fake_keyboard = Mock()
    fake_button = Mock()
    fake_button.next_action.side_effect = [Actions.TAKE_PICTURES]
    fake_keyboard.next_action.side_effect = [None]
    actionables = Actionables([fake_button, fake_keyboard])
    assert actionables.wait_for_event() == Actions.TAKE_PICTURES


def test_actionable_with_second_input_action():
    fake_keyboard = Mock()
    fake_button = Mock()
    fake_button.next_action.side_effect = [None]
    fake_keyboard.next_action.side_effect = [Actions.TAKE_PICTURES]
    actionables = Actionables([fake_button, fake_keyboard])
    assert actionables.wait_for_event() == Actions.TAKE_PICTURES
