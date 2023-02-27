from typing import TYPE_CHECKING, List, Type

from bot.сhain_responsibility.manager import HandlerManager
from bot.сhain_responsibility.handlers.handlers import NotCallbackButtonHandler, TextHandler
import bot.сhain_responsibility.receivers as rv


if TYPE_CHECKING:
    from bot.сhain_responsibility.handlers.abstract import Handler


def setup_handlers() -> List[Type["Handler"]]:
    handlers = [
        NotCallbackButtonHandler("start", rv.StartCommandButtonReceiver),
        NotCallbackButtonHandler("game_request", rv.GameRequestCommandButtonReceiver),
        NotCallbackButtonHandler("about", rv.AboutCommandButtonReceiver),
        NotCallbackButtonHandler("start_game", rv.StartGameCommandButtonReceiver),
        NotCallbackButtonHandler("guess_letter", rv.GuessLetterCommandButtonReceiver),
        NotCallbackButtonHandler("quite", rv.QuiteCommandButtonReceiver),
        NotCallbackButtonHandler("cancel_game_request", rv.CancelGameRequestCommandButtonReceiver),
        TextHandler("начать", rv.StartTextReceiver),
    ]
    return handlers


def setup_сhain_responsibility() -> HandlerManager:
    handlers = setup_handlers()
    handler_manager = HandlerManager(handlers)
    handler_manager.create_сhain_responsibility()
    return handler_manager
