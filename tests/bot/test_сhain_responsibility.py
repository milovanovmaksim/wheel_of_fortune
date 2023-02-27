from typing import TYPE_CHECKING

import bot.сhain_responsibility.receivers as rv
from .data import COMMANDS_USER1


if TYPE_CHECKING:
    from bot.сhain_responsibility.manager import HandlerManager
    from bot.state.state import State


class TestNotCallbackButtonHandler:
    def test_start_command(self, handler_manager: "HandlerManager", state: "State"):
        update = COMMANDS_USER1["start"]
        handler = handler_manager.handle(update, state)
        assert isinstance(handler, rv.StartCommandButtonReceiver)

    def test_game_request_command(self, handler_manager: "HandlerManager", state: "State"):
        update = COMMANDS_USER1["game_request"]
        handler = handler_manager.handle(update, state)
        assert isinstance(handler, rv.GameRequestCommandButtonReceiver)

    def test_about_command(self, handler_manager: "HandlerManager", state: "State"):
        update = COMMANDS_USER1["about"]
        handler = handler_manager.handle(update, state)
        assert isinstance(handler, rv.AboutCommandButtonReceiver)

    def test_start_game_command(self, handler_manager: "HandlerManager", state: "State"):
        update = COMMANDS_USER1["start_game"]
        handler = handler_manager.handle(update, state)
        assert isinstance(handler, rv.StartGameCommandButtonReceiver)

    def test_guess_letter_command(self, handler_manager: "HandlerManager", state: "State"):
        update = COMMANDS_USER1["guess_letter_correct"]
        handler = handler_manager.handle(update, state)
        assert isinstance(handler, rv.GuessLetterCommandButtonReceiver)

    def test_quite_command(self, handler_manager: "HandlerManager", state: "State"):
        update = COMMANDS_USER1["quite"]
        handler = handler_manager.handle(update, state)
        assert isinstance(handler, rv.QuiteCommandButtonReceiver)

    def test_cancel_game_request_command(self, handler_manager: "HandlerManager", state: "State"):
        update = COMMANDS_USER1["cancel_game_request"]
        handler = handler_manager.handle(update, state)
        assert isinstance(handler, rv.CancelGameRequestCommandButtonReceiver)


class TestTextHandler:
    def test_start_command(self, handler_manager: "HandlerManager", state: "State"):
        update = COMMANDS_USER1["начать"]
        handler = handler_manager.handle(update, state)
        assert isinstance(handler, rv.StartTextReceiver)
