from dataclasses import dataclass


@dataclass
class Message:
    user_id: int
    message: str
    keyboard: str = "{}"


@dataclass
class User:
    first_name: str
    last_name: str
