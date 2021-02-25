import grpc
from concurrent import futures
import time

# import the generated classes
import config_pb2
import config_pb2_grpc

# create a class to define the server functions, derived from
# config_pb2_grpc.CalculatorServicer
class Greeter(config_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        return config_pb2.HelloReply(message='Hello, %s!' % request.name)

    def SayHelloAgain(self, request, context):
        return config_pb2.HelloReply(message='Hello again, %s!' % request.name)


# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# use the generated function `add_CalculatorServicer_to_server`
# to add the defined class to the server
config_pb2_grpc.add_GreeterServicer_to_server(
        Greeter(), server)

# listen on port 50051
print('Starting server. Listening on port 50051.')
server.add_insecure_port('[::]:50051')
server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)