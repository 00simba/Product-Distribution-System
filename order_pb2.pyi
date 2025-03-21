from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OrderEmpty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class OrderInformation(_message.Message):
    __slots__ = ("orderInfo",)
    class Tuple(_message.Message):
        __slots__ = ("id", "x", "y", "quantity")
        ID_FIELD_NUMBER: _ClassVar[int]
        X_FIELD_NUMBER: _ClassVar[int]
        Y_FIELD_NUMBER: _ClassVar[int]
        QUANTITY_FIELD_NUMBER: _ClassVar[int]
        id: str
        x: str
        y: str
        quantity: str
        def __init__(self, id: _Optional[str] = ..., x: _Optional[str] = ..., y: _Optional[str] = ..., quantity: _Optional[str] = ...) -> None: ...
    ORDERINFO_FIELD_NUMBER: _ClassVar[int]
    orderInfo: _containers.RepeatedCompositeFieldContainer[OrderInformation.Tuple]
    def __init__(self, orderInfo: _Optional[_Iterable[_Union[OrderInformation.Tuple, _Mapping]]] = ...) -> None: ...
