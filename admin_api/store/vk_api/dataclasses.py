from typing import ClassVar, Type

from marshmallow_dataclass import dataclass
from marshmallow import Schema, EXCLUDE


@dataclass
class Message:
    user_id: int
    text: str

    class Meta:
        unknown = EXCLUDE


@dataclass
class UpdateMessage:
    user_id: int
    body: str
    id: int

    class Meta:
        unknown = EXCLUDE


@dataclass
class UpdateObject:
    user_id: int
    body: str
    id: int

    class Meta:
        unknown = EXCLUDE


@dataclass
class Update:
    type: str
    object: UpdateObject

    Schema_: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE
