# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: order.proto
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
    'order.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0border.proto\"\x0c\n\nOrderEmpty\"{\n\x10OrderInformation\x12*\n\torderInfo\x18\x01 \x03(\x0b\x32\x17.OrderInformation.Tuple\x1a;\n\x05Tuple\x12\n\n\x02id\x18\x01 \x01(\t\x12\t\n\x01x\x18\x02 \x01(\t\x12\t\n\x01y\x18\x03 \x01(\t\x12\x10\n\x08quantity\x18\x04 \x01(\t2D\n\x0cOrderService\x12\x34\n\x10orderInformation\x12\x0b.OrderEmpty\x1a\x11.OrderInformation\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'order_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_ORDEREMPTY']._serialized_start=15
  _globals['_ORDEREMPTY']._serialized_end=27
  _globals['_ORDERINFORMATION']._serialized_start=29
  _globals['_ORDERINFORMATION']._serialized_end=152
  _globals['_ORDERINFORMATION_TUPLE']._serialized_start=93
  _globals['_ORDERINFORMATION_TUPLE']._serialized_end=152
  _globals['_ORDERSERVICE']._serialized_start=154
  _globals['_ORDERSERVICE']._serialized_end=222
# @@protoc_insertion_point(module_scope)
