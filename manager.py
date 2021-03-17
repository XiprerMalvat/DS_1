import grpc
from concurrent import futures
import time
import config_pb2
import config_pb2_grpc
import worker
import redisFunc

global REQUEST_ID = 0

# create a class to define the server functions, derived from
class Comunicator(config_pb2_grpc.ComunicatorServicer):

    def AddWorker(self, request, context):
        worker.create_worker()
        return config_pb2.Message(message="You added a worker")

    def RemoveWorker(self, request, context):       
        for i in range(request.amount):
            worker.terminate_worker()
        return config_pb2.Message(message="You removed "+str(request.amount)+" workers")

    def ListWorker(self, request, context):
        return config_pb2.Message(message="Workers list: "+worker.WORKERS)

    def SubmitTask(self, request, context):
        REQUEST_ID += 1
        # Create return queue
        if len(request.url.split(",")) > 1:
            msg = ""
            # Create add queue
            for url in request.url[1:-1].split(","):
                result = redisFunc.send_job_to_queue('jobsQueue', request.programName, url, "request"+REQUEST_ID, "result"+REQUEST_ID, len(request.url.split(",")))
                msg = msg+"You added this task: "+request.programName+" to "+url+"\n Result: "+result+"\n"
        else:
            result = redisFunc.send_job_to_queue('jobsQueue', request.programName, url)
        # Wait return queue
        REQUEST_ID -= 1
        return config_pb2.Message(message="You added this task: "+request.programName+" to "+url+"\n Result: "+result)

if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    config_pb2_grpc.add_ComunicatorServicer_to_server(Comunicator(), server)

    print('Starting server. Listening on port 50051.')
    server.add_insecure_port('[::]:50051')
    server.start()

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)