from typing import ClassVar, Type, Optional
import json
from dataclasses import field

from marshmallow_dataclass import dataclass, NewType
from marshmallow import Schema as MarshmallowSchema, EXCLUDE, fields


class PayloadField(fields.Field):
    def _serialize(self, value: "Payload", attr, obj, **kwargs):
        if value:
            return Payload.Schema().dumps(value)
        return None

    def _deserialize(self, value: str, attr, data, **kwargs):
        return Payload.Schema().load(json.loads(value))


@dataclass
class Payload:
    command: str
    letter: Optional[str]
    Schema: ClassVar[Type[MarshmallowSchema]] = MarshmallowSchema

    class Meta:
        unknown = EXCLUDE


PayloadType = NewType('Message', Payload, PayloadField)


@dataclass
class Message:
    from_id: int
    text: str
    id: int
    payload: Optional[PayloadType] = field(default=None)

    class Meta:
        unknown = EXCLUDE


@dataclass
class UpdateObject:
    message: Message

    class Meta:
        unknown = EXCLUDE


@dataclass
class Update:
    type: str
    object: UpdateObject

    Schema: ClassVar[Type[MarshmallowSchema]] = MarshmallowSchema

    class Meta:
        unknown = EXCLUDE

    def get_payload(self) -> Optional[Payload]:
        return self.object.message.payload

    @property
    def from_id(self):
        return self.object.message.from_id
    
    @property
    def text(self):
        return self.object.message.text
