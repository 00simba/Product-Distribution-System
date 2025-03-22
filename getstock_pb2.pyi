from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StockEmpty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class StockInformation(_message.Message):
    __slots__ = ("stockInfo",)
    class Tuple(_message.Message):
        __slots__ = ("warehouse_id", "warehouse_stock")
        WAREHOUSE_ID_FIELD_NUMBER: _ClassVar[int]
        WAREHOUSE_STOCK_FIELD_NUMBER: _ClassVar[int]
        warehouse_id: str
        warehouse_stock: str
        def __init__(self, warehouse_id: _Optional[str] = ..., warehouse_stock: _Optional[str] = ...) -> None: ...
    STOCKINFO_FIELD_NUMBER: _ClassVar[int]
    stockInfo: _containers.RepeatedCompositeFieldContainer[StockInformation.Tuple]
    def __init__(self, stockInfo: _Optional[_Iterable[_Union[StockInformation.Tuple, _Mapping]]] = ...) -> None: ...
