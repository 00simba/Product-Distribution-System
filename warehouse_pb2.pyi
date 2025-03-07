from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Location(_message.Message):
    __slots__ = ("coordinates",)
    class Tuple(_message.Message):
        __slots__ = ("x", "y")
        X_FIELD_NUMBER: _ClassVar[int]
        Y_FIELD_NUMBER: _ClassVar[int]
        x: str
        y: str
        def __init__(self, x: _Optional[str] = ..., y: _Optional[str] = ...) -> None: ...
    COORDINATES_FIELD_NUMBER: _ClassVar[int]
    coordinates: _containers.RepeatedCompositeFieldContainer[Location.Tuple]
    def __init__(self, coordinates: _Optional[_Iterable[_Union[Location.Tuple, _Mapping]]] = ...) -> None: ...
