from protobuf_serialization import serializer, fields

from alvinchow_backend_protobuf.foo_pb2 import (
    Foo
)


class FooSerializer(serializer.ProtobufSerializer):
    protobuf_class = Foo

    id = fields.Field()
    created_at = fields.DateTimeField()
    name = fields.WrappedField()


foo_serializer = FooSerializer()


def serialize_foo(foo):
    return foo_serializer.dump(foo)
