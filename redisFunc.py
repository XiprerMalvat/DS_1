import json
import redis
import time

REDIS_CONN =  redis.Redis()

def send_job_to_queue(queue, program, url, queueId, resultQueue, fragments):
   data = { 
        'program': program,
        'url': url,
        'queue_id': queueId,
        'result_queue': resultQueue,
        'fragments' : fragments, 
        'time': time.time()
    }
   REDIS_CONN.rpush(queue, json.dumps(data))

def get_job_from_queue(queue):
    packed = REDIS_CONN.blpop([queue], 0)
    return json.loads(packed[1])