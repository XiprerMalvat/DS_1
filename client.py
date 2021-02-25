#import click

#@click.command()
#@click.option('--option', type=click.Choice(['worker', 'job'], case_sensitive=False), help="Mode selector (worker, job)")
#@click.option('--function', required=False, help="Function to be executed from the option")

#def hello(option, function):
#    """Simple program"""

#    print(option + " " + function)

#if __name__ == '__main__':
#    hello()


import grpc

# import the generated classes
import config_pb2
import config_pb2_grpc

# open a gRPC channel
channel = grpc.insecure_channel('localhost:50051')

# create a stub (client)
stub = config_pb2_grpc.GreeterStub(channel)

# make the call
response = stub.SayHello(config_pb2.HelloRequest(name='you'))

print("Greeter client received: " + response.message)