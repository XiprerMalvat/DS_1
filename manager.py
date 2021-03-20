import redis
from redis.connection import SERVER_CLOSED_CONNECTION_ERROR
import grpc
from concurrent import futures
import time
import config_pb2
import config_pb2_grpc
import worker
import redisFunc
import signal
import sys

REQUEST_ID = 0

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
        return config_pb2.Message(message="Workers list: "+str(worker.WORKERS))

    def SubmitTask(self, request, context):
        global REQUEST_ID
        
        REQUEST_ID += 1
        if len(request.url.split(",")) > 1:
            msg = ""
            for url in request.url.split(","):
                redisFunc.send_job_to_queue('jobsQueue', request.programName, url, "request"+str(REQUEST_ID), "result"+str(REQUEST_ID), len(request.url.split(",")))
        else:
            redisFunc.send_job_to_queue('jobsQueue', request.programName, request.url, "request"+str(REQUEST_ID), "result"+str(REQUEST_ID), 1)

        data = redisFunc.wait_element_from_queue("result"+str(REQUEST_ID))
        REQUEST_ID -= 1
        
        return config_pb2.Message(message=str(data['value']))

def signal_handler(sig, frame):
    print('Terminating process...')
    exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        config_pb2_grpc.add_ComunicatorServicer_to_server(Comunicator(), server)

        redisFunc.REDIS_CONN.flushall()
        print('Starting server. Listening on port 50051.')
        server.add_insecure_port('[::]:50051')
        server.start()
        worker.create_worker()

        try:
            while True:
                time.sleep(86400)
        except KeyboardInterrupt:
            server.stop(0)
    except redis.exceptions.RedisError:
        print("Redis Error:\n\tCould not establish connection with Redis server.")