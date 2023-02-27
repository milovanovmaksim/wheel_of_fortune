from typing import TYPE_CHECKING, Type, Optional, TypeVar
from abc import ABC, abstractmethod


if TYPE_CHECKING:
    from bot_long_poll.dcs import Update
    from bot.сhain_responsibility.receivers.receivers import R
    from bot.state.state import State


Self = TypeVar("Self", bound="Handler")


class Handler(ABC):
    """
    Интерфейс Обработчика объявляет метод построения цепочки обработчиков. Он
    также объявляет метод для обработки запроса. https://metanit.com/sharp/patterns/3.7.php
    """

    @abstractmethod
    def set_next_handler(self, handler) -> Self:
        pass

    @abstractmethod
    def handle(self, update: "Update", state: "State") -> Optional["R"]:
        pass


class AbstractHandler(Handler):
    def __init__(self):
        self._next_handler: Optional[Type[Handler]] = None

    def handle(self, update: "Update", state: "State") -> Optional["R"]:
        if self._next_handler:
            return self._next_handler.handle(update, state)
        return None

    def set_next_handler(self, handler: Handler) -> Type[Handler]:
        self._next_handler = handler
        return handler
