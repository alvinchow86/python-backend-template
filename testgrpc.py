#!/usr/bin/env python
import grpc

from alvinchow_backend_protobuf import common_pb2, alvinchow_backend_pb2_grpc


channel = grpc.insecure_channel('localhost:51051')
stub = alvinchow_backend_pb2_grpc.AlvinChowServiceStub(channel)


request = common_pb2.IdRequest(id=1)

response = stub.GetFoo(request)

print(response)
