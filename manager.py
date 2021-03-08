import grpc
from concurrent import futures
from multiprocessing import Process, Lock
import time
import config_pb2
import config_pb2_grpc
import json
import redis
import requests

REDDIS_CONN = 0
WORKERS = {}
WORKER_ID = 0

# create a class to define the server functions, derived from
class Comunicator(config_pb2_grpc.ComunicatorServicer):

    def AddWorker(self, request, context):
        create_worker()
        return config_pb2.Reply(message="You added a worker")

    def RemoveWorker(self, request, context):
        global WORKER_ID
        
        for i in range(request.amount):
            terminate_worker(WORKER_ID-1)
            WORKER_ID -= 1
        return config_pb2.Reply(message="You removed "+str(request.amount)+" workers")

    def ListWorker(self, request, context):
        return config_pb2.Reply(message="Workers list: A, B, C")

    def SubmitTask(self, request, context):
        send_job_to_queue(request.programName, request.url)
        return config_pb2.Reply(message="You added this task: "+request.programName+" to "+request.url)

def start_worker(id):
    print(id)
    while True:
        packed = REDDIS_CONN.blpop(['jobsQueue'], 0)
        to_send = json.loads(packed[1])
        print(to_send)

def terminate_worker(id):
    global WORKERS
    global WORKER_ID

    WORKERS[id].terminate()
    del WORKERS[id]

def create_worker():
    global WORKERS
    global WORKER_ID

    proc = Process(target=start_worker, args=(WORKER_ID,))
    proc.start()
    WORKERS[WORKER_ID] = proc


    WORKER_ID += 1

def send_job_to_queue(program, url):
   global REDDIS_CONN

   data = { 
        'program': program,
        'url': url,
        'time': time.time()
    }
   REDDIS_CONN.rpush('jobsQueue', json.dumps(data))

def request_file(url):
    resp = requests.get(url)
    return(resp.text)

if __name__ == '__main__':

    REDDIS_CONN = redis.Redis()

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