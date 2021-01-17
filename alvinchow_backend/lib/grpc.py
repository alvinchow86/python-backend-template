import functools

from easydict import EasyDict

from protobuf_serialization import (
    protobuf_to_dict, get_serializer_for_proto_cls,
    serialize_to_protobuf as _serialize_to_protobuf
)
from alvinchow.grpc.utils import create_message_proto_map


proto_package_paths = [
    'alvinchow_backend_protobuf',
    'google.protobuf',
]

message_proto_map = create_message_proto_map(package_paths=proto_package_paths)


def protobuf_to_easydict(proto, **kwargs):
    return protobuf_to_dict(proto, dict_cls=EasyDict, **kwargs)


def create_protobuf(proto_cls, **fields):
    return serialize_to_protobuf(fields, proto_cls)


serialize_to_protobuf = functools.partial(_serialize_to_protobuf, message_proto_map=message_proto_map)
get_serializer_for_proto_cls = functools.partial(
    get_serializer_for_proto_cls, message_proto_map=message_proto_map
)
