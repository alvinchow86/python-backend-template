#!/usr/bin/env python
import grpc

from alvinchow_service_protobuf import common_pb2, alvinchow_service_pb2_grpc


channel = grpc.insecure_channel('localhost:55555')
stub = alvinchow_service_pb2_grpc.AlvinChowServiceStub(channel)


request = common_pb2.IdRequest(id=1)

response = stub.GetFoo(request)

print(response)
