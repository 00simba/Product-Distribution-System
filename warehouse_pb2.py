# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: warehouse.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'warehouse.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fwarehouse.proto\"\x07\n\x05\x45mpty\"\x81\x01\n\x08Location\x12&\n\rwarehouseInfo\x18\x01 \x03(\x0b\x32\x0f.Location.Tuple\x1aM\n\x05Tuple\x12\n\n\x02id\x18\x01 \x01(\t\x12\t\n\x01x\x18\x02 \x01(\t\x12\t\n\x01y\x18\x03 \x01(\t\x12\x10\n\x08\x63\x61pacity\x18\x04 \x01(\t\x12\x10\n\x08\x63overage\x18\x05 \x01(\t2?\n\x10WarehouseService\x12+\n\x14warehouseInformation\x12\x06.Empty\x1a\t.Location\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'warehouse_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_EMPTY']._serialized_start=19
  _globals['_EMPTY']._serialized_end=26
  _globals['_LOCATION']._serialized_start=29
  _globals['_LOCATION']._serialized_end=158
  _globals['_LOCATION_TUPLE']._serialized_start=81
  _globals['_LOCATION_TUPLE']._serialized_end=158
  _globals['_WAREHOUSESERVICE']._serialized_start=160
  _globals['_WAREHOUSESERVICE']._serialized_end=223
# @@protoc_insertion_point(module_scope)
