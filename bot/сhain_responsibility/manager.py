from typing import List, TYPE_CHECKING, Optional


if TYPE_CHECKING:
    from bot.сhain_responsibility.receivers.receivers import R
    from bot.state.state import State
    from bot.сhain_responsibility.handlers.abstract import Handler
    from bot_long_poll.dcs import Update


class HandlerManager:
    """
    Класс для создания цепочки обработчиков.
    """
    def __init__(self, handlers: List["Handler"] = []):
        self.handlers: List["Handler"] = handlers

    def create_сhain_responsibility(self):
        handler: Handler = self.handlers[0]
        for next_handler in self.handlers[1:]:
            handler: Handler = handler.set_next_handler(next_handler)

    def handle(self, update: "Update", state: "State") -> Optional["R"]:
        handler: "Handler" = self.handlers[0]
        return handler.handle(update, state)

    def append_handler(self, handler: "Handler"):
        self.handlers.append(handler)
