# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: alvinchow_service_protobuf/common.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='alvinchow_service_protobuf/common.proto',
  package='alvinchow_service',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\'alvinchow_service_protobuf/common.proto\x12\x11\x61lvinchow_service\"\x17\n\tIdRequest\x12\n\n\x02id\x18\x01 \x01(\x04\"!\n\x0eSimpleResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x62\x06proto3'
)




_IDREQUEST = _descriptor.Descriptor(
  name='IdRequest',
  full_name='alvinchow_service.IdRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='alvinchow_service.IdRequest.id', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=62,
  serialized_end=85,
)


_SIMPLERESPONSE = _descriptor.Descriptor(
  name='SimpleResponse',
  full_name='alvinchow_service.SimpleResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='alvinchow_service.SimpleResponse.success', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=87,
  serialized_end=120,
)

DESCRIPTOR.message_types_by_name['IdRequest'] = _IDREQUEST
DESCRIPTOR.message_types_by_name['SimpleResponse'] = _SIMPLERESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

IdRequest = _reflection.GeneratedProtocolMessageType('IdRequest', (_message.Message,), {
  'DESCRIPTOR' : _IDREQUEST,
  '__module__' : 'alvinchow_service_protobuf.common_pb2'
  # @@protoc_insertion_point(class_scope:alvinchow_service.IdRequest)
  })
_sym_db.RegisterMessage(IdRequest)

SimpleResponse = _reflection.GeneratedProtocolMessageType('SimpleResponse', (_message.Message,), {
  'DESCRIPTOR' : _SIMPLERESPONSE,
  '__module__' : 'alvinchow_service_protobuf.common_pb2'
  # @@protoc_insertion_point(class_scope:alvinchow_service.SimpleResponse)
  })
_sym_db.RegisterMessage(SimpleResponse)


# @@protoc_insertion_point(module_scope)
