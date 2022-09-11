from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Action(_message.Message):
    __slots__ = ["from_me", "id", "key", "name"]
    class Name(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    CLOSE: Action.Name
    CLOSED: Action.Name
    CONNECT: Action.Name
    DUPLICATE: Action.Name
    FROM_ME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NONE: Action.Name
    PAIR: Action.Name
    PAIRED: Action.Name
    TIMEOUT: Action.Name
    WS_DISCONNECT: Action.Name
    from_me: bool
    id: str
    key: str
    name: Action.Name
    def __init__(self, name: _Optional[_Union[Action.Name, str]] = ..., from_me: bool = ..., id: _Optional[str] = ..., key: _Optional[str] = ...) -> None: ...

class Alert(_message.Message):
    __slots__ = ["type"]
    class Name(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    BAD_CREDENTIALS: Alert.Name
    CONNECTED: Alert.Name
    NONE: Alert.Name
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: Alert.Name
    def __init__(self, type: _Optional[_Union[Alert.Name, str]] = ...) -> None: ...

class MediaMessage(_message.Message):
    __slots__ = ["caption", "type", "url"]
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    CAPTION_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT: MediaMessage.Type
    IMAGE: MediaMessage.Type
    NONE: MediaMessage.Type
    STICKER: MediaMessage.Type
    TYPE_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    VIDEO: MediaMessage.Type
    caption: str
    type: MediaMessage.Type
    url: str
    def __init__(self, caption: _Optional[str] = ..., url: _Optional[str] = ..., type: _Optional[_Union[MediaMessage.Type, str]] = ...) -> None: ...

class Message(_message.Message):
    __slots__ = ["from_me", "id", "mediaMessage", "textMessage"]
    FROM_ME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    MEDIAMESSAGE_FIELD_NUMBER: _ClassVar[int]
    TEXTMESSAGE_FIELD_NUMBER: _ClassVar[int]
    from_me: bool
    id: str
    mediaMessage: MediaMessage
    textMessage: TextMessage
    def __init__(self, id: _Optional[str] = ..., from_me: bool = ..., mediaMessage: _Optional[_Union[MediaMessage, _Mapping]] = ..., textMessage: _Optional[_Union[TextMessage, _Mapping]] = ...) -> None: ...

class Payload(_message.Message):
    __slots__ = ["action", "alert", "message"]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    ALERT_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    action: Action
    alert: Alert
    message: Message
    def __init__(self, alert: _Optional[_Union[Alert, _Mapping]] = ..., message: _Optional[_Union[Message, _Mapping]] = ..., action: _Optional[_Union[Action, _Mapping]] = ...) -> None: ...

class TextMessage(_message.Message):
    __slots__ = ["text"]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    text: str
    def __init__(self, text: _Optional[str] = ...) -> None: ...
