import json
import redis
import time
import ast

REDIS_CONN =  redis.Redis()

def send_job_to_queue(queue, program, url, queueId, resultQueue, fragments):
    data = { 
        'program': program,
        'url': url,
        'queue': queueId,
        'result_queue': resultQueue,
        'fragments' : fragments
    }
    REDIS_CONN.rpush(queue, json.dumps(data))

def send_element_to_add(queue, program, resultQueue, fragments, value):
    data = { 
        'program': program,
        'queue': queue,
        'result_queue': resultQueue,
        'fragments' : fragments,
        'value': value
    }
    REDIS_CONN.rpush(queue, json.dumps(data))

def notify_adder_worker(queue, queueId):
    data = { 
        'queue': queueId
    }
    REDIS_CONN.rpush(queue, json.dumps(data))

def send_response(queue, value):
    data = { 
        'value': value
    }
    REDIS_CONN.rpush(queue, json.dumps(data))

def wait_element_from_queue(queue):
    packed = REDIS_CONN.blpop(queue, 0)
    return json.loads(packed[1])

def get_element_from_queue(queue):
    packed = REDIS_CONN.lpop(queue)
    
    if packed == None:
        return None
    else:
        return ast.literal_eval(packed.decode('utf-8'))
