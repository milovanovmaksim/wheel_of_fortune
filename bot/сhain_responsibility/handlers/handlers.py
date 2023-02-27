from typing import Optional, TYPE_CHECKING

from bot.сhain_responsibility.handlers.abstract import AbstractHandler
from bot.сhain_responsibility.receivers import GuessWordReceiver

if TYPE_CHECKING:
    from bot.сhain_responsibility.receivers.receivers import R
    from bot_long_poll.dcs import Update
    from bot.state.state import State


"""
Все Конкретные Обработчики либо обрабатывают сообщение, либо передают его
следующему обработчику в цепочке.
"""


class NotCallbackButtonHandler(AbstractHandler):
    def __init__(self, command, receiver: "R"):
        self.command = command
        self.receiver = receiver
        super().__init__()

    def handle(self, update: "Update", state: "State") -> Optional["R"]:
        payload = update.get_payload()
        if payload:
            if payload.command == self.command:
                return self.receiver(update, state)
        return super().handle(update, state)


class TextHandler(AbstractHandler):
    def __init__(self, text: Optional[str], receiver: "R"):
        self.text = text
        self.receiver = receiver
        super().__init__()

    def handle(self, update: "Update", state: "State") -> Optional["R"]:
        if self.text:
            if update.text.lower() == self.text:
                return self.receiver(update, state)
        return GuessWordReceiver(update, state)
