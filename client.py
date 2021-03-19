import click
import grpc
import config_pb2
import config_pb2_grpc
import re

@click.command()
@click.option('--option', '-o', required=True, type=click.Choice(['worker', 'job'], case_sensitive=False), help="Mode selector (worker, job)")
@click.option('--function', '-f', required=True, type=click.Choice(['create', 'delete','list','run-countwords','run-wordcount']), help="Function to be executed from the option")
@click.option('--args', '-a', metavar='', required=False, help="Necessary arguments to execute the function (can be null)")

def main(option, function, args):
    """Program main"""

    channel = grpc.insecure_channel('localhost:50051')      # open a gRPC channel
    stub = config_pb2_grpc.ComunicatorStub(channel)         # create a stub (client)

    if option == "worker":
        if function == "create":
            response = stub.AddWorker(config_pb2.Message(message=""))
            print(response.message)
        elif function == "delete":
            response = stub.RemoveWorker(config_pb2.Number(amount=int(args)))
            print(response.message)
        elif function == "list":
            response = stub.ListWorker(config_pb2.Message(message=""))
            print(response.message)
        else:
            print("Invalid function.")
    elif option == "job":
        if function == "run-countwords" or function == "run-wordcount":
            pattern = re.compile(r'^\[http:\/\/[^\[\]?]*\]$')           # [http://url1,http://url2]
            if args == None or not pattern.match(args):
                print("Invalid arguments")
            else:
                response = stub.SubmitTask(config_pb2.Job(programName=function[4:], url=args[1:-1]))
                print(response.message)
        else:
            print("Invalid option.")
    else:
        print("Not acceptable option")

if __name__ == '__main__':
    main()
