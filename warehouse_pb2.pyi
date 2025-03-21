from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Location(_message.Message):
    __slots__ = ("warehouseInfo",)
    class Tuple(_message.Message):
        __slots__ = ("id", "x", "y", "capacity")
        ID_FIELD_NUMBER: _ClassVar[int]
        X_FIELD_NUMBER: _ClassVar[int]
        Y_FIELD_NUMBER: _ClassVar[int]
        CAPACITY_FIELD_NUMBER: _ClassVar[int]
        id: str
        x: str
        y: str
        capacity: str
        def __init__(self, id: _Optional[str] = ..., x: _Optional[str] = ..., y: _Optional[str] = ..., capacity: _Optional[str] = ...) -> None: ...
    WAREHOUSEINFO_FIELD_NUMBER: _ClassVar[int]
    warehouseInfo: _containers.RepeatedCompositeFieldContainer[Location.Tuple]
    def __init__(self, warehouseInfo: _Optional[_Iterable[_Union[Location.Tuple, _Mapping]]] = ...) -> None: ...
